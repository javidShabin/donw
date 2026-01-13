import pandas as pd

df = pd.read_csv("products.csv")

def detect_category(title):
    t = str(title).lower()

    if any(x in t for x in ["perfume", "musk", "eau de"]):
        return "Beauty > Fragrance"

    if any(x in t for x in ["face wash", "scrub", "derma", "skincare"]):
        return "Beauty > Skincare"

    if any(x in t for x in ["lamp", "light", "floodlight"]):
        return "Electronics > Lighting"

    if any(x in t for x in ["fan", "humidifier"]):
        return "Home Appliances"

    if "drone" in t:
        return "Electronics > Gadgets"

    if any(x in t for x in ["bag", "handbag", "purse"]):
        return "Fashion > Bags"

    if any(x in t for x in ["shaper", "vest", "shapewear"]):
        return "Fashion > Clothing"

    if any(x in t for x in ["massager", "grip", "roller skates"]):
        return "Sports & Fitness"

    return "Misc"

df["category"] = df["title"].apply(detect_category)

df.to_csv("products.csv", index=False)

print("✅ CATEGORY AUTO-FILLED IN products.csv")
