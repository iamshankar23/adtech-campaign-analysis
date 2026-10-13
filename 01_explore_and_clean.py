
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent
RAW = BASE / "data" / "raw" / "KAG_conversion_data.csv"
CLEAN = BASE / "data" / "cleaned" / "ads_clean.csv"

if not RAW.exists():
    raise SystemExit(f"CSV not found here: {RAW}\nPut KAG_conversion_data.csv in that folder.")
CLEAN.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW)

print("=== 1. SHAPE (rows, columns) ===")
print(df.shape)

print("\n=== 2. COLUMNS ===")
print(df.columns.tolist())

print("\n=== 3. FIRST 5 ROWS ===")
print(df.head().to_string())

print("\n=== 4. MISSING VALUES ===")
print(df.isna().sum())

print("\n=== 5. DUPLICATE ROWS ===")
print(df.duplicated().sum())

print("\n=== 6. CATEGORY COUNTS ===")
for col in ["xyz_campaign_id", "age", "gender"]:
    print(df[col].value_counts(), "\n")

print("=== 7. ACCOUNT TOTALS ===")
cols = ["Impressions", "Clicks", "Spent", "Total_Conversion", "Approved_Conversion"]
totals = df[cols].sum()
print(totals)
print("CTR %          :", round(totals.Clicks / totals.Impressions * 100, 4))
print("CPC            :", round(totals.Spent / totals.Clicks, 2))
print("CPM            :", round(totals.Spent / totals.Impressions * 1000, 2))
print("CPA (per sale) :", round(totals.Spent / totals.Approved_Conversion, 2))

print("\n=== 8. ODD ROWS ===")
print("Zero-click rows    :", (df.Clicks == 0).sum())
print("Zero-spend rows    :", (df.Spent == 0).sum())
print("Enquiries > clicks :", (df.Total_Conversion > df.Clicks).sum())

df = df.rename(columns={
    "xyz_campaign_id": "campaign_id",
    "Impressions": "impressions",
    "Clicks": "clicks",
    "Spent": "spend",
    "Total_Conversion": "enquiries",
    "Approved_Conversion": "sales",
})
df.columns = df.columns.str.lower()

df["campaign_id"] = df["campaign_id"].astype(str)
df["age"] = df["age"].astype("category")
df["gender"] = df["gender"].astype("category")
df["spend"] = df["spend"].round(2)

df["no_activity_flag"] = ((df.clicks == 0) & (df.spend == 0)).astype(int)
df["enq_gt_clicks_flag"] = (df.enquiries > df.clicks).astype(int)

assert (df.clicks <= df.impressions).all(), "clicks exceed impressions"
assert (df.sales <= df.enquiries).all(), "sales exceed enquiries"
assert (df.spend >= 0).all(), "negative spend"
print("\n=== 9. SANITY CHECKS === all passed")

print("\n=== 10. FLAGGED ROWS ===")
print(df[["no_activity_flag", "enq_gt_clicks_flag"]].sum())
print("\nEnquiries and sales on no-activity rows (0 = normal rows, 1 = flagged):")
print(df.groupby("no_activity_flag")[["enquiries", "sales"]].sum())

df.to_csv(CLEAN, index=False)
print("\n=== 11. SAVED ===")
print(CLEAN, "->", df.shape[0], "rows,", df.shape[1], "columns")
print(df.columns.tolist())