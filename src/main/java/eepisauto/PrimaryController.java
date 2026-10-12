package eepisauto;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import javafx.animation.*;
import javafx.fxml.FXML;
import javafx.scene.chart.*;
import javafx.scene.control.*;
import javafx.scene.effect.BoxBlur;
import javafx.scene.layout.*;
import javafx.util.Duration;

public class PrimaryController {

    @FXML private BorderPane mainAppPane;
    @FXML private StackPane loginOverlay, modalOverlay, animasiDriveOverlay;
    @FXML private VBox modalBox, receiptBox;
    @FXML private TextField txtNama, txtSaldo, txtSearch;
    @FXML private ComboBox<String> comboFilter;
    
    // 7 Sidebar & Pages
    @FXML private Button btnNavShowroom, btnNavGarasi, btnNavServis, btnNavPajak, btnNavTradeIn, btnNavRiwayat, btnNavRewards;
    @FXML private VBox pageShowroom, pageGarasi, pageServis, pagePajak, pageTradeIn, pageRiwayat, pageRewards;
    
    // UI Elements
    @FXML private Label lblSidebarUser, lblSidebarTier, lblSidebarSaldo;
    @FXML private Label lblTotalAset, lblHargaJual, lblTotalPajak, lblTierReward, lblAnimasiMobil;
    @FXML private FlowPane showroomContainer, garasiContainer;
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

    private ArrayList<Vehicle> showroom = new ArrayList<>();
    private Customer currentUser;
    private List<String> transactionHistory = new ArrayList<>();
    
    // BUG FIX: Kunci Reward agar tidak dieksploitasi
    private boolean hasClaimedReward = false; 

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
    }

    @FXML
    private void handleVerifikasi() {
        try {
            String nama = txtNama.getText();
            double saldo = Double.parseDouble(txtSaldo.getText());
            if (nama.isEmpty()) { showToast("Nama identitas wajib diisi!", true); return; }

            String nrp = "3125600065";
            if (saldo >= 3000000000.0) currentUser = new GoldCustomer(nrp, nama, saldo);
            else if (saldo >= 1000000000.0) currentUser = new SilverCustomer(nrp, nama, saldo);
            else currentUser = new RegularCustomer(nrp, nama, saldo);

            updateSemuaData();
            
            FadeTransition ftOut = new FadeTransition(Duration.millis(800), loginOverlay);
            ftOut.setToValue(0); ftOut.setOnFinished(e -> loginOverlay.setVisible(false));
            FadeTransition ftIn = new FadeTransition(Duration.millis(1200), mainAppPane);
            ftIn.setToValue(1);
            ftOut.play(); ftIn.play();
            showToast("Akses Diterima: " + currentUser.getTierName(), false);

        } catch (NumberFormatException e) {
            showToast("Format saldo salah! Masukkan angka murni.", true);
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

        for (Vehicle car : filteredList) {
            VBox card = new VBox(10);
            card.getStyleClass().add("car-card");
            card.setPrefWidth(270);

            StackPane imagePane = new StackPane();
            imagePane.getStyleClass().add(car instanceof ElectricCar ? "car-img-ev" : "car-img-gas");
            Label icon = new Label(car instanceof ElectricCar ? "⚡🚙" : "🏎️💨");
            icon.setStyle("-fx-font-size: 70px; -fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.5), 10, 0, 0, 5);");
            Label brandLogo = new Label(car.getBrand().toUpperCase());
            brandLogo.setStyle("-fx-font-size: 45px; -fx-font-weight: bold; -fx-text-fill: rgba(255,255,255,0.08);");
            imagePane.getChildren().addAll(brandLogo, icon);

            VBox textPane = new VBox(8);
            textPane.setPadding(new javafx.geometry.Insets(15));
            Label title = new Label(car.getBrand() + " " + car.getModel());
            title.getStyleClass().add("text-title"); title.setStyle("-fx-font-size: 18px;");
            Label specs = new Label(car.getSpecs());
            specs.getStyleClass().add("text-subtitle");
            Label price = new Label(String.format("Rp %,.0f", car.getPrice()));
            price.getStyleClass().add("text-accent"); price.setStyle("-fx-font-size: 18px;");
            textPane.getChildren().addAll(title, specs, price);

            HBox actions = new HBox(12);
            actions.setPadding(new javafx.geometry.Insets(0, 15, 20, 15));
            Button btnDrive = new Button("Test Drive");
            btnDrive.getStyleClass().add("btn-secondary"); btnDrive.setMaxWidth(Double.MAX_VALUE); HBox.setHgrow(btnDrive, Priority.ALWAYS);
            btnDrive.setOnAction(e -> triggerTestDrive(car));
            
            Button btnBuy = new Button("Beli Unit");
            btnBuy.getStyleClass().add("btn-primary"); btnBuy.setMaxWidth(Double.MAX_VALUE); HBox.setHgrow(btnBuy, Priority.ALWAYS);
            btnBuy.setOnAction(e -> triggerBeli(car));
            
            actions.getChildren().addAll(btnDrive, btnBuy);
            card.getChildren().addAll(imagePane, textPane, actions);
            showroomContainer.getChildren().add(card);
        }
    }

    private void renderGarasiCards() {
        garasiContainer.getChildren().clear();
        for (Vehicle car : currentUser.garage) {
            VBox card = new VBox(10);
            card.getStyleClass().add("car-card");
            card.setPrefWidth(240);
            
            StackPane imagePane = new StackPane();
            imagePane.getStyleClass().add("car-img-owned");
            Label icon = new Label("✅ LUNAS");
            icon.setStyle("-fx-font-size: 26px; -fx-font-weight: bold; -fx-text-fill: white;");
            imagePane.getChildren().add(icon);

            VBox textPane = new VBox(8);
            textPane.setPadding(new javafx.geometry.Insets(15));
            Label title = new Label(car.getBrand() + " " + car.getModel());
            title.setStyle("-fx-font-size: 16px; -fx-font-weight: bold; -fx-text-fill: white;");
            Label price = new Label("Aset: Rp " + String.format("%,.0f", car.getPrice()));
            price.setStyle("-fx-text-fill: #10b981; -fx-font-size: 13px;");
            textPane.getChildren().addAll(title, price);

            card.getChildren().addAll(imagePane, textPane);
            garasiContainer.getChildren().add(card);
        }
    }

    private void triggerTestDrive(Vehicle car) {
        mainAppPane.setEffect(new BoxBlur(20, 20, 3));
        animasiDriveOverlay.setVisible(true);
        lblAnimasiMobil.setText(car instanceof ElectricCar ? "⚡🚙" : "🏎️💨");
        lblAnimasiMobil.setTranslateX(-900); 

        TranslateTransition driveAnim = new TranslateTransition(Duration.seconds(1.2), lblAnimasiMobil);
        driveAnim.setToX(900); driveAnim.setInterpolator(Interpolator.EASE_IN);
        driveAnim.setOnFinished(e -> {
            animasiDriveOverlay.setVisible(false);
            modalOverlay.setVisible(true); modalBox.setVisible(true); receiptBox.setVisible(false);
            lblModalTitle.setText("Hasil Test Drive: " + car.getModel());
            lblModalDesc.setText(car.testDrive());
            lblModalDesc.setStyle("-fx-text-fill: #38bdf8; -fx-font-weight: bold; -fx-font-size: 22px;");
            progressBar.setVisible(false); btnCloseTestDrive.setVisible(true);
        });
        driveAnim.play();
    }

    private void triggerBeli(Vehicle car) {
        showModalAnimasi("Koneksi Bank & Validasi Saldo...", "Memproses Pembelian", () -> {
            try {
                String receipt = currentUser.buyVehicle(car);
                transactionHistory.add("PEMBELIAN: " + car.getBrand() + " " + car.getModel());
                updateSemuaData();
                modalBox.setVisible(false); txtReceiptContent.setText(receipt); receiptBox.setVisible(true);
            } catch (DealershipException ex) {
                closeModal(); showToast("Transaksi Ditolak: " + ex.getMessage(), true);
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
                updateSemuaData(); showToast("Servis Berhasil! Mesin Prima.", false);
            } else showToast("Saldo rekening Anda tidak mencukupi.", true);
        } else showToast("Pilih mobil yang ingin diservis!", true);
    }

    @FXML
    private void prosesTradeIn() {
        int idx = listTradeIn.getSelectionModel().getSelectedIndex();
        if (idx >= 0) {
            Vehicle carToSell = currentUser.garage.get(idx);
            double hargaJual = carToSell.getPrice() * 0.7; 
            currentUser.bankBalance += hargaJual; currentUser.garage.remove(idx);       
            transactionHistory.add("JUAL UNIT: " + carToSell.getModel() + " (+Rp " + String.format("%,.0f", hargaJual) + ")");
            updateSemuaData(); lblHargaJual.setText("Rp 0"); showToast("Berhasil Terjual! Dana dikembalikan.", false);
        } else showToast("Pilih mobil yang ingin dijual!", true);
    }

    @FXML
    private void klaimReward() {
        if (hasClaimedReward) {
            showToast("Anda sudah mengklaim bonus hari ini!", true);
            return;
        }

        double bonus = 0;
        if (currentUser instanceof GoldCustomer) bonus = 50000000.0;
        else if (currentUser instanceof SilverCustomer) bonus = 10000000.0;
        else bonus = 1000000.0;
        
        currentUser.bankBalance += bonus;
        transactionHistory.add("KLAIM VIP BONUS (+Rp " + String.format("%,.0f", bonus) + ")");
        lblTierReward.setText("Status: Sudah Diklaim (Rp " + String.format("%,.0f", bonus) + ")");
        
        // Kunci tombol agar tidak dieksploitasi lagi
        hasClaimedReward = true;
        btnKlaimReward.setDisable(true);
        btnKlaimReward.setText("REWARD SUDAH DIAMBIL");
        
        updateSemuaData();
        showToast("Bonus VIP berhasil ditambahkan ke saldo!", false);
    }

    @FXML private void closeModal() { modalOverlay.setVisible(false); mainAppPane.setEffect(null); btnCloseTestDrive.setVisible(false); progressBar.setVisible(true); }

    // --- NAVIGASI MULTI PAGE 7 MENU ---
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
                allPages[i].setVisible(true); allPages[i].setOpacity(0);
                FadeTransition ft = new FadeTransition(Duration.millis(300), allPages[i]);
                ft.setToValue(1); ft.play();
                allBtns[i].getStyleClass().add("active");
            } else {
                allPages[i].setVisible(false);
                allBtns[i].getStyleClass().remove("active");
            }
        }
    }

    private void showModalAnimasi(String processText, String titleText, Runnable onFinish) {
        mainAppPane.setEffect(new BoxBlur(15, 15, 3));
        modalOverlay.setVisible(true); modalBox.setVisible(true); receiptBox.setVisible(false);
        lblModalTitle.setText(titleText); lblModalDesc.setText(processText);
        lblModalDesc.setStyle("-fx-text-fill: #94a3b8;"); progressBar.setProgress(0);
        Timeline timeline = new Timeline(new KeyFrame(Duration.ZERO, new KeyValue(progressBar.progressProperty(), 0)), new KeyFrame(Duration.seconds(1.5), new KeyValue(progressBar.progressProperty(), 1)));
        timeline.setOnFinished(e -> onFinish.run()); timeline.play();
    }

    private void updateSemuaData() {
        lblSidebarUser.setText(currentUser.getName().toUpperCase());
        lblSidebarTier.setText("👑 " + currentUser.getTierName());
        lblSidebarSaldo.setText("Rp " + String.format("%,.0f", currentUser.getBankBalance()));

        renderShowroomCards(); renderGarasiCards();

        // 1. UPDATE BAR CHART
        double totalAset = 0;
        chartAset.getData().clear();
        XYChart.Series<String, Number> series = new XYChart.Series<>();
        for (Vehicle v : currentUser.garage) { 
            totalAset += v.getPrice(); 
            series.getData().add(new XYChart.Data<>(v.getModel(), v.getPrice()));
        }
        chartAset.getData().add(series);
        lblTotalAset.setText("Rp " + String.format("%,.0f", totalAset));

        // 2. UPDATE MENU PAJAK (Implementasi ITaxable Interface)
        listPajak.getItems().clear();
        double totalPajak = 0;
        for (Vehicle v : currentUser.garage) {
            double pajakMobil = v.calculateTax(v.getPrice()); // Memanggil fungsi Interface
            totalPajak += pajakMobil;
            listPajak.getItems().add(String.format("PPN 11%% | %-15s : Rp %,.0f", v.getModel(), pajakMobil));
        }
        lblTotalPajak.setText("Rp " + String.format("%,.0f", totalPajak));

        // 3. UPDATE LIST LAINNYA
        listRiwayat.getItems().clear();
        for (String log : transactionHistory) listRiwayat.getItems().add(log);
        
        listServis.getItems().clear(); listTradeIn.getItems().clear();
        for (Vehicle v : currentUser.garage) {
            String item = v.getBrand() + " " + v.getModel();
            listServis.getItems().add(item); listTradeIn.getItems().add(item);
        }
    }

    private void showToast(String message, boolean isError) {
        lblToast.setText(message); toastPane.setStyle(isError ? "-fx-background-color: #ef4444;" : "-fx-background-color: #10b981;");
        TranslateTransition slideDown = new TranslateTransition(Duration.millis(400), toastPane); slideDown.setToY(20);
        TranslateTransition slideUp = new TranslateTransition(Duration.millis(400), toastPane); slideUp.setToY(-100);
        slideUp.setDelay(Duration.seconds(3)); slideDown.setOnFinished(e -> slideUp.play()); slideDown.play();
    }
}