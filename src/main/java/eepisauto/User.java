package eepisauto;

/**
 * Superclass abstrak yang merepresentasikan entitas Pengguna dasar pada sistem EEPIS Auto.
 * <p>
 * Menyimpan atribut universal seperti ID unik (NRP/KTP) dan nama lengkap pengguna.
 * <p>
 * Konsep OOP: <b>Abstraction</b> &amp; <b>Inheritance Superclass</b>.
 *
 * @author Kelompok 3 (Mustofa Barakbah &amp; Reza Ali Muhammad)
 * @version 2.0
 */
public abstract class User {

    /** Identifier unik pengguna (misal: NRP mahasiswa atau nomor identitas KTP). */
    protected String id;

    /** Nama lengkap pengguna. */
    protected String name;

    /**
     * Konstruktor untuk menginisialisasi atribut dasar pengguna.
     *
     * @param id nomor identitas pengguna
     * @param name nama lengkap pengguna
     */
    public User(String id, String name) {
        this.id = id;
        this.name = name;
    }

    /**
     * Mengambil nomor identitas pengguna.
     *
     * @return nomor identitas
     */
    public String getId() {
        return id;
    }

    /**
     * Mengambil nama lengkap pengguna.
     *
     * @return nama pengguna
     */
    public String getName() {
        return name;
    }

    /**
     * Menampilkan profil pengguna ke media output standar (konsol/log).
     */
    public abstract void displayProfile();
}