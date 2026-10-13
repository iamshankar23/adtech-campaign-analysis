from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent
CLEAN = BASE / "data" / "cleaned" / "ads_clean.csv"
OUT = BASE / "docs" / "what_if_results.txt"

if not CLEAN.exists():
    raise SystemExit(f"File not found: {CLEAN}\nRun 01_explore_and_clean.py first.")
OUT.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CLEAN, dtype={"campaign_id": str})

# 1) One row per age x gender group
seg = (
    df.groupby(["age", "gender"], observed=True)
      .agg(spend=("spend", "sum"), sales=("sales", "sum"))
      .reset_index()
)
seg["cost_per_sale"] = seg["spend"] / seg["sales"]

total_spend = seg["spend"].sum()
total_sales = seg["sales"].sum()
avg_cps = total_spend / total_sales     
BAND = 0.10
def role_of(cps):
    if cps > avg_cps * (1 + BAND):
        return "donor"
    if cps < avg_cps * (1 - BAND):
        return "receiver"
    return "hold"
seg["role"] = seg["cost_per_sale"].apply(role_of)

lines = []
def show(text=""):
    print(text)
    lines.append(text)

show("WHAT-IF BUDGET REALLOCATION (age x gender)")
show("=" * 60)
show(f"Total spend: {total_spend:,.2f} | Total sales: {total_sales:,.0f} | "
     f"Average cost per sale: {avg_cps:.2f}")
show()
show("Current picture (sorted from most to least expensive per sale):")
show(seg.sort_values("cost_per_sale", ascending=False)
        .to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
show()

def scenario(shift_pct, haircut):
    """Move shift_pct of each donor's spend to receivers (same total budget).
    haircut = how much WORSE the extra money performs (0.25 = 25% higher cost per sale)."""
    s = seg.copy()
    donors = s["role"] == "donor"
    receivers = s["role"] == "receiver"

    cut = s.loc[donors, "spend"] * shift_pct
    pool = cut.sum()

    s["new_spend"] = s["spend"]
    s.loc[donors, "new_spend"] = s.loc[donors, "spend"] - cut
    # extra money goes to receivers in proportion to their current spend
    share = s.loc[receivers, "spend"] / s.loc[receivers, "spend"].sum()
    added = pool * share
    s.loc[receivers, "new_spend"] = s.loc[receivers, "spend"] + added

    # donors: lose sales at their usual cost per sale
    s["new_sales"] = s["sales"].astype(float)
    s.loc[donors, "new_sales"] = s.loc[donors, "new_spend"] / s.loc[donors, "cost_per_sale"]
    # receivers: extra spend buys sales at a worse (haircut) cost per sale
    s.loc[receivers, "new_sales"] = (
        s.loc[receivers, "sales"]
        + added / (s.loc[receivers, "cost_per_sale"] * (1 + haircut))
    )
    return s["new_sales"].sum()

show("SCENARIOS (total budget stays the same)")
show("shift = share of each donor group's budget moved away")
show("haircut = how much worse the extra money performs than the group's past average")
show("-" * 60)
rows = []
for shift in (0.10, 0.20, 0.30):
    for haircut in (0.0, 0.25, 0.50):
        new_sales = scenario(shift, haircut)
        rows.append({
            "shift_%": int(shift * 100),
            "haircut_%": int(haircut * 100),
            "new_sales": round(new_sales, 1),
            "extra_sales": round(new_sales - total_sales, 1),
            "uplift_%": round(100 * (new_sales / total_sales - 1), 1),
            "new_cost_per_sale": round(total_spend / new_sales, 2),
        })
show(pd.DataFrame(rows).to_string(index=False))
show()
show("HOW TO READ THIS")
show("- haircut 0% is the optimistic case (extra money works as well as before).")
show("- haircut 50% is the cautious case (extra money works 50% worse).")
show("- Real ad platforms show diminishing returns, so quote the cautious case first.")
show("- This is an estimate from past data, not a promise. Test with a small budget shift first.")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"\nSaved: {OUT}")