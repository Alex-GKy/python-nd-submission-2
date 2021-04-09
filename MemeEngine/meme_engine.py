"""Generate Memes from pictures and quotes."""

import os
import pathlib
import random
import string
import textwrap
import math

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class MemeEngine():
    """Represent an engine to generate memes."""

    def __init__(self, output_folder):
        """Set up a new meme generator.

        :param output_folder: The folder to which memes are written.
        """
        self.output_path = output_folder
        self.default_image = './_data/photos/dog/xander_1.jpg'

        if not os.path.exists(self.output_path):
            os.makedirs(output_folder)

    def make_meme(self, img_path, body, author):
        """Make a meme.

        Supple a path to an image, the text to be displayed and an author of
        the quote.

        :param img_path: A string representing the path to the image that will
        be used for the meme.
        :param body: The text to be shown on the meme.
        :param author: The author of the quote.
        """
        # resize the image
        new_width = 500

        try:
            photo = Image.open(img_path)

            new_height = self.determine_height(photo.size[0], photo.size[1],
                                           new_width)
            photo.thumbnail((new_width, new_height))

        except Exception as e:
            print('Something went wrong fetching the picture')
            photo = Image.open(self.default_image)
            body = f'Something went wrong, sorry...'
            new_height = 500

        # add text
        font = ImageFont.truetype('./_data/Arial Bold.ttf', 20)
        draw = ImageDraw.Draw(photo)

        margin = 10
        offset = 10

        # get the size of one letter in width
        letter_size = int( font.getsize(body)[0] / len(body) )

        # calculate the max amount of letters in one line:
        line_length = math.floor(photo.size[0] / letter_size) - math.floor(margin/letter_size)
        line_length = line_length * 0.9

        # write line by line
        # for line in textwrap.wrap(body, width=photo.size[0]-margin-10):
        #     draw.text((margin, offset), line, 'white', font=font)
        #     offset += font.getsize(line)[1]

        for line in textwrap.wrap(body, line_length):

            draw.text((margin, offset), line, 'white', font=font)
            offset += font.getsize(line)[1]

        # add the author
        draw.text((margin,offset), f'- {author}', 'white', font=font)

        # Generate a random string to make the filename unique - to prevent
        # issues with browser caching
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(10))

        # save
        out_path = os.path.join(self.output_path,
                               pathlib.Path(img_path).stem +
                               '_meme_' + rand_string +
                               pathlib.Path(img_path).suffix)

        if os.path.exists(out_path):
            os.remove(out_path)

        try:
            photo.save(out_path, "JPEG")

        except Exception as e:
            print('An error occurred when saving the file')
            photo.close()

        return out_path

    @classmethod
    def wrap_text(cls, quote, photo, draw, font, outpath):

        quote = f'{quote.body}\n- {quote.author}'

        margin = 10
        offset = 10

        # get the size of one letter in width
        letter_size = int( font.getsize(quote)[0] / len(quote) )

        # calculate the max amount of letters in one line:
        line_length = math.floor(photo.size[0] / letter_size) - math.floor(margin/letter_size)
        line_length = line_length * 0.9

        for line in textwrap.wrap(quote, line_length):

            draw.text((margin, offset), line, 'white', font=font)
            offset += font.getsize(line)[1]

        return draw
        # photo.save(outpath)


    @classmethod
    def determine_height(cls, original_width: int, original_height: int,
                         new_width: int) -> int:
        """
        Determine the height an image should have given its desired width.

        The goal here is to preserve a picture's aspect ratio.

        :param original_width: The width of the original image.
        :param original_height: The height of the original image.
        :param new_width: The width the new image should have to preserve the
        original's ratio.
        :return:
        """
        ratio = new_width / original_width
        new_height = int(original_height * ratio)
        return new_height
