## Karaokê do Bar do Ivan - Lista de Músicas
Este repositório contém um scraper da lista de músicas do karaokê do [Bar do Ivan](https://maps.app.goo.gl/FGH5q5LbC2vxaPVz9), escrito em Python.

Além disso, a lista de músicas pode ser visualizada em um webapp React, que realiza chamadas a uma API desenvolvida com o pacote Python FastAPI.

# Inicializar API
```
cd scraper
pip install -r requirements.txt 
uvicorn api:app --reload
```

# Inicializar WebApp
```
cd webapp
npm install
npm run dev
```