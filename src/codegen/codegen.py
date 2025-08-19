"""
Code Generator for HLang programming language.
This module implements a code generator that traverses AST nodes and generates
Java bytecode using the Emitter and Frame classes.
"""

from ast import Sub
from typing import Any, List, Optional
from ..utils.visitor import ASTVisitor
from ..utils.nodes import *
from .emitter import Emitter
from .frame import Frame
from .error import IllegalOperandException, IllegalRuntimeException
from .io import IO_SYMBOL_LIST
from .utils import *
from functools import *


class CodeGenerator(ASTVisitor):
    def __init__(self):
        self.class_name = "HLang"
        self.emit = Emitter(self.class_name + ".j")

    def visit_program(self, node: "Program", o: Any = None):
        self.emit.print_out(self.emit.emit_prolog(self.class_name, "java/lang/Object"))

        global_env = reduce(
            lambda acc, cur: self.visit(cur, acc),
            node.func_decls,
            SubBody(None, IO_SYMBOL_LIST),
        )

        self.generate_method(
            FuncDecl("<init>", [], VoidType(), []),
            SubBody(Frame("<init>", VoidType()), []),
        )
        self.emit.emit_epilog()

    def generate_method(self, node: "FuncDecl", o: SubBody = None):
        frame = o.frame

        is_init = node.name == "<init>"
        is_main = node.name == "main"

        param_types = list(map(lambda x: x.param_type, node.params))
        if is_main:
            param_types = [ArrayType(StringType(), 0)]
        return_type = node.return_type

        self.emit.print_out(
            self.emit.emit_method(
                node.name, FunctionType(param_types, return_type), not is_init
            )
        )

        frame.enter_scope(True)

        from_label = frame.get_start_label()
        to_label = frame.get_end_label()

        # Generate code for parameters
        if is_init:
            this_idx = frame.get_new_index()

            self.emit.print_out(
                self.emit.emit_var(
                    this_idx, "this", ClassType(self.class_name), from_label, to_label
                )
            )
        elif is_main:
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", ArrayType(StringType(), 0), from_label, to_label
                )
            )
        else:
            o = reduce(lambda acc, cur: self.visit(cur, acc), node.params, o)

        self.emit.print_out(self.emit.emit_label(from_label, frame))

        # Generate code for body

        if is_init:
            self.emit.print_out(
                self.emit.emit_read_var(
                    "this", ClassType(self.class_name), this_idx, frame
                )
            )
            self.emit.print_out(self.emit.emit_invoke_special(frame))

        o = reduce(lambda acc, cur: self.visit(cur, acc), node.body, o)

        if type(return_type) is VoidType:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(to_label, frame))

        self.emit.print_out(self.emit.emit_end_method(frame))

        frame.exit_scope()

    def visit_const_decl(self, node: "ConstDecl", o: Any = None):
        self.emit.print_out(self.emit.emit_attribute(node.name, node.type_annotation, True, node.value))
        return SubBody(o.frame if o else None, [Symbol(node.name, node.type_annotation, CName(self.class_name))] + (o.sym if o else []))

    def visit_func_decl(self, node: "FuncDecl", o: SubBody = None):
        function_symbol = next(filter(lambda x: x.name == node.name, o.sym), None)
        # Generate code cho parameters
        for param in node.params:
            self.visit(param, SubBody(o.frame, o.sym))
        
        # Generate code cho function call (nếu cần)
        if function_symbol:
            class_name = function_symbol.value.value
            self.emit.print_out(
                self.emit.emit_invoke_static(
                    f"{class_name}/{node.name}", function_symbol.type, o.frame
                )
            )
            return_type = function_symbol.type.return_type
        else:
            return_type = node.return_type  # fallback

        return "", return_type

    def visit_param(self, node: "Param", o: Any = None):
        idx = o.frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                node.param_type,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        return SubBody(
            o.frame,
            [Symbol(node.name, node.param_type, Index(idx))] + o.sym,
        )

    # Type system

    def visit_int_type(self, node: "IntType", o: Any = None):
        return IntType()

    def visit_float_type(self, node: "FloatType", o: Any = None):
        return FloatType()

    def visit_bool_type(self, node: "BoolType", o: Any = None):
        return BoolType()

    def visit_string_type(self, node: "StringType", o: Any = None):
        return StringType()

    def visit_void_type(self, node: "VoidType", o: Any = None):
        return VoidType()

    def visit_array_type(self, node: "ArrayType", o: Any = None):
        element_type = self.visit(node.element_type, o)
        return ArrayType(element_type, node.size if hasattr(node, 'size') else 0)

    # Statements

    def visit_var_decl(self, node: "VarDecl", o: SubBody = None):
        idx = o.frame.get_new_index()
        self.emit.print_out(
            self.emit.emit_var(
                idx,
                node.name,
                node.type_annotation,
                o.frame.get_start_label(),
                o.frame.get_end_label(),
            )
        )

        if node.value is not None:
            self.visit(
                Assignment(IdLValue(node.name), node.value),
                SubBody(
                    o.frame,
                    [Symbol(node.name, node.type_annotation, Index(idx))] + o.sym,
                ),
            )
        return SubBody(
            o.frame,
            [Symbol(node.name, node.type_annotation, Index(idx))] + o.sym,
        )

    def visit_assignment(self, node: "Assignment", o: SubBody = None):
        rc, rt = self.visit(node.value, Access(o.frame, o.sym))
        self.emit.print_out(rc)
        lc, lt = self.visit(node.lvalue, Access(o.frame, o.sym))
        self.emit.print_out(lc)
        return o

    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        frame = o.frame
        sym = o.sym
        
        end_label = frame.get_new_label()
        false_label = frame.get_new_label()
        
        # Generate code for the condition expr
        cond_code, cond_type = self.visit(node.condition, Access(frame, sym, False))
        self.emit.print_out(cond_code)
        
        # Jump to false_label if false
        self.emit.print_out(self.emit.emit_if_false(false_label, frame))
        
        # Generate code for then_stmt
        self.visit(node.then_stmt, o)
        
        # Jump to end_label with all case
        self.emit.print_out(self.emit.emit_goto(end_label, frame))
        
        # Put false_label
        self.emit.print_out(self.emit.emit_label(false_label, frame))
        
        ## Handle else_if
        if node.elif_branches:
            for (elif_cond, elif_block) in node.elif_branches:
                next_false_label = frame.get_new_label()
                
                # Generate code for the elif condition expr
                ec, et = self.visit(elif_cond, Access(frame, sym, False))
                self.emit.print_out(ec)
                
                # Jump to next_false_label if False
                self.emit.print_out(self.emit.emit_if_false(next_false_label, frame))
                
                # Generate code for elif 
                self.visit(elif_block, o)
                self.emit.print_out(self.emit.emit_goto(end_label, frame))
                
                # Put next_false_label
                self.emit.print_out(self.emit.emit_label(next_false_label, frame))
        
        if node.else_stmt:
            # Generate code for else_stmt
            self.visit(node.else_stmt, o)
        
        # Put end_label
        self.emit.print_out(self.emit.emit_label(end_label, frame))

        return o
            
        
    
    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        frame = o.frame
        sym = o.sym

        # Generate labels
        frame.enter_loop()
        continue_label = frame.get_continue_label()
        break_label = frame.get_break_label()
        
        # Put continue_label
        self.emit.print_out(self.emit.emit_label(continue_label, frame))
        
        # Generate code for condition expr
        cond_code, cond_type = self.visit(node.condition, Access(frame, sym, False))
        self.emit.print_out(cond_code)
        
        # Jump to break_label if False
        self.emit.print_out(self.emit.emit_if_false(break_label, frame))
        
        # Generate code for body
        self.visit(node.body, o)
        
        # Jump to continue_label with all cases
        self.emit.print_out(self.emit.emit_goto(continue_label, frame))
        
        # Put break_label
        self.emit.print_out(self.emit.emit_label(break_label, frame))

        frame.exit_loop()
        
        return o

    def visit_for_stmt(self, node: "ForStmt", o: Any):
        frame = o.frame
        sym = o.sym

        frame.enter_loop()
        frame.enter_scope(False)

        # Generate labels
        start_label = frame.get_new_label()
        continue_label = frame.get_continue_label()
        break_label = frame.get_break_label()

        # Emit start label
        self.emit.print_out(self.emit.emit_label(start_label))

         # Evaluate iterable expression and leave it on stack
        iterable_code, iterable_type = self.visit(node.iterable, Access(frame, sym, False))
        self.emit.print_out(iterable_code)
        
        # Initialize loop variable from iterable
        loop_var_assignment = Assignment(IdLValue(node.variable), node.iterable)
        self.visit(loop_var_assignment, SubBody(frame, sym))

        # jump to break_label if False
        self.emit.print_out(self.emit.emit_if_false(break_label, frame))

        # Generate code for loop body
        self.visit(node.body, SubBody(frame, sym))

        # Put continue_label
        self.emit.print_out(self.emit.emit_label(continue_label))
        
        # Jump back to start with all case
        self.emit.print_out(self.emit.emit_goto(start_label, frame))

        # Put break_label
        self.emit.print_out(self.emit.emit_label(break_label))
        
        frame.exit_scope()
        frame.exit_loop()

        return o

    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        frame = o.frame
    
        if node.expr:
            expr_code, expr_type = self.visit(node.expr, Access(frame, o.sym, False))
            self.emit.print_out(expr_code)
            self.emit.print_out(self.emit.emit_return(expr_type, frame))
        else:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))
        
        return o

    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_break_label(), o.frame))
        return o

    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        self.emit.print_out(self.emit.emit_goto(o.frame.get_continue_label(), o.frame))
        return o

    def visit_expr_stmt(self, node: "ExprStmt", o: SubBody = None):
        code, typ = self.visit(node.expr, Access(o.frame, o.sym))
        self.emit.print_out(code)
        return o

    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        frame = o.frame
        sym = o.sym
        
        # Enter new scope
        frame.enter_scope(False)
        self.emit.print_out(self.emit.emit_label(frame.get_start_label()))

        # Visit all statements inside the block
        for stmt in node.statements:
            self.visit(stmt, SubBody(frame, sym))

        # Emit end label for the block
        self.emit.print_out(self.emit.emit_label(frame.get_end_label()))

        # Exit scope
        frame.exit_scope()

        return o
        

    # Left-values

    def visit_id_lvalue(self, node: "IdLValue", o: Access = None):
        sym = next(
            filter(lambda x: x.name == node.name, o.sym),
            False,
        )

        if type(sym.value) is Index:
            code = self.emit.emit_write_var(
                sym.name, sym.type, sym.value.value, o.frame
            )

        return code, sym.type

    def visit_array_access_lvalue(self, node: "ArrayAccessLValue", o: Any = None):
        frame = o.frame
        sym = o.sym

        arr_code, arr_type = self.visit(node.array, Access(frame, sym, False))

        idx_code, idx_type = self.visit(node.index, Access(frame, sym, False))

    
        code = arr_code
        code += idx_code
        code += self.emit.emit_array_cell(arr_type, is_left=True, frame=frame)

        return code, arr_type.ele_type


    # Expressions

    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        frame = o.frame
        sym = o.sym
        
        # Get operators
        op = node.operator
        
        # Generate code for left and right operands
        left_code, left_type = self.visit(node.left, Access(frame, sym, False))
        right_code, right_type = self.visit(node.right, Access(frame, sym, False))
        
        if type(left_type) is type(right_type):
            rt = left_type
        elif isinstance(left_type, IntType) and isinstance(right_type, FloatType):
            left_code += self.emit.emit_i2f(frame)
            rt = FloatType()
        elif isinstance(left_type, FloatType) and isinstance(right_type, IntType):
            right_code += self.emit.emit_i2f(frame)
            rt = FloatType()
        
        if op in ['+', '-']:
            opc = self.emit.emit_add_op(op, rt, frame)
        
        elif op == '*':
            opc = self.emit.emit_mul_op(op, rt, frame)
        
        elif op == '/':
            if isinstance(rt, IntType):
                left_code += self.emit.emit_i2f(frame)
                right_code += self.emit.emit_i2f(frame)
                rt = FloatType()
            opc = self.emit.emit_mul_op(op, rt, frame)
            
        elif op == '%':
            opc = self.emit.emit_mod(frame)
            rt = IntType()
            
        elif op == ">>":
            rt = IntType()
            opc = "ishr\n"
            frame.pop()      # shift amount
            frame.pop()      # value
            frame.push(IntType())  # push kết quả
                        
        elif op in ['==', '!=', '<', '<=', '>', '>=']:
            opc = self.emit.emit_rel_op(op, rt, frame)
            rt = BoolType()

        elif op in ['&&', '||']:
            rt = BoolType()
            if op == '&&':
                false_label = frame.get_new_label()
                end_label = frame.get_new_label()
                code = ""

                # left operand
                code += left_code
                code += self.emit.emit_if_false(false_label, frame)

                # right operand
                code += right_code
                code += self.emit.emit_if_false(false_label, frame)

                # All is True
                code += self.emit.emit_push_iconst(1, frame)
                code += self.emit.emit_goto(end_label, frame)

                # One if False
                code += self.emit.emit_label(false_label, frame)
                code += self.emit.emit_push_iconst(0, frame)

                # End
                code += self.emit.emit_label(end_label, frame)
                return code, rt
            
            else:
                true_label = frame.get_new_label()
                end_label = frame.get_new_label()
                code = ""

                # left operand
                code += left_code
                code += self.emit.emit_if_true(true_label, frame)


                code += right_code
                code += self.emit.emit_if_true(true_label, frame)

                # Both false, push 0
                code += self.emit.emit_push_iconst(0, frame)
                code += self.emit.emit_goto(end_label, frame)

                # True case, push 1
                code += self.emit.emit_label(true_label, frame)
                code += self.emit.emit_push_iconst(1, frame)

                # End
                code += self.emit.emit_label(end_label, frame)
                return code, rt
        
        code = left_code + right_code + opc
        return code, rt

    def visit_unary_op(self, node: "UnaryOp", o: Any = None):
        frame = o.frame
        opc, opt = self.visit(node.operand, o)
        op = node.operator

        if op == "!": 
            code = opc + self.emit.emit_not(opt, frame)
            rt = opt

        elif op == "-":
            code = opc + self.emit.emit_neg_op(opt, frame)
            rt = opt

        elif op == "+":
            code = opc
            rt = opt

        else:
            code = opc
            rt = opt

        return code, rt


    def visit_function_call(self, node: "FunctionCall", o: Access = None):
        function_name = node.function.name
        function_symbol = next(filter(lambda x: x.name == function_name, o.sym), False)
        class_name = function_symbol.value.value
        argument_codes = []
        for argument in node.args:
            ac, at = self.visit(argument, Access(o.frame, o.sym))
            argument_codes += [ac]

        return (
            "".join(argument_codes)
            + self.emit.emit_invoke_static(
                class_name + "/" + function_name, function_symbol.type, o.frame
            ),
            VoidType(),
        )

    def visit_array_access(self, node: "ArrayAccess", o: Any = None):
        frame = o.frame
        sym = o.sym
        # Generate code for array and index
        array_code, array_typ = self.visit(node.array, Access(frame, sym, False))
        index_code, index_typ = self.visit(node.index, Access(frame, sym, False))

        ele_type = array_typ.eleType

        if o.is_left:
            code = array_code + index_code
            return code, ele_type
        else:
            code = array_code + index_code
            code += self.emit.emit_aload(ele_type, frame)
            return code, ele_type

    def visit_array_literal(self, node: "ArrayLiteral", o: Any = None):
        element_code = ""
        element_types = []

        for elem in node.elements:
            ec, et = self.visit(elem, o)
            element_code += ec
            element_types.append(et)

        element_type = element_types[0]
        arr_type = ArrayType(element_type, len(node.elements))

        code = ""
        code += self.emit.emit_push_const(len(node.elements), o.frame)
        code += self.emit.emit_new_array(element_type)

        for i, elem in enumerate(node.elements):
            ec, _ = self.visit(elem, o)
            code += self.emit.emit_dup(o.frame)
            code += self.emit.emit_push_iconst(i, o.frame)
            code += ec
            code += self.emit.emit_astore(element_type, o.frame)

        return code, arr_type


    def visit_identifier(self, node: "Identifier", o: Any = None):
        sym = next(filter(lambda x: x.name == node.name, o.sym), None)
        if o.is_left:
            if isinstance(sym.value, Index):
                code = self.emit.emit_write_var(sym.name, sym.type, sym.value.value, o.frame)
            
            elif isinstance(sym.value, CName):
                code = self.emit.emit_put_static(sym.value.value + "." + sym.name, sym.mtype, o.frame) 
        else:
            if type(sym.value) is Index:
                code = self.emit.emit_read_var(sym.name, sym.type, sym.value.value, o.frame)
            else:
                 code = self.emit.emit_get_static(sym.value.value + "." + sym.name, sym.mtype, o.frame)
        
        return code, sym.type
                

    # Literals

    def visit_integer_literal(self, node: "IntegerLiteral", o: Access = None):
        return self.emit.emit_push_iconst(node.value, o.frame), IntType()

    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        return self.emit.emit_push_fconst(node.value, o.frame), FloatType()

    def visit_boolean_literal(self, node: "BooleanLiteral", o: Any = None):
        return self.emit.emit_push_iconst(node.value, o.frame), BoolType()

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        return self.emit.emit_push_const(node.value, o.frame), StringType()
