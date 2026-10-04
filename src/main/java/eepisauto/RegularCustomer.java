package eepisauto;
public class RegularCustomer extends Customer {
    public RegularCustomer(String id, String name, double balance) { super(id, name, balance); }
    @Override public String getTierName() { return "Regular Tier"; }
    @Override public double calculateDiscount(double price) { return 0; }
    @Override public void displayProfile() { System.out.println("Login: Regular"); }
    
    // Implementasi Bonus Reguler
    @Override public String applyBonus(double finalPrice) {
        return "- (Tier Reguler tidak mendapat bonus khusus)";
    }
}