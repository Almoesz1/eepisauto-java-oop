package eepisauto;
public class GoldCustomer extends Customer {
    public GoldCustomer(String id, String name, double balance) { super(id, name, balance); }
    @Override public String getTierName() { return "Gold VVIP"; }
    @Override public double calculateDiscount(double price) { return price * 0.08; }
    @Override public void displayProfile() { System.out.println("Login: Sultan VVIP"); }

    // Implementasi Bonus Gold (Otomatis memanipulasi atribut Encapsulation)
    @Override public String applyBonus(double finalPrice) {
        double cashback = finalPrice * 0.02; // Dapat Cashback Saldo 2%
        this.bankBalance += cashback; // Saldo direfund sebagian!
        
        return "Cashback Saldo Rp " + String.format("%,.0f", cashback) + " & Asuransi All-Risk 3 Thn";
    }
}