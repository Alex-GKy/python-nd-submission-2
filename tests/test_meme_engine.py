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
