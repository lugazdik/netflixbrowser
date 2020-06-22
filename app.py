from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
import csv
app = Flask(__name__)

checkboxes = [False, False, False, False, False, False, False, False]
radio = [False, False]
search_bar = ""
movies = []
with open('IMDB_resultsFinal2.csv', encoding="utf8") as csv_file:
    movie_csv = csv.reader(csv_file, delimiter=',')
    first_line = True
    for row in movie_csv:
        if not first_line:
            movies.append({
                "imdb_id": row[0],
                "imdb_rating": row[1],
                "imdb_title": row[2],
                "image": row[3],
                "rating": row[4],
                "type": row[5],
                "title": row[6],
                "director": row[7],
                "cast": row[8],
                "release_year": row[9],
                "duration": row[10],
                "genre": row[11],
                "description": row[12],
            })
        else:
            first_line = False

original_movies = movies[:]


def get_movies(offset=0, per_page=16):
    return movies[offset: offset + per_page]


def filter_genres(genres):
    if 'Action' in genres:
        checkboxes[0] = True
    if 'Comedies' in genres:
        checkboxes[1] = True
    if 'Documentaries' in genres:
        checkboxes[2] = True
    if 'Horror' in genres:
        checkboxes[3] = True
    if 'Children' in genres:
        checkboxes[4] = True
    if 'Romantic' in genres:
        checkboxes[5] = True
    if 'Sci-Fi & Fantasy' in genres:
        checkboxes[6] = True
    if 'Thrillers' in genres:
        checkboxes[7] = True
    movies.clear()
    for movie in original_movies:
        check = False
        for genre in genres:
            if genre in movie['genre']:
                check = True
        if check:
            movies.append(movie)


def find_by_name(name):
    global movies
    movies = [movie for movie in movies if name in movie['title'].lower()]


@app.route('/', methods=['GET', 'POST'])
def index():
    global movies, checkboxes, radio, search_bar
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    if request.method == 'POST':
        checkboxes = [False] * 8
        genres = request.form.getlist('genre')
        order = request.form.get('order')
        search_bar = request.form.get('search_bar')
        if len(genres) == 0:
            movies = original_movies[:]
        else:
            filter_genres(genres)
        if search_bar != '':
            find_by_name(search_bar.lower())
        if order == 'By Year':
            radio[0] = True
            radio[1] = False
            movies = sorted(movies, key=lambda i: (- int(i['release_year']), i['title']))
        elif order == 'By Rating':
            radio[0] = False
            radio[1] = True
            movies = sorted(movies, key=lambda i: (- float(i['rating']), i['title']))
    per_page = 16
    offset = (page - 1) * per_page
    total = len(movies)
    pagination_movies = get_movies(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, alignment='center', css_framework='bootstrap4')
    return render_template('index.html',
                           movies=pagination_movies,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           checkboxes=checkboxes,
                           radio=radio,
                           search_bar=search_bar,
                           )


if __name__ == '__main__':
    app.run()
