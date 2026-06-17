import sqlite3
from datetime import date

def init_db():
    conn = sqlite3.connect('absensi.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS absensi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label_id INTEGER,
        nama TEXT,
        nis TEXT,
        jk TEXT,
        pola TEXT,
        tangan TEXT,
        tanggal TEXT,
        waktu TEXT
    )''')
    conn.commit()
    conn.close()

def simpan_absensi(label_id, nama, nis, jk, pola, tangan):
    conn = sqlite3.connect('absensi.db')
    c = conn.cursor()
    today = str(date.today())
    c.execute("SELECT * FROM absensi WHERE label_id=? AND tanggal=?", (label_id, today))
    if c.fetchone():
        conn.close()
        return False, "Sudah absen hari ini"
    from datetime import datetime
    waktu = datetime.now().strftime("%H:%M:%S")
    c.execute("INSERT INTO absensi (label_id, nama, nis, jk, pola, tangan, tanggal, waktu) VALUES (?,?,?,?,?,?,?,?)",
              (label_id, nama, nis, jk, pola, tangan, today, waktu))
    conn.commit()
    conn.close()
    return True, "Absensi berhasil"

def get_absensi_hari_ini():
    conn = sqlite3.connect('absensi.db')
    c = conn.cursor()
    today = str(date.today())
    c.execute("SELECT * FROM absensi WHERE tanggal=? ORDER BY waktu ASC", (today,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_semua_absensi():
    conn = sqlite3.connect('absensi.db')
    c = conn.cursor()
    c.execute("SELECT * FROM absensi ORDER BY tanggal DESC, waktu ASC")
    rows = c.fetchall()
    conn.close()
    return rows