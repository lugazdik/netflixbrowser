from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args
import csv
app = Flask(__name__)

movies = []
with open('netflix_titles.csv', encoding="utf8") as csv_file:
    data = csv.reader(csv_file, delimiter=',')
    first_line = True
    for row in data:
        if not first_line:
            movies.append({
                "show_id": row[0],
                "type": row[1],
                "title": row[2],
                "director": row[3],
                "cast": row[4],
                "country": row[5],
                "date_added": row[6],
                "release_year": row[7],
                "rating": row[8],
                "duration": row[9]
            })
        else:
            first_line = False


def get_movies(offset=0, per_page=16):
    return movies[offset: offset + per_page]


@app.route('/')
def index():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(movies)
    per_page = 16
    pagination_movies = get_movies(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, alignment='center',
                            css_framework='bootstrap4')
    return render_template('index.html',
                           movies=pagination_movies,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )
#    return render_template("index.html", movies=movies)


if __name__ == '__main__':
    app.run()
