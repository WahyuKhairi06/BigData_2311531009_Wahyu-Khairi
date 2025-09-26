import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://books.toscrape.com/catalogue/page-{}.html"
books = []
page = 1  

while True:
    url = base_url.format(page)
    response = requests.get(url)
    
    # jika halaman tidak ditemukan, hentikan loop
    if response.status_code != 200:
        break
    
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all("article", class_="product_pod")
    
    # jika tidak ada buku di halaman, hentikan loop
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
    page += 1  # lanjut ke halaman berikutnya

# simpan hasil
df = pd.DataFrame(books)
print(f"Total buku yang di-scrape: {len(df)}")
df.to_csv("books.csv", index=False)
df.to_json("books.json", orient="records", lines=True)
