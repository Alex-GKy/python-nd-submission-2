"""Deal with everything around Memes."""

import argparse
import os
import random
import shutil

from MemeEngine import MemeEngine
from QuoteEngine import Ingestor, QuoteModel


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an path and a quote."""
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:

        # would work, but in then there would be an all-default quote
        # which might be confusing
        if author is not None:
            raise Exception('Body required if author is used')

        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author required if body is used')
        quote = QuoteModel(body, author)

    # remove the directory to prevent it from becoming too full
    meme_dir = './tmp'
    if os.path.exists(meme_dir):
        shutil.rmtree(meme_dir)

    meme = MemeEngine(meme_dir)
    path = meme.make_meme(img, quote.body, quote.author)

    return path


if __name__ == "__main__":

    # Accepting optional parameters:
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image

    parser = argparse.ArgumentParser(
        description='Generate a meme from a picture and inspirational '
                    'quotes. If not arguments are given, default data '
                    'will be used to generate a meme.')
    parser.add_argument('--body', '-b', help='The quote to be shown on the meme.',
                        type=str)
    parser.add_argument('--author', '-a', help='The author of this quote.', type=str)
    parser.add_argument('--path', '-p', help='The path to the image for the meme.',
                        type=str)

    args = parser.parse_args()

    try:
        print(generate_meme(args.path, args.body, args.author))

    except Exception as e:
        msg = 'An error has occurred'
        if e.args[0]:
            msg = f'{msg} : {e.args[0]}'
        print(msg)
