import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Inisialisasi Presentasi 16:9
prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Skema Warna Obsidian Luxury & Dark Tech
C_BG_DARK   = RGBColor(11, 17, 32)      # #0B1120
C_BG_CARD   = RGBColor(15, 23, 42)      # #0F172A
C_BG_INPUT  = RGBColor(30, 41, 59)      # #1E293B
C_BORDER    = RGBColor(51, 65, 85)      # #334155
C_TEXT_MAIN = RGBColor(248, 250, 252)   # #F8FAFC
C_TEXT_MUTED= RGBColor(148, 163, 184)   # #94A3B8
C_ACCENT    = RGBColor(56, 189, 248)    # #38BDF8 Sky Cyan
C_INDIGO    = RGBColor(99, 102, 241)    # #6366F1 Indigo
C_GREEN     = RGBColor(16, 185, 129)    # #10B981 Emerald
C_GOLD      = RGBColor(245, 158, 11)    # #F59E0B Amber Gold
C_RED       = RGBColor(239, 68, 68)     # #EF4444 Red

ASSET_DIR = r"d:\PraktikumOOP\EepisAutoGUI\ppt_assets"

def set_slide_background(slide, color):
    bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = color
    bg_shape.line.fill.background()
    return bg_shape

def add_header(slide, module_tag, title_text, category_text):
    # Header container
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    # Baris 1: Tag & Category
    p1 = tf.paragraphs[0]
    p1.text = f"[{module_tag.upper()}]  •  {category_text}"
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = C_ACCENT
    
    # Baris 2: Title
    p2 = tf.add_paragraph()
    p2.text = title_text
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = C_TEXT_MAIN
    p2.space_before = Pt(4)

    # Line divider
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = C_BORDER
    line.line.fill.background()

def add_card(slide, left, top, width, height, title, desc, border_color=C_BORDER, fill_color=C_BG_CARD):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.18)
    tf.margin_bottom = Inches(0.18)
    
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.bold = True
    p0.font.size = Pt(13)
    p0.font.color.rgb = C_TEXT_MAIN
    
    if desc:
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.size = Pt(10.5)
        p1.font.color.rgb = C_TEXT_MUTED
        p1.space_before = Pt(6)
    return card

def add_kpi(slide, left, top, width, height, label, value, sub, val_color=C_TEXT_MAIN):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = C_BG_CARD
    box.line.color.rgb = C_BORDER
    box.line.width = Pt(1)
    
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.12)
    
    p0 = tf.paragraphs[0]
    p0.text = label.upper()
    p0.font.size = Pt(9.5)
    p0.font.bold = True
    p0.font.color.rgb = C_TEXT_MUTED
    
    p1 = tf.add_paragraph()
    p1.text = value
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = val_color
    p1.space_before = Pt(2)
    
    if sub:
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_TEXT_MUTED
        p2.space_before = Pt(2)
    return box

def add_code_box(slide, left, top, width, height, filename, code_text):
    # Header bar IDE
    hdr = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.38))
    hdr.fill.solid()
    hdr.fill.fore_color.rgb = RGBColor(15, 23, 42)
    hdr.line.color.rgb = C_BORDER
    hdr.line.width = Pt(1)
    tf_h = hdr.text_frame
    tf_h.margin_left = Inches(0.15)
    tf_h.margin_top = Inches(0.06)
    p_h = tf_h.paragraphs[0]
    p_h.text = f"● ● ●   ☕ {filename}"
    p_h.font.size = Pt(10)
    p_h.font.bold = True
    p_h.font.color.rgb = C_TEXT_MUTED
    
    # Body IDE
    body = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top + Inches(0.38), width, height - Inches(0.38))
    body.fill.solid()
    body.fill.fore_color.rgb = RGBColor(6, 11, 20)
    body.line.color.rgb = C_BORDER
    body.line.width = Pt(1)
    tf_b = body.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = Inches(0.2)
    tf_b.margin_top = Inches(0.15)
    
    lines = code_text.strip().split("\n")
    for idx, l in enumerate(lines):
        p = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
        p.text = l
        p.font.name = "Consolas"
        p.font.size = Pt(9.5)
        if l.strip().startswith("//"):
            p.font.color.rgb = RGBColor(100, 116, 139) # comment
            p.font.italic = True
        elif "@Override" in l:
            p.font.color.rgb = RGBColor(244, 63, 94) # annotation
            p.font.bold = True
        elif any(kw in l for kw in ["public", "class", "abstract", "extends", "implements", "throw new", "if", "return", "this"]):
            p.font.color.rgb = RGBColor(129, 140, 248) # keyword
        else:
            p.font.color.rgb = RGBColor(226, 232, 240)
    return body

# ==============================================================================
# SLIDE 1: COVER
# ==============================================================================
slide1 = prs.slides.add_slide(blank_layout)
set_slide_background(slide1, C_BG_DARK)

# Logo Icon Box
logo = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(1.1), Inches(1.1))
logo.fill.solid()
logo.fill.fore_color.rgb = C_INDIGO
logo.line.fill.background()
tf_l = logo.text_frame
p_l = tf_l.paragraphs[0]
p_l.text = "E"
p_l.font.size = Pt(36)
p_l.font.bold = True
p_l.font.color.rgb = RGBColor(255, 255, 255)
p_l.alignment = PP_ALIGN.CENTER

# Title & Subtitle Box
tbox1 = slide1.shapes.add_textbox(Inches(2.1), Inches(0.8), Inches(10.4), Inches(4.5))
tf1 = tbox1.text_frame
tf1.word_wrap = True

p_brand = tf1.paragraphs[0]
p_brand.text = "EEPIS MOTORS  |  VIP LUXURY AUTO DEALERSHIP v2.0"
p_brand.font.size = Pt(13)
p_brand.font.bold = True
p_brand.font.color.rgb = C_ACCENT

p_tag = tf1.add_paragraph()
p_tag.text = "FINAL PROJECT PEMROGRAMAN BERORIENTASI OBJEK — 1 D4 IT C"
p_tag.font.size = Pt(11)
p_tag.font.bold = True
p_tag.font.color.rgb = C_GOLD
p_tag.space_before = Pt(8)

p_main = tf1.add_paragraph()
p_main.text = "Sistem Dealer Terpadu, Portofolio Aset\n& Mode Test Drive Interaktif 2D"
p_main.font.size = Pt(34)
p_main.font.bold = True
p_main.font.color.rgb = C_TEXT_MAIN
p_main.space_before = Pt(14)

p_desc = tf1.add_paragraph()
p_desc.text = "Implementasi komprehensif 4 Pilar OOP (Inheritance, Polymorphism, Encapsulation, Abstraction), Interface ITaxable, Custom Exception Handling, serta Simulasi 2D Canvas 60 FPS pada platform enterprise berbasis JavaFX."
p_desc.font.size = Pt(14)
p_desc.font.color.rgb = C_TEXT_MUTED
p_desc.space_before = Pt(14)

# Line divider
l1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.6), Inches(11.733), Inches(0.02))
l1.fill.solid()
l1.fill.fore_color.rgb = C_BORDER
l1.line.fill.background()

# Authors Box
abox = slide1.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(8.5), Inches(1.3))
atf = abox.text_frame
atf.word_wrap = True

ap0 = atf.paragraphs[0]
ap0.text = "TIM PENGEMBANG PROYEK (KELOMPOK 3):"
ap0.font.size = Pt(10)
ap0.font.bold = True
ap0.font.color.rgb = C_ACCENT

ap1 = atf.add_paragraph()
ap1.text = "1. Mustofa Barakbah (NRP: 3125600065)    •    2. Reza Ali Muhammad (NRP: 3125600061)"
ap1.font.size = Pt(14)
ap1.font.bold = True
ap1.font.color.rgb = C_TEXT_MAIN
ap1.space_before = Pt(4)

ap2 = atf.add_paragraph()
ap2.text = "Departemen Teknik Informatika — Politeknik Elektronika Negeri Surabaya (PENS)"
ap2.font.size = Pt(11)
ap2.font.color.rgb = C_TEXT_MUTED
ap2.space_before = Pt(4)

# Stack Pills Box
pbox = slide1.shapes.add_textbox(Inches(9.5), Inches(5.8), Inches(3.0), Inches(1.3))
ptf = pbox.text_frame
pp0 = ptf.paragraphs[0]
pp0.text = "TECH STACK:"
pp0.font.size = Pt(10)
pp0.font.bold = True
pp0.font.color.rgb = C_TEXT_MUTED
pp1 = ptf.add_paragraph()
pp1.text = "Java 11 / 25  •  JavaFX 21\nFXML + CSS Obsidian\nCanvas 2D Engine"
pp1.font.size = Pt(12)
pp1.font.bold = True
pp1.font.color.rgb = C_GREEN
pp1.space_before = Pt(4)

# ==============================================================================
# SLIDE 2: OVERVIEW & ARSITEKTUR SISTEM
# ==============================================================================
slide2 = prs.slides.add_slide(blank_layout)
set_slide_background(slide2, C_BG_DARK)
add_header(slide2, "Overview", "Arsitektur Sistem & Gambaran Eksekutif", "Konseptual Enterprise EEPIS Auto 2.0")

# Left Column (Cards)
add_card(slide2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(1.5),
         "🚨 Latar Belakang & Keterbatasan Konvensional",
         "Aplikasi dealer mobil umumnya bersifat katalog statis: tanpa validasi kelayakan dana otomatis, tanpa audit pajak terintegrasi, dan minim interaktivitas pengalaman berkendara.")

add_card(slide2, Inches(0.8), Inches(3.5), Inches(5.6), Inches(1.6),
         "💡 Solusi EEPIS Auto 2.0: Wealth Management Terpadu",
         "Mengintegrasikan showroom mobil mewah dengan sistem Customer Tiering otomatis berbasis saldo, portofolio aset garasi dengan grafik visual BarChart, dan proteksi transaksi autodebet.")

add_card(slide2, Inches(0.8), Inches(5.3), Inches(5.6), Inches(1.6),
         "🎮 Interaktivitas Nyata: Mode Test Drive 2D Canvas",
         "Bukan sekadar dialog teks atau suara, pengguna dapat menguji mobil impian secara langsung dalam simulasi 2D 60 FPS multi-lane racing yang dinamis dan berhadiah cashback.")

# Right Column (KPIs & Modules)
add_kpi(slide2, Inches(6.7), Inches(1.8), Inches(2.7), Inches(1.1), "Arsitektur", "MVC Terpadu", "FXML + Controller + Model", C_ACCENT)
add_kpi(slide2, Inches(9.6), Inches(1.8), Inches(2.9), Inches(1.1), "Pilar OOP", "4 Pilar Utuh", "+ Interface & Custom Exception", C_INDIGO)
add_kpi(slide2, Inches(6.7), Inches(3.1), Inches(2.7), Inches(1.1), "Total Modul", "7 Modul", "Showroom s/d VIP Lounge", C_GOLD)
add_kpi(slide2, Inches(9.6), Inches(3.1), Inches(2.9), Inches(1.1), "Simulasi Game", "60 FPS Canvas", "Geometric Physics Engine", C_GREEN)

add_card(slide2, Inches(6.7), Inches(4.4), Inches(5.8), Inches(2.5),
         "✨ 7 Modul Interaktif Dalam Satu Kendali",
         "1. Katalog Showroom (Real-time Filter & Stream API)\n2. Dasbor Portofolio Aset (Wealth Management & BarChart)\n3. Pusat Servis Berkala Resmi (Audit Saldo Enkapsulasi)\n4. Modul Pajak & Asuransi (Kontrak ITaxable PPN 11%)\n5. Trade-In Mobil (Kalkulasi Depresiasi Pasar 30%)\n6. Log Riwayat Finansial (Audit Trail Lengkap)\n7. VIP Privilege Lounge (Klaim Bonus Harian Eksklusif Tier)",
         C_ACCENT)

# ==============================================================================
# SLIDE 3: OOP 1 — ABSTRACTION & INHERITANCE
# ==============================================================================
slide3 = prs.slides.add_slide(blank_layout)
set_slide_background(slide3, C_BG_DARK)
add_header(slide3, "Pilar OOP 1", "Abstraction & Inheritance (Pewarisan Kelas)", "Fondasi Hierarki Kelas & Kontrak Sistem")

add_card(slide3, Inches(0.8), Inches(1.8), Inches(5.5), Inches(1.6),
         "🔒 Abstraction: Mencegah Instansiasi Prematur",
         "Kelas User, Customer, dan Vehicle dideklarasikan sebagai abstract class. Objek tidak boleh dibuat secara instan tanpa identitas spesifik bisnis (apakah mobil bensin/listrik atau tier pelanggan tertentu).")

add_card(slide3, Inches(0.8), Inches(3.6), Inches(5.5), Inches(1.6),
         "🌲 Hierarki Inheritance 1: Customer Tiering",
         "User (Superclass Identitas)\n └── Customer (Abstract: saldo, garasi, logika beli)\n      ├── RegularCustomer (Standard Tier)\n      ├── SilverCustomer (VIP: Diskon 5%)\n      └── GoldCustomer (VVIP: Diskon 8% + Cashback 2%)")

add_card(slide3, Inches(0.8), Inches(5.4), Inches(5.5), Inches(1.5),
         "🏎️ Hierarki Inheritance 2: Vehicle Polymorphic",
         "Vehicle (Abstract: brand, price, stock, implements ITaxable)\n ├── ElectricCar (EV: kapasitas baterai kWh & jarak tempuh)\n └── GasCar (Konvensional: kapasitas mesin cc & transmisi)")

code_veh = """// 1. Base Abstract Class dengan kontrak baku
public abstract class Vehicle implements ITaxable {
    protected String brand, model, color;
    protected double price;
    protected int stock;

    public Vehicle(String b, String m, double p, int s, String c) {
        this.brand = b; this.model = m; 
        this.price = p; this.stock = s; this.color = c;
    }

    // Method Abstrak: Wajib dioverride subclass
    public abstract String testDrive();
    public abstract String getSpecs();
}

// 2. Subclass Konkret Mewarisi Vehicle
public class ElectricCar extends Vehicle {
    private int batteryCapacity, range;

    @Override
    public String testDrive() {
        return "⚡ Zzzzz... Melaju senyap bertenaga EV!";
    }
}"""
add_code_box(slide3, Inches(6.6), Inches(1.8), Inches(5.9), Inches(5.1), "Vehicle.java & ElectricCar.java", code_veh)

# ==============================================================================
# SLIDE 4: OOP 2 — POLYMORPHISM
# ==============================================================================
slide4 = prs.slides.add_slide(blank_layout)
set_slide_background(slide4, C_BG_DARK)
add_header(slide4, "Pilar OOP 2", "Polymorphism (Dynamic Method Dispatch)", "Satu Interface, Beragam Perilaku Spesifik")

add_card(slide4, Inches(0.8), Inches(1.8), Inches(5.5), Inches(1.6),
         "🎭 Dynamic Dispatch Saat Runtime",
         "Polimorfisme memungkinkan pemanggilan method yang seragam pada tipe referensi induk (Customer atau Vehicle), namun mengeksekusi logika spesifik milik kelas turunan nyata saat aplikasi berjalan.")

add_card(slide4, Inches(0.8), Inches(3.6), Inches(5.5), Inches(1.6),
         "⚡ Contoh 1: Overriding testDrive()",
         "• GasCar menghasilkan: 'VROOOM! Suara mesin 3000cc menderu!'\n• ElectricCar menghasilkan: 'Zzzzz... Melaju senyap bertenaga EV.'\nDipanggil dinamis oleh Controller tanpa percabangan if-else.")

add_card(slide4, Inches(0.8), Inches(5.4), Inches(5.5), Inches(1.5),
         "💰 Contoh 2: Overriding calculateDiscount() & applyBonus()",
         "• GoldCustomer: Diskon 8% + Cashback Saldo 2% instan\n• SilverCustomer: Diskon 5% + Paket Servis Gratis\n• RegularCustomer: Diskon 0% (Harga OTR standar)")

code_poly = """// Pemanggilan Polimorfis Seragam di Controller
Vehicle car = showroom.get(idx);
String sound = car.testDrive(); // Polimorfik!

double discount = currentUser.calculateDiscount(car.getPrice());
String bonus = currentUser.applyBonus(finalPrice);

// Implementasi di Subclass GoldCustomer
public class GoldCustomer extends Customer {
    @Override
    public double calculateDiscount(double price) {
        return price * 0.08; // Diskon 8%
    }

    @Override
    public String applyBonus(double finalPrice) {
        double cashback = finalPrice * 0.02;
        this.bankBalance += cashback; // Refund saldo
        return "Cashback Saldo Rp " + 
               String.format("%,.0f", cashback);
    }
}"""
add_code_box(slide4, Inches(6.6), Inches(1.8), Inches(5.9), Inches(5.1), "PrimaryController.java & GoldCustomer.java", code_poly)

# ==============================================================================
# SLIDE 5: OOP 3 — ENCAPSULATION
# ==============================================================================
slide5 = prs.slides.add_slide(blank_layout)
set_slide_background(slide5, C_BG_DARK)
add_header(slide5, "Pilar OOP 3", "Encapsulation & Integritas Data Finansial", "Proteksi Mutasi Saldo & Garasi Terkontrol")

add_card(slide5, Inches(0.8), Inches(1.8), Inches(5.5), Inches(1.6),
         "🛡️ Proteksi Atribut Kritis (Data Hiding)",
         "Variabel penting seperti bankBalance dideklarasikan dengan modifier protected/private. Variabel ini tidak dapat dimanipulasi secara acak dari luar kelas, melainkan hanya via transaksi resmi berintegritas.")

add_card(slide5, Inches(0.8), Inches(3.6), Inches(5.5), Inches(1.6),
         "⚙️ Alur Transaksi Atomik Terenkapsulasi",
         "Method buyVehicle() menjalankan validasi berlapis:\n1. Cek ketersediaan stok fisik unit\n2. Hitung diskon tier & beban PPN 11%\n3. Validasi kecukupan saldo rekening\n4. Autodebet saldo & transfer unit ke garasi")

add_card(slide5, Inches(0.8), Inches(5.4), Inches(5.5), Inches(1.5),
         "📋 Mutasi Resmi Lainnya",
         "• prosesServis(): Memotong Rp 2.500.000 secara terenkapsulasi.\n• prosesTradeIn(): Mengkreditkan dana penjualan 70% kembali ke saldo pelanggan.")

code_encap = """public String buyVehicle(Vehicle vehicle) 
        throws DealershipException {
    // 1. Validasi stok unit
    if (vehicle.getStock() <= 0) {
        throw new DealershipException("Stok Habis!");
    }

    double discount = calculateDiscount(vehicle.getPrice());
    double finalPrice = (vehicle.getPrice() - discount) 
                      + vehicle.calculateTax(vehicle.getPrice());

    // 2. Validasi kecukupan dana pelanggan
    if (this.bankBalance < finalPrice) {
        throw new DealershipException("Saldo Kurang! " +
            "Kekurangan: Rp " + (finalPrice - this.bankBalance));
    }

    // 3. Mutasi saldo internal (Encapsulation)
    this.bankBalance -= finalPrice;
    vehicle.decreaseStock();
    this.garage.add(vehicle);

    return TransactionReceipt.generateReceipt(this, vehicle...);
}"""
add_code_box(slide5, Inches(6.6), Inches(1.8), Inches(5.9), Inches(5.1), "Customer.java — buyVehicle()", code_encap)

# ==============================================================================
# SLIDE 6: OOP 4 — INTERFACE & CUSTOM EXCEPTION
# ==============================================================================
slide6 = prs.slides.add_slide(blank_layout)
set_slide_background(slide6, C_BG_DARK)
add_header(slide6, "Pilar OOP 4", "Interface ITaxable & Custom Exception Handling", "Kontrak Baku Perpajakan & Ketahanan Sistem (Robustness)")

add_card(slide6, Inches(0.8), Inches(1.8), Inches(5.5), Inches(2.4),
         "📜 Interface ITaxable: Kontrak Beban Pajak",
         "Interface mendefinisikan kontrak hukum perpajakan yang wajib diimplementasikan oleh seluruh kelas kendaraan.\n\n"
         "public interface ITaxable {\n"
         "    double calculateTax(double priceAfterDiscount);\n"
         "    double getTaxRate(); // 11% PPN Standar\n"
         "}\n\n"
         "Setiap unit kendaraan otomatis memiliki method kalkulasi pajak tanpa menduplikasi logika kode.",
         C_INDIGO)

add_card(slide6, Inches(0.8), Inches(4.4), Inches(5.5), Inches(2.5),
         "⚠️ Custom Exception: DealershipException",
         "Membangun kelas mandiri turunan java.lang.Exception untuk menangkap anomali bisnis (stok kosong atau saldo tidak mencukupi).\n\n"
         "public class DealershipException extends Exception {\n"
         "    public DealershipException(String message) {\n"
         "        super(message);\n"
         "    }\n"
         "}",
         C_GOLD)

code_exc = """// Penanganan Try-Catch di PrimaryController
showModalAnimasi("Memproses Pembelian...", () -> {
    try {
        // Eksekusi method yang melempar Exception
        String receipt = currentUser.buyVehicle(car);
        transactionHistory.add(0, "BELI: " + car.getModel());
        
        updateSemuaData();
        txtReceiptContent.setText(receipt);
        receiptBox.setVisible(true);

    } catch (DealershipException ex) {
        // Tangkap Exception: Aplikasi tetap aman tanpa crash!
        closeModal();
        
        // Render notifikasi Toast Merah elegan
        showToast("Transaksi Ditolak: " + ex.getMessage(), true);
    }
});"""
add_code_box(slide6, Inches(6.6), Inches(1.8), Inches(5.9), Inches(5.1), "PrimaryController.java — Exception Handling", code_exc)

# ==============================================================================
# SLIDE 7: INOVASI TEST DRIVE 2D MINI GAME
# ==============================================================================
slide7 = prs.slides.add_slide(blank_layout)
set_slide_background(slide7, C_BG_DARK)
add_header(slide7, "Inovasi Utama", "Simulasi Test Drive 2D Canvas Game (60 FPS)", "Game Engine Interaktif Menggunakan JavaFX GraphicsContext")

add_card(slide7, Inches(0.8), Inches(1.8), Inches(5.5), Inches(1.6),
         "🎮 Dari Teks Statis Menjadi Game Kemudi Nyata",
         "Menggantikan animasi dialog sederhana dengan mini-game racing 2D interaktif berbasis Canvas dan AnimationTimer. Pengguna mengendalikan mobil di jalan raya 3 jalur.")

add_card(slide7, Inches(0.8), Inches(3.6), Inches(5.5), Inches(1.6),
         "⚡ Fisika Berbeda: EV vs Gas",
         "• ElectricCar (EV): Torsi instan tinggi, akselerasi awal lebih cepat, efek partikel glow biru.\n• GasCar (Bensin): Kecepatan bertahap, efek asap knalpot menderu, top speed tinggi.")

add_card(slide7, Inches(0.8), Inches(5.4), Inches(5.5), Inches(1.5),
         "🕹️ Mekanisme Permainan & Reward Finansial",
         "• Kontrol: Tombol [←] [→] atau [A] [D]\n• 3 Nyawa (● ● ●), rintangan mobil berwarna, koin emas\n• Reward nyata: Koin menambah saldo rekening pembeli!")

# Image Container Right
img_game = os.path.join(ASSET_DIR, "1_gameplay_test_drive.png")
if not os.path.exists(img_game):
    img_game = r"C:\Users\musto\.gemini\antigravity\brain\8057df29-e5b1-42be-9daf-f109f1bece7c\.user_uploaded\media_1791777782622_1953448b.png"

if os.path.exists(img_game):
    slide7.shapes.add_picture(img_game, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.3))
    add_card(slide7, Inches(6.8), Inches(6.2), Inches(5.7), Inches(0.7),
             "🏆 60 FPS Canvas Engine", "Full geometric rendering bebas glitch font emoji. Dilengkapi Speedometer km/h.", C_ACCENT)

# ==============================================================================
# SLIDE 8: DEMONSTRASI SHOWROOM & HASIL TEST DRIVE
# ==============================================================================
slide8 = prs.slides.add_slide(blank_layout)
set_slide_background(slide8, C_BG_DARK)
add_header(slide8, "Demonstrasi UI", "Katalog Showroom & Hasil Test Drive", "Pencarian Real-Time Stream API & Scoring Game")

# Left Column (Showroom)
img_show = os.path.join(ASSET_DIR, "2_showroom_modern.png")
if not os.path.exists(img_show):
    img_show = os.path.join(ASSET_DIR, "pptx_slide_8_pic_9.png")
if os.path.exists(img_show):
    slide8.shapes.add_picture(img_show, Inches(0.8), Inches(1.8), Inches(5.6), Inches(3.6))

add_card(slide8, Inches(0.8), Inches(5.6), Inches(5.6), Inches(1.4),
         "🏎️ Katalog Showroom Pintar",
         "• Java Stream API filtering instan berdasarkan teks & combobox\n• Badge EV / GAS, stok unit, diskon tier, dan beban PPN otomatis\n• Tombol 'Test Drive' & 'Beli Unit' responsif", C_ACCENT)

# Right Column (Hasil Test Drive)
img_res = os.path.join(ASSET_DIR, "3_hasil_test_drive.png")
if not os.path.exists(img_res):
    img_res = os.path.join(ASSET_DIR, "pptx_slide_9_pic_8.png")
if os.path.exists(img_res):
    slide8.shapes.add_picture(img_res, Inches(6.8), Inches(1.8), Inches(5.7), Inches(3.6))

add_card(slide8, Inches(6.8), Inches(5.6), Inches(5.7), Inches(1.4),
         "🏆 Kartu Hasil Test Drive & Polimorfisme",
         "• Menampilkan skor akhir, jarak tempuh, dan gelar ranking driver\n• Menampilkan output polimorfik testDrive() suara kendaraan\n• Tombol 'Play Again' atau 'Tutup' langsung ke showroom", C_GOLD)

# ==============================================================================
# SLIDE 9: DEMONSTRASI DASBOR PORTOFOLIO & GARASI
# ==============================================================================
slide9 = prs.slides.add_slide(blank_layout)
set_slide_background(slide9, C_BG_DARK)
add_header(slide9, "Demonstrasi UI", "Dasbor Portofolio Aset & Garasi Pelanggan", "Wealth Management & Visualisasi Grafik BarChart")

# Left Image (Dashboard)
img_dash = os.path.join(ASSET_DIR, "4_dasbor_portofolio.png")
if not os.path.exists(img_dash):
    img_dash = os.path.join(ASSET_DIR, "pptx_slide_10_pic_10.png")
if os.path.exists(img_dash):
    slide9.shapes.add_picture(img_dash, Inches(0.8), Inches(1.8), Inches(6.6), Inches(4.3))

add_card(slide9, Inches(0.8), Inches(6.2), Inches(6.6), Inches(0.8),
         "📊 Wealth Management Real-Time", "Membaca data langsung dari memori garasi Customer dan menghitung nilai portofolio.", C_GREEN)

# Right Details
add_kpi(slide9, Inches(7.7), Inches(1.8), Inches(2.3), Inches(1.1), "Total Unit", "2 Unit", "Di garasi klien", C_TEXT_MAIN)
add_kpi(slide9, Inches(10.2), Inches(1.8), Inches(2.3), Inches(1.1), "Nilai Aset", "Rp 4,8 M", "Akumulasi nilai pasar", C_GREEN)

add_card(slide9, Inches(7.7), Inches(3.1), Inches(4.8), Inches(3.9),
         "📈 Visualisasi BarChart & Sertifikat",
         "• BarChart JavaFX Terbaca Sempurna:\n  Menampilkan grafik nilai aset per model mobil (Juta Rp) dengan gradient emerald styling.\n\n"
         "• Sertifikat Kepemilikan (Garasi):\n  Setiap mobil yang dibeli tercatat dengan stempel resmi LUNAS, nomor registrasi kepemilikan unik (#01, #02), rincian spesifikasi teknis, serta beban PPN.\n\n"
         "• Animasi Transisi Halus:\n  FadeTransition staggered saat beralih ke halaman portofolio.",
         C_ACCENT)

# ==============================================================================
# SLIDE 10: DEMONSTRASI SERVIS, PAJAK & TRADE-IN
# ==============================================================================
slide10 = prs.slides.add_slide(blank_layout)
set_slide_background(slide10, C_BG_DARK)
add_header(slide10, "Demonstrasi UI", "Pusat Servis, Kalkulasi Pajak & Faktur Transaksi", "Ekosistem Purna Jual & Transaksi Terverifikasi")

# Left Column (Servis Image)
img_serv = os.path.join(ASSET_DIR, "5_servis.png")
if not os.path.exists(img_serv):
    img_serv = os.path.join(ASSET_DIR, "pptx_slide_11_pic_7.png")
if os.path.exists(img_serv):
    slide10.shapes.add_picture(img_serv, Inches(0.8), Inches(1.8), Inches(5.6), Inches(3.6))

add_card(slide10, Inches(0.8), Inches(5.6), Inches(5.6), Inches(1.4),
         "🔧 Pusat Servis Berkala",
         "• Pemeliharaan mesin resmi Rp 2.500.000\n• Memotong bankBalance secara aman via Encapsulation\n• Tercatat langsung di log riwayat transaksi", C_ACCENT)

# Right Column (Faktur Image)
img_fak = os.path.join(ASSET_DIR, "pptx_slide_11_pic_6.png")
if os.path.exists(img_fak):
    slide10.shapes.add_picture(img_fak, Inches(6.8), Inches(1.8), Inches(5.7), Inches(3.6))

add_card(slide10, Inches(6.8), Inches(5.6), Inches(5.7), Inches(1.4),
         "🧾 Faktur Transaksi & Kalkulasi PPN 11%",
         "• Rincian pembelian: Harga OTR, diskon tier, dan PPN 11%\n• Hadiah bonus eksklusif (Cashback Saldo & Asuransi)\n• Data audit trail dicetak secara terstruktur dan profesional", C_GREEN)

# ==============================================================================
# SLIDE 11: UML CLASS DIAGRAM
# ==============================================================================
slide11 = prs.slides.add_slide(blank_layout)
set_slide_background(slide11, C_BG_DARK)
add_header(slide11, "Pemetaan Sistem", "UML Class Diagram & Relasi Antar Objek", "Struktur Kelas, Hubungan Inheritance, Realization & Aggregation")

# Left Box: Hierarki Customer
add_card(slide11, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.1),
         "👤 Hierarki Customer",
         "«abstract» User\n"
         "  - id: String\n"
         "  - name: String\n"
         "  + displayProfile(): void\n"
         "          ▲\n"
         "          │ (Inheritance)\n"
         "«abstract» Customer\n"
         "  # bankBalance: double\n"
         "  + garage: List<Vehicle>\n"
         "  + buyVehicle(v): String\n"
         "  + calculateDiscount(p)*\n"
         "  + applyBonus(fp)*\n"
         "          ▲\n"
         "   ┌──────┼──────┐\n"
         "Regular  Silver   Gold\n"
         "(0%)     (5%)     (8%+2%)",
         C_INDIGO)

# Center Box: Controller (Aggregate Root)
add_card(slide11, Inches(4.7), Inches(1.8), Inches(3.9), Inches(5.1),
         "🎮 PrimaryController\n(Aggregate Root)",
         "Hubungan Sistem:\n"
         "• Mengelola sesi Customer aktif\n"
         "• Mengelola koleksi showroom (List<Vehicle>)\n"
         "• Mengorkestrasi 7 modul FXML\n"
         "• Menjalankan Game Engine Canvas 2D\n\n"
         "       ─── Agregasi ───>\n"
         "Customer memiliki List<Vehicle> garage\n\n"
         "Exception Handling:\n"
         "• Menangkap DealershipException\n"
         "• Merender Toast & Modal Faktur",
         C_ACCENT)

# Right Box: Hierarki Vehicle & Interface
add_card(slide11, Inches(8.9), Inches(1.8), Inches(3.6), Inches(5.1),
         "🏎️ Hierarki Vehicle & Tax",
         "«interface» ITaxable\n"
         "  + calculateTax(p): double\n"
         "  + getTaxRate(): double\n"
         "          ▲\n"
         "          ┊ (Realization)\n"
         "«abstract» Vehicle\n"
         "  # brand, model, color: String\n"
         "  # price: double\n"
         "  # stock: int\n"
         "  + testDrive()*: String\n"
         "  + getSpecs()*: String\n"
         "          ▲\n"
         "     ┌────┴────┐\n"
         "  GasCar   ElectricCar\n"
         "  (cc, AT)  (kWh, km)",
         C_GREEN)

# ==============================================================================
# SLIDE 12: KESIMPULAN & PENUTUP
# ==============================================================================
slide12 = prs.slides.add_slide(blank_layout)
set_slide_background(slide12, C_BG_DARK)

tbox_end = slide12.shapes.add_textbox(Inches(1.5), Inches(1.2), Inches(10.333), Inches(4.5))
tf_end = tbox_end.text_frame
tf_end.word_wrap = True

p_end0 = tf_end.paragraphs[0]
p_end0.text = "EEPIS MOTORS — VIP DEALERSHIP SYSTEM v2.0"
p_end0.font.size = Pt(13)
p_end0.font.bold = True
p_end0.font.color.rgb = C_ACCENT

p_end1 = tf_end.add_paragraph()
p_end1.text = "Kesimpulan & Pembuktian Pilar OOP"
p_end1.font.size = Pt(32)
p_end1.font.bold = True
p_end1.font.color.rgb = C_TEXT_MAIN
p_end1.space_before = Pt(8)

p_end2 = tf_end.add_paragraph()
p_end2.text = (
    "✅ Modular & Scalable: Penerapan Abstraction dan Inheritance memungkinkan penambahan tipe mobil atau tier baru tanpa merusak kode lama.\n\n"
    "✅ Integritas Data Terjamin: Encapsulation menjaga saldo bank dan status inventaris unit garasi dari manipulasi ilegal.\n\n"
    "✅ Fleksibel & Dinamis: Polymorphism dan Interface ITaxable menyatukan perhitungan pajak dan pengalaman test drive lintas entitas.\n\n"
    "✅ Robustness: Custom DealershipException menjamin aplikasi tahan terhadap error tanpa pernah crash di hadapan pengguna.\n\n"
    "✅ Engaging & Modern: Simulasi 2D Canvas Game dan UI Obsidian membuktikan JavaFX mampu menyajikan pengalaman aplikasi setara standar industri global."
)
p_end2.font.size = Pt(13)
p_end2.font.color.rgb = C_TEXT_MUTED
p_end2.space_before = Pt(14)

# Footer Box
fbox = slide12.shapes.add_textbox(Inches(1.5), Inches(5.8), Inches(10.333), Inches(1.0))
ftf = fbox.text_frame
fp0 = ftf.paragraphs[0]
fp0.text = "Terima Kasih atas Perhatian Bapak/Ibu Dosen Penguji"
fp0.font.size = Pt(20)
fp0.font.bold = True
fp0.font.color.rgb = C_GOLD

fp1 = ftf.add_paragraph()
fp1.text = "Kelompok 3 (1 D4 IT C) — Sesi Tanya Jawab Dibuka"
fp1.font.size = Pt(13)
fp1.font.color.rgb = C_ACCENT
fp1.space_before = Pt(4)

# Simpan PPTX Final
out_pptx_path = r"d:\PraktikumOOP\EepisAutoGUI\EEPIS_Auto_VIP_Dealership_v2.pptx"
prs.save(out_pptx_path)
print(f"Presentation saved successfully to: {out_pptx_path} ({len(prs.slides)} slides)")
