#!/usr/bin/env python3.5
# -*- coding: utf-8

INTEGER, PLUS, EOF, MINUS, MULTIPLY, DIVIDE = 'INTEGER', 'PLUS', 'EOF', 'MINUS', 'MULTIPLY', 'DIVIDE'

OPERATOR = {
    '+': PLUS,
    '-': MINUS,
    '*': MULTIPLY,
    '/': DIVIDE,
}

def plus(x, y):
    return x + y

def minus(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

FUNCTIONS = {
    PLUS: plus,
    MINUS: minus,
    MULTIPLY: multiply,
    DIVIDE: divide
}

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


class Interprter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

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
        return int(result)

    def get_next_token(self):
        # boundary
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char in '+-*/':
                tmp_char = self.current_char
                self.advance()
                return Token(OPERATOR[tmp_char],
                             self.current_char)
            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        # init
        left = right = None
        self.current_token = self.get_next_token()

        while self.current_token.type != EOF:
            if not left:
                left = self.current_token
                self.eat(INTEGER)
            op = self.current_token
            self.eat(op.type)
            right = self.current_token
            self.eat(INTEGER)

            left = Token(
                    INTEGER,
                    FUNCTIONS[op.type](left.value, right.value)
                    )

        return left.value
        
def main():
    while True:
        try:
            text = input('\033[34mcalc>\033[0m')
        except EOFError:
            break

        if not text:
            continue
        interprter = Interprter(text)
        result = interprter.expr()
        print(result)

if __name__ == '__main__':
    main()
