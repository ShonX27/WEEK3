import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide"
)


# --------------------------------------------------
# Custom Styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        background-color: #fafafa;
    }

    h1 {
        text-align: center;
    }

    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
        text-align:center;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# --------------------------------------------------
# Load Data
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
# Header
# --------------------------------------------------

st.title("🎬 Netflix Content Analytics Dashboard")

st.markdown(
"""
Explore Netflix's movies and TV shows using interactive
data visualization.

**Dataset Analysis Includes:**
- Content distribution
- Release trends
- Countries
- Genres
- Ratings
- Search analytics
"""
)



# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("🎛 Dashboard Filters")


type_filter = st.sidebar.multiselect(
    "Content Type",
    df["type"].unique(),
    default=df["type"].unique()
)



if "rating" in df.columns:

    rating_filter = st.sidebar.multiselect(
        "Rating",
        df["rating"]
        .dropna()
        .unique(),
        default=df["rating"]
        .dropna()
        .unique()
    )


else:

    rating_filter = []



filtered_df = df[
    df["type"].isin(type_filter)
]


if rating_filter:

    filtered_df = filtered_df[
        filtered_df["rating"]
        .isin(rating_filter)
    ]



# --------------------------------------------------
# KPI Section
# --------------------------------------------------

st.subheader("📊 Netflix Overview")


col1,col2,col3,col4 = st.columns(4)


with col1:
    st.metric(
        "Total Titles",
        len(filtered_df)
    )


with col2:

    movies = len(
        filtered_df[
            filtered_df["type"]
            =="Movie"
        ]
    )

    st.metric(
        "Movies",
        movies
    )


with col3:

    shows = len(
        filtered_df[
            filtered_df["type"]
            =="TV Show"
        ]
    )

    st.metric(
        "TV Shows",
        shows
    )


with col4:

    years = filtered_df["release_year"].max()

    st.metric(
        "Latest Release",
        years
    )



st.divider()



# --------------------------------------------------
# Content Distribution
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


    fig,ax = plt.subplots()

    ax.pie(
        type_count,
        labels=type_count.index,
        autopct="%1.1f%%"
    )

    st.pyplot(fig)



with col2:

    st.subheader(
        "⭐ Ratings Distribution"
    )


    if "rating" in filtered_df.columns:

        rating_count = (
            filtered_df["rating"]
            .value_counts()
            .head(10)
        )


        fig,ax = plt.subplots()

        ax.bar(
            rating_count.index,
            rating_count.values
        )

        plt.xticks(
            rotation=45
        )

        st.pyplot(fig)



# --------------------------------------------------
# Release Trend
# --------------------------------------------------

st.subheader(
    "📈 Netflix Growth Over Years"
)


release = (
    filtered_df
    ["release_year"]
    .value_counts()
    .sort_index()
)


fig,ax = plt.subplots()

ax.plot(
    release.index,
    release.values
)


ax.set_xlabel(
    "Year"
)

ax.set_ylabel(
    "Number of Titles"
)


st.pyplot(fig)



# --------------------------------------------------
# Geography Analysis
# --------------------------------------------------

st.subheader(
    "🌎 Top Producing Countries"
)


countries = (

    filtered_df
    ["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)

)



fig,ax = plt.subplots()

ax.barh(
    countries.index,
    countries.values
)


ax.set_xlabel(
    "Titles"
)


st.pyplot(fig)



# --------------------------------------------------
# Genre Analysis
# --------------------------------------------------

st.subheader(
    "🎭 Most Popular Genres"
)


genres = (

    filtered_df
    ["listed_in"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)

)



fig,ax = plt.subplots()

ax.bar(
    genres.index,
    genres.values
)


plt.xticks(
    rotation=45,
    ha="right"
)


st.pyplot(fig)



# --------------------------------------------------
# Duration Analysis
# --------------------------------------------------

if "duration" in filtered_df.columns:

    st.subheader(
        "⏱ Content Duration"
    )


    duration = (
        filtered_df
        ["duration"]
        .dropna()
        .value_counts()
        .head(10)
    )


    fig,ax = plt.subplots()


    ax.bar(
        duration.index,
        duration.values
    )


    plt.xticks(
        rotation=45
    )


    st.pyplot(fig)



# --------------------------------------------------
# Search Tool
# --------------------------------------------------

st.subheader(
    "🔎 Search Netflix Library"
)


search = st.text_input(
    "Search title"
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
        result[
            [
            "title",
            "type",
            "release_year",
            "country",
            "rating"
            ]
        ],
        use_container_width=True
    )



# --------------------------------------------------
# Footer
# --------------------------------------------------

st.success(
    "Built with Python | Pandas | Matplotlib | Streamlit 🚀"
)
