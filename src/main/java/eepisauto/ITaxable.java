package eepisauto;

/**
 * Interface ITaxable mendefinisikan kontrak perpajakan yang wajib
 * diimplementasikan oleh setiap entitas kena pajak pada ekosistem EEPIS Auto Dealership.
 * <p>
 * Konsep OOP: <b>Interface</b> &amp; <b>Polymorphism</b> (Abstraksi Kontrak Perpajakan).
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public interface ITaxable {

    /**
     * Menghitung nilai nominal pajak (PPN) yang dikenakan terhadap harga kendaraan setelah diskon.
     *
     * @param priceAfterDiscount harga bersih kendaraan setelah pemotongan diskon tier pelanggan
     * @return nominal pajak yang harus dibayarkan dalam rupiah
     */
    double calculateTax(double priceAfterDiscount);

    /**
     * Mengembalikan persentase tarif pajak yang berlaku standar (misalnya 11% PPN).
     *
     * @return nilai rasio pajak dalam bentuk desimal (contoh: 0.11 untuk PPN 11%)
     */
    double getTaxRate();
}