# create database ;
# use database ;

select * from stock_data;
select * from macro_data;

select distinct index_name from stock_data;

select date, Close as nifty50_close
from stock_data
where index_name="Nifty 50 (India)"
order by date;

select year, gdp_growth_annual
from macro_data
where country="USA"
order by year;

select country, gdp_current_usd
from macro_data
where year = 2024
order by gdp_current_usd desc
limit 5;

