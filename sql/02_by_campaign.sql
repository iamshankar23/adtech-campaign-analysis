-- Performance by campaign
-- Question: Which campaign is the most cost-efficient per sale, and where does the money go?
SELECT
    campaign_id,
    COUNT(*)                                              AS ads,
    ROUND(SUM(spend), 2)                                  AS spend,
    ROUND(100.0 * SUM(spend) / (SELECT SUM(spend) FROM ads), 1) AS spend_share_pct,
    SUM(sales)                                            AS sales,
    ROUND(100.0 * SUM(sales) / (SELECT SUM(sales) FROM ads), 1) AS sales_share_pct,
    ROUND(100.0 * SUM(clicks) / SUM(impressions), 4)      AS ctr_pct,
    ROUND(1.0 * SUM(spend) / SUM(clicks), 3)              AS cpc,
    ROUND(1.0 * SUM(spend) / NULLIF(SUM(sales), 0), 2)    AS cost_per_sale
FROM ads
GROUP BY campaign_id
ORDER BY spend DESC;
