from playwright.sync_api import sync_playwright
import requests
import os

product_links = [
    "https://iqracart.com/product/%e2%98%80%ef%b8%8f-cbk-solar-interaction-wall-lamp-model-bk-888-2/",
    "https://iqracart.com/product/10-perfume-combo-for-men-women-long-lasting-fragrance-100ml-each/",
    "https://iqracart.com/product/18-in-1-nail-care-kit-manicure-pedicure-tools/",
    "https://iqracart.com/product/200w-solar-charging-floodlight-dt-919lp-portable-waterproof-ip65-work-light/"
]

os.makedirs("images", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    for link in product_links:
        print("\nOpening", link)
        page.goto(link)
        page.wait_for_timeout(3000)

        title = page.locator("h1.product_title").inner_text()
        safe_title = "".join(c for c in title if c.isalnum() or c in " -_")

        folder = f"images/{safe_title}"
        os.makedirs(folder, exist_ok=True)

        images = page.locator(".woocommerce-product-gallery__image img")

        count = images.count()
        print("Found", count, "images")

        for i in range(count):
            img_url = images.nth(i).get_attribute("src")

            if img_url:
                img_data = requests.get(img_url).content
                path = f"{folder}/img{i+1}.jpg"
                with open(path, "wb") as f:
                    f.write(img_data)
                print("Saved", path)

    browser.close()
