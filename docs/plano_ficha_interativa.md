# Plano da Ficha Interativa

> Documento historico de planejamento. O estado implementado e suas correcoes
> estao registrados em relatorio_final_implementacao.md e
> relatorio_correcoes_tecnicas.md.

Este documento encerra a Etapa 2. Nenhum PDF deve ser gerado antes de validar este plano.

## Objetivo de Design

Criar uma ficha A4 preenchivel, limpa, original, sem uso de ilustracoes, logos, molduras ou elementos protegidos do livro. O estilo visual deve ser sobrio, moderno e adequado a impressao: alto contraste, pouca ornamentacao, linhas finas, seções claras e campos com tamanho suficiente para escrita manual e digital.

## Quantidade de Paginas

Proposta: 5 paginas A4.

1. Identidade, Atributos, Habilidades e Vantagens principais.
2. Recursos de jogo: sangue, vontade, vitalidade, combate, equipamentos e fraquezas.
3. Disciplinas, Taumaturgia/Necromancia, rituais, poderes e especializacoes.
4. Historia, relacoes, refugio, rebanho, lacaios, notas e perguntas de prelude.
5. Criacao e progresso: auditoria de pontos, bonus, experiencia, Qualidades/Defeitos e validacao.

Justificativa: uma ficha de 2 paginas ficaria comprimida demais para acomodar Disciplinas, rituais, Qualidades/Defeitos e campos de calculo. Cinco paginas preservam legibilidade e ainda continuam praticas para impressao.

## Organizacao Visual

Formato:

- A4 vertical.
- Margens de 12 mm.
- Grade de 3 colunas nas paginas densas.
- Tipografia sem serifa para preenchimento e serifada discreta apenas em titulos, se necessario.
- Paleta: preto, cinza e um vermelho escuro pontual. Deve imprimir bem em escala de cinza.
- Campos de pontos com caixas/circulos clicaveis de 0 a 5, e campos extras quando necessario.

Pagina 1:

- Cabecalho: Nome, Jogador, Cronica, Conceito, Cla, Geracao, Natureza, Comportamento.
- Atributos em tres blocos: Fisicos, Sociais, Mentais.
- Habilidades em tres blocos: Talentos, Pericias, Conhecimentos.
- Vantagens resumidas: Disciplinas, Antecedentes, Virtudes.
- Rodape compacto com Humanidade/Trilha, Forca de Vontade e Sangue maximo.

Pagina 2:

- Reserva de Sangue: maximo, atual, gasto/turno, caixas de controle.
- Forca de Vontade: permanente e temporaria.
- Vitalidade: sete niveis com dano de contusao, letal e agravado.
- Combate: iniciativa, absorcao, defesa/esquiva, modificadores, armas.
- Equipamentos, armaduras, veiculos e pertences.
- Fraqueza de cla e restricoes especiais.

Pagina 3:

- Disciplinas com nivel e poderes por nivel.
- Area dedicada a Taumaturgia: trilha primaria, trilhas secundarias, rituais e observacoes.
- Area dedicada a Necromancia: linha primaria, linhas secundarias, rituais e observacoes.
- Especializacoes de Atributos/Habilidades.
- Perturbacoes e condicoes sobrenaturais.

Pagina 4:

- Historia e prelude em campos multilinha.
- Senhor, linhagem, relacoes, aliados importantes, inimigos, contatos principais.
- Refugio, territorio de caca, rebanho e lacaios.
- Identidades, mascara publica e conexoes mortais.
- Notas livres.

Pagina 5:

- Auditoria de criacao: Atributos 7/5/3, Habilidades 13/9/5, Disciplinas 3, Antecedentes 5, Virtudes 7, bonus 15.
- Qualidades e Defeitos: nome, tipo, custo/valor e nota.
- Experiencia: total, gasto, disponivel.
- Custos de experiencia e bonus em tabela de referencia.
- Validadores e avisos: limite de Defeitos, Habilidade acima de 3 na criacao, Nosferatu Aparencia 0, 14a Geracao, Caitiff.

## Fluxo de Preenchimento

1. Preencher identidade e conceito.
2. Escolher cla, natureza, comportamento e moralidade.
3. Distribuir Atributos e marcar prioridade 7/5/3.
4. Distribuir Habilidades e marcar prioridade 13/9/5.
5. Preencher Disciplinas, Antecedentes e Virtudes.
6. Escolher Qualidades/Defeitos e aplicar bonus.
7. Conferir valores derivados calculados.
8. Preencher historia, equipamentos, relacoes e notas.
9. Atualizar experiencia durante a cronica.

## Campos Editaveis

Campos de texto:

- Identidade completa.
- Historia, aparencia, notas, motivacoes e prelude.
- Especializacoes.
- Fraquezas, perturbacoes e restricoes.
- Equipamentos e armas.
- Rituais, trilhas/linhas e poderes adicionais.

Campos numericos:

- Atributos, Habilidades, Disciplinas, Antecedentes, Virtudes.
- Humanidade/Trilha manual quando necessario.
- Forca de Vontade permanente/temporaria.
- Sangue atual.
- Experiencia total/gasta/disponivel.
- Custos de Qualidades/Defeitos.

Caixas de selecao:

- Pontos em escala 0-5.
- Sangue atual.
- Vontade temporaria.
- Vitalidade/dano.
- Marcadores de cla especial: Caitiff, Nosferatu, 14a Geracao, Trilha alternativa.

Menus suspensos:

- Cla.
- Natureza.
- Comportamento.
- Moralidade: Humanidade ou Trilha.
- Geracao.
- Prioridade de Atributos e Habilidades.
- Tipo de dano.

Botoes de opcao:

- Prioridade primaria/secundaria/terciaria por grupo.
- Virtude moral: Consciencia ou Conviccao.
- Virtude de autocontrole: Autocontrole ou Instinto.

## Campos Calculados

Calculos automaticos planejados:

- Humanidade padrao = Consciencia + Autocontrole.
- Forca de Vontade inicial sugerida = Coragem.
- Geracao efetiva a partir de Antecedente Geracao.
- Reserva maxima de sangue, sangue por turno e limite maximo de Caracteristica por Geracao.
- Total gasto em cada grupo de criacao.
- Total de bonus gasto, bonus recebido por Defeitos e saldo.
- Total de experiencia disponivel = total - gasto.
- Penalidade de Vitalidade atual conforme pior nivel marcado.
- Idiomas adicionais sugeridos por Linguistica.

Calculos com modo manual:

- Trilha alternativa, pois depende das Virtudes da Trilha escolhida.
- Efeitos de Qualidades/Defeitos, porque varios dependem de julgamento do Narrador.
- Penalidades de fraqueza de cla, porque se aplicam em contexto.

## Recursos Opcionais

- Botao para limpar campos temporarios: sangue atual, vontade temporaria, dano e experiencia temporaria.
- Indicadores visuais de alerta para erros de criacao.
- Campos de "aprovado pelo Narrador" em Qualidades/Defeitos, Disciplinas fora de cla e Trilhas alternativas.
- Camada de ajuda oculta ou notas tooltip com formulas.
- Versao printer-friendly sem preenchimento digital, gerada do mesmo codigo.

## Implementacao Planejada

Linguagem sugerida: Python.

Bibliotecas:

- ReportLab para layout vetorial e campos AcroForm.
- pypdf para ajustes finais, metadados e validacao basica.

Estrutura proposta:

- `src/vampiro_sheet/data.py`: listas, custos, tabelas de geracao, clãs e disciplinas.
- `src/vampiro_sheet/layout.py`: constantes de pagina, grade, estilos e componentes visuais.
- `src/vampiro_sheet/fields.py`: criacao padronizada de campos de texto, checkboxes, radio buttons e dropdowns.
- `src/vampiro_sheet/calculations.js`: JavaScript AcroForm para calculos em leitores compativeis.
- `src/vampiro_sheet/build.py`: gerador principal.
- `assets/`: apenas assets originais se necessario; por padrao, nenhum asset protegido.
- `dist/`: PDF final gerado.
- `docs/`: analise, plano e relatorio final.

## Validacao Planejada

Validacao de conteudo:

- Conferir se todos os Atributos, Habilidades, Antecedentes, Virtudes e Disciplinas existem.
- Conferir formulas de Humanidade, Forca de Vontade, Geracao, Reserva de Sangue e experiencia.
- Conferir excecoes: Nosferatu, 14a Geracao, Caitiff, Virtudes alternativas e Trilhas.
- Conferir se Qualidades/Defeitos aceitam ate 7 pontos de Defeitos.

Validacao tecnica:

- Gerar PDF.
- Verificar existencia de campos AcroForm.
- Abrir/renderizar paginas para checar legibilidade.
- Testar calculos em leitor compativel com JavaScript de PDF.
- Confirmar que o PDF continua preenchivel apos salvar.

## Pontos que Precisam de Confirmacao

1. A ficha deve suportar somente personagens vampiros ou tambem mortais, carnicais e antagonistas do bestiario?
2. Voce quer a ficha com todos os clãs do modulo basico, incluindo independentes e Sabá, ou uma versao focada em Camarilla?
3. Para Trilhas alternativas, devo deixar calculo manual por seguranca ou criar regras automaticas por Trilha com aviso de "sujeito ao Narrador"?
4. O PDF deve priorizar compatibilidade com Adobe Acrobat/Reader, que suporta melhor JavaScript de PDF, ou compatibilidade ampla com leitores que podem ignorar calculos?

Sem essas confirmacoes, a implementacao ainda pode seguir com campos manuais e avisos, mas nao vou automatizar mecanicas ambiguas.
