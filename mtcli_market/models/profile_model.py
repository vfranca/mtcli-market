import MetaTrader5 as mt5
from collections import defaultdict
from datetime import datetime
from mtcli.mt5_context import mt5_conexao
from mtcli.logger import setup_logger


log = setup_logger()


def calcular_profile(symbol, bars, block, by):
    """
    Retorna dict onde chave = preço do bloco, valor = contagem (tempo / ticks / volume).
    """
    with mt5_conexao():
        # Exemplo: usar candles
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, bars)
        if rates is None:
            return {}

        profile = defaultdict(int)

        for r in rates:
            # preço médio ou close
            price = r["close"]
            # calcular “faixa” de bloco
            faixa = round(price / block) * block

            if by == "time":
                # cada candle representa “1 unidade de tempo”
                profile[faixa] += 1
            elif by == "ticks":
                # usar tick_volume
                profile[faixa] += r.get("tick_volume", 0)
            elif by == "volume":
                # usar volume real, se disponível
                volume = r.get("real_volume", None)
                if volume is None:
                                volume = r.get("tick_volume", 0)
                profile[faixa] += volume

    return dict(profile)

