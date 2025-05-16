import pandas as pd


df_unisef=pd.read_excel('db/UNICEF_Expanded_Global_Databases_ExclusiveBF_2024.xlsx', skiprows=4)
print(df_unisef.info())