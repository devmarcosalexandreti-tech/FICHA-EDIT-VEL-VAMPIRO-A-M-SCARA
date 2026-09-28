import unittest
from collections import Counter
from pathlib import Path

from pypdf import PdfReader
from pypdf.generic import ContentStream
from reportlab.lib.units import mm

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

    def test_all_attributes_start_with_one_filled_dot(self):
        for group, traits in data.ATTRIBUTES.items():
            for trait in traits:
                base = "atributo_" + safe_name(group) + "_" + safe_name(trait)
                with self.subTest(attribute=trait):
                    self.assertEqual("1", str(self.fields[base + "_val"].get("/V")))
                    self.assertEqual("/Yes", str(self.fields[base + "_1"].get("/V")))
                    for index in range(2, 6):
                        self.assertEqual(
                            "/Off", str(self.fields[base + "_" + str(index)].get("/V"))
                        )

    def test_animal_ken_uses_the_abbreviated_visible_label(self):
        page_text = self.reader.pages[0].extract_text()
        self.assertIn("Empatia C/ Animais", page_text)
        self.assertNotIn("Empatia com Animais", page_text)
        self.assertIn("habilidade_EmpatiacomAnimais_val", self.fields)

    def test_derived_fields_are_separated_from_the_advantage_lists(self):
        last_discipline_bottom = float(self.widgets["disciplina_Vicissitude_val"]["/Rect"][1])
        derived_field_top = float(self.widgets["humanidade_sugerida"]["/Rect"][3])
        self.assertGreaterEqual(last_discipline_bottom - derived_field_top, 10)

    def test_blood_and_willpower_labels_have_header_spacing_and_full_names(self):
        page = self.reader.pages[1]
        page_text = page.extract_text()
        self.assertIn("Força de Vontade Permanente", page_text)
        self.assertIn("Força de Vontade Temporária", page_text)
        self.assertNotIn("FV permanente", page_text)
        self.assertNotIn("FV temporaria", page_text)

        header_bottom = float(page.mediabox.height) - 25 * mm - 15
        current_blood_top = float(self.widgets["sangue_atual"]["/Rect"][3])
        self.assertGreaterEqual(header_bottom - current_blood_top, 7)

    def test_blood_and_willpower_controls_fit_and_have_readable_spacing(self):
        page = self.reader.pages[1]
        section_width = (float(page.mediabox.width) - 2 * 12 * mm - 4 * mm) / 2
        section_right = 12 * mm + section_width

        for name in [
            *(f"sangue_box_{index}" for index in range(1, 21)),
            *(f"fv_box_{index}" for index in range(1, 11)),
        ]:
            with self.subTest(field=name):
                self.assertLessEqual(float(self.widgets[name]["/Rect"][2]), section_right)

        row_names = [
            "sangue_atual",
            "sangue_max",
            "sangue_turno",
            "forca_vontade_perm",
            "forca_vontade_temp",
        ]
        for current, following in zip(row_names, row_names[1:]):
            current_bottom = float(self.widgets[current]["/Rect"][1])
            following_top = float(self.widgets[following]["/Rect"][3])
            self.assertGreaterEqual(current_bottom - following_top, 9)

        section_top = float(page.mediabox.height) - 25 * mm
        first_checkbox_top = float(self.widgets["sangue_box_1"]["/Rect"][3])
        self.assertGreaterEqual(section_top - first_checkbox_top, 54)

    def test_health_damage_headers_and_columns_stay_inside_their_section(self):
        page = self.reader.pages[1]
        page_width = float(page.mediabox.width)
        section_width = (page_width - 2 * 12 * mm - 4 * mm) / 2
        section_left = 12 * mm + section_width + 4 * mm
        section_right = section_left + section_width

        for level, _ in data.HEALTH_LEVELS:
            for damage_type in ["cont", "letal", "agr"]:
                name = f"vitalidade_{safe_name(level)}_{damage_type}"
                with self.subTest(field=name):
                    left, _, right, _ = map(float, self.widgets[name]["/Rect"])
                    self.assertGreaterEqual(left, section_left)
                    self.assertLessEqual(right, section_right)

        current_color = None
        current_matrix = None
        headers = {}
        stream = ContentStream(page.get_contents(), self.reader)
        for operands, operator in stream.operations:
            if operator == b"rg":
                current_color = tuple(float(value) for value in operands)
            elif operator == b"Tm":
                current_matrix = tuple(float(value) for value in operands)
            elif operator == b"Tj" and str(operands[0]) in {"Cont.", "Letal", "Agr."}:
                headers[str(operands[0])] = (current_color, current_matrix)

        self.assertEqual({"Cont.", "Letal", "Agr."}, set(headers))
        section_top = float(page.mediabox.height) - 25 * mm
        for color, matrix in headers.values():
            self.assertEqual((1.0, 1.0, 1.0), color)
            self.assertGreater(matrix[4], section_left)
            self.assertLess(matrix[4], section_right)
            self.assertGreater(matrix[5], section_top - 15)
            self.assertLess(matrix[5], section_top)

    def test_combat_columns_use_the_available_width_with_clear_gaps(self):
        first_row = [self.widgets[f"arma_1_{index}"] for index in range(1, 8)]
        for current, following in zip(first_row, first_row[1:]):
            current_right = float(current["/Rect"][2])
            following_left = float(following["/Rect"][0])
            self.assertGreaterEqual(following_left - current_right, 4)

        alcance_right = float(self.widgets["arma_1_4"]["/Rect"][2])
        cadence_left = float(self.widgets["arma_1_5"]["/Rect"][0])
        self.assertGreaterEqual(cadence_left - alcance_right, 4)

        page_right = float(self.reader.pages[1].mediabox.width) - 12 * mm
        notes_right = float(self.widgets["arma_1_7"]["/Rect"][2])
        self.assertLessEqual(notes_right, page_right)
        self.assertLessEqual(page_right - notes_right, 3)

    def test_dropdowns_expose_the_complete_supported_options(self):
        self.assertEqual(
            [" ", *data.CHARACTER_TYPES],
            [str(option) for option in self.fields["tipo_personagem"]["/Opt"]],
        )
        self.assertEqual(
            [" ", *data.CLANS],
            [str(option) for option in self.fields["cla"]["/Opt"]],
        )
        self.assertEqual(
            [" ", *data.GENERATION_OPTIONS],
            [str(option) for option in self.fields["geracao"]["/Opt"]],
        )

    def test_identity_dropdowns_start_blank(self):
        for name in [
            "tipo_personagem",
            "cla",
            "geracao",
            "natureza",
            "comportamento",
            "moralidade_tipo",
        ]:
            with self.subTest(field=name):
                self.assertEqual("", str(self.fields[name].get("/V", "")).strip())

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
