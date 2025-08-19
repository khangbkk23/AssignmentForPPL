from src.utils.nodes import *
from utils import CodeGenerator

def test_001():
    ast = Program(
        [], 
        [FuncDecl("main", [], VoidType(), [ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Hello World")]))])]
    )
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_002():
    ast = Program(
        [], 
        [FuncDecl("main", [], VoidType(), [ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(42)]))])]
    )
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_003():
    ast = Program(
        [], 
        [FuncDecl("main", [], VoidType(), [ExprStmt(FunctionCall(Identifier("print"), [FloatLiteral(3.14)]))])]
    )
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_004():
    ast = Program(
        [], 
        [FuncDecl("main", [], VoidType(), [ExprStmt(FunctionCall(Identifier("print"), [BooleanLiteral(True)]))])]
    )
    expected = "True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_005():
    ast = Program(
        [], 
        [FuncDecl("main", [], VoidType(), [ExprStmt(FunctionCall(Identifier("print"), [BooleanLiteral(False)]))])]
    )
    expected = "False"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_006():
    ast = Program(
        [], 
        [FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(10)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ])]
    )
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_007():
    ast = Program(
        [], 
        [FuncDecl("main", [], VoidType(), [
            VarDecl("x", FloatType(), FloatLiteral(2.5)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ])]
    )
    expected = "2.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_008():
    ast = Program(
        [], 
        [FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(IntegerLiteral(3), '+', IntegerLiteral(7))]))
        ])]
    )
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_009():
    ast = Program(
        [], 
        [FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(FloatLiteral(1.5), '*', FloatLiteral(2))]))
        ])]
    )
    expected = "3.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_010():
    ast = Program(
        [], 
        [FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(IntegerLiteral(7), '-', IntegerLiteral(2))]))
        ])]
    )
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_011():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(5)),
        VarDecl("y", IntType(), IntegerLiteral(3)),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("x"), '+', Identifier("y"))]))
    ])])
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_012():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("a", FloatType(), FloatLiteral(2.0)),
        VarDecl("b", IntType(), IntegerLiteral(3)),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("a"), '*', Identifier("b"))]))
    ])])
    expected = "6.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_013():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(10)),
        ExprStmt(FunctionCall(Identifier("print"), [UnaryOp("-", Identifier("x"))]))
    ])])
    expected = "-10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_014():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", BoolType(), BooleanLiteral(True)),
        ExprStmt(FunctionCall(Identifier("print"), [UnaryOp("!", Identifier("x"))]))
    ])])
    expected = "False"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_015():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        IfStmt(
            BinaryOp(IntegerLiteral(3), '>', IntegerLiteral(1)),
            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Yes")])),
            else_stmt=ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("No")]))
        )
    ])])
    expected = "Yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_016():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(0)),
        WhileStmt(
            BinaryOp(Identifier("x"), '<', IntegerLiteral(3)),
            BlockStmt([
                ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")])),
                Assignment(IdLValue("x"), BinaryOp(Identifier("x"), '+', IntegerLiteral(1)))
            ])
        )
    ])])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_017():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ForStmt("i", ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]),
                BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")]))]))
    ])])
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_018():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(5), IntegerLiteral(6), IntegerLiteral(7)])),
        ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(1))]))
    ])])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_019():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(2)),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("x"), '>>', IntegerLiteral(1))]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_020():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("foo", [Param("a", IntType())], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("a")]))
        ]),
        ExprStmt(FunctionCall(Identifier("foo"), [IntegerLiteral(99)]))
    ])])
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_021():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("foo", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Hi")]))
        ]),
        ExprStmt(FunctionCall(Identifier("foo"), []))
    ])])
    expected = "Hi"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_022():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("sum", [Param("x", IntType()), Param("y", IntType())], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("x"), '+', Identifier("y"))]))
        ]),
        ExprStmt(FunctionCall(Identifier("sum"), [IntegerLiteral(5), IntegerLiteral(7)]))
    ])])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_023():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("neg", [Param("a", IntType())], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [UnaryOp("-", Identifier("a"))]))
        ]),
        ExprStmt(FunctionCall(Identifier("neg"), [IntegerLiteral(42)]))
    ])])
    expected = "-42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_024():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("boolPrint", [Param("b", BoolType())], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [UnaryOp("!", Identifier("b"))]))
        ]),
        ExprStmt(FunctionCall(Identifier("boolPrint"), [BooleanLiteral(False)]))
    ])])
    expected = "True"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_025():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("maxVal", [Param("x", IntType()), Param("y", IntType())], IntType(), [
            IfStmt(
                BinaryOp(Identifier("x"), '>', Identifier("y")),
                ReturnStmt(Identifier("x")),
                else_stmt=ReturnStmt(Identifier("y"))
            )
        ]),
        VarDecl("res", IntType(), FunctionCall(Identifier("maxVal"), [IntegerLiteral(10), IntegerLiteral(20)])),
        ExprStmt(FunctionCall(Identifier("print"), [Identifier("res")]))
    ])])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_026():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("identity", [Param("x", IntType())], IntType(), [
            ReturnStmt(Identifier("x"))
        ]),
        ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("identity"), [IntegerLiteral(99)])]))
    ])])
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_027():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("double", [Param("a", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("a"), '*', IntegerLiteral(2)))
        ]),
        ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("double"), [IntegerLiteral(21)])]))
    ])])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_028():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("sumArray", [Param("arr", ArrayType(IntType(), 3))], IntType(), [
            VarDecl("total", IntType(), IntegerLiteral(0)),
            ForStmt("i", Identifier("arr"), BlockStmt([
                Assignment(IdLValue("total"), BinaryOp(Identifier("total"), '+', Identifier("i")))
            ])),
            ReturnStmt(Identifier("total"))
        ]),
        ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("sumArray"), [ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])])]))
    ])])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_029():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("printBool", [Param("b", BoolType())], VoidType(), [
            IfStmt(Identifier("b"), ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Yes")])), else_stmt=ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("No")])))
        ]),
        ExprStmt(FunctionCall(Identifier("printBool"), [BooleanLiteral(True)]))
    ])])
    expected = "Yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_030():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("inc", [Param("x", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("x"), '+', IntegerLiteral(1)))
        ]),
        VarDecl("y", IntType(), FunctionCall(Identifier("inc"), [IntegerLiteral(5)])),
        ExprStmt(FunctionCall(Identifier("print"), [Identifier("y")]))
    ])])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
    
def test_031():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
        ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(0))]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_032():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(4), IntegerLiteral(5), IntegerLiteral(6)])),
        ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(2))]))
    ])])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_033():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(7), IntegerLiteral(8), IntegerLiteral(9)])),
        Assignment(ArrayAccessLValue(Identifier("arr"), IntegerLiteral(1)), IntegerLiteral(42)),
        ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(1))]))
    ])])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_034():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
        ForStmt("i", Identifier("arr"), BlockStmt([
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")]))
        ]))
    ])])
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_035():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(2), IntegerLiteral(4), IntegerLiteral(6)])),
        VarDecl("sum", IntType(), IntegerLiteral(0)),
        ForStmt("i", Identifier("arr"), BlockStmt([
            Assignment(IdLValue("sum"), BinaryOp(Identifier("sum"), '+', Identifier("i")))
        ])),
        ExprStmt(FunctionCall(Identifier("print"), [Identifier("sum")]))
    ])])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_036():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(6), IntegerLiteral(9)])),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(ArrayAccess(Identifier("arr"), IntegerLiteral(0)), '+', ArrayAccess(Identifier("arr"), IntegerLiteral(2)))]))
    ])])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_037():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 2), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])),
        VarDecl("arr2", ArrayType(IntType(), 2), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(ArrayAccess(Identifier("arr"), IntegerLiteral(1)), '+', ArrayAccess(Identifier("arr2"), IntegerLiteral(0)))]))
    ])])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_038():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("matrix", ArrayType(ArrayType(IntType(), 2), 2), ArrayLiteral([
            ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]),
            ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])
        ])),
        ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(ArrayAccess(Identifier("matrix"), IntegerLiteral(1)), IntegerLiteral(0))]))
    ])])
    expected = "3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_039():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(ArrayAccess(Identifier("arr"), IntegerLiteral(0)), '+', BinaryOp(ArrayAccess(Identifier("arr"), IntegerLiteral(1)), '+', ArrayAccess(Identifier("arr"), IntegerLiteral(2))))]))
    ])])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_040():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
        ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(0))])),
        ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(1))])),
        ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(2))]))
    ])])
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
 
def test_041():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(0)),
        WhileStmt(BinaryOp(Identifier("x"), '<', IntegerLiteral(3)), BlockStmt([
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")])),
            Assignment(IdLValue("x"), BinaryOp(Identifier("x"), '+', IntegerLiteral(1)))
        ]))
    ])])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_042():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ForStmt("i", ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), BlockStmt([
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")]))
        ]))
    ])])
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_043():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("i", IntType(), IntegerLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"), '<', IntegerLiteral(3)), BlockStmt([
            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), '+', IntegerLiteral(1))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")]))
        ]))
    ])])
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_044():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        IfStmt(BooleanLiteral(True), ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Yes")])), else_stmt=ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("No")])))
    ])])
    expected = "Yes"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_045():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        IfStmt(BooleanLiteral(False), ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Yes")])), else_stmt=ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("No")])))
    ])])
    expected = "No"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_046():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(5)),
        IfStmt(BinaryOp(Identifier("x"), '>', IntegerLiteral(3)), ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Big")])), else_stmt=ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Small")])))
    ])])
    expected = "Big"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_047():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(1)),
        IfStmt(BinaryOp(Identifier("x"), '>', IntegerLiteral(3)), ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Big")])), else_stmt=ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Small")])))
    ])])
    expected = "Small"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_048():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(0)),
        WhileStmt(BinaryOp(Identifier("x"), '<', IntegerLiteral(5)), BlockStmt([
            Assignment(IdLValue("x"), BinaryOp(Identifier("x"), '+', IntegerLiteral(1))),
            IfStmt(BinaryOp(Identifier("x"), '==', IntegerLiteral(3)), ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Three")]))),
        ]))
    ])])
    expected = "Three"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_049():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ForStmt("i", ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), BlockStmt([
            IfStmt(BinaryOp(Identifier("i"), '==', IntegerLiteral(2)), ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Two")])))
        ]))
    ])])
    expected = "Two"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_050():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("i", IntType(), IntegerLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"), '<', IntegerLiteral(3)), BlockStmt([
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")])),
            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), '+', IntegerLiteral(1))),
            ContinueStmt(),
        ]))
    ])])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_051():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(IntegerLiteral(2), '+', IntegerLiteral(3))]))
    ])])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_052():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(IntegerLiteral(10), '-', IntegerLiteral(4))]))
    ])])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_053():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(IntegerLiteral(3), '*', IntegerLiteral(4))]))
    ])])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_054():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(IntegerLiteral(10), '/', IntegerLiteral(2))]))
    ])])
    expected = "5.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_055():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(IntegerLiteral(10), '%', IntegerLiteral(3))]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_056():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(IntegerLiteral(8), '>>', IntegerLiteral(2))]))
    ])])
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_057():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [UnaryOp('-', IntegerLiteral(5))]))
    ])])
    expected = "-5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_058():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [UnaryOp('!', BooleanLiteral(True))]))
    ])])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_059():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(5)),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("x"), '==', IntegerLiteral(5))]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_060():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(5)),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("x"), '!=', IntegerLiteral(5))]))
    ])])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_061():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(BooleanLiteral(True), '&&', BooleanLiteral(False))]))
    ])])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_062():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(BooleanLiteral(True), '||', BooleanLiteral(False))]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_063():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(BinaryOp(IntegerLiteral(2), '+', IntegerLiteral(3)), '*', IntegerLiteral(4))]))
    ])])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_064():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("a", IntType(), IntegerLiteral(5)),
        VarDecl("b", IntType(), IntegerLiteral(10)),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(BinaryOp(Identifier("a"), '<', Identifier("b")), '&&', BinaryOp(Identifier("b"), '>', Identifier("a")))]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_065():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", BoolType(), BooleanLiteral(True)),
        VarDecl("y", BoolType(), BooleanLiteral(False)),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("x"), '||', Identifier("y"))]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_066():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", BoolType(), BooleanLiteral(True)),
        VarDecl("y", BoolType(), BooleanLiteral(False)),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("x"), '&&', Identifier("y"))]))
    ])])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_067():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(BinaryOp(BooleanLiteral(True), '&&', BooleanLiteral(True)), '||', BooleanLiteral(False))]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_068():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(UnaryOp('!', BooleanLiteral(False)), '&&', BooleanLiteral(True))]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_069():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(UnaryOp('!', BooleanLiteral(True)), '||', BooleanLiteral(True))]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_070():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(BinaryOp(IntegerLiteral(1), '+', IntegerLiteral(2)), '*', BinaryOp(IntegerLiteral(3), '+', IntegerLiteral(4)))]))
    ])])
    expected = "21"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_071():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("add", [Param("a", IntType()), Param("b", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
        ]),
        ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("add"), [IntegerLiteral(3), IntegerLiteral(4)])]))
    ])])
    expected = "7"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_072():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        FuncDecl("negate", [Param("x", IntType())], IntType(), [
            ReturnStmt(UnaryOp('-', Identifier("x")))
        ]),
        ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("negate"), [IntegerLiteral(5)])]))
    ])])
    expected = "-5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_073():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(5)),
        ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
    ])])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_074():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        BlockStmt([VarDecl("x", IntType(), IntegerLiteral(10)), ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))])
    ])])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_075():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(5)),
        BlockStmt([VarDecl("y", IntType(), IntegerLiteral(10)), ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("x"), "+", Identifier("y"))]))])
    ])])
    expected = "15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_076():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        BlockStmt([VarDecl("x", IntType(), IntegerLiteral(2)), BlockStmt([VarDecl("y", IntType(), IntegerLiteral(3)), ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("x"), "*", Identifier("y"))]))])])
    ])])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_077():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("a", BoolType(), BooleanLiteral(True)),
        VarDecl("b", BoolType(), BooleanLiteral(False)),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("a"), '&&', Identifier("b"))]))
    ])])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_078():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("a", BoolType(), BooleanLiteral(True)),
        VarDecl("b", BoolType(), BooleanLiteral(False)),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("a"), '||', Identifier("b"))]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_079():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(2)),
        VarDecl("y", IntType(), IntegerLiteral(3)),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(BinaryOp(Identifier("x"), '+', Identifier("y")), '*', IntegerLiteral(2))]))
    ])])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_080():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", IntType(), IntegerLiteral(5)),
        VarDecl("y", IntType(), IntegerLiteral(10)),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(BinaryOp(Identifier("x"), '*', IntegerLiteral(2)), '+', Identifier("y"))]))
    ])])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_081():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
        ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(0))]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_082():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
        ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(2))]))
    ])])
    expected = "3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_083():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
        Assignment(ArrayAccessLValue(Identifier("arr"), IntegerLiteral(1)), IntegerLiteral(10)),
        ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(1))]))
    ])])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_084():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 2), ArrayLiteral([IntegerLiteral(5), IntegerLiteral(6)])),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(ArrayAccess(Identifier("arr"), IntegerLiteral(0)), '+', ArrayAccess(Identifier("arr"), IntegerLiteral(1)))]))
    ])])
    expected = "11"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_085():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(ArrayAccess(Identifier("x"), IntegerLiteral(0)), '*', IntegerLiteral(2))]))
    ])])
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_086():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("x", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(ArrayAccess(Identifier("x"), IntegerLiteral(1)), '+', ArrayAccess(Identifier("x"), IntegerLiteral(2)))]))
    ])])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_087():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 4), ArrayLiteral([IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)])),
        Assignment(ArrayAccessLValue(Identifier("arr"), IntegerLiteral(2)), BinaryOp(ArrayAccess(Identifier("arr"), IntegerLiteral(0)), '+', IntegerLiteral(10))),
        ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(2))]))
    ])])
    expected = "12"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_088():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(ArrayAccess(Identifier("arr"), IntegerLiteral(0)), '+', BinaryOp(ArrayAccess(Identifier("arr"), IntegerLiteral(1)), '*', ArrayAccess(Identifier("arr"), IntegerLiteral(2))))]))
    ])])
    expected = "7"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_089():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 3), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
        ExprStmt(FunctionCall(Identifier("print"), [UnaryOp('-', ArrayAccess(Identifier("arr"), IntegerLiteral(1)))]))
    ])])
    expected = "-2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_090():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("arr", ArrayType(IntType(), 2), ArrayLiteral([IntegerLiteral(5), IntegerLiteral(10)])),
        ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(UnaryOp('-', ArrayAccess(Identifier("arr"), IntegerLiteral(0))), '+', ArrayAccess(Identifier("arr"), IntegerLiteral(1)))]))
    ])])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_091():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ForStmt("i", ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), BlockStmt([
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")]))
        ]))
    ])])
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_092():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("sum", IntType(), IntegerLiteral(0)),
        ForStmt("i", ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), BlockStmt([
            Assignment(IdLValue("sum"), BinaryOp(Identifier("sum"), '+', Identifier("i")))
        ])),
        ExprStmt(FunctionCall(Identifier("print"), [Identifier("sum")]))
    ])])
    expected = "6"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_093():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("i", IntType(), IntegerLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"), '<', IntegerLiteral(3)), BlockStmt([
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")])),
            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), '+', IntegerLiteral(1)))
        ]))
    ])])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_094():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("i", IntType(), IntegerLiteral(0)),
        VarDecl("sum", IntType(), IntegerLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"), '<', IntegerLiteral(5)), BlockStmt([
            Assignment(IdLValue("sum"), BinaryOp(Identifier("sum"), '+', Identifier("i"))),
            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), '+', IntegerLiteral(1)))
        ])),
        ExprStmt(FunctionCall(Identifier("print"), [Identifier("sum")]))
    ])])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_095():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ForStmt("i", ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), BlockStmt([
            IfStmt(BinaryOp(Identifier("i"), '==', IntegerLiteral(2)), BlockStmt([
                ContinueStmt()
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")]))
        ]))
    ])])
    expected = "13"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_096():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        ForStmt("i", ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), BlockStmt([
            IfStmt(BinaryOp(Identifier("i"), '==', IntegerLiteral(2)), BlockStmt([
                BreakStmt()
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")]))
        ]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_097():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("sum", IntType(), IntegerLiteral(0)),
        ForStmt("i", ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4)]), BlockStmt([
            IfStmt(BinaryOp(Identifier("i"), '==', IntegerLiteral(3)), BlockStmt([ContinueStmt()])),
            Assignment(IdLValue("sum"), BinaryOp(Identifier("sum"), '+', Identifier("i")))
        ])),
        ExprStmt(FunctionCall(Identifier("print"), [Identifier("sum")]))
    ])])
    expected = "7"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_098():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("i", IntType(), IntegerLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"), '<', IntegerLiteral(5)), BlockStmt([
            IfStmt(BinaryOp(Identifier("i"), '==', IntegerLiteral(3)), BlockStmt([BreakStmt()])),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")])),
            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), '+', IntegerLiteral(1)))
        ]))
    ])])
    expected = "012"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_099():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("i", IntType(), IntegerLiteral(0)),
        WhileStmt(BinaryOp(Identifier("i"), '<', IntegerLiteral(5)), BlockStmt([
            IfStmt(BinaryOp(Identifier("i"), '==', IntegerLiteral(2)), BlockStmt([ContinueStmt()])),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")])),
            Assignment(IdLValue("i"), BinaryOp(Identifier("i"), '+', IntegerLiteral(1)))
        ]))
    ])])
    expected = "0134"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_100():
    ast = Program([], [FuncDecl("main", [], VoidType(), [
        VarDecl("sum", IntType(), IntegerLiteral(0)),
        ForStmt("i", ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4)]), BlockStmt([
            IfStmt(BinaryOp(Identifier("i"), '==', IntegerLiteral(2)), BlockStmt([ContinueStmt()])),
            IfStmt(BinaryOp(Identifier("i"), '==', IntegerLiteral(3)), BlockStmt([BreakStmt()])),
            Assignment(IdLValue("sum"), BinaryOp(Identifier("sum"), '+', Identifier("i")))
        ])),
        ExprStmt(FunctionCall(Identifier("print"), [Identifier("sum")]))
    ])])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
