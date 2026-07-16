# Comandos Git sugeridos

Execute dentro da pasta do projeto:

```bash
git init

git add 0_criar_banco.sql config.py banco.py requirements.txt .env.example .gitignore
git commit -m "Cria estrutura inicial e modelagem do banco"

git add 1_extrair.py
git commit -m "Implementa extracao e carga da camada raw"

git add 2_transformar.py
git commit -m "Implementa transformacao e carga da camada silver"

git add 3_analise.ipynb 3_gold_consultas.sql
git commit -m "Implementa camada gold e perguntas de negocio"

git add README.md COMANDOS_GITHUB.md docs/ data/sample/ data/raw/README.md
git commit -m "Finaliza documentacao e organizacao do projeto"

git branch -M main
git remote add origin LINK_DO_REPOSITORIO
git push -u origin main
```
