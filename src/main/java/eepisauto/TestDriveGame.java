package eepisauto;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Random;
import java.util.function.Consumer;
import javafx.animation.AnimationTimer;
import javafx.application.Platform;
import javafx.geometry.VPos;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.input.KeyCode;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.TextAlignment;

/**
 * Mini game Test Drive: pindah jalur untuk menghindari lalu lintas dan mengumpulkan koin.
 * Karakter mobil (akselerasi &amp; top speed) bergantung pada tipe Vehicle (EV vs Bensin).
 *
 * Kontrol: Panah Kiri/Kanan atau A/D, klik sisi kiri/kanan arena, Esc untuk keluar.
 */
public class TestDriveGame extends StackPane {

    /** Hasil akhir sesi test drive. */
    public static class Result {
        public final int score, coins, topSpeedKmh, livesLeft;
        public final double distanceMeters;
        public final boolean survived; // bertahan sampai waktu habis
        public final boolean aborted;  // pemain keluar sebelum selesai

        Result(int score, int coins, int topSpeedKmh, int livesLeft, double distanceMeters, boolean survived, boolean aborted) {
            this.score = score; this.coins = coins; this.topSpeedKmh = topSpeedKmh; this.livesLeft = livesLeft;
            this.distanceMeters = distanceMeters; this.survived = survived; this.aborted = aborted;
        }
    }

    // ---- Dimensi arena ----
    private static final double W = 640, H = 400;
    private static final int LANES = 3;
    private static final double LANE_W = 96;
    private static final double ROAD_W = LANE_W * LANES;
    private static final double ROAD_X = (W - ROAD_W) / 2;
    private static final double CAR_W = 44, CAR_H = 76;
    private static final double PLAYER_Y = H - CAR_H - 26;
    private static final double DURATION = 30;      // detik
    private static final double KMH_PER_PX = 0.32;  // konversi kecepatan layar -> km/h
    private static final int MAX_LIVES = 3;

    // ---- Palet ----
    private static final Color SIDE = Color.web("#f1f5f9");
    private static final Color ROAD = Color.web("#334155");
    private static final Color TEXT = Color.web("#0f172a");
    private static final Color MUTED = Color.web("#64748b");
    private static final Color ACCENT = Color.web("#4f46e5");
    private static final Color[] TRAFFIC = {
        Color.web("#94a3b8"), Color.web("#22c55e"), Color.web("#0ea5e9"),
        Color.web("#eab308"), Color.web("#e11d48"), Color.web("#a855f7"), Color.web("#e2e8f0")
    };

    private static class Entity {
        int lane; double y; boolean coin; Color color;
    }

    private final Vehicle car;
    private final boolean electric;
    private final Consumer<Result> onFinish;
    private final Canvas canvas = new Canvas(W, H);
    private final GraphicsContext g = canvas.getGraphicsContext2D();
    private final Random rnd = new Random();
    private final List<Entity> entities = new ArrayList<>();
    private final AnimationTimer timer;

    // Karakter mobil
    private final double accel, maxSpeed;
    private final Color playerColor;

    // State
    private long lastNanos;
    private double countdown, goFlash, timeLeft, speed, roadOffset, spawnTimer, invuln, shake, playerX, score, distance;
    private int targetLane, lives, coins, topSpeed;
    private boolean done;

    public TestDriveGame(Vehicle car, Consumer<Result> onFinish) {
        this.car = car;
        this.onFinish = onFinish;
        this.electric = car instanceof ElectricCar;
        // EV: torsi instan (akselerasi tinggi). Bensin: top speed lebih tinggi.
        this.accel = electric ? 42 : 30;
        this.maxSpeed = electric ? 640 : 720;
        this.playerColor = electric ? Color.web("#6366f1") : Color.web("#f97316");

        getChildren().add(canvas);
        setPrefSize(W, H);
        setMaxSize(W, H);
        setMinSize(W, H);
        Rectangle clip = new Rectangle(W, H);
        clip.setArcWidth(24); clip.setArcHeight(24);
        setClip(clip);
        setFocusTraversable(true);

        setOnKeyPressed(e -> {
            KeyCode k = e.getCode();
            if (k == KeyCode.LEFT || k == KeyCode.A) { steer(-1); e.consume(); }
            else if (k == KeyCode.RIGHT || k == KeyCode.D) { steer(1); e.consume(); }
            else if (k == KeyCode.ESCAPE) { abort(); e.consume(); }
        });
        setOnMousePressed(e -> {
            requestFocus();
            steer(e.getX() < W / 2 ? -1 : 1);
        });

        timer = new AnimationTimer() {
            @Override public void handle(long now) {
                if (lastNanos == 0) { lastNanos = now; return; }
                double dt = Math.min(0.05, (now - lastNanos) / 1e9);
                lastNanos = now;
                update(dt);
                render();
            }
        };

        // Hentikan loop jika node dilepas dari scene
        sceneProperty().addListener((obs, o, n) -> { if (n == null) timer.stop(); });
    }

    /** Mulai (atau ulang) permainan. */
    public void start() {
        entities.clear();
        countdown = 3; goFlash = 0; timeLeft = DURATION; speed = 160; roadOffset = 0;
        spawnTimer = 0.6; invuln = 0; shake = 0; score = 0; distance = 0;
        targetLane = 1; playerX = laneX(1); lives = MAX_LIVES; coins = 0; topSpeed = 0;
        done = false; lastNanos = 0;
        render();
        timer.start();
        Platform.runLater(this::requestFocus);
    }

    /** Keluar dari permainan tanpa hasil (memanggil callback dengan aborted=true). */
    public void abort() {
        if (done) return;
        finish(false, true);
    }

    /** Hentikan loop secara diam-diam tanpa memanggil callback. */
    public void dispose() {
        done = true;
        timer.stop();
    }

    // ------------------------------------------------------------------ logic

    private boolean isPlaying() { return !done && countdown <= 0; }

    private void steer(int dir) {
        if (!isPlaying()) return;
        targetLane = Math.max(0, Math.min(LANES - 1, targetLane + dir));
    }

    private static double laneX(int lane) { return ROAD_X + LANE_W * lane + LANE_W / 2; }

    private void update(double dt) {
        if (done) return;
        if (shake > 0) shake -= dt;
        if (goFlash > 0) goFlash -= dt;

        if (countdown > 0) {
            countdown -= dt;
            if (countdown <= 0) goFlash = 0.7;
            return;
        }

        timeLeft -= dt;
        if (timeLeft <= 0) { timeLeft = 0; finish(true, false); return; }

        speed = Math.min(maxSpeed, speed + accel * dt);
        int kmh = (int) (speed * KMH_PER_PX);
        topSpeed = Math.max(topSpeed, kmh);
        distance += kmh / 3.6 * dt;
        score += speed * dt * 0.05;
        roadOffset += speed * dt;
        if (invuln > 0) invuln -= dt;

        playerX += (laneX(targetLane) - playerX) * Math.min(1, dt * 14);

        // Spawn lalu lintas & koin
        spawnTimer -= dt;
        if (spawnTimer <= 0) {
            int carLane = rnd.nextInt(LANES);
            Entity c = new Entity();
            c.lane = carLane; c.y = -CAR_H; c.color = TRAFFIC[rnd.nextInt(TRAFFIC.length)];
            entities.add(c);
            if (rnd.nextDouble() < 0.45) {
                Entity coin = new Entity();
                coin.lane = (carLane + 1 + rnd.nextInt(LANES - 1)) % LANES;
                coin.y = -CAR_H; coin.coin = true;
                entities.add(coin);
            }
            spawnTimer = Math.max(0.42, 1.1 - (speed - 160) / 900);
        }

        double move = speed * 0.55 * dt;
        double px = playerX - CAR_W / 2 + 5, py = PLAYER_Y + 6, pw = CAR_W - 10, ph = CAR_H - 12;
        Iterator<Entity> it = entities.iterator();
        while (it.hasNext()) {
            Entity e = it.next();
            e.y += move;
            if (e.y > H + 20) { it.remove(); continue; }

            double ex, ey, ew, eh;
            if (e.coin) { ex = laneX(e.lane) - 12; ey = e.y + CAR_H / 2 - 12; ew = 24; eh = 24; }
            else { ex = laneX(e.lane) - CAR_W / 2 + 3; ey = e.y + 3; ew = CAR_W - 6; eh = CAR_H - 6; }

            boolean hit = px < ex + ew && px + pw > ex && py < ey + eh && py + ph > ey;
            if (!hit) continue;

            if (e.coin) {
                coins++; score += 25; it.remove();
            } else if (invuln <= 0) {
                lives--; invuln = 1.4; shake = 0.35;
                speed = Math.max(160, speed * 0.6);
                it.remove();
                if (lives <= 0) { finish(false, false); return; }
            }
        }
    }

    private void finish(boolean survived, boolean aborted) {
        done = true;
        timer.stop();
        render();
        Result r = new Result((int) score, coins, topSpeed, Math.max(0, lives), distance, survived, aborted);
        Platform.runLater(() -> onFinish.accept(r));
    }

    // ---------------------------------------------------------------- render

    private void render() {
        g.save();
        if (shake > 0) g.translate((rnd.nextDouble() - 0.5) * 10, (rnd.nextDouble() - 0.5) * 10);

        // Sisi jalan
        g.setFill(SIDE);
        g.fillRect(-10, -10, W + 20, H + 20);
        drawTrees();

        // Jalan
        g.setFill(ROAD);
        g.fillRect(ROAD_X, -10, ROAD_W, H + 20);
        g.setFill(Color.web("#f8fafc"));
        g.fillRect(ROAD_X + 4, -10, 3, H + 20);
        g.fillRect(ROAD_X + ROAD_W - 7, -10, 3, H + 20);

        g.setFill(Color.rgb(255, 255, 255, 0.55));
        double period = 44, off = roadOffset % period;
        for (int l = 1; l < LANES; l++) {
            double x = ROAD_X + LANE_W * l - 2;
            for (double y = -period + off; y < H; y += period) g.fillRoundRect(x, y, 4, 24, 4, 4);
        }

        // Entitas
        for (Entity e : entities) {
            if (e.coin) drawCoin(laneX(e.lane), e.y + CAR_H / 2);
            else drawCar(laneX(e.lane), e.y, e.color, false);
        }

        // Pemain (berkedip saat kebal)
        boolean blinkHidden = invuln > 0 && ((int) (invuln * 10)) % 2 == 0;
        if (!blinkHidden) drawCar(playerX, PLAYER_Y, playerColor, true);

        g.restore();

        drawHud();

        if (shake > 0) {
            g.setFill(Color.rgb(220, 38, 38, 0.18 * (shake / 0.35)));
            g.fillRect(0, 0, W, H);
        }
        if (countdown > 0 && !done) drawCountdown();
        else if (goFlash > 0) drawCenterText("GO!", Color.rgb(255, 255, 255, Math.min(1, goFlash * 2)), 64);
    }

    private void drawTrees() {
        double spacing = 70;
        double off = roadOffset % spacing;
        for (int i = -1; i < H / spacing + 2; i++) {
            double y = i * spacing + off;
            // Variasi posisi berbasis index absolut agar pohon stabil saat scroll
            long idx = (long) Math.floor((roadOffset - off) / spacing) - i;
            drawTree(ROAD_X - 18 - Math.floorMod(idx * 37, 9), y);
            drawTree(ROAD_X + ROAD_W + 18 + Math.floorMod(idx * 53, 9), y + 30);
        }
    }

    private void drawTree(double x, double y) {
        g.setFill(Color.rgb(15, 23, 42, 0.06));
        g.fillOval(x - 12, y + 6, 26, 10);
        g.setFill(Color.web("#86efac"));
        g.fillOval(x - 12, y - 12, 24, 24);
        g.setFill(Color.web("#4ade80"));
        g.fillOval(x - 7, y - 9, 13, 13);
    }

    private void drawCar(double cx, double y, Color body, boolean player) {
        double x = cx - CAR_W / 2;
        // bayangan
        g.setFill(Color.rgb(0, 0, 0, 0.25));
        g.fillRoundRect(x + 3, y + 5, CAR_W, CAR_H, 16, 16);
        // roda
        g.setFill(Color.web("#0f172a"));
        g.fillRoundRect(x - 3, y + 12, 6, 16, 3, 3);
        g.fillRoundRect(x + CAR_W - 3, y + 12, 6, 16, 3, 3);
        g.fillRoundRect(x - 3, y + CAR_H - 26, 6, 16, 3, 3);
        g.fillRoundRect(x + CAR_W - 3, y + CAR_H - 26, 6, 16, 3, 3);
        // bodi
        g.setFill(body);
        g.fillRoundRect(x, y, CAR_W, CAR_H, 16, 16);
        // kaca
        g.setFill(Color.rgb(15, 23, 42, 0.78));
        g.fillRoundRect(x + 6, y + 18, CAR_W - 12, 15, 6, 6);
        g.fillRoundRect(x + 7, y + CAR_H - 20, CAR_W - 14, 9, 5, 5);
        // atap
        g.setFill(Color.rgb(255, 255, 255, 0.18));
        g.fillRoundRect(x + 8, y + 36, CAR_W - 16, 18, 6, 6);
        // lampu
        g.setFill(player ? Color.web("#fef9c3") : Color.rgb(255, 255, 255, 0.7));
        g.fillRoundRect(x + 5, y + 2, 9, 4, 3, 3);
        g.fillRoundRect(x + CAR_W - 14, y + 2, 9, 4, 3, 3);
        if (player) {
            g.setFill(Color.web("#ef4444"));
            g.fillRoundRect(x + 5, y + CAR_H - 5, 9, 3, 2, 2);
            g.fillRoundRect(x + CAR_W - 14, y + CAR_H - 5, 9, 3, 2, 2);
            if (electric) { // garis aksen EV
                g.setFill(Color.rgb(255, 255, 255, 0.85));
                g.fillRect(cx - 1.5, y + 6, 3, 10);
            }
        }
    }

    private void drawCoin(double cx, double cy) {
        g.setFill(Color.rgb(0, 0, 0, 0.2));
        g.fillOval(cx - 11, cy - 8, 24, 24);
        g.setFill(Color.web("#f59e0b"));
        g.fillOval(cx - 12, cy - 12, 24, 24);
        g.setFill(Color.web("#fcd34d"));
        g.fillOval(cx - 8, cy - 8, 16, 16);
        g.setFill(Color.web("#b45309"));
        g.setFont(Font.font("System", FontWeight.BOLD, 11));
        g.setTextAlign(TextAlignment.CENTER);
        g.setTextBaseline(VPos.CENTER);
        g.fillText("$", cx, cy);
    }

    private void drawHud() {
        g.setTextBaseline(VPos.TOP);

        // ---- Panel kiri: speedometer & nyawa ----
        double lx = 20;
        g.setTextAlign(TextAlignment.LEFT);
        g.setFill(MUTED);
        g.setFont(Font.font("System", FontWeight.BOLD, 11));
        g.fillText("KECEPATAN", lx, 22);
        g.setFill(TEXT);
        g.setFont(Font.font("System", FontWeight.BOLD, 34));
        g.fillText(String.valueOf(countdown > 0 ? 0 : (int) (speed * KMH_PER_PX)), lx, 36);
        g.setFill(MUTED);
        g.setFont(Font.font("System", FontWeight.NORMAL, 12));
        g.fillText("km/h", lx, 76);

        // bar kecepatan
        double ratio = countdown > 0 ? 0 : speed / maxSpeed;
        g.setFill(Color.web("#e2e8f0"));
        g.fillRoundRect(lx, 98, 120, 6, 6, 6);
        g.setFill(ACCENT);
        g.fillRoundRect(lx, 98, 120 * ratio, 6, 6, 6);

        g.setFill(MUTED);
        g.setFont(Font.font("System", FontWeight.BOLD, 11));
        g.fillText("NYAWA", lx, 124);
        for (int i = 0; i < MAX_LIVES; i++) {
            g.setFill(i < lives ? Color.web("#ef4444") : Color.web("#e2e8f0"));
            drawHeart(lx + i * 24 + 9, 148);
        }

        g.setFill(MUTED);
        g.setFont(Font.font("System", FontWeight.BOLD, 11));
        g.fillText(electric ? "MODE EV" : "MODE BENSIN", lx, H - 58);
        g.setFill(TEXT);
        g.setFont(Font.font("System", FontWeight.NORMAL, 12));
        g.fillText(electric ? "Akselerasi instan" : "Top speed tinggi", lx, H - 42);

        // ---- Panel kanan: skor, waktu, koin ----
        double rx = W - 20;
        g.setTextAlign(TextAlignment.RIGHT);
        g.setFill(MUTED);
        g.setFont(Font.font("System", FontWeight.BOLD, 11));
        g.fillText("SKOR", rx, 22);
        g.setFill(TEXT);
        g.setFont(Font.font("System", FontWeight.BOLD, 34));
        g.fillText(String.valueOf((int) score), rx, 36);

        g.setFill(MUTED);
        g.setFont(Font.font("System", FontWeight.BOLD, 11));
        g.fillText("WAKTU", rx, 98);
        g.setFill(TEXT);
        g.setFont(Font.font("System", FontWeight.BOLD, 20));
        g.fillText(String.format("0:%02d", (int) Math.ceil(timeLeft)), rx, 112);
        g.setFill(Color.web("#e2e8f0"));
        g.fillRoundRect(rx - 120, 142, 120, 6, 6, 6);
        g.setFill(Color.web("#16a34a"));
        double tw = 120 * (timeLeft / DURATION);
        g.fillRoundRect(rx - tw, 142, tw, 6, 6, 6);

        g.setFill(MUTED);
        g.setFont(Font.font("System", FontWeight.BOLD, 11));
        g.fillText("KOIN", rx, 166);
        g.setFill(Color.web("#d97706"));
        g.setFont(Font.font("System", FontWeight.BOLD, 20));
        g.fillText("× " + coins, rx, 180);

        g.setFill(MUTED);
        g.setFont(Font.font("System", FontWeight.BOLD, 11));
        g.fillText("JARAK", rx, H - 58);
        g.setFill(TEXT);
        g.setFont(Font.font("System", FontWeight.NORMAL, 12));
        g.fillText(String.format("%.0f m", distance), rx, H - 42);
    }

    private void drawHeart(double cx, double cy) {
        g.fillOval(cx - 9, cy - 7, 10, 10);
        g.fillOval(cx - 1, cy - 7, 10, 10);
        g.fillPolygon(new double[]{cx - 9, cx + 9, cx}, new double[]{cy - 1, cy - 1, cy + 9}, 3);
    }

    private void drawCountdown() {
        g.setFill(Color.rgb(15, 23, 42, 0.45));
        g.fillRect(0, 0, W, H);
        drawCenterText(String.valueOf((int) Math.ceil(countdown)), Color.WHITE, 84);
        g.setTextAlign(TextAlignment.CENTER);
        g.setTextBaseline(VPos.CENTER);
        g.setFill(Color.rgb(255, 255, 255, 0.9));
        g.setFont(Font.font("System", FontWeight.NORMAL, 14));
        g.fillText("← →  atau  A / D  untuk pindah jalur", W / 2, H / 2 + 64);
        g.fillText("Hindari mobil lain · Kumpulkan koin · Bertahan 30 detik", W / 2, H / 2 + 86);
        g.setFont(Font.font("System", FontWeight.BOLD, 16));
        g.fillText(car.getBrand() + " " + car.getModel(), W / 2, H / 2 - 70);
    }

    private void drawCenterText(String text, Color color, double size) {
        g.setTextAlign(TextAlignment.CENTER);
        g.setTextBaseline(VPos.CENTER);
        g.setFont(Font.font("System", FontWeight.BOLD, size));
        g.setFill(Color.rgb(0, 0, 0, 0.25 * color.getOpacity()));
        g.fillText(text, W / 2 + 2, H / 2 + 3);
        g.setFill(color);
        g.fillText(text, W / 2, H / 2);
    }
}
