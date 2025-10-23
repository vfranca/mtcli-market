from mtcli_market.models.profile_model import calcular_profile


def obter_profile(symbol, bars, block, by):
    resultado = calcular_profile(symbol, bars, block, by)
    return resultado
