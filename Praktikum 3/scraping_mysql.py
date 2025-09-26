import mysql.connector
import requests
from bs4 import BeautifulSoup

# 1. Connect ke MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bigdata_praktikum"
)
cursor = db.cursor()

# buat tabel jika belum ada
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        judul VARCHAR(255),
        harga VARCHAR(50),
        availability VARCHAR(255)
    )
""")

# 2. Scraping seluruh halaman
base_url = "https://books.toscrape.com/catalogue/page-{}.html"
page = 1

while True:
    url = base_url.format(page)
    res = requests.get(url)
    
    if res.status_code != 200:
        break  # hentikan jika halaman tidak ada
    
    soup = BeautifulSoup(res.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    if not books:
        break  # hentikan jika tidak ada buku
    
    for book in books:
        judul = book.h3.a["title"]
        harga = book.find("p", class_="price_color").text
        availability = book.find("p", class_="instock availability").text.strip()
        
        cursor.execute(
            "INSERT INTO books (judul, harga, availability) VALUES (%s, %s, %s)",
            (judul, harga, availability)
        )
    
    print(f"Scraped halaman {page} dengan {len(books)} buku.")
    page += 1

# 3. Commit dan close koneksi
db.commit()
print("Semua data berhasil disimpan ke database.")

cursor.close()
db.close()
