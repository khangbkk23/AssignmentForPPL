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

// Entry point
program: constdecl* funcdecl* EOF;

// Variable and constant declarations
constdecl: CONST ID (COLON varType)? ASSIGN expr SEMI ;

vardecl: LET ID (COLON varType)? ASSIGN expr SEMI;

funcdecl: FUNC ID paramdecl ARROW returnType body ;

varType: nvoidType;

returnType: nvoidType | VOID;

nvoidType: INT | FLOAT | BOOL | STRING | arrayType ;

arrayType: LBRACK nvoidType SEMI INT_LIT RBRACK ;

// ID 
idlist: ID idlistTail ;
idlistTail: COMMA ID idlistTail | ;

// Parameters
paramdecl: LPAREN paramList? RPAREN ;
paramList: param paramListTail ;
paramListTail: COMMA param paramListTail | ;
param: ID COLON varType ;

// Body of function
body: LBRACE stmt* RBRACE;

stmt
    : vardecl
    | assignStmt
    | callStmt
    | ifStmt
    | whileStmt
    | forStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | exprStmt
    | blockStmt;

ifStmt: IF LPAREN expr RPAREN body (ELSE elseStmt)? ;
elseStmt: ifStmt | body ;

whileStmt: WHILE LPAREN expr RPAREN body ;
forStmt: FOR LPAREN ID IN expr RPAREN body ;
breakStmt: BREAK SEMI ;
continueStmt: CONTINUE SEMI ;

callStmt: callExpr SEMI ;
returnStmt: RETURN expr? SEMI;
exprStmt: expr SEMI;

assignStmt: lvalue ASSIGN expr SEMI;
lvalue: ID lvalueTail ;
lvalueTail: LBRACK expr RBRACK lvalueTail | ;

blockStmt: LBRACE stmt* RBRACE ;


// Expressions
expr: expr1 ;
expr1: expr2 ;
expr2: expr2 PIPE expr3 | expr3 ;
expr3: expr3 OR expr4 | expr4 ;
expr4: expr4 AND expr5 | expr5 ;
expr5: expr5 (EQ | NEQ) expr6 | expr6 ;
expr6: expr6 (LT | LE | GT | GE) expr7 | expr7 ;
expr7: expr7 (PLUS | MINUS) expr8 | expr8 ;
expr8: expr8 (MUL | DIV | MOD) expr9 | expr9 ;
expr9: (NOT | PLUS | MINUS) expr9 | primaryExpr expr9_tail;
expr9_tail: LBRACK expr RBRACK expr9_tail | ;

primaryExpr
        : INT_LIT
        | FLOAT_LIT
        | STRING_LIT
        | TRUE
        | FALSE
        | arrayLiteral
        | typeConversionCall
        | callExpr
        | ID
        | LPAREN expr RPAREN
        ;

typeConversionCall
        : INT LPAREN exprListOpt RPAREN
        | FLOAT LPAREN exprListOpt RPAREN
        | STR LPAREN exprListOpt RPAREN
        ;
        
callExpr: ID LPAREN exprListOpt RPAREN ;
arrayLiteral: LBRACK exprListOpt RBRACK ;
exprListOpt: exprList | ;
exprList: expr exprListTail ;
exprListTail: COMMA expr exprListTail | ;

/*------------------------------------------------------------------
 *  LEXER RULES
 *------------------------------------------------------------------*/

/* Keywords */
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
STR     : 'str';
VOID    : 'void' ;

/* Identifiers */
ID : [a-zA-Z_][a-zA-Z0-9_]* ;

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

// Separators
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

FLOAT_LIT   : (DIGIT+ DOT DIGIT* EXP?) | (DOT DIGIT+ EXP?) ;
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
    : '"' (VALID_SEQ | ASCII_CHAR)* '\\' ~[ntr"\\]
    {
        text = self.text[1:]
        self.text = text
        raise IllegalEscape(text)
    }
    ;
    
/* Comments & Whitespace */
LINE_COMMENT    : '//' ~[\r\n]* -> skip ;

BLOCK_COMMENT : '/*' (BLOCK_COMMENT | ~[*] | '*' ~[/])* '*/' -> skip ;

WS  : [ \t\r\n]+ -> skip ;

/* Catch-all error character */
ERROR_CHAR : . ;