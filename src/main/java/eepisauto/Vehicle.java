package eepisauto;

/**
 * Superclass abstrak untuk seluruh entitas Kendaraan yang dijual pada showroom EEPIS Auto.
 * <p>
 * Mengimplementasikan interface {@link ITaxable} sebagai kontrak perhitungan beban pajak PPN 11%.
 * Menyediakan kerangka atribut dasar kendaraan seperti merek, model, harga, stok, dan warna,
 * serta method abstrak {@link #testDrive()} dan {@link #getSpecs()} untuk polimorfisme turunan.
 * <p>
 * Konsep OOP: <b>Abstraction</b>, <b>Interface Realization</b>, &amp; <b>Polymorphism</b>.
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public abstract class Vehicle implements ITaxable {

    /** Merek pabrikan kendaraan (misal: Porsche, BMW, Tesla). */
    protected String brand;

    /** Model atau varian seri kendaraan. */
    protected String model;

    /** Warna eksterior kendaraan. */
    protected String color;

    /** Harga dasar kendaraan sebelum diskon dan pajak dalam rupiah (OTR). */
    protected double price;

    /** Jumlah unit stok fisik yang tersedia di dealer. */
    protected int stock;

    /**
     * Mengonstruksi objek kendaraan dengan spesifikasi awal.
     *
     * @param brand merek pabrikan kendaraan
     * @param model varian model kendaraan
     * @param price harga dasar kendaraan
     * @param stock jumlah stok awal
     * @param color warna kendaraan
     */
    public Vehicle(String brand, String model, double price, int stock, String color) {
        this.brand = brand;
        this.model = model;
        this.price = price;
        this.stock = stock;
        this.color = color;
    }

    /**
     * Mengambil nama merek pabrikan kendaraan.
     *
     * @return merek kendaraan
     */
    public String getBrand() {
        return brand;
    }

    /**
     * Mengambil varian model kendaraan.
     *
     * @return model kendaraan
     */
    public String getModel() {
        return model;
    }

    /**
     * Mengambil harga dasar kendaraan.
     *
     * @return harga kendaraan dalam rupiah
     */
    public double getPrice() {
        return price;
    }

    /**
     * Mengambil sisa stok fisik kendaraan di dealer.
     *
     * @return jumlah stok unit
     */
    public int getStock() {
        return stock;
    }

    /**
     * Mengambil warna eksterior kendaraan.
     *
     * @return nama warna
     */
    public String getColor() {
        return color;
    }

    /**
     * Mengurangi jumlah stok kendaraan sebanyak 1 unit setelah transaksi pembelian berhasil.
     */
    public void decreaseStock() {
        if (this.stock > 0) {
            this.stock--;
        }
    }

    /**
     * {@inheritDoc}
     * Menghitung nilai PPN 11% dari harga kendaraan setelah pemotongan diskon.
     */
    @Override
    public double calculateTax(double priceAfterDiscount) {
        return priceAfterDiscount * getTaxRate();
    }

    /**
     * {@inheritDoc}
     * Mengembalikan tarif PPN standar nasional sebesar 11% (0.11).
     */
    @Override
    public double getTaxRate() {
        return 0.11;
    }

    /**
     * Menghasilkan teks respons suara dan karakteristik berkendara kendaraan saat diuji coba.
     * <p>
     * Dideklarasikan abstrak untuk dioverride secara polimorfis oleh {@link ElectricCar} dan {@link GasCar}.
     *
     * @return deskripsi suara dan performa test drive
     */
    public abstract String testDrive();

    /**
     * Mengambil rincian spesifikasi teknis ringkas dari kendaraan.
     *
     * @return string rincian spesifikasi (mesin/baterai/transmisi)
     */
    public abstract String getSpecs();
}