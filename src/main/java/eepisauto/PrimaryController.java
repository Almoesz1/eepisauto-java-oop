package eepisauto;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import javafx.animation.*;
import javafx.fxml.FXML;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.chart.*;
import javafx.scene.control.*;
import javafx.scene.effect.BoxBlur;
import javafx.scene.layout.*;
import javafx.util.Duration;

public class PrimaryController {

    @FXML private BorderPane mainAppPane;
    @FXML private StackPane loginOverlay, modalOverlay;
    @FXML private VBox modalBox, receiptBox;
    @FXML private TextField txtNama, txtSaldo, txtSearch;
    @FXML private ComboBox<String> comboFilter;
    
    // Sidebar & Pages
    @FXML private Button btnNavShowroom, btnNavGarasi, btnNavServis, btnNavPajak, btnNavTradeIn, btnNavRiwayat, btnNavRewards;
    @FXML private VBox pageShowroom, pageGarasi, pageServis, pagePajak, pageTradeIn, pageRiwayat, pageRewards;
    
    // UI Elements
    @FXML private Label lblSidebarUser, lblSidebarTier, lblSidebarSaldo, lblSidebarAvatar;
    @FXML private Label lblTotalUnit, lblTotalAset, lblSummaryPajak; // Summary Garasi
    @FXML private Label lblHargaJual, lblTotalPajak, lblTierReward;
    @FXML private FlowPane showroomContainer;
    @FXML private VBox garasiContainer;
    @FXML private ListView<String> listServis, listPajak, listTradeIn, listRiwayat;
    @FXML private Button btnKlaimReward;
    
    // Chart
    @FXML private BarChart<String, Number> chartAset;
    @FXML private CategoryAxis xAxis;
    @FXML private NumberAxis yAxis;

    // Modal
    @FXML private Label lblModalTitle, lblModalDesc, lblToast;
    @FXML private ProgressBar progressBar;
    @FXML private Button btnCloseTestDrive;
    @FXML private TextArea txtReceiptContent;
    @FXML private HBox toastPane;

    // Mini Game Test Drive
    @FXML private VBox gameBox;
    @FXML private StackPane gameHost, resultOverlay;
    @FXML private Label lblGameTitle, lblGameSubtitle;
    @FXML private Label lblResultTitle, lblResultQuote, lblResultScore, lblResultSpeed, lblResultCoins, lblResultBest;
    @FXML private Button btnGameBuy;

    private static final double REWARD_PER_COIN = 100000.0;

    private ArrayList<Vehicle> showroom = new ArrayList<>();
    private Customer currentUser;
    private List<String> transactionHistory = new ArrayList<>();
    private boolean hasClaimedReward = false; 

    private TestDriveGame activeGame;
    private Vehicle gameCar;
    private final Map<Vehicle, Integer> bestScores = new HashMap<>();
    private SequentialTransition toastAnim;

    @FXML
    public void initialize() {
        showroom.add(new ElectricCar("Porsche", "Taycan Turbo S", 2500000000.0, 3, "Carrera White", 93, 500));
        showroom.add(new GasCar("BMW", "M3 Competition", 2300000000.0, 2, "Isle of Man Green", 3000, "8-Speed Auto"));
        showroom.add(new GasCar("Mercedes", "AMG G63", 6500000000.0, 1, "Obsidian Black", 4000, "9-Speed AT"));
        showroom.add(new ElectricCar("Tesla", "Model S Plaid", 3000000000.0, 2, "Solid Black", 100, 600));
        showroom.add(new ElectricCar("Hyundai", "Ioniq 5 N", 1300000000.0, 5, "Performance Blue", 84, 450));
        showroom.add(new GasCar("Honda", "Civic Type R", 1400000000.0, 2, "Championship White", 2000, "6-Speed MT"));
        showroom.add(new GasCar("Toyota", "GR Yaris", 850000000.0, 4, "Emotional Red", 1600, "6-Speed MT"));

        comboFilter.getItems().addAll("Semua Tipe", "Khusus Listrik (EV)", "Khusus Bensin (Gas)", "Harga < 2 Miliar", "Harga > 2 Miliar");
        comboFilter.getSelectionModel().selectFirst();
        
        txtSearch.textProperty().addListener((obs, oldV, newV) -> renderShowroomCards());
        comboFilter.valueProperty().addListener((obs, oldV, newV) -> renderShowroomCards());
        
        listTradeIn.getSelectionModel().selectedIndexProperty().addListener((obs, oldV, newV) -> {
            if (newV.intValue() >= 0 && !currentUser.garage.isEmpty()) {
                double jual = currentUser.garage.get(newV.intValue()).getPrice() * 0.7; 
                lblHargaJual.setText("Rp " + String.format("%,.0f", jual));
            }
        });

        listServis.setPlaceholder(placeholder("Garasi masih kosong"));
        listPajak.setPlaceholder(placeholder("Belum ada kendaraan untuk dihitung"));
        listTradeIn.setPlaceholder(placeholder("Belum ada kendaraan untuk dijual"));
        listRiwayat.setPlaceholder(placeholder("Belum ada transaksi"));
    }

    private Label placeholder(String text) {
        Label l = new Label(text);
        l.getStyleClass().add("empty-state");
        return l;
    }

    @FXML
    private void handleVerifikasi() {
        try {
            String nama = txtNama.getText().trim();
            double saldo = Double.parseDouble(txtSaldo.getText().trim());
            if (nama.isEmpty()) { showToast("Nama wajib diisi", true); return; }

            String nrp = "3125600065";
            if (saldo >= 3000000000.0) currentUser = new GoldCustomer(nrp, nama, saldo);
            else if (saldo >= 1000000000.0) currentUser = new SilverCustomer(nrp, nama, saldo);
            else currentUser = new RegularCustomer(nrp, nama, saldo);

            updateSemuaData();
            
            FadeTransition ftOut = new FadeTransition(Duration.millis(500), loginOverlay);
            ftOut.setToValue(0); ftOut.setOnFinished(e -> loginOverlay.setVisible(false));
            FadeTransition ftIn = new FadeTransition(Duration.millis(700), mainAppPane);
            ftIn.setToValue(1);
            ftOut.play(); ftIn.play();
            showToast("Selamat datang, " + nama + " · " + currentUser.getTierName(), false);

        } catch (NumberFormatException e) {
            showToast("Format saldo salah, masukkan angka saja", true);
        }
    }

    private void renderShowroomCards() {
        showroomContainer.getChildren().clear();
        String search = txtSearch.getText().toLowerCase();
        String filter = comboFilter.getValue();

        List<Vehicle> filteredList = showroom.stream()
            .filter(c -> c.getBrand().toLowerCase().contains(search) || c.getModel().toLowerCase().contains(search))
            .filter(c -> {
                if (filter.equals("Khusus Listrik (EV)")) return c instanceof ElectricCar;
                if (filter.equals("Khusus Bensin (Gas)")) return c instanceof GasCar;
                if (filter.equals("Harga < 2 Miliar")) return c.getPrice() < 2000000000.0;
                if (filter.equals("Harga > 2 Miliar")) return c.getPrice() >= 2000000000.0;
                return true;
            }).collect(Collectors.toList());

        if (filteredList.isEmpty()) {
            showroomContainer.getChildren().add(placeholder("Tidak ada kendaraan yang cocok dengan pencarian."));
            return;
        }

        for (Vehicle car : filteredList) {
            boolean ev = car instanceof ElectricCar;
            VBox card = new VBox(14);
            card.getStyleClass().add("car-card");
            card.setPrefWidth(280);
            card.setPadding(new Insets(14));

            // Header visual
            StackPane imagePane = new StackPane();
            imagePane.getStyleClass().add(ev ? "car-img-ev" : "car-img-gas");
            Label brandLogo = new Label(car.getBrand().toUpperCase());
            brandLogo.getStyleClass().add(ev ? "car-brand-ev" : "car-brand-gas");
            Label typePill = new Label(ev ? "ELECTRIC" : "GASOLINE");
            typePill.getStyleClass().addAll("pill", ev ? "pill-ev" : "pill-gas");
            StackPane.setAlignment(typePill, Pos.TOP_LEFT);
            StackPane.setMargin(typePill, new Insets(12));
            imagePane.getChildren().addAll(brandLogo, typePill);

            // Teks
            VBox textPane = new VBox(4);
            textPane.setPadding(new Insets(0, 4, 0, 4));
            Label title = new Label(car.getBrand() + " " + car.getModel());
            title.getStyleClass().add("car-title");
            Label specs = new Label(car.getSpecs());
            specs.getStyleClass().add("text-subtitle");
            specs.setStyle("-fx-font-size: 12px;");
            specs.setWrapText(true);
            HBox priceRow = new HBox();
            priceRow.setAlignment(Pos.BOTTOM_LEFT);
            priceRow.setPadding(new Insets(8, 0, 0, 0));
            Label price = new Label(String.format("Rp %,.0f", car.getPrice()));
            price.getStyleClass().add("car-price");
            Region spacer = new Region(); HBox.setHgrow(spacer, Priority.ALWAYS);
            Label stock = new Label(car.getStock() > 0 ? "Stok " + car.getStock() : "Habis");
            stock.getStyleClass().add("car-stock");
            if (car.getStock() <= 0) stock.setStyle("-fx-text-fill: #dc2626;");
            priceRow.getChildren().addAll(price, spacer, stock);
            textPane.getChildren().addAll(title, specs, priceRow);

            // Aksi
            HBox actions = new HBox(10);
            Button btnDrive = new Button("Test Drive");
            btnDrive.getStyleClass().add("btn-secondary"); btnDrive.setMaxWidth(Double.MAX_VALUE); HBox.setHgrow(btnDrive, Priority.ALWAYS);
            btnDrive.setOnAction(e -> triggerTestDrive(car));
            
            Button btnBuy = new Button("Beli");
            btnBuy.getStyleClass().add("btn-primary"); btnBuy.setMaxWidth(Double.MAX_VALUE); HBox.setHgrow(btnBuy, Priority.ALWAYS);
            btnBuy.setOnAction(e -> triggerBeli(car));
            btnBuy.setDisable(car.getStock() <= 0);
            
            actions.getChildren().addAll(btnDrive, btnBuy);
            card.getChildren().addAll(imagePane, textPane, actions);

            // Hover lift halus
            TranslateTransition up = new TranslateTransition(Duration.millis(150), card); up.setToY(-3);
            TranslateTransition down = new TranslateTransition(Duration.millis(150), card); down.setToY(0);
            card.setOnMouseEntered(e -> { down.stop(); up.playFromStart(); });
            card.setOnMouseExited(e -> { up.stop(); down.playFromStart(); });

            showroomContainer.getChildren().add(card);
        }
    }

    private void renderGarasiCards() {
        garasiContainer.getChildren().clear();
        if (currentUser.garage.isEmpty()) {
            garasiContainer.getChildren().add(placeholder("Belum ada kendaraan. Kunjungi Showroom untuk membeli."));
            return;
        }
        int counter = 1;
        for (Vehicle car : currentUser.garage) {
            HBox card = new HBox(14);
            card.setAlignment(Pos.CENTER_LEFT);
            card.getStyleClass().add("asset-card");
            
            Label noLabel = new Label(String.format("%02d", counter++));
            noLabel.getStyleClass().add("asset-no");
            noLabel.setMinWidth(Region.USE_PREF_SIZE);
            
            VBox infoBox = new VBox(3);
            HBox.setHgrow(infoBox, Priority.ALWAYS);
            Label title = new Label(car.getBrand() + " " + car.getModel());
            title.getStyleClass().add("text-h2");
            title.setStyle("-fx-font-size: 15px;");
            Label specs = new Label(car.getSpecs() + "  ·  " + car.getColor());
            specs.getStyleClass().add("text-subtitle");
            specs.setStyle("-fx-font-size: 12px;");
            infoBox.getChildren().addAll(title, specs);
            
            VBox priceBox = new VBox(4);
            priceBox.setAlignment(Pos.CENTER_RIGHT);
            Label status = new Label("LUNAS");
            status.getStyleClass().addAll("pill", "pill-success");
            Label price = new Label("Rp " + String.format("%,.0f", car.getPrice()));
            price.setStyle("-fx-font-size: 14px; -fx-font-weight: bold;");
            price.setMinWidth(Region.USE_PREF_SIZE);
            priceBox.setMinWidth(Region.USE_PREF_SIZE);
            priceBox.getChildren().addAll(status, price);

            card.getChildren().addAll(noLabel, infoBox, priceBox);
            garasiContainer.getChildren().add(card);
        }
    }

    // =============================================================== TEST DRIVE (MINI GAME)

    private void triggerTestDrive(Vehicle car) {
        gameCar = car;
        mainAppPane.setEffect(new BoxBlur(8, 8, 2));
        modalOverlay.setVisible(true);
        modalBox.setVisible(false); receiptBox.setVisible(false);
        gameBox.setVisible(true);

        boolean ev = car instanceof ElectricCar;
        lblGameTitle.setText("Test Drive · " + car.getBrand() + " " + car.getModel());
        lblGameSubtitle.setText((ev ? "Mode EV: akselerasi instan" : "Mode Bensin: top speed lebih tinggi")
                + "  ·  Bonus Rp " + String.format("%,.0f", REWARD_PER_COIN) + " per koin");

        startNewGame();

        gameBox.setOpacity(0); gameBox.setScaleX(0.96); gameBox.setScaleY(0.96);
        FadeTransition fade = new FadeTransition(Duration.millis(220), gameBox); fade.setToValue(1);
        ScaleTransition scale = new ScaleTransition(Duration.millis(220), gameBox); scale.setToX(1); scale.setToY(1);
        new ParallelTransition(fade, scale).play();
    }

    private void startNewGame() {
        if (activeGame != null) { activeGame.dispose(); gameHost.getChildren().remove(activeGame); }
        resultOverlay.setVisible(false);
        activeGame = new TestDriveGame(gameCar, this::onGameFinished);
        gameHost.getChildren().add(0, activeGame); // di bawah kartu hasil
        activeGame.start();
    }

    private void onGameFinished(TestDriveGame.Result r) {
        if (r.aborted) { // Esc / tombol keluar
            if (gameBox.isVisible()) closeGame();
            return;
        }

        lblResultTitle.setText(r.survived ? "Test Drive Selesai!" : "Mobil Rusak!");
        lblResultQuote.setText("\u201C" + gameCar.testDrive() + "\u201D"); // POLIMORFISME
        lblResultScore.setText(String.valueOf(r.score));
        lblResultSpeed.setText(r.topSpeedKmh + " km/h");
        lblResultCoins.setText(String.valueOf(r.coins));

        int best = bestScores.getOrDefault(gameCar, 0);
        boolean newBest = r.score > best;
        if (newBest) bestScores.put(gameCar, r.score);

        String info = newBest ? "Rekor baru untuk mobil ini!" : "Rekor terbaik: " + best;
        if (r.coins > 0) {
            double bonus = r.coins * REWARD_PER_COIN;
            currentUser.bankBalance += bonus; // ENCAPSULATION: saldo di-update via Customer
            transactionHistory.add("BONUS TEST DRIVE: " + gameCar.getModel() + " (+Rp " + String.format("%,.0f", bonus) + ")");
            updateSemuaData();
            info += "\n+Rp " + String.format("%,.0f", bonus) + " masuk ke saldo";
        }
        lblResultBest.setText(info);
        btnGameBuy.setDisable(gameCar.getStock() <= 0);

        resultOverlay.setOpacity(0);
        resultOverlay.setVisible(true);
        FadeTransition ft = new FadeTransition(Duration.millis(250), resultOverlay); ft.setToValue(1); ft.play();
    }

    @FXML private void retryGame() { startNewGame(); }

    @FXML private void closeGame() {
        gameBox.setVisible(false);
        resultOverlay.setVisible(false);
        if (activeGame != null) {
            TestDriveGame g = activeGame;
            activeGame = null;
            g.dispose();
            gameHost.getChildren().remove(g);
        }
        closeModal();
    }

    @FXML private void buyFromGame() {
        Vehicle car = gameCar;
        closeGame();
        triggerBeli(car);
    }

    // =============================================================== TRANSAKSI

    private void triggerBeli(Vehicle car) {
        showModalAnimasi("Menghubungkan ke bank dan memvalidasi saldo...", "Memproses Pembelian", () -> {
            try {
                // ENCAPSULATION & EXCEPTION HANDLING
                String receipt = currentUser.buyVehicle(car);
                transactionHistory.add("PEMBELIAN: " + car.getBrand() + " " + car.getModel());
                updateSemuaData();
                modalBox.setVisible(false); txtReceiptContent.setText(receipt); receiptBox.setVisible(true);
            } catch (DealershipException ex) {
                closeModal(); showToast("Transaksi ditolak: " + ex.getMessage().replace("\n", " "), true);
            }
        });
    }

    @FXML
    private void prosesServis() {
        int idx = listServis.getSelectionModel().getSelectedIndex();
        if (idx >= 0) {
            double biaya = 2500000.0;
            if (currentUser.bankBalance >= biaya) {
                currentUser.bankBalance -= biaya; 
                transactionHistory.add("SERVIS: " + currentUser.garage.get(idx).getModel() + " (-Rp 2.5 Juta)");
                updateSemuaData(); showToast("Servis berhasil, kendaraan dalam kondisi prima", false);
            } else showToast("Saldo tidak mencukupi", true);
        } else showToast("Pilih kendaraan yang ingin diservis", true);
    }

    @FXML
    private void prosesTradeIn() {
        int idx = listTradeIn.getSelectionModel().getSelectedIndex();
        if (idx >= 0) {
            Vehicle carToSell = currentUser.garage.get(idx);
            double hargaJual = carToSell.getPrice() * 0.7; 
            currentUser.bankBalance += hargaJual; currentUser.garage.remove(idx);       
            transactionHistory.add("JUAL UNIT: " + carToSell.getModel() + " (+Rp " + String.format("%,.0f", hargaJual) + ")");
            updateSemuaData(); lblHargaJual.setText("Rp 0"); showToast("Kendaraan terjual, dana masuk ke saldo", false);
        } else showToast("Pilih kendaraan yang ingin dijual", true);
    }

    @FXML
    private void klaimReward() {
        if (hasClaimedReward) {
            showToast("Bonus hari ini sudah diklaim", true);
            return;
        }
        double bonus = 0;
        if (currentUser instanceof GoldCustomer) bonus = 50000000.0;
        else if (currentUser instanceof SilverCustomer) bonus = 10000000.0;
        else bonus = 1000000.0;
        
        currentUser.bankBalance += bonus;
        transactionHistory.add("KLAIM VIP BONUS (+Rp " + String.format("%,.0f", bonus) + ")");
        lblTierReward.setText("Sudah diklaim · Rp " + String.format("%,.0f", bonus));
        lblTierReward.getStyleClass().add("pill-success");
        
        hasClaimedReward = true; btnKlaimReward.setDisable(true); btnKlaimReward.setText("Sudah Diklaim");
        updateSemuaData(); showToast("Bonus VIP ditambahkan ke saldo", false);
    }

    @FXML private void closeModal() {
        modalOverlay.setVisible(false); mainAppPane.setEffect(null);
        btnCloseTestDrive.setVisible(false); progressBar.setVisible(true);
    }

    @FXML private void navToShowroom() { switchPage(pageShowroom, btnNavShowroom); }
    @FXML private void navToGarasi() { switchPage(pageGarasi, btnNavGarasi); }
    @FXML private void navToServis() { switchPage(pageServis, btnNavServis); }
    @FXML private void navToPajak() { switchPage(pagePajak, btnNavPajak); }
    @FXML private void navToTradeIn() { switchPage(pageTradeIn, btnNavTradeIn); }
    @FXML private void navToRiwayat() { switchPage(pageRiwayat, btnNavRiwayat); }
    @FXML private void navToRewards() { switchPage(pageRewards, btnNavRewards); }

    private void switchPage(VBox activePage, Button activeBtn) {
        VBox[] allPages = {pageShowroom, pageGarasi, pageServis, pagePajak, pageTradeIn, pageRiwayat, pageRewards};
        Button[] allBtns = {btnNavShowroom, btnNavGarasi, btnNavServis, btnNavPajak, btnNavTradeIn, btnNavRiwayat, btnNavRewards};

        for (int i = 0; i < allPages.length; i++) {
            if (allPages[i] == activePage) {
                allPages[i].setVisible(true); allPages[i].setOpacity(0); allPages[i].setTranslateY(8);
                FadeTransition ft = new FadeTransition(Duration.millis(220), allPages[i]); ft.setToValue(1);
                TranslateTransition tt = new TranslateTransition(Duration.millis(220), allPages[i]); tt.setToY(0);
                new ParallelTransition(ft, tt).play();
                if (!allBtns[i].getStyleClass().contains("active")) allBtns[i].getStyleClass().add("active");
            } else {
                allPages[i].setVisible(false); allBtns[i].getStyleClass().remove("active");
            }
        }
    }

    private void showModalAnimasi(String processText, String titleText, Runnable onFinish) {
        mainAppPane.setEffect(new BoxBlur(8, 8, 2));
        modalOverlay.setVisible(true); modalBox.setVisible(true); receiptBox.setVisible(false); gameBox.setVisible(false);
        lblModalTitle.setText(titleText); lblModalDesc.setText(processText);
        progressBar.setProgress(0);
        Timeline timeline = new Timeline(new KeyFrame(Duration.ZERO, new KeyValue(progressBar.progressProperty(), 0)),
                new KeyFrame(Duration.seconds(1.5), new KeyValue(progressBar.progressProperty(), 1, Interpolator.EASE_BOTH)));
        timeline.setOnFinished(e -> onFinish.run()); timeline.play();
    }

    private void updateSemuaData() {
        String name = currentUser.getName();
        lblSidebarUser.setText(name);
        lblSidebarAvatar.setText(name.isEmpty() ? "?" : name.substring(0, 1).toUpperCase());
        lblSidebarTier.setText(currentUser.getTierName());
        lblSidebarSaldo.setText("Rp " + String.format("%,.0f", currentUser.getBankBalance()));

        renderShowroomCards(); 
        renderGarasiCards();

        // 1. UPDATE BAR CHART & GARASI SUMMARY
        double totalAset = 0;
        double totalPajak = 0;
        chartAset.getData().clear();
        XYChart.Series<String, Number> series = new XYChart.Series<>();
        
        for (Vehicle v : currentUser.garage) { 
            totalAset += v.getPrice(); 
            totalPajak += v.calculateTax(v.getPrice()); // ITaxable Interface
            series.getData().add(new XYChart.Data<>(v.getModel(), v.getPrice()));
        }
        chartAset.getData().add(series);
        
        lblTotalUnit.setText(currentUser.garage.size() + " Unit");
        lblTotalAset.setText("Rp " + String.format("%,.0f", totalAset));
        lblSummaryPajak.setText("Rp " + String.format("%,.0f", totalPajak));

        // 2. UPDATE MENU PAJAK
        listPajak.getItems().clear();
        for (Vehicle v : currentUser.garage) {
            double pajakMobil = v.calculateTax(v.getPrice());
            listPajak.getItems().add(String.format("PPN 11%%  %-16s Rp %,.0f", v.getModel(), pajakMobil));
        }
        lblTotalPajak.setText("Rp " + String.format("%,.0f", totalPajak));

        // 3. UPDATE LIST LAINNYA
        listRiwayat.getItems().clear();
        for (int i = transactionHistory.size() - 1; i >= 0; i--) listRiwayat.getItems().add(transactionHistory.get(i)); // terbaru di atas
        
        listServis.getItems().clear(); listTradeIn.getItems().clear();
        for (Vehicle v : currentUser.garage) {
            String item = v.getBrand() + " " + v.getModel();
            listServis.getItems().add(item); listTradeIn.getItems().add(item);
        }
    }

    private void showToast(String message, boolean isError) {
        lblToast.setText((isError ? "✕  " : "✓  ") + message);
        toastPane.setStyle(isError ? "-fx-background-color: #dc2626;" : "-fx-background-color: #0f172a;");
        if (toastAnim != null) toastAnim.stop();
        TranslateTransition slideDown = new TranslateTransition(Duration.millis(300), toastPane);
        slideDown.setToY(0); slideDown.setInterpolator(Interpolator.EASE_OUT);
        TranslateTransition slideUp = new TranslateTransition(Duration.millis(300), toastPane);
        slideUp.setToY(-120); slideUp.setInterpolator(Interpolator.EASE_IN);
        toastAnim = new SequentialTransition(slideDown, new PauseTransition(Duration.seconds(2.6)), slideUp);
        toastAnim.play();
    }
}