import streamlit as st
from config_loader import load_page_config
from backend import MovieRecommendation

movie = MovieRecommendation()

# Page config
page_configs = load_page_config()
st.set_page_config(page_title=page_configs['page_title'],
                   page_icon=page_configs['page_icon'],
                   layout=page_configs['layout'])

# Header
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎬 Movie Recommendation App</h1>", unsafe_allow_html=True)
st.write("Discover movies tailored to your taste with an interactive and stylish interface!")

# Sidebar for preferences
st.sidebar.header("✨ Customize Your Preferences")
genres = movie.available_genres()
selected_genre = st.sidebar.radio(
    label="Choose a genre:",
    options=genres,
    index=3
)

selected_rating = st.sidebar.slider(
    "Minimum IMDb Rating:",
    min_value=0.0, max_value=10.0, step=1.0
)

years = movie.release_year()
years.insert(0, "-------Any-------")
selected_year = st.sidebar.selectbox(
    label="Preferred Release Year:",
    options=years
)
st.sidebar.button("🎬 Apply Filters")

# --- Top 10 Popular Movies Section ---
st.subheader("🔥 Top 10 Popular Movies of all time")
popular_movies, ratings = movie.popular()

for i, movie_name in enumerate(popular_movies, start=1):
    st.markdown(f"{i}. **{movie_name}** ⭐ {round(ratings[i-1],1)}")

# --- Search bar ---
st.subheader("🔍 Search for a Movie")
movie_title = st.text_input("Enter a movie name:", placeholder="Movie name").strip().lower()

# Display search results
def show_movies_in_grid(similar_movie_list, date_list, runtime_list, status_list,
                    description_list, genre_list, language_list, ratings, row_size=3):
    """ Display movies in a grid pattern.
    :param similar_movie_list: list of movie titles
    :param date_list: list of movie release dates
    :param runtime_list: list of movie runtimes
    :param status_list: list of movie status
    :param description_list: list of movie descriptions
    :param genre_list: list of movie genres
    :param language_list: list of movie languages
    :param ratings: list of ratings
    :param row_size: number of movies per row """
    for start in range(0, len(similar_movie_list), row_size):
        cols = st.columns(row_size)
        for i, col in enumerate(cols):
            if start + i < len(similar_movie_list):
                with col:
                    st.markdown(f"[**{similar_movie_list[start+i]}**]")
                    st.markdown(f"**Ratings: {round(ratings[start+i], 1)} ⭐**")
                    st.caption(f"Genre: {genre_list[start+i]} | Runtime: {runtime_list[start+i]} mins")
                    st.caption(f"Status: {status_list[start+i]} ({date_list[start + i]})")
                    st.caption(f"Available Languages: {language_list[start+i]}")
                    st.caption(f"{description_list[start+i]}")
                    st.button("🎬 Watch", key=similar_movie_list[start+i])

if movie_title:
    st.subheader("🎥 Search Result")

    (similar_movie_list, date_list, runtime_list, status_list,
     description_list, genre_list, language_list, ratings, similarity_scores) = movie.recommend(movie_title=movie_title)

    if len(similar_movie_list)>0:
        show_movies_in_grid(similar_movie_list, date_list, runtime_list, status_list,
         description_list, genre_list, language_list, ratings)
    else:
        st.warning("Movie not found.")

    # --- Carousel-style recommendations ---
    st.subheader("🎞️ Recommended Movies")
    st.success("Swipe through these picks based on your preferences:")

    tabs = st.tabs(similar_movie_list)

    for i, tab in enumerate(tabs):
        with tab:
            st.markdown(f"**{similar_movie_list[i]}** | Similarity: {similarity_scores[i]}")


# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Made for best movie recommendation ❤️")
