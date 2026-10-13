-- CTR quartiles vs cost per sale (NTILE)  (Q3)
-- Question: Does a higher CTR mean cheaper sales?
WITH paid AS (
    SELECT *, 100.0 * clicks / impressions AS ctr
    FROM ads
    WHERE clicks > 0
),
banded AS (
    SELECT *, NTILE(4) OVER (ORDER BY ctr) AS ctr_band
    FROM paid
)
SELECT
    ctr_band,
    COUNT(*)                                                   AS ads,
    ROUND(MIN(ctr), 4)                                         AS min_ctr,
    ROUND(MAX(ctr), 4)                                         AS max_ctr,
    ROUND(SUM(spend), 2)                                       AS spend,
    SUM(sales)                                                 AS sales,
    ROUND(1.0 * SUM(spend) / NULLIF(SUM(sales), 0), 2)         AS cost_per_sale,
    ROUND(100.0 * SUM(enquiries) / SUM(clicks), 1)             AS click_to_enquiry_pct
FROM banded
GROUP BY ctr_band
ORDER BY ctr_band;
