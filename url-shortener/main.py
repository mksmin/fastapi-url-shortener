from typing import Annotated

import uvicorn
from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    status,
    Depends,
)
from fastapi.responses import (
    RedirectResponse,
)
from schemas.short_url import ShortUrl


app = FastAPI(title="URL Shortener")


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Hello {name}",
        "docs": str(docs_url),
    }


SHORT_URLS = [
    ShortUrl(
        target_url="https://www.example.com",
        slug="example",
    ),
    ShortUrl(
        target_url="https://www.google.com",
        slug="search",
    ),
]


@app.get(
    "/short-urls/",
    response_model=list[ShortUrl],
)
def read_short_urls_list():
    return SHORT_URLS


def prefetch_short_url(
    slug: str,
) -> ShortUrl:
    url: ShortUrl | None = next(
        (url for url in SHORT_URLS if url.slug == slug),
        None,
    )
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Slug {slug!r} not found",
    )


@app.get("/r/{slug}")
@app.get("/r/{slug}/")
def redirect_to_target_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
):

    return RedirectResponse(
        url=url.target_url,
    )


@app.get(
    "/short-urls/{slug}",
    response_model=ShortUrl,
)
def read_short_url_details(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
) -> ShortUrl:
    return url


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
