"""Represent a quote."""


class QuoteModel():
    """A single quote."""

    def __init__(self, author: str, body: str):
        """Build a quote.

        :param author: The author of the quote
        :param body: The deep stuff this dog said.
        """
        self.author = author
        self.body = body

    def __eq__(self, other):
        """Compare this quote to another.

        :param other: The quote to compare to.
        """
        if (self.author == other.author) and (self.body == other.body):
            return True
        else:
            return False
