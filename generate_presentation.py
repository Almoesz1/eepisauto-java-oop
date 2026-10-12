import os, base64, io
from PIL import Image

scratch = "/home/rezaali/.gemini/antigravity-cli/brain/08aa2cda-2b2b-447c-ba69-bb66915fa9d7/scratch"
images_config = [
    ("img_login", "1_login.png", 900),
    ("img_showroom", "2_showroom.png", 960),
    ("img_gameplay", "4_playing.png", 900),
    ("img_result", "8_result.png", 900),
    ("img_garasi", "9_garasi.png", 960),
    ("img_riwayat", "10_riwayat.png", 900),
    ("img_servis", "11_servis.png", 900),
    ("img_pajak", "13_pajak.png", 900),
    ("img_tradein", "14_tradein.png", 900),
    ("img_rewards", "16_rewards_claimed.png", 900),
    ("img_receipt", "7_receipt.png", 900),
]

img_data = {}
for tag, fname, max_w in images_config:
    p = os.path.join(scratch, fname)
    if os.path.exists(p):
        img = Image.open(p)
        if img.width > max_w:
            r = float(max_w) / img.width
            img = img.resize((max_w, int(img.height * r)), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=82, method=6)
        b64 = base64.b64encode(buf.getvalue()).decode('ascii')
        img_data[tag] = f"data:image/webp;base64,{b64}"
    else:
        img_data[tag] = ""

html_template = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EEPIS MOTORS — Presentasi Dokumentasi Proyek OOP & GUI JavaFX</title>
<style>
/* ==========================================================
   PRESENTATION STYLING — MODERN SLIDE DECK ENGINE
   ========================================================== */
:root {
  --bg-app: #0f172a;
  --bg-slide: #ffffff;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --text-light: #94a3b8;
  --accent: #4f46e5;
  --accent-light: #eef2ff;
  --accent-dark: #3730a3;
  --success: #16a34a;
  --success-bg: #dcfce7;
  --danger: #dc2626;
  --danger-bg: #fee2e2;
  --warning: #d97706;
  --warning-bg: #fef3c7;
  --border: #e2e8f0;
  --card-bg: #f8fafc;
  --slide-w: 1280px;
  --slide-h: 720px;
  --radius-lg: 20px;
  --radius-md: 12px;
  --radius-sm: 8px;
  --shadow-sm: 0 2px 4px rgba(15, 23, 42, 0.05);
  --shadow-md: 0 8px 24px rgba(15, 23, 42, 0.08);
  --shadow-lg: 0 20px 40px rgba(15, 23, 42, 0.16);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--bg-app);
  color: var(--text-main);
  overflow: hidden;
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  user-select: none;
}

/* PROGRESS BAR */
#progressBar {
  position: fixed;
  top: 0;
  left: 0;
  height: 4px;
  background: linear-gradient(90deg, #4f46e5, #06b6d4, #10b981);
  width: 0%;
  transition: width 0.3s ease;
  z-index: 9999;
}

/* STAGE CONTAINER */
#stage {
  position: relative;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

/* SLIDE SCALER */
#slideContainer {
  position: relative;
  width: var(--slide-w);
  height: var(--slide-h);
  transform-origin: center center;
  transition: transform 0.15s ease-out;
}

/* INDIVIDUAL SLIDE */
.slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--bg-slide);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: 44px 54px;
  display: flex;
  flex-direction: column;
  opacity: 0;
  pointer-events: none;
  transform: translateX(40px) scale(0.98);
  transition: opacity 0.35s ease, transform 0.35s ease;
  overflow: hidden;
}

.slide.active {
  opacity: 1;
  pointer-events: auto;
  transform: translateX(0) scale(1);
  z-index: 10;
}

.slide.prev {
  opacity: 0;
  transform: translateX(-40px) scale(0.98);
}

/* HEADER COMPONENT */
.slide-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
  padding-bottom: 14px;
  border-bottom: 1.5px solid var(--border);
}

.slide-header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.badge-module {
  background: var(--accent-light);
  color: var(--accent);
  font-weight: 700;
  font-size: 12px;
  padding: 5px 12px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.slide-title {
  font-size: 26px;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.5px;
}

.slide-category {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-muted);
}

.slide-body {
  flex: 1;
  display: flex;
  gap: 24px;
  min-height: 0;
  overflow: hidden;
}

/* COMMON LAYOUTS */
.col { flex: 1; display: flex; flex-direction: column; gap: 16px; min-height: 0; }
.col-2 { flex: 2; display: flex; flex-direction: column; gap: 16px; min-height: 0; }
.col-1-5 { flex: 1.5; display: flex; flex-direction: column; gap: 16px; min-height: 0; }
.row { display: flex; gap: 16px; }

/* CARDS */
.card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.card.highlight {
  border-color: #c7d2fe;
  background: #fcfdff;
}

.card-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-main);
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-desc {
  font-size: 13px;
  line-height: 1.5;
  color: var(--text-muted);
}

/* PILL BADGES */
.pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 700;
}
.pill-accent { background: var(--accent-light); color: var(--accent); }
.pill-success { background: var(--success-bg); color: var(--success); }
.pill-danger { background: var(--danger-bg); color: var(--danger); }
.pill-warning { background: var(--warning-bg); color: var(--warning); }

/* STATS KPI */
.kpi-box {
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.kpi-label { font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
.kpi-value { font-size: 22px; font-weight: 800; color: var(--text-main); }
.kpi-sub { font-size: 11px; color: var(--text-muted); }

/* CODE BOX */
.code-box {
  background: #0f172a;
  color: #e2e8f0;
  border-radius: var(--radius-md);
  padding: 14px 18px;
  font-family: "JetBrains Mono", "Consolas", "Fira Code", monospace;
  font-size: 11.5px;
  line-height: 1.55;
  overflow: auto;
  border: 1px solid #1e293b;
  flex: 1;
}
.code-kw { color: #818cf8; font-weight: bold; }
.code-type { color: #38bdf8; }
.code-str { color: #34d399; }
.code-num { color: #f59e0b; }
.code-comment { color: #64748b; font-style: italic; }

/* SCREENSHOT PREVIEWS */
.screenshot-container {
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.screenshot-container img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: contain;
}

/* LIST ITEMS WITH BULLETS */
.feature-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 13.5px;
  color: var(--text-main);
  line-height: 1.45;
}
.feature-icon {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--accent-light);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 800;
  flex-shrink: 0;
  margin-top: 1px;
}

/* COVER SLIDE SPECIAL */
.slide-cover {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 60%, #eef2ff 100%);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.cover-brand {
  display: flex;
  align-items: center;
  gap: 14px;
}
.brand-icon {
  width: 52px;
  height: 52px;
  background: var(--accent);
  color: white;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  font-weight: 800;
  box-shadow: 0 10px 20px rgba(79, 70, 229, 0.3);
}
.brand-name {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: var(--text-main);
}
.brand-tag {
  font-size: 13px;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 0.5px;
}
.cover-title {
  font-size: 46px;
  font-weight: 900;
  line-height: 1.15;
  color: var(--text-main);
  letter-spacing: -1px;
  margin-bottom: 12px;
}
.cover-desc {
  font-size: 18px;
  color: var(--text-muted);
  max-width: 880px;
  line-height: 1.5;
}
.cover-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding-top: 24px;
  border-top: 1.5px solid var(--border);
}
.author-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.author-name {
  font-size: 18px;
  font-weight: 800;
  color: var(--text-main);
}
.author-nrp {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent);
}
.author-dept {
  font-size: 13px;
  color: var(--text-muted);
}


/* IDE CODE WINDOW STYLING */
.ide-window {
  background: #0b1120;
  border: 1px solid #1e293b;
  border-radius: var(--radius-md);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
  max-height: 520px;
}
.ide-header {
  background: #0f172a;
  padding: 8px 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid #1e293b;
  flex-shrink: 0;
}
.ide-dots {
  display: flex;
  gap: 6px;
}
.ide-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
}
.ide-dot.red { background: #ef4444; }
.ide-dot.yellow { background: #f59e0b; }
.ide-dot.green { background: #10b981; }
.ide-tab {
  color: #94a3b8;
  font-size: 11px;
  font-family: 'JetBrains Mono', Consolas, monospace;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}
.ide-body {
  padding: 12px 16px;
  font-family: 'JetBrains Mono', Consolas, 'Fira Code', monospace;
  font-size: 11px;
  line-height: 1.48;
  color: #e2e8f0;
  white-space: pre !important;
  overflow: auto;
  flex: 1;
}
.kw { color: #818cf8; font-weight: bold; }
.type { color: #38bdf8; font-weight: 600; }
.str { color: #34d399; }
.num { color: #fbbf24; }
.com { color: #64748b; font-style: italic; }
.ann { color: #f43f5e; font-weight: bold; }
.fn { color: #c084fc; font-weight: 600; }

/* FLOATING CONTROLS */
#navBar {
  position: fixed;
  bottom: 20px;
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 30px;
  padding: 8px 18px;
  display: flex;
  align-items: center;
  gap: 14px;
  z-index: 1000;
  color: white;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}
.nav-btn {
  background: transparent;
  border: none;
  color: #cbd5e1;
  font-size: 15px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
  font-weight: 600;
}
.nav-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
}
.slide-counter {
  font-size: 13px;
  font-weight: 700;
  color: #38bdf8;
  padding: 0 8px;
  min-width: 60px;
  text-align: center;
}

/* OVERVIEW MODAL */
#overviewModal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(16px);
  z-index: 99999;
  display: none;
  flex-direction: column;
  padding: 40px;
  overflow-y: auto;
}
#overviewModal.show { display: flex; }
.overview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  margin-bottom: 24px;
}
.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}
.overview-thumb {
  background: white;
  border-radius: 12px;
  aspect-ratio: 16 / 9;
  padding: 16px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.overview-thumb:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(79, 70, 229, 0.4);
}
.thumb-num {
  position: absolute;
  top: 10px;
  right: 12px;
  font-weight: 800;
  font-size: 12px;
  color: var(--accent);
}
.thumb-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.3;
}
.thumb-cat {
  font-size: 11px;
  color: var(--text-muted);
}

/* PRINT & PDF EXPORT STYLING */
@media print {
  body {
    overflow: visible !important;
    height: auto !important;
    background: #ffffff !important;
    display: block !important;
  }
  #progressBar, #navBar, #overviewModal { display: none !important; }
  #stage {
    width: 100% !important;
    height: auto !important;
    display: block !important;
    overflow: visible !important;
  }
  #slideContainer {
    transform: none !important;
    width: 100% !important;
    height: auto !important;
    position: static !important;
  }
  .slide {
    position: relative !important;
    opacity: 1 !important;
    transform: none !important;
    pointer-events: auto !important;
    page-break-after: always !important;
    break-after: page !important;
    margin: 0 auto 30px auto !important;
    box-shadow: none !important;
    border: 1px solid #e2e8f0 !important;
    width: 1280px !important;
    height: 720px !important;
  }
}

</style>
</head>
<body>

<div id="progressBar"></div>

<div id="stage">
  <div id="slideContainer">

    <!-- ==========================================
         SLIDE 1: COVER
         ========================================== -->
    <div class="slide slide-cover active" data-title="Cover Judul">
      <div class="cover-brand">
        <div class="brand-icon">E</div>
        <div>
          <div class="brand-name">EEPIS MOTORS</div>
          <div class="brand-tag">INTEGRATED LUXURY AUTO DEALERSHIP</div>
        </div>
      </div>
      <div>
        <div style="display:inline-block; margin-bottom:14px;" class="pill pill-accent">DOKUMENTASI PRESENTASI PROYEK AKHIR</div>
        <h1 class="cover-title">Sistem Dealer Terpadu, Portofolio Aset &amp; Mode Test Drive Interaktif</h1>
        <p class="cover-desc">
          Implementasi mendalam 4 Pilar Object-Oriented Programming (OOP) berbasis JavaFX, modular FXML MVC, wealth management kendaraan, dan simulasi 2D Canvas Game.
        </p>
      </div>
      <div class="cover-footer">
        <div class="author-info">
          <div style="font-size:11px; font-weight:800; color:var(--accent); text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">ANGGOTA KELOMPOK PROYEK:</div>
          <div style="display:flex; gap:28px; align-items:center;">
            <div>
              <div class="author-name" style="font-size:16px;">1. Mustofa Barakbah</div>
              <div class="author-nrp">NRP : 3125600065</div>
            </div>
            <div style="width:1.5px; height:36px; background:var(--border);"></div>
            <div>
              <div class="author-name" style="font-size:16px;">2. Reza Ali Muhammad</div>
              <div class="author-nrp">NRP : 3125600061</div>
            </div>
          </div>
          <div class="author-dept" style="margin-top:6px;">Departemen Teknik Informatika — Politeknik Elektronika Negeri Surabaya (EEPIS / PENS)</div>
        </div>
        <div style="display:flex; flex-direction:column; align-items:flex-end; gap:8px;">
          <div style="display:flex; gap:8px;">
            <span class="pill pill-accent">Java 11 / 25</span>
            <span class="pill pill-success">JavaFX 21</span>
            <span class="pill pill-warning">MVC + OOP</span>
          </div>
          <span style="font-size:11.5px; color:var(--text-muted); font-weight:600;">Pemrograman Berorientasi Objek Lanjut</span>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 2: LATAR BELAKANG & RUMUSAN MASALAH
         ========================================== -->
    <div class="slide" data-title="Latar Belakang & Tujuan">
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="badge-module">Overview</span>
          <h2 class="slide-title">Latar Belakang &amp; Rumusan Masalah</h2>
        </div>
        <span class="slide-category">Konseptual Proyek</span>
      </div>
      <div class="slide-body">
        <div class="col">
          <div class="card highlight">
            <div class="card-title">🚨 Keterbatasan Dealer Konvensional</div>
            <div class="card-desc">
              Sistem dealer mobil tradisional umumnya hanya berfungsi sebagai katalog pasif tanpa memvalidasi kelayakan finansial pelanggan secara dinamis, tanpa kalkulasi pajak terotomasi, dan tanpa visualisasi portofolio kepemilikan aset.
            </div>
          </div>
          <div class="card">
            <div class="card-title">💡 Visi Inovasi EEPIS Motors</div>
            <div class="card-desc">
              Menggabungkan platform *luxury auto showroom* dengan konsep *wealth management* (Portofolio &amp; Distribusi Nilai Aset) serta menghadirkan pengalaman mencoba mobil secara nyata melalui mini game <strong>Test Drive 2D Canvas</strong> dengan reward saldo instan.
            </div>
          </div>
          <div class="card">
            <div class="card-title">🎯 Sasaran Akademik OOP</div>
            <div class="card-desc">
              Menerapkan prinsip OOP murni (Abstraction, Inheritance, Polymorphism, Encapsulation) dipadukan dengan Custom Exception Handling dan JavaFX FXML GUI modern.
            </div>
          </div>
        </div>
        <div class="col">
          <div class="row">
            <div class="kpi-box">
              <span class="kpi-label">Arsitektur</span>
              <span class="kpi-value">MVC</span>
              <span class="kpi-sub">FXML + Controller + Model</span>
            </div>
            <div class="kpi-box">
              <span class="kpi-label">Pilar OOP</span>
              <span class="kpi-value">4 Pilar</span>
              <span class="kpi-sub">+ Interface &amp; Exception</span>
            </div>
          </div>
          <div class="row">
            <div class="kpi-box">
              <span class="kpi-label">Total Modul</span>
              <span class="kpi-value">7 Modul</span>
              <span class="kpi-sub">Showroom hingga VIP Lounge</span>
            </div>
            <div class="kpi-box">
              <span class="kpi-label">Framerate Game</span>
              <span class="kpi-value">60 FPS</span>
              <span class="kpi-sub">Canvas AnimationTimer</span>
            </div>
          </div>
          <div class="card" style="flex:1;">
            <div class="card-title">✨ Nilai Tambah Proyek</div>
            <ul class="feature-list" style="margin-top:4px;">
              <li class="feature-item">
                <span class="feature-icon">✓</span>
                <span><strong>Verifikasi Proof-of-Funds</strong> otomatis mengklasifikasikan tier pelanggan (Gold, Silver, Regular).</span>
              </li>
              <li class="feature-item">
                <span class="feature-icon">✓</span>
                <span><strong>Interaktivitas Nyata</strong>: Mode test drive bukan lagi sekadar teks statis, melainkan permainan kemudi jalur 3-lane.</span>
              </li>
              <li class="feature-item">
                <span class="feature-icon">✓</span>
                <span><strong>GUI Modern &amp; Bersih</strong>: Estetika minimalis dengan transisi halus dan tata letak profesional.</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 3: ARSITEKTUR SISTEM (MVC)
         ========================================== -->
    <div class="slide" data-title="Arsitektur Sistem (MVC)">
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="badge-module">Arsitektur</span>
          <h2 class="slide-title">Arsitektur Sistem: Model-View-Controller (MVC)</h2>
        </div>
        <span class="slide-category">Software Engineering</span>
      </div>
      <div class="slide-body">
        <div class="col">
          <div class="card highlight">
            <div class="card-title">🏛️ Pola Desain MVC Terpadu</div>
            <div class="card-desc">
              Pemisahan tanggung jawab (*Separation of Concerns*) menjamin kode mudah dirawat, dimodifikasi, dan diuji.
            </div>
          </div>
          <div class="card">
            <div class="card-title">📦 1. MODEL (Logika Bisnis &amp; Data)</div>
            <div class="card-desc">
              Hierarki kelas `Vehicle`, `ElectricCar`, `GasCar`, `User`, `Customer`, `GoldCustomer`, `SilverCustomer`, `RegularCustomer`, dan interface `ITaxable`.
            </div>
          </div>
          <div class="card">
            <div class="card-title">🎨 2. VIEW (Tampilan Antarmuka)</div>
            <div class="card-desc">
              Berkas deklaratif FXML (`primary.fxml`), styling tema modern (`main.css`), dan renderer grafis dinamis 60 FPS Canvas di `TestDriveGame.java`.
            </div>
          </div>
          <div class="card">
            <div class="card-title">⚙️ 3. CONTROLLER (Orkestrator Event)</div>
            <div class="card-desc">
              `PrimaryController.java` menangani event navigasi, manipulasi koleksi showroom/garasi, validasi transaksi, dan komunikasi dua arah dengan View.
            </div>
          </div>
        </div>
        <div class="col-1-5">
          <div class="card" style="height:100%; display:flex; flex-direction:column;">
            <div class="card-title">🔄 Diagram Alur Kerja MVC</div>
            <div style="background:#f1f5f9; border-radius:10px; padding:16px; margin-top:8px; display:flex; flex-direction:column; gap:12px; font-size:12px; flex:1; justify-content:center;">
              <div style="background:white; padding:12px; border-radius:8px; border-left:4px solid var(--accent); box-shadow:var(--shadow-sm);">
                <strong>User Action (View)</strong>: Klik beli mobil / jalankan Test Drive di `primary.fxml`.
              </div>
              <div style="text-align:center; color:var(--accent); font-weight:bold;">⬇ Diproses Event Listener</div>
              <div style="background:white; padding:12px; border-radius:8px; border-left:4px solid #06b6d4; box-shadow:var(--shadow-sm);">
                <strong>Controller Routing</strong>: `PrimaryController` mengecek validasi saldo &amp; stok unit.
              </div>
              <div style="text-align:center; color:#06b6d4; font-weight:bold;">⬇ Eksekusi Aturan Bisnis</div>
              <div style="background:white; padding:12px; border-radius:8px; border-left:4px solid #10b981; box-shadow:var(--shadow-sm);">
                <strong>Model Mutation</strong>: `currentUser.buyVehicle(car)` memotong saldo, mengurangi stok, menambah ke garasi, memicu bonus tier.
              </div>
              <div style="text-align:center; color:#10b981; font-weight:bold;">⬇ Update Tampilan</div>
              <div style="background:white; padding:12px; border-radius:8px; border-left:4px solid #f59e0b; box-shadow:var(--shadow-sm);">
                <strong>View Refresh</strong>: Saldo sidebar terupdate, bar chart tergambar ulang, modal faktur dibuka.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 4: OOP 1 — INHERITANCE & ABSTRACTION
         ========================================== -->
    <div class="slide" data-title="OOP: Inheritance & Abstraction">
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="badge-module">OOP Deep Dive</span>
          <h2 class="slide-title">1. Abstraction &amp; Inheritance</h2>
        </div>
        <span class="slide-category">Prinsip Pemrograman Objek</span>
      </div>
      <div class="slide-body">
        <div class="col">
          <div class="card highlight">
            <div class="card-title">🔒 Mengapa Abstract Class?</div>
            <div class="card-desc">
              Kelas <code>User</code>, <code>Customer</code>, dan <code>Vehicle</code> dideklarasikan sebagai <code>abstract</code> untuk mencegah instansiasi objek yang belum spesifik secara bisnis.
            </div>
          </div>
          <div class="card">
            <div class="card-title">🌲 Hierarki Inheritance 1: Pengguna</div>
            <div class="card-desc" style="font-family:monospace; font-size:11.5px; line-height:1.5;">
              User (Abstract)<br>
              &nbsp;↳ Customer (Abstract)<br>
              &nbsp;&nbsp;&nbsp;&nbsp;↳ GoldCustomer (Tier VVIP)<br>
              &nbsp;&nbsp;&nbsp;&nbsp;↳ SilverCustomer (Tier VIP)<br>
              &nbsp;&nbsp;&nbsp;&nbsp;↳ RegularCustomer (Standar)
            </div>
          </div>
          <div class="card">
            <div class="card-title">🏎️ Hierarki Inheritance 2: Kendaraan</div>
            <div class="card-desc" style="font-family:monospace; font-size:11.5px; line-height:1.5;">
              Vehicle (Abstract, implements ITaxable)<br>
              &nbsp;↳ ElectricCar (EV: baterai kWh &amp; jarak)<br>
              &nbsp;↳ GasCar (Bensin: kapasitas cc &amp; transmisi)
            </div>
          </div>
        </div>
        <div class="col-1-5">
          <div class="ide-window">
            <div class="ide-header">
              <div class="ide-dots">
                <span class="ide-dot red"></span>
                <span class="ide-dot yellow"></span>
                <span class="ide-dot green"></span>
              </div>
              <span class="ide-tab">☕ Vehicle.java &amp; ElectricCar.java</span>
            </div>
            <div class="ide-body"><span class="com">// 1. Base Abstract Class dengan kontrak baku</span>
<span class="kw">public abstract class</span> <span class="type">Vehicle</span> <span class="kw">implements</span> <span class="type">ITaxable</span> {
    <span class="kw">protected</span> <span class="type">String</span> brand, model, color;
    <span class="kw">protected double</span> price;
    <span class="kw">protected int</span> stock;

    <span class="kw">public</span> <span class="fn">Vehicle</span>(<span class="type">String</span> brand, <span class="type">String</span> model, <span class="kw">double</span> price, <span class="kw">int</span> stock, <span class="type">String</span> color) {
        <span class="kw">this</span>.brand = brand;
        <span class="kw">this</span>.model = model;
        <span class="kw">this</span>.price = price;
        <span class="kw">this</span>.stock = stock;
        <span class="kw">this</span>.color = color;
    }

    <span class="com">// Kontrak Abstrak: Wajib dioverride oleh seluruh subclass</span>
    <span class="kw">public abstract</span> <span class="type">String</span> <span class="fn">testDrive</span>();
    <span class="kw">public abstract</span> <span class="type">String</span> <span class="fn">getSpecs</span>();
}

<span class="com">// 2. Subclass Konkret yang mewarisi sifat induk</span>
<span class="kw">public class</span> <span class="type">ElectricCar</span> <span class="kw">extends</span> <span class="type">Vehicle</span> {
    <span class="kw">private int</span> batteryCapacity, range;

    <span class="kw">public</span> <span class="fn">ElectricCar</span>(<span class="type">String</span> brand, <span class="type">String</span> model, <span class="kw">double</span> price, <span class="kw">int</span> stock,
                       <span class="type">String</span> color, <span class="kw">int</span> battery, <span class="kw">int</span> range) {
        <span class="kw">super</span>(brand, model, price, stock, color);
        <span class="kw">this</span>.batteryCapacity = battery;
        <span class="kw">this</span>.range = range;
    }

    <span class="ann">@Override</span>
    <span class="kw">public</span> <span class="type">String</span> <span class="fn">testDrive</span>() {
        <span class="kw">return</span> <span class="str">"Zzzzz... Melaju instan nan senyap bertenaga EV."</span>;
    }
}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 5: OOP 2 — POLYMORPHISM
         ========================================== -->
    <div class="slide" data-title="OOP: Polymorphism">
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="badge-module">OOP Deep Dive</span>
          <h2 class="slide-title">2. Polymorphism (Dynamic Method Dispatch)</h2>
        </div>
        <span class="slide-category">Prinsip Pemrograman Objek</span>
      </div>
      <div class="slide-body">
        <div class="col">
          <div class="card highlight">
            <div class="card-title">🎭 Definisi &amp; Manfaat</div>
            <div class="card-desc">
              Polimorfisme memungkinkan pemanggilan method yang seragam pada objek bertipe induk, namun eksekusi perilakunya ditentukan secara dinamis oleh subclass saat runtime.
            </div>
          </div>
          <div class="card">
            <div class="card-title">1. Overriding `testDrive()`</div>
            <div class="card-desc">
              • <strong>ElectricCar</strong>: <i>"Zzzzz... Senyap bertenaga EV."</i><br>
              • <strong>GasCar</strong>: <i>"VROOOM! Suara mesin menderu!"</i>
            </div>
          </div>
          <div class="card">
            <div class="card-title">2. Overriding `calculateDiscount()`</div>
            <div class="card-desc">
              • <strong>Gold</strong>: Diskon 8% &nbsp;·&nbsp; <strong>Silver</strong>: 3% &nbsp;·&nbsp; <strong>Regular</strong>: 0%
            </div>
          </div>
          <div class="card">
            <div class="card-title">3. Overriding `applyBonus()`</div>
            <div class="card-desc">
              • <strong>Gold</strong>: Cashback Saldo 2% + Asuransi 3 Tahun.<br>
              • <strong>Silver</strong>: Gratis servis 1 tahun &amp; merchandise.
            </div>
          </div>
        </div>
        <div class="col-1-5">
          <div class="ide-window">
            <div class="ide-header">
              <div class="ide-dots">
                <span class="ide-dot red"></span>
                <span class="ide-dot yellow"></span>
                <span class="ide-dot green"></span>
              </div>
              <span class="ide-tab">☕ PrimaryController.java &amp; GoldCustomer.java</span>
            </div>
            <div class="ide-body"><span class="com">// 1. Pemanggilan Polimorfis Seragam di Controller (Runtime Dispatch)</span>
<span class="kw">double</span> discount = currentUser.<span class="fn">calculateDiscount</span>(vehicle.getPrice());
<span class="kw">double</span> finalPrice = (vehicle.getPrice() - discount) + tax;

<span class="com">// Memicu perilaku bonus spesifik tier tanpa perlu 'if-else' bertumpuk</span>
<span class="type">String</span> bonusBrought = currentUser.<span class="fn">applyBonus</span>(finalPrice);
<span class="type">String</span> soundEffect  = vehicle.<span class="fn">testDrive</span>();

<span class="com">// 2. Implementasi Konkret pada Subclass: GoldCustomer</span>
<span class="kw">public class</span> <span class="type">GoldCustomer</span> <span class="kw">extends</span> <span class="type">Customer</span> {
    <span class="ann">@Override</span>
    <span class="kw">public</span> <span class="type">String</span> <span class="fn">getTierName</span>() {
        <span class="kw">return</span> <span class="str">"Gold VVIP"</span>;
    }

    <span class="ann">@Override</span>
    <span class="kw">public double</span> <span class="fn">calculateDiscount</span>(<span class="kw">double</span> price) { 
        <span class="kw">return</span> price * <span class="num">0.08</span>; <span class="com">// Potongan 8% khusus Gold</span>
    }

    <span class="ann">@Override</span>
    <span class="kw">public</span> <span class="type">String</span> <span class="fn">applyBonus</span>(<span class="kw">double</span> finalPrice) {
        <span class="kw">double</span> cashback = finalPrice * <span class="num">0.02</span>;
        <span class="kw">this</span>.bankBalance += cashback; <span class="com">// Refund saldo instan!</span>
        <span class="kw">return</span> <span class="str">"Cashback Saldo Rp "</span> + String.format(<span class="str">"%,.0f"</span>, cashback) + 
               <span class="str">" &amp; Asuransi All-Risk 3 Thn"</span>;
    }
}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 6: OOP 3 — ENCAPSULATION
         ========================================== -->
    <div class="slide" data-title="OOP: Encapsulation & Data Hiding">
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="badge-module">OOP Deep Dive</span>
          <h2 class="slide-title">3. Encapsulation &amp; Data Integrity</h2>
        </div>
        <span class="slide-category">Prinsip Pemrograman Objek</span>
      </div>
      <div class="slide-body">
        <div class="col">
          <div class="card highlight">
            <div class="card-title">🛡️ Proteksi Atribut Kritis</div>
            <div class="card-desc">
              Menjaga integritas data finansial agar saldo pengguna tidak dapat dimanipulasi sembarangan dari luar kelas tanpa melewati logika validasi bisnis.
            </div>
          </div>
          <div class="card">
            <div class="card-title">1. Atribut Terproteksi</div>
            <div class="card-desc">
              • <code>protected double bankBalance;</code> di kelas `Customer`.<br>
              • <code>protected int stock;</code> di kelas `Vehicle`.<br>
              Akses baca hanya melalui getter resmi <code>getBankBalance()</code>.
            </div>
          </div>
          <div class="card">
            <div class="card-title">2. Alur Transaksi Terenkapsulasi</div>
            <div class="card-desc">
              1. Validasi stok unit kendaraan.<br>
              2. Kalkulasi diskon tier dan pajak PPN 11%.<br>
              3. Verifikasi kecukupan saldo (Lempar exception jika kurang).<br>
              4. Mutasi saldo, penurunan stok, dan penambahan garasi.
            </div>
          </div>
        </div>
        <div class="col-1-5">
          <div class="ide-window">
            <div class="ide-header">
              <div class="ide-dots">
                <span class="ide-dot red"></span>
                <span class="ide-dot yellow"></span>
                <span class="ide-dot green"></span>
              </div>
              <span class="ide-tab">☕ Customer.java — Enkapsulasi Transaksi Aman</span>
            </div>
            <div class="ide-body"><span class="com">// Mutasi saldo hanya diizinkan melalui method berintegritas tinggi</span>
<span class="kw">public</span> <span class="type">String</span> <span class="fn">buyVehicle</span>(<span class="type">Vehicle</span> vehicle) <span class="kw">throws</span> <span class="type">DealershipException</span> {
    <span class="com">// 1. Validasi ketersediaan stok fisik</span>
    <span class="kw">if</span> (vehicle.getStock() &lt;= <span class="num">0</span>) {
        <span class="kw">throw new</span> <span class="type">DealershipException</span>(<span class="str">"Stok "</span> + vehicle.getModel() + <span class="str">" kosong!"</span>);
    }

    <span class="kw">double</span> discount = calculateDiscount(vehicle.getPrice());
    <span class="kw">double</span> discountedPrice = vehicle.getPrice() - discount;
    <span class="kw">double</span> tax = vehicle.calculateTax(discountedPrice);
    <span class="kw">double</span> finalPrice = discountedPrice + tax;

    <span class="com">// 2. Validasi saldo akun terenkapsulasi</span>
    <span class="kw">if</span> (<span class="kw">this</span>.bankBalance &lt; finalPrice) {
        <span class="kw">throw new</span> <span class="type">DealershipException</span>(<span class="str">"Saldo tidak mencukupi! Kurang: Rp "</span> +
            String.format(<span class="str">"%,.0f"</span>, (finalPrice - <span class="kw">this</span>.bankBalance)));
    }

    <span class="com">// 3. State data hanya dimutasi jika seluruh validasi lolos</span>
    <span class="kw">this</span>.bankBalance -= finalPrice;
    vehicle.decreaseStock();
    <span class="kw">this</span>.garage.add(vehicle);
    
    <span class="type">String</span> bonus = applyBonus(finalPrice);
    <span class="kw">return</span> <span class="type">TransactionReceipt</span>.generateReceipt(<span class="kw">this</span>, vehicle, finalPrice,
                                              discount, tax, bonus);
}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 7: OOP 4 — INTERFACE & EXCEPTION
         ========================================== -->
    <div class="slide" data-title="OOP: Interface & Exception Handling">
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="badge-module">OOP Deep Dive</span>
          <h2 class="slide-title">4. Interface &amp; Custom Exception Handling</h2>
        </div>
        <span class="slide-category">Prinsip Pemrograman Objek</span>
      </div>
      <div class="slide-body">
        <div class="col" style="gap:12px;">
          <div class="ide-window" style="flex:1;">
            <div class="ide-header">
              <div class="ide-dots">
                <span class="ide-dot red"></span>
                <span class="ide-dot yellow"></span>
                <span class="ide-dot green"></span>
              </div>
              <span class="ide-tab">📜 ITaxable.java — Kontrak Perpajakan</span>
            </div>
            <div class="ide-body" style="padding:12px 14px; font-size:11px;"><span class="com">// Interface: Memisahkan beban pajak secara decoupled</span>
<span class="kw">public interface</span> <span class="type">ITaxable</span> {
    <span class="kw">double</span> <span class="fn">calculateTax</span>(<span class="kw">double</span> priceAfterDiscount);
    <span class="kw">double</span> <span class="fn">getTaxRate</span>();
}</div>
          </div>
          <div class="ide-window" style="flex:1;">
            <div class="ide-header">
              <div class="ide-dots">
                <span class="ide-dot red"></span>
                <span class="ide-dot yellow"></span>
                <span class="ide-dot green"></span>
              </div>
              <span class="ide-tab">⚠️ DealershipException.java — Custom Exception</span>
            </div>
            <div class="ide-body" style="padding:12px 14px; font-size:11px;"><span class="com">// Custom Exception turunan java.lang.Exception</span>
<span class="kw">public class</span> <span class="type">DealershipException</span> <span class="kw">extends</span> <span class="type">Exception</span> {
    <span class="kw">public</span> <span class="fn">DealershipException</span>(<span class="type">String</span> message) {
        <span class="kw">super</span>(message);
    }
}</div>
          </div>
        </div>
        <div class="col-1-5">
          <div class="ide-window">
            <div class="ide-header">
              <div class="ide-dots">
                <span class="ide-dot red"></span>
                <span class="ide-dot yellow"></span>
                <span class="ide-dot green"></span>
              </div>
              <span class="ide-tab">⚙️ PrimaryController.java — Penanganan Try-Catch GUI</span>
            </div>
            <div class="ide-body"><span class="com">// Penanganan Error Transaksi di Level GUI secara Elegan</span>
showModalAnimasi(<span class="str">"Koneksi Bank &amp; Validasi Saldo..."</span>, <span class="str">"Memproses Pembelian"</span>, () -&gt; {
    <span class="kw">try</span> {
        <span class="com">// Pemanggilan method yang melempar DealershipException</span>
        <span class="type">String</span> receipt = currentUser.<span class="fn">buyVehicle</span>(car);
        transactionHistory.add(<span class="str">"PEMBELIAN: "</span> + car.getBrand() + <span class="str">" "</span> + car.getModel());
        
        updateSemuaData();
        modalBox.setVisible(<span class="kw">false</span>);
        txtReceiptContent.setText(receipt);
        receiptBox.setVisible(<span class="kw">true</span>);

    } <span class="kw">catch</span> (<span class="type">DealershipException</span> ex) {
        <span class="com">// Tangkap error: jangan biarkan aplikasi crash!</span>
        closeModal();
        
        <span class="com">// Tampilkan notifikasi visual merah di pojok kanan atas</span>
        showToast(<span class="str">"Transaksi ditolak: "</span> + ex.getMessage(), <span class="kw">true</span>);
    }
});</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 8: INOVASI MINI GAME TEST DRIVE
         ========================================== -->
    <div class="slide" data-title="Inovasi Mini Game Test Drive">
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="badge-module">Inovasi Utama</span>
          <h2 class="slide-title">Simulasi Mini Game Test Drive Interaktif 2D</h2>
        </div>
        <span class="slide-category">Game Engine &amp; JavaFX Canvas</span>
      </div>
      <div class="slide-body">
        <div class="col">
          <div class="card highlight">
            <div class="card-title">🎮 Dari Animasi Teks Menjadi Game 60 FPS</div>
            <div class="card-desc">
              Modul test drive dirombak total menggunakan kelas mandiri <code>TestDriveGame.java</code> berbasis JavaFX `Canvas` dan `AnimationTimer`.
            </div>
          </div>
          <div class="card">
            <div class="card-title">⚡ Fisika Berbeda Antara EV vs Gas</div>
            <div class="card-desc">
              • <strong>Electric Car (EV)</strong>: Torsi instan dengan percepatan tinggi (accel: 42, maxSpeed: 640).<br>
              • <strong>Gasoline Car (Gas)</strong>: Akselerasi bertahap dengan batas kecepatan lebih tinggi (accel: 30, maxSpeed: 720).
            </div>
          </div>
          <div class="card">
            <div class="card-title">🕹️ Kontrol &amp; Mekanisme Permainan</div>
            <div class="card-desc">
              • Kemudi 3 lajur jalan menggunakan tombol <strong>← / →</strong> atau <strong>A / D</strong>, atau klik layar.<br>
              • Sistem 3 Nyawa (*Heart*), collision detection, dan efek getar layar (*screen shake*).<br>
              • Koin emas di jalan memberikan <strong>Bonus Saldo Rp 100.000 / koin</strong> ke rekening pembeli!
            </div>
          </div>
        </div>
        <div class="col-1-5" style="display:flex; flex-direction:column; gap:12px;">
          <div class="screenshot-container" style="flex:1;">
            <img src='""" + img_data.get("img_gameplay", "") + """' alt="Gameplay Test Drive">
          </div>
          <div style="display:flex; gap:10px;">
            <div class="kpi-box"><span class="kpi-label">HUD</span><span class="kpi-value" style="font-size:16px;">Speedometer km/h</span></div>
            <div class="kpi-box"><span class="kpi-label">DURASI</span><span class="kpi-value" style="font-size:16px;">30 Detik</span></div>
            <div class="kpi-box"><span class="kpi-label">REWARD</span><span class="kpi-value" style="font-size:16px;">+Rp 100k / Koin</span></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 9: HASIL TEST DRIVE & SHOWROOM
         ========================================== -->
    <div class="slide" data-title="Hasil Test Drive & Showroom">
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="badge-module">Fitur 1</span>
          <h2 class="slide-title">Katalog Showroom &amp; Hasil Test Drive</h2>
        </div>
        <span class="slide-category">Pengalaman Pengguna</span>
      </div>
      <div class="slide-body">
        <div class="col">
          <div class="screenshot-container" style="flex:1;">
            <img src='""" + img_data.get("img_showroom", "") + """' alt="Showroom Modern">
          </div>
          <div class="card">
            <div class="card-title">🔍 Katalog Showroom Pintar</div>
            <div class="card-desc">
              Fitur pencarian instan (real-time filtering), filter jenis (EV vs Bensin), rentang harga (&lt; 2M vs &gt; 2M), status stok, dan tombol pintas Test Drive.
            </div>
          </div>
        </div>
        <div class="col">
          <div class="screenshot-container" style="flex:1;">
            <img src='""" + img_data.get("img_result", "") + """' alt="Hasil Test Drive">
          </div>
          <div class="card">
            <div class="card-title">🏆 Kartu Hasil Test Drive</div>
            <div class="card-desc">
              Menampilkan skor, kecepatan puncak, koin yang diperoleh, rekor pribadi mobil, serta tombol instan <strong>[Main Lagi]</strong> atau <strong>[Beli Mobil Ini]</strong>.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 10: DASBOR PORTOFOLIO & GARASI
         ========================================== -->
    <div class="slide" data-title="Dasbor Portofolio Aset">
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="badge-module">Fitur 2</span>
          <h2 class="slide-title">Dasbor Portofolio Aset (Wealth Management)</h2>
        </div>
        <span class="slide-category">Manajemen Portofolio</span>
      </div>
      <div class="slide-body">
        <div class="col-1-5">
          <div class="screenshot-container" style="flex:1;">
            <img src='""" + img_data.get("img_garasi", "") + """' alt="Dasbor Portofolio">
          </div>
        </div>
        <div class="col">
          <div class="card highlight">
            <div class="card-title">📊 Konsep Manajemen Kekayaan</div>
            <div class="card-desc">
              Garasi bukan sekadar daftar teks biasa, melainkan dasbor portofolio aset terintegrasi yang menghitung akumulasi kekayaan pelanggan secara otomatis.
            </div>
          </div>
          <div class="row">
            <div class="kpi-box">
              <span class="kpi-label">TOTAL UNIT</span>
              <span class="kpi-value">2 Unit</span>
              <span class="kpi-sub">Di garasi pribadi</span>
            </div>
            <div class="kpi-box">
              <span class="kpi-label">TOTAL ASET</span>
              <span class="kpi-value" style="color:var(--success);">Rp 2,15 M</span>
              <span class="kpi-sub">Nilai pasar saat ini</span>
            </div>
          </div>
          <div class="card">
            <div class="card-title">📈 BarChart &amp; Sertifikat Digital</div>
            <div class="card-desc">
              • Visualisasi JavaFX `BarChart` membandingkan nilai aset antar kendaraan di garasi.<br>
              • Setiap unit tercatat dengan nomor urut kepemilikan (`01`, `02`), spesifikasi, dan stempel <strong>LUNAS</strong>.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 11: SERVIS, PAJAK, TRADE-IN & LOUNGE
         ========================================== -->
    <div class="slide" data-title="Servis, Pajak, Trade-In & VIP">
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="badge-module">Fitur 3</span>
          <h2 class="slide-title">Ekosistem Purna Jual &amp; VIP Privilege</h2>
        </div>
        <span class="slide-category">Operasional Bisnis Lengkap</span>
      </div>
      <div class="slide-body">
        <div class="col">
          <div class="card">
            <div class="card-title">🔧 Servis Berkala Resmi</div>
            <div class="card-desc">
              Pemeliharaan mesin resmi Rp 2.500.000 dengan pengecekan 40 titik. Mengurangi saldo secara terenkapsulasi dan dicatat di histori log.
            </div>
          </div>
          <div class="card">
            <div class="card-title">⚖️ Kalkulasi Pajak &amp; Asuransi</div>
            <div class="card-desc">
              Menghitung total estimasi kewajiban pajak PPN 11% seluruh unit di garasi secara dinamis via interface `ITaxable`.
            </div>
          </div>
          <div class="card">
            <div class="card-title">🤝 Trade-In (Jual Kembali)</div>
            <div class="card-desc">
              Menghitung depresiasi pasar 30%. Dana 70% dari nilai kendaraan langsung dicairkan kembali ke saldo rekening pelanggan.
            </div>
          </div>
          <div class="card">
            <div class="card-title">🎁 VIP Privilege Lounge</div>
            <div class="card-desc">
              Klaim bonus harian per tier: Gold (+Rp 50 Juta), Silver (+Rp 10 Juta), Regular (+Rp 1 Juta). Dilengkapi proteksi satu kali klaim per sesi.
            </div>
          </div>
        </div>
        <div class="col-1-5" style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
          <div class="screenshot-container">
            <img src='""" + img_data.get("img_servis", "") + """' alt="Servis">
          </div>
          <div class="screenshot-container">
            <img src='""" + img_data.get("img_pajak", "") + """' alt="Pajak">
          </div>
          <div class="screenshot-container">
            <img src='""" + img_data.get("img_tradein", "") + """' alt="Trade-In">
          </div>
          <div class="screenshot-container">
            <img src='""" + img_data.get("img_rewards", "") + """' alt="VIP Lounge">
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 12: GALERI SHOWCASE LIVE APP
         ========================================== -->
    <div class="slide" data-title="Galeri Showcase Aplikasi">
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="badge-module">Showcase</span>
          <h2 class="slide-title">Galeri Antarmuka EEPIS Motors</h2>
        </div>
        <span class="slide-category">Dokumentasi Visual</span>
      </div>
      <div class="slide-body">
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; width:100%;">
          <div class="card" style="padding:10px; gap:6px;">
            <div class="screenshot-container" style="height:140px;">
              <img src='""" + img_data.get("img_login", "") + """' alt="Login">
            </div>
            <div class="card-title" style="font-size:13px;">1. Autentikasi KTP &amp; Saldo</div>
          </div>
          <div class="card" style="padding:10px; gap:6px;">
            <div class="screenshot-container" style="height:140px;">
              <img src='""" + img_data.get("img_showroom", "") + """' alt="Showroom">
            </div>
            <div class="card-title" style="font-size:13px;">2. Katalog Showroom Mobil</div>
          </div>
          <div class="card" style="padding:10px; gap:6px;">
            <div class="screenshot-container" style="height:140px;">
              <img src='""" + img_data.get("img_gameplay", "") + """' alt="Test Drive Game">
            </div>
            <div class="card-title" style="font-size:13px;">3. Mini Game Test Drive 2D</div>
          </div>
          <div class="card" style="padding:10px; gap:6px;">
            <div class="screenshot-container" style="height:140px;">
              <img src='""" + img_data.get("img_result", "") + """' alt="Hasil Drive">
            </div>
            <div class="card-title" style="font-size:13px;">4. Rekor &amp; Hasil Test Drive</div>
          </div>
          <div class="card" style="padding:10px; gap:6px;">
            <div class="screenshot-container" style="height:140px;">
              <img src='""" + img_data.get("img_garasi", "") + """' alt="Portofolio Garasi">
            </div>
            <div class="card-title" style="font-size:13px;">5. Portofolio &amp; Distribusi Aset</div>
          </div>
          <div class="card" style="padding:10px; gap:6px;">
            <div class="screenshot-container" style="height:140px;">
              <img src='""" + img_data.get("img_receipt", "") + """' alt="Faktur">
            </div>
            <div class="card-title" style="font-size:13px;">6. Faktur Transaksi Digital</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 14: DIAGRAM KELAS (UML) & METRIK
         ========================================== -->
    <div class="slide" data-title="UML Diagram & Metrik Kode">
      <div class="slide-header">
        <div class="slide-header-left">
          <span class="badge-module">Engineering</span>
          <h2 class="slide-title">Diagram Hubungan Kelas (UML) &amp; Metrik Proyek</h2>
        </div>
        <span class="slide-category">Struktur Arsitektur Kode</span>
      </div>
      <div class="slide-body">
        <div class="col-2" style="display:flex; flex-direction:column; height:100%; min-height:0;">
          <div class="card" style="padding:12px; flex:1; display:flex; flex-direction:column; min-height:0; overflow:hidden; background:#ffffff;">
            <div class="card-title" style="margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
              <span>📐 Diagram Relasi Kelas (UML Class Diagram)</span>
              <span class="pill pill-accent" style="font-size:10px;">Visual Vector Diagram</span>
            </div>
            <div style="flex:1; width:100%; min-height:0; display:flex; align-items:center; justify-content:center;">
              <svg viewBox="0 0 760 450" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <defs>
    <filter id="cardShadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    
    <!-- UML Inheritance Arrow (Hollow Triangle) -->
    <marker id="umlInherit" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <polygon points="1,1 10,6 1,11" fill="#ffffff" stroke="#4f46e5" stroke-width="1.8"/>
    </marker>
    
    <!-- UML Realize Arrow (Hollow Triangle for Interface) -->
    <marker id="umlRealize" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <polygon points="1,1 10,6 1,11" fill="#ffffff" stroke="#0d9488" stroke-width="1.8"/>
    </marker>
    
    <!-- UML Aggregation (Hollow Diamond) -->
    <marker id="umlAgg" markerWidth="14" markerHeight="10" refX="2" refY="5" orient="auto">
      <polygon points="1,5 7,1 13,5 7,9" fill="#ffffff" stroke="#3b82f6" stroke-width="1.8"/>
    </marker>
  </defs>

  <!-- BACKGROUND GRID SUBTLE -->
  <rect width="760" height="450" rx="12" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
  
  <!-- ================= RELATIONS (DRAWN FIRST SO CARDS SIT ON TOP) ================= -->
  
  <!-- Customer extends User (Vertical Up) -->
  <path d="M 125, 140 L 125, 102" fill="none" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#umlInherit)"/>
  
  <!-- Subclasses extend Customer (3 branches) -->
  <path d="M 50, 310 L 50, 280 L 125, 280 L 125, 252" fill="none" stroke="#4f46e5" stroke-width="1.8" marker-end="url(#umlInherit)"/>
  <path d="M 130, 310 L 130, 252" fill="none" stroke="#4f46e5" stroke-width="1.8"/>
  <path d="M 210, 310 L 210, 280 L 125, 280" fill="none" stroke="#4f46e5" stroke-width="1.8"/>

  <!-- Vehicle implements ITaxable (Vertical Up) -->
  <path d="M 570, 160 L 570, 95" fill="none" stroke="#0d9488" stroke-width="1.8" stroke-dasharray="5,4" marker-end="url(#umlRealize)"/>

  <!-- ElectricCar & GasCar extend Vehicle -->
  <path d="M 480, 320 L 480, 290 L 570, 290 L 570, 275" fill="none" stroke="#d97706" stroke-width="1.8" marker-end="url(#umlInherit)"/>
  <path d="M 660, 320 L 660, 290 L 570, 290" fill="none" stroke="#d97706" stroke-width="1.8"/>

  <!-- Customer Aggregation to Vehicle (garage: List<Vehicle>) -->
  <path d="M 240, 195 L 450, 195" fill="none" stroke="#3b82f6" stroke-width="2" marker-start="url(#umlAgg)"/>
  <!-- Aggregation Label -->
  <text x="325" y="186" text-anchor="middle" font-size="10" font-weight="700" fill="#2563eb">+ garage (1 : 0..*)</text>

  <!-- ================= CLASS CARDS ================= -->

  <!-- 1. <<abstract>> User -->
  <g transform="translate(45, 16)" filter="url(#cardShadow)">
    <rect width="160" height="84" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <rect width="160" height="24" rx="8" fill="#eef2ff"/>
    <rect y="16" width="160" height="8" fill="#eef2ff"/>
    <text x="80" y="16" text-anchor="middle" font-size="10" font-weight="700" fill="#4f46e5">&lt;&lt;abstract&gt;&gt; User</text>
    <line x1="0" y1="24" x2="160" y2="24" stroke="#e2e8f0" stroke-width="1"/>
    <text x="10" y="38" font-size="9.5" fill="#475569">- id : String</text>
    <text x="10" y="51" font-size="9.5" fill="#475569">- name : String</text>
    <line x1="0" y1="57" x2="160" y2="57" stroke="#e2e8f0" stroke-width="1"/>
    <text x="10" y="71" font-size="9.5" fill="#0f172a">+ displayProfile() : void</text>
  </g>

  <!-- 2. <<abstract>> Customer -->
  <g transform="translate(20, 140)" filter="url(#cardShadow)">
    <rect width="210" height="110" rx="8" fill="#ffffff" stroke="#818cf8" stroke-width="1.5"/>
    <rect width="210" height="25" rx="8" fill="#4f46e5"/>
    <rect y="17" width="210" height="8" fill="#4f46e5"/>
    <text x="105" y="17" text-anchor="middle" font-size="11" font-weight="800" fill="#ffffff">&lt;&lt;abstract&gt;&gt; Customer</text>
    <line x1="0" y1="25" x2="210" y2="25" stroke="#818cf8" stroke-width="1"/>
    <text x="10" y="40" font-size="10" fill="#475569"># bankBalance : double</text>
    <text x="10" y="53" font-size="10" fill="#475569">+ garage : List&lt;Vehicle&gt;</text>
    <line x1="0" y1="60" x2="210" y2="60" stroke="#e2e8f0" stroke-width="1"/>
    <text x="10" y="74" font-size="9.5" fill="#0f172a">+ buyVehicle(v) : String</text>
    <text x="10" y="87" font-size="9.5" fill="#0f172a">+ calculateDiscount(p)* : double</text>
    <text x="10" y="100" font-size="9.5" fill="#0f172a">+ applyBonus(fp)* : String</text>
  </g>

  <!-- 3. Subclasses: Gold, Silver, Regular Customer -->
  <!-- GoldCustomer -->
  <g transform="translate(10, 310)" filter="url(#cardShadow)">
    <rect width="80" height="74" rx="6" fill="#ffffff" stroke="#f59e0b" stroke-width="1.2"/>
    <rect width="80" height="20" rx="6" fill="#fef3c7"/>
    <rect y="14" width="80" height="6" fill="#fef3c7"/>
    <text x="40" y="14" text-anchor="middle" font-size="9.5" font-weight="800" fill="#b45309">GoldCustomer</text>
    <line x1="0" y1="20" x2="80" y2="20" stroke="#fcd34d" stroke-width="1"/>
    <text x="6" y="34" font-size="8.5" fill="#475569">Disc: 8%</text>
    <text x="6" y="47" font-size="8.5" fill="#475569">Cashback: 2%</text>
    <text x="6" y="60" font-size="8.5" fill="#16a34a">Tier: VVIP</text>
  </g>

  <!-- SilverCustomer -->
  <g transform="translate(95, 310)" filter="url(#cardShadow)">
    <rect width="80" height="74" rx="6" fill="#ffffff" stroke="#94a3b8" stroke-width="1.2"/>
    <rect width="80" height="20" rx="6" fill="#f1f5f9"/>
    <rect y="14" width="80" height="6" fill="#f1f5f9"/>
    <text x="40" y="14" text-anchor="middle" font-size="9.5" font-weight="800" fill="#475569">SilverCustomer</text>
    <line x1="0" y1="20" x2="80" y2="20" stroke="#cbd5e1" stroke-width="1"/>
    <text x="6" y="34" font-size="8.5" fill="#475569">Disc: 3%</text>
    <text x="6" y="47" font-size="8.5" fill="#475569">Free Servis</text>
    <text x="6" y="60" font-size="8.5" fill="#0284c7">Tier: VIP</text>
  </g>

  <!-- RegularCustomer -->
  <g transform="translate(180, 310)" filter="url(#cardShadow)">
    <rect width="80" height="74" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.2"/>
    <rect width="80" height="20" rx="6" fill="#f8fafc"/>
    <rect y="14" width="80" height="6" fill="#f8fafc"/>
    <text x="40" y="14" text-anchor="middle" font-size="9.5" font-weight="800" fill="#64748b">RegularCust</text>
    <line x1="0" y1="20" x2="80" y2="20" stroke="#e2e8f0" stroke-width="1"/>
    <text x="6" y="34" font-size="8.5" fill="#475569">Disc: 0%</text>
    <text x="6" y="47" font-size="8.5" fill="#475569">Bonus: -</text>
    <text x="6" y="60" font-size="8.5" fill="#64748b">Tier: Reguler</text>
  </g>

  <!-- 4. <<interface>> ITaxable -->
  <g transform="translate(465, 16)" filter="url(#cardShadow)">
    <rect width="210" height="76" rx="8" fill="#ffffff" stroke="#0d9488" stroke-width="1.5"/>
    <rect width="210" height="24" rx="8" fill="#ccfbf1"/>
    <rect y="16" width="210" height="8" fill="#ccfbf1"/>
    <text x="105" y="16" text-anchor="middle" font-size="10.5" font-weight="800" fill="#0f766e">&lt;&lt;interface&gt;&gt; ITaxable</text>
    <line x1="0" y1="24" x2="210" y2="24" stroke="#99f6e4" stroke-width="1"/>
    <text x="10" y="42" font-size="9.5" fill="#0f172a">+ calculateTax(p : double) : double</text>
    <text x="10" y="58" font-size="9.5" fill="#0f172a">+ getTaxRate() : double</text>
  </g>

  <!-- 5. <<abstract>> Vehicle -->
  <g transform="translate(465, 160)" filter="url(#cardShadow)">
    <rect width="210" height="114" rx="8" fill="#ffffff" stroke="#f59e0b" stroke-width="1.5"/>
    <rect width="210" height="25" rx="8" fill="#d97706"/>
    <rect y="17" width="210" height="8" fill="#d97706"/>
    <text x="105" y="17" text-anchor="middle" font-size="11" font-weight="800" fill="#ffffff">&lt;&lt;abstract&gt;&gt; Vehicle</text>
    <line x1="0" y1="25" x2="210" y2="25" stroke="#f59e0b" stroke-width="1"/>
    <text x="10" y="40" font-size="10" fill="#475569"># brand, model, color : String</text>
    <text x="10" y="53" font-size="10" fill="#475569"># price : double, stock : int</text>
    <line x1="0" y1="60" x2="210" y2="60" stroke="#e2e8f0" stroke-width="1"/>
    <text x="10" y="74" font-size="9.5" fill="#0f172a">+ testDrive()* : String</text>
    <text x="10" y="87" font-size="9.5" fill="#0f172a">+ getSpecs()* : String</text>
    <text x="10" y="100" font-size="9.5" fill="#0f172a">+ decreaseStock() : void</text>
  </g>

  <!-- 6. ElectricCar -->
  <g transform="translate(415, 320)" filter="url(#cardShadow)">
    <rect width="130" height="80" rx="6" fill="#ffffff" stroke="#6366f1" stroke-width="1.2"/>
    <rect width="130" height="20" rx="6" fill="#eef2ff"/>
    <rect y="14" width="130" height="6" fill="#eef2ff"/>
    <text x="65" y="14" text-anchor="middle" font-size="10" font-weight="800" fill="#4f46e5">⚡ ElectricCar</text>
    <line x1="0" y1="20" x2="130" y2="20" stroke="#c7d2fe" stroke-width="1"/>
    <text x="8" y="34" font-size="9" fill="#475569">- batteryCapacity : int</text>
    <text x="8" y="47" font-size="9" fill="#475569">- range : int</text>
    <line x1="0" y1="52" x2="130" y2="52" stroke="#e2e8f0" stroke-width="1"/>
    <text x="8" y="66" font-size="9" fill="#0f172a">+ testDrive() : "Zzzz EV"</text>
  </g>

  <!-- 7. GasCar -->
  <g transform="translate(590, 320)" filter="url(#cardShadow)">
    <rect width="130" height="80" rx="6" fill="#ffffff" stroke="#ea580c" stroke-width="1.2"/>
    <rect width="130" height="20" rx="6" fill="#fff7ed"/>
    <rect y="14" width="130" height="6" fill="#fff7ed"/>
    <text x="65" y="14" text-anchor="middle" font-size="10" font-weight="800" fill="#c2410c">🏎️ GasCar</text>
    <line x1="0" y1="20" x2="130" y2="20" stroke="#fed7aa" stroke-width="1"/>
    <text x="8" y="34" font-size="9" fill="#475569">- engineCapacity : int</text>
    <text x="8" y="47" font-size="9" fill="#475569">- transmission : String</text>
    <line x1="0" y1="52" x2="130" y2="52" stroke="#e2e8f0" stroke-width="1"/>
    <text x="8" y="66" font-size="9" fill="#0f172a">+ testDrive() : "VROOOM!"</text>
  </g>

  <!-- DIAGRAM LEGEND FOOTER -->
  <g transform="translate(20, 412)">
    <rect width="720" height="26" rx="6" fill="#ffffff" stroke="#e2e8f0" stroke-width="1"/>
    <text x="15" y="17" font-size="9.5" font-weight="700" fill="#475569">LEGEND UML:</text>
    
    <path d="M 100, 14 L 125, 14" stroke="#4f46e5" stroke-width="1.5" marker-end="url(#umlInherit)"/>
    <text x="135" y="17" font-size="9" fill="#334155">Generalisasi / Inheritance (`extends`)</text>
    
    <path d="M 330, 14 L 355, 14" stroke="#0d9488" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#umlRealize)"/>
    <text x="365" y="17" font-size="9" fill="#334155">Realisasi Interface (`implements`)</text>
    
    <path d="M 545, 14 L 575, 14" stroke="#3b82f6" stroke-width="1.5" marker-start="url(#umlAgg)"/>
    <text x="585" y="17" font-size="9" fill="#334155">Agregasi (`Customer` memiliki `Vehicle`)</text>
  </g>
</svg>
            </div>
          </div>
        </div>
        <div class="col" style="display:flex; flex-direction:column; gap:12px;">
          <div class="card highlight">
            <div class="card-title">📊 Metrik Arsitektur OOP</div>
            <div class="card-desc" style="font-size:12.5px;">
              Implementasi relasi kelas mencakup <strong>Generalisasi</strong>, <strong>Realisasi Interface</strong>, serta <strong>Agregasi</strong> kepemilikan aset.
            </div>
          </div>
          <div class="row">
            <div class="kpi-box">
              <span class="kpi-label">KELAS JAVA</span>
              <span class="kpi-value">14 File</span>
              <span class="kpi-sub">Source code OOP</span>
            </div>
            <div class="kpi-box">
              <span class="kpi-label">STATUS BUILD</span>
              <span class="kpi-value" style="color:var(--success);">SUCCESS</span>
              <span class="kpi-sub">Maven Java 11/25</span>
            </div>
          </div>
          <div class="card" style="flex:1;">
            <div class="card-title">✅ Verifikasi 4 Pilar OOP</div>
            <ul class="feature-list" style="margin-top:4px; gap:7px;">
              <li class="feature-item"><span class="feature-icon">1</span><span style="font-size:12px;"><strong>Abstraction</strong>: Base class `User`, `Customer`, `Vehicle`.</span></li>
              <li class="feature-item"><span class="feature-icon">2</span><span style="font-size:12px;"><strong>Inheritance</strong>: Hierarki bertingkat EV/Gas &amp; Tier Customer.</span></li>
              <li class="feature-item"><span class="feature-icon">3</span><span style="font-size:12px;"><strong>Polymorphism</strong>: Overriding method `testDrive()` &amp; kalkulasi bonus.</span></li>
              <li class="feature-item"><span class="feature-icon">4</span><span style="font-size:12px;"><strong>Encapsulation</strong>: Proteksi saldo `#bankBalance` &amp; stok unit.</span></li>
              <li class="feature-item"><span class="feature-icon">5</span><span style="font-size:12px;"><strong>Interface &amp; Ex</strong>: `ITaxable` (PPN 11%) &amp; `DealershipException`.</span></li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- ==========================================
         SLIDE 14: KESIMPULAN & PENUTUP
         ========================================== -->
    <div class="slide slide-cover" data-title="Kesimpulan & Penutup">
      <div class="slide-header" style="border:none; margin-bottom:0; padding-bottom:0;">
        <div class="slide-header-left">
          <span class="badge-module">Penutup</span>
          <h2 class="slide-title">Kesimpulan &amp; Rencana Pengembangan</h2>
        </div>
        <span class="slide-category">Refleksi Proyek Akhir</span>
      </div>
      <div class="slide-body" style="gap:24px;">
        <div class="col">
          <div class="card highlight">
            <div class="card-title">🎯 Kesimpulan Hasil Karya</div>
            <div class="card-desc" style="font-size:14px; line-height:1.6;">
              Proyek <strong>EEPIS MOTORS</strong> berhasil mendemonstrasikan bahwa konsep teori Pemrograman Berorientasi Objek (OOP) tingkat lanjut dapat diimplementasikan ke dalam aplikasi desktop JavaFX yang nyata, fungsional, dan memiliki estetika visual kelas atas.
            </div>
          </div>
          <div class="card">
            <div class="card-title">💎 3 Keunggulan Utama Proyek</div>
            <ul class="feature-list" style="margin-top:6px;">
              <li class="feature-item"><span class="feature-icon">1</span><span><strong>Arsitektur Kokoh</strong>: 4 Pilar OOP, Interface, dan Custom Exception berjalan harmonis.</span></li>
              <li class="feature-item"><span class="feature-icon">2</span><span><strong>Gamifikasi Interaktif</strong>: Test drive 2D Canvas 60 FPS dengan reward ekonomi riil.</span></li>
              <li class="feature-item"><span class="feature-icon">3</span><span><strong>Wealth Management UI</strong>: Dasbor aset portofolio elegan dengan BarChart.</span></li>
            </ul>
          </div>
        </div>
        <div class="col">
          <div class="card">
            <div class="card-title">🚀 Roadmap Pengembangan Masa Depan</div>
            <ul class="feature-list" style="margin-top:6px;">
              <li class="feature-item"><span class="feature-icon">✦</span><span><strong>Database RDBMS</strong>: Integrasi SQLite / PostgreSQL menggunakan JDBC / Hibernate.</span></li>
              <li class="feature-item"><span class="feature-icon">✦</span><span><strong>Online Multiplayer</strong>: Leaderboard skor Test Drive secara cloud antar mahasiswa.</span></li>
              <li class="feature-item"><span class="feature-icon">✦</span><span><strong>Payment Gateway API</strong>: Simulasi integrasi Midtrans / QRIS untuk pembayaran riil.</span></li>
            </ul>
          </div>
          <div class="card highlight" style="text-align:center; padding:22px; justify-content:center; align-items:center; flex:1;">
            <div style="font-size:24px; font-weight:800; color:var(--accent); margin-bottom:4px;">Terima Kasih!</div>
            <div style="font-size:13px; color:var(--text-muted); margin-bottom:12px;">Sesi Tanya Jawab (Q&amp;A) Dibuka</div>
            <div style="display:flex; gap:20px; justify-content:center; align-items:center; margin-bottom:10px;">
              <div style="text-align:center;">
                <div style="font-weight:700; font-size:14px; color:var(--text-main);">Mustofa Barakbah</div>
                <div style="font-size:12px; color:var(--accent); font-weight:700;">3125600065</div>
              </div>
              <div style="width:1.5px; height:32px; background:var(--border);"></div>
              <div style="text-align:center;">
                <div style="font-weight:700; font-size:14px; color:var(--text-main);">Reza Ali Muhammad</div>
                <div style="font-size:12px; color:var(--accent); font-weight:700;">3125600061</div>
              </div>
            </div>
            <div style="font-size:12px; color:var(--text-muted);">Politeknik Elektronika Negeri Surabaya (EEPIS / PENS)</div>
          </div>
        </div>
      </div>
      <div class="cover-footer" style="padding-top:14px;">
        <span style="font-size:12px; color:var(--text-muted);">Tekan <strong>[F]</strong> Fullscreen &nbsp;·&nbsp; <strong>[O]</strong> Grid Overview &nbsp;·&nbsp; <strong>[← / →]</strong> Navigasi Slide</span>
        <span class="pill pill-accent">EEPIS AUTO v1.0 Final</span>
      </div>
    </div>

  </div>
</div>

<!-- ==========================================
     FLOATING PRESENTATION CONTROLS
     ========================================== -->
<div id="navBar">
  <button class="nav-btn" onclick="prevSlide()" title="Slide Sebelumnya (Panah Kiri)">◀ Prev</button>
  <span class="slide-counter" id="slideNum">01 / 15</span>
  <button class="nav-btn" onclick="nextSlide()" title="Slide Berikutnya (Panah Kanan)">Next ▶</button>
  <span style="opacity:0.3;">|</span>
  <button class="nav-btn" onclick="toggleOverview()" title="Lihat Semua Slide (O)">⊞ Grid</button>
  <button class="nav-btn" onclick="toggleFullscreen()" title="Layar Penuh (F)">⛶ Layar Penuh</button>
</div>

<!-- ==========================================
     OVERVIEW GRID MODAL
     ========================================== -->
<div id="overviewModal">
  <div class="overview-header">
    <h2 style="font-size:22px; font-weight:800;">Daftar Semua Slide (Navigasi Cepat)</h2>
    <button class="nav-btn" onclick="toggleOverview()" style="background:rgba(255,255,255,0.2);">✕ Tutup (Esc)</button>
  </div>
  <div class="overview-grid" id="overviewGrid"></div>
</div>

<script>
/* ==========================================================
   SLIDE CONTROLLER ENGINE (RESPONSIVE SCALING & KEYBOARD)
   ========================================================== */
const slides = document.querySelectorAll('.slide');
const container = document.getElementById('slideContainer');
const slideNum = document.getElementById('slideNum');
const progressBar = document.getElementById('progressBar');
const overviewModal = document.getElementById('overviewModal');
const overviewGrid = document.getElementById('overviewGrid');

let cur = 0;
const total = slides.length;

// RESPONSIVE 16:9 AUTO-SCALING
function autoScale() {
  const w = window.innerWidth;
  const h = window.innerHeight;
  const scale = Math.min(w / 1280, h / 720) * 0.94;
  container.style.transform = `scale(${scale})`;
}
window.addEventListener('resize', autoScale);
autoScale();

// UPDATE ACTIVE SLIDE
function showSlide(idx) {
  if (idx < 0) idx = 0;
  if (idx >= total) idx = total - 1;
  cur = idx;

  slides.forEach((s, i) => {
    s.classList.remove('active', 'prev');
    if (i === cur) s.classList.add('active');
    else if (i < cur) s.classList.add('prev');
  });

  slideNum.textContent = `${String(cur + 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}`;
  progressBar.style.width = `${((cur + 1) / total) * 100}%`;
}

function nextSlide() { showSlide(cur + 1); }
function prevSlide() { showSlide(cur - 1); }

// KEYBOARD SHORTCUTS
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
    e.preventDefault(); nextSlide();
  } else if (e.key === 'ArrowLeft' || e.key === 'Backspace' || e.key === 'PageUp') {
    e.preventDefault(); prevSlide();
  } else if (e.key === 'Home') {
    e.preventDefault(); 
// URL HASH & TOUCH SWIPE SUPPORT
function getHashSlide() {
  const h = window.location.hash;
  if (h && /^#\d+$/.test(h)) {
    const n = parseInt(h.substring(1), 10);
    if (!isNaN(n) && n >= 1 && n <= total) return n - 1;
  }
  return 0;
}

window.addEventListener('hashchange', () => {
  const hIdx = getHashSlide();
  if (hIdx !== cur) showSlide(hIdx);
});

// Update URL hash without extra history clutter
const origShow = showSlide;
showSlide = function(idx) {
  origShow(idx);
  history.replaceState(null, null, `#${cur + 1}`);
};

// Touch gestures
let touchStartX = 0;
document.addEventListener('touchstart', (e) => {
  touchStartX = e.changedTouches[0].screenX;
}, { passive: true });

document.addEventListener('touchend', (e) => {
  const touchEndX = e.changedTouches[0].screenX;
  if (touchStartX - touchEndX > 50) nextSlide();
  else if (touchEndX - touchStartX > 50) prevSlide();
}, { passive: true });

// Init with hash if present
showSlide(getHashSlide());

  } else if (e.key === 'End') {
    e.preventDefault(); showSlide(total - 1);
  } else if (e.key.toLowerCase() === 'f') {
    e.preventDefault(); toggleFullscreen();
  } else if (e.key.toLowerCase() === 'o') {
    e.preventDefault(); toggleOverview();
  } else if (e.key === 'Escape') {
    if (overviewModal.classList.contains('show')) toggleOverview();
  }
});

// FULLSCREEN TOGGLE
function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(err => console.log(err));
  } else {
    document.exitFullscreen().catch(err => console.log(err));
  }
}

// OVERVIEW GRID BUILDER
function toggleOverview() {
  const isOpen = overviewModal.classList.contains('show');
  if (isOpen) {
    overviewModal.classList.remove('show');
  } else {
    overviewGrid.innerHTML = '';
    slides.forEach((s, i) => {
      const title = s.getAttribute('data-title') || `Slide ${i+1}`;
      const thumb = document.createElement('div');
      thumb.className = 'overview-thumb';
      if (i === cur) thumb.style.border = '2px solid var(--accent)';
      thumb.innerHTML = `
        <span class="thumb-num">#${i+1}</span>
        <div class="thumb-title">${title}</div>
        <div class="thumb-cat">${s.querySelector('.slide-category')?.textContent || 'Slide'}</div>
      `;
      thumb.onclick = () => {
        showSlide(i);
        overviewModal.classList.remove('show');
      };
      overviewGrid.appendChild(thumb);
    });
    overviewModal.classList.add('show');
  }
}

// INIT

// URL HASH & TOUCH SWIPE SUPPORT
function getHashSlide() {
  const h = window.location.hash;
  if (h && /^#\d+$/.test(h)) {
    const n = parseInt(h.substring(1), 10);
    if (!isNaN(n) && n >= 1 && n <= total) return n - 1;
  }
  return 0;
}

window.addEventListener('hashchange', () => {
  const hIdx = getHashSlide();
  if (hIdx !== cur) showSlide(hIdx);
});

// Update URL hash without extra history clutter
const origShow = showSlide;
showSlide = function(idx) {
  origShow(idx);
  history.replaceState(null, null, `#${cur + 1}`);
};

// Touch gestures
let touchStartX = 0;
document.addEventListener('touchstart', (e) => {
  touchStartX = e.changedTouches[0].screenX;
}, { passive: true });

document.addEventListener('touchend', (e) => {
  const touchEndX = e.changedTouches[0].screenX;
  if (touchStartX - touchEndX > 50) nextSlide();
  else if (touchEndX - touchStartX > 50) prevSlide();
}, { passive: true });

// Init with hash if present
showSlide(getHashSlide());

</script>

</body>
</html>
"""

out_file = "/home/rezaali/Downloads/eepisauto-java-oop-main(4)/eepisauto-java-oop-main/presentation.html"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Success! Generated standalone presentation at: {out_file}")
print(f"File size: {os.path.getsize(out_file) / 1024:.1f} KB")
