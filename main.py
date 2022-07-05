import dataclasses
import sys
import json
from typing import Iterator
import bs4
import requests
from dataclasses import dataclass


@dataclass
class Movie:
    rank: int
    title: str
    alt_title: str


# html of a sample page: 'https://movie.douban.com/top250?start=0'
# This function get all 25 pages of them.
def get_all_index_html() -> Iterator[str]:
    for i in range(10):
        base_url = 'https://movie.douban.com/top250?start={}'
        page_url = base_url.format(i*25)
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        headers = {'User-Agent': user_agent}
        yield requests.get(page_url, headers=headers).text


def get_all_movie_of_page(page_html: str):
    # Refer to the page html yourself
    soup = bs4.BeautifulSoup(page_html, 'html.parser')
    for item in soup.select('div.item'):
        rank = item.select_one('em').text
        title = item.select('span.title')[0].text
        try:
            alt_title = item.select('span.title')[1].text
        except:
            alt_title = item.select_one('span.other').text

        alt_title = alt_title.split('/')[1].strip()
        yield Movie(int(rank), title, alt_title)


if __name__ == '__main__':
    movies = []
    # iterator of html data of index pages
    index = get_all_index_html()
    for html in index:
        # iterator of all movie data in one page
        movie = get_all_movie_of_page(html)
        for mov in movie:
            mov = dataclasses.asdict(mov)
            print(mov, file=sys.stderr)
            movies.append(mov)

    print(json.dumps(movies, indent=4, ensure_ascii=False))
