package eepisauto;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class App extends Application {
    @Override
    public void start(Stage stage) throws Exception {
        Parent root = FXMLLoader.load(getClass().getResource("primary.fxml"));
        Scene scene = new Scene(root, 900, 650);
        stage.setScene(scene);
        stage.setTitle("EEPIS AUTO VIP - Sistem Dealer Terpadu");
        stage.show();
    }
    public static void main(String[] args) { launch(args); }
}