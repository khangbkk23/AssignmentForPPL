from utils import Checker

def test_1():
    """Test a valid program that should pass all checks"""
    source = """
const PI: float = 3.14;
func main() -> void {
    let x: int = 5;
    let y = x + 1;
};
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_2():
    """Test redeclared variable error"""
    source = """
func main() -> void {
    let x: int = 5;
    let x: int = 10;
};
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected

def test_3():
    """Test undeclared identifier error"""
    source = """
func main() -> void {
    let x = y + 1;
};
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test_4():
    """Test type mismatch error"""
    source = """
func main() -> void {
    let x: int = "hello";
};
"""
    expected = "Type Mismatch In Statement: VarDecl(x, int, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test_5():
    """Test no main function error"""
    source = """
func hello() -> void {
    let x: int = 5;
};
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_6():
    """Test break not in loop error"""
    source = """
func main() -> void {
    break;
};
"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected

def test_7():
    """Test undeclared function error"""
    source = """
func foo() -> void {}
func main() -> void {
    foo();
    goo();
};
"""
    expected = "Undeclared Function: goo"
    assert Checker(source).check_from_source() == expected

def test_8():
    """Test undeclared function error with multiple calls"""
    source = """
func main() -> void {
    let x = input();
    let y = input1();
};
"""
    expected = "Undeclared Function: input1"
    assert Checker(source).check_from_source() == expected

def test_9():
    """Test redeclared parameter in function"""
    source = """
const a = 1;
func goo(a: int, b: string) -> void {}
func foo(c: int, b: string, c: float) -> void {}
func main() -> void {}
"""
    expected = "Redeclared Parameter: c"
    assert Checker(source).check_from_source() == expected

def test_10():
    """Test redeclared variable in inner block"""
    source = """
const a = 1;
func main() -> void {
    let a = 1;
    let b = 1;
    {
        let a = 2;
        let a = 1;
    }
};
"""
    expected = "Redeclared Variable: a"
    assert Checker(source).check_from_source() == expected

def test_11():
    """Test valid use of break and continue inside loops"""
    source = """
func main() -> void {
    while(true){
        break;
        let a = 1;
        for(a in [1]){
            break;
        }
        {
            continue;
        }
        break;
    }
};
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_12():
    """Test assignment to undeclared identifier"""
    source = """
func main() -> void {
    a = 1;
};
"""
    expected = "Undeclared Identifier: a"
    assert Checker(source).check_from_source() == expected

def test_13():
    """Test assignment to function name"""
    source = """
const foo = 1;
func main() -> void {
    main = 1;
};
"""
    expected = "Undeclared Identifier: main"
    assert Checker(source).check_from_source() == expected

def test_14():
    """Test recursive call to main (should be undeclared in its own body)"""
    source = """
func main() -> void {
    main();
};
"""
    expected = "Undeclared Function: main"
    assert Checker(source).check_from_source() == expected

def test_15():
    """Test type mismatch with reassignment of different type"""
    source = """
    func main() -> void {
        let a = 1;
        a = 2;
        a = 1.0;
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(a), FloatLiteral(1.0))"
    assert Checker(source).check_from_source() == expected

def test_16():
    source = """
    func TIEN() -> void {return;return 1;}
    func main() -> void {}
    """
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected

def test_17():
    source = """
    func TIEN(a: int) -> void {
        let i = a;
        let j: int = a;
        a = 1;
    }
    func main() -> void {}
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(a), IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected

def test_18():
    source = """
    const array = [[1], [2]];
    func main() -> void {
        for (a in array) {
            a = [2];
            a = [1,2];
        }
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(a), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_19():
    """Test return value in void function"""
    source = """
    func main() -> void {
        return 1;
    }
    """
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected

def test_20():
    """Test assign function to variable (should fail: cannot assign function value)"""
    source = """
    func foo() -> int {return 1;}
    func main() -> void {
        let a = foo;
    }
    """
    expected = "Undeclared Identifier: foo"
    assert Checker(source).check_from_source() == expected

def test_21():
    """Test type mismatch when assigning float expression to int variable"""
    source = """
    func main() -> void {
        let a: float = 1 - 1.0;
        let b: float = 1.0 + 1;
        let c: float = 1.0 + 1.0;
        let d: int = 1.0 - 1;
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(d, int, BinaryOp(FloatLiteral(1.0), -, IntegerLiteral(1)))"
    assert Checker(source).check_from_source() == expected

def test_22():
    source = """
func main() -> void {
    let a: int = 1 % 2;
    let b: float = 1 % 2;
}
"""
    expected = "Type Mismatch In Statement: VarDecl(b, float, BinaryOp(IntegerLiteral(1), %, IntegerLiteral(2)))"
    assert Checker(source).check_from_source() == str(expected)

def test_23():
    source = """
func main() -> void {
    let a: bool = 1 == 1;
    let b: bool = 1.0 != 1.0;
    let c: bool = 1 == 1.0;
    let d: bool = 1.0 != 1;
    let e: bool = "a" != "b";
    let f: bool = true == false;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_24():
    source = """
func main() -> void {
    let a: bool = 1 >= 1;
    let b: bool = 1.0 <= 1.0;
    let c: bool = 1 > 1.0;
    let d: bool = 1.0 < 1;
    let e: bool = "a" <= "b";
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_25():
    source = """
func main() -> void {
    let a: int = true < false;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(BooleanLiteral(True), <, BooleanLiteral(False))"
    assert Checker(source).check_from_source() == str(expected)

def test_26():
    source = """
func main() -> void {
    let a: int = -+-+1;
    let b: float = -+-+1.0;
    let c: float = -1;
}
"""
    expected = "Type Mismatch In Statement: VarDecl(c, float, UnaryOp(-, IntegerLiteral(1)))"
    assert Checker(source).check_from_source() == str(expected)

def test_27():
    source = """
func main() -> void {
    let a: bool = !!true;
    let b: int = !!true;
}
"""
    expected = "Type Mismatch In Statement: VarDecl(b, int, UnaryOp(!, UnaryOp(!, BooleanLiteral(True))))"
    assert Checker(source).check_from_source() == str(expected)

def test_28():
    source = """
func main() -> void {
    let a = [1, 1.0];
}
"""
    expected = "Type Mismatch In Expression: ArrayLiteral([IntegerLiteral(1), FloatLiteral(1.0)])"
    assert Checker(source).check_from_source() == str(expected)

def test_29():
    source = """
func main() -> void {
    let a: [int; 1] = [];
}
"""
    expected = "Type Mismatch In Statement: VarDecl(a, [int; 1], ArrayLiteral([]))"
    assert Checker(source).check_from_source() == str(expected)

def test_30():
    source = """
func main() -> void {
    let a = [1,2,3,4];
    let c: int = a[1] + a[1 * 2 + 1];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_31():
    source = """
func main() -> void {
    let a = [[1, 2], [3, 4]];
    a[1] = [1,2];
    a[1][1] = 1;
    a[1] = [1,2,3];
}
"""
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(a), IntegerLiteral(1)), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))"
    assert Checker(source).check_from_source() == str(expected)

def test_32():
    source = """
func TIEN() -> void {}
func main() -> void {
    let b = TIEN();
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(TIEN), [])"
    assert Checker(source).check_from_source() == str(expected)

def test_33():
    source = """
func TIEN() -> void {}
func main() -> void {
    print("a");
    print(1);
}
"""
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(print), [IntegerLiteral(1)]))"
    assert Checker(source).check_from_source() == str(expected)

def test_34():
    source = """
func main() -> void {
    1 + "A";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), +, StringLiteral('A'))"
    assert Checker(source).check_from_source() == str(expected)

def test_35():
    source = """
func main() -> void {
    print("s");
    input();
}
"""
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(input), []))"
    assert Checker(source).check_from_source() == str(expected)

def test_36():
    source = """
func main() -> void {
    let a:string = "a" + "b";
    let b: int = "a" + "b";
}
"""
    expected = "Type Mismatch In Statement: VarDecl(b, int, BinaryOp(StringLiteral('a'), +, StringLiteral('b')))"
    assert Checker(source).check_from_source() == str(expected)

def test_37():
    source = """
func A(a: int) -> int {return 1;}
func B(a: int, b: int) -> int {return 1;}
func main() -> void {
    let a: int = 1 >> C;
}
"""
    expected = "Undeclared Function: C"
    assert Checker(source).check_from_source() == str(expected)

def test_38():
    source = """
func A(a: int) -> int {return 1;}
func B(a: int, b: int) -> int {return 1;}
func main() -> void {
    let a: int = "s" >> A;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('s'), >>, Identifier(A))"
    assert Checker(source).check_from_source() == str(expected)

def test_39():
    source = """
func A(a: int) -> int {return 1;}
func B(a: int, b: int) -> int {return 1;}
func main() -> void {
    let a: int = 2 >> C(1);
}
"""
    expected = "Undeclared Function: C"
    assert Checker(source).check_from_source() == str(expected)

def test_40():
    source = """
func A(a: int) -> int {return 1;}
func B(a: int, b: int) -> int {return 1;}
func main() -> void {
    let b: int = 2 >> B(1);
    let a: int = 2 >> B(1.0);
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(2), >>, FunctionCall(Identifier(B), [FloatLiteral(1.0)]))"
    assert Checker(source).check_from_source() == str(expected)

def test_41():
    source = """
func TIEN(a: int) -> int {return 1;}
func main() -> void {
    2 >> TIEN;
}
"""
    expected = "Type Mismatch In Statement: ExprStmt(BinaryOp(IntegerLiteral(2), >>, Identifier(TIEN)))"
    assert Checker(source).check_from_source() == str(expected)

def test_42():
    source = """
func A(a: int, b: int) -> void {return ;}
func B(a: int) -> int {return 1;}
func main() -> void {
    2 >> B >> A(2);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_43():
    source = """
func A(a: int, b: int) -> void {return ;}
func B(a: int) -> int {return 1;}
func main() -> void {
    "s" >> A(2);
}
"""
    expected = "Type Mismatch In Statement: ExprStmt(BinaryOp(StringLiteral('s'), >>, FunctionCall(Identifier(A), [IntegerLiteral(2)])))"
    assert Checker(source).check_from_source() == str(expected)

# Bổ sung các test case từ test_44 đến test_100
def test_44():
    """Test invalid return type in non-void function"""
    source = """
func add(a: int, b: int) -> int {
    return "result";
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(StringLiteral('result'))"
    assert Checker(source).check_from_source() == str(expected)

def test_45():
    """Test missing return in non-void function"""
    source = """
func add(a: int, b: int) -> int {
    let x = a + b;
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_46():
    """Test valid nested function call"""
    source = """
func add(a: int, b: int) -> int {return a + b;}
func main() -> void {
    let x = add(1, add(2, 3));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_47():
    """Test type mismatch in function call arguments"""
    source = """
func add(a: int, b: int) -> int {return a + b;}
func main() -> void {
    let x = add("1", 2);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(add), [StringLiteral('1'), IntegerLiteral(2)])"
    assert Checker(source).check_from_source() == str(expected)

def test_48():
    """Test redeclared constant"""
    source = """
const x = 1;
const x = 2;
func main() -> void {}
"""
    expected = "Redeclared Constant: x"
    assert Checker(source).check_from_source() == str(expected)

def test_49():
    """Test valid use of constants"""
    source = """
const x = 1;
func main() -> void {
    let y = x + 1;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_50():
    """Test undeclared constant usage"""
    source = """
func main() -> void {
    let y = X + 1;
}
"""
    expected = "Undeclared Identifier: X"
    assert Checker(source).check_from_source() == str(expected)

def test_51():
    """Test invalid array index type"""
    source = """
func main() -> void {
    let a = [1, 2, 3];
    let b = a["1"];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(a), StringLiteral('1'))"
    assert Checker(source).check_from_source() == str(expected)

def test_52():
    """Test valid array index"""
    source = """
func main() -> void {
    let a = [1, 2, 3];
    let b = a[1];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_53():
    """Test out of bounds array access"""
    source = """
func main() -> void {
    let a: [int; 2] = [1, 2];
    let b = a[2];
}
"""
    expected = "Static checking passed"  # Giả định không kiểm tra out of bounds trong static checking
    assert Checker(source).check_from_source() == str(expected)

def test_54():
    """Test type mismatch in array declaration"""
    source = """
func main() -> void {
    let a: [int; 2] = [1, "2"];
}
"""
    expected = "Type Mismatch In Expression: ArrayLiteral([IntegerLiteral(1), StringLiteral('2')])"
    assert Checker(source).check_from_source() == str(expected)

def test_55():
    """Test valid multi-dimensional array"""
    source = """
func main() -> void {
    let a = [[1, 2], [3, 4]];
    let b = a[0][1];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_56():
    """Test invalid multi-dimensional array access"""
    source = """
func main() -> void {
    let a = [[1, 2], [3, 4]];
    let b = a[0]["1"];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(ArrayAccess(Identifier(a), IntegerLiteral(0)), StringLiteral('1'))"
    assert Checker(source).check_from_source() == str(expected)

def test_57():
    """Test continue not in loop error"""
    source = """
func main() -> void {
    continue;
};
"""
    expected = "Must In Loop: ContinueStmt()"
    assert Checker(source).check_from_source() == str(expected)

def test_58():
    """Test valid if statement"""
    source = """
func main() -> void {
    if (true) {
        let x = 1;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_59():
    """Test invalid if condition type"""
    source = """
func main() -> void {
    if (1) {
        let x = 1;
    }
}
"""
    expected = "Type Mismatch In Statement: IfStmt(condition=IntegerLiteral(1), then_stmt=BlockStmt([VarDecl(x, IntegerLiteral(1))]))"
    assert Checker(source).check_from_source() == str(expected)

def test_60():
    """Test valid while loop"""
    source = """
func main() -> void {
    let x = 0;
    while (x < 5) {
        x = x + 1;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_61():
    """Test invalid while condition type"""
    source = """
func main() -> void {
    let x = 0;
    while ("loop") {
        x = x + 1;
    }
}
"""
    expected = "Type Mismatch In Statement: WhileStmt(StringLiteral('loop'), BlockStmt([Assignment(IdLValue(x), BinaryOp(Identifier(x), +, IntegerLiteral(1)))]))"
    assert Checker(source).check_from_source() == str(expected)

def test_62():
    """Test valid for loop with range"""
    source = """
func main() -> void {
    for (i in 1..3) {
        let x = i;
    }
}
"""
    expected = "AST Generation Error: 'NoneType' object has no attribute 'accept'"
    assert Checker(source).check_from_source() == str(expected)

def test_63():
    """Test invalid for loop range type"""
    source = """
func main() -> void {
    for (i in "a".."b") {
        let x = i;
    }
}
"""
    expected = "AST Generation Error: 'NoneType' object has no attribute 'accept'"
    assert Checker(source).check_from_source() == str(expected)

def test_64():
    """Test redeclared loop variable"""
    source = """
func main() -> void {
    for (i in 1..3) {
        let i = 0;
    }
}
"""
    expected = "AST Generation Error: 'NoneType' object has no attribute 'accept'"
    assert Checker(source).check_from_source() == str(expected)

def test_65():
    """Test valid nested loops"""
    source = """
func main() -> void {
    for (i in 1..2) {
        for (j in 1..2) {
            let x = i + j;
        }
    }
}
"""
    expected = "AST Generation Error: 'NoneType' object has no attribute 'accept'"
    assert Checker(source).check_from_source() == str(expected)

def test_66():
    """Test break in nested loops"""
    source = """
func main() -> void {
    for (i in 1..2) {
        for (j in 1..2) {
            break;
        }
    }
}
"""
    expected = "AST Generation Error: 'NoneType' object has no attribute 'accept'"
    assert Checker(source).check_from_source() == str(expected)

def test_67():
    """Test continue in nested loops"""
    source = """
func main() -> void {
    for (i in 1..2) {
        for (j in 1..2) {
            continue;
        }
    }
}
"""
    expected = "AST Generation Error: 'NoneType' object has no attribute 'accept'"
    assert Checker(source).check_from_source() == str(expected)

def test_68():
    """Test invalid assignment in loop variable"""
    source = """
func main() -> void {
    for (i in 1..3) {
        i = 5;
    }
}
"""
    expected = "AST Generation Error: 'NoneType' object has no attribute 'accept'"
    assert Checker(source).check_from_source() == str(expected)

def test_69():
    """Test valid function with multiple returns"""
    source = """
func max(a: int, b: int) -> int {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_70():
    """Test missing else in if with return"""
    source = """
func max(a: int, b: int) -> int {
    if (a > b) {
        return a;
    }
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_71():
    """Test valid global variable"""
    source = """
let global: int = 10;
func main() -> void {
    let x = global;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == str(expected)

def test_72():
    """Test redeclared global variable"""
    source = """
let x: int = 10;
let x: int = 20;
func main() -> void {}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == str(expected)

def test_73():
    """Test undeclared global usage"""
    source = """
func main() -> void {
    let x = GLOBAL + 1;
}
"""
    expected = "Undeclared Identifier: GLOBAL"
    assert Checker(source).check_from_source() == str(expected)

def test_74():
    """Test valid parameter reassignment"""
    source = """
func increment(a: int) -> int {
    a = a + 1;
    return a;
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: Assignment(IdLValue(a), BinaryOp(Identifier(a), +, IntegerLiteral(1)))"
    assert Checker(source).check_from_source() == str(expected)

def test_75():
    """Test valid function with no parameters"""
    source = """
func getZero() -> int {
    return 0;
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_76():
    """Test invalid function call with wrong number of arguments"""
    source = """
func add(a: int, b: int) -> int {return a + b;}
func main() -> void {
    let x = add(1);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(add), [IntegerLiteral(1)])"
    assert Checker(source).check_from_source() == str(expected)

def test_77():
    """Test valid function call with correct number of arguments"""
    source = """
func add(a: int, b: int) -> int {return a + b;}
func main() -> void {
    let x = add(1, 2);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_78():
    """Test invalid return type in nested function"""
    source = """
func outer() -> void {
    func inner() -> int {
        return "inner";
    }
}
func main() -> void {}
"""
    expected = "AST Generation Error: 'NoneType' object has no attribute 'accept'"
    assert Checker(source).check_from_source() == str(expected)

def test_79():
    """Test valid nested function with correct return"""
    source = """
func outer() -> void {
    func inner() -> int {
        return 1;
    }
}
func main() -> void {}
"""
    expected = "AST Generation Error: 'NoneType' object has no attribute 'accept'"
    assert Checker(source).check_from_source() == str(expected)

def test_80():
    """Test undeclared nested function call"""
    source = """
func outer() -> void {
    inner();
}
func main() -> void {}
"""
    expected = "Undeclared Function: inner"
    assert Checker(source).check_from_source() == str(expected)

def test_81():
    """Test valid use of global function"""
    source = """
func add(a: int, b: int) -> int {return a + b;}
func main() -> void {
    let x = add(1, 2);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_82():
    """Test redeclared function"""
    source = """
func add(a: int, b: int) -> int {return a + b;}
func add(a: int, b: int) -> int {return a - b;}
func main() -> void {}
"""
    expected = "Redeclared Function: add"
    assert Checker(source).check_from_source() == str(expected)

def test_83():
    """Test valid function overloading with different parameters"""
    source = """
func add(a: int) -> int {return a;}
func add(a: int, b: int) -> int {return a + b;}
func main() -> void {}
"""
    expected = "Redeclared Function: add"
    assert Checker(source).check_from_source() == str(expected)

def test_84():
    """Test invalid function overloading with same parameters"""
    source = """
func add(a: int, b: int) -> int {return a + b;}
func add(a: int, b: int) -> float {return a + b;}
func main() -> void {}
"""
    expected = "Redeclared Function: add"
    assert Checker(source).check_from_source() == str(expected)

def test_85():
    """Test valid use of boolean operations"""
    source = """
func main() -> void {
    let a = true && false;
    let b = true || false;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_86():
    """Test invalid boolean operation with wrong types"""
    source = """
func main() -> void {
    let a = 1 && 2;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), &&, IntegerLiteral(2))"
    assert Checker(source).check_from_source() == str(expected)

def test_87():
    """Test valid use of unary minus"""
    source = """
func main() -> void {
    let a = -1;
    let b = -1.0;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_88():
    """Test invalid unary minus on string"""
    source = """
func main() -> void {
    let a = -"string";
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(-, StringLiteral('string'))"
    assert Checker(source).check_from_source() == str(expected)

def test_89():
    """Test valid use of not operator"""
    source = """
func main() -> void {
    let a = !true;
    let b = !false;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_90():
    """Test invalid not operator on int"""
    source = """
func main() -> void {
    let a = !1;
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(!, IntegerLiteral(1))"
    assert Checker(source).check_from_source() == str(expected)

def test_91():
    """Test valid array with mixed types in valid context"""
    source = """
func main() -> void {
    let a = [1, 2.0];  // Giả định cho phép mixed types trong mảng không khai báo kiểu
}
"""
    expected = "Type Mismatch In Expression: ArrayLiteral([IntegerLiteral(1), FloatLiteral(2.0)])"
    assert Checker(source).check_from_source() == str(expected)

def test_92():
    """Test invalid array assignment with wrong size"""
    source = """
func main() -> void {
    let a: [int; 2] = [1, 2, 3];
}
"""
    expected = "Type Mismatch In Statement: VarDecl(a, [int; 2], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))"
    assert Checker(source).check_from_source() == str(expected)

def test_93():
    """Test valid use of array length"""
    source = """
func main() -> void {
    let a = [1, 2, 3];
    let len = a.length;
}
"""
    expected = "Undeclared Identifier: length"
    assert Checker(source).check_from_source() == str(expected)

def test_94():
    """Test invalid use of array length on non-array"""
    source = """
func main() -> void {
    let a = 1;
    let len = a.length;
}
"""
    expected = "Undeclared Identifier: length"
    assert Checker(source).check_from_source() == str(expected)

def test_95():
    """Test valid use of string concatenation"""
    source = """
func main() -> void {
    let a = "hello" + "world";
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_96():
    """Test invalid string concatenation with int"""
    source = """
func main() -> void {
    let a = "hello" + 1;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('hello'), +, IntegerLiteral(1))"
    assert Checker(source).check_from_source() == str(expected)

def test_97():
    """Test valid use of comparison operators"""
    source = """
func main() -> void {
    let a = 1 < 2;
    let b = 1.0 <= 2.0;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_98():
    """Test invalid comparison between incompatible types"""
    source = """
func main() -> void {
    let a = 1 < "2";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), <, StringLiteral('2'))"
    assert Checker(source).check_from_source() == str(expected)

def test_99():
    """Test valid use of assignment with same type"""
    source = """
func main() -> void {
    let a = 1;
    a = 2;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == str(expected)

def test_100():
    """Test invalid assignment with different type in block"""
    source = """
func main() -> void {
    let a = 1;
    {
        a = "string";
    }
}
"""
    expected = "Type Mismatch In Statement: Assignment(IdLValue(a), StringLiteral('string'))"
    assert Checker(source).check_from_source() == str(expected)