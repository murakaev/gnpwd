import typer
from gnpwd.generators.password import generate_password

app = typer.Typer()

@app.command()
def generate(
    length: int = typer.Option(12, "-l/--length", min=8, help="Password length (minimum 8)"),
    digits: bool = typer.Option(False, "--use-digits", help="Include digits (0-9)"),
    capital: bool = typer.Option(False, "--use-capital", help="Include uppercase letters (A-Z)"),
    symbols: bool = typer.Option(False, "--symbols", help="Include symbols (!@#$%&*)"),
    no_ambiguous: bool = typer.Option(False, "--ambiguous/--exclude-ambiguous",
                                     help="Exclude ambiguous characters like 0O1lI|2Z5S"),
):
    """Generate a cryptographically secure random password."""
    try:
        password = generate_password(
            length=length,
            use_digits=digits,
            use_capital=capital,
            use_symbols=symbols,
            exclude_ambiguous=no_ambiguous
        )
        typer.echo(f"Generated password: {password}")
    except ValueError as e:
        typer.secho(str(e), fg=typer.colors.RED)

if __name__ == "__main__":
    app()