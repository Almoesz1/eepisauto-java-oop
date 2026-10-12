package eepisauto;

/**
 * Launcher mandiri alternatif untuk memintas pembatasan JavaFX runtime module graph
 * saat dieksekusi dari bundel JAR atau lingkungan IDE tanpa modul eksplisit.
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public class MainLauncher {

    /**
     * Mendelegasikan eksekusi langsung ke {@link App#main(String[])}.
     *
     * @param args argumen baris perintah
     */
    public static void main(String[] args) {
        App.main(args);
    }
}