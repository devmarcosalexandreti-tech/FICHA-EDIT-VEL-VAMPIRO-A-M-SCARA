import sys
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "dist" / "ficha_vampiro_interativa.pdf"

REQUIRED_FIELDS = [
    "tipo_personagem",
    "cla",
    "geracao",
    "moralidade_tipo",
    "humanidade_sugerida",
    "forca_vontade_sugerida",
    "sangue_max",
    "sangue_turno",
    "sangue_max_resumo",
    "sangue_turno_resumo",
    "fraqueza_cla",
    "taumaturgia_trilhas",
    "necromancia_linhas",
    "defeitos_total",
    "bonus_saldo",
    "xp_disponivel",
    "avisos_criacao",
    "aprovacao_narrador",
]

READ_ONLY_FIELDS = [
    "humanidade_sugerida",
    "forca_vontade_sugerida",
    "limite_caracteristica",
    "sangue_max_resumo",
    "sangue_turno_resumo",
    "avisos_criacao",
    "defeitos_aviso",
    "bonus_total",
    "bonus_saldo",
    "xp_disponivel",
    "idiomas_sugeridos",
]


def main() -> int:
    if not PDF.exists():
        print(f"missing: {PDF}")
        return 1

    reader = PdfReader(str(PDF))
    fields = reader.get_fields() or {}
    failures = []

    if len(reader.pages) != 5:
        failures.append(f"expected 5 pages, found {len(reader.pages)}")
    if "/AcroForm" not in reader.trailer["/Root"]:
        failures.append("missing AcroForm")
    if len(fields) < 400:
        failures.append(f"expected at least 400 fields, found {len(fields)}")
    for name in REQUIRED_FIELDS:
        if name not in fields:
            failures.append(f"missing field: {name}")
    root = reader.trailer["/Root"]
    names = root.get("/Names", {})
    javascript_tree = names.get("/JavaScript") if names else None
    if not javascript_tree:
        failures.append("missing document JavaScript name tree")
    else:
        javascript_names = javascript_tree.get("/Names", [])
        scripts = [
            str(javascript_names[index].get_object().get("/JS", ""))
            for index in range(1, len(javascript_names), 2)
        ]
        if not any("recalcVampiro" in script for script in scripts):
            failures.append("missing recalcVampiro document JavaScript")
        if any("setInterval" in script for script in scripts):
            failures.append("document JavaScript still uses polling")

    terminal_names = [str(field.get_object().get("/T")) for field in root["/AcroForm"]["/Fields"]]
    duplicates = {name: count for name, count in Counter(terminal_names).items() if count > 1}
    if duplicates:
        failures.append(f"duplicate terminal fields: {duplicates}")

    required_buttons = [
        name
        for name, field in fields.items()
        if field.get("/FT") == "/Btn" and int(field.get("/Ff", 0)) & 2
    ]
    if required_buttons:
        failures.append(f"checkboxes incorrectly required: {len(required_buttons)}")

    for name in READ_ONLY_FIELDS:
        if name in fields and not int(fields[name].get("/Ff", 0)) & 1:
            failures.append(f"calculated field is editable: {name}")

    if str(root.get("/Lang")) != "pt-BR":
        failures.append("document language is not pt-BR")
    if any(page.get("/Tabs") != "/S" for page in reader.pages):
        failures.append("page tab order is not structural")

    dot_actions = 0
    for page in reader.pages:
        for annotation_ref in page.get("/Annots", []):
            annotation = annotation_ref.get_object()
            name = str(annotation.get("/T", ""))
            if name.startswith(("atributo_", "habilidade_")) and annotation.get("/AA"):
                dot_actions += 1
    if dot_actions < 190:
        failures.append(f"missing trait synchronization actions: found {dot_actions}")

    if failures:
        print("validation failed")
        for item in failures:
            print(f"- {item}")
        return 1

    print("validation ok")
    print(f"pages: {len(reader.pages)}")
    print(f"fields: {len(fields)}")
    print("acroform: yes")
    print("javascript: yes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
