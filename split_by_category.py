import pandas as pd
import os
import re

df = pd.read_csv("products.csv")

if "category" not in df.columns:
    print("ERROR: 'category' column not found in products.csv")
    exit()

output_dir = "category_excel"
os.makedirs(output_dir, exist_ok=True)

print("Saving files to:", os.path.abspath(output_dir))

for category, group in df.groupby("category"):

    if pd.isna(category):
        continue

    # ✅ clean filename (remove invalid characters)
    safe_category = re.sub(r'[\\/:*?"<>|]', "_", category)

    file_path = os.path.join(output_dir, f"{safe_category}.xlsx")
    group.to_excel(file_path, index=False)

print("✅ ALL CATEGORY EXCEL FILES CREATED")
