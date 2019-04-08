from flask import Flask, jsonify, request
from recommendations import *

app = Flask(__name__)
app.secret_key = 'python/labs/lab3'


@app.route('/', methods=['GET'])
def initial():
    return get_login_error()


@app.route('/all_movies', methods=['GET'])
def get_movies():
    movies = get_titles_list()
    return jsonify({'results': movies})


@app.route('/autocomplete/<search_text>', methods=['GET'])
def autocomplete_user_search(search_text):
    movies = generate_autocomplete(search_text)
    sorted_list = sorted(movies, key=lambda movie: (movies_sorting(movie, search_text)), reverse=True)
    return jsonify({'results': sorted_list})


@app.route('/recommend', methods=['POST'])
def get_recommendations_by_one():
    json = request.get_json()
    movie_names = json['movie_names']
    if len(movie_names) != 0:
        recommended_movies = several_films(movie_names)
        return jsonify({'results': recommended_movies})
    else:
        return something_went_wrong()


def get_login_error():
    result = {"error": True, "message": "Login error. Please, log in and try again."}
    return jsonify(result)


def get_access_error():
    result = {"error": True, "message": "Access error. You have no access to this data."}
    return jsonify(result)


def something_went_wrong():
    result = {"error": True, "message": "Something went wrong. Please, try again."}
    return jsonify(result)


def movies_sorting(movie, search_text):
    return movie['title'].decode("utf8").lower().startswith(search_text)
