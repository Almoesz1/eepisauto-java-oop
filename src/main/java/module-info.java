module eepisauto {
    requires javafx.controls;
    requires javafx.fxml;

    opens eepisauto to javafx.fxml;
    exports eepisauto;
}
