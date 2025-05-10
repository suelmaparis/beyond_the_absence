import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns



from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

single_mom_df = pd.read_csv('db/single_mom_dataset.csv')

print(single_mom_df.info())

print(single_mom_df.describe())
print(single_mom_df.columns)

# Converter 'Timestamp' para datetime
single_mom_df['Timestamp'] = pd.to_datetime(single_mom_df['Timestamp'])

# Criar coluna apenas com a data
single_mom_df['date_only'] = single_mom_df['Timestamp'].dt.date

# Criar coluna apenas com a hora
single_mom_df['time_only'] = single_mom_df['Timestamp'].dt.time

# Remover a coluna original se quiser
single_mom_df.drop(columns=['Timestamp'], inplace=True)

# Confirmação
print(single_mom_df[['date_only', 'time_only']].head())


# Visualizar distribuição das idades
#sns.histplot(single_mom_df['age'], bins=10)
plt.title('Distribuição das Idades')
plt.show()

# Correlação geral
# Selecionar apenas colunas numéricas
numeric_df = single_mom_df.select_dtypes(include=['number'])
# Calcular a matriz de correlação
corr = numeric_df.corr()
#sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Mapa de Calor das Correlações')
plt.show()

