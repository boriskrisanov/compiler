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

let_regex = re.compile(r"let(?!\\w)")
equals_regex = re.compile(r"=")
identifier_regex = re.compile(r"[^\\d]?[Aa-zZ]([Aa-zZ]|[0-9]*)(?!\\w)")
integer_literal_regex = re.compile(r"\d+")

def tokenize(string: str) -> list[Token]:
    tokens: list[Token] = []

    while len(string) > 0:
        let_match = re.search(let_regex, string)
        if let_match is not None and let_match.start() == 0:
            tokens.append(Token(TokenKind.KEYWORD_LET))
            string = string[(let_match.end() + 1):]
            string.lstrip()
            continue

        equals_match = re.search(equals_regex, string)
        if equals_match is not None and equals_match.start() == 0:
            tokens.append(Token(TokenKind.ASSIGNMENT_OPERATOR))
            string = string[(equals_match.end() + 1):]
            string.lstrip()
            continue

        # Did not match anything, assume identifier or literal
        identifier_match = re.search(identifier_regex, string)
        if identifier_match is not None and identifier_match.start() == 0:
            tokens.append(Token(TokenKind.IDENTIFIER, str(string[0:identifier_match.end()])))
            string = string[(identifier_match.end() + 1):]
            string.lstrip()
            continue
        
        integer_literal_match = re.search(integer_literal_regex, string)
        if integer_literal_match is not None and integer_literal_match.start() == 0:
            tokens.append(Token(TokenKind.INTEGER_LITERAL, int(string[0:integer_literal_match.end()])))
            string = string[(integer_literal_match.end() + 1):]
            string.lstrip()
            continue

        # Might be unreachable if properly implemented?
        print("Failed to tokenize")
        break


    tokens.append(Token(TokenKind.EOF))

    return tokens