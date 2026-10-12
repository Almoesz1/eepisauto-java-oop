package eepisauto;

/**
 * Subclass konkret yang merepresentasikan Pelanggan Tier Standar (Regular Customer).
 * <p>
 * Pelanggan kategori ini belum memenuhi batas saldo minimum VIP sehingga
 * tidak mendapatkan potongan diskon harga maupun bonus saldo khusus.
 * <p>
 * Konsep OOP: <b>Inheritance</b> &amp; <b>Polymorphism (Method Overriding)</b>.
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public class RegularCustomer extends Customer {

    /**
     * Mengonstruksi pelanggan kategori Regular.
     *
     * @param id nomor identitas pelanggan
     * @param name nama lengkap pelanggan
     * @param balance saldo awal rekening
     */
    public RegularCustomer(String id, String name, double balance) {
        super(id, name, balance);
    }

    /**
     * {@inheritDoc}
     * Mengembalikan identitas tier "Regular Tier".
     */
    @Override
    public String getTierName() {
        return "Regular Tier";
    }

    /**
     * {@inheritDoc}
     * Pelanggan Regular tidak mendapatkan diskon (0%).
     */
    @Override
    public double calculateDiscount(double price) {
        return 0.0;
    }

    /**
     * {@inheritDoc}
     * Mencetak keterangan profil pengguna biasa ke konsol log.
     */
    @Override
    public void displayProfile() {
        System.out.println("Login: Regular Customer");
    }

    /**
     * {@inheritDoc}
     * Pelanggan Regular tidak mendapatkan paket bonus khusus.
     */
    @Override
    public String applyBonus(double finalPrice) {
        return "- (Tier Reguler tidak mendapat bonus khusus)";
    }
}