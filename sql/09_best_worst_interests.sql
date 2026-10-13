-- Best and worst interest codes by cost per sale (RANK)  (Q5)
-- Question: Which interest codes give the cheapest and the most expensive sales (spend of at least 500)?
WITH by_interest AS (
    SELECT interest,
           SUM(spend)                                    AS spend,
           SUM(sales)                                    AS sales,
           1.0 * SUM(spend) / NULLIF(SUM(sales), 0)      AS cost_per_sale
    FROM ads
    GROUP BY interest
    HAVING SUM(spend) >= 500 AND SUM(sales) > 0
),
ranked AS (
    SELECT *,
           RANK() OVER (ORDER BY cost_per_sale ASC)  AS cheapest_rank,
           RANK() OVER (ORDER BY cost_per_sale DESC) AS priciest_rank
    FROM by_interest
)
SELECT
    CASE WHEN cheapest_rank <= 5 THEN 'Cheapest' ELSE 'Most expensive' END AS group_name,
    interest,
    ROUND(spend, 2)         AS spend,
    sales,
    ROUND(cost_per_sale, 2) AS cost_per_sale
FROM ranked
WHERE cheapest_rank <= 5 OR priciest_rank <= 5
ORDER BY cost_per_sale;
