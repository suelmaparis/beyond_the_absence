import pandas as pd
from models import db, Resource
from app import app

csv_file = 'beyond_resources_full.csv'
df = pd.read_csv(csv_file)

def clean_value(x):
    if pd.isna(x):
        return None
    s = str(x).strip()
    return None if s == "" or s.lower() == "nan" else s

def fix_row(row):
    # normalize
    row = {k: clean_value(row.get(k)) for k in
           ["category","title","description","address","phone","website","email","tags"]}

    # remover lixo comum
    def strip_visit_site(v):
        if not v: return v
        v = v.replace("Website: Visit Site", "").strip()
        return v or None
    row["phone"] = strip_visit_site(row["phone"])
    row["address"] = strip_visit_site(row["address"])

    # se phone vier com URL, mover para website (se estiver vazio)
    if row.get("phone") and ("http://" in row["phone"] or "https://" in row["phone"]):
        if not row.get("website"):
            row["website"] = row["phone"]
        row["phone"] = None

    # padronizar website sem prefixo
    if row.get("website") and not row["website"].startswith(("http://","https://")):
        if "." in row["website"] and " " not in row["website"]:
            row["website"] = "https://" + row["website"]

    return row

with app.app_context():
    for _, r in df.iterrows():
        data = fix_row(r)
        db.session.add(Resource(**data))
    db.session.commit()

print("Importação concluída!")
