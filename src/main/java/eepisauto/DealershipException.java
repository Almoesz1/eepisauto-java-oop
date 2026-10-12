package eepisauto;

/**
 * Custom Exception mandiri untuk menangani seluruh kondisi anomali bisnis
 * dalam operasional EEPIS Auto VIP Dealership (seperti stok kosong atau saldo tidak mencukupi).
 * <p>
 * Konsep OOP: <b>Custom Exception Handling</b> &amp; <b>Robustness</b>.
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public class DealershipException extends Exception {

    /**
     * Mengonstruksi DealershipException baru dengan pesan rincian kesalahan.
     *
     * @param message pesan deskriptif alasan penolakan transaksi
     */
    public DealershipException(String message) {
        super(message);
    }
}