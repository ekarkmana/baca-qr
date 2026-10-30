import cv2
import webbrowser
from pyzbar.pyzbar import decode

def scan_semua_qr():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("=== FAST QR SCANNER (AUTO-OPEN LINK) ===")
    print("Arahkan QR Code ke kamera...")

    last_scanned = None

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Convert ke Grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Binarization (Otsu Thresholding) agar peka cetakan fisik & artistik
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Coba decode threshold dulu, kalau gagal pakai gray biasa
        detected_objects = decode(thresh)
        if not detected_objects:
            detected_objects = decode(gray)

        for obj in detected_objects:
            qr_data = obj.data.decode('utf-8')

            # Gambar kotak hijau penanda
            (x, y, w, h) = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # Eksekusi LANGSUNG begitu ter-scan (tidak perlu klik terminal)
            if qr_data != last_scanned:
                print(f"\n🔥 [BERHASIL BACA]: {qr_data}")
                last_scanned = qr_data
                
                # LANGSUNG EKSEKUSI / BUKA LINK
                proses_otomatis(qr_data)

        cv2.imshow("Super QR Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def proses_otomatis(data):
    # Cek apakah isi QR Code berupa link/URL
    if data.startswith("http://") or data.startswith("https://"):
        print(f"🚀 [AUTO OPEN]: Langsung membuka browser ke '{data}' ...")
        # Otomatis buka link di browser laptop tanpa diklik!
        webbrowser.open(data)
    else:
        print(f"⚙️ [AUTO PROSES]: Menjalankan perintah data '{data}'")

if __name__ == "__main__":
    scan_semua_qr()