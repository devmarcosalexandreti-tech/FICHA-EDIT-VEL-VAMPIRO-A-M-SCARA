# Como contribuir

Este projeto gera uma ficha interativa baseada em regras publicadas. Mudanças devem preservar a fidelidade ao sistema, a compatibilidade com Adobe Acrobat Reader e a impressão em A4.

## Ambiente local

Use Python 3.11 ou superior e Node.js 20 ou superior:

~~~powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
~~~

Não adicione o livro-fonte, extrações do livro, PDFs preenchidos, dados de jogadores, credenciais ou recursos visuais protegidos ao repositório.

## Desenvolvimento

- Mantenha alterações pequenas e relacionadas a um único objetivo.
- Preserve nomes de campos e contratos do PDF, salvo quando a mudança estiver documentada como incompatível.
- Não invente nem simplifique regras. Toda mudança de mecânica deve indicar a origem no material de referência disponível ao colaborador.
- Inclua testes que demonstrem o comportamento alterado.
- Não edite manualmente o PDF final; altere o gerador e reconstrua o artefato.

## Verificações obrigatórias

~~~powershell
ruff check src scripts tests
ruff format --check src scripts tests
python -W error -m compileall -q -f src scripts tests
python -m coverage run --branch -m unittest discover -s tests -p "test_*.py"
python -m coverage report -m --fail-under=95
node --test tests/test_calculations.js
python scripts/build_sheet.py
python scripts/validate_sheet.py
~~~

## Pull requests

Descreva o problema, os comportamentos anterior e esperado, as regras afetadas, os arquivos modificados, os testes executados e qualquer validação manual ainda necessária no Acrobat Reader.

Confirme também que nenhum material de consulta local, dado pessoal ou segredo foi incluído.
