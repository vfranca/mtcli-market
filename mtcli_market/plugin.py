from mtcli_market.commands.profile import profile


def register(cli):
    cli.add_command(profile, name="market")
