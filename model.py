import cv2
import numpy as np
import os
import pickle
from sklearn.neighbors import KNeighborsClassifier

DATASET_DIR = 'dataset'
MODEL_FILE = 'knn_model.pkl'

SISWA = {
    1:  {"nama": "Angel Veronika Meylania",          "nis": "14013/1674.063", "jk": "P", "pola": "Whorl", "tangan": "Kiri"},
    2:  {"nama": "Azzahra Cahya Desyienta",           "nis": "14016/1677.063", "jk": "P", "pola": "Whorl", "tangan": "Kiri"},
    3:  {"nama": "Bunga Kirana Eiffel Okafila",       "nis": "14022/1683.063", "jk": "P", "pola": "Whorl", "tangan": "Kanan"},
    4:  {"nama": "Linda Angellina",                   "nis": "14046/1707.063", "jk": "P", "pola": "Whorl", "tangan": "Kiri"},
    5:  {"nama": "Sely Aljannata",                    "nis": "14076/1737.063", "jk": "P", "pola": "Loop",  "tangan": "Kiri"},
    6:  {"nama": "Fardhan Vaccari Pradiasyah",        "nis": "14031/1692.063", "jk": "L", "pola": "Loop",  "tangan": "Kanan"},
    7:  {"nama": "Hirzi Aqillah Annafi Heva",         "nis": "14037/1698.063", "jk": "L", "pola": "Loop",  "tangan": "Kanan"},
    8:  {"nama": "Muhammad Fadhlur Rohman Thoriq",    "nis": "14055/1716.063", "jk": "L", "pola": "Whorl", "tangan": "Kanan"},
    9:  {"nama": "Raffi Gani Jabbaaru",               "nis": "14067/1728.063", "jk": "L", "pola": "Whorl", "tangan": "Kanan"},
    10: {"nama": "Adhitamaa Azar Wicaksono Zein",     "nis": "14007/1668.063", "jk": "L", "pola": "Loop",  "tangan": "Kanan"},
    11: {"nama": "Achmad Adam Sajjad Suhadi Arifin",  "nis": "14004/1665.063", "jk": "L", "pola": "Loop",  "tangan": "Kanan"},
}

def extract_features(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    img = cv2.resize(img, (128, 128))
    img = cv2.equalizeHist(img)
    return img.flatten().astype(np.float32)

def train_model():
    X, y = [], []
    for folder in os.listdir(DATASET_DIR):
        folder_path = os.path.join(DATASET_DIR, folder)
        if not os.path.isdir(folder_path):
            continue
        try:
            label_id = int(folder.split('_')[0])
        except:
            continue
        for file in os.listdir(folder_path):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                fitur = extract_features(os.path.join(folder_path, file))
                if fitur is not None:
                    X.append(fitur)
                    y.append(label_id)
    if len(X) == 0:
        return False, "Dataset kosong! Isi folder dataset dulu."
    knn = KNeighborsClassifier(n_neighbors=min(3, len(X)))
    knn.fit(X, y)
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(knn, f)
    return True, f"Model berhasil dilatih dengan {len(X)} gambar."

def predict_image(img_path):
    if not os.path.exists(MODEL_FILE):
        return None, "Model belum dilatih!"
    with open(MODEL_FILE, 'rb') as f:
        knn = pickle.load(f)
    fitur = extract_features(img_path)
    if fitur is None:
        return None, "Gambar tidak bisa dibaca."
    pred = int(knn.predict([fitur])[0])
    proba = knn.predict_proba([fitur])[0]
    confidence = round(max(proba) * 100, 2)
    siswa = SISWA.get(pred)
    if siswa:
        return {"id": pred, "confidence": confidence, **siswa}, None
    return None, "Siswa tidak ditemukan."