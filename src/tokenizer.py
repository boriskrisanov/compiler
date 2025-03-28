from dataclasses import dataclass
from enum import Enum
from typing import Any
import re

class TokenKind(Enum):
    KEYWORD_LET = 1
    ASSIGNMENT_OPERATOR = 2
    INTEGER_LITERAL = 3
    IDENTIFIER = 4
    EOF = 5

@dataclass
class Token:
    kind: TokenKind
    value: Any = None

@dataclass
class TokenMatch:
    token: Token
    start: int

let_regex = re.compile(r"let(?!(\\w)+)")

# def lookahead(str, pos, lookahead):
#     return str[pos + lookahead] if pos + lookahead < len(str) else ""

def match_tokens(regex: str, string: str, token_kind: TokenKind) -> list[TokenMatch]: 
    token_matches: list[TokenMatch] = []

    match = re.search(let_regex, string)
    while match is not None:
        token = Token(token_kind)
        token_matches.append(TokenMatch(token, match.start))
        string = string[:match.start()] + string[(match.end() + 1):]

        match = re.search(let_regex, string)

    return token_matches

def tokenize(string: str) -> list[Token]:
    token_matches: list[TokenMatch] = []

    token_matches += match_tokens(let_regex, string, TokenKind.KEYWORD_LET)

    tokens = list(map(lambda t: t.token, token_matches))
    tokens.append(Token(TokenKind.EOF))

    return tokens