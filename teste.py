import pandas as pd
from country_continent_map import country_continent_map

df = pd.read_csv('db/mom_world_dataset.csv', skiprows=4)
# Lista de regiões que queremos excluir
excluidos = [
    'Africa Eastern and Southern',
    'Africa Western and Central',
    'Arab World',
    'World',
    'High income',
    'Low income',
    'Upper middle income',
    'Lower middle income',
    'Low & middle income',
    'OECD members',
    'Fragile and conflict affected situations',
    'Latin America & Caribbean',
    'Sub-Saharan Africa',
    'Europe & Central Asia',
    'Middle East & North Africa',
    'South Asia',
    'East Asia & Pacific'
]

df = df[~df['Country Name'].isin(excluidos)]

df['Continent'] = df['Country Name'].map(country_continent_map)
print(df['Continent'].head())
print(df['Continent'].value_counts())

\
print(df.columns.tolist())
