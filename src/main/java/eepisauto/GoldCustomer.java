package eepisauto;

/**
 * Subclass konkret yang merepresentasikan Pelanggan Kasta Tertinggi (Gold VVIP).
 * <p>
 * Berhak mendapatkan potongan diskon pembelian mobil sebesar 8%, proteksi asuransi all-risk 3 tahun,
 * serta fasilitas cashback tunai sebesar 2% yang otomatis dikreditkan kembali ke saldo rekening.
 * <p>
 * Konsep OOP: <b>Inheritance</b> &amp; <b>Polymorphism (Method Overriding)</b>.
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public class GoldCustomer extends Customer {

    /**
     * Mengonstruksi pelanggan kategori Gold VVIP.
     *
     * @param id nomor identitas pelanggan
     * @param name nama lengkap pelanggan
     * @param balance saldo rekening pelanggan
     */
    public GoldCustomer(String id, String name, double balance) {
        super(id, name, balance);
    }

    /**
     * {@inheritDoc}
     * Mengembalikan identitas tier "Gold VVIP".
     */
    @Override
    public String getTierName() {
        return "Gold VVIP";
    }

    /**
     * {@inheritDoc}
     * Pelanggan Gold mendapatkan potongan diskon maksimal 8% dari harga mobil.
     */
    @Override
    public double calculateDiscount(double price) {
        return price * 0.08;
    }

    /**
     * {@inheritDoc}
     * Mencetak keterangan profil pengguna Sultan Gold VVIP ke konsol log.
     */
    @Override
    public void displayProfile() {
        System.out.println("Login: Sultan VVIP");
    }

    /**
     * {@inheritDoc}
     * Menerapkan reward cashback saldo instan sebesar 2% dan asuransi all-risk 3 tahun.
     * Mengubah variabel enkapsulasi {@code bankBalance} secara aman di internal kelas.
     */
    @Override
    public String applyBonus(double finalPrice) {
        double cashback = finalPrice * 0.02; // Dapat Cashback Saldo 2%
        this.bankBalance += cashback;        // Saldo direfund sebagian secara aman
        
        return "Cashback Saldo Rp " + String.format("%,.0f", cashback) + " & Asuransi All-Risk 3 Thn";
    }
}