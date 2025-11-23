from mtcli.logger import setup_logger
from mtcli_market.model import calcular_profile

log = setup_logger()


def obter_profile(
    symbol: str,
    bars: int,
    block: float,
    by: str,
    ib_minutes: int = 30,
    va_percent: float = 0.7,
    timeframe: str = "M1",
):
    # Normalização / validação de parâmetros
    if by not in ("time", "ticks", "volume"):
        log.warning("Parâmetro 'by' inválido (%s). Usando 'time'.", by)
        by = "time"

    if va_percent <= 0 or va_percent > 1:
        log.warning("va_percent fora de intervalo (0,1]. Usando 0.7.")
        va_percent = 0.7

    try:
        block = float(block)
    except Exception:
        log.warning("block inválido (%s). Usando 1.0.", block)
        block = 1.0

    resultado = calcular_profile(
        symbol=symbol,
        bars=bars,
        block=block,
        by=by,
        ib_minutes=ib_minutes,
        va_percent=va_percent,
        timeframe=timeframe,
    )
    return resultado
