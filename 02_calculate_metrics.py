
import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parent
CLEAN = BASE / "data" / "cleaned" / "ads_clean.csv"
OUT = BASE / "data" / "cleaned" / "ads_metrics.csv"

if not CLEAN.exists():
    raise SystemExit(f"Cleaned file not found: {CLEAN}\nRun 01_explore_and_clean.py first.")

df = pd.read_csv(CLEAN, dtype={"campaign_id": str})

def safe_div(a, b):
    return np.where(b > 0, a / b.replace(0, np.nan), np.nan)

df["ctr_pct"]       = safe_div(df.clicks, df.impressions) * 100
df["cpc"]           = safe_div(df.spend, df.clicks)
df["cpm"]           = safe_div(df.spend, df.impressions) * 1000
df["cost_per_enq"]  = safe_div(df.spend, df.enquiries)
df["cpa"]           = safe_div(df.spend, df.sales)          
df["click_to_enq"]  = safe_div(df.enquiries, df.clicks)
df["approval_rate"] = safe_div(df.sales, df.enquiries)      
df["has_sale"]      = (df.sales > 0).astype(int)

df.round(4).to_csv(OUT, index=False)
print("=== 1. METRICS ADDED ===")
print(df[["ad_id", "ctr_pct", "cpc", "cpm", "cost_per_enq", "cpa", "approval_rate"]].head().round(3).to_string())


def summarise(g):
    t = g[["impressions", "clicks", "spend", "enquiries", "sales"]].sum()
    return pd.Series({
        "ads": len(g),
        "spend": t.spend,
        "sales": t.sales,
        "ctr_pct": t.clicks / t.impressions * 100,
        "cpc": t.spend / t.clicks if t.clicks else np.nan,
        "cpm": t.spend / t.impressions * 1000,
        "cost_per_sale": t.spend / t.sales if t.sales else np.nan,
        "approval_rate": t.sales / t.enquiries if t.enquiries else np.nan,
    })


print("\n=== 2. ACCOUNT TOTAL ===")
print(summarise(df).round(3).to_string())

print("\n=== 3. BY CAMPAIGN ===")
print(df.groupby("campaign_id").apply(summarise, include_groups=False).round(3).to_string())

print("\n=== 4. FUNNEL ===")
f = df[["impressions", "clicks", "enquiries", "sales"]].sum()
print(f.to_string())
print("Impression -> click rate :", round(f.clicks / f.impressions * 100, 4), "%")
print("Click -> enquiry rate    :", round(f.enquiries / f.clicks * 100, 2), "%")
print("Enquiry -> sale rate     :", round(f.sales / f.enquiries * 100, 2), "%")

print("\n=== 5. Q2: SPEND ON ZERO-SALE ADS ===")
zero = df[df.sales == 0]
print("Zero-sale ads      :", len(zero), "of", len(df), f"({len(zero)/len(df):.1%})")
print("Spend on them      :", round(zero.spend.sum(), 2), f"({zero.spend.sum()/df.spend.sum():.1%} of total spend)")

print("\n=== 6. Q3: DOES HIGHER CTR MEAN CHEAPER SALES? ===")
paid = df[df.clicks > 0].copy()                      # ads that actually got clicks
paid["ctr_band"] = pd.qcut(paid.ctr_pct, 4, labels=["1 Lowest CTR", "2", "3", "4 Highest CTR"])
print(paid.groupby("ctr_band", observed=True).apply(summarise, include_groups=False)[
    ["ads", "spend", "sales", "ctr_pct", "cost_per_sale", "approval_rate"]].round(3).to_string())

print("\nSaved:", OUT)