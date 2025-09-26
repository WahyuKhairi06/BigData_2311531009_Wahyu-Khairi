import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# 1. Koneksi ke MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bigdata_praktikum"]
collection = db["books_travel"]  

# 2. Scraping seluruh halaman kategori Travel
base_url = "https://books.toscrape.com/catalogue/page-{}.html"
page = 1
books = []

while True:
    url = base_url.format(page)
    response = requests.get(url)
    
    # hentikan jika halaman tidak ada
    if response.status_code != 200:
        break
    
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all("article", class_="product_pod")
    
    # hentikan jika tidak ada buku di halaman
    if not items:
        break
    
    for item in items:
        title = item.h3.a["title"]
        price = item.find("p", class_="price_color").text
        availability = item.find("p", class_="instock availability").text.strip()
        
        books.append({
            "judul": title,
            "harga": price,
            "availability": availability
        })
    
    print(f"Scraped halaman {page} dengan {len(items)} buku.")
    page += 1

# 3. Insert data ke MongoDB
if books:
    collection.insert_many(books)
    print(f"Total {len(books)} buku berhasil disimpan ke MongoDB.")
else:
    print("Tidak ada data buku yang ditemukan.")