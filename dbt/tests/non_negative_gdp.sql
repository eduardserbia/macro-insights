-- Fails if any negative GDP values exist in staging
select *
from {{ ref('stg_gdp') }}
where gdp_usd_bn < 0
