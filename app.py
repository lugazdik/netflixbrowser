from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
import csv
import requests
from lxml import html
app = Flask(__name__)

movies = []
with open('IMDB_results.csv', encoding="utf8") as csv_file:
    movie_csv = csv.reader(csv_file, delimiter=',')
    first_line = True
    for row in movie_csv:
        if not first_line:
            movies.append({
                "imdb_id": row[0],
                "imdb_rating": row[1],
                "imdb_title": row[2],
                "type": row[3],
                "title": row[4],
                "director": row[5],
                "cast": row[6],
                "release_year": row[7],
                "duration": row[8],
                "genre": row[9],
                "description": row[10],
            })
        else:
            first_line = False


def get_movies(offset=0, per_page=16):
    return movies[offset: offset + per_page]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form.getlist('genre'), request.form.getlist('order'), request.form.get('search_bar'))

    url = "https://www.imdb.com/title/tt9428190/"
    r = requests.get(url)
    html_content = html.fromstring(r.content)
    news_links = html_content.xpath('//div[@class="poster"]/a/img[@src]/@src')[0]
    print(news_links)

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(movies)
    per_page = 16
    pagination_movies = get_movies(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, alignment='center', css_framework='bootstrap4')
    return render_template('index.html',
                           movies=pagination_movies,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


if __name__ == '__main__':
    app.run()
