from utils import Checker

def test_001():
    """Test assignment to constant identifier"""
    source = """
const PI = 3.14;
func main() -> void {
    PI = 2.71;
}
"""
    expected = "Type Mismatch In Statement: Assignment(IdLValue(PI), FloatLiteral(2.71))"
    assert Checker(source).check_from_source() == expected

def test_002():
    """Test constant without type annotation with complex expression"""
    source = """
const RESULT = 10 + 5 * 2;
func main() -> void {
    let x = RESULT;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_003():
    """Test constant with wrong type annotation"""
    source = """
const X: string = 42;
func main() -> void {}
"""
    expected = "Type Mismatch In Expression: ConstDecl(X, string, IntegerLiteral(42))"
    assert Checker(source).check_from_source() == expected

def test_004():
    """Test function parameter shadowing constant"""
    source = """
const VALUE = 10;
func test(VALUE: int) -> void {
    let x = VALUE;
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_005():
    """Test local variable shadowing constant"""
    source = """
const MAX = 100;
func main() -> void {
    let MAX = "hundred";
    let x = MAX;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_006():
    """Test array access on non-array identifier"""
    source = """
func main() -> void {
    let x = 42;
    let y = x[0];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(x), IntegerLiteral(0))"
    assert Checker(source).check_from_source() == expected

def test_007():
    """Test array assignment with wrong element type"""
    source = """
func main() -> void {
    let arr = [1, 2, 3];
    arr[0] = "hello";
}
"""
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test_008():
    """Test assignment to array access with float index"""
    source = """
func main() -> void {
    let arr = [1, 2, 3];
    arr[1.5] = 10;
}
"""
    expected = "Type Mismatch In Expression: ArrayAccessLValue(Identifier(arr), FloatLiteral(1.5))"
    assert Checker(source).check_from_source() == expected

def test_009():
    """Test for loop with non-array iterable"""
    source = """
func main() -> void {
    for (x in 42) {
        let y = x;
    }
}
"""
    expected = "Type Mismatch In Statement: ForStmt(x, IntegerLiteral(42), BlockStmt([VarDecl(y, Identifier(x))]))"
    assert Checker(source).check_from_source() == expected

def test_010():
    """Test for loop variable assignment inside loop"""
    source = """
func main() -> void {
    for (x in [1, 2, 3]) {
        x = 5;
    }
}
"""
    expected = "Type Mismatch In Statement: Assignment(IdLValue(x), IntegerLiteral(5))"
    assert Checker(source).check_from_source() == expected

def test_011():
    """Test for loop with correct array type inference"""
    source = """
func main() -> void {
    let arr = ["a", "b", "c"];
    for (s in arr) {
        let len = s + "suffix";
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_012():
    """Test nested for loops with same variable name"""
    source = """
func main() -> void {
    for (i in [1, 2]) {
        for (i in [3, 4]) {
            let x = i;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_013():
    """Test while loop with string condition"""
    source = """
func main() -> void {
    while ("true") {
        break;
    }
}
"""
    expected = "Type Mismatch In Statement: WhileStmt(StringLiteral('true'), BlockStmt([BreakStmt()]))"
    assert Checker(source).check_from_source() == expected

def test_014():
    """Test if statement with array condition"""
    source = """
func main() -> void {
    if ([1, 2, 3]) {
        let x = 1;
    }
}
"""
    expected = "Type Mismatch In Statement: IfStmt(condition=ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), then_stmt=BlockStmt([VarDecl(x, IntegerLiteral(1))]))"
    assert Checker(source).check_from_source() == expected

def test_015():
    """Test if with wrong condition type (should be boolean)"""
    source = """
    func main() -> void {
        if (42) {
            let x = 1;
        }
    }
    """
    expected = "Type Mismatch In Statement: IfStmt(condition=IntegerLiteral(42), then_stmt=BlockStmt([VarDecl(x, IntegerLiteral(1))]))"
    assert Checker(source).check_from_source() == expected

def test_016():
    """Test function call with too many arguments"""
    source = """
    func greet(name: string) -> void {
        return;
    }
    func main() -> void {
        greet("Alice", "Bob");
    }
    """
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(greet), [StringLiteral('Alice'), StringLiteral('Bob')]))"
    assert Checker(source).check_from_source() == expected


def test_017():
    """Test function call with mixed argument types"""
    source = """
func process(a: int, b: string, c: bool) -> void {
    return;
}
func main() -> void {
    process(1, 2, true);
}
"""
    expected = "Type Mismatch In Statement: FunctionCall(Identifier(process), [IntegerLiteral(1), IntegerLiteral(2), BooleanLiteral(True)])"
    assert Checker(source).check_from_source() == expected

def test_018():
    """Test pipe operator with wrong argument count"""
    source = """
func add(a: int, b: int) -> int {
    return a + b;
}
func main() -> void {
    let x = 5 >> add;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), >>, Identifier(add))"
    assert Checker(source).check_from_source() == expected

def test_019():
    """Test pipe operator with function call having wrong total arguments"""
    source = """
func multiply(a: int, b: int, c: int) -> int {
    return a * b * c;
}
func main() -> void {
    let x = 5 >> multiply(2);
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), >>, FunctionCall(Identifier(multiply), [IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_020():
    """Test return in main function"""
    source = """
func main() -> void {
    return 42;
}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(42))"
    assert Checker(source).check_from_source() == expected

def test_021():
    """Test function with no return statement for non-void"""
    source = """
func getValue() -> int {
    let x = 42;
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_022():
    """Test return with wrong type in nested block"""
    source = """
func compute() -> string {
    if (true) {
        return 123;
    }
    return "result";
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(123))"
    assert Checker(source).check_from_source() == expected

def test_023():
    """Test binary operation with incompatible types"""
    source = """
func main() -> void {
    let x = true + false;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(BooleanLiteral(True), +, BooleanLiteral(False))"
    assert Checker(source).check_from_source() == expected

def test_024():
    """Test modulo with float operands"""
    source = """
func main() -> void {
    let x = 5.0 % 2.0;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(FloatLiteral(5.0), %, FloatLiteral(2.0))"
    assert Checker(source).check_from_source() == expected

def test_025():
    """Test logical AND with mixed types"""
    source = """
func main() -> void {
    let x = true && 1;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(BooleanLiteral(True), &&, IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected

def test_026():
    """Test logical OR with string operands"""
    source = """
func main() -> void {
    let x = "true" || "false";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('true'), ||, StringLiteral('false'))"
    assert Checker(source).check_from_source() == expected

def test_027():
    """Test unary plus on boolean"""
    source = """
func main() -> void {
    let x = +true;
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(+, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_028():
    """Test unary minus on array"""
    source = """
func main() -> void {
    let x = -[1, 2, 3];
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(-, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))"
    assert Checker(source).check_from_source() == expected

def test_029():
    """Test empty array with explicit type"""
    source = """
func main() -> void {
    let arr: [int; 0] = [];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_030():
    """Test array size mismatch"""
    source = """
func main() -> void {
    let arr: [int; 3] = [1, 2];
}
"""
    expected = "Type Mismatch In Statement: VarDecl(arr, [int; 3], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_031():
    """Test nested array type mismatch"""
    source = """
func main() -> void {
    let arr = [[1, 2], ["a", "b"]];
}
"""
    expected = "Type Mismatch In Expression: ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([StringLiteral('a'), StringLiteral('b')])])"
    assert Checker(source).check_from_source() == expected

def test_032():
    """Test string comparison operators"""
    source = """
func main() -> void {
    let x = "apple" > "banana";
    let y = "cat" <= "dog";
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_033():
    """Test boolean comparison with ordering operators"""
    source = """
func main() -> void {
    let x = true > false;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(BooleanLiteral(True), >, BooleanLiteral(False))"
    assert Checker(source).check_from_source() == expected

def test_034():
    """Test array comparison"""
    source = """
func main() -> void {
    let x = [1, 2] == [1, 2];
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ==, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_035():
    """Test function call in expression statement with non-void return"""
    source = """
func getValue() -> int {
    return 42;
}
func main() -> void {
    getValue();
}
"""
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(getValue), []))"
    assert Checker(source).check_from_source() == expected

def test_036():
    """Test built-in str function with wrong argument type"""
    source = """
func main() -> void {
    let x = str([1, 2, 3]);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(str), [ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])])"
    assert Checker(source).check_from_source() == expected

def test_037():
    """Test built-in int function with valid string"""
    source = """
func main() -> void {
    let x = int("123");
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_038():
    """Test built-in float function with wrong argument"""
    source = """
func main() -> void {
    let x = float(true);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(float), [BooleanLiteral(True)])"
    assert Checker(source).check_from_source() == expected

def test_039():
    """Test input function with arguments"""
    source = """
func main() -> void {
    let x = input("prompt");
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(input), [StringLiteral('prompt')])"
    assert Checker(source).check_from_source() == expected

def test_040():
    """Test pipe with str function and wrong type"""
    source = """
func main() -> void {
    "hello" >> str;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('hello'), >>, Identifier(str))"
    assert Checker(source).check_from_source() == expected

def test_041():
    """Test pipe with print function"""
    source = """
func main() -> void {
    "Hello World" >> print;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_042():
    """Test chain of pipe operations"""
    source = """
func double(x: int) -> int { return x * 2; }
func toString(x: int) -> string { return str(x); }
func main() -> void {
    5 >> double >> toString >> print;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_043():
    """Test variable declaration without initialization"""
    source = """
func main() -> void {
    let x: int;
}
"""
    expected = "AST Generation Error: Variable declaration must have an initial value"
    assert Checker(source).check_from_source() == expected

def test_044():
    """Test constant declaration with array type"""
    source = """
const NUMBERS: [int; 3] = [1, 2, 3];
func main() -> void {
    let x = NUMBERS[0];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_045():
    """Test function with array parameter"""
    source = """
func sum(arr: [int; 3]) -> int {
    return arr[0] + arr[1] + arr[2];
}
func main() -> void {
    let result = sum([1, 2, 3]);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_046():
    """Test function call with wrong array size"""
    source = """
func process(arr: [int; 2]) -> void {
    return;
}
func main() -> void {
    process([1, 2, 3, 4]);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(process), [ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4)])])"
    assert Checker(source).check_from_source() == expected

def test_047():
    """Test assignment between arrays of different sizes"""
    source = """
func main() -> void {
    let arr1: [int; 2] = [1, 2];
    let arr2: [int; 3] = [3, 4, 5];
    arr1 = arr2;
}
"""
    expected = "Type Mismatch In Statement: Assignment(IdLValue(arr1), Identifier(arr2))"
    assert Checker(source).check_from_source() == expected

def test_048():
    """Test nested block variable redeclaration"""
    source = """
func main() -> void {
    let x = 1;
    {
        let y = 2;
        {
            let x = 3;
            let y = 4;
        }
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_049():
    """Test break in if statement without loop"""
    source = """
func main() -> void {
    if (true) {
        break;
    }
}
"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected

def test_050():
    """Test continue in function without loop"""
    source = """
func test() -> void {
    continue;
}
func main() -> void {}
"""
    expected = "Must In Loop: ContinueStmt()"
    assert Checker(source).check_from_source() == expected

def test_051():
    """Test function parameter with same name as function"""
    source = """
func test(test: int) -> void {
    let x = test;
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_052():
    """Test main function with parameters"""
    source = """
func main(argc: int) -> void {
    let x = argc;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_053():
    """Test main function with return type int"""
    source = """
func main() -> int {
    return 0;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_054():
    """Test multiple main functions"""
    source = """
func main() -> void {}
func main() -> void {}
"""
    expected = "Redeclared Function: main"
    assert Checker(source).check_from_source() == expected

def test_055():
    """Test assignment to array element with wrong type"""
    source = """
func main() -> void {
    let arr = [[1, 2], [3, 4]];
    arr[0][1] = "hello";
}
"""
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(ArrayAccess(Identifier(arr), IntegerLiteral(0)), IntegerLiteral(1)), StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test_056():
    """Test complex arithmetic expression type checking"""
    source = """
func main() -> void {
    let x = 1 + 2 * 3.0 - 4 / 2;
    let y: int = x;
}
"""
    expected = "Type Mismatch In Statement: VarDecl(y, int, Identifier(x))"
    assert Checker(source).check_from_source() == expected

def test_057():
    """Test division result type"""
    source = """
func main() -> void {
    let x = 10 / 3;
    let y: float = x;
}
"""
    expected = "Type Mismatch In Statement: VarDecl(y, float, Identifier(x))"
    assert Checker(source).check_from_source() == expected

def test_058():
    """Test function call as array index"""
    source = """
func getIndex() -> int {
    return 1;
}
func main() -> void {
    let arr = [10, 20, 30];
    let x = arr[getIndex()];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_059():
    """Test function call as array index with wrong return type"""
    source = """
func getIndex() -> string {
    return "1";
}
func main() -> void {
    let arr = [10, 20, 30];
    let x = arr[getIndex()];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(arr), FunctionCall(Identifier(getIndex), []))"
    assert Checker(source).check_from_source() == expected

def test_060():
    """Test nested function calls with type checking"""
    source = """
func add(a: int, b: int) -> int { return a + b; }
func multiply(a: int, b: int) -> int { return a * b; }
func main() -> void {
    let result = add(multiply(2, 3), multiply(4, 5));
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_061():
    """Test recursive function definition"""
    source = """
func factorial(n: int) -> int {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
func main() -> void {}
"""
    expected = "Undeclared Function: factorial"
    assert Checker(source).check_from_source() == expected

def test_062():
    """Test function forward declaration not allowed"""
    source = """
func helper() -> int;
func main() -> void {
    let x = helper();
}
func helper() -> int {
    return 42;
}
"""
    expected = "AST Generation Error: Function forward declaration not supported"
    assert Checker(source).check_from_source() == expected

def test_063():
    """Test array literal in function call"""
    source = """
func process(arr: [int; 3]) -> void {
    return;
}
func main() -> void {
    process([1, 2, 3]);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_064():
    """Test string concatenation in complex expression"""
    source = """
func main() -> void {
    let greeting = "Hello " + "World" + "!";
    let mixed = "Count: " + str(42);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_065():
    """Test type coercion in arithmetic with constants"""
    source = """
const INT_VAL = 42;
const FLOAT_VAL = 3.14;
func main() -> void {
    let result = INT_VAL + FLOAT_VAL;
    let x: float = result;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_066():
    """Test invalid constant assignment in nested scope"""
    source = """
const VALUE = 10;
func main() -> void {
    {
        VALUE = 20;
    }
}
"""
    expected = "Type Mismatch In Statement: Assignment(IdLValue(VALUE), IntegerLiteral(20))"
    assert Checker(source).check_from_source() == expected

def test_067():
    """Test array access on function return value"""
    source = """
func getArray() -> [int; 3] {
    return [1, 2, 3];
}
func main() -> void {
    let x = getArray()[1];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_068():
    """Test assignment to function call result"""
    source = """
func getValue() -> int {
    return 42;
}
func main() -> void {
    getValue() = 100;
}
"""
    expected = "Type Mismatch In Statement: Assignment(FunctionCall(Identifier(getValue), []), IntegerLiteral(100))"
    assert Checker(source).check_from_source() == expected

def test_069():
    """Test boolean expression in while loop"""
    source = """
func main() -> void {
    let x = 0;
    while (x < 10 && x >= 0) {
        x = x + 1;
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_070():
    """Test complex boolean expression with wrong types"""
    source = """
func main() -> void {
    let condition = 1 < 2 && "true";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(BinaryOp(IntegerLiteral(1), <, IntegerLiteral(2)), &&, StringLiteral('true'))"
    assert Checker(source).check_from_source() == expected

def test_071():
    """Test assignment to parameter in different scope"""
    source = """
func test(param: int) -> void {
    {
        param = 100;
    }
}
func main() -> void {}
"""
    expected = "Type Mismatch In Statement: Assignment(IdLValue(param), IntegerLiteral(100))"
    assert Checker(source).check_from_source() == expected

def test_072():
    """Test shadowing of parameter by local variable"""
    source = """
func test(x: int) -> void {
    let x = "shadow";
    let y = x + " variable";
}
func main() -> void {}
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected

def test_073():
    """Test array of arrays with mixed inner sizes"""
    source = """
func main() -> void {
    let arr = [[1, 2], [3, 4, 5]];
}
"""
    expected = "Type Mismatch In Expression: ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)])])"
    assert Checker(source).check_from_source() == expected

def test_074():
    """Test empty block statement"""
    source = """
func main() -> void {
    {}
    {
        {}
    }
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_075():
    """Test function call in array literal"""
    source = """
func getValue() -> int {
    return 42;
}
func main() -> void {
    let arr = [1, getValue(), 3];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_076():
    """Test pipe with built-in function having wrong arg count"""
    source = """
func main() -> void {
    5 >> print("extra");
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), >>, FunctionCall(Identifier(print), [StringLiteral('extra')]))"
    assert Checker(source).check_from_source() == expected

def test_077():
    """Test unary operators on complex expressions"""
    source = """
func main() -> void {
    let x = -(5 + 3);
    let y = !(true && false);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_078():
    """Test type annotation with wrong array element type"""
    source = """
func main() -> void {
    let arr: [string; 2] = [1, 2];
}
"""
    expected = "Type Mismatch In Statement: VarDecl(arr, [string; 2], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_079():
    """Test comparison between different numeric types"""
    source = """
func main() -> void {
    let a = 5;
    let b = 3.14;
    let result = a > b;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_080():
    """Test invalid equality comparison between incompatible types"""
    source = """
func main() -> void {
    let result = "hello" == 42;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('hello'), ==, IntegerLiteral(42))"
    assert Checker(source).check_from_source() == expected

def test_081():
    """Redeclared variable in same scope"""
    source = """
    func main() -> void {
        let x = 1;
        let x = 2;
    }
    """
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected

def test_082():
    """Redeclared parameter"""
    source = """
    func foo(x: int, x: float) -> void {}
    """
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_083():
    source = """
    func foo(x: int, x: float) -> void {}
    func main() -> void {}
    """
    expected = "Redeclared Parameter: x"
    assert Checker(source).check_from_source() == expected

def test_084():
    """Undeclared identifier"""
    source = """
    func main() -> void {
        y = 10;
    }
    """
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test_085():
    """Undeclared function"""
    source = """
    func main() -> void {
        foo();
    }
    """
    expected = "Undeclared Function: foo"
    assert Checker(source).check_from_source() == expected

def test_086():
    """Wrong number of arguments in function call"""
    source = """
    func foo(x: int, y: int) -> void {}
    func main() -> void {
        foo(1);
    }
    """
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(foo), [IntegerLiteral(1)]))"
    assert Checker(source).check_from_source() == expected

def test_087():
    """Wrong argument type in function call"""
    source = """
    func foo(x: int) -> void {}
    func main() -> void {
        foo("hello");
    }
    """
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(foo), [StringLiteral('hello')]))"
    assert Checker(source).check_from_source() == expected

def test_088():
    """Type mismatch in binary operation"""
    source = """
    func main() -> void {
        let x = 1 + "str";
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(1), +, StringLiteral('str'))"
    assert Checker(source).check_from_source() == expected

def test_089():
    """If condition is not boolean"""
    source = """
    func main() -> void {
        if (1) {
            let x = 2;
        }
    }
    """
    expected = "Type Mismatch In Statement: IfStmt(IntegerLiteral(1), BlockStmt([VarDecl(x, IntegerLiteral(2))]))"
    assert Checker(source).check_from_source() == expected

def test_090():
    """While condition is not boolean"""
    source = """
    func main() -> void {
        while (2.5) {
            let x = 2;
        }
    }
    """
    expected = "Type Mismatch In Statement: WhileStmt(FloatLiteral(2.5), BlockStmt([VarDecl(x, IntegerLiteral(2))]))"
    assert Checker(source).check_from_source() == expected

def test_091():
    """Assign wrong type to inferred variable"""
    source = """
    func main() -> void {
        let x = 1;
        x = "str";
    }
    """
    expected = "Type Mismatch In Statement: Assignment(IdLValue(x), StringLiteral('str'))"
    assert Checker(source).check_from_source() == expected

def test_092():
    """Index with non-int"""
    source = """
    func main() -> void {
        let arr = [1, 2, 3];
        let x = arr[1.2];
    }
    """
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(arr), FloatLiteral(1.2))"
    assert Checker(source).check_from_source() == expected

def test_093():
    """Assign to array element with wrong value type"""
    source = """
    func main() -> void {
        let arr = [1, 2, 3];
        arr[0] = "str";
    }
    """
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), StringLiteral('str'))"
    assert Checker(source).check_from_source() == expected

def test_094():
    """Function return type mismatch"""
    source = """
    func foo() -> int {
        return true;
    }
    """
    expected = "Type Mismatch In Statement: Return(BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_095():
    """Return value inferred to wrong type"""
    source = """
    func foo() {
        return 1;
    }
    func main() -> void {
        let x: bool = foo();
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(x, bool, FunctionCall(Identifier(foo), []))"
    assert Checker(source).check_from_source() == expected

def test_096():
    """Empty array without annotation"""
    source = """
    func main() -> void {
        let arr = [];
    }
    """
    expected = "TypeCannotBeInferred: VarDecl(arr, None, ArrayLiteral([]))"
    assert Checker(source).check_from_source() == expected

def test_097():
    """Array with inconsistent element types"""
    source = """
    func main() -> void {
        let arr = [1, "a", 3];
    }
    """
    expected = "Type Mismatch In Expression: ArrayLiteral([IntegerLiteral(1), StringLiteral('a'), IntegerLiteral(3)])"
    assert Checker(source).check_from_source() == expected

def test_098():
    """Call 'str' with unsupported argument type"""
    source = """
    func main() -> void {
        str("hello");
    }
    """
    expected = "Type Mismatch In Statement: ExprStmt(FunctionCall(Identifier(str), [StringLiteral('hello')]))"
    assert Checker(source).check_from_source() == expected

def test_099():
    """Shadowing allowed"""
    source = """
    func main() -> void {
        let x = 1;
        {
            let x = true;
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_100():
    """Redeclare function"""
    source = """
    func foo() -> void {}
    func foo(x: int) -> void {}
    """
    expected = "Redeclared Function: foo"
    assert Checker(source).check_from_source() == expected
