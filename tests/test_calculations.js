const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const source = fs.readFileSync(
  path.join(__dirname, "..", "src", "vampiro_sheet", "calculations.js"),
  "ascii"
);

function createSheet(initialValues) {
  const fields = {};
  for (const [name, value] of Object.entries(initialValues || {})) {
    fields[name] = { value: String(value) };
  }

  const alerts = [];
  const timers = [];
  const context = {
    getField(name) {
      if (!fields[name]) fields[name] = { value: "" };
      return fields[name];
    },
    app: {
      alert(message) {
        alerts.push(String(message));
      },
      setTimeOut(code, delay) {
        timers.push([code, delay]);
      },
    },
  };
  vm.createContext(context);
  vm.runInContext(source, context, { filename: "calculations.js" });

  return {
    alerts,
    context,
    fields,
    values() {
      return Object.fromEntries(
        Object.entries(fields).map(([name, field]) => [name, field.value])
      );
    },
  };
}

function vampireValues(overrides) {
  return Object.assign(
    {
      tipo_personagem: "Vampiro jogador",
      moralidade_tipo: "Humanidade",
      geracao: "13+",
      virtude_ConscienciaConviccao_val: "3",
      virtude_AutocontroleInstinto_val: "4",
      virtude_Coragem_val: "3",
    },
    overrides || {}
  );
}

test("document script does not use permanent polling", () => {
  assert.equal(source.includes("setInterval"), false);
});

test("all generation options calculate their documented limits", () => {
  const expected = {
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
    "14": ["5", "10/8 util", "1"],
  };

  for (const [generation, values] of Object.entries(expected)) {
    const sheet = createSheet(vampireValues({ geracao: generation })).values();
    assert.deepEqual(
      [sheet.limite_caracteristica, sheet.sangue_max, sheet.sangue_turno],
      values
    );
    assert.equal(sheet.sangue_max_resumo, values[1]);
    assert.equal(sheet.sangue_turno_resumo, values[2]);
  }
});

test("humanity and willpower are derived for a player vampire", () => {
  const sheet = createSheet(vampireValues({ geracao: "9" })).values();
  assert.equal(sheet.humanidade_sugerida, "7");
  assert.equal(sheet.forca_vontade_sugerida, "3");
  assert.equal(sheet.sangue_max, "14");
  assert.equal(sheet.sangue_turno, "2");
});

test("alternative paths remain manual", () => {
  const sheet = createSheet(
    vampireValues({ moralidade_tipo: "Trilha" })
  ).values();
  assert.equal(sheet.humanidade_sugerida, "manual");
  assert.equal(sheet.forca_vontade_sugerida, "3");
});

test("non-vampire profiles preserve manual blood resources", () => {
  for (const characterType of ["Mortal", "Carnical", "Antagonista"]) {
    const sheet = createSheet({
      tipo_personagem: characterType,
      sangue_max: "manual",
      sangue_turno: "manual",
    }).values();
    assert.equal(sheet.sangue_max, "manual");
    assert.equal(sheet.sangue_turno, "manual");
    assert.equal(sheet.limite_caracteristica, "manual");
    assert.match(sheet.avisos_criacao, /preenchidos manualmente/);
  }
});

test("switching from vampire to a manual profile clears stale blood values", () => {
  const sheet = createSheet(vampireValues({ geracao: "8" }));
  assert.equal(sheet.values().sangue_max, "15");
  sheet.fields.tipo_personagem.value = "Mortal";
  sheet.context.recalcVampiro();
  assert.equal(sheet.values().sangue_max, "");
  assert.equal(sheet.values().sangue_turno, "");
});

test("trait numeric value synchronizes its visual dots", () => {
  const sheet = createSheet(vampireValues({ habilidade_Briga_val: "3" })).values();
  assert.equal(sheet.habilidade_Briga_1, "Yes");
  assert.equal(sheet.habilidade_Briga_3, "Yes");
  assert.equal(sheet.habilidade_Briga_4, "Off");
});

test("clicking a trait dot updates the numeric source of truth", () => {
  const sheet = createSheet(vampireValues());
  sheet.fields.habilidade_Briga_3.value = "Yes";
  sheet.context.syncDotsFromClick("habilidade_Briga", 3, 5);
  assert.equal(sheet.values().habilidade_Briga_val, "3");
  assert.equal(sheet.values().habilidade_Briga_1, "Yes");
  assert.equal(sheet.values().habilidade_Briga_4, "Off");
});

test("player can explicitly reduce an attribute to zero", () => {
  const sheet = createSheet(vampireValues({ atributo_Fisicos_Forca_val: "1" }));
  sheet.fields.atributo_Fisicos_Forca_1.value = "Off";
  sheet.context.syncDotsFromClick("atributo_Fisicos_Forca", 1, 5);
  assert.equal(sheet.values().atributo_Fisicos_Forca_val, "0");
  assert.equal(sheet.values().atributo_Fisicos_Forca_1, "Off");
});

test("blank identity choices do not imply character rules", () => {
  const sheet = createSheet({}).values();
  assert.equal(sheet.tipo_personagem, "");
  assert.equal(sheet.humanidade_sugerida, "");
  assert.equal(sheet.limite_caracteristica, "");
  assert.equal(sheet.sangue_max, "");
  assert.match(sheet.avisos_criacao, /Tipo: selecione uma opcao/);
});

test("blank generation does not imply thirteenth generation", () => {
  const sheet = createSheet(vampireValues({ geracao: "" })).values();
  assert.equal(sheet.limite_caracteristica, "");
  assert.equal(sheet.sangue_max, "");
  assert.equal(sheet.sangue_turno, "");
  assert.match(sheet.avisos_criacao, /Geracao: selecione uma opcao/);
});

test("damage types are mutually exclusive within one health level", () => {
  const sheet = createSheet({
    tipo_personagem: "Mortal",
    vitalidade_Escoriado_cont: "Yes",
    vitalidade_Escoriado_letal: "Yes",
    vitalidade_Escoriado_agr: "Yes",
  });
  sheet.context.syncHealthDamage("vitalidade_Escoriado", "letal");
  assert.equal(sheet.values().vitalidade_Escoriado_cont, "Off");
  assert.equal(sheet.values().vitalidade_Escoriado_letal, "Yes");
  assert.equal(sheet.values().vitalidade_Escoriado_agr, "Off");
});

test("experience and defect bonus balances are calculated", () => {
  const sheet = createSheet(
    vampireValues({
      bonus_base: "15",
      bonus_gasto: "4",
      xp_total: "20",
      xp_gasto: "7",
      qd_1_1: "Inimigo",
      qd_1_2: "Defeito",
      qd_1_3: "2",
      qd_2_1: "Bom Senso",
      qd_2_2: "Qualidade",
      qd_2_3: "1",
    })
  ).values();
  assert.equal(sheet.defeitos_total, "2");
  assert.equal(sheet.bonus_total, "17");
  assert.equal(sheet.bonus_saldo, "13");
  assert.equal(sheet.xp_disponivel, "13");
});

test("manual defect total remains supported when no rows are used", () => {
  const sheet = createSheet(
    vampireValues({ bonus_base: "15", defeitos_total: "4" })
  ).values();
  assert.equal(sheet.defeitos_total, "4");
  assert.equal(sheet.bonus_total, "19");
});

test("defects above seven produce a hard-limit warning", () => {
  const sheet = createSheet(
    vampireValues({
      qd_1_1: "Defeito A",
      qd_1_2: "Defeito",
      qd_1_3: "5",
      qd_2_1: "Defeito B",
      qd_2_2: "Defeito",
      qd_2_3: "3",
    })
  ).values();
  assert.equal(sheet.defeitos_total, "8");
  assert.equal(sheet.defeitos_aviso, "Limite de 7 excedido");
  assert.match(sheet.avisos_criacao, /limite de 7 excedido/);
});

test("valid creation totals do not produce distribution warnings", () => {
  const sheet = createSheet(
    vampireValues({
      attr_fisicos_total: "7",
      attr_sociais_total: "5",
      attr_mentais_total: "3",
      hab_talentos_total: "13",
      hab_pericias_total: "9",
      hab_conhecimentos_total: "5",
      disc_total: "3",
      ante_total: "5",
      virt_total: "7",
    })
  ).values();
  assert.equal(sheet.avisos_criacao, "OK");
});

test("invalid and incomplete creation totals produce actionable warnings", () => {
  const sheet = createSheet(
    vampireValues({
      attr_fisicos_total: "7",
      attr_sociais_total: "4",
      attr_mentais_total: "3",
      hab_talentos_total: "13",
    })
  ).values();
  assert.match(sheet.avisos_criacao, /Atributos: distribuicao esperada 3\/5\/7/);
  assert.match(sheet.avisos_criacao, /Habilidades: preencha todos os totais/);
});

test("Nosferatu appearance and generation background are validated", () => {
  const sheet = createSheet(
    vampireValues({
      cla: "Nosferatu",
      geracao: "10",
      atributo_Sociais_Aparencia_val: "1",
      antecedente_Geracao_val: "2",
    })
  ).values();
  assert.match(sheet.avisos_criacao, /Nosferatu: Aparencia deve ser 0/);
  assert.match(sheet.avisos_criacao, /Geracao nao corresponde/);
});

test("invalid integer input is visible instead of silently accepted", () => {
  const sheet = createSheet(
    vampireValues({ xp_total: "dez", xp_gasto: "2" })
  ).values();
  assert.equal(sheet.xp_disponivel, "-2");
  assert.match(sheet.avisos_criacao, /xp_total: informe um numero inteiro/);
});

test("invalid quality or defect type is reported", () => {
  const sheet = createSheet(
    vampireValues({
      qd_1_1: "Entrada",
      qd_1_2: "Outro",
      qd_1_3: "2",
    })
  ).values();
  assert.match(sheet.avisos_criacao, /tipo deve ser Qualidade ou Defeito/);
});
