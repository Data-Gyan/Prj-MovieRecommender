# use streamlit to create quick web application
import pickle
import numpy as np
import pandas as pd
import streamlit as st
import requests
# pickle to serialize python objects
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# open the pkl file to load movies data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# use enumerate to introduce positional index to every item
# send it to the list and reverse sort it based on the second index
def get_recommendations(movie, count=5):
    recommendations = []
    posters = []
    orig_index =  movies[movies['title'] == movie].index[0]
    recommended = sorted(list(enumerate(similarity[orig_index])), reverse=True, key=lambda indx: indx[1])[1:count+1]
    for rec in recommended:
        # Convert first letter to uppercase for convenience
        recommendations.append((movies.loc[rec[0]]['title'])) 
        posters.append(fetch_poster(movies.loc[rec[0]]['id']))
    return recommendations, posters


st.title("The Movie Recommender System")
movies_lst = movies['title'].values
selected_movie = st.selectbox(
    "           Select the movie you want to see similar movies for:                 ",
    movies_lst)

if st.button('Recommend'):
    st.header("Liking '{}'!.., You may also like ".format(selected_movie))
    movie_lst, poster_lst = get_recommendations(selected_movie, count=5)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text(movie_lst[0])
        st.image(poster_lst[0])
        st.text(movie_lst[3])
        st.image(poster_lst[3])
    with col2:
        st.text(movie_lst[1])
        st.image(poster_lst[1])
        st.text(movie_lst[4])
        st.image(poster_lst[4])
    with col3:
        st.text(movie_lst[2])
        st.image(poster_lst[2])       

