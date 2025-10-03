{{ config(materialized='view') }}
-- Staging GDP with year filter and deterministic deduplication

with src as (
    select
        country_code,
        country_name,
        toInt32(year)       as year,
        toFloat64(gdp_usd_bn) as gdp_usd_bn
    from {{ ref('gdp') }}
    where year between 2010 and 2025  -- project scope
),

dedup as (
    select
        country_code,
        country_name,
        year,
        gdp_usd_bn
    from (
        select
            s.*,
            row_number() over (
                partition by country_code, year
                order by (gdp_usd_bn is null) asc, gdp_usd_bn desc
            ) as rn
        from src s
    )
    where rn = 1   -- keep exactly one row per (country_code, year)
)

select * from dedup