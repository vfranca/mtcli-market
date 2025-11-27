import click

from mtcli_market.conf import (
    IB,
    LIMIT,
    PERIOD,
    RANGE,
    SYMBOL,
    VOLUME,
)
from mtcli_market.controller import obter_profile
from mtcli_market.view import exibir_profile


@click.command()
@click.version_option(package_name="mtcli-market")
@click.option(
    "--symbol", "-s", default=SYMBOL, show_default=True, help="Codigo do ativo."
)
@click.option(
    "--period",
    "-p",
    default=PERIOD,
    show_default=True,
    help="Timeframe para o calculo do profile.",
)
@click.option(
    "--limit",
    "-l",
    default=LIMIT,
    show_default=True,
    type=int,
    help="Número de períodos .",
)
@click.option(
    "--range",
    "-r",
    default=RANGE,
    show_default=True,
    type=float,
    help="Tamanho do range de preco.",
)
@click.option(
    "--volume",
    "-v",
    type=click.Choice(["tpo", "tick", "real"]),
    default=VOLUME,
    show_default=True,
    help="Base para o profile.",
)
@click.option(
    "--initial-balance",
    "-ib",
    default=IB,
    show_default=True,
    type=int,
    help="Duracao em minutos do Initial Balance.",
)
@click.option(
    "--va-percent",
    "-va",
    default=0.7,
    show_default=True,
    type=float,
    help="Percentual da Value Area.",
)
@click.option(
    "--verbose",
    "-vv",
    is_flag=True,
    default=False,
    show_default=True,
    help="Modo verboso (texto descritivo).",
)
def profile(symbol, period, limit, range, volume, initial_balance, va_percent, verbose):
    """Calcula e exibe o Market Profile de um ativo."""
    # Validação simples de entrada
    if va_percent <= 0 or va_percent > 1:
        raise click.BadParameter("va-percent deve estar no intervalo (0, 1].")
    if range <= 0:
        raise click.BadParameter("Range deve ser maior que zero.")
    resultado = obter_profile(
        symbol=symbol,
        period=period,
        limit=int(limit),
        range=float(range),
        volume=volume,
        ib_minutes=initial_balance,
        va_percent=va_percent,
    )
    exibir_profile(resultado, symbol=symbol, verbose=verbose)


if __name__ == "__main__":
    profile()
