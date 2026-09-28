# Estrategia de Testes

## Objetivo

As verificacoes automatizadas protegem as regras deterministicas do gerador e
o contrato estrutural do PDF. A execucao real de JavaScript, navegacao,
salvamento e impressao no Adobe Acrobat/Reader continua sendo uma etapa manual.

## Diagnostico

A base anterior possuia:

- testes Python com unittest para build, campos AcroForm e pos-processamento;
- um teste JavaScript com asserts para dois cenarios;
- validacao estrutural pelo script scripts/validate_sheet.py;
- comparacao entre um build temporario e o PDF distribuido.

Os maiores riscos sem cobertura eram as ramificacoes de calculations.js,
integridade das listas do sistema, presenca de todos os campos, geometria dos
widgets, conteudo JavaScript incorporado e falhas do pos-processamento.

## Camadas

| Camada | Ferramenta | Escopo |
|---|---|---|
| Unidade Python | unittest | dados do sistema e selecao de acoes AcroForm |
| Unidade JavaScript | node:test, assert e vm | formulas, avisos e sincronizacao |
| Integracao | unittest, ReportLab e pypdf | geracao e pos-processamento |
| Contrato | pypdf | campos, flags, opcoes, widgets, JavaScript e A4 |
| Regressao | snapshot estrutural | equivalencia entre build limpo e PDF distribuido |
| Qualidade estatica | Ruff e compilacao Python | imports, codigo morto e sintaxe |

## Fluxos automatizados

### Regras do sistema

- todos os tipos de personagem suportados;
- todos os valores da tabela de Geracao;
- Humanidade, Trilha e Forca de Vontade;
- sangue maximo, sangue por turno e limite de Caracteristica;
- experiencia disponivel;
- bonus, Qualidades, Defeitos e limite de 7;
- distribuicoes 7/5/3, 13/9/5, 3, 5 e 7;
- Aparencia de Nosferatu;
- consistencia entre Geracao e Antecedente Geracao;
- entradas numericas invalidas e tipos de Qualidade/Defeito invalidos.

### Interacao do formulario

- sincronizacao entre valor numerico e marcadores;
- clique em marcador atualizando o valor numerico;
- exclusividade de dano de contusao, letal e agravado;
- preservacao de recursos manuais para Mortal, Carnical e Antagonista;
- limpeza de valores vampiricos ao trocar para perfil manual;
- ausencia de polling permanente.

### Contrato do PDF

- cinco paginas A4;
- 485 campos AcroForm;
- nomes terminais unicos;
- listas completas de clas, geracoes e tipos;
- campos para todos os Atributos, Habilidades, Disciplinas, Antecedentes e
  Virtudes;
- widgets dentro dos limites das paginas;
- campos multilinha e limite de 4.000 caracteres;
- checkboxes nao obrigatorios;
- idioma pt-BR e tabulacao estrutural;
- JavaScript incorporado identico ao arquivo revisado;
- build temporario equivalente ao artefato distribuido.

### Erros e extremos

- arquivo de entrada inexistente;
- JavaScript de documento inexistente;
- saida nao criada quando o pos-processamento falha;
- valores nao inteiros;
- totais incompletos ou invalidos;
- Defeitos acima do limite;
- tipos de linha desconhecidos.

## Comandos

Instalacao reproduzivel:

~~~powershell
python -m pip install -e ".[test]"
~~~

Lint e formatacao:

~~~powershell
ruff check --no-cache src scripts tests
ruff format --check --no-cache src scripts tests
~~~

Testes e cobertura Python:

~~~powershell
coverage erase
coverage run -m unittest discover -s tests -p "test_*.py" -v
coverage report
~~~

Testes JavaScript:

~~~powershell
node --check src\vampiro_sheet\calculations.js
node tests\test_calculations.js
~~~

Build e contrato final:

~~~powershell
python scripts\build_sheet.py
python scripts\validate_sheet.py
~~~

## Resultado desta fase

- 28 testes Python aprovados;
- 20 testes JavaScript aprovados;
- cobertura Python de 99% no relatorio combinado;
- 95,2% dos ramos Python cobertos;
- lint e formatacao aprovados;
- build limpo e validacao do PDF aprovados.

O relatorio de cobertura experimental do Node cobre o harness, mas nao atribui
corretamente o codigo carregado por vm em calculations.js. Por isso nao e usado
como evidencia de cobertura do codigo de producao. A evidencia JavaScript e a
matriz de 17 testes comportamentais.

## Validacao manual obrigatoria

No Adobe Acrobat/Reader:

1. clicar nos marcadores e confirmar atualizacao visual e numerica;
2. editar campos numericos e confirmar validacao e recalculo;
3. alternar tipos de personagem e Geracao;
4. marcar os tres tipos de dano;
5. preencher, salvar, fechar e reabrir o documento;
6. testar JavaScript desabilitado;
7. navegar integralmente por teclado;
8. executar o verificador de acessibilidade;
9. imprimir as cinco paginas em A4, escala 100%, colorido e monocromatico.

## Limitacoes

- o ambiente automatizado nao executa o motor JavaScript do Acrobat;
- nao ha teste visual por renderizacao de paginas nesta fase;
- leitores de PDF alternativos podem ignorar acoes JavaScript;
- a cobertura Python nao mede calculations.js;
- a fidelidade das regras continua dependente da analise do livro e das
  decisoes manuais do Narrador para Trilhas e antagonistas.
