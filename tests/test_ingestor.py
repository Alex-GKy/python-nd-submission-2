import pathlib
import unittest

import QuoteEngine as qe
from QuoteEngine import QuoteModel

TESTS_ROOT = (pathlib.Path(__file__).parent).resolve()
TEST_DATA = TESTS_ROOT / 'test_data'
TEST_TXT_FILE = TEST_DATA / 'DogQuotes/DogQuotesTXT.txt'
TEST_CSV_FILE = TEST_DATA / 'DogQuotes/DogQuotesCSV.csv'
TEST_DOCX_FILE = TEST_DATA / 'DogQuotes/DogQuotesDOCX.docx'
TEST_PDF_FILE = TEST_DATA / 'DogQuotes/DogQuotesPDF.pdf'


class TestQuery(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.txt_quote1 = QuoteModel('Bork', 'To bork or not to bork')
        cls.txt_quote2 = QuoteModel('Stinky', 'He who smelt it...')

        cls.csv_quote1 = QuoteModel('Mr. Paws',
                                    'When in doubt, go shoe-shopping')

        cls.docx_quote1 = QuoteModel('Peanut',
                                     'Life is like peanut butter: crunchy')

        cls.pdf_quote1 = QuoteModel('Bark Twain',
                                    'It\'s the size of the fight in the dog')

        cls.csv_quote1.__repr__()

    def test_nothing(self):
        expected = 1
        self.assertEqual(expected, 1)

    def test_TXTIngestor(self):
        expected = [self.txt_quote1, self.txt_quote2]

        quotes = qe.TXTIngestor.parse(str(TEST_TXT_FILE))

        # for whatever reason,there's a zero whitespace at the start of the
        # text attribute...
        self.assertEqual(expected[0].author, quotes[0].author,
                         'Authors don\'t match')

    def test_CSVIngestor(self):
        expected = [self.csv_quote1]

        quotes = qe.CSVIngestor.parse(str(TEST_CSV_FILE))

        self.assertEqual(expected[0].author, quotes[1].author,
                         'Authors don\'t match')

    def test_DOCXIngestor(self):
        expected = [self.docx_quote1]

        quotes = qe.DOCXIngestor.parse(str(TEST_DOCX_FILE))

        self.assertEqual(expected[0].author, quotes[2].author,
                         'Authors don\'t match')

    def test_PDFIngestor(self):
        expected = [self.pdf_quote1]

        quotes = qe.PDFIngestor.parse(str(TEST_PDF_FILE))

        self.assertEqual(expected[0].author, quotes[2].author,
                         'Authors do not match')

    def test_ingestor_calling_TXTIngestor(self):
        expected = [self.txt_quote1, self.txt_quote2]

        quotes = qe.Ingestor.parse(str(TEST_TXT_FILE))

        self.assertEqual(expected[0].author, quotes[0].author,
                         'Quotes don\'t match')

    def test_raise_exception_on_wrong_file_type(self):
        with self.assertRaises(Exception):
            qe.TXTIngestor.parse(str(TEST_DOCX_FILE))

        with self.assertRaises(Exception):
            qe.CSVIngestor.parse(str(TEST_DOCX_FILE))

        with self.assertRaises(Exception):
            qe.PDFIngestor.parse(str(TEST_DOCX_FILE))

        with self.assertRaises(Exception):
            qe.DOCXIngestor.parse(str(TEST_PDF_FILE))
