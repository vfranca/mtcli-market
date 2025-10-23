from mtcli_market.commands.market import market


def register(cli):
    cli.add_command(market)
