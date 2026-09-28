var previousCharacterType = null;

var traitBases = [
  "atributo_Fisicos_Forca",
  "atributo_Fisicos_Destreza",
  "atributo_Fisicos_Vigor",
  "atributo_Sociais_Carisma",
  "atributo_Sociais_Manipulacao",
  "atributo_Sociais_Aparencia",
  "atributo_Mentais_Percepcao",
  "atributo_Mentais_Inteligencia",
  "atributo_Mentais_Raciocinio",
  "habilidade_Prontidao",
  "habilidade_Esportes",
  "habilidade_Briga",
  "habilidade_Esquiva",
  "habilidade_Empatia",
  "habilidade_Expressao",
  "habilidade_Intimidacao",
  "habilidade_Lideranca",
  "habilidade_Manha",
  "habilidade_Labia",
  "habilidade_EmpatiacomAnimais",
  "habilidade_Oficios",
  "habilidade_Conducao",
  "habilidade_Etiqueta",
  "habilidade_ArmasdeFogo",
  "habilidade_ArmasBrancas",
  "habilidade_Performance",
  "habilidade_Seguranca",
  "habilidade_Furtividade",
  "habilidade_Sobrevivencia",
  "habilidade_Academicos",
  "habilidade_Computador",
  "habilidade_Financas",
  "habilidade_Investigacao",
  "habilidade_Direito",
  "habilidade_Linguistica",
  "habilidade_Medicina",
  "habilidade_Ocultismo",
  "habilidade_Politica",
  "habilidade_Ciencia"
];

function vf(name) {
  var field = this.getField(name);
  return field ? field.value : "";
}

function selectedValue(name) {
  return String(vf(name)).replace(/^\s+|\s+$/g, "");
}

function hasValue(name) {
  var value = vf(name);
  return value !== "" && value !== "Off";
}

function numericField(name, warnings, minimum, maximum) {
  var raw = vf(name);
  if (raw === "" || raw === "Off") return 0;

  var normalized = String(raw).replace(",", ".");
  var value = Number(normalized);
  if (!isFinite(value) || Math.floor(value) !== value) {
    warnings.push(name + ": informe um numero inteiro");
    return null;
  }
  if (minimum !== null && value < minimum) {
    warnings.push(name + ": minimo " + minimum);
  }
  if (maximum !== null && value > maximum) {
    warnings.push(name + ": maximo " + maximum);
  }
  return value;
}

function numberOrZero(name, warnings, minimum, maximum) {
  var value = numericField(name, warnings, minimum, maximum);
  return value === null ? 0 : value;
}

function setv(name, value) {
  var field = this.getField(name);
  var next = String(value);
  if (field && String(field.value) !== next) field.value = next;
}

function setDots(baseName, value, count) {
  for (var index = 1; index <= count; index += 1) {
    var field = this.getField(baseName + "_" + index);
    if (field) field.value = index <= value ? "Yes" : "Off";
  }
}

function syncDotsFromClick(baseName, index, count) {
  var clicked = this.getField(baseName + "_" + index);
  var value = clicked && clicked.value !== "Off" ? Number(index) : Number(index) - 1;
  setv(baseName + "_val", value);
  setDots(baseName, value, count);
  recalcVampiro();
}

function syncHealthDamage(baseName, damageType) {
  var selected = this.getField(baseName + "_" + damageType);
  var damageTypes = ["cont", "letal", "agr"];
  if (selected && selected.value !== "Off") {
    for (var index = 0; index < damageTypes.length; index += 1) {
      if (damageTypes[index] !== damageType) {
        var field = this.getField(baseName + "_" + damageTypes[index]);
        if (field) field.value = "Off";
      }
    }
  }
  recalcVampiro();
}

function syncAllTraitDots(warnings) {
  for (var index = 0; index < traitBases.length; index += 1) {
    var value = numericField(traitBases[index] + "_val", warnings, 0, 10);
    if (value !== null) setDots(traitBases[index], Math.min(value, 5), 5);
  }
}

function genStats(generation) {
  var table = {
    "3": ["10", "indef.", "indef."],
    "4": ["9", "50", "10"],
    "5": ["8", "40", "8"],
    "6": ["7", "30", "6"],
    "7": ["6", "20", "4"],
    "8": ["5", "15", "3"],
    "9": ["5", "14", "2"],
    "10": ["5", "13", "1"],
    "11": ["5", "12", "1"],
    "12": ["5", "11", "1"],
    "13+": ["5", "10", "1"],
    "14": ["5", "10/8 util", "1"]
  };
  return table[generation] || null;
}

function validateDistribution(names, expected, label, warnings) {
  var entered = 0;
  var values = [];
  for (var index = 0; index < names.length; index += 1) {
    if (hasValue(names[index])) entered += 1;
    values.push(numberOrZero(names[index], warnings, 0, null));
  }
  if (entered === 0) return;
  if (entered !== names.length) {
    warnings.push(label + ": preencha todos os totais");
    return;
  }
  values.sort(function (left, right) { return left - right; });
  expected.sort(function (left, right) { return left - right; });
  for (var item = 0; item < expected.length; item += 1) {
    if (values[item] !== expected[item]) {
      warnings.push(label + ": distribuicao esperada " + expected.join("/"));
      return;
    }
  }
}

function validateCreation(warnings, isPlayerVampire) {
  validateDistribution(
    ["attr_fisicos_total", "attr_sociais_total", "attr_mentais_total"],
    [7, 5, 3],
    "Atributos",
    warnings
  );
  validateDistribution(
    ["hab_talentos_total", "hab_pericias_total", "hab_conhecimentos_total"],
    [13, 9, 5],
    "Habilidades",
    warnings
  );

  var fixedTotals = [
    ["disc_total", 3, "Disciplinas"],
    ["ante_total", 5, "Antecedentes"],
    ["virt_total", 7, "Virtudes"]
  ];
  for (var index = 0; index < fixedTotals.length; index += 1) {
    var fieldName = fixedTotals[index][0];
    var expected = fixedTotals[index][1];
    if (hasValue(fieldName)) {
      var actual = numericField(fieldName, warnings, 0, null);
      if (actual !== null && actual !== expected) {
        warnings.push(fixedTotals[index][2] + ": esperado " + expected);
      }
    }
  }

  if (selectedValue("cla") === "Nosferatu" && hasValue("atributo_Sociais_Aparencia_val")) {
    var appearance = numericField("atributo_Sociais_Aparencia_val", warnings, 0, 10);
    if (appearance !== null && appearance !== 0) {
      warnings.push("Nosferatu: Aparencia deve ser 0");
    }
  }

  if (
    isPlayerVampire &&
    hasValue("antecedente_Geracao_val") &&
    selectedValue("geracao") !== "14"
  ) {
    var background = numericField("antecedente_Geracao_val", warnings, 0, 5);
    var expectedGenerations = ["13+", "12", "11", "10", "9", "8"];
    if (background !== null && selectedValue("geracao") !== expectedGenerations[background]) {
      warnings.push("Geracao nao corresponde ao Antecedente Geracao");
    }
  }
}

function calculateFlaws(warnings) {
  var hasRows = false;
  var total = 0;
  for (var row = 1; row <= 8; row += 1) {
    var meritName = String(vf("qd_" + row + "_1"));
    var type = String(vf("qd_" + row + "_2"))
      .toLowerCase()
      .replace(/^\s+|\s+$/g, "");
    var hasPoints = hasValue("qd_" + row + "_3");
    if (meritName !== "" || type !== "" || hasPoints) {
      hasRows = true;
      if (type !== "qualidade" && type !== "defeito") {
        warnings.push("Linha " + row + ": tipo deve ser Qualidade ou Defeito");
      }
      var points = numberOrZero("qd_" + row + "_3", warnings, 0, 7);
      if (type === "defeito") total += points;
    }
  }
  if (hasRows) setv("defeitos_total", total);
  return hasRows ? total : numberOrZero("defeitos_total", warnings, 0, null);
}

function recalcVampiro() {
  var warnings = [];
  var characterType = selectedValue("tipo_personagem");
  var isPlayerVampire = characterType === "Vampiro jogador";

  syncAllTraitDots(warnings);

  if (characterType === "") {
    setv("humanidade_sugerida", "");
    setv("forca_vontade_sugerida", "");
    setv("limite_caracteristica", "");
    setv("sangue_max", "");
    setv("sangue_turno", "");
    warnings.push("Tipo: selecione uma opcao");
  } else if (isPlayerVampire) {
    var morality = selectedValue("moralidade_tipo");
    if (morality === "Humanidade") {
      var conscience = numberOrZero(
        "virtude_ConscienciaConviccao_val", warnings, 0, 5
      );
      var selfControl = numberOrZero(
        "virtude_AutocontroleInstinto_val", warnings, 0, 5
      );
      setv("humanidade_sugerida", conscience + selfControl);
    } else if (morality === "Trilha") {
      setv("humanidade_sugerida", "manual");
    } else {
      setv("humanidade_sugerida", "");
      warnings.push("Moralidade: selecione uma opcao");
    }
    setv(
      "forca_vontade_sugerida",
      numberOrZero("virtude_Coragem_val", warnings, 0, 5)
    );

    var stats = genStats(selectedValue("geracao"));
    if (stats) {
      setv("limite_caracteristica", stats[0]);
      setv("sangue_max", stats[1]);
      setv("sangue_turno", stats[2]);
    } else {
      setv("limite_caracteristica", "");
      setv("sangue_max", "");
      setv("sangue_turno", "");
      warnings.push("Geracao: selecione uma opcao");
    }
  } else {
    if (previousCharacterType === "Vampiro jogador") {
      setv("sangue_max", "");
      setv("sangue_turno", "");
    }
    setv("humanidade_sugerida", "manual");
    setv("forca_vontade_sugerida", "manual");
    setv("limite_caracteristica", "manual");
  }
  previousCharacterType = characterType;
  setv("sangue_max_resumo", vf("sangue_max"));
  setv("sangue_turno_resumo", vf("sangue_turno"));

  var xpTotal = numberOrZero("xp_total", warnings, 0, null);
  var xpSpent = numberOrZero("xp_gasto", warnings, 0, null);
  setv("xp_disponivel", xpTotal - xpSpent);

  var bonusBase = numberOrZero("bonus_base", warnings, 0, null);
  var flaws = calculateFlaws(warnings);
  var bonusSpent = numberOrZero("bonus_gasto", warnings, 0, null);
  if (flaws > 7) {
    setv("defeitos_aviso", "Limite de 7 excedido");
    warnings.push("Defeitos: limite de 7 excedido");
  } else {
    setv("defeitos_aviso", "OK");
  }
  setv("bonus_total", bonusBase + flaws);
  setv("bonus_saldo", bonusBase + flaws - bonusSpent);

  var linguistics = numberOrZero("habilidade_Linguistica_val", warnings, 0, 5);
  var languages = ["0", "1", "2", "4", "8", "16"];
  setv("idiomas_sugeridos", languages[Math.max(0, Math.min(5, linguistics))]);

  validateCreation(warnings, isPlayerVampire);
  if (characterType !== "" && !isPlayerVampire) {
    warnings.push("Recursos deste tipo de personagem sao preenchidos manualmente");
  }
  setv("avisos_criacao", warnings.length ? warnings.join(" | ") : "OK");
}

try {
  recalcVampiro();
} catch (error) {
  if (typeof console !== "undefined" && console.println) {
    console.println("Falha ao recalcular a ficha: " + error);
  }
}
