import shutil
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import Mock, patch
from uuid import uuid4

from PIL import Image

import main


@contextmanager
def test_directory():
    directory = Path.cwd() / f".test-temp-{uuid4().hex}"
    directory.mkdir()
    try:
        yield directory
    finally:
        shutil.rmtree(directory, ignore_errors=True)


class NormalizeFilenameTests(unittest.TestCase):
    def test_adds_png_extension(self):
        self.assertEqual(main.normalize_filename("менин-кодум"), "менин-кодум.png")

    def test_does_not_duplicate_png_extension(self):
        self.assertEqual(main.normalize_filename("код.PNG"), "код.png")

    def test_rejects_unsafe_or_empty_names(self):
        invalid_names = (
            "",
            "   ",
            "../secret",
            "..\\secret",
            "folder/code",
            "folder\\code",
            "bad*name",
            "bad\nname",
            "CON",
            "NUL.txt",
        )

        for name in invalid_names:
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    main.normalize_filename(name)


class GenerateQrTests(unittest.TestCase):
    def test_generates_file_in_requested_directory(self):
        fake_image = Mock()
        fake_image.save.side_effect = lambda stream, format: stream.write(b"png-data")

        with test_directory() as output_directory:
            with patch("main.qrcode.make", return_value=fake_image) as make_qr:
                result = main.generate_qr(
                    "https://example.com",
                    "example.png",
                    output_directory,
                )

            self.assertEqual(result, output_directory / "example.png")
            self.assertEqual(result.read_bytes(), b"png-data")
            make_qr.assert_called_once_with("https://example.com")
            fake_image.save.assert_called_once()

    def test_rejects_empty_content(self):
        with test_directory() as output_directory:
            with self.assertRaises(ValueError):
                main.generate_qr("   ", "empty", output_directory)

    def test_does_not_overwrite_existing_file(self):
        with test_directory() as output_directory:
            existing_file = output_directory / "existing.png"
            existing_file.write_bytes(b"original")

            with self.assertRaises(FileExistsError):
                main.generate_qr("new data", "existing", output_directory)

            self.assertEqual(existing_file.read_bytes(), b"original")

    def test_creates_valid_png_with_real_qrcode_library(self):
        with test_directory() as output_directory:
            result = main.generate_qr(
                "https://example.com",
                "real-qr",
                output_directory,
            )

            with Image.open(result) as image:
                self.assertEqual(image.format, "PNG")
                self.assertGreater(image.width, 0)
                self.assertGreater(image.height, 0)


if __name__ == "__main__":
    unittest.main()
