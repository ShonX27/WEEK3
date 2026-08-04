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
# Styling
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        background-color:#fafafa;
    }

    h1 {
        text-align:center;
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

    return df



df = load_data()



# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🎬 Netflix Content Analytics Dashboard")


st.markdown(
"""
Explore Netflix movies and TV shows with interactive filters.

Dashboard Features:
- Search Netflix titles
- Filter by release year
- Analyze genres
- Explore countries
- Compare movies and TV shows
"""
)



# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.header("🎛 Dashboard Filters")


# Content Type

type_filter = st.sidebar.multiselect(

    "🎥 Content Type",

    df["type"].dropna().unique(),

    default=df["type"].dropna().unique()

)



# Rating

if "rating" in df.columns:

    rating_filter = st.sidebar.multiselect(

        "⭐ Rating",

        sorted(
            df["rating"]
            .dropna()
            .unique()
        ),

        default=sorted(
            df["rating"]
            .dropna()
            .unique()
        )

    )

else:

    rating_filter=[]



# Year Slider

min_year = int(
    df["release_year"]
    .min()
)


max_year = int(
    df["release_year"]
    .max()
)



year_range = st.sidebar.slider(

    "📅 Release Year",

    min_year,

    max_year,

    (min_year,max_year)

)



# Search

search_title = st.sidebar.text_input(

    "🔎 Search Movie / TV Show"

)



# --------------------------------------------------
# Apply Filters
# --------------------------------------------------

filtered_df = df.copy()



filtered_df = filtered_df[
    filtered_df["type"]
    .isin(type_filter)
]



if rating_filter:

    filtered_df = filtered_df[
        filtered_df["rating"]
        .isin(rating_filter)
    ]



filtered_df = filtered_df[

    (filtered_df["release_year"] >= year_range[0])

    &

    (filtered_df["release_year"] <= year_range[1])

]



if search_title:

    filtered_df = filtered_df[

        filtered_df["title"]
        .str.contains(

            search_title,

            case=False,

            na=False

        )

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

    st.metric(

        "Movies",

        len(
            filtered_df[
                filtered_df["type"]=="Movie"
            ]
        )

    )



with col3:

    st.metric(

        "TV Shows",

        len(
            filtered_df[
                filtered_df["type"]=="TV Show"
            ]
        )

    )



with col4:

    st.metric(

        "Latest Release",

        filtered_df["release_year"]
        .max()

        if len(filtered_df)>0

        else "N/A"

    )



# --------------------------------------------------
# Filter Results Table
# --------------------------------------------------

st.divider()


st.subheader("🎬 Filtered Netflix Titles")


st.write(
    f"Showing **{len(filtered_df)} titles**"
)



if len(filtered_df)>0:


    columns = [

        "title",
        "type",
        "release_year",
        "country",
        "rating",
        "listed_in"

    ]


    available_columns = [

        c for c in columns

        if c in filtered_df.columns

    ]



    st.dataframe(

        filtered_df[available_columns],

        use_container_width=True,

        height=350

    )


else:

    st.warning(
        "No results found. Adjust your filters."
    )



# --------------------------------------------------
# Movies vs TV Shows
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




# --------------------------------------------------
# Ratings
# --------------------------------------------------


with col2:


    st.subheader(
        "⭐ Ratings Distribution"
    )


    if "rating" in filtered_df.columns:


        rating_count=(

            filtered_df["rating"]

            .value_counts()

            .head(10)

        )


        fig,ax=plt.subplots()


        ax.bar(

            rating_count.index,

            rating_count.values

        )


        plt.xticks(rotation=45)


        st.pyplot(fig)



# --------------------------------------------------
# Release Trend
# --------------------------------------------------

st.subheader(
    "📈 Netflix Growth Over Years"
)



release=(

    filtered_df["release_year"]

    .value_counts()

    .sort_index()

)



fig,ax=plt.subplots()



ax.plot(

    release.index,

    release.values

)



ax.set_xlabel("Year")

ax.set_ylabel("Titles")



st.pyplot(fig)



# --------------------------------------------------
# Countries
# --------------------------------------------------

if "country" in filtered_df.columns:


    st.subheader(
        "🌎 Top Producing Countries"
    )


    countries=(

        filtered_df["country"]

        .dropna()

        .str.split(", ")

        .explode()

        .value_counts()

        .head(10)

    )


    fig,ax=plt.subplots()


    ax.barh(

        countries.index,

        countries.values

    )


    st.pyplot(fig)




# --------------------------------------------------
# Genres
# --------------------------------------------------

if "listed_in" in filtered_df.columns:


    st.subheader(
        "🎭 Popular Genres"
    )


    genres=(

        filtered_df["listed_in"]

        .dropna()

        .str.split(", ")

        .explode()

        .value_counts()

        .head(10)

    )



    fig,ax=plt.subplots()



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
# Footer
# --------------------------------------------------

st.success(
    "Built with Python | Pandas | Matplotlib | Streamlit 🚀"
)
