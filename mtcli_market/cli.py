import click

from mtcli_market.conf import (
    BLOCK,
    BY,
    PERIOD,
    PERIODOS,
    SYMBOL,
)
from mtcli_market.controller import obter_profile
from mtcli_market.view import exibir_profile


@click.command()
@click.version_option(package_name="mtcli-market")
@click.option(
    "--symbol", "-s", default=SYMBOL, show_default=True, help="Ticker do ativo."
)
@click.option(
    "--periodos",
    "-po",
    default=PERIODOS,
    show_default=True,
    type=int,
    help="Número de períodos (barras) usados para o cálculo.",
)
@click.option(
    "--block",
    "-k",
    default=BLOCK,
    show_default=True,
    type=float,
    help="Tamanho de bloco de preço (em pontos).",
)
@click.option(
    "--by",
    type=click.Choice(["time", "ticks", "volume"]),
    default=BY,
    show_default=True,
    help="Base para o profile: time, ticks ou volume.",
)
@click.option(
    "--initial-balance",
    "-ib",
    default=30,
    show_default=True,
    type=int,
    help="Duração (em minutos) do Initial Balance (IB).",
)
@click.option(
    "--va-percent",
    "-va",
    default=0.7,
    show_default=True,
    type=float,
    help="Percentual (0..1) para cálculo da Value Area.",
)
@click.option(
    "--period",
    "-p",
    default=PERIOD,
    show_default=True,
    help="Timeframe para o cálculo do profile. Aceita valores customizados como 2d (2 dias).",
)
@click.option(
    "--verbose",
    "-vv",
    is_flag=True,
    default=False,
    show_default=True,
    help="Modo verboso (texto descritivo).",
)
def profile(symbol, periodos, block, by, initial_balance, va_percent, period, verbose):
    """Calcula e exibe o Market Profile de um ativo, com saída textual acessível."""
    # Validação simples de entrada
    if va_percent <= 0 or va_percent > 1:
        raise click.BadParameter("va-percent deve estar no intervalo (0, 1].")
    if block <= 0:
        raise click.BadParameter("block deve ser maior que zero.")
    resultado = obter_profile(
        symbol=symbol,
        bars=periodos,
        block=float(block),
        by=by,
        ib_minutes=initial_balance,
        va_percent=va_percent,
        timeframe=period,
    )
    exibir_profile(resultado, symbol=symbol, verbose=verbose)


if __name__ == "__main__":
    profile()
