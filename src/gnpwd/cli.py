import typer
from gnpwd.generators.password import generate_password

app = typer.Typer(help="gnpwd: A cryptographically secure password and passphrase generator.")

@app.command()
def password(
    length: int = typer.Option(12, "-l/--length", min=8, help="Password length (minimum 8)"),
    digits: bool = typer.Option(False, "--digits", help="Include digits (0-9)"),
    capital: bool = typer.Option(False, "--capital", help="Include uppercase letters (A-Z)"),
    symbols: bool = typer.Option(False, "--symbols", help="Include symbols (!@#$%&*)"),
    no_ambiguous: bool = typer.Option(False, "--ambiguous/--exclude-ambiguous",
                                     help="Exclude ambiguous characters like 0O1lI|2Z5S"),
):
    """Generate a secure password."""
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

@app.command()
def passphrase(
    word_count: int = typer.Option(6, "-w/--words", min=1, help="Number of words in the passphrase"),
):
    """Generate a secure passphrase."""
    from gnpwd.generators.passphrase import PassphraseGenerator

    generator = PassphraseGenerator(word_count=word_count)
    passphrase = generator.generate_passphrase()
    typer.echo(f"Generated passphrase: {passphrase}")

if __name__ == "__main__":
    app()