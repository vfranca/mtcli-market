from mtcli.logger import setup_logger
from mtcli_market.model import calcular_profile

log = setup_logger()


def obter_profile(
    symbol: str,
    period: str,
    limit: int,
    range: float,
    volume: str,
    ib_minutes: int = 30,
    va_percent: float = 0.7,
):
    # Normalização / validação de parâmetros
    if volume not in ("tpo", "tick", "real"):
        log.warning(f"Parametro volume invalido {volume}. Usando tpo")
        volume = "tpo"

    if va_percent <= 0 or va_percent > 1:
        log.warning("va_percent fora de intervalo (0,1]. Usando 0.7")
        va_percent = 0.7

    try:
        range = float(range)
    except Exception:
        log.warning(f"range invalido {range}. Usando 1.0.")
        range = 1.0

    resultado = calcular_profile(
        symbol=symbol,
        limit=limit,
        block=range,
        by=volume,
        ib_minutes=ib_minutes,
        va_percent=va_percent,
        timeframe=period,
    )
    return resultado
