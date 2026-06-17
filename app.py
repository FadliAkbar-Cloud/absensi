from flask import Flask, request, jsonify, render_template
import os
from model import train_model, predict_image
from database import init_db, simpan_absensi, get_absensi_hari_ini, get_semua_absensi

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/riwayat')
def riwayat():
    return render_template('riwayat.html')

@app.route('/train', methods=['POST'])
def train():
    success, msg = train_model()
    return jsonify({"success": success, "message": msg})

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "Tidak ada file"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "File kosong"})
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    result, error = predict_image(filepath)
    if error:
        return jsonify({"success": False, "message": error})
    return jsonify({"success": True, "data": result, "filepath": filepath})

@app.route('/absen', methods=['POST'])
def absen():
    data = request.json
    success, msg = simpan_absensi(
        data['id'], data['nama'], data['nis'],
        data['jk'], data['pola'], data['tangan']
    )
    return jsonify({"success": success, "message": msg})

@app.route('/api/absensi-hari-ini')
def api_hari_ini():
    rows = get_absensi_hari_ini()
    result = [{"id": r[0], "label_id": r[1], "nama": r[2], "nis": r[3],
               "jk": r[4], "pola": r[5], "tangan": r[6],
               "tanggal": r[7], "waktu": r[8]} for r in rows]
    return jsonify(result)

@app.route('/api/semua-absensi')
def api_semua():
    rows = get_semua_absensi()
    result = [{"id": r[0], "label_id": r[1], "nama": r[2], "nis": r[3],
               "jk": r[4], "pola": r[5], "tangan": r[6],
               "tanggal": r[7], "waktu": r[8]} for r in rows]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')