# Menggunakan Python 3.11 agar cocok dengan versi package terbaru
FROM python:3.11-slim

# Mengatur folder kerja di dalam container
WORKDIR /app

# Install dependensi sistem yang dibutuhkan oleh OpenCV dan library lainnya
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    glib-2.0 \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements.txt terlebih dahulu (manfaatkan Docker cache)
COPY requirements.txt .

# Install semua library Python tanpa menyimpan cache agar ukuran image kecil
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh source code project dari laptop ke dalam container
COPY . .

# Menentukan perintah untuk menjalankan aplikasi (sesuaikan jika file utama bukan app.py)
CMD ["python", "app.py"]
