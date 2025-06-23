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
program:  EOF;

declaration
    : variableDecl
    | constDecl
    | functionDecl
    ;

    variableDecl
    : LET ID (':' typeSpec)? '=' expression ';'
    ;

constDecl
    : CONST ID (':' typeSpec)? '=' expression ';'
    ;

functionDecl
    : FUNC ID '(' paramList? ')' ARROW typeSpec block
    ;

paramList
    : param (',' param)*
    ;

param
    : ID ':' typeSpec
    ;

typeSpec
    : primitiveType
    | arrayType
    ;

primitiveType
    : INT
    | FLOAT
    | BOOL
    | STRING
    | VOID
    ;

arrayType
    : '[' typeSpec ';' INT_LIT ']'
    ;

block
    : '{' statement* '}'
    ;

statement
    : variableDecl
    | constDecl
    | assignment
    | ifStmt
    | whileStmt
    | forStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | expressionStmt
    | block
    ;

assignment
    : lvalue '=' expression ';'
    ;

ifStmt
    : IF '(' expression ')' block (ELSE block)?
    ;

whileStmt
    : WHILE '(' expression ')' block
    ;

forStmt
    : FOR '(' ID IN expression ')' block
    ;

breakStmt
    : BREAK ';'
    ;

continueStmt    : CONTINUE ';' ;

returnStmt  : RETURN expression? ';' ;

expressionStmt: expression ';' ;

/* Expression precedence climbing (lowest -> highest)
   pipeline (>>) lowest precedence, unary highest      */

expression  : pipelineExpr ;

pipelineExpr    : logicOrExpr ('>>' logicOrExpr)* ;

logicOrExpr : logicAndExpr ('||' logicAndExpr)* ;

logicAndExpr: equalExpr ('&&' equalExpr)* ;

equalExpr: relationExpr (('==' | '!=') relationExpr)* ;

relationExpr : addiExpr (('<' | '<=' | '>' | '>=') addiExpr)* ;

addiExpr    : canMulExpr (('+' | '-') canMulExpr)* ;

canMulExpr  : unaryExpr (('*' | '/' | '%') unaryExpr)* ;

unaryExpr   : ('!' | '+' | '-') unaryExpr | postfixExpr ;

postfixExpr
    : primaryExpr
      ( '[' expression ']'
      | '(' argList? ')'
      )*
    ;


argList
    : expression (',' expression)*
    ;

primaryExpr
    : literal
    | ID
    | '(' expression ')'
    ;

literal
    : INT_LIT
    | FLOAT_LIT
    | STRING_LIT
    | TRUE
    | FALSE
    | arrayLiteral
    ;


lvalue
    : ID                             // x
    | ID '[' expression ']'         // x[0]
    ;

arrayLiteral : '[' expressionList? ']' ;

expressionList  : expression (',' expression)* ;

    
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
MULTI   : '*' ;
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
SCOLON  : ';' ;
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

fragment VALID_SEQ
    : '\\' [ntr"\\]
    ;

fragment ASCII_CHAR
    : ~["\\\r\n\u0080-\uFFFF]
    ;


/* Error tokens for strings */
UNCLOSE_STRING  : '"' (VALID_SEQ | ASCII_CHAR)* EOF {self.text = self.text[1:]} ;

ILLEGAL_ESCAPE  : '"' (VALID_SEQ | ASCII_CHAR)* '\\' ~[ntr"\\\r\n] (~["\r\n])* '"' { self.text = self.text[1:-1] };

/* Comments & Whitespace */
LINE_COMMENT    : '//' ~[\r\n]* -> skip ;

BLOCK_COMMENT   : '/*' .*? '*/' -> skip ;

WS
    : [ \t\r\n]+ -> skip ;

/* Catch-all error character */
ERROR_CHAR : . ;