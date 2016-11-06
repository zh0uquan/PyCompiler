#!/usr/bin/env python3.5
# -*- coding: utf-8
from compiler07 import NodeVistor, Lexer, Parser


class RNPTranslator(NodeVistor):
    def __init__(self, parser):
        self.parser = parser

    def visit_Num(self, node):
        return str(node.value)

    def visit_BinOp(self, node):
        return '{left} {right} {op}'.format(
                left=self.visit(node.left),
                right=self.visit(node.right),
                op=node.op.value
            )

    def translate(self):
        tree = self.parser.parse()
        return self.visit(tree)


class LispTranslator(NodeVistor):
    def __init__(self, parser):
        self.parser = parser

    def visit_Num(self, node):
        return str(node.value)

    def visit_BinOp(self, node):
        return '({op} {left} {right})'.format(
                left=self.visit(node.left),
                right=self.visit(node.right),
                op=node.op.value
            )

    def translate(self):
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    while True:
        try:
            option = input('input option 1.RNP 2.LISP\n')
        except EOFError:
            break
        if option not in ['1', '2']:
            print('wrong option')
            continue

        while True:
            try:
                text = input('>>>')
            except EOFError:
                break
            except KeyboardInterrupt:
                exit(1)

            if not text:
                continue

            lexer = Lexer(text)
            parser = Parser(lexer)
            if option == '1':
                translator = RNPTranslator(parser)
            elif option == '2':
                translator = LispTranslator(parser)
            result = translator.translate()
            print(result)

if __name__ == '__main__':
    main()
