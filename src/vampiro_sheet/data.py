"""System data used by the sheet generator.

The labels intentionally avoid accents so the source remains portable in
PDF toolchains that still default to WinAnsi encodings.
"""

CHARACTER_TYPES = ["Vampiro jogador", "Mortal", "Carnical", "Antagonista"]

CLANS = [
    "Assamita",
    "Brujah",
    "Gangrel",
    "Giovanni",
    "Lasombra",
    "Malkaviano",
    "Nosferatu",
    "Ravnos",
    "Seguidores de Set",
    "Toreador",
    "Tremere",
    "Tzimisce",
    "Ventrue",
    "Caitiff",
    "Mortal/Carnical",
    "Outro antagonista",
]

ARCHETYPES = [
    "Excentrico",
    "Arquiteto",
    "Autocrata",
    "Bon Vivant",
    "Cacador de Emocoes",
    "Celebrante",
    "Competidor",
    "Conformista",
    "Crianca",
    "Diretor",
    "Durao",
    "Esperto",
    "Fanatico",
    "Filantropo",
    "Galante",
    "Gozador",
    "Juiz",
    "Martir",
    "Masoquista",
    "Monstro",
    "Pedagogo",
    "Penitente",
    "Perfeccionista",
    "Ranzinza",
    "Rebelde",
    "Sobrevivente",
    "Solitario",
    "Tradicionalista",
    "Valentao",
    "Visionario",
]

ATTRIBUTES = {
    "Fisicos": ["Forca", "Destreza", "Vigor"],
    "Sociais": ["Carisma", "Manipulacao", "Aparencia"],
    "Mentais": ["Percepcao", "Inteligencia", "Raciocinio"],
}

ABILITIES = {
    "Talentos": [
        "Prontidao",
        "Esportes",
        "Briga",
        "Esquiva",
        "Empatia",
        "Expressao",
        "Intimidacao",
        "Lideranca",
        "Manha",
        "Labia",
    ],
    "Pericias": [
        "Empatia com Animais",
        "Oficios",
        "Conducao",
        "Etiqueta",
        "Armas de Fogo",
        "Armas Brancas",
        "Performance",
        "Seguranca",
        "Furtividade",
        "Sobrevivencia",
    ],
    "Conhecimentos": [
        "Academicos",
        "Computador",
        "Financas",
        "Investigacao",
        "Direito",
        "Linguistica",
        "Medicina",
        "Ocultismo",
        "Politica",
        "Ciencia",
    ],
}

DISCIPLINES = [
    "Animalismo",
    "Auspicios",
    "Rapidez",
    "Demencia",
    "Dominacao",
    "Fortitude",
    "Metamorfose",
    "Necromancia",
    "Tenebrosidade",
    "Ofuscacao",
    "Potencia",
    "Presenca",
    "Quietus",
    "Quimerismo",
    "Serpentis",
    "Taumaturgia",
    "Vicissitude",
]

CLAN_DISCIPLINES = {
    "Assamita": "Rapidez, Ofuscacao, Quietus",
    "Brujah": "Rapidez, Potencia, Presenca",
    "Gangrel": "Animalismo, Fortitude, Metamorfose",
    "Giovanni": "Dominacao, Necromancia, Potencia",
    "Lasombra": "Dominacao, Tenebrosidade, Potencia",
    "Malkaviano": "Auspicios, Demencia, Ofuscacao",
    "Nosferatu": "Animalismo, Ofuscacao, Potencia",
    "Ravnos": "Animalismo, Quimerismo, Fortitude",
    "Seguidores de Set": "Ofuscacao, Presenca, Serpentis",
    "Toreador": "Auspicios, Rapidez, Presenca",
    "Tremere": "Auspicios, Dominacao, Taumaturgia",
    "Tzimisce": "Animalismo, Auspicios, Vicissitude",
    "Ventrue": "Dominacao, Fortitude, Presenca",
    "Caitiff": "Qualquer Disciplina, com aprovacao do Narrador",
}

BACKGROUNDS = [
    "Aliados",
    "Contatos",
    "Fama",
    "Geracao",
    "Influencia",
    "Lacaios",
    "Mentor",
    "Rebanho",
    "Recursos",
    "Status",
]

VIRTUES = ["Consciencia/Conviccao", "Autocontrole/Instinto", "Coragem"]

GENERATION_TABLE = {
    "3": ("10", "indef.", "indef."),
    "4": ("9", "50", "10"),
    "5": ("8", "40", "8"),
    "6": ("7", "30", "6"),
    "7": ("6", "20", "4"),
    "8": ("5", "15", "3"),
    "9": ("5", "14", "2"),
    "10": ("5", "13", "1"),
    "11": ("5", "12", "1"),
    "12": ("5", "11", "1"),
    "13+": ("5", "10", "1"),
    "14": ("5", "10/8 util", "1"),
}

GENERATION_OPTIONS = list(GENERATION_TABLE.keys())

HEALTH_LEVELS = [
    ("Escoriado", "0"),
    ("Machucado", "-1"),
    ("Ferido", "-1"),
    ("Ferido gravemente", "-2"),
    ("Espancado", "-2"),
    ("Aleijado", "-5"),
    ("Incapacitado", "Imovel"),
]

BONUS_COSTS = [
    ("Atributo", "5 por ponto"),
    ("Habilidade", "2 por ponto"),
    ("Disciplina", "7 por ponto"),
    ("Antecedente", "1 por ponto"),
    ("Virtude", "2 por ponto"),
    ("Humanidade", "1 por ponto"),
    ("Forca de Vontade", "1 por ponto"),
]

XP_COSTS = [
    ("Nova Habilidade", "3"),
    ("Nova Trilha/Linha", "7"),
    ("Nova Disciplina", "10"),
    ("Atributo", "nivel atual x 4"),
    ("Habilidade", "nivel atual x 2"),
    ("Disciplina do Cla", "nivel atual x 5"),
    ("Outra Disciplina", "nivel atual x 7"),
    ("Disciplina Caitiff", "nivel atual x 6"),
    ("Trilha/Linha secundaria", "nivel atual x 4"),
    ("Virtude", "nivel atual x 2"),
    ("Humanidade", "nivel atual x 2"),
    ("Forca de Vontade", "nivel atual"),
]

MERITS_FLAWS = [
    "Sentido Agucado",
    "Ambidestro",
    "Ingerir Comida",
    "Equilibrio Perfeito",
    "Rubor de Saude",
    "Voz Encantadora",
    "Temerario",
    "Digestao Eficiente",
    "Corpo Grande",
    "Bom Senso",
    "Concentracao",
    "Codigo de Honra",
    "Memoria Eidetica",
    "Sono Leve",
    "Linguista Nato",
    "Temperamento Calmo",
    "Vontade de Ferro",
    "Senhor de Prestigio",
    "Lider Nato",
    "Divida de Gratidao",
    "Medium",
    "Resistencia a Magia",
    "Habilidade Oracular",
    "Mentor Espiritual",
    "Imunidade ao Laco de Sangue",
    "Sorte",
    "Amor Verdadeiro",
    "Nove Vidas",
    "Fe Verdadeira",
    "Cheiro do Tumulo",
    "14a Geracao",
    "Sangue Fraco",
    "Imagem sem Reflexo",
    "Presenca Sinistra",
    "Repulsa a Cruzes",
    "Assombrado",
    "Futuro Negro",
    "Sensibilidade a Luz",
]
