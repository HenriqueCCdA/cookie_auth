# Client Python

Cliente python que acessa a `API python`. Olient faz a solicitação de um novo `Access Token` usndo o `Refresh Token` de forma transparente sem precisar explicitamnte acessar a rota `token/refresh`.


Instalando dependencias

```
python -m venv .venv --upgrade-deps
source .venv/bin/activate
pip install -r .venv/bin/activate
```

Usando o cliente

```
python client.py
```