import parser
from tokenizer import tokenize

src = """let x = 1
if (x > 0) {
x = 2
}

"""

print(tokenize(src))
# print(parser.parse(tokenize(src)))