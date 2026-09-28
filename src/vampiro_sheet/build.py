"""Build the interactive PDF character sheet."""

from pathlib import Path

from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from . import data
from .fields import checkbox, choice, numeric, text, text_labeled, trait_row
from .layout import (
    GAP,
    INK,
    MARGIN,
    PAGE_H,
    PAGE_SIZE,
    PAGE_W,
    RED,
    columns,
    label,
    section,
    small_note,
    title,
)
from .pdf_postprocess import postprocess_pdf as add_javascript

SOURCE_ROOT = Path(__file__).resolve().parents[2]
ROOT = SOURCE_ROOT if (SOURCE_ROOT / "src" / "vampiro_sheet").exists() else Path.cwd()
DIST = ROOT / "dist"
BUILD = ROOT / "build"


def _safe(name: str) -> str:
    return "".join(ch for ch in name if ch.isalnum())


def draw_trait_block(c, title_text, traits, x, y, w, prefix, minimum=0):
    h = 19 + len(traits) * 13
    section(c, title_text, x, y, w, h)
    yy = y - 28
    for trait in traits:
        safe = _safe(trait)
        trait_row(c, trait, f"{prefix}_{safe}", x + 7, yy, value=minimum)
        numeric(
            c,
            f"{prefix}_{safe}_val",
            x + w - 30,
            yy - 2,
            21,
            10,
            value=str(minimum) if minimum else "",
            tooltip=f"{trait}: valor numerico",
        )
        yy -= 13


def draw_identity(c):
    title(c, "Identidade e Caracteristicas", 1)
    top = PAGE_H - 25 * mm
    col_w = (PAGE_W - 2 * MARGIN - 2 * GAP) / 3
    x1, x2, x3 = MARGIN, MARGIN + col_w + GAP, MARGIN + 2 * (col_w + GAP)
    choice(
        c,
        "tipo_personagem",
        "Tipo",
        data.CHARACTER_TYPES,
        x1,
        top - 14,
        col_w,
        allow_blank=True,
    )
    text_labeled(c, "nome_personagem", "Nome", x2, top - 14, col_w)
    text_labeled(c, "jogador", "Jogador", x3, top - 14, col_w)

    y = top - 36
    text_labeled(c, "cronica", "Cronica", x1, y, col_w)
    choice(c, "cla", "Cla / origem", data.CLANS, x2, y, col_w, allow_blank=True)
    choice(c, "geracao", "Geracao", data.GENERATION_OPTIONS, x3, y, col_w, allow_blank=True)

    y -= 36
    text_labeled(c, "conceito", "Conceito", x1, y, col_w)
    choice(c, "natureza", "Natureza", data.ARCHETYPES, x2, y, col_w, allow_blank=True)
    choice(
        c,
        "comportamento",
        "Comportamento",
        data.ARCHETYPES,
        x3,
        y,
        col_w,
        allow_blank=True,
    )

    y -= 36
    text_labeled(c, "senhor", "Senhor / criador", x1, y, col_w)
    text_labeled(c, "refugio", "Refugio", x2, y, col_w)
    choice(
        c,
        "moralidade_tipo",
        "Moralidade",
        ["Humanidade", "Trilha"],
        x3,
        y,
        col_w,
        allow_blank=True,
    )

    y -= 28
    attr_y = y
    for i, (group, traits) in enumerate(data.ATTRIBUTES.items()):
        x, w = columns(3)[i]
        draw_trait_block(
            c,
            group,
            traits,
            x,
            attr_y,
            w,
            f"atributo_{_safe(group)}",
            minimum=1,
        )

    abil_y = attr_y - 67
    for i, (group, traits) in enumerate(data.ABILITIES.items()):
        x, w = columns(3)[i]
        draw_trait_block(c, group, traits, x, abil_y, w, "habilidade")

    adv_y = 100 * mm
    x, w = MARGIN, PAGE_W - 2 * MARGIN
    section(c, "Vantagens e Derivados", x, adv_y, w, 83 * mm)
    third = (w - 20) / 3
    draw_trait_list(c, "Disciplinas", data.DISCIPLINES, x + 7, adv_y - 24, third, "disciplina")
    draw_trait_list(
        c, "Antecedentes", data.BACKGROUNDS, x + 10 + third, adv_y - 24, third, "antecedente"
    )
    draw_trait_list(c, "Virtudes", data.VIRTUES, x + 13 + 2 * third, adv_y - 24, third, "virtude")

    bottom_y = 19 * mm
    for i, (fname, lab) in enumerate(
        [
            ("humanidade_sugerida", "Humanidade/Trilha sugerida"),
            ("forca_vontade_sugerida", "Forca de Vontade sugerida"),
            ("limite_caracteristica", "Limite Caracteristica"),
            ("sangue_max_resumo", "Sangue max."),
            ("sangue_turno_resumo", "Sangue/turno"),
        ]
    ):
        xx = MARGIN + i * 34 * mm
        text_labeled(c, fname, lab, xx, bottom_y, 30 * mm, h=12, readonly=True)


def draw_trait_list(c, title_text, traits, x, y, w, prefix):
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x, y, title_text)
    yy = y - 13
    for trait in traits:
        safe = _safe(trait)
        c.setFillColor(INK)
        c.setFont("Helvetica", 6.7)
        c.drawString(x, yy + 1, trait[:25])
        text(
            c,
            f"{prefix}_{safe}_val",
            x + w - 18,
            yy - 2,
            16,
            10,
            size=6,
            tooltip=f"{trait}: valor numerico",
        )
        yy -= 11


def draw_resources(c):
    title(c, "Recursos de Jogo", 2)
    x1, w1 = MARGIN, (PAGE_W - 2 * MARGIN - GAP) / 2
    x2 = x1 + w1 + GAP
    top = PAGE_H - 25 * mm

    section(c, "Sangue e Vontade", x1, top, w1, 70 * mm)
    fields = [
        ("sangue_atual", "Sangue atual"),
        ("sangue_max", "Sangue max."),
        ("sangue_turno", "Gasto/turno"),
        ("forca_vontade_perm", "FV permanente"),
        ("forca_vontade_temp", "FV temporaria"),
    ]
    yy = top - 28
    for name, lab in fields:
        text_labeled(c, name, lab, x1 + 7, yy, 38 * mm, h=12)
        yy -= 18
    small_note(
        c,
        "Pontos iniciais de sangue: jogue 1d10. Carnicais e antagonistas podem usar campos manuais.",
        x1 + 58 * mm,
        top - 29,
        w1 - 62 * mm,
    )
    for i in range(20):
        checkbox(
            c,
            f"sangue_box_{i + 1}",
            x1 + 58 * mm + (i % 10) * 11,
            top - 52 - (i // 10) * 13,
            size=8,
        )
    for i in range(10):
        checkbox(c, f"fv_box_{i + 1}", x1 + 58 * mm + i * 11, top - 83, size=8)

    section(c, "Vitalidade", x2, top, w1, 70 * mm)
    yy = top - 28
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(x2 + 67 * mm, yy + 13, "Cont.")
    c.drawString(x2 + 82 * mm, yy + 13, "Letal")
    c.drawString(x2 + 97 * mm, yy + 13, "Agr.")
    for level, penalty in data.HEALTH_LEVELS:
        c.setFont("Helvetica", 7)
        c.drawString(x2 + 7, yy + 1, f"{level} ({penalty})")
        checkbox(c, f"vitalidade_{_safe(level)}_cont", x2 + 68 * mm, yy - 2, size=8)
        checkbox(c, f"vitalidade_{_safe(level)}_letal", x2 + 83 * mm, yy - 2, size=8)
        checkbox(c, f"vitalidade_{_safe(level)}_agr", x2 + 98 * mm, yy - 2, size=8)
        yy -= 13

    section(c, "Combate", x1, top - 76 * mm, PAGE_W - 2 * MARGIN, 72 * mm)
    headers = ["Arma", "Dif.", "Dano", "Alcance", "Cad.", "Pente", "Notas"]
    widths = [45, 16, 22, 22, 18, 18, 56]
    table_x = x1 + 7
    yy = top - 101 * mm
    xx = table_x
    for h, ww in zip(headers, widths):
        label(c, h, xx, yy + 15)
        xx += ww
    for r in range(5):
        xx = table_x
        for i, ww in enumerate(widths):
            text(c, f"arma_{r + 1}_{i + 1}", xx, yy, ww - 2, 12, size=6)
            xx += ww
        yy -= 15

    section(c, "Equipamentos, Fraquezas e Condicoes", x1, 84 * mm, PAGE_W - 2 * MARGIN, 62 * mm)
    text_labeled(
        c,
        "equipamentos",
        "Pertences, armaduras, veiculos e recursos",
        x1 + 7,
        34 * mm,
        83 * mm,
        h=38,
        multiline=True,
    )
    text_labeled(
        c,
        "fraqueza_cla",
        "Fraqueza de cla / especie",
        x1 + 97 * mm,
        34 * mm,
        83 * mm,
        h=38,
        multiline=True,
    )


def draw_disciplines(c):
    title(c, "Disciplinas e Poderes", 3)
    top = PAGE_H - 25 * mm
    section(c, "Disciplinas", MARGIN, top, PAGE_W - 2 * MARGIN, 92 * mm)
    col_w = (PAGE_W - 2 * MARGIN - 2 * GAP - 18) / 3
    for idx, disc in enumerate(data.DISCIPLINES):
        col = idx % 3
        row = idx // 3
        x = MARGIN + 7 + col * (col_w + GAP)
        y = top - 28 - row * 13
        c.setFont("Helvetica", 7)
        c.drawString(x, y + 1, disc)
        text(c, f"disciplina_detalhe_{_safe(disc)}_nivel", x + col_w - 16, y - 2, 14, 10, size=6)
    text_labeled(
        c,
        "poderes_disciplinas",
        "Poderes, custos, testes e observacoes",
        MARGIN + 7,
        top - 129,
        PAGE_W - 2 * MARGIN - 14,
        h=72,
        multiline=True,
    )

    y2 = 124 * mm
    section(c, "Taumaturgia e Necromancia", MARGIN, y2, PAGE_W - 2 * MARGIN, 65 * mm)
    half = (PAGE_W - 2 * MARGIN - 20) / 2
    text_labeled(
        c,
        "taumaturgia_trilhas",
        "Taumaturgia: trilhas, niveis e rituais",
        MARGIN + 7,
        y2 - 58 * mm,
        half,
        h=47,
        multiline=True,
    )
    text_labeled(
        c,
        "necromancia_linhas",
        "Necromancia: linhas, niveis e rituais",
        MARGIN + 13 + half,
        y2 - 58 * mm,
        half,
        h=47,
        multiline=True,
    )

    section(c, "Especializacoes e Perturbacoes", MARGIN, 54 * mm, PAGE_W - 2 * MARGIN, 34 * mm)
    text_labeled(
        c, "especializacoes", "Especializacoes", MARGIN + 7, 22 * mm, 83 * mm, h=22, multiline=True
    )
    text_labeled(
        c,
        "perturbacoes",
        "Perturbacoes / compulsos / condicoes",
        MARGIN + 97 * mm,
        22 * mm,
        83 * mm,
        h=22,
        multiline=True,
    )


def draw_story(c):
    title(c, "Historia e Relacoes", 4)
    top = PAGE_H - 25 * mm
    section(c, "Preludio e Historia", MARGIN, top, PAGE_W - 2 * MARGIN, 78 * mm)
    text_labeled(
        c,
        "historia",
        "Historia, Abraco, motivacoes e vida mortal",
        MARGIN + 7,
        top - 69 * mm,
        PAGE_W - 2 * MARGIN - 14,
        h=58,
        multiline=True,
    )

    section(c, "Rede de Personagens", MARGIN, 184 * mm, PAGE_W - 2 * MARGIN, 70 * mm)
    headers = ["Nome", "Tipo", "Relacao", "Notas"]
    widths = [45, 30, 40, 80]
    yy = 164 * mm
    for r in range(6):
        xx = MARGIN + 7
        for i, ww in enumerate(widths):
            if r == 0:
                label(c, headers[i], xx, yy + 15)
            text(c, f"relacao_{r + 1}_{i + 1}", xx, yy, ww - 2, 12, size=6)
            xx += ww
        yy -= 15

    section(c, "Refugio, Caca e Identidades", MARGIN, 91 * mm, PAGE_W - 2 * MARGIN, 66 * mm)
    third = (PAGE_W - 2 * MARGIN - 24) / 3
    text_labeled(
        c,
        "territorio_caca",
        "Territorio de caca / predilecao",
        MARGIN + 7,
        36 * mm,
        third,
        h=42,
        multiline=True,
    )
    text_labeled(
        c,
        "lacaios_rebanho",
        "Rebanho, lacaios, carnicais e animais",
        MARGIN + 12 + third,
        36 * mm,
        third,
        h=42,
        multiline=True,
    )
    text_labeled(
        c,
        "identidades",
        "Identidades, mascara publica e documentos",
        MARGIN + 17 + 2 * third,
        36 * mm,
        third,
        h=42,
        multiline=True,
    )


def draw_progress(c):
    title(c, "Criacao e Progresso", 5)
    top = PAGE_H - 25 * mm
    section(c, "Auditoria de Criacao", MARGIN, top, PAGE_W - 2 * MARGIN, 55 * mm)
    fields = [
        ("attr_fisicos_total", "Fisicos"),
        ("attr_sociais_total", "Sociais"),
        ("attr_mentais_total", "Mentais"),
        ("hab_talentos_total", "Talentos"),
        ("hab_pericias_total", "Pericias"),
        ("hab_conhecimentos_total", "Conhec."),
        ("disc_total", "Discip. 3"),
        ("ante_total", "Antec. 5"),
        ("virt_total", "Virt. 7"),
    ]
    for i, (name, lab) in enumerate(fields):
        x = MARGIN + 7 + (i % 5) * 36 * mm
        y = top - 26 - (i // 5) * 20
        text_labeled(c, name, lab, x, y, 26 * mm, h=11)
    text_labeled(
        c,
        "avisos_criacao",
        "Avisos automaticos",
        MARGIN + 7,
        top - 48 * mm,
        116 * mm,
        h=18,
        multiline=True,
        readonly=True,
    )
    text_labeled(
        c,
        "aprovacao_narrador",
        "Notas e aprovacao do Narrador",
        MARGIN + 126 * mm,
        top - 48 * mm,
        54 * mm,
        h=18,
        multiline=True,
    )

    section(c, "Qualidades e Defeitos", MARGIN, 215 * mm, PAGE_W - 2 * MARGIN, 85 * mm)
    headers = ["Nome", "Tipo", "Pts", "Aprov.", "Notas"]
    widths = [60, 24, 16, 18, 78]
    yy = 191 * mm
    for r in range(8):
        xx = MARGIN + 7
        for i, ww in enumerate(widths):
            if r == 0:
                label(c, headers[i], xx, yy + 15)
            if i == 3:
                checkbox(c, f"qd_{r + 1}_aprovado", xx + 4, yy + 1, size=8)
            else:
                text(c, f"qd_{r + 1}_{i + 1}", xx, yy, ww - 2, 12, size=6)
            xx += ww
        yy -= 15
    text_labeled(c, "defeitos_total", "Total Defeitos", MARGIN + 7, 93 * mm, 28 * mm, h=12)
    text_labeled(
        c,
        "defeitos_aviso",
        "Aviso Defeitos",
        MARGIN + 41 * mm,
        93 * mm,
        58 * mm,
        h=12,
        readonly=True,
    )

    section(c, "Bonus e Experiencia", MARGIN, 82 * mm, PAGE_W - 2 * MARGIN, 64 * mm)
    bonus = [
        ("bonus_base", "Bonus base", "15"),
        ("bonus_total", "Bonus total", ""),
        ("bonus_gasto", "Bonus gasto", ""),
        ("bonus_saldo", "Saldo", ""),
        ("xp_total", "XP total", ""),
        ("xp_gasto", "XP gasto", ""),
        ("xp_disponivel", "XP disponivel", ""),
        ("idiomas_sugeridos", "Idiomas por Linguistica", ""),
    ]
    for i, (name, lab, val) in enumerate(bonus):
        x = MARGIN + 7 + (i % 4) * 46 * mm
        y = 58 * mm - (i // 4) * 20
        label(c, lab, x, y + 14)
        text(
            c,
            name,
            x,
            y,
            34 * mm,
            12,
            value=val,
            size=7,
            tooltip=lab,
            readonly=name in {"bonus_total", "bonus_saldo", "xp_disponivel", "idiomas_sugeridos"},
        )

    xcost = MARGIN + 7
    ycost = 28 * mm
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(xcost, ycost + 22, "Custos de bonus")
    for i, (k, v) in enumerate(data.BONUS_COSTS):
        c.setFillColor(INK)
        c.setFont("Helvetica", 5.7)
        c.drawString(xcost + (i % 4) * 44 * mm, ycost + 12 - (i // 4) * 8, f"{k}: {v}")
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(xcost, ycost - 6, "Custos de experiencia")
    for i, (k, v) in enumerate(data.XP_COSTS):
        c.setFillColor(INK)
        c.setFont("Helvetica", 5.5)
        c.drawString(xcost + (i % 3) * 62 * mm, ycost - 16 - (i // 3) * 7, f"{k}: {v}")


def build(output: Path | None = None, work_dir: Path | None = None):
    final = Path(output) if output else DIST / "ficha_vampiro_interativa.pdf"
    draft_dir = Path(work_dir) if work_dir else BUILD
    final.parent.mkdir(parents=True, exist_ok=True)
    draft_dir.mkdir(parents=True, exist_ok=True)
    draft = draft_dir / "ficha_vampiro_interativa_draft.pdf"
    c = canvas.Canvas(str(draft), pagesize=PAGE_SIZE)
    c.setTitle("Ficha Interativa - Vampiro A Mascara 3e")
    c.setAuthor("Projeto Ficha Interativa")
    c.setSubject("Ficha preenchivel original para Vampiro: A Mascara 3e")
    for drawer in [draw_identity, draw_resources, draw_disciplines, draw_story, draw_progress]:
        drawer(c)
        c.showPage()
    c.save()
    add_javascript(draft, final)
    return final


if __name__ == "__main__":
    print(build())
