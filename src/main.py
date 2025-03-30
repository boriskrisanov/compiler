import parser
from tokenizer import tokenize

src = """let x = 1
if (x > 0) {
    x = x + 1
}
"""

print(tokenize(src))
# print(parser.parse(tokenize(src)))