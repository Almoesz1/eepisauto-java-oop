package eepisauto;

import java.util.ArrayList;
import java.util.List;

public abstract class Customer extends User {
    protected double bankBalance;
    public List<Vehicle> garage;

    public Customer(String id, String name, double bankBalance) {
        super(id, name); this.bankBalance = bankBalance; this.garage = new ArrayList<>();
    }

    public double getBankBalance() { return bankBalance; }
    public abstract String getTierName();
    public abstract double calculateDiscount(double price);
    
    // Abstract method baru untuk mengurus Bonus & Cashback tiap Tier
    public abstract String applyBonus(double finalPrice);
    
    public String buyVehicle(Vehicle vehicle) throws DealershipException {
        if (vehicle.getStock() <= 0) {
            throw new DealershipException("Stok " + vehicle.getBrand() + " " + vehicle.getModel() + " sedang kosong!");
        }

        double discount = calculateDiscount(vehicle.getPrice());
        double discountedPrice = vehicle.getPrice() - discount;
        double tax = vehicle.calculateTax(discountedPrice);
        double finalPrice = discountedPrice + tax;

        if (this.bankBalance < finalPrice) {
            throw new DealershipException("Saldo Anda tidak mencukupi!\nKekurangan: Rp " + String.format("%,.0f", (finalPrice - this.bankBalance)));
        }

        this.bankBalance -= finalPrice;
        vehicle.decreaseStock();
        this.garage.add(vehicle);
        
        // Terapkan bonus SETELAH transaksi sukses
        String bonusBrought = applyBonus(finalPrice);
        
        return TransactionReceipt.generateReceipt(this, vehicle, finalPrice, discount, tax, bonusBrought);
    }
}