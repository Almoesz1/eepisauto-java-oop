package eepisauto;

// Custom Exception: Menunjukkan kamu bisa membuat sistem error mandiri
public class DealershipException extends Exception {
    public DealershipException(String message) {
        super(message);
    }
}