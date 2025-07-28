"""
Static Semantic Checker for HLang Programming Language
"""

from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, ConstDecl, FuncDecl, Param, VarDecl, Assignment, 
    IfStmt, WhileStmt, ForStmt, ReturnStmt, BreakStmt, ContinueStmt, 
    ExprStmt, BlockStmt, IntType, FloatType, BoolType, StringType, 
    VoidType, ArrayType, IdLValue, ArrayAccessLValue, BinaryOp, UnaryOp, 
    FunctionCall, ArrayAccess, Identifier, IntegerLiteral, FloatLiteral, 
    BooleanLiteral, StringLiteral, ArrayLiteral
)
from .static_error import (
    StaticError, Redeclared, Undeclared, TypeMismatchInExpression,
    TypeMismatchInStatement, TypeCannotBeInferred, NoEntryPoint,
    MustInLoop
)

# Import marker classes with different names to avoid conflict  
from .static_error import Identifier as IdentifierMarker, Function as FunctionMarker
class FunctionType(Type):
    def __init__(self, param_types: List[Type], return_type: Type):
        super().__init__()
        self.param_types = param_types if param_types is not None else []
        self.return_type = return_type if return_type is not None else VoidType()
        
    def accept(self, visitor):
        return visitor.visit_function_type(self)
    
    def __str__(self):
        params_str = ', '.join(str(t) for t in self.param_types) if self.param_types else ""
        params_part = f"({params_str})" if params_str else "()"
        return f"FunctionType{params_part} -> {self.return_type}"

class Symbol:
    def __init__(self, name: str, typ: 'Type', is_constant: bool = False):
        self.name = name
        self.type = typ
        self.is_constant = is_constant
    
    def __str__(self):
        return f"Symbol({self.name}, {self.typ})"
    
    @staticmethod
    def str(params: List[List['Symbol']]) -> str:
        return "[" + ", ".join(
            "[" + ", ".join(str(sym) for sym in scope) + "]"
            for scope in params
        ) + "]"

class Unknown:
    def __str__(self):
        return "Unknown"

def is_unknown(t):
    return isinstance(t, Unknown)

def is_array(t):
    return isinstance(t, ArrayType)

def is_primitive(t):
    return isinstance(t, (IntType, FloatType, BoolType, StringType, VoidType))

    
class StaticChecker(ASTVisitor):
    def __init__(self):
        self.curr_func: Optional[FuncDecl] = None
    
    def check(self, ast):
        return 

    def lookup(self, name: str, lst: List, func):
        for x in lst:
            if name == func(x):
                return x
        return None

    def compare_types(self, lhs: 'Type', rhs: 'Type'):
        if isinstance(lhs, ArrayType) and isinstance(rhs, ArrayType):
            return lhs.size == rhs.size and self.compare_types(lhs.element_type, rhs.element_type)
        return type(lhs) == type(rhs)

    def visit(self, node: 'ASTNode', param):
        return node.accept(self, param)

    def check_program(self, node: 'ASTNode'):
        self.visit(node, [])
        
    def visit_program(self, node: 'Program', param: List):
        for func in node.func_decls:
            if func.name == "main" and type(func.return_type) != VoidType and len(func.params) == 0:
                break
        else:
            raise NoEntryPoint("No valid main function found")

        reduce(
            lambda acc, cur: [([self.visit(cur, acc)] + acc[0])] + acc[1:],
            node.const_decls + node.func_decls,
            [[
                Symbol("print", FunctionType([StringType()], VoidType())),
                Symbol("str", FunctionType([IntType()], StringType())),
                Symbol("int", FunctionType([StringType()], IntType())),
                Symbol("float", FunctionType([StringType()], FloatType())),
                Symbol("input", FunctionType([], StringType())),
            ]]
        )

    def visit_const_decl(self, node: 'ConstDecl', param: List[List['Symbol']]) -> Symbol:
        if self.lookup(node.name, param[0], lambda x: x.name):
            raise Redeclared('Constant', node.name)
        
        typ_val = self.visit(node.value, param)
        if node.type_annnotation and not self.compare_types(typ_val, node.type_annotation):
            raise TypeMismatchInExpression(node)
        
        return Symbol(node.name, node.type_annotation or typ_val, is_constant=True)
        
    def visit_func_decl(self, node: 'FuncDecl', param: List[List['Symbol']]) -> Symbol:
        if self.lookup(node.name, param[0], lambda x: x.name):
            raise Redeclared('Function', node.name)
        
        func_symbol = Symbol(node.name, FunctionType(
            list(map(lambda item: item.param_type, node.params)), None))
        param[0].insert(0, func_symbol)

        self.curr_function = node

        # Phân tích body
        reduce(lambda acc, ele: [
            ([result] + acc[0]) if isinstance(result := self.visit(ele, acc), Symbol) else acc[0]
        ] + acc[1:], node.body,
            [reduce(lambda acc, ele: [self.visit(ele, acc)] + acc, node.params, [])] + param)

        return func_symbol