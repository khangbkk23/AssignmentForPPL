"""
AST Generation module for HLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from ast import expr
from functools import reduce
from build.HLangVisitor import HLangVisitor
from build.HLangParser import HLangParser
from src.utils.nodes import *


class ASTGeneration(HLangVisitor):
    def visitProgram(self, ctx: HLangParser.ProgramContext):
        decls = self.visit(ctx.decllist())
        const_decls = [d for d in decls if isinstance(d, ConstDecl)]
        func_decls = [d for d in decls if isinstance(d, FuncDecl)]
        return Program(const_decls, func_decls)

    
    def visitDecllist(self, ctx: HLangParser.DecllistContext):
        if ctx.getChildCount() == 0:
            return []
        decl = self.visit(ctx.decl())
        tail = self.visit(ctx.decllistTail())
        return [decl] + tail
    
    def visitDecllistTail(self, ctx: HLangParser.DecllistTailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.decl())] + self.visit(ctx.decllistTail())
    
    def visitDecl(self, ctx: HLangParser.DeclContext):
        if ctx.vardecl():
            return self.visit(ctx.vardecl())
        elif ctx.constdecl():
            return self.visit(ctx.constdecl())
        elif ctx.funcdecl():
            return self.visit(ctx.funcdecl())

    def visitVardecl(self, ctx: HLangParser.VardeclContext):
        name = ctx.ID().getText()
        typ = self.visit(ctx.typeOpt())
        value = self.visit(ctx.expr()) if ctx.expr() else None
        return VarDecl(name, typ, value)
    
    def visitConstdecl(self, ctx: HLangParser.ConstdeclContext):
        name = ctx.ID().getText()
        typ = self.visit(ctx.typeOpt())
        value = self.visit(ctx.expr())
        return ConstDecl(name, typ, value)
    
    def visitFuncdecl(self, ctx: HLangParser.FuncdeclContext):
        name = ctx.ID().getText()
        params = self.visit(ctx.paramOpt())
        returnType = self.visit(ctx.typeSpec())
        body = self.visit(ctx.blockStmt())
        return FuncDecl(name, params, returnType, body.statements)
    
    def visitTypeOpt(self, ctx: HLangParser.TypeOptContext):
        if ctx.getChildCount() == 0:
            return None
        return self.visit(ctx.typeSpec())
    
    def visitTypeSpec(self, ctx: HLangParser.TypeSpecContext):
        return self.visit(ctx.getChild(0))
    
    def visitDataType(self, ctx: HLangParser.DataTypeContext):
        return {
            "int": IntType(),
            "float": FloatType(),
            "bool": BoolType(),
            "string": StringType(),
            "void": VoidType()
        }.get(ctx.getChild(0).getText())
        
    def visitArrayType(self, ctx: HLangParser.ArrayTypeContext):
        elementType = self.visit(ctx.typeSpec())
        size = int(ctx.INT_LIT().getText())
        return ArrayType(elementType, size)
    
    def visitParam(self, ctx: HLangParser.ParamContext):
        param_name = ctx.ID().getText()
        param_type = self.visit(ctx.typeSpec())
        return Param(name=param_name, param_type=param_type)
    
    def visitParamOpt(self, ctx: HLangParser.ParamOptContext):
        if ctx.getChildCount() == 0:
            return []
        first_param = self.visit(ctx.param())
        tail = self.visit(ctx.paramTail())
        return [first_param] + tail
    
    def visitParamTail(self, ctx: HLangParser.ParamTailContext):
        if ctx.getChildCount() == 0:
            return []
        this_param = self.visit(ctx.param())
        rest = self.visit(ctx.paramTail())
        return [this_param] + rest

    def visitBlockStmt(self, ctx: HLangParser.BlockStmtContext):
        stmts = self.visit(ctx.stmtList()) if ctx.stmtList() else []
        return BlockStmt(stmts)
    
    def visitStmtList(self, ctx: HLangParser.StmtListContext):
        if ctx.getChildCount() == 0:
            return []
        stmt = self.visit(ctx.stmt())
        tail = self.visit(ctx.stmtListTail())
        return [stmt] + tail
    
    def visitStmtListTail(self, ctx: HLangParser.StmtListTailContext):
        if not ctx.getChildCount():
            return []
        return [self.visit(ctx.stmt())] + self.visit(ctx.stmtListTail())
    
    def visitStmt(self, ctx: HLangParser.StmtContext):
        return self.visit(ctx.getChild(0))
    
    # Visit statements
    
    def visitAssignStmt(self, ctx: HLangParser.AssignStmtContext):
        lhs = self.visit(ctx.lvalue())
        rhs = self.visit(ctx.expr())
        return Assignment(lhs, rhs)
    
    def visitIfStmt(self, ctx: HLangParser.IfStmtContext):
        cond = self.visit(ctx.expr())
        thenStmt = self.visit(ctx.blockStmt())
        elseifList = self.visit(ctx.elseifTail())
        elseStmt = self.visit(ctx.elseOpt()) if ctx.elseOpt() else None
        return IfStmt(cond, thenStmt, elseifList, elseStmt)

    def visitElseifTail(self, ctx: HLangParser.ElseifTailContext):
        if not ctx.getChildCount():
            return []
        cond = self.visit(ctx.expr())
        block = self.visit(ctx.blockStmt())
        tail = self.visit(ctx.elseifTail())
        return [(cond, block)] + tail

    def visitElseOpt(self, ctx: HLangParser.ElseOptContext):
        if ctx.blockStmt():
            return self.visit(ctx.blockStmt())
        return None
    
    def visitWhileStmt(self, ctx: HLangParser.WhileStmtContext):
        cond = self.visit(ctx.expr())
        body = self.visit(ctx.blockStmt())
        return WhileStmt(cond, body)
    
    def visitForStmt(self, ctx: HLangParser.ForStmtContext):
        name = ctx.ID().getText()
        ite = self.visit(ctx.expr())
        body = self.visit(ctx.blockStmt())
        return ForStmt(name, ite, body)
    
    def visitBreakStmt(self, ctx: HLangParser.BreakStmtContext):
        return BreakStmt()
    
    def visitContinueStmt(self, ctx: HLangParser.ContinueStmtContext):
        return ContinueStmt()
    
    def visitReturnStmt(self, ctx: HLangParser.ReturnStmtContext):
        if ctx.exprReturn():
            expr_val = self.visit(ctx.exprReturn())
            return ReturnStmt(expr_val)
        else:
            return ReturnStmt(None)
        
    def visitExprReturn(self, ctx: HLangParser.ExprReturnContext):
        if ctx.expr():
            return self.visit(ctx.expr())
        return None
    
    def visitExprStmt(self, ctx: HLangParser.ExprStmtContext):
        return ExprStmt(self.visit(ctx.expr()))

    def visitExpr(self, ctx: HLangParser.ExprContext):
        return self.visit(ctx.pipelineExpr())
    
    
    def visitPipelineExpr(self, ctx: HLangParser.PipelineExprContext):
        left = self.visit(ctx.logicOrExpr())
        tail = self.visit(ctx.pipelineExprTail())
        for _, expr in tail:
            left = BinaryOp(left, ">>", expr)
        return left

    def visitPipelineExprTail(self, ctx: HLangParser.PipelineExprTailContext):
        if not ctx.getChildCount():
            return []
        return [(">>", self.visit(ctx.logicOrExpr()))] + self.visit(ctx.pipelineExprTail())

    def visitLogicOrExpr(self, ctx: HLangParser.LogicOrExprContext):
        left = self.visit(ctx.logicAndExpr())
        tail = self.visit(ctx.logicOrExprTail())
        for _, expr in tail:
            left = BinaryOp(left, "||", expr)
        return left

    def visitLogicOrExprTail(self, ctx: HLangParser.LogicOrExprTailContext):
        if not ctx.getChildCount():
            return []
        return [("||", self.visit(ctx.logicAndExpr()))] + (self.visit(ctx.logicOrExprTail()) or [])
    
    def visitLogicAndExpr(self, ctx: HLangParser.LogicAndExprContext):
        left = self.visit(ctx.equalExpr())
        tail = self.visit(ctx.logicAndExprTail())
        for _, expr in tail:
            left = BinaryOp(left, "&&", expr)
        return left

    def visitLogicAndExprTail(self, ctx: HLangParser.LogicAndExprTailContext):
        if not ctx.getChildCount():
            return []
        tail = self.visit(ctx.logicAndExprTail()) or []
        return [("&&", self.visit(ctx.equalExpr()))] + tail
    
    def visitEqualExpr(self, ctx: HLangParser.EqualExprContext):
        left = self.visit(ctx.relExpr())
        tail = self.visit(ctx.equalExprTail())
        for op, expr in tail:
            left = BinaryOp(left, op, expr)
        return left

    def visitEqualExprTail(self, ctx: HLangParser.EqualExprTailContext):
        if not ctx.getChildCount():
            return []
        op = ctx.EQ().getText() if ctx.EQ() else ctx.NEQ().getText()
        expr = self.visit(ctx.relExpr())
        tail = self.visit(ctx.equalExprTail()) or []
        return [(op, expr)] + tail

    def visitRelExpr(self, ctx: HLangParser.RelExprContext):
        left = self.visit(ctx.addiExpr())
        tail = self.visit(ctx.relExprTail())
        for op, expr in tail:
            left = BinaryOp(left, op, expr)
        return left

    def visitRelExprTail(self, ctx: HLangParser.RelExprTailContext):
        if not ctx.getChildCount():
            return []
        op = ctx.getChild(0).getText()
        tail = self.visit(ctx.relExprTail()) or []
        return [(op, self.visit(ctx.addiExpr()))] + tail

    def visitAddiExpr(self, ctx: HLangParser.AddiExprContext):
        left = self.visit(ctx.multiExpr())
        tail = self.visit(ctx.addiExprTail())
        for op, expr in tail:
            left = BinaryOp(left, op, expr)
        return left

    def visitAddiExprTail(self, ctx: HLangParser.AddiExprTailContext):
        if not ctx.getChildCount():
            return []
        op = ctx.PLUS().getText() if ctx.PLUS() else ctx.MINUS().getText()
        return [(op, self.visit(ctx.multiExpr()))] + (self.visit(ctx.addiExprTail()) or [])

    def visitMultiExpr(self, ctx: HLangParser.MultiExprContext):
        left = self.visit(ctx.unaryExpr())
        tail = self.visit(ctx.multiExprTail())
        for op, expr in tail:
            left = BinaryOp(left, op, expr)
        return left

    def visitMultiExprTail(self, ctx: HLangParser.MultiExprTailContext):
        if not ctx.getChildCount():
            return []
        op = ctx.getChild(0).getText()
        return [(op, self.visit(ctx.unaryExpr()))] + (self.visit(ctx.multiExprTail()) or [])

    def visitUnaryExpr(self, ctx: HLangParser.UnaryExprContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.postfixExpr())
        else:
            op = ctx.getChild(0).getText()
            operand = self.visit(ctx.unaryExpr())
            return UnaryOp(op, operand)

    def visitPostfixExpr(self, ctx: HLangParser.PostfixExprContext):
        expr = self.visit(ctx.primaryExpr())
        ops = self.visit(ctx.postfixExprTail())
        return self.foldPostfix(expr, ops)

    def visitPostfixExprTail(self, ctx: HLangParser.PostfixExprTailContext):
        if not ctx.getChildCount():
            return []
        postfix_op = self.visit(ctx.postfixOp())
        tail = self.visit(ctx.postfixExprTail()) or []
        return [postfix_op] + tail

    def visitPostfixOp(self, ctx: HLangParser.PostfixOpContext):
        if ctx.LBRACK():
            return ("[]", self.visit(ctx.expr()))
        elif ctx.LPAREN():
            args = self.visit(ctx.argsOpt())
            return ("()", args)
    
    def visitArgsOpt(self, ctx: HLangParser.ArgsOptContext):
        if not ctx.getChildCount():
            return []
        return [self.visit(ctx.expr())] + self.visit(ctx.argTail())

    def visitArgTail(self, ctx: HLangParser.ArgTailContext):
        if not ctx.getChildCount():
            return []
        expr = self.visit(ctx.expr())
        tail = self.visit(ctx.argTail()) or []
        return [expr] + tail

    def foldPostfix(self, base, ops):
        for kind, val in ops:
            if kind == "[]":
                base = ArrayAccess(base, val)
            elif kind == "()":
                base = FunctionCall(base, val)
        return base
    
    def visitPrimaryExpr(self, ctx: HLangParser.PrimaryExprContext):
        if ctx.literal():
            return self.visit(ctx.literal())
        if ctx.ID():
            return Identifier(ctx.ID().getText())
        if ctx.expr():
            return self.visit(ctx.expr())
        if ctx.LBRACK():
            return ArrayLiteral(self.visit(ctx.exprOpt()))
    
    def visitExprOpt(self, ctx: HLangParser.ExprOptContext):
        if not ctx.getChildCount():
            return []
        return [self.visit(ctx.expr())] + self.visit(ctx.exprTail())

    def visitExprTail(self, ctx: HLangParser.ExprTailContext):
        if not ctx.getChildCount(): return []
        expr = self.visit(ctx.expr())
        tail = self.visit(ctx.exprTail()) or []
        return [expr] + tail
    
    def visitLiteral(self, ctx: HLangParser.LiteralContext):
        if ctx.INT_LIT():
            return IntegerLiteral(int(ctx.INT_LIT().getText()))
        if ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        if ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())
        if ctx.TRUE():
            return BooleanLiteral(True)
        if ctx.FALSE():
            return BooleanLiteral(False)
        if ctx.arrayLiteral():
            return self.visit(ctx.arrayLiteral())

    def visitArrayLiteral(self, ctx: HLangParser.ArrayLiteralContext):
        exprs = self.visit(ctx.exprOpt())
        return ArrayLiteral(exprs if exprs is not None else [])
    
    def visitLvalue(self, ctx: HLangParser.LvalueContext):
        name = ctx.ID().getText()
        indices = self.visit(ctx.indexTail())
        if not indices:
            return IdLValue(name)
        result = Identifier(name)
        for index in indices:
            result = ArrayAccess(result, index)
        return result
    
    def visitIndexTail(self, ctx: HLangParser.IndexTailContext):
        if not ctx.getChildCount():
            return []
        index = self.visit(ctx.expr())
        tail = self.visit(ctx.indexTail()) or []
        return [index] + tail
