# FastAPI URL Shortener

[![Python checks 🐍](https://github.com/mksmin/fastapi-url-shortener/actions/workflows/python-checks.yaml/badge.svg)](https://github.com/mksmin/fastapi-url-shortener/actions/workflows/python-checks.yaml)

## Develop

Check GitHub Actions after any push

### Setup:
Right click `url-shortener` -> Mark directory as ->  Sources Root

### Install dependencies

Install packages:
```shell
poetry install
```

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
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
