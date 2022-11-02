# API DRF

## Usando a API

Instalando dependencias

```
python -m venv .venv --upgrade-deps
source .venv/bin/activate
pip install -r .venv/bin/activate
```

Fanzendo as migrações iniciais

```
python migrate
```

Subindo o servidor

```
python manage.py 3001
```

## Rotas

### 1) POST login

- URL

```curl
http://localhost:3001/login
```

```json
{
  "email": "nicolas@mail.com",
  "password": "12345678"
}
```

- Response

```json
{
  "uuid": "cc9e750e-0426-41ac-a898-c68a532d58a2"
  "message": "Login success"
}
```

Com os cookies

> * jwt-access-token=<Token>; expires=Wed, 02 Nov 2022 19:22:56 GMT; HttpOnly; Max-Age=5; Path=/; SameSite=Lax
> * jwt-refresh-token=<Token>; expires=Wed, 02 Nov 2022 19:23:51 GMT; HttpOnly; Max-Age=60; Path=/token; SameSite=Lax


### 2) POST register

- URL

```curl
http://localhost:3001/register
```

- Request

```json
{
  "name": "Nicolas",
  "email": "nicolas@mail.com",
  "password": "123456!!",
  "password2": "123456!!"
}
```

- Response

```json
{
  "id": "cc9e750e-0426-41ac-a898-c68a532d58a2"
}
```

Com os `cookies`

> * jwt-access-token=<Token>; expires=Wed, 02 Nov 2022 19:22:56 GMT; HttpOnly; Max-Age=5; Path=/; SameSite=Lax
> * jwt-refresh-token=<Token>; expires=Wed, 02 Nov 2022 19:23:51 GMT; HttpOnly; Max-Age=60; Path=/token; SameSite=Lax


### 3) GET get user info

- URL

```curl
http://localhost:3001/users
```

- Request

> Precida apenas do `cookie jwt-access-token`.

- Response

```json
{
  "uuid": "cc9e750e-0426-41ac-a898-c68a532d58a2",
  "name": "Nicolas",
  "email": "nicolas@mail.com",
}
```

### 4) POST logout

- URL

```curl
http://localhost:3001/token/logout
```

- Response

```json
{"detail":"Successfully logged out."}
```

Com os `cookies`

> * jwt-access-token=""; expires=Wed, 02 Nov 2022 19:22:56 GMT; HttpOnly; Max-Age=0; Path=/; SameSite=Lax
> * jwt-refresh-token=""; expires=Wed, 02 Nov 2022 19:23:51 GMT; HttpOnly; Max-Age=0; Path=/token; SameSite=Lax


### 5) POST refresh

- URL

```curl
http://localhost:3001/token/refresh
```

- Request

> Precida apenas do `cookie jwt-refresh-token`.

- Response

```json
{"access_token_expiration":"2022-11-02T19:32:13.267003Z"}
```

Com os `cookies`

> * jwt-access-token=<Token>; expires=Wed, 02 Nov 2022 19:22:56 GMT; HttpOnly; Max-Age=5; Path=/; SameSite=Lax
