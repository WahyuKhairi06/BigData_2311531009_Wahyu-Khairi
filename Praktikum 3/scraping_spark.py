import requests
from bs4 import BeautifulSoup
from pyspark.sql import SparkSession

# 1. Buat Spark Session
spark = SparkSession.builder \
    .appName("ScrapingBooksSparkDynamic") \
    .getOrCreate()

# 2. Fungsi untuk scrape satu halaman
def scrape_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        return []  
    
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("article", class_="product_pod")
    
    page_books = []
    for article in articles:
        title = article.h3.a["title"]
        price = article.find("p", class_="price_color").text
        availability = article.find("p", class_="instock availability").text.strip()
        page_books.append((title, price, availability))
    return page_books

# 3. Scraping seluruh halaman 
books_data = []
base_url = "https://books.toscrape.com/catalogue/page-{}.html"
page = 1

while True:
    url = base_url.format(page)
    page_books = scrape_page(url)
    
    if not page_books:  
        break
    
    books_data.extend(page_books)
    print(f"Scraped halaman {page} dengan {len(page_books)} buku.")
    page += 1

# 4. Konversi ke Spark DataFrame
columns = ["title", "price", "availability"]
df = spark.createDataFrame(books_data, columns)

# 5. Tampilkan 5 data pertama
df.show(5, truncate=False)

# 6. Simpan ke CSV & Parquet via Pandas
pdf = df.toPandas()
pdf.to_csv("books_spark.csv", index=False)
pdf.to_parquet("books_spark.parquet", index=False)

print(f"Total buku yang di-scrape: {len(books_data)}")
print("Data berhasil disimpan ke CSV & Parquet via Pandas!")

# 7. Stop Spark session
spark.stop()