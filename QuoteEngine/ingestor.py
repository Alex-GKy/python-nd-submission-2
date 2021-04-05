"""Extract data from various file types, such as txt, pdf, csv, and docx."""
import pathlib
import subprocess
from abc import ABC, abstractmethod
from typing import List

import docx
import pandas

from .quoteModel import QuoteModel


class IngestorInterface(ABC):
    """An abstract representation of an ingest."""

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if a file type can be processed by this class.

        :param path: A string describing the path to the file to be processed.
        """
        extension = path.split('.')[-1]
        return extension in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a file.

        :param path: A string describing the path to the file to be processed.
        """
        pass


class TXTIngestor(IngestorInterface):
    """A txt file processor."""

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a file.

        :param path: A string describing the path to the file to be processed.
        """
        check_exception(cls, path)

        quotes = list()
        with open(path, 'r') as infile:
            for line in infile:
                quote = line.split('-')[0].strip()
                author = line.split('-')[1].strip()
                quotes.append(QuoteModel(author, quote))

        return quotes


class CSVIngestor(IngestorInterface):
    """A CSV file processor."""

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a file.

        :param path: A string describing the path to the file to be processed.
        """
        check_exception(cls, path)

        quotes = list()
        df = pandas.read_csv(path)

        for index, row in df.iterrows():
            quotes.append(QuoteModel(row['author'], row['body']))


        # with open(path, 'r') as infile:
        #     reader = pandas.read_csv(infile, index_col=0)
        #     # reader = csv.DictReader(infile)
        #
        #     for row in reader:
        #         quotes.append(QuoteModel(row['author'], row['body']))

        return quotes


class DOCXIngestor(IngestorInterface):
    """A docx file processor."""

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a file.

        :param path: A string describing the path to the file to be processed.
        """
        check_exception(cls, path)

        quotes = list()
        doc = docx.Document(path)

        for para in doc.paragraphs:
            if para.text != '':
                quote = para.text.split('-')[0].strip().strip('"')
                author = para.text.split('-')[1].strip().strip('"')
                quotes.append(QuoteModel(author, quote))

        return quotes


class PDFIngestor(IngestorInterface):
    """A pdf file processor."""

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a file.

        :param path: A string describing the path to the file to be processed.
        """
        check_exception(cls, path)

        quotes = list()
        outpath = './_data/pdftotext-output.txt'
        DIR = pathlib.Path(__file__).parent.parent.resolve()
        pdftotext = subprocess.Popen(
            [r'./bin/pdftotext', '-layout', path, outpath],
            stdout=subprocess.PIPE)

        status = pdftotext.wait()
        output, err = pdftotext.communicate()

        # now, open the output file again and read it
        with open(outpath, 'r') as infile:
            for line in infile:
                if line != '\f':
                    quote = line.split('-')[0].strip().strip('"')
                    author = line.split('-')[1].strip().strip('"')
                    quotes.append(QuoteModel(author, quote))

        return quotes


class Ingestor(IngestorInterface):
    """A generic represenation of the other classes in this file."""

    ingestors = [TXTIngestor, CSVIngestor, DOCXIngestor, PDFIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a file.

        :param path: A string describing the path to the file to be processed.
        """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)


def check_exception(cls, path):
    """Check for exceptions in a generic way."""
    if not cls.can_ingest(path):
        raise Exception('Cannot ingest this file type.')
