module eepisauto {
    requires javafx.controls;
    requires javafx.fxml;
    requires javafx.graphics;

    opens eepisauto to javafx.fxml;
    exports eepisauto;
}
