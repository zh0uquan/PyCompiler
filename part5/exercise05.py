#!/usr/bin/env python3.5
# -*- coding: utf-8

INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF', 'LPAREN', 'RPAREN'
)


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
                type=self.type,
                value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """
        Return a multidigit int from the input
        """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        print(result)
        return int(result)

    def get_next_token(self):
        # boundary
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            self.error()

        return Token(EOF, None)


class Interprter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invaild syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        factor : INTEGER
        Return an INTEGER value.
        """
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value

        if token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            if result is None:
                raise self.error()
            return result

    def order(self):
        """
        order  : factor((MUL | DIV)factor)*
        Return an INTEGER value.
        """
        result = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result *= self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result /= self.factor()
        return result

    def expr(self):
        """
        Arithmetic expression parser / interpreter.
        expr   : order((PLUS | MINUS)order)*
        order  : factor((MUL | DIV)factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        result = self.order()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.order()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.order()
        return result


def main():
    while True:
        try:
            text = input('\033[34m>>> \033[0m')
        except EOFError:
            break

        if not text:
            continue

        lexer = Lexer(text)
        interprter = Interprter(lexer)
        result = interprter.expr()
        print(result)

if __name__ == '__main__':
    main()
