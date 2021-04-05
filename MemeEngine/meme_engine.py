"""Generate Memes from pictures and quotes."""

import os
import pathlib
import random
import string

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
        if not os.path.exists(self.output_path):
            os.makedirs(output_folder)

    def make_meme(self, img_path, text, author):
        """Make a meme.

        Supple a path to an image, the text to be displayed and an author of
        the quote.

        :param img_path: A string representing the path to the image that will
        be used for the meme.
        :param text: The text to be shown on the meme.
        :param author: The author of the quote.
        """
        # resize the image
        new_width = 500
        photo = Image.open(img_path)
        new_height = self.determine_height(photo.size[0], photo.size[1],
                                           new_width)
        photo.thumbnail((new_width, new_height))

        # add text
        quote = f'{text}\n- {author}'
        font = ImageFont.truetype('./_data/Arial Bold.ttf', 20)
        draw = ImageDraw.Draw(photo)
        draw.text((new_width / 4, new_height / 4), quote, 'white', font=font)

        # Generate a random string to make the filename unique - to prevent
        # issues with browser caching
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(10))

        # save
        outpath = os.path.join(self.output_path,
                               pathlib.Path(img_path).stem +
                               '_meme_' + rand_string +
                               pathlib.Path(img_path).suffix)

        if os.path.exists(outpath):
            os.remove(outpath)

        try:
            photo.save(outpath, "JPEG")

        except Exception as e:
            print('An error occurred when saving the file')
            photo.close()

        return outpath

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
