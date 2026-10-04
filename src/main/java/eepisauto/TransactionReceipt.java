package eepisauto;

public class TransactionReceipt {
    // Tambahkan parameter String bonus di akhir
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