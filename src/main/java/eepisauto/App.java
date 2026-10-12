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
        Scene scene = new Scene(root, 1280, 800);
        stage.setScene(scene);
        stage.setMinWidth(1100); stage.setMinHeight(720);
        stage.setTitle("EEPIS AUTO VIP - Sistem Dealer Terpadu");
        stage.show();
    }
    public static void main(String[] args) { launch(args); }
}