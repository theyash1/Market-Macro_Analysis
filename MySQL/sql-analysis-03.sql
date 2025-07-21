use global_analysis;

create table index_country_map (
index_name varchar(100),
country_code varchar(10)
);

insert into index_country_map (index_name, country_code) values
('S&P 500 (USA)',"USA"),
("WTI Crude Oil (CL=F)","Global"),
("DAX (Germany)","DEU"),
("Nikkei 225 (Japan)","JPN"),
("Nifty 50 (India)","IND"),
("Shanghai Composite (China)","CHN");

alter table stock_data add column country_code varchar(10);

# set sql_safe_updates = 1;

update stock_data sd
join index_country_map map on sd.index_name = map.index_name
set sd.country_code = map.country_code;

create view stock_macro_view as
SELECT 
    s.date,
    s.index_name,
    s.country_code,
    s.close,
    YEAR(s.date) AS stock_year,
    m.year AS macro_year,
    m.gdp_growth_annual,
    m.inflation_percent_annual
from stock_data s
join macro_data m
	on s.country_code = m.country_code
    and year(s.date) = m.year;

select * from stock_macro_view limit 10;








