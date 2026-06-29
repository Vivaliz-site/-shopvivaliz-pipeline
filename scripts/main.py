import os
from PIL import Image
import pandas as pd

os.makedirs("storage/processed", exist_ok=True)
os.makedirs("logs", exist_ok=True)

def processar():
    for root, dirs, files in os.walk("storage/olist-images"):
        for file in files:
            if file.endswith(".jpg"):
                try:
                    img = Image.open(os.path.join(root, file))
                    img = img.resize((1000, 1000))
                    out = os.path.join("storage/processed", file)
                    img.save(out)
                except:
                    pass

def planilha():
    if not os.path.exists("planilhas/produtos.xlsx"):
        return
    df = pd.read_excel("planilhas/produtos.xlsx")
    if "sku" not in df.columns:
        return
    df["image_url"] = df["sku"].apply(lambda x: f"https://dev.shopvivaliz.com.br/uploads/olist/{x}/1.jpg")
    df.to_excel("planilhas/produtos_final.xlsx", index=False)

processar()
planilha()
