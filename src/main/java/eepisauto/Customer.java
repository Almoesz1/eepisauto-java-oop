package eepisauto;

import java.util.ArrayList;
import java.util.List;

/**
 * Superclass abstrak yang merepresentasikan Pelanggan (Customer) dealer.
 * <p>
 * Mewarisi {@link User} dan menerapkan konsep Enkapsulasi ketat terhadap saldo rekening
 * ({@code bankBalance}) serta koleksi aset mobil di garasi ({@code garage}).
 * Seluruh mutasi finansial wajib melalui method bisnis terproteksi seperti {@link #buyVehicle(Vehicle)}.
 * <p>
 * Konsep OOP: <b>Abstraction</b>, <b>Inheritance</b>, &amp; <b>Encapsulation</b>.
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public abstract class Customer extends User {

    /** Saldo rekening pelanggan yang terproteksi dari manipulasi luar secara langsung. */
    protected double bankBalance;

    /** Daftar koleksi kendaraan yang sah dimiliki pelanggan di garasi pribadinya. */
    public List<Vehicle> garage;

    /**
     * Mengonstruksi pelanggan baru dengan saldo rekening awal dan garasi kosong.
     *
     * @param id nomor identitas unik pelanggan
     * @param name nama lengkap pelanggan
     * @param bankBalance saldo awal rekening
     */
    public Customer(String id, String name, double bankBalance) {
        super(id, name);
        this.bankBalance = bankBalance;
        this.garage = new ArrayList<>();
    }

    /**
     * Mengambil sisa saldo rekening terenkapsulasi milik pelanggan.
     *
     * @return nilai saldo dalam rupiah
     */
    public double getBankBalance() {
        return bankBalance;
    }

    /**
     * Mengambil nama tier hak istimewa pelanggan (Regular, Silver, atau Gold).
     *
     * @return nama tier VIP
     */
    public abstract String getTierName();

    /**
     * Menghitung besaran potongan diskon tier yang berhak didapatkan pelanggan.
     *
     * @param price harga dasar mobil
     * @return nominal potongan harga dalam rupiah
     */
    public abstract double calculateDiscount(double price);

    /**
     * Menerapkan bonus dan hadiah eksklusif sesuai tier pelanggan setelah transaksi berhasil.
     *
     * @param finalPrice harga total yang telah dibayarkan pelanggan
     * @return string deskripsi bonus yang didapatkan
     */
    public abstract String applyBonus(double finalPrice);

    /**
     * Menjalankan proses transaksi pembelian kendaraan secara terenkapsulasi dan atomik.
     * <p>
     * Alur validasi:
     * <ol>
     *   <li>Validasi stok unit kendaraan</li>
     *   <li>Perhitungan diskon tier dan penambahan pajak PPN 11%</li>
     *   <li>Verifikasi kecukupan saldo rekening pelanggan</li>
     *   <li>Autodebet saldo, pengurangan stok fisik, dan penambahan unit ke garasi</li>
     *   <li>Pemberian reward/bonus tier dan pencetakan faktur digital</li>
     * </ol>
     *
     * @param vehicle objek mobil yang hendak dibeli
     * @return string faktur resmi transaksi pembelian
     * @throws DealershipException jika stok kosong atau saldo tidak mencukupi
     */
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