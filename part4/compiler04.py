#!/usr/bin/env python3.5
# -*- coding: utf-8
#!/usr/bin/env python3.5
# -*- coding: utf-8

INTEGER, PLUS, EOF, MINUS, MULTIPLY, DIVIDE = 'INTEGER', 'PLUS', 'EOF', 'MINUS', 'MULTIPLY', 'DIVIDE'


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
            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, self.current_char)
            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, self.current_char)

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        Return an INTEGER value.
        """
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        """
        Arithmetic expression parser / interpreter.
        expr   : factor((MUL | DIV)factor)*
        factor : INTEGER
        """
        self.current_token = self.get_next_token()

        result = self.factor()
        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
                result *= self.factor()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result /= self.factor()

        return result


def main():
    while True:
        try:
            text = input('\033[34m>>> \033[0m')
        except EOFError:
            break

        if not text:
            continue
        interprter = Interprter(text)
        result = interprter.expr()
        print(result)

if __name__ == '__main__':
    main()
