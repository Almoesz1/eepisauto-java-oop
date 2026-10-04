package eepisauto;

public abstract class Vehicle implements ITaxable {
    protected String brand;
    protected String model;
    protected double price;
    protected int stock;
    protected String color;

    public Vehicle(String brand, String model, double price, int stock, String color) {
        this.brand = brand; this.model = model; this.price = price; this.stock = stock; this.color = color;
    }

    public String getBrand() { return brand; }
    public String getModel() { return model; }
    public double getPrice() { return price; }
    public int getStock() { return stock; }
    public String getColor() { return color; }
    public void decreaseStock() { if(this.stock > 0) this.stock--; }

    // Implementasi Interface ITaxable (PPN 11%)
    @Override
    public double calculateTax(double priceAfterDiscount) { return priceAfterDiscount * getTaxRate(); }
    @Override
    public double getTaxRate() { return 0.11; }

    public abstract void testDrive();
    public abstract String getSpecs();
}