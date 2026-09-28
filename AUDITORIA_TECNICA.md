# Auditoria Técnica

## 1. Resumo executivo

O projeto é um gerador de ficha interativa em PDF para *Vampiro: A Máscara 3ª Edição*. A implementação usa Python para desenhar o documento e criar os campos AcroForm, `pypdf` para o pós-processamento, e JavaScript de documento para cálculos no Adobe Acrobat/Reader.

A base é pequena, compreensível e possui uma separação inicial adequada entre dados do sistema, layout, componentes de formulário, montagem do PDF e cálculos. O PDF existente tem cinco páginas A4, 482 nomes de campo reconhecidos, AcroForm e JavaScript incorporado. A sintaxe de todos os arquivos Python foi validada e a validação estrutural existente termina com sucesso.

O projeto ainda não está pronto para publicação profissional. Os principais bloqueadores são:

- o suporte declarado a mortais, carniçais e antagonistas é apenas nominal, pois cálculos vampíricos continuam sendo aplicados a todos os tipos;
- duas propriedades derivadas possuem campos terminais duplicados no AcroForm, tornando ambíguo qual widget o JavaScript atualiza;
- valores mecânicos têm duas fontes de entrada independentes, caixas e texto, sem sincronização ou validação;
- as verificações centrais da criação de personagem foram desenhadas como campos manuais, não como auditoria automática;
- o diretório não é um repositório Git funcional e não contém README, manifesto de dependências, licença, `.gitignore` ou automação de CI;
- o livro-fonte e sua extração textual estão dentro do diretório, o que cria risco de direitos autorais para uma publicação aberta.

Não foi encontrada falha crítica de segurança, credencial exposta ou comunicação externa. O maior risco é de integridade funcional da ficha e de publicação inadequada do material-fonte.

## 2. Escopo e método

Foram inspecionados:

- todos os arquivos Python e JavaScript em `src/` e `scripts/`;
- toda a documentação em `docs/`;
- metadados, catálogo, campos, flags, anotações, páginas e JavaScript do PDF em `dist/`;
- estrutura do diretório, artefatos gerados e arquivos auxiliares;
- sintaxe Python e execução de `scripts/validate_sheet.py`.

Limitações da auditoria:

- o diretório `.git` está vazio, portanto não foi possível avaliar histórico, branches, rastreamento dos arquivos ou qualidade dos commits;
- não existe manifesto ou lockfile, portanto não é possível determinar versões suportadas nem confirmar ou descartar CVEs das dependências do projeto;
- o PDF não foi executado no Adobe Acrobat/Reader nesta sessão; a presença do JavaScript foi confirmada estruturalmente, mas seu comportamento real no leitor-alvo ainda requer teste manual;
- a inspeção visual automatizada não ficou disponível nesta sessão. Observações de acessibilidade e layout abaixo são baseadas na estrutura do PDF e no código, não em uma homologação visual completa.

## 3. Stack e ferramentas identificadas

| Camada | Tecnologia | Uso observado |
|---|---|---|
| Linguagem principal | Python 3 | Geração, pós-processamento e validação do PDF |
| Geração de PDF | ReportLab | Canvas vetorial e campos AcroForm |
| Pós-processamento | pypdf | Clonagem do documento, `NeedAppearances` e JavaScript |
| Automação do formulário | Acrobat JavaScript | Derivados, bônus, experiência e idiomas |
| Formato de saída | PDF A4 interativo | Cinco páginas, voltado ao Adobe Acrobat/Reader |
| Documentação | Markdown | Análise do sistema, plano e relatório de implementação |

O ambiente usado na auditoria possui Python 3.13.9, ReportLab 4.4.10 e pypdf 6.7.3. Essas versões não estão declaradas pelo projeto e não devem ser tratadas como requisitos oficiais.

## 4. Estrutura e arquitetura atuais

```text
src/vampiro_sheet/
  data.py             Dados estáticos do sistema
  layout.py           Constantes e primitivas visuais
  fields.py           Fábrica de campos AcroForm
  build.py            Composição das cinco páginas e pós-processamento
  calculations.js     Regras executadas no leitor de PDF
scripts/
  build_sheet.py      Ponto de entrada para geração
  validate_sheet.py   Validação estrutural mínima
docs/
  analise_sistema_vampiro_3e.md
  plano_ficha_interativa.md
  relatorio_final_implementacao.md
build/                 PDF intermediário
dist/                  PDF final
```

### Avaliação arquitetural

Pontos positivos confirmados:

- dados, desenho, campos e cálculos estão em módulos distintos;
- as cinco páginas estão separadas em funções de responsabilidade reconhecível;
- listas centrais de Atributos, Habilidades, Disciplinas, Antecedentes e clãs são dirigidas por dados;
- não há backend, banco, API, autenticação ou estado remoto desnecessário;
- o PDF final é pequeno para o volume de campos, cerca de 342 KB;
- não há arte, logotipo ou moldura extraída do livro no código do layout.

Limites atuais:

- `build.py` concentra composição, regras de posicionamento e definição semântica de campos em 319 linhas;
- o modelo de domínio está implícito em listas e nomes de campo, sem uma camada validável de regras;
- a mesma regra de geração existe em Python e JavaScript, criando duas fontes de verdade;
- cálculos importantes só existem dentro do PDF, o que dificulta testes automatizados.

## 5. Achados detalhados

### AT-01 — Regras vampíricas são aplicadas a todos os tipos de personagem

- **Classificação:** falha confirmada.
- **Severidade:** alta.
- **Localização:** `src/vampiro_sheet/data.py:7`; `src/vampiro_sheet/build.py:39`; `src/vampiro_sheet/calculations.js:37-68`.
- **Evidência:** o menu oferece vampiro, mortal, carniçal e antagonista, mas `recalcVampiro()` não consulta `tipo_personagem`. Ele sempre calcula Humanidade, Força de Vontade, limite de Característica, sangue máximo e gasto por turno a partir da geração.
- **Impacto técnico:** mortais, carniçais e antagonistas recebem valores derivados vampíricos incorretos. O suporte declarado no relatório de implementação não corresponde ao comportamento do formulário.
- **Correção recomendada:** definir perfis de personagem explícitos e condicionar campos, padrões e cálculos por tipo. Para regras não determinadas pelo livro, manter campos manuais e indicar claramente que não há cálculo.
- **Risco de regressão:** alto; a mudança afeta JavaScript, valores padrão, visibilidade ou bloqueio de campos e testes de todos os perfis.

### AT-02 — Campos terminais duplicados tornam a atualização ambígua

- **Classificação:** falha confirmada.
- **Severidade:** alta.
- **Localização:** `src/vampiro_sheet/build.py:82-85`, `src/vampiro_sheet/build.py:111-121`, `src/vampiro_sheet/calculations.js:14-17`.
- **Evidência:** `sangue_max` e `sangue_turno` são criados uma vez na página 1 e novamente na página 2. O AcroForm possui 484 campos de topo e quatro objetos terminais independentes para esses dois nomes, sem relação pai/filhos. `get_fields()` reporta 482 porque colapsa as chaves duplicadas.
- **Impacto técnico:** `this.getField(name)` pode resolver apenas uma das instâncias; valores exibidos em páginas diferentes podem divergir. A validação atual mascara a duplicidade.
- **Correção recomendada:** usar um único campo com múltiplos widgets corretamente relacionados, ou nomes únicos com sincronização explícita e testada. Adicionar teste que rejeite nomes terminais duplicados.
- **Risco de regressão:** médio; exige preservar a exibição nas duas páginas e a compatibilidade com dados já salvos.

### AT-03 — Pontos visuais e valores numéricos podem divergir

- **Classificação:** falha confirmada.
- **Severidade:** alta.
- **Localização:** `src/vampiro_sheet/build.py:23-31`; `src/vampiro_sheet/fields.py:69-82`; `docs/relatorio_final_implementacao.md:89`.
- **Evidência:** cada Atributo e Habilidade possui cinco checkboxes independentes e um campo textual numérico. Os cálculos leem somente o campo com sufixo `_val`; nenhuma rotina sincroniza as caixas com esse valor.
- **Impacto técnico:** a ficha pode exibir simultaneamente duas pontuações diferentes para a mesma característica. Como os checkboxes também não impõem sequência, é possível marcar apenas o quinto ponto ou combinações descontínuas.
- **Correção recomendada:** escolher uma fonte de verdade. Opções seguras são grupos de rádio que representem 0–5, ou campo numérico validado que atualize a representação visual. Centralizar a conversão e testar ida e volta.
- **Risco de regressão:** alto; altera muitos nomes e widgets e pode afetar preenchimentos existentes.

### AT-04 — A “Auditoria de Criação” não audita os valores da ficha

- **Classificação:** falha confirmada.
- **Severidade:** alta.
- **Localização:** `src/vampiro_sheet/build.py:219-235`; ausência correspondente em `src/vampiro_sheet/calculations.js`.
- **Evidência:** totais de Atributos, Habilidades, Disciplinas, Antecedentes e Virtudes são campos de texto editáveis. O JavaScript não soma as características nem verifica 7/5/3, 13/9/5, 3, 5 e 7. Também não valida Habilidade acima de 3, Aparência 0 para Nosferatu, geração, Caitiff ou restrições da 14ª geração, embora `docs/plano_ficha_interativa.md:67-71` planeje esses avisos.
- **Impacto técnico:** erros centrais de criação passam sem alerta e os totais podem ser preenchidos de forma inconsistente com a ficha.
- **Correção recomendada:** implementar um motor de validação puro, gerar avisos específicos e tornar totais derivados somente leitura. Separar pontos iniciais, pontos de bônus e valores finais para evitar inferências incorretas.
- **Risco de regressão:** alto; a regra precisa distinguir criação de progressão e exceções de clã/tipo.

### AT-05 — Campos supostamente numéricos aceitam qualquer texto

- **Classificação:** falha confirmada.
- **Severidade:** alta.
- **Localização:** `src/vampiro_sheet/fields.py:81-82`; `src/vampiro_sheet/calculations.js:7-11`.
- **Evidência:** `numeric()` apenas chama `text()`; não define máscara, formato, intervalo ou validação. `nf()` converte entrada inválida silenciosamente para zero. Isso afeta características, bônus, defeitos e experiência.
- **Impacto técnico:** erros de digitação viram zero sem indicação, valores negativos ou acima dos limites são aceitos e cálculos aparentemente válidos podem estar incorretos.
- **Correção recomendada:** adicionar validação de tecla e formato compatível com Acrobat, limites por domínio e mensagens de erro. Não converter entrada inválida em zero sem sinalização.
- **Risco de regressão:** médio; dados antigos com texto não numérico precisarão de tratamento.

### AT-06 — O modelo de dano permite estados contraditórios

- **Classificação:** falha confirmada.
- **Severidade:** média.
- **Localização:** `src/vampiro_sheet/build.py:129-141`.
- **Evidência:** cada nível de Vitalidade contém três checkboxes independentes para contusão, letal e agravado. Mais de um tipo pode ser marcado no mesmo nível e a penalidade atual planejada não é calculada.
- **Impacto técnico:** o estado de dano pode ser impossível ou ambíguo; não há fonte confiável para derivar a penalidade.
- **Correção recomendada:** representar cada nível com estado exclusivo, incluindo vazio, ou usar um campo por caixa com valores de exportação controlados. Calcular a penalidade a partir do pior nível ocupado.
- **Risco de regressão:** médio; altera widgets de uma área isolada, mas pode quebrar dados preenchidos.

### AT-07 — Defeitos e bônus dependem de totais manuais

- **Classificação:** falha confirmada.
- **Severidade:** média.
- **Localização:** `src/vampiro_sheet/build.py:237-270`; `src/vampiro_sheet/calculations.js:56-64`.
- **Evidência:** as oito linhas de Qualidades/Defeitos não têm tipo controlado nem pontos validados. `defeitos_total` e `bonus_gasto` são digitados manualmente; o cálculo só soma esses totais. O aviso chama 7 de “limite recomendado”, enquanto a análise registra que não deve haver mais de 7 pontos adicionais.
- **Impacto técnico:** o saldo não é auditável a partir dos itens listados e pode contrariar a regra documentada.
- **Correção recomendada:** usar tipo controlado, pontos numéricos e soma automática por categoria; tratar 7 como limite de criação e permitir exceção apenas com sinalização explícita do Narrador.
- **Risco de regressão:** médio.

### AT-08 — Moralidade e Virtudes alternativas não têm representação inequívoca

- **Classificação:** falha confirmada.
- **Severidade:** média.
- **Localização:** `src/vampiro_sheet/data.py:156`; `src/vampiro_sheet/build.py:56`, `src/vampiro_sheet/build.py:73-88`; `src/vampiro_sheet/calculations.js:38-44`.
- **Evidência:** “Consciência/Convicção” e “Autocontrole/Instinto” são valores combinados, sem seleção de qual Virtude está ativa. Há apenas “Humanidade” ou “Trilha”; não existe campo estruturado para nome e valor da Trilha. Para Trilha, o campo derivado recebe literalmente `manual`.
- **Impacto técnico:** a ficha não consegue expressar com clareza qual conjunto de Virtudes é usado e mistura valor numérico com texto de estado.
- **Correção recomendada:** separar escolha da Virtude, valor de moralidade e nome da Trilha. Manter cálculo manual quando a regra depender da Trilha, mas usar campo numérico próprio e aviso separado.
- **Risco de regressão:** médio.

### AT-09 — Geração selecionada e Antecedente Geração são independentes

- **Classificação:** falha confirmada.
- **Severidade:** média.
- **Localização:** `src/vampiro_sheet/build.py:45-46`, `src/vampiro_sheet/build.py:73-75`; `src/vampiro_sheet/calculations.js:46-50`.
- **Evidência:** a geração é escolhida diretamente no cabeçalho e o Antecedente Geração é outro campo livre. Não há cálculo nem aviso relacionando os dois, apesar de `docs/analise_sistema_vampiro_3e.md:203-207` registrar essa relação.
- **Impacto técnico:** combinações incompatíveis podem produzir reserva de sangue e limites incorretos.
- **Correção recomendada:** durante a criação, derivar ou validar geração a partir do Antecedente e do perfil aplicável; oferecer modo manual claramente identificado para personagens antigos e antagonistas.
- **Risco de regressão:** alto, pois precisa preservar casos fora do padrão inicial.

### AT-10 — Campos identificados na análise não chegaram ao layout

- **Classificação:** falha confirmada por divergência interna.
- **Severidade:** média.
- **Localização:** `docs/analise_sistema_vampiro_3e.md:19-38`, `docs/analise_sistema_vampiro_3e.md:369-379`; `src/vampiro_sheet/build.py:34-88`, `src/vampiro_sheet/build.py:143-161`.
- **Evidência:** não existem campos explícitos para idade aparente, idade real/nascimento, data do Abraço, seita/facção e restrição alimentar. A tabela de armas não inclui Tipo nem Ocultabilidade, ambos requeridos pela análise. Alguns dados poderiam ser improvisados em áreas livres, mas não possuem campo próprio.
- **Impacto técnico:** reduz completude, descoberta e consistência do preenchimento.
- **Correção recomendada:** revisar a matriz requisito–campo e adicionar ou justificar formalmente cada exclusão. Evitar depender de campos genéricos para dados mecânicos ou de consulta frequente.
- **Risco de regressão:** baixo a médio; o principal risco é redistribuição do layout.

### AT-11 — JavaScript usa polling permanente e silencia todos os erros

- **Classificação:** risco potencial com evidência no código.
- **Severidade:** média.
- **Localização:** `src/vampiro_sheet/calculations.js:71-74`.
- **Evidência:** `app.setInterval("recalcVampiro()", 1000)` recalcula e reatribui valores a cada segundo. O identificador do timer não é armazenado e qualquer exceção é descartada por `catch (e) {}`.
- **Impacto técnico:** trabalho contínuo enquanto o documento está aberto, dificuldade de diagnóstico e possível alteração recorrente do estado do documento. O impacto real precisa ser medido no Acrobat/Reader.
- **Correção recomendada:** usar ações de cálculo/validação associadas aos campos ou ao evento de cálculo do AcroForm. Registrar falhas de modo compatível com o leitor durante desenvolvimento e remover apenas mensagens destinadas a depuração na versão final.
- **Risco de regressão:** médio; eventos de formulário têm diferenças entre leitores e exigem homologação no alvo.

### AT-12 — Checkboxes são marcados como obrigatórios pelo PDF

- **Classificação:** falha confirmada.
- **Severidade:** média.
- **Localização:** `src/vampiro_sheet/fields.py:53-66` e todos os usos de `checkbox()`.
- **Evidência:** 254 campos `/Btn` possuem flag `/Ff = 2`, correspondente a `Required`. Nenhum campo textual está marcado como obrigatório.
- **Impacto técnico:** a semântica do formulário é incorreta; ferramentas de acessibilidade ou eventual submissão podem exigir todas as caixas, inclusive todos os pontos e danos.
- **Correção recomendada:** definir flags explicitamente e marcar como obrigatório apenas o que for realmente obrigatório. Adicionar asserção sobre flags na validação.
- **Risco de regressão:** baixo.

### AT-13 — O PDF não possui estrutura de acessibilidade

- **Classificação:** falha confirmada.
- **Severidade:** média.
- **Localização:** `src/vampiro_sheet/layout.py`, `src/vampiro_sheet/fields.py`; catálogo do PDF final.
- **Evidência:** o catálogo não contém `/Lang`, `/MarkInfo` nem `/StructTreeRoot`; páginas não têm `/Tabs`. Tooltips usam identificadores técnicos como `atributo_Fisicos_Forca_1`, não rótulos humanos. Tamanhos de texto chegam a 5,5 pt em `src/vampiro_sheet/build.py:279-287`.
- **Impacto técnico:** navegação por teclado e leitura por tecnologia assistiva não têm ordem ou semântica garantida; nomes anunciados são pouco compreensíveis; textos pequenos podem prejudicar impressão e baixa visão.
- **Correção recomendada:** definir idioma, ordem de tabulação, tooltips legíveis e, se a stack permitir, estrutura marcada. Aumentar textos informativos ou reduzir densidade. Validar com Acrobat Accessibility Checker e teclado.
- **Risco de regressão:** médio; ReportLab pode limitar PDF marcado e exigir outra estratégia de geração ou pós-processamento.

### AT-14 — A validação existente produz confiança excessiva

- **Classificação:** falha confirmada.
- **Severidade:** média.
- **Localização:** `scripts/validate_sheet.py:28-60`.
- **Evidência:** o script confere cinco páginas, presença de AcroForm, mínimo de 400 campos, 14 nomes e qualquer árvore `/Names`. Ele não confirma que a árvore contém JavaScript válido, não detecta nomes duplicados, flags, fórmulas, opções, valores, coordenadas, campos faltantes do sistema ou execução no Acrobat.
- **Impacto técnico:** a mensagem `validation ok` ocorre mesmo com os problemas AT-01 a AT-13.
- **Correção recomendada:** dividir testes em unidade de regras, contrato do PDF, snapshots estruturais e homologação no leitor. Validar nomes únicos, flags, opções, JavaScript esperado e matriz completa de campos.
- **Risco de regressão:** baixo; testes mais rigorosos inicialmente revelarão falhas existentes.

### AT-15 — Não há suíte de testes do domínio

- **Classificação:** risco confirmado de cobertura insuficiente.
- **Severidade:** alta.
- **Localização:** todo o projeto; existe apenas `scripts/validate_sheet.py`.
- **Evidência:** não há diretório de testes nem testes de geração, regras, exceções de clã, perfis, limites, nomes de campos ou compatibilidade de versões.
- **Impacto técnico:** alterações em centenas de campos e fórmulas têm alto risco de regressão silenciosa.
- **Correção recomendada:** extrair cálculos para funções puras com vetores de teste; testar geração e contrato do AcroForm; criar uma checklist reproduzível de Adobe Reader para os fluxos críticos.
- **Risco de regressão:** baixo para adicionar testes; médio quando o código precisar ser refatorado para ficar testável.

### AT-16 — O projeto não declara dependências nem ambiente suportado

- **Classificação:** falha confirmada.
- **Severidade:** alta.
- **Localização:** raiz do projeto; ausência de `pyproject.toml`, `requirements.txt` e lockfile.
- **Evidência:** imports externos de `reportlab` e `pypdf` existem em `src/vampiro_sheet/build.py:5-8`, mas não há instalação reproduzível.
- **Impacto técnico:** outro desenvolvedor ou CI não consegue reproduzir o build com versões conhecidas; a análise de vulnerabilidades não pode ser vinculada às dependências efetivamente suportadas.
- **Correção recomendada:** criar `pyproject.toml` com faixa de Python, dependências mínimas testadas e ferramentas de desenvolvimento; usar lockfile ou constraints para builds reproduzíveis e scanner automatizado de dependências.
- **Risco de regressão:** baixo, desde que as versões sejam obtidas a partir de uma matriz testada.

### AT-17 — O diretório não está preparado como repositório público

- **Classificação:** falha confirmada.
- **Severidade:** alta.
- **Localização:** raiz do projeto.
- **Evidência:** `.git` existe, mas está vazio e `git rev-parse` falha. Não existem README, `.gitignore`, licença, arquivos de contribuição, configuração de CI ou metadados de pacote. Há `__pycache__` dentro de `src/`.
- **Impacto técnico:** não há histórico auditável nem instruções de uso; artefatos locais podem ser publicados por engano; o projeto não pode ser clonado e reproduzido profissionalmente no estado atual.
- **Correção recomendada:** inicializar Git após definir exclusões, criar documentação de instalação/uso/arquitetura, escolher licença para o código, configurar CI e excluir caches/artefatos transitórios do rastreamento.
- **Risco de regressão:** baixo. O risco principal é publicar arquivos indevidos antes da higiene inicial.

### AT-18 — Material-fonte pode impedir publicação aberta

- **Classificação:** risco potencial de publicação, não infração confirmada.
- **Severidade:** alta.
- **Localização:** `vampiro-a-mascara-modulo-basico-3a-edicao-biblioteca-elfica.pdf`; `_extracted_text.txt`.
- **Evidência:** o diretório contém o livro completo com 12,3 MB e uma extração textual com 1,5 MB. Não há licença ou autorização anexada.
- **Impacto técnico/profissional:** esses arquivos podem ser enviados ao GitHub junto com o código e gerar remoção, reclamação de direitos autorais ou percepção negativa no portfólio.
- **Correção recomendada:** não publicar os dois arquivos sem autorização explícita. Adicioná-los ao `.gitignore`, documentar como fornecer uma fonte local opcional e revisar também os direitos de distribuição do PDF derivado, nome da marca e conteúdo textual.
- **Risco de regressão:** baixo para o código; alto para a rastreabilidade da análise se a documentação não indicar claramente a origem e o procedimento local.

### AT-19 — Dados sem uso e regras duplicadas aumentam risco de divergência

- **Classificação:** risco potencial e código morto confirmado.
- **Severidade:** baixa.
- **Localização:** `src/vampiro_sheet/data.py:126-141`, `src/vampiro_sheet/data.py:158-173`, `src/vampiro_sheet/data.py:210-249`; `src/vampiro_sheet/calculations.js:19-35`.
- **Evidência:** `CLAN_DISCIPLINES`, `GENERATION_TABLE` e `MERITS_FLAWS` não são consumidos fora de `data.py`; somente as chaves da tabela de geração alimentam o menu. Os valores da mesma tabela são repetidos manualmente no JavaScript.
- **Impacto técnico:** uma correção pode ser aplicada em Python e esquecida no JavaScript; listas aparentemente funcionais podem induzir manutenção inútil.
- **Correção recomendada:** definir uma única fonte de dados e gerar a representação JavaScript ou os scripts de campo a partir dela. Remover dados mortos ou usá-los em validações e interface.
- **Risco de regressão:** médio ao unificar geração de código; baixo ao remover itens comprovadamente sem uso após testes.

### AT-20 — Tratamento de erros e saída de build são mínimos

- **Classificação:** sugestão de robustez baseada em risco potencial.
- **Severidade:** baixa.
- **Localização:** `src/vampiro_sheet/build.py:290-315`; `scripts/build_sheet.py:1-11`.
- **Evidência:** falhas de leitura/escrita e pós-processamento não ganham contexto; o destino personalizado não tem diretório pai criado; o PDF final é sobrescrito diretamente, sem escrita atômica. Os metadados usam autor `Codex` e criador `anonymous`.
- **Impacto técnico:** diagnósticos de CI são pobres e uma falha durante a escrita pode deixar saída incompleta. Metadados não representam o autor do portfólio.
- **Correção recomendada:** validar caminhos, escrever em temporário e substituir ao concluir, fornecer mensagens de erro contextualizadas e parametrizar metadados do projeto.
- **Risco de regressão:** baixo.

### AT-21 — Documentação de planejamento está desatualizada

- **Classificação:** falha confirmada de documentação.
- **Severidade:** baixa.
- **Localização:** `docs/plano_ficha_interativa.md:105-155`, `docs/plano_ficha_interativa.md:195-200`; `docs/relatorio_final_implementacao.md:65-90`.
- **Evidência:** o plano ainda apresenta perguntas já respondidas e promete radios, seletores de prioridade, penalidade de Vitalidade e alertas que não foram implementados. O relatório final chama a checagem estrutural limitada de “validação realizada” sem explicitar que o JavaScript não foi executado no Acrobat.
- **Impacto técnico/profissional:** leitores não conseguem distinguir backlog, decisão e funcionalidade entregue.
- **Correção recomendada:** separar requisitos, ADRs, backlog e estado implementado; manter uma matriz de rastreabilidade e registrar limitações de teste com precisão.
- **Risco de regressão:** baixo.

## 6. Segurança e dependências

### Confirmado

- não há chamadas HTTP, APIs, banco de dados, autenticação, autorização ou armazenamento remoto;
- não foram encontrados segredos, tokens, senhas ou credenciais no código e na documentação pesquisável;
- o JavaScript incorporado acessa somente campos do documento e timer do Acrobat; não há ação de rede, arquivo, execução externa ou submissão;
- o gerador não recebe entrada de usuário remoto.

### Não determinável no estado atual

- vulnerabilidades de dependências, porque não há manifesto nem versões declaradas;
- segurança do arquivo-fonte obtido de terceiros;
- comportamento do JavaScript sob as configurações de segurança de diferentes versões do Acrobat/Reader.

### Recomendação

Após criar o manifesto, habilitar scanner de dependências no CI e revisão automatizada. Tratar PDF com JavaScript como conteúdo ativo, documentar essa característica no README e fornecer, se útil, uma variante sem automação.

## 7. Performance e consumo de recursos

O build é pequeno e linear; não há gargalo relevante confirmado em Python. O PDF final tem 5 páginas, 484 widgets e aproximadamente 342 KB. O risco principal está no `setInterval` de um segundo, que mantém o cálculo ativo durante todo o uso do documento. Substituir polling por eventos reduz trabalho e torna o comportamento determinístico.

Não há evidência de problema de memória, concorrência ou I/O em escala, pois o projeto gera um único documento local.

## 8. Usabilidade, impressão e acessibilidade

### Confirmado

- páginas são A4, 595,28 × 841,89 pontos;
- margens e paleta são centralizadas em `layout.py`;
- o documento oferece campos multilinha, menus e caixas de seleção;
- a estrutura é fixa, portanto “responsividade” web não se aplica.

### Riscos e lacunas

- textos de 5,5–7 pt podem ficar pouco legíveis em impressão;
- não há semântica acessível, idioma, ordem de tabulação ou tooltips amigáveis;
- as duas representações de pontuação e o modelo de dano favorecem estados contraditórios;
- 254 checkboxes aparecem tecnicamente como obrigatórios;
- a qualidade visual final ainda precisa ser homologada em impressão A4 a 100%, tela pequena e Acrobat/Reader.

## 9. Priorização e dependências técnicas

| Ordem | Etapa | Dependência | Objetivo |
|---:|---|---|---|
| 0 | Higiene de publicação | nenhuma | Impedir publicação de material protegido e criar base Git reproduzível |
| 1 | Modelo de domínio | decisão sobre perfis e regras manuais | Uma fonte de verdade para tipos, características, geração e validações |
| 2 | Contrato de campos | modelo de domínio | Nomes únicos, tipos, limites, estados exclusivos e acessibilidade básica |
| 3 | Motor de cálculo | contrato de campos | Cálculos testáveis, condicionais por perfil e sem polling |
| 4 | Layout e UX | contrato estável | Integrar campos faltantes, legibilidade, tabulação e impressão |
| 5 | Testes e CI | regras e build estabilizados | Prevenir regressões e validar artefato em cada alteração |
| 6 | Documentação de portfólio | comportamento validado | README, arquitetura, demonstração, decisões e limitações verdadeiras |

## 10. Plano de execução por etapas

### Etapa 0 — Preparar publicação sem expor material indevido

1. Confirmar direitos do PDF final e excluir livro/extrato do futuro repositório público.
2. Criar `.gitignore` para fonte local, extração, `__pycache__`, build intermediário e temporários.
3. Inicializar um repositório Git funcional.
4. Definir licença apenas para o código e conteúdo original que o autor pode licenciar.

### Etapa 1 — Formalizar regras e perfis

1. Criar modelos explícitos para vampiro jogador, mortal, carniçal e antagonista.
2. Definir quais regras são automáticas, manuais ou não aplicáveis a cada perfil.
3. Unificar tabela de geração, clãs, Disciplinas, Qualidades/Defeitos e limites.
4. Criar testes puros para fórmulas e exceções antes de alterar o PDF.

### Etapa 2 — Corrigir o contrato AcroForm

1. Eliminar campos terminais duplicados.
2. Substituir entrada dupla por uma fonte de verdade sincronizada.
3. Adicionar validação numérica, limites e estados exclusivos de dano.
4. Separar Virtudes, Trilha e valor de moralidade.
5. Corrigir flags obrigatórias, tooltips e ordem de tabulação.

### Etapa 3 — Implementar validação funcional

1. Calcular os totais de criação a partir dos campos reais.
2. Validar prioridades, máximos, clã, geração e exceções.
3. Somar Qualidades, Defeitos, bônus e experiência a partir dos itens.
4. Condicionar cálculos ao tipo de personagem.
5. Substituir timer por eventos de cálculo do formulário.

### Etapa 4 — Completar e revisar layout

1. Fechar a matriz de campos da análise do sistema.
2. Incluir dados de identidade e combate atualmente ausentes.
3. Revisar densidade, fontes, impressão em escala real e fluxo de teclado.
4. Verificar cinco páginas no Acrobat/Reader em Windows e, secundariamente, em leitor sem JavaScript.

### Etapa 5 — Engenharia de qualidade

1. Adicionar `pyproject.toml`, versões suportadas e instalação de desenvolvimento.
2. Criar testes de unidade e contrato do PDF.
3. Configurar lint, formatação, testes e build em CI.
4. Validar dependências com ferramenta automatizada.
5. Tornar o build reproduzível e conferir o artefato gerado no CI.

### Etapa 6 — Apresentação de portfólio

1. Escrever README com problema, solução, arquitetura, instalação, geração, validação e screenshots próprios.
2. Documentar decisões importantes e limitações conhecidas.
3. Incluir demonstração sem redistribuir o livro-fonte.
4. Substituir metadados genéricos pelo autor e versão do projeto.
5. Preparar release versionada com PDF, checksum e notas de compatibilidade.

## 11. Critérios de aceitação

### Fidelidade funcional

- cada tipo de personagem executa apenas regras aplicáveis ao seu perfil;
- todos os campos da matriz de requisitos estão implementados ou têm exclusão justificada;
- nenhuma característica possui duas fontes de verdade divergentes;
- geração e Antecedente Geração são consistentes no modo de criação;
- totais e avisos de criação são derivados, não digitados manualmente;
- Qualidades/Defeitos respeitam soma e limite configurados;
- dano tem um estado inequívoco por nível;
- Trilhas continuam manuais quando a regra não puder ser determinada sem escolha do Narrador.

### Contrato do PDF

- não há nomes terminais duplicados;
- campos calculados são somente leitura quando apropriado;
- campos numéricos rejeitam entrada inválida e respeitam intervalos;
- flags `Required`, `ReadOnly` e exportação correspondem à semântica real;
- JavaScript não usa polling contínuo e não falha silenciosamente;
- o arquivo abre, edita, salva, reabre e imprime corretamente no Adobe Reader.

### Qualidade e testes

- fórmulas possuem testes unitários com casos normais, limites e exceções;
- validação estrutural cobre todos os campos obrigatórios, tipos, opções, flags e duplicidades;
- build e testes executam em ambiente limpo a partir do manifesto;
- CI falha quando o PDF diverge do contrato esperado;
- homologação manual do Acrobat/Reader está documentada por versão e sistema operacional.

### Acessibilidade e usabilidade

- idioma do documento está definido;
- ordem de tabulação segue o fluxo visual;
- tooltips são compreensíveis para pessoas, não identificadores internos;
- texto e campos permanecem legíveis em A4 a 100%;
- navegação por teclado e Acrobat Accessibility Checker não apresentam bloqueadores acordados.

### Publicação

- repositório Git funcional, com histórico limpo e commits coerentes;
- README, licença do código, `.gitignore`, manifesto e instruções reproduzíveis presentes;
- livro e extração textual ausentes do repositório público, salvo autorização documentada;
- nenhuma credencial ou dado pessoal está presente;
- release contém somente arquivos que podem ser redistribuídos.

## 12. Verificações necessárias antes da publicação

1. Executar testes em ambiente novo, sem dependências previamente instaladas.
2. Gerar o PDF duas vezes e investigar diferenças não determinísticas.
3. Abrir no Adobe Reader, preencher todos os perfis, salvar, fechar e reabrir.
4. Confirmar cálculos após alteração de cada campo-fonte.
5. Testar JavaScript desabilitado e documentar degradação funcional.
6. Imprimir as cinco páginas em A4, escala 100%, monocromático e colorido.
7. Navegar integralmente por teclado e executar o verificador de acessibilidade do Acrobat.
8. Executar scanner de segredos, dependências e licença no repositório final.
9. Revisar juridicamente a redistribuição do PDF gerado e referências à marca.
10. Conferir que livro, extração, caches e artefatos intermediários não estão no commit.

## 13. Conclusão

O projeto tem uma base modular adequada ao tamanho atual e demonstra domínio prático de PDF vetorial, AcroForm e automação no Acrobat. Para se tornar um portfólio profissional, a prioridade não é ampliar o visual, mas garantir que o documento expresse um único estado mecânico válido, diferencie corretamente os quatro perfis suportados e possua testes capazes de comprovar isso. Em paralelo, a higiene de publicação e a exclusão do material-fonte precisam acontecer antes do primeiro push público.
