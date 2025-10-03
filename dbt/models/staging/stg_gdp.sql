-- Staging view over seed gdp
-- Keeps canonical types and basic constraints
select
  country_code::String   as country_code,  -- ISO/alpha-2-ish
  country_name::String   as country_name,
  toInt32(year)          as year,
  toFloat64(gdp_usd_bn)  as gdp_usd_bn
from {{ ref('gdp') }}      -- seed table name = CSV filename (without .csv)