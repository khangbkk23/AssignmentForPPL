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
program: decllist EOF ;

decllist: decl decllistTail | ;

decllistTail: decl decllistTail | ;

decl: vardecl | constdecl | funcdecl;

// Variable and constant declarations
vardecl: LET ID typeOpt ASSIGN expr SEMI;

constdecl: CONST ID typeOpt ASSIGN expr SEMI;

typeOpt: COLON typeSpec | ;

typeSpec: dataType | arrayType;

dataType: INT | FLOAT | BOOL | STRING | VOID;

arrayType: LBRACK typeSpec SEMI INT_LIT RBRACK;

// Function declaration
funcdecl: FUNC ID LPAREN paramOpt RPAREN ARROW typeSpec blockStmt ;

paramOpt: param paramTail | ;

paramTail: COMMA param paramTail | ;

param: ID COLON typeSpec;

// Statements
stmtList: stmt stmtListTail | ;

stmtListTail: stmt stmtListTail | ;


stmt
    : vardecl
    | constdecl
    | assignStmt
    | ifStmt
    | whileStmt
    | forStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | exprStmt
    | blockStmt;

assignStmt: lvalue ASSIGN expr SEMI;

ifStmt: IF LPAREN expr RPAREN blockStmt elseifTail elseOpt;

elseifTail: ELSE IF LPAREN expr RPAREN blockStmt elseifTail | ;

elseOpt: ELSE blockStmt | ;

whileStmt: WHILE LPAREN expr RPAREN blockStmt;

forStmt: FOR LPAREN ID IN expr RPAREN blockStmt;

breakStmt: BREAK SEMI;

continueStmt: CONTINUE SEMI;

returnStmt: RETURN exprReturn SEMI;

exprReturn: expr | ;

exprStmt: expr SEMI;

blockStmt: LBRACE stmtList RBRACE;


// Expressions
expr: pipelineExpr;


pipelineExpr: logicOrExpr pipelineExprTail;

pipelineExprTail: PIPE logicOrExpr pipelineExprTail | ;


logicOrExpr: logicAndExpr logicOrExprTail;

logicOrExprTail: OR logicAndExpr logicOrExprTail | ;


logicAndExpr: equalExpr logicAndExprTail;

logicAndExprTail: AND equalExpr logicAndExprTail | ;


equalExpr: relExpr equalExprTail;

equalExprTail: (EQ | NEQ) relExpr equalExprTail | ;


relExpr: addiExpr relExprTail;

relExprTail: (LT | LE | GT | GE) addiExpr relExprTail | ;


addiExpr: multiExpr addiExprTail;

addiExprTail: (PLUS | MINUS) multiExpr addiExprTail | ;


multiExpr: unaryExpr multiExprTail;

multiExprTail: (MUL | DIV | MOD) unaryExpr multiExprTail | ;


unaryExpr: (NOT | PLUS | MINUS) unaryExpr | postfixExpr;


postfixExpr: primaryExpr postfixExprTail;

postfixExprTail: postfixOp postfixExprTail | ;

postfixOp: LBRACK expr RBRACK | LPAREN argsOpt RPAREN;

argsOpt: expr argTail | ;

argTail: COMMA expr argTail | ;

primaryExpr: literal | ID | LPAREN expr RPAREN | LBRACK expr RBRACK;

literal: INT_LIT | FLOAT_LIT | STRING_LIT | TRUE | FALSE | arrayLiteral;

arrayLiteral: LBRACK exprOpt RBRACK;

exprOpt: expr exprTail | ;

exprTail: COMMA expr exprTail | ;

lvalue: ID indexTail;

indexTail: LBRACK expr RBRACK indexTail | ;

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

BLOCK_COMMENT   : '/*' .*? '*/' -> skip ;

WS  : [ \t\r\n]+ -> skip ;

/* Catch-all error character */
ERROR_CHAR : . ;