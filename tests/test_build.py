import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

from src.vampiro_sheet.build import build

ROOT = Path(__file__).resolve().parents[1]
DISTRIBUTED_PDF = ROOT / "dist" / "ficha_vampiro_interativa.pdf"


def pdf_contract(pdf_path):
    reader = PdfReader(str(pdf_path))
    fields = reader.get_fields() or {}
    field_contract = {
        name: (
            str(field.get("/FT", "")),
            int(field.get("/Ff", 0)),
            tuple(str(option) for option in field.get("/Opt", [])),
        )
        for name, field in fields.items()
    }
    actions = {}
    for page in reader.pages:
        for annotation_ref in page.get("/Annots", []):
            annotation = annotation_ref.get_object()
            if annotation.get("/T"):
                actions[str(annotation["/T"])] = str(annotation.get("/AA", ""))
    javascript_names = reader.trailer["/Root"]["/Names"]["/JavaScript"]["/Names"]
    javascript = tuple(
        str(javascript_names[index].get_object().get("/JS", ""))
        for index in range(1, len(javascript_names), 2)
    )
    return {
        "page_sizes": tuple(
            (float(page.mediabox.width), float(page.mediabox.height)) for page in reader.pages
        ),
        "page_text": tuple(page.extract_text() for page in reader.pages),
        "fields": field_contract,
        "actions": actions,
        "javascript": javascript,
        "language": str(reader.trailer["/Root"].get("/Lang")),
        "tabs": tuple(str(page.get("/Tabs")) for page in reader.pages),
    }


class CleanBuildTests(unittest.TestCase):
    def test_builds_complete_pdf_outside_project_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            output = temporary / "dist" / "sheet.pdf"
            work_dir = temporary / "build"

            result = build(output=output, work_dir=work_dir)

            self.assertEqual(output, result)
            self.assertTrue(output.exists())
            self.assertTrue((work_dir / "ficha_vampiro_interativa_draft.pdf").exists())
            reader = PdfReader(str(output))
            self.assertEqual(5, len(reader.pages))
            self.assertGreaterEqual(len(reader.get_fields() or {}), 480)
            self.assertIn("/JavaScript", reader.trailer["/Root"]["/Names"])
            self.assertEqual(pdf_contract(DISTRIBUTED_PDF), pdf_contract(output))


if __name__ == "__main__":
    unittest.main()
