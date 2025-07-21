import wbdata
import pandas as pd
import datetime

# --- Display options for better readability ---
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# --- Define countries from yfinance setup ---
country_mapping_for_fetch = {
    "USA": "USA",      # S&P 500 
    "China": "CHN",    # Shanghai Composite
    "Japan": "JPN",    # Nikkei 225
    "Germany": "DEU",  # DAX
    "India": "IND"     # Nifty 50
}
countries_wb_codes = list(country_mapping_for_fetch.values())

# --- Get all World Bank country info ---
wb_countries = wbdata.get_countries()

# --- Create necessary mapping dictionaries ---
wb_name_to_your_name_map = {} # Maps WB full name (e.g., 'United States') to desired name (e.g., 'USA')
wb_full_name_to_code_map = {} # Maps WB full name to its 3-letter ISO code (e.g., 'United States' to 'USA')

for country_info in wb_countries:
    if country_info['id'] in countries_wb_codes:
        wb_full_name = country_info['name']
        wb_iso_code = country_info['id']

        # Populate wb_full_name_to_code_map
        wb_full_name_to_code_map[wb_full_name] = wb_iso_code

        # Populate wb_name_to_your_name_map for consistency with yfinance names
        if wb_iso_code == 'USA':
            wb_name_to_your_name_map[wb_full_name] = 'USA'
        elif wb_iso_code == 'CHN':
            wb_name_to_your_name_map[wb_full_name] = 'China'
        elif wb_iso_code == 'JPN':
            wb_name_to_your_name_map[wb_full_name] = 'Japan'
        elif wb_iso_code == 'DEU':
            wb_name_to_your_name_map[wb_full_name] = 'Germany'
        elif wb_iso_code == 'IND':
            wb_name_to_your_name_map[wb_full_name] = 'India'
        else: # Fallback, should not be hit for our selected countries
            wb_name_to_your_name_map[wb_full_name] = wb_full_name

# --- Define macroeconomic indicators (NOW INCLUDING FDI, GDP, Gross Savings) ---
indicators_to_fetch = {
    "FP.CPI.TOTL.ZG": "Inflation (Annual %)",
    "NY.GDP.MKTP.KD.ZG": "GDP Growth (Annual %)",
    "SP.POP.TOTL": "Total Population",
    "BX.KLT.DINV.WD.GD.ZS": "FDI Net Inflows (% of GDP)", # New
    "NY.GDP.MKTP.CD": "GDP (Current US$)",                 # New
    "NY.GNS.ICTR.ZS": "Gross Savings (% of GDP)"          # New
}

# --- Define date range (annual data for WB) ---
start_year = 2019
end_year = 2024 # Data for 2024 will likely have NaNs for some indicators due to lag

# Convert years to datetime objects for wbdata
start_date_wb = datetime.datetime(start_year, 1, 1)
end_date_wb = datetime.datetime(end_year, 12, 31)

# --- Fetch the data from World Bank ---
indicator_names_str = ", ".join(list(indicators_to_fetch.values()))
print(f"🔄 Downloading World Bank data for {list(country_mapping_for_fetch.keys())} for indicators: {indicator_names_str} from {start_year} to {end_year}...\n")
world_bank_dfs = []

try:
    temp_df = wbdata.get_dataframe(
        indicators_to_fetch,
        country=countries_wb_codes,
        date=(start_date_wb, end_date_wb)
    )

    # --- Reset index to make 'country' (WB full name) and 'date' (Year) regular columns ---
    temp_df = temp_df.reset_index()

    # --- Rename 'date' column to 'Year' ---
    temp_df.rename(columns={'date': 'Year'}, inplace=True)

    # --- Map 'country' column to your desired 'Country' names ---
    temp_df['Country'] = temp_df['country'].map(wb_name_to_your_name_map)

    # --- Map original 'country' column (full name) to 'CountryCode' (3-letter ISO) ---
    temp_df['CountryCode'] = temp_df['country'].map(wb_full_name_to_code_map)

    # --- Drop the original 'country' column ---
    temp_df.drop(columns=['country'], inplace=True)

    # Reorder columns for clarity
    world_bank_df_final = temp_df[['Country', 'CountryCode', 'Year'] + list(indicators_to_fetch.values())]

    world_bank_dfs.append(world_bank_df_final)

except Exception as e:
    print(f"❌ Failed to download World Bank data: {e}")

# --- Combine all into one table (if multiple fetches were made, but here it's one) ---
if not world_bank_dfs:
    print("❌ No World Bank data downloaded. Exiting.")
    exit()

final_world_bank_df = pd.concat(world_bank_dfs, ignore_index=True)

# --- Save the World Bank data ---
wb_file_name = "world_bank_macro_data_standardized.csv"
final_world_bank_df.to_csv(wb_file_name, index=False)

print(f"\n✅ Standardized World Bank data saved to '{wb_file_name}'")
print("\n📊 Final preview of World Bank data (showing all columns, including NaNs for 2024 where data is unavailable):")
print(final_world_bank_df.tail(10)) # Show more tail rows to capture more countries/years

print("\nMissing values per column in the final DataFrame:")
print(final_world_bank_df.isnull().sum())
