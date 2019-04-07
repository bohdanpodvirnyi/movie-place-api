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
    print(movies)
    return jsonify({'results': movies})


@app.route('/autocomplete/<search_text>', methods=['GET'])
def autocomplete_user_search(search_text):
    movies = get_titles_list()
    result_dic = {key: value for key, value in movies.items() if movies_filter(value, search_text)}
    result_list = [(v, k) for k, v in result_dic.items()]
    sorted_list = sorted(result_list, key=lambda movie: (movies_sorting(movie, search_text)), reverse=True)
    modified_list = modify(sorted_list)
    return jsonify({'results': modified_list})


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


def movies_filter(value, search_text):
    return search_text.decode("utf8") in str(value).decode("utf8").lower()


def movies_sorting(movie, search_text):
    return movie[0].decode("utf8").lower().startswith(search_text)


def modify(original_list):
    new_list = []
    for movie in original_list:
        if len(new_list) == 5:
            return new_list
        new_movie = {'name': movie[0], 'base_id': movie[1], 'imdb_id': get_imdbid_by_baseid(movie[1])}
        new_list.append(new_movie)
    return new_list
