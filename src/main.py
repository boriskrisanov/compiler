import parser
from tokenizer import tokenize

src = """let x = 1
x = x + 1
let y = 2
y = y + 2

"""

print(tokenize(src))
# print(parser.parse(tokenize(src)))