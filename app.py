from flask import Flask, jsonify
from recommendations import get_titles_list, improved_recommendations, get_imdbid_by_baseid

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


@app.route('/recommend/<film_id>', methods=['GET'])
def get_recommendations_by_one(film_id):
    movies = get_titles_list()
    movie = movies.get(int(film_id))
    if movie is None:
        return something_went_wrong()
    else:
        recommended_movies = improved_recommendations(movie, 5)
        return jsonify({'results': recommended_movies})


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
        new_movie = (movie[0], get_imdbid_by_baseid(movie[1]))
        new_list.append(new_movie)
    return new_list
