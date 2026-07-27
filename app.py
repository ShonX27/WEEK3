import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM NETFLIX STYLE UI
# --------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0f0f0f;
        color: white;
    }


    h1 {
        color: #E50914;
        text-align:center;
        font-size:45px;
    }


    h2, h3 {
        color:white;
    }


    [data-testid="stMetric"] {

        background-color:#181818;
        padding:20px;
        border-radius:15px;
        border:1px solid #333;

    }


    [data-testid="stMetricValue"] {

        color:#E50914;

    }


    section[data-testid="stSidebar"] {

        background-color:#141414;

    }


    .block-container {

        padding-top:2rem;

    }

    </style>
    """,
    unsafe_allow_html=True
)



# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

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

    return df



df = load_data()



# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title(
    "🎬 Netflix Movies & TV Shows Analytics Dashboard"
)


st.markdown(
"""
Explore Netflix's global content library through
interactive business intelligence visualizations.

**Dashboard Insights**
- Content distribution
- Audience ratings
- Global production trends
- Genre popularity
- Release growth
"""
)



# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title(
    "🎛 Filters"
)


type_filter = st.sidebar.multiselect(
    "Content Type",
    df["type"].dropna().unique(),
    default=df["type"].dropna().unique()
)



if "rating" in df.columns:

    rating_filter = st.sidebar.multiselect(
        "Rating",
        df["rating"].dropna().unique(),
        default=df["rating"].dropna().unique()
    )

else:

    rating_filter = []



filtered_df = df[
    df["type"].isin(type_filter)
]



if rating_filter:

    filtered_df = filtered_df[
        filtered_df["rating"].isin(rating_filter)
    ]



# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.subheader(
    "📊 Netflix Overview"
)


col1,col2,col3,col4 = st.columns(4)


with col1:

    st.metric(
        "Total Titles",
        f"{len(filtered_df):,}"
    )


with col2:

    movies = len(
        filtered_df[
            filtered_df["type"]=="Movie"
        ]
    )

    st.metric(
        "Movies",
        f"{movies:,}"
    )


with col3:

    shows = len(
        filtered_df[
            filtered_df["type"]=="TV Show"
        ]
    )

    st.metric(
        "TV Shows",
        f"{shows:,}"
    )


with col4:

    latest = filtered_df["release_year"].max()

    st.metric(
        "Latest Release",
        latest
    )



st.divider()



# --------------------------------------------------
# MOVIE VS TV SHOW
# --------------------------------------------------

col1,col2 = st.columns(2)



with col1:

    st.subheader(
        "🎥 Movies vs TV Shows"
    )


    type_count = (
        filtered_df["type"]
        .value_counts()
    )


    fig = px.pie(

        values=type_count.values,
        names=type_count.index,
        hole=0.45,

        color_discrete_sequence=[
            "#E50914",
            "#555555"
        ]

    )


    fig.update_layout(
        template="plotly_dark",
        height=400
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# --------------------------------------------------
# RATINGS
# --------------------------------------------------

with col2:

    st.subheader(
        "⭐ Content Ratings"
    )


    if "rating" in filtered_df.columns:


        ratings = (
            filtered_df["rating"]
            .value_counts()
            .head(10)
        )


        fig = px.bar(

            x=ratings.index,
            y=ratings.values,

            color=ratings.values,

            color_continuous_scale="reds"

        )


        fig.update_layout(

            template="plotly_dark",

            height=400,

            xaxis_title="Rating",

            yaxis_title="Titles",

            showlegend=False

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



# --------------------------------------------------
# RELEASE TREND
# --------------------------------------------------

st.subheader(
    "📈 Netflix Growth Over Time"
)



release = (

    filtered_df["release_year"]
    .value_counts()
    .sort_index()

)



fig = px.line(

    x=release.index,

    y=release.values,

    markers=True

)


fig.update_traces(

    line_color="#E50914",

    line_width=4

)


fig.update_layout(

    template="plotly_dark",

    height=450,

    xaxis_title="Year",

    yaxis_title="Number of Titles"

)



st.plotly_chart(
    fig,
    use_container_width=True
)



# --------------------------------------------------
# COUNTRIES
# --------------------------------------------------

st.subheader(
    "🌎 Top Netflix Producing Countries"
)



countries = (

    filtered_df["country"]
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

    color_continuous_scale="blues"

)


fig.update_layout(

    template="plotly_dark",

    height=500,

    xaxis_title="Titles",

    yaxis_title="Country"

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# --------------------------------------------------
# GENRES
# --------------------------------------------------

st.subheader(
    "🎭 Most Popular Genres"
)



genres = (

    filtered_df["listed_in"]

    .dropna()

    .str.split(", ")

    .explode()

    .value_counts()

    .head(10)

)



fig = px.bar(

    x=genres.index,

    y=genres.values,

    color=genres.values,

    color_continuous_scale="purples"

)



fig.update_layout(

    template="plotly_dark",

    height=450,

    xaxis_tickangle=-45,

    showlegend=False

)



st.plotly_chart(

    fig,

    use_container_width=True

)



# --------------------------------------------------
# DURATION
# --------------------------------------------------

if "duration" in filtered_df.columns:


    st.subheader(
        "⏱ Content Duration"
    )


    duration = (

        filtered_df["duration"]

        .dropna()

        .value_counts()

        .head(10)

    )



    fig = px.bar(

        x=duration.index,

        y=duration.values,

        color=duration.values,

        color_continuous_scale="greens"

    )



    fig.update_layout(

        template="plotly_dark",

        height=400

    )



    st.plotly_chart(

        fig,

        use_container_width=True

    )



# --------------------------------------------------
# SEARCH
# --------------------------------------------------

st.subheader(
    "🔎 Search Netflix Titles"
)



search = st.text_input(
    "Search a movie or TV show"
)



if search:


    result = filtered_df[

        filtered_df["title"]

        .str.contains(

            search,

            case=False,

            na=False

        )

    ]


    st.dataframe(

        result,

        use_container_width=True

    )



# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.success(
    "Built with Python | Pandas | Plotly | Streamlit 🚀"
)
