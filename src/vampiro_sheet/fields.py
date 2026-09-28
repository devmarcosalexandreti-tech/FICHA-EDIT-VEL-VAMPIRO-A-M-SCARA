"""AcroForm helper functions."""

from reportlab.lib import colors

from .layout import INK, LIGHT, MID, RED, label


def text(
    c,
    name,
    x,
    y,
    w,
    h=14,
    value="",
    size=8,
    multiline=False,
    tooltip=None,
    readonly=False,
    maxlen=None,
):
    flags = []
    if multiline:
        flags.append("multiline")
    if readonly:
        flags.append("readOnly")
    c.acroForm.textfield(
        name=name,
        tooltip=tooltip or name,
        x=x,
        y=y,
        width=w,
        height=h,
        value=value,
        borderStyle="underlined",
        borderColor=LIGHT,
        fillColor=colors.white,
        textColor=INK,
        forceBorder=True,
        fontName="Helvetica",
        fontSize=size,
        fieldFlags=" ".join(flags),
        maxlen=maxlen or (4000 if multiline else 200),
    )


def text_labeled(
    c,
    name,
    label_text,
    x,
    y,
    w,
    h=14,
    size=8,
    multiline=False,
    readonly=False,
    label_gap=2,
):
    label(c, label_text, x, y + h + label_gap)
    text(
        c,
        name,
        x,
        y,
        w,
        h,
        size=size,
        multiline=multiline,
        tooltip=label_text,
        readonly=readonly,
    )


def choice(c, name, label_text, options, x, y, w, h=14, value=None, allow_blank=False):
    label(c, label_text, x, y + h + 2)
    field_options = [" ", *options] if allow_blank else options
    selected_value = " " if allow_blank and value is None else (value or options[0])
    c.acroForm.choice(
        name=name,
        tooltip=label_text,
        x=x,
        y=y,
        width=w,
        height=h,
        options=field_options,
        value=selected_value,
        borderColor=LIGHT,
        fillColor=colors.white,
        textColor=INK,
        forceBorder=True,
        fontName="Helvetica",
        fontSize=8,
    )


def checkbox(c, name, x, y, size=8, checked=False, tooltip=None):
    c.acroForm.checkbox(
        name=name,
        tooltip=tooltip or name,
        x=x,
        y=y,
        size=size,
        buttonStyle="check",
        borderColor=MID,
        fillColor=colors.white,
        textColor=RED,
        checked=checked,
        forceBorder=True,
        fieldFlags="",
    )


def dots(c, base_name, x, y, count=5, size=7, tooltip=None, value=0):
    for i in range(1, count + 1):
        checkbox(
            c,
            f"{base_name}_{i}",
            x + (i - 1) * (size + 2),
            y,
            size=size,
            checked=i <= value,
            tooltip=f"{tooltip or base_name}: ponto {i}",
        )


def trait_row(c, label_text, base_name, x, y, w_label=63, count=5, value=0):
    c.setFillColor(INK)
    c.setFont("Helvetica", 7.2)
    c.drawString(x, y + 1.5, label_text)
    dots(c, base_name, x + w_label, y - 1, count=count, tooltip=label_text, value=value)


def numeric(c, name, x, y, w=26, h=12, value="", tooltip=None, readonly=False):
    text(
        c,
        name,
        x,
        y,
        w,
        h,
        value=value,
        size=7,
        tooltip=tooltip,
        readonly=readonly,
    )
