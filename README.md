# SalesInsight PY

Mini-projeto de análise de dados de vendas com a biblioteca padrão do Python (`csv`, `json`, `os`, `random`).

## Requisitos
- Python 3.10 ou superior (não são necessárias bibliotecas externas)
- Git para versionamento

## Como executar
1. Abra esta pasta no VS Code.
2. Abra o terminal integrado.
3. Execute `python main.py` (no Windows, `py main.py` também costuma funcionar).
4. O programa cria `vendas.csv` com 150 registros caso o arquivo ainda não exista.
5. Os relatórios aparecem na pasta `outputs/`.

## Arquivos
- `main.py`: ponto de entrada e orquestração do pipeline.
- `modulo_vendas.py`: funções de geração, leitura, inspeção, limpeza, transformação, agregação, segmentação e exportação.
- `vendas.csv`: base sintética criada na primeira execução.
- `outputs/metricas_resumo.csv`: receita total por categoria.
- `outputs/estatisticas.json`: métricas gerais, por região e categoria, e gastos/segmentos dos clientes.

## Regras aplicadas
- Receita por registro = quantidade × preço unitário.
- Faixa de preço: Baixo (< R$ 500), Médio (R$ 500 a R$ 2.000, inclusive), Alto (> R$ 2.000).
- Segmentos: Bronze (< R$ 3.000), Prata (R$ 3.000 a R$ 8.000, inclusive), Ouro (> R$ 8.000).

## Git: exemplo de cinco commits
Faça cada etapa e registre o progresso:
1. `git init`
2. `git add README.md main.py modulo_vendas.py && git commit -m "feat: cria estrutura inicial"`
3. `git add modulo_vendas.py && git commit -m "feat: adiciona leitura e limpeza dos dados"`
4. `git add modulo_vendas.py && git commit -m "feat: calcula métricas e segmenta clientes"`
5. `git add main.py modulo_vendas.py README.md && git commit -m "feat: integra pipeline e exportação"`

Os comandos com `&&` funcionam no terminal do VS Code no Windows se estiver usando PowerShell moderno, Git Bash ou CMD; se necessário, execute-os um por vez.

## Observação
Este projeto atende ao pipeline de análise descritiva/agrupada descrito no enunciado. Não treina um modelo de machine learning para prever vendas futuras.
