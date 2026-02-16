import pickle
import streamlit as st
import requests
import pandas as pd
import io  
import gdown
import os

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data.get('poster_path') 
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        full_path = "https://via.placeholder.com/500x750?text=No+Image"
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster

st.header("Movies Recommendation Sytem Using ML")
# Example Google Drive direct link
#url1 = "https://drive.google.com/uc?export=download&id=1No5I5CtE1kC2404sGamLWVJH8mW83FVa"
#url2 = "https://drive.google.com/uc?export=download&id=1ktKeIokj74omtoBnkUPBlcyVGALdojpo"

# Folder to store downloaded files
if not os.path.exists("artifacts"):
    os.mkdir("artifacts")

# Google Drive file IDs
movie_dict_id = "1No5I5CtE1kC2404sGamLWVJH8mW83FVa"
similarity_id = "1ktKeIokj74omtoBnkUPBlcyVGALdojpo"

# Download files if not already downloaded
movie_dict_file = "artifacts/movie_dict.pkl"
similarity_file = "artifacts/similarity.pkl"

if not os.path.exists(movie_dict_file):
    gdown.download(f"https://drive.google.com/uc?id={movie_dict_id}", movie_dict_file, quiet=False)

if not os.path.exists(similarity_file):
    gdown.download(f"https://drive.google.com/uc?id={similarity_id}", similarity_file, quiet=False)

# Load pickle files
with open(movie_dict_file, "rb") as f:
    movies_dict = pickle.load(f)

with open(similarity_file, "rb") as f:
    similarity = pickle.load(f)


#r = requests.get(url1)
#r1 = requests.get(url2)
#movies_dict = pickle.load(io.BytesIO(r.content))
# movies_dict = pickle.load(open('artifacts/movie_dict.pkl', 'rb'))
# similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
#similarity  = pickle.load(io.BytesIO(r1.content))
movies = pd.DataFrame(movies_dict)
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie to get recommendation",
     movie_list
)

if st.button("Show recommendation"):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])

    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])

    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])

    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])

    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])
