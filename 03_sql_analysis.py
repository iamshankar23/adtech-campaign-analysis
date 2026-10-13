import sqlite3
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent
CLEAN = BASE / "data" / "cleaned" / "ads_clean.csv"
DB = BASE / "data" / "ads.db"
SQL_DIR = BASE / "sql"
DOCS = BASE / "docs"

if not CLEAN.exists():
    raise SystemExit(f"Cleaned file not found: {CLEAN}\nRun 01_explore_and_clean.py first.")
SQL_DIR.mkdir(exist_ok=True)
DOCS.mkdir(exist_ok=True)

df = pd.read_csv(CLEAN, dtype={"campaign_id": str})
conn = sqlite3.connect(DB)
df.to_sql("ads", conn, if_exists="replace", index=False)

# Every query: (file_name, title, business_question, sql)
QUERIES = [

("01_account_kpis", "Account KPIs",
 "What are the overall CTR, CPC, CPM and cost per sale?",
"""
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
"""),

("02_by_campaign","Performance by campaign",
 "Which campaign is the most cost-efficient per sale, and where does the money go?",
"""
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
"""),

("03_spend_vs_sales_by_segment", "Spend share vs sales share by age and gender  (Q1)",
 "Which segments take a big share of spend but give a smaller share of sales?",
"""
SELECT
    age,
    gender,
    ROUND(SUM(spend), 2)                                         AS spend,
    ROUND(100.0 * SUM(spend) / SUM(SUM(spend)) OVER (), 1)       AS spend_share_pct,
    SUM(sales)                                                   AS sales,
    ROUND(100.0 * SUM(sales) / SUM(SUM(sales)) OVER (), 1)       AS sales_share_pct,
    ROUND(100.0 * SUM(spend) / SUM(SUM(spend)) OVER ()
        - 100.0 * SUM(sales) / SUM(SUM(sales)) OVER (), 1)       AS gap_pts,
    ROUND(1.0 * SUM(spend) / NULLIF(SUM(sales), 0), 2)           AS cost_per_sale
FROM ads
GROUP BY age, gender
ORDER BY gap_pts DESC;
"""),

("04_zero_sale_spend", "Spend on ads with zero sales  (Q2)",
 "How much money went to ads that produced no sales?",
"""
SELECT
    CASE WHEN sales = 0 THEN 'No sales' ELSE 'Had sales' END   AS ad_group,
    COUNT(*)                                                    AS ads,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)          AS ads_share_pct,
    ROUND(SUM(spend), 2)                                        AS spend,
    ROUND(100.0 * SUM(spend) / SUM(SUM(spend)) OVER (), 1)      AS spend_share_pct
FROM ads
GROUP BY ad_group;
"""),

("05_approval_by_segment", "Enquiry-to-sale rate by age and gender  (Q4)",
 "Which segments turn enquiries into sales, and which do not?",
"""
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
"""),

("06_funnel", "Funnel with drop-off (CTE + LAG)",
 "Where is the biggest drop-off: impression, click, enquiry or sale?",
"""
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
"""),

("07_ctr_bands", "CTR quartiles vs cost per sale (NTILE)  (Q3)",
 "Does a higher CTR mean cheaper sales?",
"""
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
"""),

("08_interest_pareto", "Budget concentration by interest code (running total)  (Q5)",
 "How concentrated is the budget in a few interest codes?",
"""
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
"""),

("09_best_worst_interests", "Best and worst interest codes by cost per sale (RANK)  (Q5)",
 "Which interest codes give the cheapest and the most expensive sales (spend of at least 500)?",
"""
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
"""),

("10_efficiency_index", "Efficiency index by segment (spend and sales vs account average)",
 "How much more or less expensive is each segment than the account average?",
"""
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
"""),

("11_top_wasted_ads_per_campaign", "Biggest zero-sale ads in each campaign (ROW_NUMBER)  (Q2)",
 "Which individual ads wasted the most money, per campaign?",
"""
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
"""),
]

report = []
for file_name, title, question, sql in QUERIES:
    (SQL_DIR / f"{file_name}.sql").write_text(
        f"-- {title}\n-- Question: {question}\n{sql.strip()}\n", encoding="utf-8")
    result = pd.read_sql(sql, conn)
    block = f"\n{'=' * 78}\n{title}\nQuestion: {question}\n{'-' * 78}\n{result.to_string(index=False)}\n"
    print(block)
    report.append(block)

(DOCS / "sql_results.txt").write_text("".join(report), encoding="utf-8")
conn.close()
print("\nDone.")
print("Database :", DB)
print("SQL files:", SQL_DIR)
print("Results  :", DOCS / "sql_results.txt")