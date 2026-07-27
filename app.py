import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df


df = load_data()

st.write(df.columns.tolist())


# -----------------------------
# Title
# -----------------------------
st.title("🎬 Netflix Movies & TV Shows Dashboard")

st.write(
    """
    Interactive dashboard analyzing Netflix content using data visualization.
    Explore movies, TV shows, countries, ratings, and release trends.
    """
)


# -----------------------------
# Dataset Preview
# -----------------------------
with st.expander("View Dataset"):
    st.dataframe(df.head(20))


# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

type_filter = st.sidebar.multiselect(
    "Select Content Type",
    options=df["type"].unique(),
    default=df["type"].unique()
)


rating_filter = st.sidebar.multiselect(
    "Select Rating",
    options=df["rating"].dropna().unique(),
    default=df["rating"].dropna().unique()[:10]
)


filtered_df = df[
    (df["type"].isin(type_filter)) &
    (df["rating"].isin(rating_filter))
]


# -----------------------------
# Key Metrics
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Titles",
        len(filtered_df)
    )

with col2:
    movies = len(
        filtered_df[filtered_df["type"] == "Movie"]
    )
    st.metric(
        "Movies",
        movies
    )

with col3:
    shows = len(
        filtered_df[filtered_df["type"] == "TV Show"]
    )
    st.metric(
        "TV Shows",
        shows
    )


st.divider()


# -----------------------------
# Content Type Chart
# -----------------------------
st.subheader("Movies vs TV Shows")

type_count = filtered_df["type"].value_counts()

fig, ax = plt.subplots()

ax.bar(
    type_count.index,
    type_count.values
)

ax.set_xlabel("Type")
ax.set_ylabel("Number of Titles")

st.pyplot(fig)



# -----------------------------
# Release Year Trend
# -----------------------------
st.subheader("Netflix Releases Over Time")

year_count = (
    filtered_df["release_year"]
    .value_counts()
    .sort_index()
)


fig, ax = plt.subplots()

ax.plot(
    year_count.index,
    year_count.values
)

ax.set_xlabel("Year")
ax.set_ylabel("Number of Releases")

st.pyplot(fig)



# -----------------------------
# Top Countries
# -----------------------------
st.subheader("Top 10 Countries Producing Netflix Content")


countries = (
    filtered_df["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)


fig, ax = plt.subplots()

ax.barh(
    countries.index,
    countries.values
)

ax.set_xlabel("Number of Titles")

st.pyplot(fig)



# -----------------------------
# Genre Analysis
# -----------------------------
st.subheader("Most Popular Genres")


genres = (
    filtered_df["listed_in"]
    .dropna()
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)


fig, ax = plt.subplots()

ax.bar(
    genres.index,
    genres.values
)

plt.xticks(
    rotation=45,
    ha="right"
)

ax.set_ylabel("Titles")

st.pyplot(fig)



# -----------------------------
# Search Titles
# -----------------------------
st.subheader("🔎 Search Netflix Titles")


search = st.text_input(
    "Search movie or TV show"
)


if search:
    results = filtered_df[
        filtered_df["title"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

    st.dataframe(
        results[
            [
                "title",
                "type",
                "country",
                "release_year",
                "rating"
            ]
        ]
    )



# -----------------------------
# Footer
# -----------------------------
st.success(
    "Dashboard created using Python, Pandas, Matplotlib, and Streamlit 🚀"
)
