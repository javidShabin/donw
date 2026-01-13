import requests
from bs4 import BeautifulSoup
import os

headers = {"User-Agent": "Mozilla/5.0"}

product_links = [
    "https://iqracart.com/product/%e2%98%80%ef%b8%8f-cbk-solar-interaction-wall-lamp-model-bk-888-2/",
    "https://iqracart.com/product/10-perfume-combo-for-men-women-long-lasting-fragrance-100ml-each/",
    "https://iqracart.com/product/18-in-1-nail-care-kit-manicure-pedicure-tools/",
    "https://iqracart.com/product/200w-solar-charging-floodlight-dt-919lp-portable-waterproof-ip65-work-light/"
]

os.makedirs("images", exist_ok=True)

for index, url in enumerate(product_links, start=1):
    print(f"\nOpening {url}")
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.select_one("h1.product_title").text.strip()
    safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()

    product_folder = f"images/{safe_title}"
    os.makedirs(product_folder, exist_ok=True)

    gallery = soup.select("div.woocommerce-product-gallery__image")

    print("Found", len(gallery), "images")

    for i, g in enumerate(gallery, start=1):
        img_url = g.get("data-large_image")

        if not img_url:
            continue

        img_data = requests.get(img_url, headers=headers).content
        img_name = f"{product_folder}/img{i}.jpg"

        with open(img_name, "wb") as f:
            f.write(img_data)

        print("Saved", img_name)

print("\nALL DONE")
