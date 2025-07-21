# python -m venv venv
# .\venv\Scripts\activate

import yfinance as yf
import pandas as pd
from datetime import date

# --- Display options for better readability ---
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# --- Define time range ---
start_date = "2019-05-01"
end_date = date.today().isoformat()

# --- Top index from each country + Crude Oil ---
indices = {
    "S&P 500 (USA)": "^GSPC",
    "Shanghai Composite (China)": "000001.SS",
    "Nikkei 225 (Japan)": "^N225",
    "DAX (Germany)": "^GDAXI",
    "Nifty 50 (India)": "^NSEI",
    "WTI Crude Oil (CL=F)": "CL=F"  # Crude oil futures
}

# --- Download and combine ---
dfs = []

for name, symbol in indices.items():
    print(f"🔄 Downloading data for {name} ({symbol})...")
    try:
        df = yf.download(symbol, start=start_date, end=end_date)

        # Flatten multi-level columns if needed
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        required_cols = ["Open", "High", "Low", "Close"]
        if not all(col in df.columns for col in required_cols):
            print(f"⚠️ Missing required columns for {name}. Skipping.")
            continue

        df = df[required_cols].reset_index()
        df["Index"] = name

        # Reorder for clarity
        df = df[["Date", "Index", "Open", "High", "Low", "Close"]]
        dfs.append(df)
    except Exception as e:
        print(f"❌ Failed to download {name}: {e}")

# --- Combine all into one table ---
if not dfs:
    print("❌ No data downloaded. Exiting.")
    exit()

final_df = pd.concat(dfs, ignore_index=True)

# --- Save ---
file_name = "top_indices_and_crude_oil_comparison.csv"
final_df.to_csv(file_name, index=False)

print(f"\n✅ Data saved in table format to '{file_name}'")
print("\n📊 Final preview:")
print(final_df.tail())
print("\n")
print(final_df.head())
