package eepisauto;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

/**
 * Titik masuk utama (Main Application Class) dari aplikasi JavaFX EEPIS Auto VIP Dealership.
 * <p>
 * Memuat berkas FXML antarmuka ({@code primary.fxml}), mengatur ukuran jendela minimum,
 * dan menginisialisasi panggung utama ({@link Stage}).
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public class App extends Application {

    /**
     * Memulai siklus hidup aplikasi JavaFX dan menampilkan jendela utama.
     *
     * @param stage panggung utama yang disediakan runtime JavaFX
     * @throws Exception jika gagal memuat berkas layout primary.fxml
     */
    @Override
    public void start(Stage stage) throws Exception {
        Parent root = FXMLLoader.load(getClass().getResource("primary.fxml"));
        Scene scene = new Scene(root, 1280, 800);
        stage.setScene(scene);
        stage.setMinWidth(1100);
        stage.setMinHeight(720);
        stage.setTitle("EEPIS AUTO VIP - Sistem Dealer Terpadu");
        stage.show();
    }

    /**
     * Method main standar untuk mengeksekusi aplikasi JavaFX.
     *
     * @param args argumen baris perintah
     */
    public static void main(String[] args) {
        launch(args);
    }
}