import click
from mtcli_market.controllers.profile_controller import obter_profile
from mtcli_market.views.profile_view import exibir_profile
from mtcli_market.conf import (
    SYMBOL,
    BARS,
    BLOCK,
    BY,
)


@click.command()
@click.version_option(package_name="mtcli-market")
@click.option("--symbol", "-s", default=SYMBOL, show_default=True, help="Ticker do ativo")
@click.option("--bars", "-b", default=BARS, show_default=True, help="Número de candles ou ticks a usar")
@click.option("--block", "-k", default=BLOCK, show_default=True, help="Tamanho de bloco de preço (em pontos)")
@click.option("--by", type=click.Choice(["time","ticks","volume"]), default=BY, show_default=True, help="Base para o profile: tempo, ticks ou volume")
def profile(symbol, bars, block, by):
    """Calcula e exibe o Market Profile de um ativo."""
    profile = obter_profile(symbol, bars, block, by)
    exibir_profile(profile, symbol, block)
