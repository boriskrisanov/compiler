from dataclasses import dataclass
from enum import Enum
from typing import Any
import re

class TokenKind(Enum):
    KEYWORD_LET = 1
    ASSIGNMENT_OPERATOR = 2
    INTEGER_LITERAL = 3
    IDENTIFIER = 4
    KEYWORD_IF = 5
    OPEN_BRACKET = 6
    CLOSE_BRACKET = 7
    OPEN_BRACE = 8
    CLOSE_BRACE = 9
    OPEN_ANGLE_BRACKET = 10
    SEMICOLON = 254
    EOF = 255

@dataclass
class Token:
    kind: TokenKind
    value: Any = None

    def __repr__(self):
        return str(self.kind) if self.value is None else f"{str(self.kind)}({str(self.value)})"

@dataclass
class TokenRule:
    regex: re.Pattern
    token_kind: TokenKind

# TODO: Don't use regex for simple tokens for performance?
let_regex = re.compile(r"let(?!\w)")
if_regex = re.compile(r"if(?!\w)")
equals_regex = re.compile(r"=")
open_angle_bracket_regex = re.compile(r">")
open_bracket_regex = re.compile(r"\(")
close_bracket_regex = re.compile(r"\)")
open_brace_regex = re.compile(r"\{")
close_brace_regex = re.compile(r"\}")
identifier_regex = re.compile(r"[^\d]?[Aa-zZ]([Aa-zZ]|[0-9]*)(?!\w)")
integer_literal_regex = re.compile(r"\d+")

rules = [
    TokenRule(let_regex, TokenKind.KEYWORD_LET),
    TokenRule(equals_regex, TokenKind.ASSIGNMENT_OPERATOR),
    TokenRule(if_regex, TokenKind.KEYWORD_IF),
    TokenRule(open_bracket_regex, TokenKind.OPEN_BRACKET),
    TokenRule(close_bracket_regex, TokenKind.CLOSE_BRACKET),
    TokenRule(open_brace_regex, TokenKind.OPEN_BRACE),
    TokenRule(close_brace_regex, TokenKind.CLOSE_BRACE),
    TokenRule(open_angle_bracket_regex, TokenKind.OPEN_ANGLE_BRACKET),
]

def match_token(regex, string: str, tokens: list[Token], token_kind: TokenKind) -> tuple[str, bool]:
    match = re.search(regex, string)
    if match is not None and match.start() == 0:
        tokens.append(Token(token_kind))
        string = string[(match.end()):]
        string = string.lstrip(" ")
        return (string, True)
    
    return (string, False)

def tokenize(string: str) -> list[Token]:
    tokens: list[Token] = []

    while len(string) > 0:
        if string.startswith("\n"):
            string = string[1:]
            continue

        if string.startswith(";"):
            string = string[1:]
            tokens.append(Token(TokenKind.SEMICOLON))
            continue
        
        match = False
        for rule in rules:
            string, match = match_token(rule.regex, string, tokens, rule.token_kind)
            if match:
                break
        if match:
            continue        

        # Did not match anything, assume identifier or literal
        identifier_match = re.search(identifier_regex, string)
        if identifier_match is not None and identifier_match.start() == 0:
            tokens.append(Token(TokenKind.IDENTIFIER, str(string[0:identifier_match.end()])))
            string = string[(identifier_match.end()):]
            string = string.lstrip(" ")
            continue
        
        integer_literal_match = re.search(integer_literal_regex, string)
        if integer_literal_match is not None and integer_literal_match.start() == 0:
            tokens.append(Token(TokenKind.INTEGER_LITERAL, int(string[0:integer_literal_match.end()])))
            string = string[integer_literal_match.end():]
            string = string.lstrip(" ")
            continue

        # Might be unreachable if properly implemented?
        print("Failed to tokenize")
        break


    tokens.append(Token(TokenKind.EOF))

    return tokens