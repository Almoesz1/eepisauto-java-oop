package eepisauto;

/**
 * Kelas utilitas untuk memformat dan mencetak faktur bukti transaksi resmi EEPIS Auto VIP.
 * <p>
 * Menghasilkan rincian komprehensif mulai dari data pelanggan, spesifikasi kendaraan,
 * kalkulasi harga OTR, diskon tier, beban PPN 11%, bonus reward, dan sisa saldo akhir.
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public class TransactionReceipt {

    /**
     * Menghasilkan teks faktur transaksi pembelian yang rapi dan terstruktur.
     *
     * @param customer objek pelanggan yang melakukan transaksi
     * @param vehicle objek kendaraan yang dibeli
     * @param finalPrice total harga akhir yang telah dibayarkan
     * @param discount nilai potongan diskon tier
     * @param tax nilai beban PPN 11%
     * @param bonus rincian bonus hadiah yang didapatkan
     * @return string struk faktur pembelian
     */
    public static String generateReceipt(Customer customer, Vehicle vehicle, double finalPrice, double discount, double tax, String bonus) {
        StringBuilder sb = new StringBuilder();
        sb.append("=======================================================\n");
        sb.append("            FAKTUR PEMBELIAN - EEPIS AUTO VIP          \n");
        sb.append("=======================================================\n");
        sb.append("DATA PELANGGAN\n");
        sb.append("Nama / ID  : ").append(customer.getName()).append(" (").append(customer.getId()).append(")\n");
        sb.append("Status VIP : ").append(customer.getTierName()).append("\n");
        sb.append("-------------------------------------------------------\n");
        sb.append("DETAIL KENDARAAN\n");
        sb.append("Unit       : ").append(vehicle.getBrand()).append(" ").append(vehicle.getModel()).append("\n");
        sb.append("Warna      : ").append(vehicle.getColor()).append("\n");
        sb.append("Spesifikasi: ").append(vehicle.getSpecs()).append("\n");
        sb.append("-------------------------------------------------------\n");
        sb.append("RINCIAN PEMBAYARAN\n");
        sb.append(String.format("Harga OTR  : Rp %,.0f\n", vehicle.getPrice()));
        sb.append(String.format("Diskon Tier: -Rp %,.0f\n", discount));
        sb.append(String.format("PPN (11%%)  : +Rp %,.0f\n", tax)); 
        sb.append(String.format("TOTAL BAYAR: Rp %,.0f\n", finalPrice));
        sb.append("-------------------------------------------------------\n");
        sb.append("BONUS & HADIAH (Sesuai Tier)\n");
        sb.append(">> ").append(bonus).append("\n");
        sb.append("-------------------------------------------------------\n");
        sb.append(String.format("Sisa Saldo : Rp %,.0f\n", customer.getBankBalance()));
        sb.append("=======================================================\n");
        sb.append("    Terima kasih telah berbelanja di EEPIS AUTO!     \n");
        
        System.out.println(sb.toString()); 
        return sb.toString(); 
    }
}