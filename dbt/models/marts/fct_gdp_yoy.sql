/* GDP YoY: percentage change vs previous year (TABLE) */
{{ config(materialized='table') }}

with base as (
  select
    country_code,
    country_name,
    year,
    gdp_usd_bn,
    lag(gdp_usd_bn, 1) over (partition by country_code order by year) as gdp_prev
  from {{ ref('stg_gdp') }}
)

select
  country_code,
  any(country_name) as country_name,  -- CH aggregate to keep a single value
  year,
  gdp_usd_bn,
  gdp_prev,
  -- YoY formula (null/zero safe)
  if(gdp_prev = 0 OR gdp_prev IS NULL, NULL, (gdp_usd_bn - gdp_prev) / gdp_prev) as yoy_pct
from base
group by
  country_code, year, gdp_usd_bn, gdp_prev
order by country_code, year