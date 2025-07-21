-- volatility (stddev)
select country_code, stddev(annual_return_percent) as volatility
from stock_annual_returns
group by country_code;

-- 5-year rolling average of annual stock returns for each country
SELECT 
    s.country_code,
    s.year,
    ROUND(
        AVG(s.annual_return_percent) OVER (
            PARTITION BY s.country_code 
            ORDER BY s.year 
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ), 2
    ) AS five_year_avg_return
FROM stock_annual_returns s;

