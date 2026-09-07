# Detailed Insights & Findings — Udemy Courses Market Analysis

This document contains the full set of findings, methodology notes, and nuanced observations from the analysis. See `README.md` for a quick overview.

---

## 1. Which Subject Has More Audience Interest / Revenue?

**Method:** Measured with three combined metrics — total subscribers, course count, and average subscribers per course — rather than a single number, since popularity, market supply, and per-course efficiency each tell a different part of the story.

**Findings:**
- **Web Development** leads on all three metrics simultaneously: highest total subscribers, highest course count, *and* highest average subscribers per course. This confirms it is the most in-demand subject, not just the most crowded one.
- For **total revenue**, the ranking is: Web Development ≫ Business Finance > Graphic Design > Musical Instruments.
- **Business Finance vs. Graphic Design:** Business Finance generates more total revenue despite a *lower* average revenue per course than Graphic Design. This is not a contradiction — Business Finance has nearly double the course count (1,191 vs. 602), so higher volume compensates for lower per-course efficiency. `total = avg × count` explains the ranking fully.

**Recommendation:** For a course creator deciding where to launch, Web Development offers the strongest demand signal across every angle. Business Finance and Graphic Design represent different trade-offs — volume-driven vs. efficiency-driven markets.

---

## 2. Does Price Affect Number of Subscribers? (Paid Courses Only)

**Method:** Restricted to paid courses only (`is_paid = True`), since including free courses (price = 0) would conflate "price level" with "free vs. paid" — a separate question already covered in section 3.

**Findings:**
- Pearson correlation: **0.23**
- Spearman correlation (robust to outliers): **0.26**
- Both methods agree: the relationship is weak. Price is **not** a strong driver of subscriber count among paid courses. There is no evidence of a meaningful negative relationship (higher price does not clearly deter subscribers) nor a strong positive one.

**Recommendation:** Other factors (subject, course quality signals, marketing) likely matter more for subscriber count than price positioning alone — pricing strategy should not be assumed to be the primary lever for demand in this market.

---

## 3. Free vs. Paid Courses: Engagement Rate

**Method:** Engagement rate was calculated as **total reviews ÷ total subscribers per group** (not the average of each course's individual engagement rate), because a per-course average is heavily distorted by courses with very few subscribers (e.g., 1 subscriber + 1 review = 100% engagement, despite being statistically meaningless).

**Findings:**
- Paid courses: **5.43%** engagement rate
- Free courses: **3.69%** engagement rate
- Paid courses show ~47% relatively higher engagement than free courses.

**Interpretation:** Learners who paid for a course have a stronger incentive to complete it and leave a review (positive or negative), since they've invested money. Free course sign-ups are more likely to include casual or low-commitment enrollments.

---

## 4. Which Level Achieves More Success?

**Method:** Split explicitly into two perspectives, since "success" means different things to different stakeholders:
- **Business view:** total subscribers, total revenue, course count
- **Learner view:** engagement rate (total reviews ÷ total subscribers)

**Findings:**
- **All Levels** wins on *both* perspectives — highest revenue, highest subscriber count, and highest engagement rate (5.88%).
- Among the specific levels: **Intermediate** (5.26% engagement) outperforms **Expert** (4.65%), which outperforms **Beginner** (3.19%) — even though Beginner has the *second-highest* subscriber volume (4M) after All Levels.
- **Key mismatch:** Beginner-level courses attract large enrollment numbers but have the *lowest* engagement/completion signal of any level. This suggests many beginners sign up (low barrier to entry, curiosity) but a smaller proportion follow through to actually review the course, compared to Intermediate/Expert learners who tend to be more deliberate and committed.

**Recommendation:** High subscriber counts for Beginner content should not be read as a pure success signal — engagement data suggests a gap between initial interest and follow-through at that level.

---

## 5. Does Course Duration Affect Number of Subscribers?

**Method:** Ran on the full dataset (unlike the price analysis, duration is meaningful for both free and paid courses).

**Findings:**
- Correlation: **0.16** — even weaker than the price relationship.
- Beyond the weak correlation, the scatter plot reveals that **the market itself is heavily skewed toward short courses** — the vast majority of courses cluster under 20 hours of content, with very few courses extending beyond 40-50 hours.

**Recommendation:** Course length should not be treated as a meaningful lever for attracting subscribers; the market's natural concentration around shorter formats is a more relevant structural fact than any length-driven demand effect.

---

## 6. Publishing Trend Over Time

**Method:** Grouped by `year_month` (a proper time-ordered period), with the final month **excluded** from the trend chart.

**Why exclude the last month:** The dataset snapshot was taken in the first week of the final month, meaning that month's course count reflects only ~7 days of activity instead of a full month — including it would visually (and misleadingly) suggest a sudden market collapse.

**Findings:**
- The market shows **continuous, accelerating growth** from 2012 through early 2017 — from a handful of courses per month to a peak of ~155 courses/month.
- No sustained decline appears anywhere in the trend; month-to-month dips are followed by continued growth.

---

## 7. Publishing Seasonality

**Method:** Grouped by `month` only (ignoring year), to detect recurring annual patterns independent of the overall growth trend.

**Findings:**
- There is a **mild** seasonal dip in course publishing during the summer months (July–September) compared to the rest of the year.
- Comparing the weakest month in each half of the year (January ≈ 290 vs. September ≈ 240) shows roughly a 17% difference — a real but modest effect, not a dominant pattern in the data.

**Note:** This finding is presented as a supporting observation rather than a standalone dashboard chart, given its comparatively modest effect size relative to the other findings in this analysis.

---

## 8. Top 10 Courses by Revenue

**Method:** Ranked individual courses by estimated revenue (`price × num_subscribers`), using `course_id` as the unique identifier (course titles are not guaranteed unique — see note below).

**Findings:**
- **8 of the top 10** courses by revenue belong to **Web Development**, reinforcing its dominance at the individual course level, not just as a category aggregate.
- One notable exception: **"Pianoforall"** (Musical Instruments) ranks 3rd overall — despite Musical Instruments being the weakest subject category overall across every other metric in this analysis. This shows that a single standout course can compete with top performers even from an otherwise weaker category.

---

## Data Quality Note: Duplicate Course Titles

During data exploration, 9 courses were found to share identical or near-identical titles (e.g., multiple courses titled "Introduction to Web Development"). Investigation confirmed these are **genuinely different courses** — each has a distinct `course_id`, price, subscriber count, and instructor content — most likely created independently by different instructors covering similar topics. This is not a data quality issue.

**Implication:** `course_id` is the correct unique identifier for this dataset. Any course-level grouping or ranking (such as the Top 10 analysis above) must use `course_id`, not `course_title` alone, to avoid incorrectly merging distinct courses that happen to share a name.

---

## Scope Note

An additional analysis was originally planned — a composite "effectiveness score" per subject (combining normalized subscriber count and engagement rate) along with a ranking-validity check (using diff/ECDF/percentile analysis to test whether course rankings are meaningfully distinct or clustered). This was intentionally descoped during development due to unexpected data issues in the normalization step, in favor of keeping the delivered analysis focused and fully validated.
