import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Netflix Business Intelligence Dashboard",
    page_icon="🎬",
    layout="wide"
)


# -------------------------------------------------
# CUSTOM UI
# -------------------------------------------------

st.markdown(
"""
<style>

.stApp {
    background-color:#0f0f0f;
    color:white;
}


h1 {
    color:#E50914;
    text-align:center;
}


h2,h3 {
    color:white;
}


[data-testid="stMetric"] {

    background:#181818;
    padding:20px;
    border-radius:15px;
    border:1px solid #333;

}


[data-testid="stMetricValue"] {

    color:#E50914;

}


</style>
""",
unsafe_allow_html=True
)



# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "netflix_titles.csv"
    )


    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ","_")
    )


    # Date processing

    if "date_added" in df.columns:

        df["date_added"] = pd.to_datetime(
            df["date_added"],
            errors="coerce"
        )

        df["month_added"] = (
            df["date_added"]
            .dt.month_name()
        )


    return df



df = load_data()



# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title(
    "🎬 Netflix Business Intelligence Dashboard"
)


st.write(
"""
A strategic analytics dashboard designed to help
business leaders understand content investment,
customer preferences, and global opportunities.
"""
)



# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.header(
    "🎛 Filters"
)


content_type = st.sidebar.multiselect(

    "Content Type",

    df["type"].unique(),

    default=df["type"].unique()

)



filtered = df[
    df["type"].isin(content_type)
]



# -------------------------------------------------
# EXECUTIVE KPI
# -------------------------------------------------

st.subheader(
    "📊 Executive Overview"
)


col1,col2,col3,col4 = st.columns(4)



col1.metric(
    "Total Content",
    f"{len(filtered):,}"
)


col2.metric(
    "Movies",
    f"{len(filtered[filtered.type=='Movie']):,}"
)


col3.metric(
    "TV Shows",
    f"{len(filtered[filtered.type=='TV Show']):,}"
)


col4.metric(
    "Countries",
    filtered.country.nunique()
)



st.divider()



# -------------------------------------------------
# CONTENT STRATEGY
# -------------------------------------------------

st.subheader(
    "🎥 Content Portfolio Strategy"
)


col1,col2 = st.columns(2)



# Movies vs Shows

with col1:


    content = filtered["type"].value_counts()


    fig = px.pie(

        values=content.values,

        names=content.index,

        hole=.5,

        color_discrete_sequence=[
            "#E50914",
            "#444444"
        ],

        title="Movies vs TV Shows"

    )


    fig.update_layout(
        template="plotly_dark"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# Rating

with col2:


    if "rating" in filtered.columns:


        ratings = (
            filtered.rating
            .value_counts()
            .head(10)
        )


        fig = px.bar(

            x=ratings.index,

            y=ratings.values,

            color=ratings.values,

            color_continuous_scale="reds",

            title="Audience Rating Distribution"

        )


        fig.update_layout(
            template="plotly_dark"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



# -------------------------------------------------
# CONTENT GROWTH
# -------------------------------------------------

st.subheader(
    "📈 Content Growth Trend"
)


growth = (
    filtered.release_year
    .value_counts()
    .sort_index()
)



fig = px.line(

    x=growth.index,

    y=growth.values,

    markers=True,

    title="Netflix Content Added Over Time"

)


fig.update_traces(
    line_color="#E50914"
)


fig.update_layout(
    template="plotly_dark"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# -------------------------------------------------
# GENRE ANALYSIS
# -------------------------------------------------

st.subheader(
    "🎭 Popular Genres"
)


genres = (

    filtered.listed_in
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)

)



fig = px.bar(

    x=genres.values,

    y=genres.index,

    orientation="h",

    color=genres.values,

    color_continuous_scale="purples",

    title="Most Popular Content Categories"

)



fig.update_layout(
    template="plotly_dark"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# -------------------------------------------------
# GLOBAL MARKET ANALYSIS
# -------------------------------------------------

st.subheader(
    "🌎 Global Market Opportunity"
)


countries = (

    filtered.country
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)

)



fig = px.bar(

    x=countries.values,

    y=countries.index,

    orientation="h",

    color=countries.values,

    color_continuous_scale="blues",

    title="Top Content Producing Countries"

)



fig.update_layout(
    template="plotly_dark"
)



st.plotly_chart(
    fig,
    use_container_width=True
)



# -------------------------------------------------
# RELEASE SEASONALITY
# -------------------------------------------------

if "month_added" in filtered.columns:


    st.subheader(
        "📅 Best Release Months"
    )


    months = (

        filtered.month_added
        .value_counts()

    )


    fig = px.bar(

        x=months.index,

        y=months.values,

        color=months.values,

        color_continuous_scale="greens"

    )


    fig.update_layout(
        template="plotly_dark"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# -------------------------------------------------
# CONTENT AGE ANALYSIS
# -------------------------------------------------

st.subheader(
    "⏳ Content Freshness Analysis"
)


current_year = 2026


filtered["content_age"] = (

    current_year -

    filtered.release_year

)



fig = px.histogram(

    filtered,

    x="content_age",

    nbins=20,

    title="Age of Netflix Content"

)



fig.update_layout(
    template="plotly_dark"
)



st.plotly_chart(
    fig,
    use_container_width=True
)



# -------------------------------------------------
# BUSINESS INSIGHTS
# -------------------------------------------------

st.subheader(
    "💡 Business Recommendations"
)


st.info(
"""
Based on the dashboard:

• Invest in high-performing genres with strong audience demand.

• Expand international content markets with high production volume.

• Balance movies and TV shows according to customer engagement.

• Prioritize newer content to maintain subscriber interest.

• Use seasonal release patterns to maximize marketing impact.
"""
)



# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.success(
"Built with Python | Pandas | Plotly | Streamlit 🚀"
)
