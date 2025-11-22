import os

from mtcli.conf import config

SYMBOL = os.getenv("SYMBOL", config["DEFAULT"].get("symbol", fallback="WIN$N"))
PERIOD = os.getenv("PERIOD", config["DEFAULT"].get("period", fallback="M1"))
PERIODOS = int(os.getenv("PERIODOS", config["DEFAULT"].getint("periodos", fallback=566)))
BLOCK = int(os.getenv("BLOCK", config["DEFAULT"].getint("block", fallback=100)))
BY = os.getenv("BY", config["DEFAULT"].get("by", fallback="time"))
IB = int(os.getenv("IB", config["DEFAULT"].getint("ib", fallback=30)))
DIGITOS = int(os.getenv("DIGITOS", config["DEFAULT"].getint("digitos", fallback=0)))
