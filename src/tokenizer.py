from dataclasses import dataclass
from enum import Enum
from typing import Any

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

def tokenize(string: str) -> list[Token]:
    tokens: list[Token] = []
    buffer = ""

    for c in string:
        if c in [" ", "=", "\n"]:
            # Keywords and literals
            if buffer == "let":
                tokens.append(Token(TokenKind.KEYWORD_LET))
                buffer = ""
            elif buffer != "":
                if buffer.isnumeric():
                    tokens.append(Token(TokenKind.INTEGER_LITERAL, int(buffer)))
                else:
                    tokens.append(Token(TokenKind.IDENTIFIER, buffer))
                buffer = ""

        if c != " ":
            buffer += c

        if buffer == "=":
            tokens.append(Token(TokenKind.ASSIGNMENT_OPERATOR))
            buffer = ""
        
    tokens.append(Token(TokenKind.EOF))

    return tokens