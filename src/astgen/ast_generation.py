"""
AST Generation module for HLang programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from functools import reduce
from build.HLangVisitor import HLangVisitor
from build.HLangParser import HLangParser
from src.utils.nodes import *

class ASTGeneration(HLangVisitor):
    def visitProgram(self, ctx: HLangParser.ProgramContext):
        consts = [self.visit(decl) for decl in ctx.constdecl()]
        funcs = [self.visit(decl) for decl in ctx.funcdecl()]
        return Program(consts, funcs)
    
    def visitConstdecl(self, ctx: HLangParser.ConstdeclContext):
        name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        constTyp = self.visit(ctx.varType()) if ctx.varType() else None
        return ConstDecl(name, constTyp, value)
    
    def visitVardecl(self, ctx: HLangParser.VardeclContext):
        name = ctx.ID().getText()
        varTyp = self.visit(ctx.varType()) if ctx.varType() else None
        value = self.visit(ctx.expr())
        return VarDecl(name, varTyp, value)
    
    def visitFuncdecl(self, ctx: HLangParser.FuncdeclContext):
        name = ctx.ID().getText()
        params = self.visit(ctx.paramdecl())
        returnType = self.visit(ctx.returnType())
        body = self.visit(ctx.body())
        bodyStmt = body.statements
        return FuncDecl(name, params, returnType, bodyStmt)
    
    def visitParamdecl(self, ctx: HLangParser.ParamdeclContext):
        if ctx.paramList():
            return self.visit(ctx.paramList())
        return []
    
    def visitParamList(self, ctx: HLangParser.ParamListContext):
        param = [self.visit(ctx.param())]
        tail = self.visit(ctx.paramListTail())
        return param + tail
    
    def visitParamListTail(self, ctx: HLangParser.ParamListTailContext):
        if ctx.getChildCount() == 0:
            return []
        param = self.visit(ctx.param())
        tail = self.visit(ctx.paramListTail())
        return [param] + tail
    
    def visitParam(self, ctx: HLangParser.ParamContext):
        name = ctx.ID().getText()
        typ = self.visit(ctx.varType())
        return Param(name, typ)
    
    def visitVarType(self, ctx: HLangParser.VarTypeContext):
        return self.visit(ctx.nvoidType())
    
    def visitReturnType(self, ctx: HLangParser.ReturnTypeContext):
        if ctx.VOID():
            return VoidType()
        return self.visit(ctx.nvoidType())
    
    def visitNvoidType(self, ctx: HLangParser.NvoidTypeContext):
        if ctx.INT():
            return IntType()
        if ctx.FLOAT():
            return FloatType()
        if ctx.BOOL():
            return BoolType()
        if ctx.STRING():
            return StringType()
        return self.visit(ctx.arrayType())
    
    def visitArrayType(self, ctx: HLangParser.ArrayTypeContext):
        size = int(ctx.INT_LIT().getText())
        elementType = self.visit(ctx.nvoidType())
        return ArrayType(elementType, size)
    
    def visitBody(self, ctx: HLangParser.BodyContext):
        stmts = []
        for stmt in ctx.stmt():
            visit = self.visit(stmt)
            if visit is not None:
                stmts.append(visit)
        return BlockStmt(stmts)
    
    #* STATEMENTS =================================================
    
    def visitStmt(self, ctx: HLangParser.StmtContext):
        if ctx.vardecl():
            return self.visit(ctx.vardecl())
        
        if ctx.assignStmt():
            return self.visit(ctx.assignStmt())
        
        if ctx.callStmt():
            return self.visit(ctx.callStmt())
        
        if ctx.returnStmt():
            return self.visit(ctx.returnStmt())
        
        if ctx.ifStmt():
            return self.visit(ctx.ifStmt())
        
        if ctx.whileStmt():
            return self.visit(ctx.whileStmt())
        
        if ctx.forStmt():
            return self.visit(ctx.forStmt())
        
        if ctx.breakStmt():
            return self.visit(ctx.breakStmt())
        
        if ctx.continueStmt():
            return self.visit(ctx.continueStmt())
        
        if ctx.exprStmt():
            return self.visit(ctx.exprStmt())
        
        if ctx.blockStmt():
            return self.visit(ctx.blockStmt())
        
        return None

    def visitAssignStmt(self, ctx: HLangParser.AssignStmtContext):
        lhs = self.visit(ctx.lvalue()) # Handle left-side operands
        rhs = self.visit(ctx.expr()) # Handle right-side operands
        return Assignment(lhs, rhs)
    
    def visitLvalue(self, ctx: HLangParser.LvalueContext):
        name = ctx.ID().getText()
        indices = self.visit(ctx.lvalueTail())
        if not indices:
            return IdLValue(name)
        base = Identifier(name)
        for idx in indices[:-1]:
            base = ArrayAccess(base, idx)
        return ArrayAccessLValue(base, indices[-1])
    
    def visitLvalueTail(self, ctx: HLangParser.LvalueTailContext):
        if ctx.getChildCount() == 0:
            return []
        idx = self.visit(ctx.expr())
        tail = self.visit(ctx.lvalueTail())
        return [idx] + tail
    
    #* CONDITION AND LOOPS ========================================
    def visitIfStmt(self, ctx: HLangParser.IfStmtContext):
        cond = self.visit(ctx.expr())
        thenStmt = self.visit(ctx.body())
        elseStmt = self.visit(ctx.elseStmt()) if ctx.elseStmt() else None
        if isinstance(elseStmt, IfStmt):
            elifs = [(elseStmt.condition, elseStmt.then_stmt)] + elseStmt.elif_branches
            return IfStmt(cond, thenStmt, elifs, elseStmt.else_stmt)
        return IfStmt(cond, thenStmt, [], elseStmt)

    def visitElseStmt(self, ctx: HLangParser.ElseStmtContext):
        if ctx.ifStmt():
            return self.visit(ctx.ifStmt())
        return self.visit(ctx.body())
    
    def visitWhileStmt(self, ctx: HLangParser.WhileStmtContext):
        cond = self.visit(ctx.expr())
        body = self.visit(ctx.body())
        return WhileStmt(cond, body)
    
    def visitForStmt(self, ctx: HLangParser.ForStmtContext):
        name = ctx.ID().getText()
        ite = self.visit(ctx.expr())
        body = self.visit(ctx.body())
        return ForStmt(name, ite, body)

    def visitCallStmt(self, ctx: HLangParser.CallStmtContext):
        return ExprStmt(self.visit(ctx.callExpr()))

    def visitBreakStmt(self, ctx: HLangParser.BreakStmtContext):
        return BreakStmt()
    
    def visitContinueStmt(self, ctx: HLangParser.ContinueStmtContext):
        return ContinueStmt()
    
    def visitReturnStmt(self, ctx):
        if ctx.expr():
            return ReturnStmt(self.visit(ctx.expr()))
        return ReturnStmt(None)

    def visitExprStmt(self, ctx: HLangParser.ExprStmtContext):
        return ExprStmt(self.visit(ctx.expr()))

    def visitBlockStmt(self, ctx: HLangParser.BlockStmtContext):
        stmts = []
        for stmtContext in ctx.stmt():
            stmt = self.visit(stmtContext)
            if stmt is not None:
                stmts.append(stmt)
        return BlockStmt(stmts)
    
    #* EXPR ========================================================

    def visitExpr(self, ctx: HLangParser.ExprContext):
        return self.visit(ctx.expr1())

    def visitExpr1(self, ctx: HLangParser.Expr1Context):
        return self.visit(ctx.expr2())

    def visitExpr2(self, ctx: HLangParser.Expr2Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr3())
        
        operands = []
        cur = ctx
        while isinstance(cur, HLangParser.Expr2Context) and cur.PIPE():
            operands.append(self.visit(cur.expr3()))
            cur = cur.expr2()
        
        operands.append(self.visit(cur.expr3()))
        operands = list(reversed(operands))
        res = operands[0]
        for op in operands[1:]:
            res = BinaryOp(res, ">>", op)
        return res
            

    def visitExpr3(self, ctx: HLangParser.Expr3Context):
        if ctx.OR():
            left = self.visit(ctx.expr3())
            right = self.visit(ctx.expr4())
            return BinaryOp(left, "||", right)
        
        return self.visit(ctx.expr4())

    def visitExpr4(self, ctx: HLangParser.Expr4Context):
        if ctx.AND():
            l = self.visit(ctx.expr4())
            r = self.visit(ctx.expr5())
            return BinaryOp(l, "&&", r)
        
        return self.visit(ctx.expr5())
    
    def visitExpr5(self, ctx: HLangParser.Expr5Context):
        if ctx.EQ():
            l = self.visit(ctx.expr5())
            r = self.visit(ctx.expr6())
            return BinaryOp(l, "==", r)
        
        elif ctx.NEQ():
            l = self.visit(ctx.expr5())
            r = self.visit(ctx.expr6())
            return BinaryOp(l, "!=", r)
        
        return self.visit(ctx.expr6())

    def visitExpr6(self, ctx: HLangParser.Expr6Context):
        if ctx.LT():
            l = self.visit(ctx.expr6())
            r = self.visit(ctx.expr7())
            return BinaryOp(l, "<", r)
        
        elif ctx.LE():
            l = self.visit(ctx.expr6())
            r = self.visit(ctx.expr7())
            return BinaryOp(l, "<=", r)

        elif ctx.GT():
            l = self.visit(ctx.expr6())
            r = self.visit(ctx.expr7())
            return BinaryOp(l, ">", r)
        
        elif ctx.GE():
            l = self.visit(ctx.expr6())
            r = self.visit(ctx.expr7())
            return BinaryOp(l, ">=", r)

        return self.visit(ctx.expr7())

    def visitExpr7(self, ctx: HLangParser.Expr7Context):
        if ctx.PLUS():
            l = self.visit(ctx.expr7())
            r = self.visit(ctx.expr8())
            return BinaryOp(l, "+", r)
        
        elif ctx.MINUS():
            l = self.visit(ctx.expr7())
            r = self.visit(ctx.expr8())
            return BinaryOp(l, "-", r)
        return self.visit(ctx.expr8())
    
    def visitExpr8(self, ctx: HLangParser.Expr8Context):
        if ctx.MUL():
            l = self.visit(ctx.expr8())
            r = self.visit(ctx.expr9())
            return BinaryOp(l, "*", r)
        
        elif ctx.DIV():
            l = self.visit(ctx.expr8())
            r = self.visit(ctx.expr9())
            return BinaryOp(l, "/", r)
        
        elif ctx.MOD():
            l = self.visit(ctx.expr8())
            r = self.visit(ctx.expr9())
            return BinaryOp(l, "%", r)
        return self.visit(ctx.expr9())
    
    def visitExpr9(self, ctx: HLangParser.Expr9Context):
        if ctx.PLUS():
            return UnaryOp("+", self.visit(ctx.expr9()))
        elif ctx.MINUS():
            return UnaryOp("-", self.visit(ctx.expr9()))
        elif ctx.NOT():
            return UnaryOp("!", self.visit(ctx.expr9()))
        
        primary = self.visit(ctx.primaryExpr())
        # Check for ID values:
        if isinstance(primary, IdLValue):
            primary = Identifier(primary.name)
        
        indices = self.visit(ctx.expr9_tail())
        if not indices:
            return primary

        return reduce(lambda acc, cur: ArrayAccess(acc, cur), indices, primary)
        
    
    def visitExpr9_tail(self, ctx: HLangParser.Expr9_tailContext):
        if ctx.getChildCount() == 0:
            return []
        index = self.visit(ctx.expr())
        opt = self.visit(ctx.expr9_tail())
        return [index] + opt
    
    def visitPrimaryExpr(self, ctx: HLangParser.PrimaryExprContext):
        if ctx.INT_LIT():
            return IntegerLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.TRUE():
            return BooleanLiteral(True)
        elif ctx.FALSE():
            return BooleanLiteral(False)
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())
        elif ctx.arrayLiteral():
            return self.visit(ctx.arrayLiteral())
        elif ctx.callExpr():
            return self.visit(ctx.callExpr())
        elif ctx.typeConversionCall():
            return self.visit(ctx.typeConversionCall())
        elif ctx.ID():
            return Identifier(ctx.ID().getText())
        elif ctx.expr():
            return self.visit(ctx.expr())
        return None
#* CALL==========================================================
    def visitTypeConversionCall(self, ctx: HLangParser.TypeConversionCallContext):
        function_name = ""
        if ctx.INT():
            function_name = "int"
        elif ctx.FLOAT():
            function_name = "float"
        elif ctx.STR():
            function_name = "str"

        args = self.visit(ctx.exprListOpt())
        return FunctionCall(Identifier(function_name), args)

    def visitCallExpr(self, ctx: HLangParser.CallExprContext):
        args = self.visit(ctx.exprListOpt())
        name = ctx.ID().getText()
        return FunctionCall(Identifier(name), args)
    
    def visitArrayLiteral(self, ctx: HLangParser.ArrayLiteralContext):
        return ArrayLiteral(self.visit(ctx.exprListOpt()))

    def visitExprListOpt(self, ctx: HLangParser.ExprListOptContext):
        if ctx.getChildCount() == 0:
            return []
        return self.visit(ctx.exprList())
    
    def visitExprList(self, ctx: HLangParser.ExprListContext):
        return [self.visit(ctx.expr())] + self.visit(ctx.exprListTail())
    
    def visitExprListTail(self, ctx: HLangParser.ExprListTailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.expr())] + self.visit(ctx.exprListTail())