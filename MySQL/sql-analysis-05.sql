alter table stock_data
add primary key (date, index_name, country_code);

alter table macro_data
add primary key (year, country_code);

select * from stock_annual_returns; 

-- Average returns by country
SELECT country_code, AVG(annual_return_percent) AS avg_return
FROM stock_annual_returns
GROUP BY country_code;

