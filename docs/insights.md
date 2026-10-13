# Ad Spend Leakage Audit: Insights and Recommendations

## 1. Project Overview

This analysis uses the Kaggle Sales Conversion Optimization dataset, which contains 1,143 advertisements across three campaigns: 916, 936, and 1178.

The objective is to identify audience segments that consume advertising budgets without generating enough approved sales and recommend ways to improve campaign efficiency.

The analysis uses Approved_Conversion as the sales measure. Since the dataset does not contain revenue data, performance is evaluated using cost per sale rather than return on ad spend (ROAS).

## 2. Key Findings

### 2.1 Overall Advertising Performance

Total advertising expenditure was 58,705.23, resulting in 1,079 approved sales. The average cost per sale was 54.41.

This provides a baseline for comparing the efficiency of different audience segments.

### 2.2 Audience Segments With Potential Budget Leakage

Four audience segments (women aged 45–49, women aged 40–44, men aged 45–49, and women aged 35–39) accounted for 58.3% of total advertising spend but generated only 36.7% of approved sales.

This suggests that these segments may be receiving more budget than their current sales performance justifies.

### 2.3 Largest Potential Source of Inefficiency

Women aged 45–49 accounted for 13,433.21 in advertising expenditure, representing 22.9% of total spend. However, this segment generated only 112 approved sales, or 10.4% of all sales.

The cost per sale was 119.94, approximately 2.2 times the overall average of 54.41.

This audience segment should be investigated first to determine whether its advertising spend can be used more effectively.

### 2.4 Better-Performing Audience Segments

Men aged 30–34, women aged 30–34, and men aged 35–39 together accounted for 34.6% of advertising expenditure while generating 56.2% of approved sales.

Men aged 30–34 performed particularly well, with a cost per sale of 25.55.

These segments are potential candidates for a controlled budget increase, subject to further testing.

### 2.5 Advertisements With No Approved Sales

Out of 1,143 advertisements, 559 generated no approved sales. These ads consumed 14,754.42, equivalent to 25.1% of total advertising spend.

Despite producing no approved sales, these advertisements generated 769 enquiries. This indicates that some prospects showed interest but did not progress to an approved conversion.

Further investigation is needed to identify whether the issue relates to lead quality, follow-up, the offer, or the approval process.

### 2.6 Conversion Funnel

The campaign generated 38,165 clicks, followed by 3,264 enquiries and 1,079 approved sales.

About 8.6% of clicks became enquiries, and 33.1% of enquiries became approved sales.

The click-through rate (CTR) is 0.018% (38,165 clicks / 213,434,828 impressions).

## 3. Recommendations

### 3.1 Test a Small Budget Reallocation

Initially, reallocate 10% of the budget assigned to the four weaker audience segments. This represents approximately 3,421, or 5.8% of total advertising spend.

Test this allocation across men aged 30–34, women aged 30–34, and men aged 35–39.

Compare cost per sale and approved sales before and after the change, while keeping the overall budget unchanged.

### 3.2 Investigate High-Spending Ads With No Sales

Review advertisements with the highest spend and zero approved sales, starting with women aged 45–49 in campaign 1178.

Determine whether these ads should be paused, modified, or tested with different creative content or offers.

### 3.3 Improve Enquiry-to-Sale Conversion

Investigate why enquiries are not becoming approved sales, particularly in the weaker-performing audience segments.

Review lead quality, response times, follow-up procedures, offer suitability, and sales approval criteria.

### 3.4 Scale Gradually

If the initial budget reallocation improves performance, consider increasing the shift to 20%.

Avoid making large changes immediately because increased spending may produce diminishing returns.

## 4. Budget Reallocation: What-If Analysis

The following scenarios estimate potential additional sales while keeping the total advertising budget unchanged.

| Budget shift | Cautious (extra money works 50% worse) | Optimistic (same efficiency as now) |
|---|---|---|
| 10% | +28.5 sales (+2.6%) | +62.5 sales (+5.8%) |
| 20% | +56.9 sales (+5.3%) | +125.0 sales (+11.6%) |
| 30% | +85.4 sales (+7.9%) | +187.5 sales (+17.4%) |

- **Optimistic:** the extra budget performs as well as each segment performs today.
- **Cautious:** the extra budget performs 50% worse, because ad performance usually drops as spend rises.

The cautious estimates should guide initial planning because additional advertising spend does not always maintain the same efficiency.

These values are projections, not guaranteed results. Actual performance should be measured through a controlled experiment before implementing larger budget changes.

## 5. Limitations

- **No revenue data:** The dataset does not include revenue, so ROAS and profitability cannot be calculated without additional assumptions.
- **Correlation does not prove causation:** Differences in performance may be associated with campaign strategy, creative content, audience characteristics, or other factors rather than age or gender alone.
- **Campaign concentration:** Campaign 1178 accounts for 94.8% of total spend, so the findings largely reflect this campaign.
- **Results may differ in practice:** The optimistic case assumes constant efficiency and the cautious case assumes 50% worse. Real results could fall outside this range, so test first.
- **Need for validation:** The proposed changes should be tested on a small scale before being implemented more broadly.

## 6. Conclusion

The analysis identified substantial differences in advertising efficiency across audience segments. Some segments consumed a large share of the budget while generating a relatively small share of approved sales, whereas other segments achieved sales at a lower cost.

The recommended next steps are to test a small budget reallocation, investigate high-spending advertisements with no approved sales, and identify opportunities to improve enquiry-to-sale conversion.

These actions could improve advertising efficiency without increasing the overall budget. The results should be validated through further testing before making major campaign decisions.