-- Enquiry-to-sale rate by age and gender  (Q4)
-- Question: Which segments turn enquiries into sales, and which do not?
SELECT
    age,
    gender,
    SUM(enquiries)                                              AS enquiries,
    SUM(sales)                                                  AS sales,
    ROUND(100.0 * SUM(sales) / NULLIF(SUM(enquiries), 0), 1)    AS enquiry_to_sale_pct,
    ROUND(100.0 * SUM(enquiries) / NULLIF(SUM(clicks), 0), 1)   AS click_to_enquiry_pct
FROM ads
GROUP BY age, gender
ORDER BY enquiry_to_sale_pct DESC;
