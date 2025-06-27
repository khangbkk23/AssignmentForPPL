grammar HLang;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
    
}

options{
	language=Python3;
}

/*------------------------------------------------------------------
 *  PARSER RULES
 *------------------------------------------------------------------*/
program: decl+ EOF;

decl: vardecl| constdecl | funcdecl ;

vardecl : LET ID (COLON typeSpec)? EQ exp SEMI ;

constdecl: CONST ID (COLON typeSpec)? EQ exp SEMI ;

funcdecl: FUNC ID LPAREN paramlist RPAREN ARROW typeSpec body;

paramlist: paramprime ;

paramprime: param COMMA paramprime | param;

param: ID EQ typeSpec ;

typeSpec: dataType | arrayType;

dataType
    : INT
    | FLOAT
    | BOOL
    | STRING
    | VOID
    ;

arrayType: LBRACK typeSpec SEMI INT_LIT RBRACK;

body: LBRACE stmtlist RBRACE;

stmtlist: stmt stmtlist | ;


stmt
    : vardecl
    | constdecl
    | assignment
    | ifStmt
    | whileStmt
    | forStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | expStmt
    | body
    ;

assignment  : lvalue EQ exp SEMI ;

ifStmt      : IF LPAREN exp RPAREN body (ELSE body)? ;

whileStmt   : WHILE LPAREN exp RPAREN body ;

forStmt     : FOR LPAREN ID IN exp RPAREN body
    ;

breakStmt   : BREAK SEMI ;

continueStmt    : CONTINUE SEMI ;

returnStmt  : RETURN exp? SEMI ;

expStmt: exp SEMI ;

/* exp precedence climbing (lowest -> highest)
   pipeline (>>) lowest precedence, unary highest      */

exp  : pipelineExpr ;

pipelineExpr    : logicOrExpr (PIPE logicOrExpr)* ;

logicOrExpr : logicAndExpr (OR logicAndExpr)* ;

logicAndExpr: equalExpr (AND equalExpr)* ;

equalExpr: relationExpr ((EQ | NEQ) relationExpr)* ;

relationExpr : addiExpr ((LT | LE | GT | GE) addiExpr)* ;

addiExpr    : canMulExpr ((PLUS | MINUS) canMulExpr)* ;

canMulExpr  : unaryExpr ((MUL | DIV | MOD) unaryExpr)* ;

unaryExpr   : (NOT | PLUS | MINUS) unaryExpr | postfixExpr ;

postfixExpr
    : primaryExpr
      ( LBRACK exp RBRACK
      | LPAREN arglist? RPAREN
      )*
    ;


arglist: exp (COMMA exp)* ;

primaryExpr: literal | ID | LBRACK exp RBRACK;

literal
    : INT_LIT
    | FLOAT_LIT
    | STRING_LIT
    | TRUE
    | FALSE
    | arrayLiteral
    ;


lvalue: ID | ID LBRACK exp RBRACK;

arrayLiteral : LBRACK explist? RBRACK ;

explist  : exp (COMMA exp)* ;

    
/*------------------------------------------------------------------
 *  LEXER RULES
 *------------------------------------------------------------------*/

/* Keywords */
ID : [a-zA-Z_][a-zA-Z0-9_]* ;

LET     : 'let' ;
CONST   : 'const' ;
FUNC    : 'func' ;
IF      : 'if' ;
ELSE    : 'else' ;
FOR     : 'for' ;
IN      : 'in' ;
WHILE   : 'while' ;
RETURN  : 'return' ;
BREAK   : 'break' ;
CONTINUE : 'continue' ;
TRUE    : 'true' ;
FALSE   : 'false' ;

INT     : 'int' ;
FLOAT   : 'float' ;
BOOL    : 'bool' ;
STRING  : 'string' ;
VOID    : 'void' ;

/* Operators & Separators */
// Arithmetic
PLUS    : '+' ;
MINUS   : '-' ;
MUL     : '*' ;
DIV     : '/' ;
MOD     : '%' ;

// Comparison
LT      : '<' ;
LE      : '<=' ;
GT      : '>' ;
GE      : '>=' ;
EQ      : '==' ;
NEQ     : '!=' ;

// Logical
AND     : '&&' ;
OR      : '||' ;
NOT     : '!' ;
ASSIGN  : '=' ;

// Seperators
LBRACK   : '[' ;
RBRACK   : ']' ;
LPAREN   : '(' ;
RPAREN   : ')' ;
LBRACE   : '{' ;
RBRACE   : '}' ;

// Sign
COLON   : ':' ;
SEMI    : ';' ;
COMMA   : ',' ;
DOT     : '.' ;

// else
ARROW    : '->' ;
PIPE     : '>>' ;

/* Literals */

INT_LIT     : DIGIT+ ;
fragment DIGIT : [0-9] ;

FLOAT_LIT   : DIGIT+ DOT DIGIT* EXP? | DOT DIGIT+ EXP? ;
fragment EXP : [eE] [+-]? DIGIT+ ;


STRING_LIT
    : '"' (VALID_SEQ | ASCII_CHAR)* '"' 
    {
        self.text = self.text[1:-1]
    }
    ;

fragment VALID_SEQ  : '\\' [ntr"\\] ;

fragment ASCII_CHAR : ~["\\\r\n\u0080-\uFFFF] ;


/* Error tokens for strings */
UNCLOSE_STRING
    : '"' (VALID_SEQ | ASCII_CHAR)* ([\r\n] | EOF)
    {
        text = self.text[1:]
        if text[-1:] in ['\n', '\r']:
            text = text[:-1]
        raise UncloseString(text)
    }
    ;

ILLEGAL_ESCAPE
    : '"' (VALID_SEQ | ASCII_CHAR)* '\\' ~[ntr"\\\r\n] ( ~["\r\n] )* '"'
    {
        raise IllegalEscape(self.text[1:-1])
    }
    ;
    
/* Comments & Whitespace */
LINE_COMMENT    : '//' ~[\r\n]* -> skip ;

BLOCK_COMMENT   : '/*' .*? '*/' -> skip ;

WS  : [ \t\r\n]+ -> skip ;

/* Catch-all error character */
ERROR_CHAR : . ;