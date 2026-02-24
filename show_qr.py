#!/usr/bin/env python3
"""
Hiển thị QR code kết nối — chạy trong terminal riêng, scan xong đóng đi.
"""
import sys
import os

def print_qr(url, label):
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=1, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        print(f"\n{'='*50}")
        print(f"  {label}")
        print(f"{'='*50}")
        print(f"  🔗 {url}")
        print(f"\n📱 Scan QR:")
        qr.print_ascii(invert=True)
    except ImportError:
        print(f"\n{label}: {url}")

if __name__ == "__main__":
    urls = sys.argv[1:]  # format: "LABEL|URL" ...

    for item in urls:
        label, url = item.split("|", 1)
        print_qr(url, label)

    print(f"\n{'='*50}")
    print("✅ Server đang chạy ngầm.")
    print("   Scan QR xong → đóng cửa sổ này là được.")
    print(f"{'='*50}")
    input("\n[Nhấn Enter để đóng...] ")
