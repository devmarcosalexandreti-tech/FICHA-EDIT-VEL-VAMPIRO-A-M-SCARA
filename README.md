# Ficha Interativa para Vampiro: A Máscara

Gerador de uma ficha de personagem A4, preenchível e automatizada para a terceira edição de Vampiro: A Máscara. O projeto prioriza compatibilidade com Adobe Acrobat Reader, impressão legível e manutenção das regras extraídas do módulo básico.

O projeto reduz erros de preenchimento manual ao sincronizar pontos, recursos e valores derivados. O gerador produz um PDF AcroForm com JavaScript compatível com Acrobat sem esconder os valores do jogador.

> Projeto independente, sem vínculo com os titulares de Vampiro: A Máscara. O livro de regras e seus elementos visuais não são distribuídos neste repositório. Para conferir regras, utilize uma cópia obtida legalmente.

## Funcionalidades

- PDF A4 com 5 páginas e 485 campos AcroForm.
- Campos de texto, numéricos, seletores, caixas de seleção e áreas multilinha.
- Suporte automatizado ao personagem vampiro jogador.
- Suporte manual a mortais, carniçais e antagonistas, sem aplicar automaticamente regras exclusivas de vampiros.
- Clãs do módulo básico, incluindo Camarilla, Sabá, independentes e Caitiff.
- Atributos, Habilidades, Disciplinas, Antecedentes, Virtudes, Humanidade, Força de Vontade, Sangue, Vitalidade, equipamento, armas, rituais, história, relações, Qualidades, Defeitos e experiência.
- Sincronização entre campos numéricos e marcadores visuais.
- Todos os Atributos iniciam em 1, mas o jogador pode reduzi-los explicitamente para 0.
- Seletores de identidade começam vazios e só assumem um valor após a escolha do jogador.
- Exclusividade das marcações de dano e atualização dos recursos.
- Cálculos e alertas de geração, reserva de sangue, Humanidade, Força de Vontade, pontos de bônus, Defeitos, idiomas e experiência.
- Validação estrutural automatizada do PDF gerado.

O artefato atual está em [dist/ficha_vampiro_interativa.pdf](dist/ficha_vampiro_interativa.pdf).

## Tecnologias

- Python 3.11 ou superior
- ReportLab para desenho e formulários PDF
- pypdf para inspeção, pós-processamento e validação
- JavaScript de formulário para cálculos no Adobe Acrobat Reader
- unittest e Coverage.py
- Node.js para testes isolados dos cálculos JavaScript
- Ruff para lint e formatação
- GitHub Actions para integração contínua

## Arquitetura

O projeto separa definição visual, pós-processamento e verificação:

~~~text
src/vampiro_sheet/
  build.py             composição e montagem das páginas
  layout.py            primitivas visuais e seções reutilizáveis
  fields.py            criação e configuração dos campos AcroForm
  data.py              catálogos e dados estáticos do sistema
  pdf_postprocess.py   AcroForm, JavaScript e propriedades finais
  calculations.js     regras executadas no leitor de PDF
scripts/
  build_sheet.py       entrada para gerar o PDF final
  validate_sheet.py    contrato estrutural do artefato
tests/
  test_build.py
  test_data_contract.py
  test_pdf_contract.py
  test_pdf_postprocess.py
  test_calculations.js
docs/
  analise_sistema_vampiro_3e.md
  plano_ficha_interativa.md
  relatorio_final_implementacao.md
  estrategia_testes.md
~~~

A análise das regras e as decisões de implementação estão documentadas em [docs/analise_sistema_vampiro_3e.md](docs/analise_sistema_vampiro_3e.md), [docs/plano_ficha_interativa.md](docs/plano_ficha_interativa.md) e [docs/relatorio_final_implementacao.md](docs/relatorio_final_implementacao.md).

## Pré-requisitos

- Python 3.11+
- Node.js 20+ para executar os testes JavaScript
- Adobe Acrobat Reader para validar toda a interatividade do PDF

O projeto não utiliza servidor, banco de dados, credenciais nem variáveis de ambiente. Por isso, nenhum arquivo .env é necessário.

## Instalação

No diretório raiz, crie um ambiente virtual e instale o projeto com as dependências de desenvolvimento:

~~~powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[test]
~~~

Em Linux ou macOS:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[test]
~~~

## Geração e validação

~~~powershell
python scripts/build_sheet.py
python scripts/validate_sheet.py
~~~

O arquivo resultante é dist/ficha_vampiro_interativa.pdf.

## Testes e qualidade

~~~powershell
python -m coverage run --branch -m unittest discover -s tests -p test_*.py
python -m coverage report -m
node --test tests/test_calculations.js
ruff check src scripts tests
ruff format --check src scripts tests
python -W error -m compileall -q -f src scripts tests
~~~

O workflow em [.github/workflows/ci.yml](.github/workflows/ci.yml) executa essas verificações, gera o PDF e valida seu contrato em cada push e pull request.

## Uso

1. Abra dist/ficha_vampiro_interativa.pdf no Adobe Acrobat Reader.
2. Escolha o tipo de personagem e preencha os dados básicos.
3. Informe os valores conforme as regras da crônica.
4. Revise os avisos de criação e os totais calculados.
5. Salve uma cópia preenchida ou imprima em papel A4.

Leitores baseados apenas no navegador podem exibir os campos, mas normalmente não executam todo o JavaScript de formulário. Para os cálculos e sincronizações, use Adobe Acrobat Reader.

## Limitações conhecidas

- A automação completa está concentrada em vampiros jogadores; mortais, carniçais e antagonistas usam campos manuais onde as regras dependem da crônica.
- A execução do JavaScript precisa de um leitor compatível com Acrobat.
- Compatibilidade visual e comportamental ainda deve ser conferida manualmente nas versões de Acrobat e nos sistemas operacionais alvo.
- O projeto não inclui o livro-fonte nem imagens protegidas.
- A licença do código ainda precisa ser definida antes da publicação pública.

## Melhorias futuras

- Matriz de validação manual em diferentes versões do Acrobat Reader.
- Capturas de tela próprias do PDF, após revisão final do conteúdo.
- Testes adicionais em leitores PDF alternativos.
- Política formal de versões e lançamentos.

## Contribuição

Consulte [CONTRIBUTING.md](CONTRIBUTING.md). Alterações de regra precisam ser fundamentadas no material de referência e acompanhadas por testes; não devem introduzir mecânicas presumidas.

## Licença

Nenhuma licença foi definida. A ausência de licença não concede permissão automática para copiar, modificar ou redistribuir o código. Escolha e adicione uma licença compatível com seus objetivos antes de tornar o repositório público.
