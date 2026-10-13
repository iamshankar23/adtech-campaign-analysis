-- Spend on ads with zero sales  (Q2)
-- Question: How much money went to ads that produced no sales?
SELECT
    CASE WHEN sales = 0 THEN 'No sales' ELSE 'Had sales' END   AS ad_group,
    COUNT(*)                                                    AS ads,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)          AS ads_share_pct,
    ROUND(SUM(spend), 2)                                        AS spend,
    ROUND(100.0 * SUM(spend) / SUM(SUM(spend)) OVER (), 1)      AS spend_share_pct
FROM ads
GROUP BY ad_group;
