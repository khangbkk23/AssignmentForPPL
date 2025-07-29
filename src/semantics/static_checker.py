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
    
    def accept(self, visitor):
        return visitor.visit_unknown_type(self)

def is_unknown(typ: Type) -> bool:
    return isinstance(typ, Unknown)

def is_array(typ: Type) -> bool:
    return isinstance(typ, ArrayType)

def is_primitive(typ: Type) -> bool:
    return isinstance(typ, (IntType, FloatType, BoolType, StringType, VoidType))

    
class StaticChecker(ASTVisitor):
    def __init__(self):
        self.number_of_loop = 0
        self.curr_function: Optional[FuncDecl] = None
        
    def check(self, ast):
        return self.check_program(ast)

    def lookup(self, name: str, lst: List, func):
        for x in lst:
            result = func(x)
            if result is not None and name == result:
                return x
        return None

    def compare_types(self, lhs: Type, rhs: Type) -> bool:
        if isinstance(lhs, Unknown) or isinstance(rhs, Unknown):
            return False
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
        if node.type_annotation:
            if not self.compare_types(typ_val, node.type_annotation):
                raise TypeMismatchInExpression(node.value)
            final_type = node.type_annotation
        else:
            final_type = typ_val
        
        if isinstance(final_type, Unknown):
            raise TypeCannotBeInferred(node)            
        
        return Symbol(node.name, final_type, is_constant=True)
        
    def visit_func_decl(self, node: 'FuncDecl', param: List[List['Symbol']]) -> Symbol:
        if self.lookup(node.name, param[0], lambda x: x.name):
            raise Redeclared('Function', node.name)
        
        param_types = [p.param_type for p in node.params]
        func_symbol = Symbol(node.name, FunctionType(param_types, node.return_type))
        
        old_function = self.curr_function
        self.curr_function = node

        try:
            # Analyze body using reduce as specified
            reduce(lambda acc, ele: [
                ([result] + acc[0]) if isinstance(result := self.visit(ele, acc), Symbol) else acc[0]
            ] + acc[1:], node.body,
                [reduce(lambda acc, ele: [self.visit(ele, acc)] + acc, node.params, [])] + param)
        finally:
            # Restore previous function
            self.curr_function = old_function
            
        return func_symbol
    
    def visit_param(self, node: 'Param', param: List[List['Symbol']]) -> Symbol:
        if self.lookup(node.name, param[0], lambda x: x.name):
            raise Redeclared('Parameter', node.name)
        
        if not node.param_type:
            raise TypeCannotBeInferred("Parameter type cannot be inferred", node)
        
        param_symbol = Symbol(node.name, node.param_type)
        # param[0].insert(0, param_symbol)
        return param_symbol

    def visit_var_decl(self, node: 'VarDecl', param: List[List['Symbol']]) -> Symbol:
        if self.lookup(node.name, param[0], lambda x: x.name):
            raise Redeclared('Variable', node.name)
        
        value_typ = self.visit(node.value, param) if node.value else Unknown()
        declared_typ = node.type_annotation or value_typ

        if not self.compare_types(self.visit(node.value, param), declared_typ):
            raise TypeMismatchInStatement(node)

        var_symbol = Symbol(node.name, declared_typ)
        param[0].insert(0, var_symbol)
        return var_symbol
    
    def visit_assignment(self, node: 'Assignment', param: List[List['Symbol']]) -> None:
        def check_declared_const(lvalue, param):
            current = lvalue
            while isinstance(current, (IdLValue, Identifier)):
                current = current.array
            
            def is_variable_symbol(symbol: Symbol) -> bool:
                return not isinstance(symbol.type, FunctionType)
    
            found_symbol: Optional[Symbol] = None
            for scope in param:
                symbol = self.lookup(current.name, scope, lambda sym: sym.name if is_variable_symbol(sym) else None)
                if symbol:
                    found_symbol = symbol
                    break

            if found_symbol is None:
                raise Undeclared(IdentifierMarker(), current.name)

            return found_symbol.is_constant
        
        if check_declared_const(node.lvalue, param):
            raise TypeMismatchInStatement(node)
        
        lvalue_typ = self.visit(node.lvalue, param)
        value_typ = self.visit(node.value, param)
        
        if not self.compare_types(lvalue_typ, value_typ):
            raise TypeMismatchInStatement(node)
        
        if self.curr_function and self.curr_function.return_type:
            if self.compare_types(value_typ, self.curr_function.return_type):
                raise TypeMismatchInStatement(node)
    
    def visit_block_stmt(self, node: 'BlockStmt', param: List[List['Symbol']]) -> None:
        pass
    
    def visit_if_stmt(self, node: 'IfStmt', param: List[List['Symbol']]) -> None:
        pass
    
    def visit_for_stmt(self, node: 'ForStmt', param: List[List['Symbol']]) -> None:
        pass
    
    def visit_while_stmt(self, node: 'WhileStmt', param: List[List['Symbol']]) -> None:
        pass
    
    def visit_break_stmt(self, node: 'BreakStmt', param: List[List['Symbol']]) -> None:
        pass
    
    def visit_continue_stmt(self, node: 'ContinueStmt', param: List[List['Symbol']]) -> None:
        pass
    
    def visit_expr_stmt(self, node: 'ExprStmt', param: List[List['Symbol']]) -> None:
        pass
    
    def visit_identifier(self, node: 'Identifier', param: List[List['Symbol']]) -> Type:
        pass
    
    def visit_id_lvalue(self, node: 'IdLValue', param: List[List['Symbol']]) -> Type:
        pass
    
    def visit_array_access(self, node, param):
        pass
    
    def visit_array_access_lvalue(self, node, param):
        pass
    
    def visit_array_literal(self, node: 'ArrayLiteral', param: List[List['Symbol']]) -> Type:
        if not node.elements:
            raise TypeMismatchInStatement(node)  # hoặc bạn có thể giả định kiểu cụ thể hơn

        element_types = [self.visit(ele, param) for ele in node.elements]
        first_type = element_types[0]

        for typ in element_types[1:]:
            if not self.compare_types(first_type, typ):
                raise TypeMismatchInStatement(node)

        return ArrayType(first_type, len(element_types))
    
    def visit_array_type(self, node, param):
        pass
    
    def visit_binary_op(self, node, param):
        pass
    
    def visit_unary_op(self, node, param):
        pass
    
     def visit_function_call(self, node: 'FunctionCall', param: List[List['Symbol']]) -> Type:
         # Check self-call
        if self.curr_function and node.function.name == self.curr_function.name:
            raise Undeclared(FunctionMarker(), node.function.name)
        
    def visit_return_stmt(self, node, param):
        pass
     # Literals
    def visit_integer_literal(self, node, param):
        return IntType()
    
    def visit_float_literal(self, node, param):
        return FloatType()
    
    def visit_float_type(self, node, param):
        return FloatType()
    
    def visit_int_type(self, node, param):
        return IntType()
    
    def visit_string_type(self, node, param):
        return StringType()
    
    def visit_bool_type(self, node, param):
        return BoolType()
    
    def visit_void_type(self, node, param):
        return VoidType()
    
    def visit_boolean_literal(self, node, param):
        return BoolType()
    
    def visit_string_literal(self, node, param):
        return StringType()