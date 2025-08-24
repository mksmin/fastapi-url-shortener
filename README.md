# FastAPI URL Shortener

## Develop

Check GitHub Actions after any push

### Setup:
Right click `url-shortener` -> Mark directory as ->  Sources Root

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Install

Install packages:
```shell
poetry install
```

### Run

Go to work dir:
```shell
cd url-shortener
```

Run dev server:
```shell
fastapi dev
```

## Snippets
```shell
python -c 'import secrets;print(secrets.token_urlsafe(16))'
```
