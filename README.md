# 📊 Udemy Courses Market Analysis

A data analysis project exploring the Udemy courses market (3,672 courses) using Python (Pandas, NumPy, Matplotlib, Seaborn), presented as a Streamlit report.

The analysis is framed as a business-style investigation: what drives success in this market, from both the **platform/instructor perspective** (revenue, reach) and the **learner perspective** (engagement, satisfaction).

## 🔗 Live Report
[View the live report](#) <!-- استبدل الـ # برابط streamlit.app بتاعك بعد الـ deploy -->

## 📁 Project Structure
```
├── app.py                      # Streamlit report (main file)
├── udemy_courses-raw.csv       # Raw dataset
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── INSIGHTS.md                 # Full detailed findings and analysis notes
```

## 🧹 What Was Done
- **Data Cleaning:** removed duplicate rows, converted timestamps to proper datetime, engineered `revenue` and `engagement_rate` columns, extracted year/month for time-based analysis
- **Exploratory Analysis:** subject and course-level popularity vs. revenue, pricing effects, free vs. paid engagement, course level effectiveness, course duration effects, publishing trend and seasonality
- **Ranking:** identified the top 10 highest-revenue courses individually (not just by category)

## 🔑 Key Highlights
- **Web Development** dominates the market — highest total subscribers, course count, and revenue, and 8 of the top 10 individual courses by revenue
- **Price** and **course duration** have only a weak relationship with subscriber count (correlation ≈ 0.2 and ≈ 0.16 respectively)
- **Paid courses** show noticeably higher engagement (5.43%) than **free courses** (3.69%)
- The market has grown continuously since 2012, with a mild seasonal dip in publishing activity during summer months

Full details, methodology notes, and nuanced findings are in [`INSIGHTS.md`](./INSIGHTS.md).

## ⚙️ How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🛠️ Tools Used
Python · Pandas · NumPy · Matplotlib · Seaborn · Streamlit

## 📌 Note
This is a static analytical report built with Streamlit's layout features (tabs), not a fully interactive dashboard with live filters — it was designed to present a complete, structured analytical narrative rather than an ad-hoc exploration tool.
