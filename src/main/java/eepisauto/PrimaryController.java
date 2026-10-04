package eepisauto;

import java.util.ArrayList;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.Priority;

public class PrimaryController {

    @FXML private TextField txtNama;
    @FXML private TextField txtSaldo;
    @FXML private Button btnVerifikasi;
    @FXML private Label lblStatus;
    
    @FXML private ListView<String> listShowroom;
    @FXML private ListView<String> listGarasi;
    @FXML private Button btnTestDrive;
    @FXML private Button btnBeli;

    private ArrayList<Vehicle> showroom;
    private Customer currentUser;

    @FXML
    public void initialize() {
        showroom = new ArrayList<>();
        // Koleksi sultan lengkap
        showroom.add(new ElectricCar("Porsche", "Taycan Turbo S", 2500000000.0, 1, "Carrera White", 93, 500));
        showroom.add(new GasCar("BMW", "M3 Competition", 2300000000.0, 2, "Isle of Man Green", 3000, "8-Speed Auto"));
        showroom.add(new GasCar("Honda", "Civic Type R", 1400000000.0, 1, "Championship White", 2000, "6-Speed Manual"));
        showroom.add(new ElectricCar("Hyundai", "Ioniq 5 N", 1300000000.0, 3, "Performance Blue", 84, 450));
        showroom.add(new GasCar("Toyota", "GR Yaris", 850000000.0, 2, "Emotional Red", 1600, "6-Speed Manual"));
        refreshShowroomView();
    }

    @FXML
    private void handleVerifikasi() {
        try {
            String nama = txtNama.getText();
            double saldo = Double.parseDouble(txtSaldo.getText());
            String nrp = "3125600065"; // NRP Spesifik Mahasiswa

            if (nama.isEmpty()) { showErrorDialog("Validasi Gagal", "Nama KTP wajib diisi!"); return; }

            // Factory Logic: Penentuan Tier
            if (saldo >= 2000000000) currentUser = new GoldCustomer(nrp, nama, saldo);
            else if (saldo >= 1000000000) currentUser = new SilverCustomer(nrp, nama, saldo);
            else currentUser = new RegularCustomer(nrp, nama, saldo);

            lblStatus.setText("Status: " + currentUser.getTierName() + " | Saldo: Rp" + String.format("%,.0f", currentUser.getBankBalance()));
            lblStatus.setStyle("-fx-text-fill: #27ae60; -fx-font-weight: bold;");
            
            btnBeli.setDisable(false); btnTestDrive.setDisable(false);
            txtNama.setDisable(true); txtSaldo.setDisable(true); btnVerifikasi.setDisable(true);
            
            currentUser.displayProfile();
        } catch (NumberFormatException e) {
            showErrorDialog("Format Salah", "Mohon masukkan nominal saldo berupa angka mutlak (tanpa titik/koma).");
        }
    }

    @FXML
    private void handleTestDrive() {
        int index = listShowroom.getSelectionModel().getSelectedIndex();
        if (index >= 0) {
            Vehicle car = showroom.get(index);
            car.testDrive();
            showInfoDialog("Test Drive Dimulai", "Anda sedang mengendarai " + car.getBrand() + " " + car.getModel() + "\n\n(Cek Output Terminal untuk suara mesin/motor listriknya!)");
        } else {
            showErrorDialog("Peringatan", "Pilih kendaraan di katalog terlebih dahulu.");
        }
    }

    @FXML
    private void handleBeli() {
        int index = listShowroom.getSelectionModel().getSelectedIndex();
        if (index >= 0) {
            Vehicle selectedCar = showroom.get(index);
            try {
                // Menjalankan transaksi (bisa melempar DealershipException)
                String receipt = currentUser.buyVehicle(selectedCar);
                
                // Jika sukses, tampilkan Faktur GUI
                showReceiptDialog("Transaksi Berhasil", receipt);
                
                refreshGarasiView(); 
                refreshShowroomView();
                lblStatus.setText("Status: " + currentUser.getTierName() + " | Sisa Saldo: Rp" + String.format("%,.0f", currentUser.getBankBalance()));
                
            } catch (DealershipException ex) {
                // Menangkap Custom Error jika saldo kurang atau stok habis
                showErrorDialog("Transaksi Dibatalkan", ex.getMessage());
            }
        } else {
            showErrorDialog("Peringatan", "Pilih kendaraan yang ingin dibeli terlebih dahulu.");
        }
    }

    private void refreshShowroomView() {
        listShowroom.getItems().clear();
        for (Vehicle v : showroom) listShowroom.getItems().add(v.getBrand() + " " + v.getModel() + " | Rp" + String.format("%,.0f", v.getPrice()) + " | Stok: " + v.getStock());
    }

    private void refreshGarasiView() {
        listGarasi.getItems().clear();
        for (Vehicle v : currentUser.garage) listGarasi.getItems().add(v.getBrand() + " " + v.getModel() + " (" + v.getColor() + ") - " + v.getSpecs());
    }

    // --- CUSTOM UI DIALOGS UNTUK KESAN PROFESIONAL ---
    private void showInfoDialog(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle(title); alert.setHeaderText(null); alert.setContentText(message); alert.showAndWait();
    }

    private void showErrorDialog(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title); alert.setHeaderText(null); alert.setContentText(message); alert.showAndWait();
    }

    private void showReceiptDialog(String title, String receiptText) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle(title); alert.setHeaderText("Faktur Pembelian Resmi (Auto-Debet)");
        
        TextArea textArea = new TextArea(receiptText);
        textArea.setEditable(false);
        textArea.setWrapText(false);
        textArea.setStyle("-fx-font-family: 'Consolas'; -fx-font-size: 13px;"); // Font ala struk POS Kasir
        
        textArea.setMaxWidth(Double.MAX_VALUE);
        textArea.setMaxHeight(Double.MAX_VALUE);
        GridPane.setVgrow(textArea, Priority.ALWAYS);
        GridPane.setHgrow(textArea, Priority.ALWAYS);
        GridPane content = new GridPane();
        content.setMaxWidth(Double.MAX_VALUE);
        content.add(textArea, 0, 0);

        alert.getDialogPane().setContent(content);
        alert.showAndWait();
    }
}