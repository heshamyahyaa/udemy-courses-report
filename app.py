import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Page configuration must be the first Streamlit command in the script
st.set_page_config(page_title="Udemy Courses Market Analysis", layout="centered")

# ============================================================
# TITLE & INTRODUCTION
# ============================================================
st.title("📊 Udemy Courses Market Analysis")
st.markdown("""
A comprehensive analysis of the Udemy courses market (3,672 courses), viewed from two perspectives:
the business perspective (revenue and reach) and the learner perspective (engagement and satisfaction).
""")

# ============================================================
# DATA LOADING & CLEANING
# ============================================================
df = pd.read_csv('udemy_courses-raw.csv')

# Remove exact duplicate rows found during initial inspection
df = df.drop_duplicates()

# Feature engineering: derived columns used throughout the analysis
df['revenue'] = df['price'] * df['num_subscribers']                     # estimated revenue per course
df['engagement_rate'] = df['num_reviews'] / df['num_subscribers']       # reviews as a % of subscribers

# Convert timestamp string to proper datetime, then extract time components
df['published_timestamp'] = pd.to_datetime(df['published_timestamp'])
df['year'] = df['published_timestamp'].dt.year
df['month'] = df['published_timestamp'].dt.month
df['year_month'] = df['published_timestamp'].dt.tz_localize(None).dt.to_period('M')  # for trend chart ordering

# ============================================================
# TABS LAYOUT
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Subject & Level",
    "Success Drivers",
    "Time Trend",
    "Top Performers"
])

# ------------------------------------------------------------
# TAB 1: OVERVIEW — high-level dataset summary
# ------------------------------------------------------------
with tab1:
    st.subheader("Dataset Overview")

    col1, col2 = st.columns(2)
    col1.metric("Total Courses", df.shape[0])
    col2.metric("Subjects", df['subject'].nunique())

    st.write(f"**Date Range:** {df['published_timestamp'].min().date()} → {df['published_timestamp'].max().date()}")

    st.write("Courses per Subject:")
    st.dataframe(df['subject'].value_counts(), use_container_width=True)
    st.dataframe(df.head(), use_container_width=True)

# ------------------------------------------------------------
# TAB 2: SUBJECT & LEVEL — which category performs best, and by what measure
# ------------------------------------------------------------
with tab2:
    st.subheader("Which Subject Has More Audience Interest?")

    subject_result = df.groupby('subject').agg(
        total_subscribers=('num_subscribers', 'sum'),
        course_count=('course_id', 'count'),
        avg_subscribers_per_course=('num_subscribers', 'mean')
    ).sort_values('total_subscribers', ascending=False)

    fig1, axes1 = plt.subplots(3, 1, figsize=(8, 10))
    sns.barplot(x=subject_result['total_subscribers'], y=subject_result.index, hue=subject_result.index, palette='viridis', legend=False, ax=axes1[0])
    axes1[0].set_title('Total Subscribers', fontsize=12)
    sns.barplot(x=subject_result['course_count'], y=subject_result.index, hue=subject_result.index, palette='viridis', legend=False, ax=axes1[1])
    axes1[1].set_title('Course Count', fontsize=12)
    sns.barplot(x=subject_result['avg_subscribers_per_course'], y=subject_result.index, hue=subject_result.index, palette='viridis', legend=False, ax=axes1[2])
    axes1[2].set_title('Avg Subscribers per Course', fontsize=12)
    plt.tight_layout()
    st.pyplot(fig1)

    st.info("💡 **Insight:** Web Development leads on all three metrics — total subscribers, course count, and even average subscribers per course — confirming it's the most in-demand subject, not just the most crowded.")

    st.subheader("Which Subject Brings the Most Revenue?")
    revenue_by_subject = df.groupby('subject')['revenue'].sum().sort_values(ascending=False)
    st.bar_chart(revenue_by_subject, use_container_width=True, height=400)

    st.info("💡 **Insight:** Business Finance generates more total revenue than Graphic Design despite a lower average revenue per course — because it has nearly double the course count. Volume compensates for lower per-course efficiency.")

    st.subheader("Which Level Achieves More Success?")

    level_business = df.groupby('level').agg(
        total_subscribers=('num_subscribers', 'sum'),
        total_revenue=('revenue', 'sum'),
        course_count=('course_id', 'count')
    ).sort_values('total_revenue', ascending=False)

    level_learner = df.groupby('level').apply(
        lambda g: g['num_reviews'].sum() / g['num_subscribers'].sum() * 100
    ).sort_values(ascending=False)

    fig2, axes2 = plt.subplots(1, 2, figsize=(10, 4))
    sns.barplot(x=level_business['total_revenue'], y=level_business.index, hue=level_business.index, palette='viridis', legend=False, ax=axes2[0])
    axes2[0].set_title('Total Revenue by Level (Business View)', fontsize=11)

    sns.barplot(x=level_learner.values, y=level_learner.index, hue=level_learner.index, palette='viridis', legend=False, ax=axes2[1])
    axes2[1].set_title('Engagement Rate by Level (Learner View)', fontsize=11)
    axes2[1].set_xlabel('Engagement Rate (%)')

    plt.tight_layout()
    st.pyplot(fig2)

    st.info("💡 **Insight:** 'All Levels' wins on both business and learner metrics. However, notice the mismatch for Beginner courses: second-highest subscriber volume, yet the *lowest* engagement rate — suggesting many beginners sign up but fewer follow through, unlike Intermediate/Expert learners who engage more relative to their volume.")

# ------------------------------------------------------------
# TAB 3: SUCCESS DRIVERS — what factors actually affect subscriber count
# ------------------------------------------------------------
with tab3:
    st.subheader("Does Price Affect Number of Subscribers? (Paid Courses Only)")

    paid_df = df[df['is_paid']]
    price_corr = paid_df['price'].corr(paid_df['num_subscribers'])
    st.write(f"Correlation (Price vs Subscribers): **{price_corr:.2f}**")

    fig3, ax3 = plt.subplots(figsize=(7, 4))
    sns.scatterplot(data=paid_df, x='price', y='num_subscribers', alpha=0.4, ax=ax3)
    ax3.set_title('Price vs Num Subscribers (Paid Courses)')
    st.pyplot(fig3)

    st.info("💡 **Insight:** Correlation is weak (~0.23-0.26 across Pearson and Spearman methods) — price is not a strong driver of subscriber count among paid courses.")

    st.subheader("Free vs Paid Courses: Engagement Rate")

    engagement_by_paid = df.groupby('is_paid').apply(
        lambda g: g['num_reviews'].sum() / g['num_subscribers'].sum() * 100
    )

    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.barplot(x=engagement_by_paid.index.astype(str), y=engagement_by_paid.values,
                hue=engagement_by_paid.index.astype(str), palette='viridis', legend=False, ax=ax4)
    ax4.set_title('Engagement Rate: Free vs Paid Courses')
    ax4.set_xlabel('Is Paid')
    ax4.set_ylabel('Engagement Rate (%)')
    st.pyplot(fig4)

    st.info("💡 **Insight:** Paid courses show higher engagement (5.43%) than free courses (3.69%) — learners who paid have more incentive to complete and review the course.")

    st.subheader("Does Course Duration Affect Number of Subscribers?")

    duration_corr = df['content_duration'].corr(df['num_subscribers'])
    st.write(f"Correlation (Duration vs Subscribers): **{duration_corr:.2f}**")

    fig5, ax5 = plt.subplots(figsize=(7, 4))
    sns.scatterplot(data=df, x='content_duration', y='num_subscribers', alpha=0.4, ax=ax5)
    ax5.set_title('Content Duration vs Num Subscribers')
    st.pyplot(fig5)

    st.caption("Note: Most courses in the market are clustered at short durations (under 20 hours), which limits the visibility of any relationship at higher durations.")
    st.info("💡 **Insight:** Correlation is very weak (~0.16) — course duration has little to no effect on subscriber count.")

# ------------------------------------------------------------
# TAB 4: TIME TREND — how the market evolved over time
# ------------------------------------------------------------
with tab4:
    st.subheader("Number of Courses Published Over Time")

    trend = df.groupby('year_month').size()
    trend_clean = trend[:-1]  # exclude the last month: only partially covered by the data snapshot

    fig6, ax6 = plt.subplots(figsize=(9, 4))
    trend_clean.plot(kind='line', marker='o', ax=ax6)
    ax6.set_title('Number of Courses Published Over Time (Excluding Incomplete Last Month)')
    ax6.set_xlabel('Year-Month')
    ax6.set_ylabel('Number of Courses')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig6)

    st.info("💡 **Insight:** The market shows continuous, accelerating growth from 2012 through early 2017, with no sustained decline at any point. The last data point is excluded because it only covers the first week of that month.")

    st.subheader("Publishing Seasonality (by Month, All Years Combined)")

    seasonality = df.groupby('month').size()

    fig7, ax7 = plt.subplots(figsize=(8, 4))
    sns.barplot(x=seasonality.index, y=seasonality.values, hue=seasonality.index, palette='viridis', legend=False, ax=ax7)
    ax7.set_title('Course Publishing Seasonality')
    ax7.set_xlabel('Month')
    ax7.set_ylabel('Number of Courses')
    st.pyplot(fig7)

    st.caption("Note: There is a mild seasonal dip in publishing activity during summer months (Jul-Sep) compared to the rest of the year.")

# ------------------------------------------------------------
# TAB 5: TOP PERFORMERS — individual course-level ranking
# ------------------------------------------------------------
with tab5:
    st.subheader("Top 10 Courses by Revenue")

    top10_revenue = df[['course_id', 'course_title', 'subject', 'revenue']].sort_values('revenue', ascending=False).head(10)
    st.dataframe(top10_revenue, use_container_width=True)

    fig8, ax8 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top10_revenue, x='revenue', y='course_title', hue='subject', dodge=False, palette='viridis', ax=ax8)
    ax8.set_title('Top 10 Courses by Revenue')
    ax8.set_xlabel('Revenue')
    ax8.set_ylabel('')
    plt.tight_layout()
    st.pyplot(fig8)

    st.info("💡 **Insight:** 8 of the top 10 courses by revenue belong to Web Development — reinforcing its dominance at the individual-course level, not just as a category. The one exception, *Pianoforall* (Musical Instruments), shows that a single standout course can compete with top performers even from an overall weaker subject.")