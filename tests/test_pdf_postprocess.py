import tempfile
import unittest
from pathlib import Path

from reportlab.pdfgen import canvas

from src.vampiro_sheet.build import add_javascript
from src.vampiro_sheet.pdf_postprocess import field_action, postprocess_pdf


class FieldActionTests(unittest.TestCase):
    def test_legacy_add_javascript_symbol_is_preserved(self):
        self.assertIs(add_javascript, postprocess_pdf)

    def test_trait_dot_synchronizes_on_mouse_up(self):
        event, script = field_action("habilidade_Briga_3", "/Btn")
        self.assertEqual("/U", event)
        self.assertEqual('syncDotsFromClick("habilidade_Briga", 3, 5);', script)

    def test_health_damage_synchronizes_on_mouse_up(self):
        event, script = field_action("vitalidade_Escoriado_letal", "/Btn")
        self.assertEqual("/U", event)
        self.assertEqual(
            'syncHealthDamage("vitalidade_Escoriado", "letal");',
            script,
        )

    def test_numeric_text_field_validates_before_recalculation(self):
        event, script = field_action("habilidade_Briga_val", "/Tx")
        self.assertEqual("/V", event)
        self.assertIn("event.rc = false", script)
        self.assertIn("recalcVampiro", script)

    def test_attribute_numeric_field_requires_minimum_one(self):
        event, script = field_action("atributo_Fisicos_Forca_val", "/Tx")
        self.assertEqual("/V", event)
        self.assertIn("Number(event.value) < 1", script)
        self.assertIn("event.rc = false", script)

    def test_regular_text_field_only_recalculates(self):
        event, script = field_action("nome_personagem", "/Tx")
        self.assertEqual("/V", event)
        self.assertNotIn("event.rc", script)
        self.assertIn("recalcVampiro", script)

    def test_unrelated_button_has_no_action(self):
        self.assertIsNone(field_action("qd_1_aprovado", "/Btn"))

    def test_missing_input_fails_without_creating_output(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            output = temporary / "output.pdf"
            with self.assertRaises(FileNotFoundError):
                postprocess_pdf(temporary / "missing.pdf", output)
            self.assertFalse(output.exists())

    def test_missing_javascript_fails_without_creating_output(self):
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            draft = temporary / "draft.pdf"
            output = temporary / "output.pdf"
            document = canvas.Canvas(str(draft))
            document.drawString(20, 20, "draft")
            document.save()

            with self.assertRaises(FileNotFoundError):
                postprocess_pdf(draft, output, temporary / "missing.js")
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
