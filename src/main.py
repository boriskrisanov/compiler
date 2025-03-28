import parser
from tokenizer import tokenize

src = "let x = 1" + "\n"

print(tokenize(src))
print(parser.parse(tokenize(src)))