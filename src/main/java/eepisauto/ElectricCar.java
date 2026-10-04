package eepisauto;

public class ElectricCar extends Vehicle {
    private int batteryCapacity;
    private int range;

    public ElectricCar(String brand, String model, double price, int stock, String color, int batteryCapacity, int range) {
        super(brand, model, price, stock, color);
        this.batteryCapacity = batteryCapacity;
        this.range = range;
    }
    @Override public void testDrive() { System.out.println("[TEST DRIVE] Zzzzz... " + brand + " " + model + " melaju instan nan senyap bertenaga EV."); }
    @Override public String getSpecs() { return "Listrik Murni (EV) | " + batteryCapacity + " kWh | Jarak: " + range + " km"; }
}