-- Efficiency index by segment (spend and sales vs account average)
-- Question: How much more or less expensive is each segment than the account average?
WITH account AS (
    SELECT 1.0 * SUM(spend) / SUM(sales) AS avg_cost_per_sale FROM ads
)
SELECT
    a.age,
    a.gender,
    ROUND(SUM(a.spend), 2)                                         AS spend,
    SUM(a.sales)                                                   AS sales,
    ROUND(1.0 * SUM(a.spend) / NULLIF(SUM(a.sales), 0), 2)         AS cost_per_sale,
    ROUND(1.0 * SUM(a.spend) / NULLIF(SUM(a.sales), 0)
          / acc.avg_cost_per_sale, 2)                              AS index_vs_average
FROM ads a
CROSS JOIN account acc
GROUP BY a.age, a.gender
ORDER BY index_vs_average DESC;
