"""Post-processing for the interactive AcroForm document."""

import re
import tempfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, TextStringObject

DEFAULT_JAVASCRIPT = Path(__file__).with_name("calculations.js")

DOT_FIELD_PATTERN = re.compile(r"^((?:atributo|habilidade)_.+)_([1-5])$")
HEALTH_FIELD_PATTERN = re.compile(r"^(vitalidade_.+)_(cont|letal|agr)$")
NUMERIC_FIELD_PATTERN = re.compile(
    r"(^qd_[1-8]_3$|_val$|_nivel$|_(?:total|gasto)$|^bonus_base$|"
    r"^sangue_atual$|^forca_vontade_(?:perm|temp)$)"
)

RECALCULATE_ACTION = 'app.setTimeOut("recalcVampiro()", 10);'
NUMERIC_VALIDATION_ACTION = (
    r'if (event.value !== "" && !/^\d+$/.test(String(event.value))) {'
    ' app.alert("Informe um numero inteiro nao negativo.");'
    " event.rc = false;"
    f"}} else {{ {RECALCULATE_ACTION} }}"
)
ATTRIBUTE_NUMERIC_VALIDATION_ACTION = (
    r"if (!/^\d+$/.test(String(event.value)) || Number(event.value) < 1) {"
    ' app.alert("Atributos devem ter valor minimo 1.");'
    " event.rc = false;"
    f"}} else {{ {RECALCULATE_ACTION} }}"
)


def field_action(field_name: str, field_type: str) -> tuple[str, str] | None:
    """Return the additional-action event and script for a writable field."""
    health_match = HEALTH_FIELD_PATTERN.match(field_name)
    if health_match:
        base_name, damage_type = health_match.groups()
        return "/U", f'syncHealthDamage("{base_name}", "{damage_type}");'

    dot_match = DOT_FIELD_PATTERN.match(field_name)
    if dot_match:
        base_name, index = dot_match.groups()
        return "/U", f'syncDotsFromClick("{base_name}", {index}, 5);'

    if field_type == "/Tx" and field_name.startswith("atributo_") and field_name.endswith("_val"):
        return "/V", ATTRIBUTE_NUMERIC_VALIDATION_ACTION
    if field_type == "/Tx" and NUMERIC_FIELD_PATTERN.search(field_name):
        return "/V", NUMERIC_VALIDATION_ACTION
    if field_type in {"/Tx", "/Ch"}:
        return "/V", RECALCULATE_ACTION
    return None


def _javascript_action(code: str) -> DictionaryObject:
    return DictionaryObject(
        {
            NameObject("/S"): NameObject("/JavaScript"),
            NameObject("/JS"): TextStringObject(code),
        }
    )


def _add_field_actions(writer: PdfWriter) -> None:
    for page in writer.pages:
        page[NameObject("/Tabs")] = NameObject("/S")
        for annotation_ref in page.get("/Annots", []):
            annotation = annotation_ref.get_object()
            if int(annotation.get("/Ff", 0)) & 1:
                continue

            action = field_action(
                str(annotation.get("/T", "")),
                str(annotation.get("/FT", "")),
            )
            if action is None:
                continue

            event_name, code = action
            annotation[NameObject("/AA")] = DictionaryObject(
                {NameObject(event_name): _javascript_action(code)}
            )


def _write_atomic(writer: PdfWriter, output_pdf: Path) -> None:
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    temporary_output = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", suffix=".pdf", dir=output_pdf.parent, delete=False
        ) as temporary_file:
            temporary_output = Path(temporary_file.name)
            writer.write(temporary_file)
        temporary_output.replace(output_pdf)
    finally:
        if temporary_output is not None and temporary_output.exists():
            temporary_output.unlink()


def postprocess_pdf(
    input_pdf: Path,
    output_pdf: Path,
    javascript_path: Path = DEFAULT_JAVASCRIPT,
) -> None:
    """Attach form behavior and write the final PDF atomically."""
    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.set_need_appearances_writer(True)
    writer.root_object[NameObject("/Lang")] = TextStringObject("pt-BR")
    _add_field_actions(writer)
    writer.add_js(javascript_path.read_text(encoding="ascii"))
    _write_atomic(writer, output_pdf)
