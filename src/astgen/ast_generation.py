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
    pass

    def visitProgram(self, ctx: HLangParser.ProgramContext):
        return Program(self.visit(ctx.decllist()))
    
    def visitDecllist(self, ctx: HLangParser.DecllistContext):
        decl = self.visit(ctx.decl())
        tail = self.visit(ctx.decllistTail())
        return [decl] + tail
    
    def visitDecllistTail(self, ctx: HLangParser.DecllistTailContext):
        if ctx.getChildCount() == 0:
            return []
        return [self.visit(ctx.decl())] + self.visit(ctx.decllistTail())
    
    def visitDecl(self, ctx: HLangParser.DeclContext):
        return self.visit(ctx.getChild(0))

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
    
    def visitTypeSpec(self, ctx: HLangParser.TypeSpecContext):
        return self.visit(ctx.getChild(0))
    
    def visitDataType(self, ctx: HLangParser.DataTypeContext):
        kw = ctx.getChild(0).getText()
        if kw == "int": return IntType()
        if kw == "float": return FloatType()
        if kw == "bool": return BoolType()
        if kw == "string": return StringType()
        if kw == "void": return VoidType()
        
    def visitArrayType(self, ctx: HLangParser.ArrayTypeContext):
        elementType = self.visit(ctx.typeSpec())
        size = int(ctx.INT_LIT().getText())
        return ArrayType(elementType, size)

    def visitFuncdecl(self, ctx: HLangParser.FuncdeclContext):
        name = ctx.ID().getText()
        params = self.visit(ctx.paramOpt())
        returnType = self.visit(ctx.typeSpec())
        body = self.visit(ctx.blockStmt())
        return FuncDecl(name, params, returnType, body.stmts)
    
    def visitParamOpt(self, ctx: HLangParser.ParamOptContext):
        if ctx.getChildCount() == 0:
            return []
        return self.visit(ctx.paramList())
