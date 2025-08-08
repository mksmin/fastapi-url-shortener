import typer
from typing import Annotated
from rich import print

from api.api_v1.auth.services import redis_tokens

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
):
    """
    Check if the passed token exists
    """
    print(
        f"Token [bold]{token}[/bold] ",
        (
            "[green]exists[/green]"
            if redis_tokens.token_exists(token)
            else "[red]does not exist[/red]"
        ),
    )


@app.command(name="list")
def list_tokens():
    """
    List all tokens
    """
    if data := redis_tokens.get_tokens():
        print("Available API tokens:")
        for i, token in enumerate(data, start=1):
            print(f"{i}. [bold]{token}[/bold]")

    else:
        print("You don't have any tokens yet. ")
