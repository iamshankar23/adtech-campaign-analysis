-- Biggest zero-sale ads in each campaign (ROW_NUMBER)  (Q2)
-- Question: Which individual ads wasted the most money, per campaign?
WITH zero_sale AS (
    SELECT ad_id, campaign_id, age, gender, interest, spend, clicks, enquiries,
           ROW_NUMBER() OVER (PARTITION BY campaign_id ORDER BY spend DESC) AS rn
    FROM ads
    WHERE sales = 0
)
SELECT campaign_id, rn AS rank_in_campaign, ad_id, age, gender, interest,
       ROUND(spend, 2) AS spend, clicks, enquiries
FROM zero_sale
WHERE rn <= 3
ORDER BY campaign_id, rn;
