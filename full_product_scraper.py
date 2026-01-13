from playwright.sync_api import sync_playwright
import pandas as pd
import requests
import os
import time

product_links = [
    "https://iqracart.com/product/%e2%98%80%ef%b8%8f-cbk-solar-interaction-wall-lamp-model-bk-888-2/",
    "https://iqracart.com/product/10-perfume-combo-for-men-women-long-lasting-fragrance-100ml-each/",
    "https://iqracart.com/product/18-in-1-nail-care-kit-manicure-pedicure-tools/",
    "https://iqracart.com/product/200w-solar-charging-floodlight-dt-919lp-portable-waterproof-ip65-work-light/",
    "https://iqracart.com/product/3x-elastic-bandage-washable-reusable-super-stretchable-support-wrap/",
    "https://iqracart.com/product/5-in-1-mobile-creator-dock-wireless-audio-station-phone-stand-power-bank-microphone-hub/",
    "https://iqracart.com/product/540-needles-derma-roller-skin-rejuvenation-collagen-therapy-tool/",
    "https://iqracart.com/product/8-inch-oscillating-clip-fan-2-speed-adjustable-desk-fan-with-2200-rpm-power/",
    "https://iqracart.com/product/adjustable-counting-grip-hand-forearm-strength-trainer/",
    "https://iqracart.com/product/adjustable-hand-grip-strengthener-with-smart-counter/",
    "https://iqracart.com/product/adjustable-inline-roller-skates-comfortable-durable-smooth-ride-for-all-ages/",
    "https://iqracart.com/product/aloe-vera-foam-face-wash-for-acne-oil-control-100ml-touch-me-please/",
    "https://iqracart.com/product/apple-ammonia-free-hair-color-gel-100-gray-coverage-long-lasting-natural-black-for-men-women/",
    "https://iqracart.com/product/arman-eau-de-perfume-from-lavish-perfumes-100ml-3-4-fl-oz/",
    "https://iqracart.com/product/avocado-face-wash-deep-cleanse-whitening-anti-aging-100ml-touch-me-please/",
    "https://iqracart.com/product/ball-blowing-train-atomizing-humidifier-toy-with-lights-music-spray-function/",
    "https://iqracart.com/product/blueidea-mini-fascial-gun-deep-muscle-massage-model-bld-668/",
    "https://iqracart.com/product/brut-eau-de-toilette-for-men-100ml-classic-masculine-fragrance/",
    "https://iqracart.com/product/caliph-hamraa-ahwa-eau-de-parfum-100ml-oriental-luxury-unisex-fragrance/",
    "https://iqracart.com/product/coffee-turmeric-face-wash-deep-cleanse-oil-free-100ml-touch-me-please/",
    "https://iqracart.com/product/colors-pour-femme-eau-de-parfum-100ml-gianni-venturi/",
    "https://iqracart.com/product/colors-pour-homme-eau-de-parfum-100ml-gianni-venturi/",
    "https://iqracart.com/product/concord-8-in-1-stainless-steel-manicure-pedicure-kit-travel-nail-care-set/",
    "https://iqracart.com/product/digital-quran-reading-pen-smart-portable-reader-with-built-in-speaker-3gb-memory-ideal-for-learning-recitation/",
    "https://iqracart.com/product/dual-fan-mist-humidifier-3-speed-portable-spray-cooling-fan-rechargeable-personal-desktop-cooler/",
    "https://iqracart.com/product/e99-drone-pro-wifi-real-time-hd-camera-drone/",
    "https://iqracart.com/product/elegant-womens-handbag-with-scarf-handle-premium-textured-top-handle-purse-maroon/",
    "https://iqracart.com/product/energizing-coffee-scrub-for-cellulite-stretch-marks-glowing-skin-500ml/",
    "https://iqracart.com/product/lavish-1000-zahra-bukhoor-83g-premium-oriental-incense/",
    "https://iqracart.com/product/kuwait-shop-white-silk-musk-luxurious-long-lasting-perfume-for-body-sensitive-areas/",
    "https://iqracart.com/product/kuwait-shop-vip-musk-luxurious-distinctive-all-day-fragrance-6ml/",
    "https://iqracart.com/product/kuwait-shop-pomegranate-musk-fruity-sensual-fragrance-12ml/",
    "https://iqracart.com/product/kuwait-shop-powder-musk-clean-fresh-scent-for-all-day-wear-12ml/",
    "https://iqracart.com/product/just-one-shapers-seamless-waist-shapewear/",
    "https://iqracart.com/product/impex-hunter-z-rechargeable-tactical-led-flashlight-ipx5-waterproof-zoomable-aircraft-grade-aluminum/",
    "https://iqracart.com/product/head-massager-for-scalp-relief-flexible-arms-multi-point-relaxation-tool/",
    "https://iqracart.com/product/hamda-bukhoor-premium-long-lasting-home-fragrance/",
    "https://iqracart.com/product/fully-automatic-electric-fruit-peeler-one-touch-skin-remover-for-grapes-cherry-tomatoes-kiwi-more/",
    "https://iqracart.com/product/the-flameglow-portable-led-lantern-speaker-wireless-bluetooth-realistic-flame-effect/",
    "https://iqracart.com/product/fitente-mens-body-sculpting-vest-thin-waist-slimming-compression-tank-top-model-st-7562/"
]

os.makedirs("images", exist_ok=True)
products = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    for idx, link in enumerate(product_links, start=1):
        print(f"\nScraping {idx}/{len(product_links)}")
        page.goto(link)
        page.wait_for_timeout(4000)

        title = page.locator("h1.product_title").inner_text()
        price = page.locator("p.price").inner_text()
        desc = page.locator("div.woocommerce-product-details__short-description").inner_text()

        safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()
        folder = f"images/{safe_title}"
        os.makedirs(folder, exist_ok=True)

        image_paths = []

        images = page.locator(".woocommerce-product-gallery__image img")
        count = images.count()

        for i in range(count):
            img_url = images.nth(i).get_attribute("src")
            if img_url:
                img_data = requests.get(img_url).content
                img_path = f"{folder}/img{i+1}.jpg"
                with open(img_path, "wb") as f:
                    f.write(img_data)
                image_paths.append(img_path)

        products.append({
            "title": title,
            "price": price,
            "description": desc,
            "images": "|".join(image_paths),
            "link": link
        })

        print("Saved:", title, "(", len(image_paths), "images )")
        time.sleep(1)

    browser.close()

pd.DataFrame(products).to_csv("products.csv", index=False)
print("\nALL PRODUCTS SAVED INTO products.csv")
