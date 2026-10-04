package eepisauto;
public class SilverCustomer extends Customer {
    public SilverCustomer(String id, String name, double balance) { super(id, name, balance); }
    @Override public String getTierName() { return "Silver VIP"; }
    @Override public double calculateDiscount(double price) { return price * 0.03; }
    @Override public void displayProfile() { System.out.println("Login: Silver VIP"); }

    // Implementasi Bonus Silver
    @Override public String applyBonus(double finalPrice) {
        return "Gratis Servis 1 Tahun & Merchandise Jaket EepisAuto";
    }
}