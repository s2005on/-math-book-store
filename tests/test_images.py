"""Ensure the packaged site never regresses to blurry demo thumbnails."""
import json
import unittest
from pathlib import Path
from PIL import Image
import test_settings

WEB = Path(__file__).resolve().parents[1] / 'server' / 'web'


class ProductImageTests(unittest.TestCase):
    def test_full_resolution_book_images(self):
        books=json.loads((WEB/'catalog.json').read_text(encoding='utf-8'))
        for book in books:
            with self.subTest(book=book['id']):
                with Image.open(WEB / book['image']) as photo:
                    self.assertGreaterEqual(photo.width, 900)
                    self.assertGreaterEqual(photo.height, 800)

    def test_canonical_prices(self):
        books={b['id']:b for b in json.loads((WEB/'catalog.json').read_text(encoding='utf-8'))}
        self.assertEqual(books['hsg8']['price'],198000)
        self.assertEqual(books['upcoming-logic']['price'],280000)
        self.assertEqual(books['upcoming-logic']['status'],'coming_soon')
        self.assertEqual(books['hsg7']['status'],'coming_soon')

if __name__=='__main__': unittest.main()
