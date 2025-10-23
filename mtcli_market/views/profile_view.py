import click

def exibir_profile(profile, symbol, block):
    if not profile:
        click.echo("Nenhum dado para exibir.")
        return

    click.echo(f"\nMarket Profile para {symbol} — bloco = {block}\n")
    # Ordenar por preço descendente para visual tipo gráfico vertical
    ordered = sorted(profile.items(), key=lambda x: x[0], reverse=True)

    max_count = max(count for _, count in ordered)
    max_bar_len = 50  # largura máxima da barra no terminal

    for price, count in ordered:
        # comprimento da barra proporcional
        bar = "#" * int((count / max_count) * max_bar_len)
        click.echo(f"{price:>10.2f} | {count:>7} {bar}")

