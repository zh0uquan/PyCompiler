"use strict";

const INTEGER = 'INTEGER',
      PLUS    = 'PLUS',
      MINUS   = 'MINUS',
      MUL     = 'MUL',
      DIV     = 'DIV',
      LPAREN  = 'LPAREN',
      RPAREN  = 'RPAREN',
      EOF     = 'EOF';

class Token {
  constructor(type, value) {
    this.type = type;
    this.value = value;
  }
}

class Lexer {
  constructor(text) {
    this.text = text;
    this.pos = 0;
    this.current_char = this.text[this.pos];
  }

  error() {
    throw "invaild character";
  }

  isSpace(char) {
    return char === ' ';
  }

  isDigit(char) {
    return !isNaN(char);
  }

  skip_whitespace() {
    while (this.current_char && this.isSpace(this.current_char)) {
      this.advance();
    }
  }

  integer() {
    let result = '';
    while (this.current_char && this.isDigit(this.current_char)) {
      result += this.current_char;
      this.advance();
    }
    return parseInt(result);
  }

  advance() {
    this.pos += 1;
    if (this.pos > this.text.length - 1) {
      this.current_char = null;
    } else {
      this.current_char = this.text[this.pos];
    }
  }

  get_next_token() {
    while (this.current_char !== null) {
      if (this.isSpace(this.current_char)) {
        this.skip_whitespace();
        continue;
      }

      if (this.isDigit(this.current_char)){
        return new Token(INTEGER, this.integer());
      }

      if (this.current_char === '+') {
        this.advance();
        return new Token(PLUS, '+');
      }

      if (this.current_char === '-') {
        this.advance();
        return new Token(MINUS, '-');
      }

      if (this.current_char === '*') {
        this.advance();
        return new Token(MUL, '*');
      }

      if (this.current_char === '/') {
        this.advance();
        return new Token(DIV, '/');
      }

      if (this.current_char === '(') {
        this.advance();
        return new Token(LPAREN, '(');
      }
      if (this.current_char === ')') {
        this.advance();
        return new Token(RPAREN, ')');
      }

      this.error();
    }

    return new Token(EOF, null);
  }
}


class Interprter {
  constructor(lexer) {
    this.lexer = lexer;
    this.current_token = this.lexer.get_next_token();
  }

  error() {
    throw 'Invaild syntax';
  }

  eat(type) {
    if (this.current_token.type === type) {
      this.current_token = this.lexer.get_next_token();
    } else {
      this.error();
    }
  }

  factor() {
    let token = this.current_token;
    if (token.type === INTEGER) {
      this.eat(INTEGER);
      return token.value;
    }

    if (token.type === LPAREN) {
      this.eat(LPAREN);
      let result = this.expr();
      this.eat(RPAREN);
      return result;
    }
  }

  term() {
    let result = this.factor();
    while ([MUL, DIV].indexOf(this.current_token.type) !== -1) {

      if (this.current_token.type === MUL) {
        this.eat(MUL);
        result *= this.factor();
      }
      else if (this.current_token.type === DIV) {
        this.eat(DIV);
        result /= this.factor();
      }
    }
    return result;
  }

  expr() {
    // factor : INTEGER | LPAREN expr RPAREN
    // term   : factor((MUL | DIV)factor)*
    // expr   : term((PLUS | MINUS)term)*
    let result = this.term();
    while ([PLUS, MINUS].indexOf(this.current_token.type) !== -1) {

      if (this.current_token.type === PLUS) {
        this.eat(PLUS);
        result += this.term();
      }
      else if (this.current_token.type === MINUS) {
        this.eat(MINUS);
        result -= this.term();
      }
    }
    return result;
  }

}

const expr = () => {
  let result = '';
  try {
    let text = document.getElementById("demo").value,
        lexer = new Lexer(text),
        interprter = new Interprter(lexer);
    result = interprter.expr();
  } catch (e) {
    result = e.toString();
  } finally {
    document.getElementById("result").innerHTML = 'Result: ' + result;
  }
}
