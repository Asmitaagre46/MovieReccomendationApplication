from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests

app = Flask(__name__, static_folder='static')

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=318950068d02c0404f88480caefd6ac7&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies =[]
    recommended_movies_posters=[]

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    poster = None
    if request.method == 'POST':
        value = request.form.get('input_value')
        name, poster = recommend(value)
    return render_template('index.html', name=name, poster=poster)
