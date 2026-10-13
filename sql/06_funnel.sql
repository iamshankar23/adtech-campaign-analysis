-- Funnel with drop-off (CTE + LAG)
-- Question: Where is the biggest drop-off: impression, click, enquiry or sale?
WITH totals AS (
    SELECT SUM(impressions) AS i, SUM(clicks) AS c,
           SUM(enquiries)   AS e, SUM(sales)  AS s
    FROM ads
),
stages AS (
    SELECT 1 AS step, 'Impressions' AS stage, i AS value FROM totals
    UNION ALL SELECT 2, 'Clicks',    c FROM totals
    UNION ALL SELECT 3, 'Enquiries', e FROM totals
    UNION ALL SELECT 4, 'Sales',     s FROM totals
)
SELECT
    stage,
    value,
    ROUND(100.0 * value / LAG(value) OVER (ORDER BY step), 4) AS pct_of_previous_stage
FROM stages
ORDER BY step;
