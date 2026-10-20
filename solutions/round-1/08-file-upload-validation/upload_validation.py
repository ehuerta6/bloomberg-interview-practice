"""Reference upload metadata validation with regression tests."""

import unittest


MAX_BYTES = 5_000_000
ALLOWED = {".pdf": "application/pdf", ".png": "image/png"}


def validate_upload(filename, content_type, size_bytes):
    """Validate a leaf filename, matching MIME type, and bounded byte size."""
    if not isinstance(filename, str) or not filename or filename != filename.strip():
        raise ValueError("filename must be non-empty text without surrounding whitespace")
    if any(char in filename for char in ("/", "\\", "\x00")) or any(ord(char) < 32 for char in filename):
        raise ValueError("filename must be a plain file name")

    lowered = filename.lower()
    extension = next((suffix for suffix in ALLOWED if lowered.endswith(suffix)), None)
    if extension is None or lowered == extension:
        raise ValueError("unsupported extension")

    normalized_type = content_type.strip().lower() if isinstance(content_type, str) else ""
    if normalized_type != ALLOWED[extension]:
        raise ValueError("content type does not match extension")
    if isinstance(size_bytes, bool) or not isinstance(size_bytes, int) or not 0 < size_bytes <= MAX_BYTES:
        raise ValueError("upload size is out of range")

    return {"filename": filename, "content_type": normalized_type, "size_bytes": size_bytes}


class UploadValidationTests(unittest.TestCase):
    def test_pdf_metadata_is_accepted(self):
        self.assertEqual(validate_upload("resume.pdf", "application/pdf", 1200)["filename"], "resume.pdf")

    def test_extension_comparison_is_case_insensitive(self):
        self.assertEqual(validate_upload("chart.PNG", " IMAGE/PNG ", 300)["content_type"], "image/png")

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

    def test_hidden_file_without_a_name_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_upload(".pdf", "application/pdf", 10)

    def test_zero_and_oversized_uploads_are_rejected(self):
        for size in (0, MAX_BYTES + 1):
            with self.subTest(size=size), self.assertRaises(ValueError):
                validate_upload("resume.pdf", "application/pdf", size)


if __name__ == "__main__":
    unittest.main()
