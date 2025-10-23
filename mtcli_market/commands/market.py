import click


@click.command("market")
@click.version_option(package_name="mtcli-market")
def market():
    """Ajuda do comando."""
    click.echo("funcionou!")


if __name__ == "__main__":
    market()
