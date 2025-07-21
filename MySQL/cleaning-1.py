import pandas as pd

df = pd.read_csv("top_indices_and_crude_oil_comparison_sheet_xls - all_data.csv")

for col in ['Open','High','Low', 'Close']:
    df[col] = df[col].astype(str).str.replace(',','').astype(float)

# print(df.head())

df.to_csv("cleaned_stock_data.csv", index=False)
