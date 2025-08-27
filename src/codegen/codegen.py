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
        self.current_frame: Optional[Frame] = None
        self.global_inits = []
    
    def generate_method(self, node: "FuncDecl", o: SubBody = None):
        frame = self.gframe(o)
        old_frame = self.current_frame
        self.current_frame = frame

        is_init, is_main = node.name == "<init>", node.name == "main"

        if is_main:
            param_types, return_type = [ArrayType(StringType(), 0)], VoidType()
        else:
            param_types = [p.param_type for p in node.params]
            return_type = node.return_type

        method_type = FunctionType(param_types, return_type)
        self.emit.print_out(self.emit.emit_method(node.name, method_type, not is_init))

        frame.enter_scope(is_proc=True)
        start_lbl, end_lbl = frame.get_start_label(), frame.get_end_label()

        if is_init:
            idx_this = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(idx_this, "this", ClassType(self.class_name), start_lbl, end_lbl)
            )
        elif is_main:
            args_idx = frame.get_new_index()
            self.emit.print_out(
                self.emit.emit_var(
                    args_idx, "args", ArrayType(StringType(), 0), start_lbl, end_lbl
                )
            )

        else:
            for prm in node.params:
                o = self.visit(prm, o)

        self.emit.print_out(self.emit.emit_label(start_lbl, frame))

        if is_init:
            self.emit.print_out(self.emit.emit_read_var("this", ClassType(self.class_name), idx_this, frame))
            self.emit.print_out(self.emit.emit_invoke_special(frame))

        for stmt in node.body:
            o = self.visit(stmt, o)

        if isinstance(return_type, VoidType):
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))

        self.emit.print_out(self.emit.emit_label(end_lbl, frame))
        self.emit.print_out(self.emit.emit_end_method(frame))
        frame.exit_scope()
        
        self.current_frame = old_frame
        
    def get_name_string(self, name_obj):
        """Convert name to string, handling both Identifier objects and strings"""
        if hasattr(name_obj, 'name'):
            return name_obj.name
        return str(name_obj)
    
    def _infer_type(self, node, sym_table):

        def _lookup_identifier(id_node):
            sym = next((s for s in sym_table if s.name == id_node.name), None)
            if not sym:
                raise IllegalOperandException(id_node.name)
            return sym.type

        match node:
            case IntegerLiteral():
                return IntType()
            case FloatLiteral():
                return FloatType()
            case BooleanLiteral():
                return BoolType()
            case StringLiteral():
                return StringType()
            case ArrayLiteral():
                elems = getattr(node, "elements", None) or getattr(node, "value", None)
                if not elems:
                    raise IllegalOperandException("Cannot infer type of empty array literal")

                first = elems[0]
                if isinstance(first, Identifier):
                    elem_type = _lookup_identifier(first)
                else:
                    elem_type = self._infer_type(first, sym_table)

                return ArrayType(elem_type, len(elems))

            case Identifier():
                return _lookup_identifier(node)

            case ArrayAccess():
                arr_type = (
                    _lookup_identifier(node.array)
                    if isinstance(node.array, Identifier)
                    else self._infer_type_from_literal(node.array, sym_table)
                )
                if not isinstance(arr_type, ArrayType):
                    raise IllegalOperandException("Cannot index into non-array")
                return arr_type.element_type

            case _:
                # fallback: gọi visit nhưng dùng frame đặc biệt chỉ để lấy type
                _, t = self.visit(node, Access(Frame("<infer>", VoidType()), sym_table))
                return t

    def visit_program(self, node: "Program", o: Any = None):
        self.emit.print_out(self.emit.emit_prolog(self.class_name, "java/lang/Object"))
        symbols = list(IO_SYMBOL_LIST)
        self.global_inits = []
        
        # Case 1: Handle const and variable
        env = SubBody(None, symbols)
        for decl in node.const_decls:
            if isinstance(decl, (ConstDecl, VarDecl)):
                env = self.visit(decl, env)
        symbols = env.sym
        
        # Case 2: Handle function declaration
        for func in filter(lambda acc: isinstance(acc, FuncDecl), node.func_decls):
            function_type = FunctionType([p.param_type for p in func.params], func.return_type)
            symbols.append(Symbol(func.name, function_type, CName(self.class_name)))
        global_env = SubBody(None, symbols)
        
        # Case 3: Generate <clinit>
        if self.global_inits:
            self._gen_clinit(symbols)

        # Case 4: Code
        for func in node.func_decls:
            if isinstance(func, FuncDecl):
                self.visit(func, global_env)

        # Constructor
        constructor_decl = FuncDecl("<init>", [], VoidType(), [])
        self.generate_method(constructor_decl, SubBody(Frame("<init>", VoidType()), []))

        self.emit.emit_epilog()
    
    def _gen_clinit(self, symbols):
        frame = Frame("<clinit>", VoidType())
        out = self.emit.print_out

        out(".method public static <clinit>()V\n")
        out("Label0:\n")

        for name, value, typ in self.global_inits:
            name_str = self.get_name_string(name)
            rc, _ = self.visit(value, Access(frame, symbols))
            out(rc)
            putstatic_code = self.emit.emit_put_static(f"{self.class_name}/{name_str}", typ, frame)
            out(putstatic_code if putstatic_code.endswith("\n") else putstatic_code + "\n")

        out("\treturn\nLabel1:\n")
        out(".limit stack 10\n.limit locals 0\n.end method\n")
    
    def gframe(self, o: Any):
        if isinstance(o, (Access, SubBody)) and getattr(o, "frame", None) is not None:
            return o.frame
        if self.current_frame is not None:
            return self.current_frame
        raise IllegalRuntimeException("Frame is not available")

    def gsym(self, o: Any):
        if isinstance(o, (Access, SubBody)):
            return getattr(o, "sym", [])
        return []

    def visit_const_decl(self, node: "ConstDecl", o: Any = None):
        symbols = self.gsym(o)
        const_type = self._infer_type(node.value, symbols)
        
        const_name = self.get_name_string(node.name)
        
        decl = self.emit.emit_attribute(const_name, const_type, is_final=True, value=None)
        self.emit.print_out(decl)
        
        # Add into symbol table
        symbols.append(Symbol(const_name, const_type, CName(self.class_name)))
        
        self.global_inits = getattr(self, "global_inits", [])
        self.global_inits.append((node.name, node.value, const_type))
        return SubBody(getattr(o, "frame", None), symbols)

    def visit_func_decl(self, node: "FuncDecl", o: SubBody = None):
        func_name = self.get_name_string(node.name)
        func_frame = Frame(func_name, node.return_type)
        self.generate_method(node, SubBody(func_frame, o.sym))
        
        # Take the param lists
        param_types = [param.param_type for param in node.params]
        func_symbol = Symbol(
            func_name,
            FunctionType(param_types, node.return_type),
            CName(self.class_name),
        )
        return SubBody(None, [func_symbol] + o.sym)

    def visit_param(self, node: "Param", o: Any = None):
        frame = self.gframe(o)
        
        param_name = self.get_name_string(node.name)
        index = frame.get_new_index()
        
        var_decl = self.emit.emit_var(
            index, param_name, node.param_type, frame.get_start_label(), frame.get_end_label()
        )
        self.emit.print_out(var_decl)
        
        param_symbol = Symbol(param_name, node.param_type, Index(index))
        return SubBody(frame, [param_symbol] + o.sym)

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
        return ArrayType()

    # Statements

    # def visit_var_decl(self, node: "VarDecl", o: SubBody = None):
    #     frame = self.gframe(o)
    #     symbols = self.gsym(o)
        
    #     var_name = self.get_name_string(node.name).strip()
    #     if node.type_annotation:
    #         typ = node.type_annotation
    #     else:
    #         if node.value is None:
    #             raise IllegalOperandException(f"Cannot infer type for variable '{var_name}' without initializer")
        
    #         def check_type(expr):
    #             if isinstance(expr, IntegerLiteral):
    #                 return IntType()
    #             if isinstance(expr, FloatLiteral):
    #                 return FloatType()
    #             if isinstance(expr, BooleanLiteral):
    #                 return BoolType()
    #             if isinstance(expr, StringLiteral):
    #                 return StringType()
    #             if isinstance(expr, ArrayLiteral):
    #                 elements = getattr(expr, "elements", None) or getattr(expr, "value", None)
    #                 if not elements:
    #                     raise IllegalOperandException("Cannot infer type of empty array literal")

    #                 first = elements[0]
    #                 if isinstance(first, Identifier):
    #                     symbol = next((sym.type for sym in symbols if sym.name == first.name), None)
    #                     element_type = symbol or self.visit(first, Access(Frame("<infer>", VoidType()), symbols))[1]
    #                 else:
    #                     element_type = check_type(first)
                    
    #                 return ArrayType(element_type, len(elements))
                
    #             if isinstance(expr, Identifier):
    #                 symbol = next((sym for sym in symbols if sym.name == expr.name), None)
    #                 if not symbol:
    #                     raise IllegalOperandException(expr.name)
    #                 return symbol.type
    #             if isinstance(expr, ArrayAccess):
    #                 temp = None
    #                 if isinstance(expr.array, Identifier):
    #                     symbol = next((sym for sym in symbols if sym.name == expr.array.name), None)
    #                     if not symbol:
    #                         raise IllegalOperandException(expr.array.name)
    #                     temp = symbol.type()
    #                 else:
    #                     temp = check_type(expr.array)
                    
    #                 if not isinstance(temp, ArrayType):
    #                     raise IllegalOperandException("Cannot index the non-array type")
    #                 return temp.element_type
    #             _, t = self.visit(expr, Access(frame, symbols))
                
    #             return t
    #         typ = check_type(node.value)
    #     index = frame.get_new_index()
    #     var_decl = self.emit.emit_var(index, var_name, typ, frame.get_start_label(), frame.get_end_label())
    #     self.emit.print_out(var_decl)

    #     new_symbols = [Symbol(var_name, typ, Index(index))] + symbols
    #     if node.value:
    #         if isinstance(node.value, ArrayLiteral):
    #             code, temp = self.visit(node.value, Access(frame, new_symbols))
    #             self.emit.print_out(code)
    #             self.emit.print_out(self.emit.emit_write_var(var_name, temp, index, frame))
    #         else:
    #             self.visit(Assignment(IdLValue(var_name), node.value), SubBody(frame, new_symbols))

    #     return SubBody(frame, new_symbols)
    def visit_var_decl(self, node: "VarDecl", o: SubBody = None):
        frame = self.gframe(o)
        symbols = self.gsym(o)

        var_name = self.get_name_string(node.name)

        # determine var type
        if node.type_annotation:
            var_type = node.type_annotation
        else:
            if node.value is None:
                raise IllegalOperandException(f"Cannot infer type for variable '{var_name}' without initializer")
            var_type = self._infer_type(node.value, symbols)
        print(f"Variable type is: : {var_type}")
        index = frame.get_new_index()
        var_decl = self.emit.emit_var(index, var_name, var_type, frame.get_start_label(), frame.get_end_label())
        self.emit.print_out(var_decl)

        new_symbols = [Symbol(var_name, var_type, Index(index))] + symbols

        # initializer handling
        if node.value:
            print("value is not None")
            if isinstance(node.value, ArrayLiteral):
                code, elem_t = self.visit(node.value, Access(frame, new_symbols))
                self.emit.print_out(code)
                print(f"DEBUG: Writing var {var_name} of type {elem_t}")
                self.emit.print_out(self.emit.emit_write_var(var_name, elem_t, index, frame))
            else:
                self.visit(Assignment(IdLValue(var_name), node.value), SubBody(frame, new_symbols))
        else:
            print("value is None")
            init_code = ""
            if isinstance(var_type, IntType) or isinstance(var_type, BoolType):
                init_code += self.emit.emit_push_iconst(0, frame)
            elif isinstance(var_type, FloatType):
                init_code += self.emit.emit_push_fconst(0.0, frame)  # or fconst_0
            elif isinstance(var_type, StringType):
                pass
            elif isinstance(var_type, ArrayType):
                size = getattr(var_type, "size", 0) or 0
                init_code += self.emit.emit_push_iconst(size, frame)
                et = var_type.element_type
                if isinstance(et, IntType):
                    init_code += self.emit.emit_new_array("int")
                elif isinstance(et, BoolType):
                    init_code += self.emit.emit_new_array("boolean")
                    print("Created boolean array")
                elif isinstance(et, FloatType):
                    init_code += self.emit.emit_new_array("float")
                elif isinstance(et, StringType):
                    init_code += "anewarray java/lang/String\n"
                elif isinstance(et, ArrayType):
                    descriptor = self.emit.get_jvm_type(et)
                    init_code += f"anewarray {descriptor}\n"
                else:
                    raise IllegalOperandException(f"Unsupported array element type: {et}")

            init_code += self.emit.emit_write_var(var_name, var_type, index, frame)
            self.emit.print_out(init_code)

        return SubBody(frame, new_symbols)


    def visit_assignment(self, node: "Assignment", o: SubBody = None):
        frame = self.gframe(o)
        symbols = self.gsym(o)

        # Case 1: Assignment the array's component
        if isinstance(node.lvalue, ArrayAccessLValue):
            arr_code, arr_type = self.visit(node.lvalue.array, Access(frame, symbols))
            idx_code, idx_type = self.visit(node.lvalue.index, Access(frame, symbols))
            rhs_code, rhs_type = self.visit(node.value, Access(frame, symbols))

            if isinstance(rhs_type, ArrayType):
                desc = self.emit.get_jvm_type(rhs_type)
                rhs_code += f"\tinvokevirtual {desc}/clone()Ljava/lang/Object;\n"
                rhs_code += f"\tcheckcast {desc}\n"

            self.emit.print_out(arr_code)
            self.emit.print_out(idx_code)
            self.emit.print_out(rhs_code)

            etype = arr_type.element_type
            if isinstance(etype, IntType):
                self.emit.print_out("iastore\n")
            elif isinstance(etype, BoolType):
                self.emit.print_out("bastore\n")
            elif isinstance(etype, FloatType):
                self.emit.print_out("fastore\n")
            else:
                self.emit.print_out("aastore\n")

        # Case 2: Assignment for common variable
        else:
            # rhs_code, rhs_type = self.visit(node.value, Access(frame, symbols))

            # if isinstance(rhs_type, ArrayType):
            #     desc = self.emit.get_jvm_type(rhs_type)
            #     rhs_code += f"\tinvokevirtual {desc}/clone()Ljava/lang/Object;\n"
            #     rhs_code += f"\tcheckcast {desc}\n"

            # self.emit.print_out(rhs_code)

            # lhs_code, _ = self.visit(node.lvalue, Access(frame, symbols))
            # self.emit.print_out(lhs_code)
            rhs_code, rhs_type = self.visit(node.value, Access(frame, symbols))
            self.emit.print_out(rhs_code)

            # Determine variable symbol
            var_name = node.lvalue.name
            symbol = next((s for s in symbols if s.name == var_name), None)
            if symbol is None:
                raise IllegalOperandException(f"Undeclared variable: {var_name}")
            self.emit.print_out(self.emit.emit_write_var(var_name, symbol.type, symbol.value.value, frame))
            print("flag called them")

        return o

    def visit_if_stmt(self, node: "IfStmt", o: Any = None):
        frame = self.gframe(o)
        symbols = self.gsym(o)
        
        end_label = frame.get_new_label()
        else_label = frame.get_new_label()
        
        # Generate code for the condition expr
        cond_code, cond_type = self.visit(node.condition, Access(frame, symbols, False))
        self.emit.print_out(cond_code)
        
        # Jump to else_label if false
        self.emit.print_out(self.emit.emit_if_false(else_label, frame))
        
        # Generate code for then_stmt
        self.visit(node.then_stmt, o)
        
        # Jump to end_label with all case
        self.emit.print_out(self.emit.emit_goto(end_label, frame))
        
        # Jump to else elif label
        self.emit.print_out(self.emit.emit_label(else_label, frame))
        
        if getattr(node, "elif_branches", None):
            for cond, body in node.elif_branches:
                next_label = frame.get_new_label()
                cond_code, _ = self.visit(cond, Access(frame, symbols))
                self.emit.print_out(cond_code)
                self.emit.print_out(self.emit.emit_if_false(next_label, frame))
                self.visit(body, o)
                self.emit.print_out(self.emit.emit_goto(end_label, frame))
                self.emit.print_out(self.emit.emit_label(next_label, frame))
        
        # Generate code for else_stmt
        if node.else_stmt:
            self.visit(node.else_stmt, o)
            
        # Put end_label
        self.emit.print_out(self.emit.emit_label(end_label, frame))

        return o
            
    def visit_while_stmt(self, node: "WhileStmt", o: Any = None):
        frame = self.gframe(o)
        sym = self.gsym(o)

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
        self.visit(node.body, SubBody(frame, sym))
        
        # Jump to continue_label with all cases
        self.emit.print_out(self.emit.emit_goto(continue_label, frame))
        
        # Put break_label
        self.emit.print_out(self.emit.emit_label(break_label, frame))

        frame.exit_loop()
        return o

    def visit_for_stmt(self, node: "ForStmt", o: Any):
        frame = self.gframe(o)
        sym = self.gsym(o)

        full_code = ""

        # 1. Collection
        col_code, col_type = self.visit(node.iterable, Access(frame, sym))
        full_code += col_code

        arr_tmp_idx = frame.get_new_index()
        arr_tmp_name = f"__arr_for_{arr_tmp_idx}"
        full_code += self.emit.emit_var(arr_tmp_idx, arr_tmp_name, col_type, frame.get_start_label(), frame.get_end_label())
        full_code += self.emit.emit_write_var(arr_tmp_name, col_type, arr_tmp_idx, frame)

        # 2. Create index = 0
        idx_tmp_idx = frame.get_new_index()
        idx_tmp_name = f"__idx_for_{idx_tmp_idx}"
        full_code += self.emit.emit_var(idx_tmp_idx, idx_tmp_name, IntType(), frame.get_start_label(), frame.get_end_label())
        full_code += self.emit.emit_push_iconst(0, frame)
        full_code += self.emit.emit_write_var(idx_tmp_name, IntType(), idx_tmp_idx, frame)

        # 3. Generate label break/continue
        start_label = frame.get_new_label()
        end_label = frame.get_new_label()
        continue_target_label = frame.get_new_label()

        prev_break = getattr(frame, "_break_label", None)
        prev_continue = getattr(frame, "_continue_label", None)
        frame._break_label = end_label
        frame._continue_label = continue_target_label

        # 4. Loop
        full_code += self.emit.emit_label(start_label, frame)
        full_code += self.emit.emit_read_var(idx_tmp_name, IntType(), idx_tmp_idx, frame)
        full_code += self.emit.emit_read_var(arr_tmp_name, col_type, arr_tmp_idx, frame)
        full_code += "arraylength\n"
        full_code += f"if_icmpge Label{end_label}\n"

        # 5. Take element
        full_code += self.emit.emit_read_var(arr_tmp_name, col_type, arr_tmp_idx, frame)
        full_code += self.emit.emit_read_var(idx_tmp_name, IntType(), idx_tmp_idx, frame)

        elem_type = col_type.element_type
        if isinstance(elem_type, (IntType, BoolType)):
            full_code += "iaload\n"
        elif isinstance(elem_type, FloatType):
            full_code += "faload\n"
        else:
            full_code += "aaload\n"

        loop_var_name = node.variable
        loop_var_idx = frame.get_new_index()
        full_code += self.emit.emit_var(loop_var_idx, loop_var_name, elem_type, frame.get_start_label(), frame.get_end_label())
        full_code += self.emit.emit_write_var(loop_var_name, elem_type, loop_var_idx, frame)

        body_sym = [Symbol(loop_var_name, elem_type, Index(loop_var_idx))] + sym

        self.emit.print_out(full_code)

        # Visit body of loop
        self.visit(node.body, SubBody(frame, body_sym))

        # Update index
        cont_code = ""
        cont_code += self.emit.emit_label(continue_target_label, frame)
        cont_code += f"iinc {idx_tmp_idx} 1\n"
        cont_code += self.emit.emit_goto(start_label, frame)
        cont_code += self.emit.emit_label(end_label, frame)

        self.emit.print_out(cont_code)

        # Restore
        frame._break_label = prev_break
        frame._continue_label = prev_continue

        return o

    def visit_return_stmt(self, node: "ReturnStmt", o: Any = None):
        frame = self.gframe(o)
        symbols = self.gsym(o)
        
        if node.value:
            expr_code, expr_type = self.visit(node.value, Access(frame, symbols, False))
            self.emit.print_out(expr_code)
            self.emit.print_out(self.emit.emit_return(expr_type, frame))
        else:
            self.emit.print_out(self.emit.emit_return(VoidType(), frame))
        
        return o

    def visit_break_stmt(self, node: "BreakStmt", o: Any = None):
        frame = self.gframe(o)
        break_label = frame.get_break_label()

        if break_label is None:
            raise IllegalRuntimeException("Break not in loop")

        code = self.emit.emit_goto(break_label, frame)
        self.emit.print_out(code)
        return o

    def visit_continue_stmt(self, node: "ContinueStmt", o: Any = None):
        frame = self.gframe(o)
        continue_label = frame.get_continue_label()

        if continue_label is None:
            raise IllegalRuntimeException("Continue not in loop")

        code = self.emit.emit_goto(continue_label, frame)
        self.emit.print_out(code)
        return o

    def visit_expr_stmt(self, node: "ExprStmt", o: SubBody = None):
        frame = self.gframe(o)
        symbols = self.gsym(o)
        code, typ = self.visit(node.expr, Access(frame, symbols))
        full_code = code
        
        if not isinstance(typ, VoidType):
            full_code += self.emit.emit_pop(frame)

        self.emit.print_out(full_code)
        return o

    def visit_block_stmt(self, node: "BlockStmt", o: Any = None):
        frame = self.gframe(o)
        symbols = self.gsym(o)
        
        # Enter new scope
        frame.enter_scope(False)
        
        full_code = ""
        full_code += self.emit.emit_label(frame.get_start_label(), frame)

        # Visit all statements inside the block
        in_env = SubBody(frame, symbols[:])
        for stmt in node.statements:
            # self.visit(stmt, SubBody(frame, in_env))
            self.visit(stmt, in_env)

        # Emit end label for the block
        full_code += self.emit.emit_label(frame.get_end_label(), frame)

        # Exit scope
        frame.exit_scope()
        self.emit.print_out(full_code)
        return SubBody(frame, symbols)

    # Left-values

    def visit_id_lvalue(self, node: "IdLValue", o: Access = None):
        frame = self.gframe(o)
        
        lvalue_name = self.get_name_string(node.name)
        sym = next((s for s in o.sym if s.name == lvalue_name), None)
        if not sym:
            raise IllegalOperandException(lvalue_name)

        if isinstance(sym.value, Index):
            return self.emit.emit_write_var(sym.name, sym.type, sym.value.value, frame), sym.type
        elif isinstance(sym.value, CName):
            return self.emit.emit_put_static(f"{self.class_name}/{sym.name}", sym.type, frame), sym.type
        else:
            raise IllegalOperandException(lvalue_name)

    def visit_array_access_lvalue(self, node: "ArrayAccessLValue", o: Any = None):
        frame = self.gframe(o)
        sym = self.gsym(o)
        arr_code, arr_type = self.visit(node.array, Access(frame, sym, False))
        idx_code, idx_type = self.visit(node.index, Access(frame, sym, False))

        elem_type = arr_type.element_type if isinstance(arr_type, ArrayType) else arr_type
        code = arr_code
        code += idx_code
        code += self.emit.emit_aload(elem_type, frame)

        return code, elem_type


    # Expressions
    def _jvm_array_signature(self, arr_type):
        if isinstance(arr_type, ArrayType):
            return "[" + self._jvm_array_signature(arr_type.element_type)
        elif isinstance(arr_type, IntType):
            return "I"
        elif isinstance(arr_type, FloatType):
            return "F"
        elif isinstance(arr_type, BoolType):
            return "Z"
        elif isinstance(arr_type, StringType):
            return "Ljava/lang/String;"
        else:
            raise IllegalOperandException(f"Unsupported array element type: {arr_type}")

    def visit_binary_op(self, node: "BinaryOp", o: Any = None):
        frame = self.gframe(o)
        sym = self.gsym(o)
        op = node.operator
        
        if op == ">>":
            left_code, left_type = self.visit(node.left, Access(frame, sym))
            function_name = ""
            existing_args = []

            if isinstance(node.right, Identifier):
                function_name = node.right.name
                existing_args = []
            elif isinstance(node.right, FunctionCall):
                function_name = node.right.function.name
                existing_args = node.right.args
            else:
                raise IllegalOperandException(
                    f"Right operand of '>>' must be a function name or call, not {type(node.right)}"
                )

            function_symbol = next((s for s in sym if s.name == function_name), None)
            if not function_symbol or not isinstance(function_symbol.type, FunctionType):
                raise IllegalOperandException(f"'{function_name}' is not a function.")

            # build code
            code = left_code
            for arg in existing_args:
                arg_code, _ = self.visit(arg, Access(frame, sym))
                code += arg_code
            class_name_str = self.class_name.name if isinstance(self.class_name, Identifier) else str(self.class_name)
            code += self.emit.emit_invoke_static( f"{class_name_str}/{function_name}", function_symbol.type, frame)
            return code, function_symbol.type.return_type

        # boolean short-circuit &&, ||
        if op in ["&&", "||"]:
            left_code, left_type = self.visit(node.left, Access(frame, sym))
            label_check = frame.get_new_label()
            label_false = frame.get_new_label()
            label_end = frame.get_new_label()

            code = left_code
            if op == "&&":
                code += self.emit.emit_if_false(label_false, frame)
                right_code, _ = self.visit(node.right, Access(frame, sym))
                code += right_code
                code += self.emit.emit_if_false(label_false, frame)
                code += self.emit.emit_push_iconst(1, frame)
                code += self.emit.emit_goto(label_end, frame)
            else:  # op == "||"
                code += self.emit.emit_if_false(label_check, frame)
                code += self.emit.emit_push_iconst(1, frame)
                code += self.emit.emit_goto(label_end, frame)
                code += self.emit.emit_label(label_check, frame)
                right_code, _ = self.visit(node.right, Access(frame, sym))
                code += right_code
                code += self.emit.emit_if_false(label_false, frame)
                code += self.emit.emit_push_iconst(1, frame)
                code += self.emit.emit_goto(label_end, frame)

            code += self.emit.emit_label(label_false, frame)
            code += self.emit.emit_push_iconst(0, frame)
            code += self.emit.emit_label(label_end, frame)
            return code, BoolType()

        # normal binary ops
        left_code, left_type = self.visit(node.left, Access(frame, sym))
        right_code, right_type = self.visit(node.right, Access(frame, sym))

        # string concatenation
        if op == '+' and (isinstance(left_type, StringType) or isinstance(right_type, StringType)):
            def _to_string_code(code_str, in_type):
                if isinstance(in_type, StringType):
                    return code_str
                elif isinstance(in_type, IntType):
                    return code_str + "invokestatic io/int2str(I)Ljava/lang/String;\n"
                elif isinstance(in_type, FloatType):
                    return code_str + "invokestatic io/float2str(F)Ljava/lang/String;\n"
                elif isinstance(in_type, BoolType):
                    return code_str + "invokestatic io/bool2str(Z)Ljava/lang/String;\n"
                return code_str

            str_left_code = _to_string_code(left_code, left_type)
            str_right_code = _to_string_code(right_code, right_type)

            return str_left_code + str_right_code + self.emit.emit_concat(frame), StringType()

        if op == '/':
            code = ""
            # push left then convert if needed
            code += left_code
            if isinstance(left_type, IntType):
                code += self.emit.emit_i2f(frame)
            # push right then convert if needed
            code += right_code
            if isinstance(right_type, IntType):
                code += self.emit.emit_i2f(frame)
            # emit float divide (your emitter may have a helper; use it)
            # if your emitter uses emit_mul_op for '/' too, call with FloatType
            code += self.emit.emit_mul_op('/', FloatType(), frame)
            return code, FloatType()    
        
        # type promotion
        result_type = left_type
        if isinstance(left_type, IntType) and isinstance(right_type, FloatType):
            left_code += self.emit.emit_i2f(frame)
            result_type = FloatType()
        elif isinstance(left_type, FloatType) and isinstance(right_type, IntType):
            right_code += self.emit.emit_i2f(frame)
            result_type = FloatType()
        elif isinstance(left_type, FloatType) and isinstance(right_type, FloatType):
            result_type = FloatType()

        full_code = left_code + right_code

        if op in ['+', '-']:
            return full_code + self.emit.emit_add_op(op, result_type, frame), result_type
        elif op in ['*', '/']:
            if op == '*':
                return full_code + self.emit.emit_mul_op(op, result_type, frame), result_type
            else:
                if not isinstance(left_type, FloatType):
                    left_code += self.emit.emit_i2f(frame)
                if not isinstance(right_type, FloatType):
                    right_code += self.emit.emit_i2f(frame)
                result_type = FloatType()
            return left_code + right_code + self.emit.emit_mul_op(op, result_type, frame), result_type

        elif op == '%':
            return full_code + self.emit.emit_mod(frame), IntType()
        elif op in ['==', '!=', '<', '<=', '>', '>=']:
            return full_code + self.emit.emit_re_op(op, result_type, frame), BoolType()
        raise IllegalOperandException(f"Unsupported operator: {op}")

    def visit_unary_op(self, node: "UnaryOp", o):
        frame = self.gframe(o)
        sym = self.gsym(o)
        expr_code, expr_type = self.visit(node.operand, Access(frame, sym))
        op = node.operator

        self.emit.print_out(expr_code)

        if op == "-":
            self.emit.print_out(self.emit.emit_neg_op(expr_type, frame))
            return "", expr_type

        elif op == "+":
            return "", expr_type

        elif op == "!":
            label_true = frame.get_new_label()
            label_end = frame.get_new_label()

            self.emit.print_out(f"ifeq Label{label_true}\n")
            self.emit.print_out("iconst_0\n")
            self.emit.print_out(f"goto Label{label_end}\n")
            self.emit.print_out(f"Label{label_true}:\n")
            self.emit.print_out("iconst_1\n")
            self.emit.print_out(f"Label{label_end}:\n")
            return "", BoolType()

        else:
            raise IllegalOperandException(f"Unsupported unary operator: {op}")

    def visit_function_call(self, node: "FunctionCall", o: Access = None):
        frame = self.gframe(o)
        sym = self.gsym(o)
        if not isinstance(node.function, Identifier):
            raise IllegalOperandException(f"Unsupported function type: {type(node.function)}")

        function_name = node.function.name

        # builtin len (đặc biệt vì không nằm trong class io)
        if function_name == "len":
            if len(node.args) != 1:
                raise IllegalOperandException("len requires exactly one argument")

            arg_code, arg_type = self.visit(node.args[0], Access(frame, sym))
            if isinstance(arg_type, ArrayType):
                code = arg_code + "arraylength\n"
                return code, IntType()

            elif isinstance(arg_type, StringType):
                code = arg_code + "invokevirtual java/lang/String/length()I\n"
                return code, IntType()
            else:
                raise IllegalOperandException("len expects array or string argument")
        
        if function_name == "print":
            if len(node.args) != 1:
                raise IllegalOperandException("print requires exactly one argument")
            
            arg_code, arg_type = self.visit(node.args[0], Access(frame, sym))
            code = arg_code
            
            if isinstance(arg_type, IntType):
                code += self.emit.emit_invoke_static(
                    "io/int2str", 
                    FunctionType([IntType()], StringType()),  # (I)Ljava/lang/String;
                    frame
                )
            elif isinstance(arg_type, FloatType):
                code += self.emit.emit_invoke_static(
                    "io/float2str",
                    FunctionType([FloatType()], StringType()),  # (F)Ljava/lang/String;
                    frame
                )
            elif isinstance(arg_type, BoolType):
                code += self.emit.emit_invoke_static(
                    "io/bool2str",
                    FunctionType([BoolType()], StringType()),  # (Z)Ljava/lang/String;
                    frame
                )
            elif isinstance(arg_type, StringType):
                pass
            else:
                raise IllegalOperandException(f"print does not support type: {type(arg_type)}")
            
            code += self.emit.emit_invoke_static(
                "io/print",
                FunctionType([StringType()], VoidType()),
                frame
            )
            return code, VoidType()

        # tìm trong symbol table hoặc IO builtins
        function_symbol = next((x for x in sym if x.name == function_name), None)
        if not function_symbol:
            function_symbol = next((x for x in IO_SYMBOL_LIST if x.name == function_name), None)
        if not function_symbol:
            raise IllegalOperandException(function_name)

        # class chứa hàm
        class_name = (
            function_symbol.value.value
            if isinstance(function_symbol.value, CName)
            else self.class_name
        )

        # sinh code cho arguments (push lên stack trước khi invoke)
        code = ""
        arg_types = []
        for arg in node.args:
            ac, at = self.visit(arg, Access(frame, sym))
            code += ac
            arg_types.append(at)

        # emit invokestatic (dùng emit_invoke_static để sinh descriptor đúng)
        code += self.emit.emit_invoke_static(
            f"{class_name}/{function_name}", function_symbol.type, frame
        )

        ret_type = getattr(function_symbol.type, "return_type", VoidType())
        return code, ret_type

    def visit_array_access(self, node: "ArrayAccess", o: Any = None):
        frame = self.gframe(o)
        sym = self.gsym(o)
        # Generate code for array and index
        array_code, array_typ = self.visit(node.array, Access(frame, sym, False))
        index_code, index_typ = self.visit(node.index, Access(frame, sym, False))

        ele_type = array_typ.element_type
        code = array_code + index_code

        if o.is_left:
            return code, ele_type
        else:
            if isinstance(ele_type, IntType):
                code += "iaload\n"
            elif isinstance(ele_type, FloatType):
                code += "faload\n"
            elif isinstance(ele_type, BoolType):
                code += "baload\n"  # boolean array in JVM uses baload
            elif isinstance(ele_type, (ArrayType, StringType, ClassType)):
                code += "aaload\n"
            else:
                raise IllegalOperandException(f"Unsupported array element type: {ele_type}")
            
            return code, ele_type

    def visit_array_literal(self, node: "ArrayLiteral", o: Any = None):
        frame = self.gframe(o)
        sym = self.gsym(o)
        
        elements = getattr(node, "elements", None) or getattr(node, "value", [])
        array_size = len(elements)

        if array_size == 0:
            raise IllegalOperandException("Cannot infer type from empty array literal")

        _, first_elem_type = self.visit(elements[0], Access(frame, sym))
        array_type = ArrayType(first_elem_type, array_size)

        code = ""
        code += self.emit.emit_push_iconst(array_size, frame)

        # Create array
        if isinstance(first_elem_type, IntType):
            code += self.emit.emit_new_array("int")
        elif isinstance(first_elem_type, BoolType):
            code += self.emit.emit_new_array("boolean")
        elif isinstance(first_elem_type, FloatType):
            code += self.emit.emit_new_array("float")
        elif isinstance(first_elem_type, StringType):
            code += "anewarray java/lang/String\n"
        elif isinstance(first_elem_type, ArrayType):
            descriptor = self.emit.get_jvm_type(first_elem_type)
            code += f"anewarray {descriptor}\n"
        else:
            raise IllegalOperandException(f"Unsupported array element type: {first_elem_type}")

        # Assign elements
        for idx, elem in enumerate(elements):
            code += "dup\n"
            code += self.emit.emit_push_iconst(idx, frame)

            elem_code, elem_type = self.visit(elem, Access(frame, sym))
            code += elem_code

            if isinstance(elem_type, IntType):
                code += "iastore\n"
            elif isinstance(elem_type, BoolType):
                code += "bastore\n"
            elif isinstance(elem_type, FloatType):
                code += "fastore\n"
            elif isinstance(elem_type, (StringType, ArrayType)):
                code += "aastore\n"
            else:
                raise IllegalOperandException(f"Unsupported element type for array store: {elem_type}")

        return code, array_type


    def visit_identifier(self, node: "Identifier", o: Any = None):
        frame = self.gframe(o)
        name = self.get_name_string(node.name).strip()
        sym = next((s for s in self.gsym(o) if s.name == name), None)
        if not sym:
            raise IllegalOperandException(f"Undeclared identifier: {name}")

        # Local / param
        if isinstance(sym.value, Index):
            code = self.emit.emit_read_var(sym.name, sym.type, sym.value.value, frame)
            return code, sym.type

       # Global variable (static field)
        if isinstance(sym.value, CName):
            code = self.emit.emit_get_static(f"{sym.value.value}/{sym.name}", sym.type, frame)
            return code, sym.type

        # Function reference
        if isinstance(sym.type, FunctionType):
            return "", sym.type
        raise IllegalOperandException(f"Unsupported identifier binding: {name}")        

    # Literals

    def visit_integer_literal(self, node: "IntegerLiteral", o: Access = None):
        return self.emit.emit_push_iconst(node.value, self.gframe(o)), IntType()

    def visit_float_literal(self, node: "FloatLiteral", o: Any = None):
        return self.emit.emit_push_fconst(node.value, self.gframe(o)), FloatType()

    def visit_boolean_literal(self, node: "BooleanLiteral", o: Any = None):
        frame = self.gframe(o)
        jvm_value = 1 if node.value else 0
        code = self.emit.emit_push_iconst(jvm_value, frame)
        return code, BoolType()

    def visit_string_literal(self, node: "StringLiteral", o: Any = None):
        frame = self.gframe(o)
        return (
            self.emit.emit_push_const('"' + node.value + '"', StringType(), frame),
            StringType(),
        )