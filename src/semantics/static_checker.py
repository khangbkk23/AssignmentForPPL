"""
Static Semantic Checker for HLang Programming Language
"""

from functools import reduce
from platform import node
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from ..utils.visitor import ASTVisitor
from ..utils.nodes import (
    ASTNode, Program, ConstDecl, FuncDecl, Param, VarDecl, Assignment, 
    IfStmt, WhileStmt, ForStmt, ReturnStmt, BreakStmt, ContinueStmt, 
    ExprStmt, BlockStmt, IntType, FloatType, BoolType, StringType, 
    VoidType, ArrayType, IdLValue, ArrayAccessLValue, BinaryOp, UnaryOp, 
    FunctionCall, ArrayAccess, Identifier, IntegerLiteral, FloatLiteral, 
    BooleanLiteral, StringLiteral, ArrayLiteral, Type
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
        self.param_types = param_types
        self.return_type = return_type
        
    def accept(self, visitor):
        return visitor.visit_function_type(self)
    
    def __str__(self):
        params_str = ', '.join(str(t) for t in self.param_types) if self.param_types else ""
        params_part = f"({params_str})" if params_str else "()"
        return f"FunctionType{params_part} -> {self.return_type}"

class Symbol:
    def __init__(self, name: str, typ: 'Type', is_constant: bool = False):
        self.name = name
        self.typ = typ
        self.is_constant = is_constant
    
    def __str__(self):
        return f"Symbol(name={self.name}, type={self.typ})"
    
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
        self.number_loop = 0
        self.curr_function: FuncDecl = None

    def lookup(self, name: str, lst: List, func):
        for x in lst:
            result = func(x)
            if result is not None and name == result:
                return x
        return None

    def compare_types(self, lhs: 'Type', rhs: 'Type') -> bool:
        if isinstance(lhs, Unknown) or isinstance(rhs, Unknown):
            return False
        if isinstance(lhs, ArrayType) and isinstance(rhs, ArrayType):
            return lhs.size == rhs.size and self.compare_types(lhs.element_type, rhs.element_type)
        return type(lhs) == type(rhs)

    def check_program(self, node: 'ASTNode'):
        self.visit(node, [])
        
    def visit(self, node: 'ASTNode', param):
        return node.accept(self, param)
    
    #* Visit methods for different AST nodes =======================
    def visit_program(self, node: 'Program', param: List):
        main_found = False
        for func in node.func_decls:
            if isinstance(func.return_type, VoidType) and len(func.params) == 0:
                main_found = True
                break
        
        if not main_found:
            raise NoEntryPoint()
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
            raise Redeclared("Constant", node.name)
        typ_val = self.visit(node.value, param)
        if node.type_annotation:
            if not self.compare_types(typ_val, node.type_annotation):
                raise TypeMismatchInExpression(node)
            final_type = node.type_annotation
        else:
            if isinstance(typ_val, Unknown):
                raise TypeCannotBeInferred(node)
            final_type = typ_val          
        
        return Symbol(node.name, final_type, is_constant=True)
        
    # def visit_func_decl(self, node: 'FuncDecl', param: List[List['Symbol']]) -> Symbol:
    #     if self.lookup(node.name, param[0], lambda x: x.name):
    #         raise Redeclared("Function", node.name)

    #     func_symbol = Symbol(node.name, FunctionType(list(map(lambda x: x.param_type, node.params)), node.return_type))
    #     param[0].insert(0, func_symbol)
    #     self.curr_function = node
        
    #     reduce(lambda acc, cur: [([result] + acc[0]) if isinstance(result := self.visit(cur, param), Symbol) else acc[0]
    #     ] + acc[1:], node.body, [reduce(lambda acc, cur: [self.visit(cur, acc)] + acc, node.params, [])] + param)
    #     return func_symbol
    def visit_func_decl(self, node: 'FuncDecl', param: List[List['Symbol']]) -> Symbol:
        if self.lookup(node.name, param[0], lambda x: x.name):
            raise Redeclared("Function", node.name)

        func_symbol = Symbol(node.name, FunctionType(list(map(lambda x: x.param_type, node.params)), node.return_type))
        param[0].insert(0, func_symbol)
        self.curr_function = node
        
        param_symbols = []
        param_names = set()
        for p in node.params:
            if p.name in param_names:
                raise Redeclared('Parameter', p.name)
            param_names.add(p.name)
            param_symbols.append(Symbol(p.name, p.param_type, is_constant=True))
        function_param = [param_symbols] + param
        for stmt in node.body:
            result = self.visit(stmt, function_param)
            if isinstance(result, Symbol):
                function_param[0].append(result)
    
        return func_symbol

    def visit_param(self, node: 'Param', param: List[List['Symbol']]) -> Symbol:
        return Symbol(node.name, node.param_type, is_constant=True)
    
    def visit_var_decl(self, node: 'VarDecl', param: List[List['Symbol']]) -> Symbol:
        if self.lookup(node.name, param[0], lambda x: x.name):
            raise Redeclared('Variable', node.name)

        value_type = self.visit(node.value, param)
        if node.type_annotation:
            if not self.compare_types(value_type, node.type_annotation):
                raise TypeMismatchInStatement(node)
            final_type = node.type_annotation
        else:
            if isinstance(value_type, Unknown):
                raise TypeCannotBeInferred(node)
            final_type = value_type
        
        return Symbol(node.name, final_type, is_constant=False)
    
    def visit_assignment(self, node: 'Assignment', param: List[List['Symbol']]) -> None:
        def check_declared_const(lvalue, param):
            current = lvalue
            while not isinstance(current, (IdLValue, Identifier)):
                current = current.array
            
            def is_variable_symbol(symbol: Symbol) -> bool:
                return not isinstance(symbol.typ, FunctionType)

            res = next(filter(None, map(lambda itemLst: self.lookup(current.name, itemLst, lambda x: x.name if is_variable_symbol(x) else None), param)), None)
            if res is None:
                raise Undeclared(IdentifierMarker(), current.name)
            return res.is_constant

        if check_declared_const(node.lvalue, param):
            raise TypeMismatchInStatement(node)
        
        if isinstance(node.lvalue, IdLValue) and self.curr_function:
            if node.lvalue.name == self.curr_function.name:
                raise TypeMismatchInStatement(node)

        lvalue_typ = self.visit(node.lvalue, param)
        value_typ = self.visit(node.value, param)
        
        if not self.compare_types(lvalue_typ, value_typ):
            raise TypeMismatchInStatement(node)
    
    def visit_block_stmt(self, node: BlockStmt, param: List[List['Symbol']]) -> None:
        block_scope = []
        new_params = [block_scope] + param
        
        for stmt in node.statements:
            res = self.visit(stmt, new_params)
            if isinstance(res, Symbol):
                block_scope.append(res)
                
#* LOOPS AND CONDITIONALS ==========================================
    def visit_while_stmt(self, node: 'WhileStmt', param: List[List['Symbol']]) -> None:
        type_cond = self.visit(node.condition, param)
        if not self.compare_types(type_cond, BoolType()):
            raise TypeMismatchInStatement(node)
        self.number_loop += 1
        self.visit(node.body, param)
        self.number_loop -= 1
    
    def visit_for_stmt(self, node: 'ForStmt', param: List[List['Symbol']]) -> None:
        type_ite = self.visit(node.iterable, param)
        if type(type_ite) != ArrayType:
            raise TypeMismatchInStatement(node)
        self.number_loop += 1
        reduce(lambda acc, cur: [
            ([result] + acc[0]) if isinstance(result := self.visit(cur, acc), Symbol) else acc[0]
        ] + acc[1:], node.body.statements,  [[Symbol(node.variable, type_ite.element_type)]] + param)
        self.number_loop -= 1
    
    def visit_break_stmt(self, node: 'BreakStmt', param: List[List['Symbol']]) -> None:
        if self.number_loop == 0: 
            raise MustInLoop(node)

    def visit_continue_stmt(self, node: 'ContinueStmt', param: List[List['Symbol']]) -> None:
        if self.number_loop == 0: 
            raise MustInLoop(node)

    def visit_if_stmt(self, node: 'IfStmt', param: List[List['Symbol']]) -> None:
        list_cond = [node.condition] + [item[0] for item in node.elif_branches]
        for condition in list_cond:
            type_cond = self.visit(condition, param)
            if not isinstance(type_cond, BoolType):
                raise TypeMismatchInStatement(node)
            
        self.visit(node.then_stmt, param)
        [self.visit(item[1], param) for item in node.elif_branches]
        if node.else_stmt:
            self.visit(node.else_stmt, param)
    
    def visit_expr_stmt(self, node: 'ExprStmt', param: List[List['Symbol']]) -> None:
        if isinstance(node.expr, FunctionCall):
            if self.curr_function and node.expr.function.name == self.curr_function.name:
                raise Undeclared(FunctionMarker(), node.expr.function.name)
            res: Optional['Symbol'] = next(
                filter(None, map(lambda item_list: self.lookup(node.expr.function.name, item_list, lambda x: x.name), param)),
                None
            )
            if res and isinstance(res.typ, FunctionType):
                type_params = res.typ.param_types
                type_args = [self.visit(item, param) for item in node.expr.args]
                if len(type_params) != len(type_args):
                    raise TypeMismatchInStatement(node)
                if node.expr.function.name == "str":
                    if not isinstance(type_args[0], (IntType, FloatType, BoolType)):
                        raise TypeMismatchInStatement(node)
                else:
                    for param_type, arg_type in zip(type_params, type_args):
                        if not self.compare_types(param_type, arg_type):
                            raise TypeMismatchInStatement(node)
                if not isinstance(res.typ.return_type, VoidType):
                    raise TypeMismatchInStatement(node)
                return
            raise Undeclared(FunctionMarker(), node.expr.function.name)

        elif isinstance(node.expr, BinaryOp) and node.expr.operator == '>>':
            try:
                expr_type = self.visit(node.expr, param)
                if not isinstance(expr_type, VoidType):
                    raise TypeMismatchInStatement(node)
            except TypeMismatchInExpression:
                raise TypeMismatchInStatement(node)

        else:
            self.visit(node.expr, param)

    def visit_id_lvalue(self, node: 'IdLValue', param: List[List['Symbol']]) -> Type:
        for scope in param:
            symbol = self.lookup(node.name, scope, lambda x: x.name)
            if symbol:
                return symbol.typ
        raise Undeclared(IdentifierMarker(), node.name)
    
    def visit_identifier(self, node: 'Identifier', param: List[List['Symbol']]) -> Type:
        for scope in param:
            symbol = self.lookup(node.name, scope, lambda x: x.name)
            if symbol:
                if isinstance(symbol.typ, FunctionType):
                    raise Undeclared(IdentifierMarker(), node.name)
                return symbol.typ
        raise Undeclared(IdentifierMarker(), node.name)
    
    def visit_array_access(self, node: 'ArrayAccess', param: List[List['Symbol']]) -> Type:
        array_type = self.visit(node.array, param)
        index_type = self.visit(node.index, param)
        
        if not isinstance(array_type, ArrayType):
            raise TypeMismatchInExpression(node)
        if not isinstance(index_type, IntType):
            raise TypeMismatchInExpression(node.index)
        
        return array_type.element_type

    def visit_array_access_lvalue(self, node: 'ArrayAccessLValue', param: List[List['Symbol']]) -> Type:
        array_type = self.visit(node.array, param)
        index_type = self.visit(node.index, param)
        
        if not isinstance(array_type, ArrayType):
            raise TypeMismatchInExpression(node)
        if not isinstance(index_type, IntType):
            raise TypeMismatchInExpression(node)
        
        return array_type.element_type

    def visit_array_literal(self, node: 'ArrayLiteral', param: List[List['Symbol']]) -> Type:
        if not node.elements:
            return ArrayType(IntType(), 0)

        element_types = [self.visit(ele, param) for ele in node.elements]
        first_type = element_types[0]

        for typ in element_types[1:]:
            if not self.compare_types(first_type, typ):
                raise TypeMismatchInExpression(node)

        return ArrayType(first_type, len(element_types))

    def visit_array_type(self, node: 'ArrayType', param: List[List['Symbol']]) -> Type:
        element_type = self.visit(node.element_type, param)
        return ArrayType(element_type, node.size)

    def visit_binary_op(self, node: 'BinaryOp', param: List[List['Symbol']]) -> Type:
        left_type = self.visit(node.left, param)

        if node.operator == '>>':
            if isinstance(node.right, Identifier):
                res: Optional['Symbol'] = next(
                    filter(None, map(lambda item_list: self.lookup(node.right.name, item_list, lambda x: x.name), param)),
                    None
                )
                if res and isinstance(res.typ, FunctionType):
                    type_params = res.typ.param_types
                    if len(type_params) != 1:
                        raise TypeMismatchInExpression(node)
                    if node.right.name == "str":
                        if not isinstance(left_type, (IntType, FloatType, BoolType)):
                            raise TypeMismatchInExpression(node)
                    else:
                        if not self.compare_types(type_params[0], left_type):
                            raise TypeMismatchInExpression(node)
                    return res.typ.return_type
                raise Undeclared(FunctionMarker(), node.right.name)

            elif isinstance(node.right, FunctionCall):
                res: Optional['Symbol'] = next(
                    filter(None, map(lambda item_list: self.lookup(node.right.function.name, item_list, lambda x: x.name), param)),
                    None
                )
                if res and isinstance(res.typ, FunctionType):
                    type_params = res.typ.param_types
                    type_args = [left_type] + [self.visit(arg, param) for arg in node.right.args]
                    if len(type_params) != len(type_args):
                        raise TypeMismatchInExpression(node)
                    for param_type, arg_type in zip(type_params, type_args):
                        if not self.compare_types(param_type, arg_type):
                            raise TypeMismatchInExpression(node)
                    return res.typ.return_type
                raise Undeclared(FunctionMarker(), node.right.function.name)

            raise TypeMismatchInExpression(node)

        right_type = self.visit(node.right, param)

        if node.operator == '+':
            if (isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType))):
                return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
            if isinstance(left_type, StringType) and isinstance(right_type, StringType):
                return StringType()
            raise TypeMismatchInExpression(node)

        if node.operator in ['-', '*', '/']:
            if not (isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType))):
                raise TypeMismatchInExpression(node)
            return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

        if node.operator == '%':
            if not (isinstance(left_type, IntType) and isinstance(right_type, IntType)):
                raise TypeMismatchInExpression(node)
            return IntType()

        if node.operator in ['>', '<', '>=', '<=', '==', '!=']:
            if not (isinstance(left_type, (IntType, FloatType, StringType, BoolType)) and 
                    isinstance(right_type, (IntType, FloatType, StringType, BoolType))):
                raise TypeMismatchInExpression(node)
            if node.operator in ['>', '<', '>=', '<=']:
                if not (isinstance(left_type, (IntType, FloatType, StringType)) and 
                        isinstance(right_type, (IntType, FloatType, StringType))):
                    raise TypeMismatchInExpression(node)
            if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
                return BoolType()
            if not self.compare_types(left_type, right_type):
                raise TypeMismatchInExpression(node)
            return BoolType()

        if node.operator in ['&&', '||']:
            if not self.compare_types(left_type, right_type):
                raise TypeMismatchInExpression(node)
            if not isinstance(left_type, BoolType):
                raise TypeMismatchInExpression(node)
            return BoolType()

        raise TypeMismatchInExpression(node)

    def visit_function_call(self, node: 'FunctionCall', param: List[List['Symbol']]) -> Type:

        res: Optional['Symbol'] = next(
            filter(None, map(lambda item_list: self.lookup(node.function.name, item_list, lambda x: x.name), param)),
            None
        )
        if res is None:
            raise Undeclared(FunctionMarker(), node.function.name)
        if not isinstance(res.typ, FunctionType):
            raise TypeMismatchInExpression(node)
        type_params = res.typ.param_types
        type_args = [self.visit(arg, param) for arg in node.args]

        if len(type_params) != len(type_args):
            raise TypeMismatchInExpression(node)

        if node.function.name == "str":
            if not isinstance(type_args[0], (IntType, FloatType, BoolType)):
                raise TypeMismatchInExpression(node)
        else:
            for expected, actual in zip(type_params, type_args):
                if not self.compare_types(expected, actual):
                    raise TypeMismatchInExpression(node)
        if isinstance(res.typ.return_type, VoidType):
            raise TypeMismatchInExpression(node)

        return res.typ.return_type

    def visit_return_stmt(self, node: 'ReturnStmt', param: List[List['Symbol']]) -> None:
        expected_type = self.curr_function.return_type if self.curr_function else VoidType()

        if node.value is None:
            if not isinstance(expected_type, VoidType):
                raise TypeMismatchInStatement(node)
        else:
            actual_type = self.visit(node.value, param)
            if not self.compare_types(expected_type, actual_type):
                raise TypeMismatchInStatement(node)
        
    def visit_unary_op(self, node: 'UnaryOp', param: List[List['Symbol']]) -> Type:
        operand_type = self.visit(node.operand, param)
        
        if node.operator in ['-', '+']:
            if not isinstance(operand_type, (IntType, FloatType)):
                raise TypeMismatchInExpression(node)
            return operand_type
        
        if node.operator == '!':
            if not isinstance(operand_type, BoolType):
                raise TypeMismatchInExpression(node)
            return BoolType()
        
        raise TypeMismatchInExpression(node)
#* Literals ========================================================
    def visit_integer_literal(self, node: 'IntegerLiteral', param):
        return IntType()
    
    def visit_float_literal(self, node: 'FloatLiteral', param):
        return FloatType()
    
    def visit_float_type(self, node: 'FloatType', param):
        return FloatType()
    
    def visit_int_type(self, node: 'IntType', param):
        return IntType()
    
    def visit_string_type(self, node: 'StringType', param):
        return StringType()
    
    def visit_bool_type(self, node: 'BoolType', param):
        return BoolType()
    
    def visit_void_type(self, node: 'VoidType', param):
        return VoidType()
    
    def visit_boolean_literal(self, node: 'BooleanLiteral', param):
        return BoolType()
    
    def visit_string_literal(self, node: 'StringLiteral', param):
        return StringType()