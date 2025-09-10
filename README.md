# FastAPI URL Shortener

[![Python checks 🐍](https://img.shields.io/github/actions/workflow/status/mksmin/fastapi-url-shortener/python-checks.yaml?branch=master&label=Python%20checks%20%F0%9F%90%8D&style=for-the-badge&logo=github&logoColor=white)](https://github.com/mksmin/fastapi-url-shortener/actions/workflows/python-checks.yaml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Code style: Black](https://img.shields.io/badge/Code%20style-Black-000000?style=for-the-badge&logo=python&logoColor=white)](https://github.com/psf/black)
[![Lint: Ruff](https://img.shields.io/badge/Lint-Ruff-2b9348?style=for-the-badge&logo=python&logoColor=white)](https://github.com/astral-sh/ruff-action)
[![Type checking: mypy](https://img.shields.io/badge/Type%20checking-mypy-007ec6?style=for-the-badge&logo=python&logoColor=white)](https://github.com/python/mypy)
[![Dependencies: Poetry](https://img.shields.io/badge/dependencies-Poetry-8A2BE2?style=for-the-badge&logo=python&logoColor=white)](https://github.com/python-poetry/poetry)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-555555?style=for-the-badge&logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mksmin/fastapi-url-shortener/master.svg)](https://results.pre-commit.ci/latest/github/mksmin/fastapi-url-shortener/master)
[![codecov](https://codecov.io/gh/OWNER/REPO/branch/master/graph/badge.svg)](https://app.codecov.io/gh/OWNER/REPO)

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
