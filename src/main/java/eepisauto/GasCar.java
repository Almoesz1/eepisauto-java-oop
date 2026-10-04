package eepisauto;

public class GasCar extends Vehicle {
    private int engineCapacity;
    private String transmission;

    public GasCar(String brand, String model, double price, int stock, String color, int engineCapacity, String transmission) {
        super(brand, model, price, stock, color);
        this.engineCapacity = engineCapacity;
        this.transmission = transmission;
    }
    @Override public void testDrive() { System.out.println("[TEST DRIVE] VROOOM! Suara mesin " + engineCapacity + "cc menderu dari " + brand + " " + model); }
    @Override public String getSpecs() { return "Bahan Bakar Bensin | " + engineCapacity + "cc | " + transmission; }
}