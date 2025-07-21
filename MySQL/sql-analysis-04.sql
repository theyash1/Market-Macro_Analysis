CREATE VIEW stock_annual_returns AS
SELECT 
    country_code,
    index_name,
    YEAR(date) AS year,
    MIN(DATE) AS start_date,
    MAX(DATE) AS end_date,
    SUBSTRING_INDEX(GROUP_CONCAT(close ORDER BY date), ',', 1) AS start_close,
    SUBSTRING_INDEX(GROUP_CONCAT(close ORDER BY date DESC), ',', 1) AS end_close,
    ROUND((SUBSTRING_INDEX(GROUP_CONCAT(close ORDER BY date DESC), ',', 1) - 
           SUBSTRING_INDEX(GROUP_CONCAT(close ORDER BY date), ',', 1)) / 
           SUBSTRING_INDEX(GROUP_CONCAT(close ORDER BY date), ',', 1) * 100, 2) AS annual_return_percent
FROM stock_data
GROUP BY country_code, index_name, YEAR(date);

CREATE VIEW stock_macro_annual AS
SELECT 
    s.*,
    m.gdp_growth_annual,
    m.inflation_percent_annual
FROM stock_annual_returns s
JOIN macro_data m 
    ON s.country_code = m.country_code
   AND s.year = m.year;

-- See GDP vs stock returns
SELECT * FROM stock_macro_annual WHERE country_code = 'USA';

-- Correlation-style insight
SELECT year, annual_return_percent, gdp_growth_annual
FROM stock_macro_annual
WHERE index_name = 'S&P 500 (USA)';

select * from stock_annual_returns;

