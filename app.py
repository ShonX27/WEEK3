import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# Netflix Theme Styling
# --------------------------------------------------

st.markdown(
"""
<style>

body {
background-color:#0e1117;
}

.main {
background-color:#0e1117;
}

h1 {
color:#E50914;
text-align:center;
}

h2,h3 {
color:white;
}

[data-testid="metric-container"] {
background-color:#181818;
padding:15px;
border-radius:15px;
box-shadow:0px 4px 10px black;
}

[data-testid="metric-container"] label {
color:#aaaaaa;
}

[data-testid="metric-container"] div {
color:white;
}

</style>
""",
unsafe_allow_html=True
)



# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("netflix_titles.csv")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ","_")
    )


    df["date_added"] = pd.to_datetime(
        df["date_added"],
        errors="coerce"
    )


    df["year_added"] = (
        df["date_added"]
        .dt.year
    )


    return df



df = load_data()



# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🎬 Netflix Business Analytics Dashboard")


st.write(
"""
Analyze Netflix's content strategy, customer preferences,
and global production trends.
"""
)



# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("🎛 Dashboard Filters")



# Content Type

type_filter = st.sidebar.multiselect(
    "Content Type",
    df.type.unique(),
    default=df.type.unique()
)



# Year

year_range = st.sidebar.slider(
    "Release Year",
    int(df.release_year.min()),
    int(df.release_year.max()),
    (
        int(df.release_year.min()),
        int(df.release_year.max())
    )
)



# Rating

rating_filter = st.sidebar.multiselect(
    "Rating",
    sorted(df.rating.dropna().unique())
)



# Country

country_list = (
    df.country
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(50)
    .index
)


country_filter = st.sidebar.multiselect(
    "Country",
    country_list
)



# Genre

genre_list = (
    df.listed_in
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .index
)


genre_filter = st.sidebar.multiselect(
    "Genre",
    genre_list
)



# Director Search

director = st.sidebar.text_input(
    "Director Search"
)



# Apply Filters

filtered = df[
    (df.type.isin(type_filter)) &
    (df.release_year.between(
        year_range[0],
        year_range[1]
    ))
]



if rating_filter:
    filtered = filtered[
        filtered.rating.isin(rating_filter)
    ]



if country_filter:

    filtered = filtered[
        filtered.country.fillna("")
        .apply(
            lambda x:
            any(c in x for c in country_filter)
        )
    ]



if genre_filter:

    filtered = filtered[
        filtered.listed_in.fillna("")
        .apply(
            lambda x:
            any(g in x for g in genre_filter)
        )
    ]



if director:

    filtered = filtered[
        filtered.director
        .fillna("")
        .str.contains(
            director,
            case=False
        )
    ]



# --------------------------------------------------
# KPI Dashboard
# --------------------------------------------------

st.subheader("📊 Netflix Overview")


c1,c2,c3,c4,c5 = st.columns(5)



c1.metric(
"Total Titles",
len(filtered)
)


c2.metric(
"Movies",
len(filtered[filtered.type=="Movie"])
)


c3.metric(
"TV Shows",
len(filtered[filtered.type=="TV Show"])
)


c4.metric(
"Top Year",
filtered.release_year.mode()[0]
)


c5.metric(
"Top Genre",
filtered.listed_in.mode()[0].split(",")[0]
)



st.divider()



# --------------------------------------------------
# Charts
# --------------------------------------------------

col1,col2,col3 = st.columns(3)



# Movie TV

with col1:

    data = filtered.type.value_counts()

    fig = px.pie(
        values=data.values,
        names=data.index,
        hole=.5,
        title="Movie vs TV Show"
    )

    fig.update_layout(
        height=300
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



# Ratings

with col2:

    ratings = (
        filtered.rating
        .value_counts()
        .head(8)
    )


    fig = px.bar(
        ratings,
        x=ratings.index,
        y=ratings.values,
        title="Top Ratings"
    )


    fig.update_layout(
        height=300,
        xaxis_title="",
        yaxis_title=""
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# Release trend

with col3:

    trend = (
        filtered.release_year
        .value_counts()
        .sort_index()
    )


    fig = px.line(
        trend,
        x=trend.index,
        y=trend.values,
        title="Content Growth"
    )


    fig.update_layout(
        height=300
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# --------------------------------------------------
# Business Insights Row
# --------------------------------------------------

col1,col2 = st.columns(2)



with col1:

    countries = (
        filtered.country
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
        .head(10)
    )


    fig = px.bar(
        countries,
        orientation="h",
        title="Top Producing Countries"
    )


    fig.update_layout(
        height=350
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )




with col2:


    genres = (
        filtered.listed_in
        .dropna()
        .str.split(", ")
        .explode()
        .value_counts()
        .head(10)
    )


    fig = px.bar(
        genres,
        title="Most Popular Genres"
    )


    fig.update_layout(
        height=350,
        xaxis_tickangle=-45
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# --------------------------------------------------
# Content Added Analysis
# --------------------------------------------------

st.subheader(
"📅 Netflix Content Added Over Time"
)



added = (
    filtered.year_added
    .value_counts()
    .sort_index()
)



fig = px.area(
    added,
    x=added.index,
    y=added.values
)


fig.update_layout(
    height=350
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# --------------------------------------------------
# Search
# --------------------------------------------------

st.subheader(
"🔎 Search Netflix Titles"
)


search = st.text_input(
"Search movie or show"
)


if search:

    result = filtered[
        filtered.title
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]


    st.dataframe(
        result[
            [
            "title",
            "type",
            "release_year",
            "country",
            "rating",
            "listed_in"
            ]
        ],
        use_container_width=True
    )



st.success(
"Netflix Dashboard | Python + Pandas + Plotly + Streamlit 🚀"
)
