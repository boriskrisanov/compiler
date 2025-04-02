from dataclasses import dataclass
from enum import Enum
from tokenizer import Token, TokenKind
from typing import Self

class Operator(Enum):
    EQUALS = 0
    GREATER_THAN = 1

type ExprTermNode = IntLiteralNode | IdentifierNode

@dataclass
class IntLiteralNode:
    value: int

@dataclass
class IdentifierNode:
    name: str

@dataclass
class Node:
    tokens_consumed: int

@dataclass
class ExprNode:
    lhs: Self
    rhs: Self
    operator: Operator

type StatementNode = AssignmentNode

@dataclass
class AssignmentNode(Node):
    identifier: str
    expr: ExprNode

@dataclass
class IfNode(Node):
    condition: ExprNode
    statement_list: list[StatementNode]

# <expr_term> ::= <int_literal> | <identifier>
# <expr> ::= <expr_term> | <expr> <operator> <expr>
# <assignment> ::= let <identifier> = <expr>
# <statement> ::= <assignment>;
# <statement_list> ::= <statement> | <statement> <statement_list>
# <if> ::= if (<expr>) { <statement_list> }

# Match terminal node
def match_token(tokens: list[Token], pos: int, lookahead: int, token_kind: TokenKind) -> Token | None:
    if pos + lookahead < len(tokens) and tokens[pos + lookahead].kind == token_kind:
        return tokens[pos + lookahead]
    
    return None

def match_expr_term(tokens: list[Token], pos: int, lookahead: int) -> ExprTermNode | None:
    integer_literal = match_token(tokens, pos, lookahead, TokenKind.INTEGER_LITERAL)
    if integer_literal is not None:
        return integer_literal.value
    
    identifier = match_token(tokens, pos, lookahead, TokenKind.IDENTIFIER)
    if identifier is not None:
        return identifier.value
    
    return None

def match_assignment(tokens: list[Token], pos: int) -> AssignmentNode | None:
    let_keyword = match_token(tokens, pos, 0, TokenKind.KEYWORD_LET)
    identifier = match_token(tokens, pos, 1, TokenKind.IDENTIFIER)
    assignment_operator = match_token(tokens, pos, 2, TokenKind.ASSIGNMENT_OPERATOR)
    expr = match_expr(tokens, pos, 3)

    if let_keyword is None or assignment_operator is None or expr is None or identifier is None:
        return None
    
    return AssignmentNode(5, identifier.value, expr)

def match_statement(tokens: list[Token], pos: int) -> StatementNode | None:
    assignment = match_assignment(tokens, pos)
    if assignment is None:
        return None
    
    semicolon = match_token(tokens, pos, assignment.tokens_consumed, TokenKind.SEMICOLON)
    if semicolon is None:
        return None
    
    return AssignmentNode(2, assignment.identifier, assignment.expr)

def match_if(tokens: list[Token], pos: int) -> IfNode | None:
    if_keyword = match_token(tokens, pos, 0, TokenKind.KEYWORD_IF)
    return None

def parse(tokens: list[Token]):
    ast: list = []

    while tokens[0].kind != TokenKind.EOF:
        assignment_node = match_assignment(tokens, 0)
        if_node = match_if(tokens, 0)
        if assignment_node is not None:
            ast.append(assignment_node)
            tokens = tokens[assignment_node.tokens_consumed:]
        else:
            print("Failed to parse. Remaining tokens: " + str(tokens))
            break

    return ast