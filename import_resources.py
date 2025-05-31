import csv
from app import app, db
from models import Resource
import pandas as pd

df_special = pd.read_excel("db/special_needs_moms.xlsx", header=0)  # <- Lê a linha correta como cabeçalho
df_special.columns = df_special.columns.str.strip().str.lower().str.replace(' ', '_')

print("📊 Colunas finais:", df_special.columns.tolist())





