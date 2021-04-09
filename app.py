"""Run the meme generator app."""

import os
import random
import shutil

import requests
from flask import Flask, render_template, request

from MemeEngine import MemeEngine
from QuoteEngine import Ingestor

app = Flask(__name__)

meme_dir = './static'

# remove the directory to prevent it from becoming too full
if os.path.exists(meme_dir):
    shutil.rmtree(meme_dir)

meme = MemeEngine(meme_dir)


def setup():
    """Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    quotes = list()
    for path in quote_files:
        ingest = Ingestor.parse(path)
        quotes = [*quotes, *ingest]

    # images_path = "_data/photos/dog/"
    imgs = list()
    for dirpath, dirnames, files in os.walk('./_data/photos'):
        for filename in files:
            path = os.path.join(dirpath, filename)
            imgs.append(path)

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    img_url = request.form['image_url']
    body = request.form['body']
    author = request.form['author']
    local_tmp_file = './_data/tmp-file-from-web.jpg'

    # make sure there is no old file around
    if os.path.exists(local_tmp_file):
        os.remove(local_tmp_file)

    try:
        r = requests.get(img_url, allow_redirects=True)
        file = open(local_tmp_file, 'wb')
        file.write(r.content)
        file.close()

    except Exception as e:
        print('An error occurred when fetching the image.')

    path = meme.make_meme(local_tmp_file, body, author)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
