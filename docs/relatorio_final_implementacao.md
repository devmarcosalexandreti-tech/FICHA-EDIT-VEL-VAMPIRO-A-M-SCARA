# Relatorio Final de Implementacao

## Entregaveis

- Analise do sistema: `docs/analise_sistema_vampiro_3e.md`
- Estrutura e planejamento: `docs/plano_ficha_interativa.md`
- Codigo-fonte: `src/vampiro_sheet/`
- Script de geracao: `scripts/build_sheet.py`
- Script de validacao: `scripts/validate_sheet.py`
- PDF preenchivel: `dist/ficha_vampiro_interativa.pdf`
- PDF intermediario sem pos-processamento: `build/ficha_vampiro_interativa_draft.pdf`

## Decisoes Aplicadas

A ficha suporta:

- Vampiros jogadores.
- Mortais.
- Carnicais.
- Antagonistas.
- Todos os clas do modulo basico, incluindo Camarilla, Saba, independentes e Caitiff.

O PDF prioriza Adobe Acrobat/Reader:

- Usa campos AcroForm.
- Inclui JavaScript de documento para recalculos em Acrobat/Reader.
- Mantem campos editaveis mesmo em leitores que ignorem JavaScript.

Trilhas alternativas foram deixadas com calculo manual:

- Humanidade padrao e calculada como Consciencia + Autocontrole.
- Trilhas exibem "manual" no campo derivado, pois a selecao de Virtudes e a permissao de uso dependem do Narrador.

## Estrutura do PDF

O PDF possui 5 paginas A4:

1. Identidade, Atributos, Habilidades, Vantagens e derivados principais.
2. Sangue, Forca de Vontade, Vitalidade, combate, equipamentos e fraquezas.
3. Disciplinas, Taumaturgia, Necromancia, especializacoes e perturbacoes.
4. Historia, relacoes, refugio, caca, rebanho, lacaios e identidades.
5. Auditoria de criacao, Qualidades/Defeitos, bonus, experiencia e custos.

## Automacoes

Automacoes implementadas no JavaScript do PDF:

- Humanidade sugerida para Humanidade padrao.
- Forca de Vontade sugerida a partir de Coragem.
- Limite de Caracteristica, sangue maximo e sangue por turno a partir da Geracao.
- XP disponivel.
- Bonus total e saldo.
- Aviso se Defeitos ultrapassarem 7 pontos.
- Idiomas sugeridos por Linguistica.

Campos que permanecem manuais por fidelidade ao sistema:

- Pontos iniciais de sangue por 1d10.
- Efeitos narrativos de Qualidades/Defeitos.
- Fraquezas de cla em contexto.
- Trilhas alternativas.
- Rituais, linhas e trilhas de Taumaturgia/Necromancia.
- Mortais, carnicais e antagonistas fora do padrao vampirico.

## Validacao Realizada

Validacao estrutural executada por `scripts/validate_sheet.py`:

- 5 paginas.
- 485 campos AcroForm.
- AcroForm presente.
- JavaScript presente.
- Campos obrigatorios principais presentes.

Resultado esperado:

```text
validation ok
pages: 5
fields: 485
acroform: yes
javascript: yes
```

## Limites Conhecidos

- Campos multilinha em PDF nao crescem fisicamente na pagina impressa; eles rolam digitalmente em leitores compativeis.
- Nem todo leitor de PDF executa JavaScript; Acrobat/Reader e o alvo principal.
- Os marcadores de pontos em bolinhas e os campos numericos coexistem. Os campos numericos alimentam os calculos; as bolinhas servem para uso visual/manual.
- A ficha evita copiar arte, logos, molduras ou identidade visual protegida do livro.
- As correcoes e validacoes posteriores estao em
  docs/relatorio_correcoes_tecnicas.md.
