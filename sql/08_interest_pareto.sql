-- Budget concentration by interest code (running total)  (Q5)
-- Question: How concentrated is the budget in a few interest codes?
WITH by_interest AS (
    SELECT interest,
           SUM(spend) AS spend,
           SUM(sales) AS sales
    FROM ads
    GROUP BY interest
)
SELECT
    interest,
    ROUND(spend, 2)                                                         AS spend,
    sales,
    ROUND(1.0 * spend / NULLIF(sales, 0), 2)                                AS cost_per_sale,
    ROUND(100.0 * spend / SUM(spend) OVER (), 1)                            AS spend_share_pct,
    ROUND(100.0 * SUM(spend) OVER (ORDER BY spend DESC
          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
          / SUM(spend) OVER (), 1)                                          AS cumulative_spend_pct
FROM by_interest
ORDER BY spend DESC
LIMIT 15;
