from typing import Annotated

import typer
from rich import print

from api.api_v1.auth.services import redis_tokens as tokens

app = typer.Typer(
    name="token",
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Tokens management",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(
            help="Token to check",
        ),
    ],
) -> None:
    """
    Check if the passed token exists
    """
    print(
        f"Token [bold]{token}[/bold] ",
        (
            "[green]exists[/green]"
            if tokens.token_exists(token)
            else "[red]does not exist[/red]"
        ),
    )


@app.command(name="list")
def list_tokens() -> None:
    """
    List all tokens
    """
    if data := tokens.get_tokens():
        print("Available API tokens:")
        for i, token in enumerate(data, start=1):
            print(f"{i}. [bold]{token}[/bold]")

    else:
        print("You don't have any tokens yet. ")


@app.command()
def add(
    token: Annotated[
        str,
        typer.Argument(help="Token for save in db")
    ],
) -> None:
    """
    Save a token to storage
    """
    tokens.add_token(token=token)
    print(
        f"Token [bold]{token[:10]}...[/bold] saved",
    )


@app.command()
def create() -> None:
    """
    Create and save a token in storage
    """
    new_token = tokens.generate_and_save_token()
    print(
        f"Token [bold]{new_token}[/bold] was created and saved",
    )


@app.command()
def rm(
    token: Annotated[
        str,
        typer.Argument(help="Token to delete"),
    ],
) -> None:
    """
    Delete a token
    """
    if not tokens.token_exists(token):
        print(f"Token [bold]{token}[/bold] [red]does not exist[/red]")
        return

    tokens.delete_token(token=token)
    print(
        f"Token [bold]{token[:10]}...[/bold] was deleted",
    )
