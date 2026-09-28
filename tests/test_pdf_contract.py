import unittest
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

from src.vampiro_sheet import data

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "dist" / "ficha_vampiro_interativa.pdf"
CALCULATIONS = ROOT / "src" / "vampiro_sheet" / "calculations.js"


def safe_name(value):
    return "".join(character for character in value if character.isalnum())


class ExistingPdfContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = PdfReader(str(PDF))
        cls.form = cls.reader.trailer["/Root"]["/AcroForm"]
        cls.fields = cls.reader.get_fields() or {}
        cls.widgets = {
            str(annotation.get_object().get("/T")): annotation.get_object()
            for page in cls.reader.pages
            for annotation in page.get("/Annots", [])
            if annotation.get_object().get("/Subtype") == "/Widget"
        }

    def test_terminal_field_names_are_unique(self):
        names = [str(ref.get_object().get("/T")) for ref in self.form["/Fields"]]
        duplicates = {name: count for name, count in Counter(names).items() if count > 1}
        self.assertEqual({}, duplicates)

    def test_checkboxes_are_not_required(self):
        required_buttons = [
            name
            for name, field in self.fields.items()
            if field.get("/FT") == "/Btn" and int(field.get("/Ff", 0)) & 2
        ]
        self.assertEqual([], required_buttons)

    def test_document_has_basic_accessibility_metadata(self):
        root = self.reader.trailer["/Root"]
        self.assertEqual("pt-BR", str(root.get("/Lang")))
        self.assertTrue(all(page.get("/Tabs") == "/S" for page in self.reader.pages))

    def test_numeric_fields_and_damage_boxes_have_actions(self):
        actions = {}
        for page in self.reader.pages:
            for annotation_ref in page.get("/Annots", []):
                annotation = annotation_ref.get_object()
                name = str(annotation.get("/T", ""))
                if name:
                    actions[name] = annotation.get("/AA")
        self.assertIn("/V", actions["habilidade_Briga_val"])
        self.assertIn("event.rc", str(actions["habilidade_Briga_val"]["/V"]["/JS"]))
        self.assertIn("/U", actions["vitalidade_Escoriado_letal"])

    def test_all_system_traits_have_expected_fields(self):
        expected = set()
        for group, traits in data.ATTRIBUTES.items():
            for trait in traits:
                base = "atributo_" + safe_name(group) + "_" + safe_name(trait)
                expected.add(base + "_val")
                expected.update(base + "_" + str(index) for index in range(1, 6))
        for traits in data.ABILITIES.values():
            for trait in traits:
                base = "habilidade_" + safe_name(trait)
                expected.add(base + "_val")
                expected.update(base + "_" + str(index) for index in range(1, 6))
        expected.update("disciplina_" + safe_name(item) + "_val" for item in data.DISCIPLINES)
        expected.update(
            "disciplina_detalhe_" + safe_name(item) + "_nivel" for item in data.DISCIPLINES
        )
        expected.update("antecedente_" + safe_name(item) + "_val" for item in data.BACKGROUNDS)
        expected.update("virtude_" + safe_name(item) + "_val" for item in data.VIRTUES)
        self.assertEqual(set(), expected - set(self.fields))

    def test_dropdowns_expose_the_complete_supported_options(self):
        self.assertEqual(
            data.CHARACTER_TYPES,
            [str(option) for option in self.fields["tipo_personagem"]["/Opt"]],
        )
        self.assertEqual(
            data.CLANS,
            [str(option) for option in self.fields["cla"]["/Opt"]],
        )
        self.assertEqual(
            data.GENERATION_OPTIONS,
            [str(option) for option in self.fields["geracao"]["/Opt"]],
        )

    def test_multiline_fields_allow_long_form_content(self):
        for name in [
            "equipamentos",
            "fraqueza_cla",
            "poderes_disciplinas",
            "historia",
            "avisos_criacao",
        ]:
            with self.subTest(field=name):
                self.assertTrue(int(self.fields[name].get("/Ff", 0)) & 4096)
                self.assertEqual(4000, int(self.widgets[name].get("/MaxLen", 0)))

    def test_widgets_stay_inside_their_a4_pages(self):
        for page_number, page in enumerate(self.reader.pages, start=1):
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            for annotation_ref in page.get("/Annots", []):
                annotation = annotation_ref.get_object()
                if annotation.get("/Subtype") != "/Widget":
                    continue
                left, bottom, right, top = map(float, annotation["/Rect"])
                with self.subTest(page=page_number, field=annotation.get("/T")):
                    self.assertLess(left, right)
                    self.assertLess(bottom, top)
                    self.assertGreaterEqual(left, 0)
                    self.assertGreaterEqual(bottom, 0)
                    self.assertLessEqual(right, width)
                    self.assertLessEqual(top, height)

    def test_embedded_javascript_matches_the_reviewed_source(self):
        names = self.reader.trailer["/Root"]["/Names"]["/JavaScript"]["/Names"]
        embedded = [
            str(names[index].get_object().get("/JS", "")) for index in range(1, len(names), 2)
        ]
        self.assertEqual(1, len(embedded))
        self.assertEqual(CALCULATIONS.read_text(encoding="ascii"), embedded[0])


if __name__ == "__main__":
    unittest.main()
