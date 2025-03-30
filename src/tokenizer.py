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

    def __repr__(self):
        return str(self.kind) if self.value is None else f"{str(self.kind)}({str(self.value)})"

@dataclass
class TokenMatch:
    token: Token
    start: int

    def __gt__(self, other):
        return self.start > other.start
    
    def __eq__(self, other):
        return self.start == other.start

let_regex = re.compile(r"let(?!(\\w)+)")
equals_regex = re.compile(r"=")

def match_tokens(regex: str, string: str, token_kind: TokenKind) -> list[TokenMatch]: 
    token_matches: list[TokenMatch] = []

    match = re.search(regex, string)
    while match is not None:
        token = Token(token_kind)
        token_matches.append(TokenMatch(token, match.start()))
        string = string[:match.start()] + string[(match.end() + 1):]

        match = re.search(let_regex, string)

    return token_matches

def tokenize(string: str) -> list[Token]:
    token_matches: list[TokenMatch] = []

    token_matches += match_tokens(let_regex, string, TokenKind.KEYWORD_LET)
    token_matches += match_tokens(equals_regex, string, TokenKind.ASSIGNMENT_OPERATOR)

    print(token_matches)

    token_matches.sort(reverse=True)
    tokens = list(map(lambda t: t.token, token_matches))
    tokens.append(Token(TokenKind.EOF))

    return tokens