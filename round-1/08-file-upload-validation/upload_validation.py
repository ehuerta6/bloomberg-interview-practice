"""Validate metadata for a small document-upload endpoint."""

import unittest


MAX_BYTES = 5_000_000
ALLOWED = {".pdf": "application/pdf", ".png": "image/png"}


def validate_upload(filename, content_type, size_bytes):
    """Return normalized metadata for an accepted upload or raise ValueError."""
    if not filename or not filename.lower().endswith((".pdf", ".png")):
        raise ValueError("unsupported extension")
    if content_type not in ALLOWED.values():
        raise ValueError("unsupported content type")
    if size_bytes <= 0 or size_bytes > MAX_BYTES:
        raise ValueError("upload size is out of range")
    return {"filename": filename, "content_type": content_type, "size_bytes": size_bytes}


class UploadValidationTests(unittest.TestCase):
    def test_pdf_metadata_is_accepted(self):
        self.assertEqual(validate_upload("resume.pdf", "application/pdf", 1200)["filename"], "resume.pdf")

    def test_extension_comparison_is_case_insensitive(self):
        self.assertEqual(validate_upload("chart.PNG", "image/png", 300)["filename"], "chart.PNG")

    def test_exact_size_limit_is_allowed(self):
        self.assertEqual(validate_upload("large.pdf", "application/pdf", MAX_BYTES)["size_bytes"], MAX_BYTES)

    def test_path_components_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_upload("../private.pdf", "application/pdf", 10)

    def test_windows_path_components_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_upload(r"C:\private\report.pdf", "application/pdf", 10)

    def test_extension_and_mime_type_must_match(self):
        with self.assertRaises(ValueError):
            validate_upload("photo.png", "application/pdf", 10)

    def test_boolean_size_is_not_an_integer_byte_count(self):
        with self.assertRaises(ValueError):
            validate_upload("tiny.png", "image/png", True)

    def test_double_extension_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_upload("invoice.pdf.exe", "application/pdf", 10)


if __name__ == "__main__":
    unittest.main()
