package eepisauto;

/**
 * Subclass konkret yang merepresentasikan Kendaraan Bensin Konvensional (Internal Combustion Engine / ICE).
 * <p>
 * Mewarisi {@link Vehicle} dan menambahkan atribut khusus mesin pembakaran dalam seperti
 * kapasitas silinder mesin dalam cc dan konfigurasi tipe transmisi.
 * <p>
 * Konsep OOP: <b>Inheritance</b> &amp; <b>Polymorphism (Method Overriding)</b>.
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public class GasCar extends Vehicle {

    /** Kapasitas silinder mesin bensin dalam centimeter kubik (cc). */
    private int engineCapacity;

    /** Jenis sistem transmisi (misal: 6-Speed MT, 8-Speed Auto). */
    private String transmission;

    /**
     * Mengonstruksi mobil bensin dengan spesifikasi mesin dan transmisi.
     *
     * @param brand merek kendaraan
     * @param model varian model kendaraan
     * @param price harga OTR kendaraan
     * @param stock jumlah unit stok
     * @param color warna kendaraan
     * @param engineCapacity kapasitas mesin dalam cc
     * @param transmission jenis sistem transmisi
     */
    public GasCar(String brand, String model, double price, int stock, String color, int engineCapacity, String transmission) {
        super(brand, model, price, stock, color);
        this.engineCapacity = engineCapacity;
        this.transmission = transmission;
    }

    /**
     * {@inheritDoc}
     * Menghasilkan suara raungan knalpot dan deru mesin konvensional bertenaga.
     */
    @Override
    public String testDrive() {
        return "🏎️💨 VROOOM! Suara mesin " + engineCapacity + "cc menderu kencang!";
    }

    /**
     * {@inheritDoc}
     * Mengembalikan ringkasan spesifikasi mesin bensin (kapasitas cc dan transmisi).
     */
    @Override
    public String getSpecs() {
        return "Bahan Bakar Bensin | " + engineCapacity + "cc | " + transmission;
    }

    /**
     * Mengambil kapasitas mesin bensin.
     *
     * @return kapasitas mesin dalam cc
     */
    public int getEngineCapacity() {
        return engineCapacity;
    }

    /**
     * Mengambil jenis transmisi mobil bensin.
     *
     * @return jenis transmisi
     */
    public String getTransmission() {
        return transmission;
    }
}