from dataclasses import dataclass
from tokenizer import Token, TokenKind

@dataclass
class Node[T]:
    node: T
    tokens_consumed: int

@dataclass
class AssignmentNode:
    identifier: str
    expr: int

type ASTNode = AssignmentNode

# <expr> ::= <int_literal>
# <assignment> ::= let <identifier> = <expr>

# Match terminal node
def match_token(tokens: list[Token], pos: int, lookahead: int, token_kind: TokenKind) -> Token | None:
    if pos + lookahead < len(tokens) and tokens[pos + lookahead].kind == token_kind:
        return tokens[pos + lookahead]
    
    return None

def match_assignment(tokens: list[Token], pos: int) -> Node[AssignmentNode] | None:
    let_keyword = match_token(tokens, pos, 0, TokenKind.KEYWORD_LET)
    identifier = match_token(tokens, pos, 1, TokenKind.IDENTIFIER)
    assignment_operator = match_token(tokens, pos, 2, TokenKind.ASSIGNMENT_OPERATOR)
    int_literal = match_token(tokens, pos, 3, TokenKind.INTEGER_LITERAL)

    if let_keyword is None or assignment_operator is None or int_literal is None or identifier is None:
        return None
    
    return Node(AssignmentNode(identifier.value, int_literal.value), 4)

def parse(tokens: list[Token]):
    ast: list = []

    while tokens[0].kind != TokenKind.EOF:
        assignment_node = match_assignment(tokens, 0)
        if assignment_node is not None:
            ast.append(assignment_node.node)
            tokens = tokens[assignment_node.tokens_consumed:]
        else:
            print("Failed to parse. Remaining tokens: " + str(tokens))
            break

    return ast