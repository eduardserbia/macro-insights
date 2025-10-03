-- Daily aggregated fact table based on stg_hello
SELECT
  toDate(ts) AS d,
  count()    AS rows_cnt
FROM {{ ref('stg_hello') }}
GROUP BY d
ORDER BY d DESC
