package eepisauto;

/**
 * Subclass konkret yang merepresentasikan Pelanggan Tier Prioritas Menengah (Silver VIP).
 * <p>
 * Berhak mendapatkan potongan diskon pembelian mobil sebesar 3% dan paket bonus servis 1 tahun.
 * <p>
 * Konsep OOP: <b>Inheritance</b> &amp; <b>Polymorphism (Method Overriding)</b>.
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public class SilverCustomer extends Customer {

    /**
     * Mengonstruksi pelanggan kategori Silver VIP.
     *
     * @param id nomor identitas pelanggan
     * @param name nama lengkap pelanggan
     * @param balance saldo rekening pelanggan
     */
    public SilverCustomer(String id, String name, double balance) {
        super(id, name, balance);
    }

    /**
     * {@inheritDoc}
     * Mengembalikan identitas tier "Silver VIP".
     */
    @Override
    public String getTierName() {
        return "Silver VIP";
    }

    /**
     * {@inheritDoc}
     * Pelanggan Silver mendapatkan diskon sebesar 3% dari harga mobil.
     */
    @Override
    public double calculateDiscount(double price) {
        return price * 0.03;
    }

    /**
     * {@inheritDoc}
     * Mencetak keterangan profil pengguna Silver VIP ke konsol log.
     */
    @Override
    public void displayProfile() {
        System.out.println("Login: Silver VIP");
    }

    /**
     * {@inheritDoc}
     * Memberikan paket keuntungan gratis servis 1 tahun dan merchandise resmi.
     */
    @Override
    public String applyBonus(double finalPrice) {
        return "Gratis Servis 1 Tahun & Merchandise Jaket EepisAuto";
    }
}