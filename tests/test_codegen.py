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
    """Test recursive fibonacci"""
    ast = Program(
        [],
        [
            FuncDecl(
                "fib",
                [Param("n", IntType())],
                IntType(),
                [
                    IfStmt(
                        BinaryOp(Identifier("n"), "<=", IntegerLiteral(1)),
                        BlockStmt([ReturnStmt(Identifier("n"))]),
                        [],  # không có elif
                        BlockStmt([  # else
                            ReturnStmt(
                                BinaryOp(
                                    FunctionCall(
                                        Identifier("fib"),
                                        [BinaryOp(Identifier("n"), "-", IntegerLiteral(1))],
                                    ),
                                    "+",
                                    FunctionCall(
                                        Identifier("fib"),
                                        [BinaryOp(Identifier("n"), "-", IntegerLiteral(2))],
                                    ),
                                )
                            )
                        ]),
                    )
                ],
            ),
            FuncDecl(
                "main",
                [],
                VoidType(),
                [
                    ExprStmt(
                        FunctionCall(
                            Identifier("print"),
                            [FunctionCall(Identifier("fib"), [IntegerLiteral(6)])],
                        )
                    )
                ],
            ),
        ],
    )
    expected = "8"
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


def test_070():
    """Complex pipeline operator with multiple transformations"""
    ast = Program([], [
        # Helper functions
        FuncDecl("double", [Param("x", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("x"), "*", IntegerLiteral(2)))
        ]),
        FuncDecl("add_five", [Param("x", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("x"), "+", IntegerLiteral(5)))
        ]),
        
        # Main function
        FuncDecl("main", [], VoidType(), [
            # Basic pipeline: 3 >> double
            VarDecl("result1", None, 
                    BinaryOp(IntegerLiteral(3), ">>", Identifier("double"))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("result1")])),
            
            # Chained pipeline: 2 >> double >> add_five
            VarDecl("result2", None,
                    BinaryOp(
                        BinaryOp(IntegerLiteral(2), ">>", Identifier("double")),
                        ">>", Identifier("add_five")
                    )),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("result2")])),
            
            # Pipeline with variable
            VarDecl("num", None, IntegerLiteral(4)),
            VarDecl("result3", None,
                    BinaryOp(Identifier("num"), ">>", Identifier("double"))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("result3")]))
        ])
    ])
    expected = "6\n9\n8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected
    
def test_071():
    """2D integer array declaration and access"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("matrix", None, ArrayLiteral([
                ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]),
                ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)])
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(ArrayAccess(Identifier("matrix"), IntegerLiteral(0)), IntegerLiteral(1))]))
        ])
    ])
    expected = "2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_072():
    """3D boolean array declaration and access"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("flags", None, ArrayLiteral([
                ArrayLiteral([
                    ArrayLiteral([BooleanLiteral(True), BooleanLiteral(False)]),
                    ArrayLiteral([BooleanLiteral(False), BooleanLiteral(True)])
                ]),
                ArrayLiteral([
                    ArrayLiteral([BooleanLiteral(False), BooleanLiteral(False)]),
                    ArrayLiteral([BooleanLiteral(True), BooleanLiteral(True)])
                ])
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(ArrayAccess(ArrayAccess(Identifier("flags"), IntegerLiteral(0)), IntegerLiteral(1)), IntegerLiteral(0))]))
        ])
    ])
    expected = "false"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_073():
    """2D float array declaration, assignment and access"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("nums", None, ArrayLiteral([
                ArrayLiteral([FloatLiteral(1.5), FloatLiteral(2.5)]),
                ArrayLiteral([FloatLiteral(3.5), FloatLiteral(4.5)])
            ])),
            Assignment(ArrayAccessLValue(ArrayAccess(Identifier("nums"), IntegerLiteral(1)), IntegerLiteral(0)), FloatLiteral(9.9)),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(ArrayAccess(Identifier("nums"), IntegerLiteral(1)), IntegerLiteral(0))]))
        ])
    ])
    expected = "9.9"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_074():
    """Nested string array declaration and access"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("words", None, ArrayLiteral([
                ArrayLiteral([StringLiteral("hello"), StringLiteral("world")]),
                ArrayLiteral([StringLiteral("foo"), StringLiteral("bar")])
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(ArrayAccess(Identifier("words"), IntegerLiteral(1)), IntegerLiteral(1))]))
        ])
    ])
    expected = "bar"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_075():
    """Mixed type 2D array (int array inside float array) access"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("mixed", None, ArrayLiteral([
                ArrayLiteral([FloatLiteral(1), FloatLiteral(2)]),
                ArrayLiteral([FloatLiteral(3.1), FloatLiteral(4.2)])
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [ArrayAccess(ArrayAccess(Identifier("mixed"), IntegerLiteral(0)), IntegerLiteral(0))]))
        ])
    ])
    expected = "1.0"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_076():
    """Simple if statement - true condition"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", None, IntegerLiteral(10)),
            IfStmt(BinaryOp(Identifier("x"), "==", IntegerLiteral(10)), 
                   BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("equal")]))]),
                   [], None)
        ])
    ])
    expected = "equal"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_077():
    """Simple if statement - false condition"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", None, IntegerLiteral(5)),
            IfStmt(BinaryOp(Identifier("x"), "==", IntegerLiteral(10)), 
                   BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("equal")]))]),
                   [], None)
        ])
    ])
    expected = ""
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_078():
    """If-else statement"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", None, IntegerLiteral(5)),
            IfStmt(BinaryOp(Identifier("x"), "==", IntegerLiteral(10)), 
                   BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("equal")]))]),
                   [],
                   BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("not equal")]))]))
        ])
    ])
    expected = "not equal"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_079():
    """If-elif-else statement"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("score", None, IntegerLiteral(85)),
            IfStmt(BinaryOp(Identifier("score"), ">=", IntegerLiteral(90)), 
                   BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("A")]))]),
                   [(BinaryOp(Identifier("score"), ">=", IntegerLiteral(80)), 
                     BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("B")]))]))],
                   BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("C")]))]))
        ])
    ])
    expected = "B"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_080():
    """Nested if statements with float-int type"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", None, IntegerLiteral(15)),
            IfStmt(BinaryOp(Identifier("x"), ">", IntegerLiteral(10)), 
                   BlockStmt([
                       IfStmt(BinaryOp(Identifier("x"), "<", FloatLiteral(20)), 
                              BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("between 10 and 20")]))]),
                              [], None)
                   ]),
                   [], None)
        ])
    ])
    expected = "between 10 and 20"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_081():
    """Simple while loop"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", None, IntegerLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntegerLiteral(3)), 
                      BlockStmt([
                          ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")])),
                          Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                      ]))
        ])
    ])
    expected = "0\n1\n2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_082():
    """While loop with condition false from start"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", None, IntegerLiteral(5)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntegerLiteral(3)), 
                      ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("inside loop")])))
        ])
    ])
    expected = ""
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_083():
    """For loop with array"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("nums", None, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
            ForStmt("x", Identifier("nums"), 
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")])))
        ])
    ])
    expected = "1\n2\n3"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_084():
    """For loop with empty array"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("nums", ArrayType(IntType(), 0), None),
            ForStmt("x", Identifier("nums"), 
                    ExprStmt(FunctionCall(Identifier("print"), [Identifier("x")])))
        ])
    ])
    expected = ""
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_085():
    """While loop with break"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", None, IntegerLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntegerLiteral(10)), 
                      BlockStmt([
                          IfStmt(BinaryOp(Identifier("i"), "==", IntegerLiteral(3)), 
                                 BlockStmt([BreakStmt()]), [], None),
                          ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")])),
                          Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1)))
                      ]))
        ])
    ])
    expected = "0\n1\n2"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_086():
    """While loop with continue"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("i", None, IntegerLiteral(0)),
            WhileStmt(BinaryOp(Identifier("i"), "<", IntegerLiteral(5)), 
                      BlockStmt([
                          Assignment(IdLValue("i"), BinaryOp(Identifier("i"), "+", IntegerLiteral(1))),
                          IfStmt(BinaryOp(Identifier("i"), "==", IntegerLiteral(3)), 
                                 BlockStmt([ContinueStmt()]), [], None),
                          ExprStmt(FunctionCall(Identifier("print"), [Identifier("i")]))
                      ]))
        ])
    ])
    expected = "1\n2\n4\n5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_087():
    """Function with return value"""
    ast = Program([], [
        FuncDecl("add", [Param("a", IntType()), Param("b", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
        ]),
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("add"), [IntegerLiteral(5), IntegerLiteral(3)])]))
        ])
    ])
    expected = "8"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_088():
    """Short-circuit AND in IF"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            IfStmt(BinaryOp(BooleanLiteral(True), "&&", BooleanLiteral(True)),
                   BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("A")]))]),
                   [], None),

            IfStmt(BinaryOp(BooleanLiteral(False), "&&", 
                            FunctionCall(Identifier("print"), [StringLiteral("B")])),
                   BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("C")]))]),
                   [], None),

            IfStmt(BinaryOp(BooleanLiteral(True), "&&", 
                            FunctionCall(Identifier("print"), [StringLiteral("D")])),
                   BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("E")]))]),
                   [], None),
        ])
    ])
    expected = "A\nD\nE"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_089():
    """Short-circuit OR in IF"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            IfStmt(BinaryOp(BooleanLiteral(True), "||", 
                            FunctionCall(Identifier("print"), [StringLiteral("X")])),
                   BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Y")]))]),
                   [], None),
            IfStmt(BinaryOp(BooleanLiteral(False), "||", 
                            FunctionCall(Identifier("print"), [StringLiteral("Z")])),
                   BlockStmt([ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("W")]))]),
                   [], None),
        ])
    ])
    expected = "Y\nZ\nW"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_090():
    """Expression statement with side effects"""
    ast = Program([], [
        FuncDecl("side_effect", [], IntType(), [
            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("side effect")])),
            ReturnStmt(IntegerLiteral(42))
        ]),
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("side_effect"), [])),
            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("done")]))
        ])
    ])
    expected = "side effect\ndone"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_091():
    """Boolean short-circuit AND"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", None, BooleanLiteral(False)),
            VarDecl("b", None, BooleanLiteral(True)),
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("a"), "&&", Identifier("b"))])),
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("b"), "&&", Identifier("a"))])),
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("b"), "&&", Identifier("b"))]))
        ])
    ])
    expected = "false\nfalse\ntrue"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_092():
    """Boolean short-circuit OR"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", None, BooleanLiteral(False)),
            VarDecl("b", None, BooleanLiteral(True)),
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("a"), "||", Identifier("b"))])),
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("a"), "||", Identifier("a"))])),
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("b"), "||", Identifier("a"))]))
        ])
    ])
    expected = "true\nfalse\ntrue"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_093():
    """String concatenation with mixed types"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("name", None, StringLiteral("Value:")),
            VarDecl("num", None, IntegerLiteral(42)),
            VarDecl("flag", None, BooleanLiteral(True)),
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(Identifier("name"), "+", Identifier("num"))])),
            ExprStmt(FunctionCall(Identifier("print"), [BinaryOp(StringLiteral("Flag is "), "+", Identifier("flag"))]))
        ])
    ])
    expected = "Value:42\nFlag is true"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_094():
    """Unary operators"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", None, IntegerLiteral(5)),
            VarDecl("y", None, FloatLiteral(3.14)),
            VarDecl("flag", None, BooleanLiteral(True)),
            ExprStmt(FunctionCall(Identifier("print"), [UnaryOp("-", Identifier("x"))])),
            ExprStmt(FunctionCall(Identifier("print"), [UnaryOp("-", Identifier("y"))])),
            ExprStmt(FunctionCall(Identifier("print"), [UnaryOp("!", Identifier("flag"))])),
            ExprStmt(FunctionCall(Identifier("print"), [UnaryOp("+", Identifier("x"))]))
        ])
    ])
    expected = "-5\n-3.14\nfalse\n5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_095():
    """Complex expression with precedence"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("a", None, IntegerLiteral(2)),
            VarDecl("b", None, IntegerLiteral(3)),
            VarDecl("c", None, IntegerLiteral(4)),
            # (a + b) * c - a
            VarDecl("result", None, BinaryOp(
                BinaryOp(BinaryOp(Identifier("a"), "+", Identifier("b")), "*", Identifier("c")), 
                "-", 
                Identifier("a"))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("result")]))
        ])
    ])
    expected = "18"  # (2 + 3) * 4 - 2 = 20 - 2 = 18
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_096():
    """Pipeline operator (>>)"""
    ast = Program([], [
        FuncDecl("double", [Param("x", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("x"), "*", IntegerLiteral(2)))
        ]),
        FuncDecl("main", [], VoidType(), [
            VarDecl("result", None, BinaryOp(IntegerLiteral(5), ">>", Identifier("double"))),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("result")]))
        ])
    ])
    expected = "10"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_097():
    """Constants declaration and usage"""
    ast = Program([
        ConstDecl("PI", None, FloatLiteral(3.14159)),
        ConstDecl("MAX_SIZE", None, IntegerLiteral(100))
    ], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("PI")])),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("MAX_SIZE")]))
        ])
    ])
    expected = "3.1416\n100"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_098():
    """Len function with array and string"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("arr", None, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])),
            VarDecl("str", None, StringLiteral("hello")),
            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("len"), [Identifier("arr")])])),
            ExprStmt(FunctionCall(Identifier("print"), [FunctionCall(Identifier("len"), [Identifier("str")])]))
        ])
    ])
    expected = "3\n5"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_099():
    """Nested function calls"""
    ast = Program([], [
        FuncDecl("add", [Param("a", IntType()), Param("b", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("a"), "+", Identifier("b")))
        ]),
        FuncDecl("multiply", [Param("a", IntType()), Param("b", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("a"), "*", Identifier("b")))
        ]),
        FuncDecl("main", [], VoidType(), [
            # multiply(add(2, 3), add(4, 1))
            VarDecl("result", None, FunctionCall(Identifier("multiply"), [
                FunctionCall(Identifier("add"), [IntegerLiteral(2), IntegerLiteral(3)]),
                FunctionCall(Identifier("add"), [IntegerLiteral(4), IntegerLiteral(1)])
            ])),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("result")]))
        ])
    ])
    expected = "25"  # (2+3) * (4+1) = 5 * 5 = 25
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected

def test_100():
    """Complex program with multiple features - Modified to remove factorial"""
    ast = Program([
        ConstDecl("LIMIT", None, IntegerLiteral(10))
    ], [
        FuncDecl("square", [Param("n", IntType())], IntType(), [
            ReturnStmt(BinaryOp(Identifier("n"), "*", Identifier("n")))
        ]),
        FuncDecl("main", [], VoidType(), [
            VarDecl("numbers", None, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4)])),
            ExprStmt(FunctionCall(Identifier("print"), [StringLiteral("Squares:")])),
            ForStmt("num", Identifier("numbers"),
                    BlockStmt([
                        IfStmt(BinaryOp(Identifier("num"), "<", Identifier("LIMIT")),
                               ExprStmt(FunctionCall(Identifier("print"),
                                       [BinaryOp(BinaryOp(Identifier("num"), "+", StringLiteral("^2 = ")),
                                                "+", FunctionCall(Identifier("square"), [Identifier("num")]))])),
                               [], None)
                    ]))
        ])
    ])
    expected = "Squares:\n1^2 = 1\n2^2 = 4\n3^2 = 9\n4^2 = 16"
    result = CodeGenerator().generate_and_run(ast)
    assert result == expected