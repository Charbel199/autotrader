from dataclasses import dataclass


@dataclass
class Symbol(object):
    """
    Symbol
    """
    PrimarySymbol: str = ''
    SecondarySymbol: str = ''
    SymbolPair: str = ''
