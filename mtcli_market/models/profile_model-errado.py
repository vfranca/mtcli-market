import MetaTrader5 as mt5
from collections import defaultdict, OrderedDict
from datetime import datetime
from math import floor
from mtcli.mt5_context import mt5_conexao
from mtcli.logger import setup_logger
from typing import Dict, Any, Tuple, List, Union

log = setup_logger()

def _mapear_timeframe(timeframe: Union[str, int]) -> int:
    mapping = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
    }
    if isinstance(timeframe, int):
        minutos = timeframe
    else:
        tf_str = str(timeframe).upper().strip()
        if tf_str in mapping:
            return mapping[tf_str]
        minutos = 1
        if tf_str.endswith("M"):
            try:
                minutos = int(tf_str[:-1])
            except ValueError:
                minutos = 1
        elif tf_str.endswith("H"):
            try:
                minutos = int(tf_str[:-1]) * 60
            except ValueError:
                minutos = 60
        elif tf_str.endswith("D"):
            try:
                minutos = int(tf_str[:-1]) * 1440
            except ValueError:
                minutos = 1440
        else:
            minutos = 1

    # conversão aproximada para timeframe MT5
    if minutos <= 1:
        return mt5.TIMEFRAME_M1
    elif minutos <= 5:
        return mt5.TIMEFRAME_M5
    elif minutos <= 15:
        return mt5.TIMEFRAME_M15
    elif minutos <= 30:
        return mt5.TIMEFRAME_M30
    elif minutos <= 60:
        return mt5.TIMEFRAME_H1
    elif minutos <= 240:
        return mt5.TIMEFRAME_H4
    else:
        return mt5.TIMEFRAME_D1

def _block_price(price: float, block: float) -> float:
    return round(round(price / block) * block, 8)

def _range_blocks(low: float, high: float, block: float) -> List[float]:
    low_b = floor(low / block) * block
    high_b = floor(high / block) * block
    blocks = []
    b = high_b
    while b >= low_b:
        blocks.append(round(b, 8))
        b -= block
    return blocks

def _distribuir_volume_uniforme(volume: float, blocks: List[float]) -> Dict[float, float]:
    if not blocks:
        return {}
    per = volume / len(blocks)
    return {b: per for b in blocks}

def calcular_profile(symbol: str, bars: int, block: float, by: str = 'time', ib_minutes: int = 30, va_percent: float = 0.7, timeframe: Union[str, int] = "M1") -> Dict[str, Any]:
    tf = _mapear_timeframe(timeframe)
    with mt5_conexao():
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars)
        if rates is None:
            log.warning('Nenhum dado retornado para %s', symbol)
            return {}

        profile = defaultdict(float)
        tpo = defaultdict(int)
        rates_list = sorted(list(rates), key=lambda r: r['time'])

        for r in rates_list:
            low = r.get('low', r.get('close'))
            high = r.get('high', r.get('close'))
            blocks = _range_blocks(low, high, block)

            if by == 'time':
                for b in blocks:
                    tpo[b] += 1
                    profile[b] += 1
            elif by == 'ticks':
                tick_vol = r.get('tick_volume', 0) or 0
                dist = _distribuir_volume_uniforme(tick_vol, blocks)
                for b, v in dist.items():
                    profile[b] += v
                    tpo[b] += 1
            elif by == 'volume':
                vol = r.get('real_volume', None) or r.get('tick_volume', 0) or 0
                dist = _distribuir_volume_uniforme(vol, blocks)
                for b, v in dist.items():
                    profile[b] += v
                    tpo[b] += 1

        ordered_profile = OrderedDict(sorted(profile.items(), key=lambda x: x[0], reverse=True))
        ordered_tpo = OrderedDict(sorted(tpo.items(), key=lambda x: x[0], reverse=True))

        total_volume = sum(ordered_profile.values())
        poc = max(ordered_profile.items(), key=lambda x: x[1])[0] if ordered_profile else None

        def calcular_value_area(profile_map: Dict[float, float], percent: float) -> Tuple[float, float, List[float]]:
            if not profile_map or percent <= 0 or percent > 1:
                return (None, None, [])
            target = sum(profile_map.values()) * percent
            items = sorted(profile_map.items(), key=lambda x: x[1], reverse=True)
            acum, selected = 0, []
            for price, vol in items:
                selected.append((price, vol))
                acum += vol
                if acum >= target:
                    break
            prices = [p for p, _ in selected]
            return (max(prices), min(prices), prices)

        vah, val, va_prices = (None, None, [])
        if ordered_profile:
            vah, val, va_prices = calcular_value_area(dict(ordered_profile), va_percent)

        hvn, lvn = [], []
        if ordered_profile:
            vols = list(ordered_profile.values())
            media = sum(vols) / len(vols)
            desvio = (sum((v - media) ** 2 for v in vols) / len(vols)) ** 0.5
            for price, vol in ordered_profile.items():
                if vol >= media + desvio:
                    hvn.append(price)
                elif vol <= max(0.0, media - desvio):
                    lvn.append(price)

        ib_high, ib_low = None, None
        if rates_list:
            start_time = rates_list[0]['time']
            limite = start_time + ib_minutes * 60
            ib_rates = [r for r in rates_list if r['time'] <= limite]
            if ib_rates:
                ib_high = max(r['high'] for r in ib_rates)
                ib_low = min(r['low'] for r in ib_rates)

        return {
            'profile': ordered_profile,
            'tpo': ordered_tpo,
            'total_volume': total_volume,
            'poc': poc,
            'vah': vah,
            'val': val,
            'va_prices': va_prices,
            'hvn': hvn,
            'lvn': lvn,
            'ib': {'high': ib_high, 'low': ib_low} if ib_high and ib_low else None,
            'rates_count': len(rates_list),
            'by': by,
            'block': block,
            'va_percent': va_percent,
            'timeframe': timeframe,
        }
