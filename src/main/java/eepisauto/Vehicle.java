package eepisauto;

public abstract class Vehicle implements ITaxable {
    protected String brand, model, color;
    protected double price;
    protected int stock;

    public Vehicle(String brand, String model, double price, int stock, String color) {
        this.brand = brand; this.model = model; this.price = price; this.stock = stock; this.color = color;
    }

    public String getBrand() { return brand; }
    public String getModel() { return model; }
    public double getPrice() { return price; }
    public int getStock() { return stock; }
    public String getColor() { return color; }
    public void decreaseStock() { if(this.stock > 0) this.stock--; }

    @Override public double calculateTax(double priceAfterDiscount) { return priceAfterDiscount * getTaxRate(); }
    @Override public double getTaxRate() { return 0.11; }

    // PERUBAHAN: Sekarang me-return String agar ditangkap GUI Animasi
    public abstract String testDrive();
    public abstract String getSpecs();
}