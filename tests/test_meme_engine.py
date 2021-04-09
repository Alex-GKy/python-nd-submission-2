import os
import pathlib
import unittest
import importlib

from MemeEngine import MemeEngine
from PIL import Image
from QuoteEngine import QuoteModel

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

TESTS_ROOT = (pathlib.Path(__file__).parent).resolve()
TEST_DATA = TESTS_ROOT / 'test_data'


class TestQuery(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.quote = QuoteModel('Quote Author', 'Quote Text')

    def test_height_is_calculated_correctly_for_resizing(self):
        new_height = MemeEngine.determine_height(200, 400, 100)
        self.assertEqual(new_height, 200)

    def test_make_meme_returns_path(self):
        meme = MemeEngine('./static')
        img = TEST_DATA / 'Photos/xander_1.jpg'

        result = meme.make_meme(img, self.quote.body, self.quote.author)

        self.assertTrue(type(result) == str)

    def test_image_is_correctly_resized(self):
        meme = MemeEngine('./static')
        img = TEST_DATA / 'Photos/xander_resized.jpg'

        result = meme.make_meme(img, self.quote.body, self.quote.author)

        generated_meme = Image.open(result)
        self.assertEqual(generated_meme.size, (498, 279))

        # clean up
        generated_meme.close()
        os.remove(result)

    def test_text_wrap(self):

        text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, ' \
               'sed do eiusmod tempor incididunt ut labore et dolore magna ' \
               'aliqua. Ut enim ad minim veniam, quis nostrud exercitation ' \
               'ullamco laboris nisi ut aliquip ex ea commodo consequat. ' \
               'Duis aute irure dolor in reprehenderit in voluptate velit ' \
               'esse cillum dolore eu fugiat nulla pariatur. Excepteur sint ' \
               'occaecat cupidatat non proident, sunt in culpa qui officia ' \
               'deserunt mollit anim id est laborum.'

        quote = QuoteModel('Author', text)

        me = MemeEngine('./tmp')

        img_path = TEST_DATA / 'Photos/xander_1.jpg'

        photo = Image.open(img_path)
        font = ImageFont.truetype('./_data/Arial Bold.ttf', 20)
        draw = ImageDraw.Draw(photo)
        outpath = TEST_DATA / './tmp/wrapped-text.jpg'

        draw = MemeEngine.wrap_text(quote, photo, draw, font, outpath)


        photo.save(outpath)