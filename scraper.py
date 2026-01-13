import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

BASE_URL = "https://iqracart.com"
SHOP_URL = "https://iqracart.com/shop/"
headers = {"User-Agent": "Mozilla/5.0"}

os.makedirs("images", exist_ok=True)

print("Collecting product links...")
shop = requests.get(SHOP_URL, headers=headers)
shop_soup = BeautifulSoup(shop.text, "html.parser")

cards = shop_soup.select("li.product a.woocommerce-loop-product__link")

product_links = []
for c in cards:
    if c["href"] not in product_links:
        product_links.append(c["href"])

print(f"Found {len(product_links)} products")

products = []

for idx, link in enumerate(product_links, start=1):
    print(f"Scraping product {idx}/{len(product_links)}")

    res = requests.get(link, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    try:
        title = soup.select_one("h1.product_title").text.strip()
        price = soup.select_one("p.price").text.strip()
        description = soup.select_one("div.woocommerce-product-details__short-description").text.strip()

        product_folder = f"images/product_{idx}"
        os.makedirs(product_folder, exist_ok=True)

        image_paths = []

        images = soup.select("figure.woocommerce-product-gallery__wrapper img")

        for i, img in enumerate(images, start=1):
            srcset = img.get("srcset")

            if not srcset:
                continue

            # get the largest image from srcset
            best_url = srcset.split(",")[-1].split(" ")[0]

            img_data = requests.get(best_url, headers=headers).content

            img_name = f"{product_folder}/img{i}.jpg"

            with open(img_name, "wb") as f:
                f.write(img_data)

            image_paths.append(img_name)

        products.append({
            "title": title,
            "price": price,
            "description": description,
            "images": "|".join(image_paths),
            "link": link
        })

        print("Saved:", title, "with", len(image_paths), "images")

        time.sleep(1)

    except Exception as e:
        print("Error:", e)

pd.DataFrame(products).to_csv("products.csv", index=False)

print("ALL PRODUCTS + MULTIPLE IMAGES DOWNLOADED")
