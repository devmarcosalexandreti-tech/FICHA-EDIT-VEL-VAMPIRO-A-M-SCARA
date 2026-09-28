# Relatório de pré-publicação

Data da verificação: 28 de setembro de 2026.

## Escopo

Esta revisão preparou o projeto para uma futura publicação pública sem criar repositório remoto, commit ou push. O gerador, as regras da ficha e o artefato funcional não foram alterados nesta etapa.

## Segurança

- A busca por padrões de tokens, chaves, senhas, chaves privadas e credenciais não encontrou ocorrências nos arquivos candidatos ao primeiro commit.
- A busca por e-mails, telefones, documentos e outros dados pessoais não encontrou ocorrências nos arquivos candidatos.
- O repositório Git ainda não possui commits nem arquivos rastreados. Portanto, não existe histórico Git contendo segredos a remover.
- Não há autenticação, serviços externos, banco de dados ou variáveis de ambiente no projeto.
- O livro-fonte e o texto extraído permanecem somente como material local e estão explicitamente ignorados.
- Caches, cobertura, ambientes virtuais, logs, arquivos temporários e configurações locais de editores e agentes estão ignorados.

Nenhuma credencial versionada foi encontrada e, com as evidências disponíveis, não há indicação de rotação. Uma nova varredura deve ser feita imediatamente antes do primeiro commit caso novos arquivos sejam adicionados.

## Arquivos de publicação

Criados:

- .gitattributes
- CONTRIBUTING.md
- docs/relatorio_pre_publicacao.md

Modificados:

- .gitignore
- .github/workflows/ci.yml
- README.md
- pyproject.toml

Não foi criado .env.example porque o projeto não usa variáveis de ambiente. Não foi criada uma LICENSE porque os termos ainda não foram definidos pelo responsável.

## Instalação verificada

~~~powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
~~~

Após a instalação, as verificações são executadas com Ruff, unittest, Coverage.py, Node.js, o gerador e o validador do PDF.

## Resultados verificados

- Instalação editável em ambiente virtual limpo: concluída.
- Ruff lint: aprovado.
- Ruff format check: aprovado em 12 arquivos.
- Compilação Python com avisos tratados como erro: aprovada.
- Testes Python: 24 aprovados.
- Cobertura Python combinada: 99%, com medição de ramificações.
- Testes JavaScript: 17 aprovados.
- Geração e validação do PDF: aprovadas.
- Contrato do PDF: 5 páginas, 485 campos, AcroForm e JavaScript presentes.

## Integração contínua

O workflow usa permissões somente de leitura, cancela execuções obsoletas da mesma referência, limita a execução a 15 minutos, instala as dependências de teste, verifica lint, formatação e compilação, executa testes Python e JavaScript, gera o PDF e valida seu contrato.

O workflow não depende de secrets e não publica releases ou artefatos.

## Limitações e pendências

- Definir os termos de licenciamento e adicionar o arquivo LICENSE é condição para uma publicação pública com permissões claras.
- Fazer inspeção manual final da interatividade no Adobe Acrobat Reader.
- Confirmar que o uso e a distribuição do PDF gerado estão de acordo com os direitos aplicáveis às marcas e ao sistema de RPG.
- Capturas de tela não foram adicionadas porque não havia imagens aprovadas disponíveis.
- O histórico não pôde ser auditado além do estado atual porque ainda não existem commits.
- O pypdf 6.19 emite aviso de descontinuação para add_js. A dependência está limitada a versões abaixo de 7, portanto o funcionamento atual é preservado; a migração para add_open_action deve ser avaliada antes de permitir pypdf 7.

## Checklist de liberação

- [x] Segredos e dados pessoais pesquisados.
- [x] Material de consulta local excluído do versionamento.
- [x] Caches e arquivos gerados locais excluídos.
- [x] README com instalação, arquitetura, uso, testes e limitações.
- [x] Guia de contribuição.
- [x] Integração contínua com permissões mínimas.
- [x] PDF final mantido como artefato versionável.
- [ ] Licença escolhida e adicionada.
- [ ] Revisão manual final no Adobe Acrobat Reader concluída.
- [ ] Direitos de distribuição revisados pelo responsável.
- [ ] Primeiro commit revisado antes de qualquer publicação.
