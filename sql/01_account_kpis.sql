-- Account KPIs
-- Question: What are the overall CTR, CPC, CPM and cost per sale?
SELECT
    COUNT(*)                                         AS ads,
    SUM(impressions)                                 AS impressions,
    SUM(clicks)                                      AS clicks,
    ROUND(SUM(spend), 2)                             AS spend,
    SUM(enquiries)                                   AS enquiries,
    SUM(sales)                                       AS sales,
    ROUND(100.0 * SUM(clicks) / SUM(impressions), 4) AS ctr_pct,
    ROUND(1.0 * SUM(spend) / SUM(clicks), 3)         AS cpc,
    ROUND(1000.0 * SUM(spend) / SUM(impressions), 3) AS cpm,
    ROUND(1.0 * SUM(spend) / SUM(sales), 2)          AS cost_per_sale
FROM ads;
