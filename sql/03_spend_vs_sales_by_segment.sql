-- Spend share vs sales share by age and gender  (Q1)
-- Question: Which segments take a big share of spend but give a smaller share of sales?
SELECT
    age,
    gender,
    ROUND(SUM(spend), 2)                                         AS spend,
    ROUND(100.0 * SUM(spend) / SUM(SUM(spend)) OVER (), 1)       AS spend_share_pct,
    SUM(sales)                                                   AS sales,
    ROUND(100.0 * SUM(sales) / SUM(SUM(sales)) OVER (), 1)       AS sales_share_pct,
    ROUND(100.0 * SUM(spend) / SUM(SUM(spend)) OVER ()
        - 100.0 * SUM(sales) / SUM(SUM(sales)) OVER (), 1)       AS gap_pts,
    ROUND(1.0 * SUM(spend) / NULLIF(SUM(sales), 0), 2)           AS cost_per_sale
FROM ads
GROUP BY age, gender
ORDER BY gap_pts DESC;
