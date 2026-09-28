# Relatorio de Correcoes Tecnicas

## Escopo

Este ciclo tratou primeiro falhas de severidade alta e correcoes de risco
controlado identificadas em AUDITORIA_TECNICA.md. Nao houve remocao de paginas,
campos funcionais, tipos de personagem, clas, regras, artefatos ou dados locais.
O PDF continua com cinco paginas A4 e prioriza Adobe Acrobat/Reader.

## Correcoes concluidas

### 1. Calculos condicionados ao tipo de personagem

- Causa-raiz: recalcVampiro ignorava tipo_personagem.
- Alteracao: derivados vampiricos so sao impostos a Vampiro jogador. Mortal,
  Carnical e Antagonista preservam sangue manual e recebem aviso explicito.
- Arquivo: src/vampiro_sheet/calculations.js.
- Teste: tests/test_calculations.js cobre mortal e vampiro de 9a geracao.
- Risco remanescente: antagonistas vampiricos continuam no modo manual por nao
  haver dados suficientes para inferir sua construcao.

### 2. Nomes AcroForm duplicados

- Causa-raiz: sangue_max e sangue_turno eram campos terminais distintos nas
  paginas 1 e 2, mas compartilhavam o mesmo nome.
- Alteracao: os widgets da pagina 1 agora sao sangue_max_resumo e
  sangue_turno_resumo; os campos originais da pagina 2 preservam o contrato.
- Arquivos: src/vampiro_sheet/build.py e calculations.js.
- Teste: o contrato rejeita qualquer nome terminal duplicado.
- Risco remanescente: arquivos preenchidos gerados pela versao anterior nao sao
  migrados automaticamente para o novo PDF.

### 3. Sincronizacao entre pontos e valor numerico

- Causa-raiz: checkboxes e campos com sufixo _val eram fontes independentes.
- Alteracao: valores numericos atualizam os pontos; cliques nos pontos atualizam
  o valor numerico por acoes JavaScript associadas aos widgets.
- Arquivos: build.py, calculations.js e fields.py.
- Testes: teste Node verifica sincronizacao e o contrato verifica as acoes.
- Risco remanescente: a interacao de clique deve ser homologada no Adobe Reader,
  pois leitores alternativos podem ignorar JavaScript.

### 4. Validacao numerica

- Causa-raiz: numeric era apenas um campo de texto e entrada invalida virava
  zero silenciosamente.
- Alteracao: campos mecanicos recebem validacao de inteiro nao negativo no
  Acrobat; faixas e inconsistencias tambem entram nos avisos automaticos.
- Arquivos: build.py, calculations.js e fields.py.
- Testes: contrato verifica a presenca da acao de validacao.
- Risco remanescente: limites dependentes de geracao sao avisados, mas nem todos
  sao bloqueados para preservar personagens antigos e antagonistas.

### 5. Auditoria de criacao

- Causa-raiz: totais eram livres e nao havia verificacao de distribuicao.
- Alteracao: o JavaScript valida 7/5/3, 13/9/5, Disciplinas 3,
  Antecedentes 5, Virtudes 7, Nosferatu e consistencia entre Geracao e seu
  Antecedente. Avisos automaticos foram separados das notas do Narrador.
- Arquivos: build.py e calculations.js.
- Risco remanescente: os totais continuam sendo informados pelo jogador, pois
  os valores finais nao distinguem pontos iniciais de pontos de bonus. Somar os
  valores finais como se fossem pontos de criacao produziria regra incorreta.

### 6. Dano mutuamente exclusivo

- Causa-raiz: contusao, letal e agravado podiam coexistir no mesmo nivel.
- Alteracao: marcar um tipo desmarca os outros dois no mesmo nivel, mantendo
  nomes, posicoes e aparencia.
- Arquivos: build.py e calculations.js.
- Teste: contrato confirma a acao nos widgets de Vitalidade.
- Risco remanescente: penalidade atual ainda nao possui campo derivado dedicado.

### 7. Qualidades, Defeitos e bonus

- Causa-raiz: o total de Defeitos era inteiramente manual.
- Alteracao: linhas preenchidas com tipo Defeito sao somadas; tipos invalidos,
  pontos invalidos e total acima de 7 geram avisos. O preenchimento manual foi
  mantido quando nenhuma linha esta sendo usada.
- Arquivo: calculations.js.
- Teste: teste Node confere soma e reflexo em bonus_total.
- Risco remanescente: bonus_gasto continua manual, pois a ficha nao registra a
  aplicacao individual de cada ponto de bonus.

### 8. Polling e tratamento de erros

- Causa-raiz: setInterval executava a cada segundo e o catch era vazio.
- Alteracao: o timer permanente foi removido. Campos-fonte recebem acoes de
  validacao que agendam um recalc pontual; erros inesperados sao enviados ao
  console do Acrobat quando disponivel.
- Arquivos: build.py e calculations.js.
- Testes: teste Node rejeita a presenca de setInterval; validador inspeciona o
  JavaScript incorporado.
- Risco remanescente: eventos precisam de homologacao nas versoes de Acrobat
  declaradas como suportadas.

### 9. Flags, acessibilidade basica e campos derivados

- Causa-raiz: ReportLab marca checkbox como required por padrao e os tooltips
  usavam identificadores internos.
- Alteracao: flags sao explicitas; derivados sao read-only; tooltips principais
  usam rotulos humanos; documento define pt-BR e ordem estrutural de tabulacao.
  Campos multilinha passam de 100 para 4000 caracteres.
- Arquivos: fields.py e build.py.
- Testes: contrato verifica flags, read-only, idioma e tabulacao.
- Risco remanescente: o PDF ainda nao possui StructTreeRoot e nao e um PDF
  totalmente marcado para tecnologia assistiva.

### 10. Validador e testes

- Causa-raiz: a verificacao anterior aceitava qualquer arvore Names, minimo
  generico de campos e nao detectava duplicidade ou flags.
- Alteracao: o validador verifica JavaScript esperado, ausencia de polling,
  nomes unicos, flags, derivados, idioma, tabulacao e acoes. Foram adicionados
  testes Python de contrato e build limpo, alem de teste Node das formulas.
- Arquivos: scripts/validate_sheet.py e tests/.
- Risco remanescente: testes automatizados nao substituem Acrobat/Reader real.

### 11. Build e empacotamento

- Causa-raiz: dependencias nao declaradas, build sempre escrevia na arvore do
  projeto e JavaScript nao estava configurado como dado de pacote.
- Alteracao: pyproject.toml declara Python e dependencias; calculations.js faz
  parte do pacote; build aceita diretorio temporario, cria destinos e grava o
  PDF final de forma atomica. Metadado de autor deixou de atribuir o trabalho
  ao Codex.
- Arquivos: pyproject.toml, build.py e scripts/build_sheet.py.
- Testes: build completo em diretorio temporario e pip install --dry-run.
- Risco remanescente: builds ainda incluem data/hora gerada pelo ReportLab e
  nao sao binariamente reproduziveis.

### 12. Preparacao para GitHub

- Causa-raiz: diretorio Git vazio, sem README, manifest, ignore ou CI.
- Alteracao: Git inicializado; README, .gitignore, pyproject.toml e workflow de
  CI adicionados. Livro e extracao textual estao ignorados, sem serem apagados.
- Arquivos: README.md, .gitignore, pyproject.toml e .github/workflows/ci.yml.
- Risco remanescente: o autor ainda precisa escolher a licenca, revisar o
  primeiro commit e confirmar direitos sobre o PDF distribuido.

## Verificacoes executadas

| Verificacao | Resultado |
|---|---|
| Sintaxe Python | aprovada |
| Sintaxe JavaScript com node --check | aprovada |
| Testes Python unittest | 5 aprovados |
| Testes JavaScript Node | aprovados |
| Build limpo em diretorio temporario | aprovado |
| Validador do PDF | aprovado |
| Paginas | 5 |
| Campos AcroForm | 485 |
| JavaScript incorporado | presente |
| Manifesto com pip install --dry-run | aprovado |

## Arquivos modificados

- src/vampiro_sheet/build.py
- src/vampiro_sheet/calculations.js
- src/vampiro_sheet/fields.py
- scripts/build_sheet.py
- scripts/validate_sheet.py
- docs/plano_ficha_interativa.md
- docs/relatorio_final_implementacao.md
- dist/ficha_vampiro_interativa.pdf
- build/ficha_vampiro_interativa_draft.pdf

## Arquivos adicionados

- tests/test_build.py
- tests/test_pdf_contract.py
- tests/test_calculations.js
- pyproject.toml
- README.md
- .gitignore
- .github/workflows/ci.yml
- docs/relatorio_correcoes_tecnicas.md

## Pendencias deliberadas

1. Homologar preenchimento, eventos, salvamento e reabertura no Adobe
   Acrobat/Reader em Windows.
2. Separar Consciencia/Conviccao e Autocontrole/Instinto somente apos fechar o
   contrato visual e de dados para Trilhas.
3. Adicionar campos de idade, data do Abraco, seita, tipo e ocultabilidade de
   arma sem comprometer a legibilidade A4.
4. Implementar estrutura PDF marcada se acessibilidade completa for requisito.
5. Unificar a tabela de Geracao entre Python e JavaScript.
6. Escolher licenca do codigo e revisar direitos de distribuicao do PDF final.
7. Executar scanner de dependencias no CI depois do primeiro push.

## Validacao manual recomendada

No Adobe Reader, abrir dist/ficha_vampiro_interativa.pdf e testar:

1. alternancia entre Vampiro jogador e os tres perfis manuais;
2. clique nos pontos e edicao do valor numerico correspondente;
3. selecao exclusiva dos tipos de dano;
4. rejeicao de letras e valores negativos em campos numericos;
5. mudanca de cla, Geracao, Antecedente Geracao e totais de criacao;
6. soma de Defeitos e limite de 7;
7. salvamento, fechamento, reabertura e impressao A4 a 100%.
