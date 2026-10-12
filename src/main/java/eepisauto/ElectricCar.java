package eepisauto;

/**
 * Subclass konkret yang merepresentasikan Kendaraan Listrik (Electric Vehicle / EV).
 * <p>
 * Mewarisi {@link Vehicle} dan menambahkan atribut khusus motor listrik seperti
 * kapasitas baterai dalam kWh dan jarak tempuh jelajah dalam kilometer.
 * <p>
 * Konsep OOP: <b>Inheritance</b> &amp; <b>Polymorphism (Method Overriding)</b>.
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public class ElectricCar extends Vehicle {

    /** Kapasitas paket baterai dalam kilowatt-hour (kWh). */
    private int batteryCapacity;

    /** Estimasi jarak tempuh maksimal per pengisian daya dalam kilometer (km). */
    private int range;

    /**
     * Mengonstruksi mobil listrik dengan spesifikasi baterai dan performa.
     *
     * @param brand merek kendaraan
     * @param model varian model kendaraan
     * @param price harga OTR kendaraan
     * @param stock jumlah unit stok
     * @param color warna kendaraan
     * @param batteryCapacity kapasitas baterai dalam kWh
     * @param range estimasi jarak tempuh dalam km
     */
    public ElectricCar(String brand, String model, double price, int stock, String color, int batteryCapacity, int range) {
        super(brand, model, price, stock, color);
        this.batteryCapacity = batteryCapacity;
        this.range = range;
    }

    /**
     * {@inheritDoc}
     * Menghasilkan suara karakteristik melaju senyap dan akselerasi instan motor listrik EV.
     */
    @Override
    public String testDrive() {
        return "⚡ Zzzzz... Melaju instan nan senyap bertenaga EV.";
    }

    /**
     * {@inheritDoc}
     * Mengembalikan ringkasan spesifikasi kelistrikan (kapasitas kWh dan jarak km).
     */
    @Override
    public String getSpecs() {
        return "Listrik Murni (EV) | " + batteryCapacity + " kWh | Jarak: " + range + " km";
    }

    /**
     * Mengambil kapasitas baterai mobil listrik.
     *
     * @return kapasitas baterai dalam kWh
     */
    public int getBatteryCapacity() {
        return batteryCapacity;
    }

    /**
     * Mengambil jarak tempuh jelajah mobil listrik.
     *
     * @return jarak tempuh dalam km
     */
    public int getRange() {
        return range;
    }
}