-- Custom singular test: fails if yoy_pct is out of expected bounds (-1..10)
select *
from {{ ref('fct_gdp_yoy') }}
where yoy_pct is not null
  and (yoy_pct < -1 or yoy_pct > 10)
