from src.utils.nodes import *
from utils import CodeGenerator

def test_001():
    """Test basic print statement with string literal"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"), [StringLiteral("Hello World")]
                        )
                    )
                ],
            )
        ],
    )
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_002():
    """Test integer literal printing with auto-conversion"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [IntegerLiteral(123)],  # Direct integer - auto-converts to string
                        )
                    )
                ],
            )
        ],
    )
    expected = "123"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_003():
    """Test float literal printing with auto-conversion"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [FloatLiteral(3.14)],  # Direct float - auto-converts to string
                        )
                    )
                ],
            )
        ],
    )
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_004():
    """Test negative integer literal with auto-conversion"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [IntegerLiteral(-17)],  # Direct negative integer - auto-converts
                        )
                    )
                ],
            )
        ],
    )
    expected = "-17"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_005():
    """Test boolean false literal with auto-conversion"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [BooleanLiteral(False)],  # Direct boolean - auto-converts to string
                        )
                    )
                ],
            )
        ],
    )
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_006():
    """Test boolean true literal with auto-conversion"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [BooleanLiteral(True)],  # Direct boolean - auto-converts to string
                        )
                    )
                ],
            )
        ],
    )
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_007():
    """Test explicit converter function calls still work"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [FunctionCall(Identifier("int2str"), [IntegerLiteral(456)])],
                        )
                    )
                ],
            )
        ],
    )
    expected = "456"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_008():
    """Test mixed expression with auto-conversion"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [IntegerLiteral(0)],  # Should print "0"
                        )
                    )
                ],
            )
        ],
    )
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
    
def test_009():
    """Test function call with len on string"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [
                                FunctionCall(
                                    Identifier("len"),
                                    [StringLiteral("hello")],  # len("hello") = 5
                                )
                            ],
                        )
                    )
                ],
            )
        ],
    )
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_010():
    """Test function call with str conversion"""
    ast = Program(
        [],
        [
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [
                                FunctionCall(
                                    Identifier("float2str"),
                                    [FloatLiteral(3.14)],
                                )
                            ],
                        )
                    )
                ],
            )
        ],
    )
    expected = "3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_011():
    """Test integer variable declaration and usage"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(100)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ])
    ])
    expected = "100"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_012():
    """Test float variable declaration"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("y", FloatType(), FloatLiteral(2.718)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("y")]))
        ])
    ])
    expected = "2.718"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_013():
    """Test string variable declaration"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("name", StringType(), StringLiteral("Alice")),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("name")]))
        ])
    ])
    expected = "Alice"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_014():
    """Test boolean variable declaration"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("flag", BoolType(), BooleanLiteral(True)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("flag")]))
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_015():
    """Test variable without explicit type (type inference)"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("auto_var", None, IntegerLiteral(777)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("auto_var")]))
        ])
    ])
    expected = "777"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
    
def test_016():
    """Test integer addition"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(10), "+", IntegerLiteral(20))
            ]))
        ])
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_017():
    """Test integer subtraction"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(50), "-", IntegerLiteral(30))
            ]))
        ])
    ])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_018():
    """Test integer multiplication"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(6), "*", IntegerLiteral(7))
            ]))
        ])
    ])
    expected = "42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_019():
    """Test integer division"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(81), "/", IntegerLiteral(3))
            ]))
        ])
    ])
    expected = "27.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_020():
    """Test modulo operation"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(17), "%", IntegerLiteral(5))
            ]))
        ])
    ])
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
    
def test_021():
    """Test float addition"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(FloatLiteral(1.5), "+", FloatLiteral(2.5))
            ]))
        ])
    ])
    expected = "4.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_022():
    """Test mixed int-float addition"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(10), "+", FloatLiteral(3.14))
            ]))
        ])
    ])
    expected = "13.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_023():
    """Test float multiplication"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(FloatLiteral(2.0), "*", FloatLiteral(3.5))
            ]))
        ])
    ])
    expected = "7.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_024():
    """Test float division"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(FloatLiteral(15.0), "/", FloatLiteral(3.0))
            ]))
        ])
    ])
    expected = "5.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_025():
    """Test complex float expression"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(FloatLiteral(10.0), "*", FloatLiteral(2.0)),
                    "/",
                    FloatLiteral(4.0)
                )
            ]))
        ])
    ])
    expected = "5.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_026():
    """Test string concatenation"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral("Hello"), "+", StringLiteral(" World"))
            ]))
        ])
    ])
    expected = "Hello World"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_027():
    """Test string + integer concatenation"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral("Number: "), "+", IntegerLiteral(42))
            ]))
        ])
    ])
    expected = "Number: 42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_028():
    """Test integer + string concatenation"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(100), "+", StringLiteral(" points"))
            ]))
        ])
    ])
    expected = "100 points"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_029():
    """Test string + boolean concatenation"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(StringLiteral("Result: "), "+", BooleanLiteral(True))
            ]))
        ])
    ])
    expected = "Result: true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_030():
    """Test multiple string concatenations"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(StringLiteral("Hello "), "+", StringLiteral("World")),
                    "+",
                    StringLiteral("!")
                )
            ]))
        ])
    ])
    expected = "Hello World!"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_031():
    """Test int divided by float (int -> float promotion)"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(5), "/", FloatLiteral(2.0))
            ]))
        ])
    ])
    expected = "2.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_032():
    """Test float divided by int (int -> float promotion)"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(FloatLiteral(7.5), "/", IntegerLiteral(3))
            ]))
        ])
    ])
    expected = "2.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_033():
    """Test int divided by int (should keep float if semantics say so)"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(7), "/", IntegerLiteral(2))
            ]))
        ])
    ])
    expected = "3.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_034():
    """Test float numerator, int denominator"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(FloatLiteral(10.0), "/", IntegerLiteral(4))
            ]))
        ])
    ])
    expected = "2.5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected


def test_035():
    """Test int numerator, float denominator"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(9), "/", FloatLiteral(4.5))
            ]))
        ])
    ])
    expected = "2.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
def test_036():
    """Test integer equality"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(5), "==", IntegerLiteral(5))
            ]))
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_037():
    """Test integer inequality"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(3), "!=", IntegerLiteral(7))
            ]))
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_038():
    """Test less than comparison"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(5), "<", IntegerLiteral(10))
            ]))
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_039():
    """Test greater than comparison"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(15), ">", IntegerLiteral(10))
            ]))
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_040():
    """Test less than or equal"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(IntegerLiteral(5), "<=", IntegerLiteral(5))
            ]))
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_041():
    """Test logical AND - true case"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(BooleanLiteral(True), "&&", BooleanLiteral(True))
            ]))
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_042():
    """Test logical AND - false case"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(BooleanLiteral(True), "&&", BooleanLiteral(False))
            ]))
        ])
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_043():
    """Test logical OR - true case"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(BooleanLiteral(False), "||", BooleanLiteral(True))
            ]))
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_044():
    """Test logical OR - false case"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(BooleanLiteral(False), "||", BooleanLiteral(False))
            ]))
        ])
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_045():
    """Test logical NOT"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                UnaryOp("!", BooleanLiteral(False))
            ]))
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_046():
    """Test unary minus on integer"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                UnaryOp("-", IntegerLiteral(42))
            ]))
        ])
    ])
    expected = "-42"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_047():
    """Test unary minus on float"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                UnaryOp("-", FloatLiteral(3.14))
            ]))
        ])
    ])
    expected = "-3.14"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_048():
    """Test unary plus on integer"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                UnaryOp("+", IntegerLiteral(25))
            ]))
        ])
    ])
    expected = "25"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_049():
    """Test double negative"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                UnaryOp("-", UnaryOp("-", IntegerLiteral(100)))
            ]))
        ])
    ])
    expected = "100"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_050():
    """Test NOT on comparison"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [
                UnaryOp("!", BinaryOp(IntegerLiteral(5), "<", IntegerLiteral(3)))
            ]))
        ])
    ])
    expected = "true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
    
def test_051():
    """Test simple assignment"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(10)),
            Assignment(IdLValue("x"), IntegerLiteral(20)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")]))
        ])
    ])
    expected = "20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_052():
    """Test assignment with expression"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("y", IntType(), IntegerLiteral(5)),
            Assignment(IdLValue("y"), BinaryOp(Identifier("y"), "*", IntegerLiteral(3))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("y")]))
        ])
    ])
    expected = "15"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_053():
    """Test multiple assignments"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", IntType(), IntegerLiteral(1)),
            VarDecl("b", IntType(), IntegerLiteral(2)),
            Assignment(IdLValue("a"), IntegerLiteral(10)),
            Assignment(IdLValue("b"), IntegerLiteral(20)),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(Identifier("a"), "+", Identifier("b"))
            ]))
        ])
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_054():
    """Test assignment to different types"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("msg", StringType(), StringLiteral("Hello")),
            Assignment(IdLValue("msg"), StringLiteral("Goodbye")),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("msg")]))
        ])
    ])
    expected = "Goodbye"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_055():
    """Test assignment chain"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(5)),
            VarDecl("y", IntType(), IntegerLiteral(0)),
            Assignment(IdLValue("y"), Identifier("x")),
            Assignment(IdLValue("x"), IntegerLiteral(100)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("y")]))
        ])
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_056():
    """Test integer array literal"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("arr", None, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(0))]))
        ])
    ])
    expected = "1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_057():
    """Test string array literal"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("words", None, ArrayLiteral([StringLiteral("apple"), StringLiteral("banana")])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("words"), IntegerLiteral(1))]))
        ])
    ])
    expected = "banana"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_058():
    """Test float array literal"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("nums", None, ArrayLiteral([FloatLiteral(1.1), FloatLiteral(2.2)])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("nums"), IntegerLiteral(0))]))
        ])
    ])
    expected = "1.1"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_059():
    """Test boolean array literal"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("flags", None, ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False)])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("flags"), IntegerLiteral(1))]))
        ])
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_060():
    """Test single element array"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("single", None, ArrayLiteral([IntegerLiteral(99)])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("single"), IntegerLiteral(0))]))
        ])
    ])
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_061():
    """Test array length function"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("arr", None, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("len"), [Identifier("arr")])]))
        ])
    ])
    expected = "3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_062():
    """Test array access with variable index"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("arr", None, ArrayLiteral([IntegerLiteral(10), IntegerLiteral(20), IntegerLiteral(30)])),
            VarDecl("idx", IntType(), IntegerLiteral(2)),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), Identifier("idx"))]))
        ])
    ])
    expected = "30"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_063():
    """Test array access with expression index"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("data", None, ArrayLiteral([IntegerLiteral(100), IntegerLiteral(200)])),
            ExprStmt(FunctionCall(Identifier("print"), [
                ArrayAccess(Identifier("data"), BinaryOp(IntegerLiteral(2), "-", IntegerLiteral(1)))
            ]))
        ])
    ])
    expected = "200"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_064():
    """Test empty array length"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("empty", ArrayType(IntType(), 0), None),
            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("len"), [Identifier("empty")])]))
        ])
    ])
    expected = "0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_065():
    """Test array length with large array"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("big", None, ArrayLiteral([
                IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3),
                IntegerLiteral(4), IntegerLiteral(5)
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("len"), [Identifier("big")])]))
        ])
    ])
    expected = "5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_066():
    """Test array element assignment"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("arr", None, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])),
            Assignment(ArrayAccessLValue(Identifier("arr"), IntegerLiteral(0)), IntegerLiteral(99)),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("arr"), IntegerLiteral(0))]))
        ])
    ])
    expected = "99"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_067():
    """Test multiple array assignments"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("nums", None, ArrayLiteral([IntegerLiteral(0), IntegerLiteral(0), IntegerLiteral(0)])),
            Assignment(ArrayAccessLValue(Identifier("nums"), IntegerLiteral(0)), IntegerLiteral(10)),
            Assignment(ArrayAccessLValue(Identifier("nums"), IntegerLiteral(1)), IntegerLiteral(20)),
            Assignment(ArrayAccessLValue(Identifier("nums"), IntegerLiteral(2)), IntegerLiteral(30)),
            ExprStmt(FunctionCall(Identifier("print"), [
                BinaryOp(
                    BinaryOp(ArrayAccess(Identifier("nums"), IntegerLiteral(0)), "+",
                             ArrayAccess(Identifier("nums"), IntegerLiteral(1))),
                    "+",
                    ArrayAccess(Identifier("nums"), IntegerLiteral(2))
                )
            ]))
        ])
    ])
    expected = "60"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_068():
    """Test array assignment with variable index"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("data", None, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])),
            VarDecl("pos", IntType(), IntegerLiteral(1)),
            Assignment(ArrayAccessLValue(Identifier("data"), Identifier("pos")), IntegerLiteral(77)),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("data"), IntegerLiteral(1))]))
        ])
    ])
    expected = "77"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_069():
    """Test string array assignment"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("words", None, ArrayLiteral([StringLiteral("old")])),
            Assignment(ArrayAccessLValue(Identifier("words"), IntegerLiteral(0)), StringLiteral("new")),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(Identifier("words"), IntegerLiteral(0))]))
        ])
    ])
    expected = "new"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected