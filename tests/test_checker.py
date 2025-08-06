from utils import Checker

def test_101():
    """Test assignment to constant identifier"""
    source = """
const PI = 3.14;
func main() -> void {
    PI = 2.71;
}
"""
    expected = "Type Mismatch In Statement: Assignment(IdLValue(PI), FloatLiteral(2.71))"
    assert Checker(source).check_from_source() == expected

def test_102():
    """Test constant without type annotation with complex expression"""
    source = """
const RESULT = 10 + 5 * 2;
func main() -> void {
    let x = RESULT;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_103():
    """Test constant with wrong type annotation"""
    source = """
const X: string = 42;
func main() -> void {}
"""
    expected = "Type Mismatch In Expression: ConstDecl(X, string, IntegerLiteral(42))"
    assert Checker(source).check_from_source() == expected

def test_104():
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

def test_105():
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

def test_106():
    """Test array access on non-array identifier"""
    source = """
func main() -> void {
    let x = 42;
    let y = x[0];
}
"""
    expected = "Type Mismatch In Expression: ArrayAccess(Identifier(x), IntegerLiteral(0))"
    assert Checker(source).check_from_source() == expected

def test_107():
    """Test array assignment with wrong element type"""
    source = """
func main() -> void {
    let arr = [1, 2, 3];
    arr[0] = "hello";
}
"""
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(Identifier(arr), IntegerLiteral(0)), StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test_108():
    """Test assignment to array access with float index"""
    source = """
func main() -> void {
    let arr = [1, 2, 3];
    arr[1.5] = 10;
}
"""
    expected = "Type Mismatch In Expression: ArrayAccessLValue(Identifier(arr), FloatLiteral(1.5))"
    assert Checker(source).check_from_source() == expected

def test_109():
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

def test_110():
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

def test_111():
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

def test_112():
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

def test_113():
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

def test_114():
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

def test_115():
    """Test elif with wrong condition type"""
    source = """
func main() -> void {
    if (true) {
        let x = 1;
    } elif (42) {
        let y = 2;
    }
}
"""
    expected = "Type Mismatch In Statement: IfStmt(condition=BooleanLiteral(True), then_stmt=BlockStmt([VarDecl(x, IntegerLiteral(1))]), elif_branches=[(IntegerLiteral(42), BlockStmt([VarDecl(y, IntegerLiteral(2))]))])"
    assert Checker(source).check_from_source() == expected

def test_116():
    """Test function call with too many arguments"""
    source = """
func greet(name: string) -> void {
    return;
}
func main() -> void {
    greet("Alice", "Bob");
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(greet), [StringLiteral('Alice'), StringLiteral('Bob')])"
    assert Checker(source).check_from_source() == expected

def test_117():
    """Test function call with mixed argument types"""
    source = """
func process(a: int, b: string, c: bool) -> void {
    return;
}
func main() -> void {
    process(1, 2, true);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(process), [IntegerLiteral(1), IntegerLiteral(2), BooleanLiteral(True)])"
    assert Checker(source).check_from_source() == expected

def test_118():
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

def test_119():
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

def test_120():
    """Test return in main function"""
    source = """
func main() -> void {
    return 42;
}
"""
    expected = "Type Mismatch In Statement: ReturnStmt(IntegerLiteral(42))"
    assert Checker(source).check_from_source() == expected

def test_121():
    """Test function with no return statement for non-void"""
    source = """
func getValue() -> int {
    let x = 42;
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_122():
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

def test_123():
    """Test binary operation with incompatible types"""
    source = """
func main() -> void {
    let x = true + false;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(BooleanLiteral(True), +, BooleanLiteral(False))"
    assert Checker(source).check_from_source() == expected

def test_124():
    """Test modulo with float operands"""
    source = """
func main() -> void {
    let x = 5.0 % 2.0;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(FloatLiteral(5.0), %, FloatLiteral(2.0))"
    assert Checker(source).check_from_source() == expected

def test_125():
    """Test logical AND with mixed types"""
    source = """
func main() -> void {
    let x = true && 1;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(BooleanLiteral(True), &&, IntegerLiteral(1))"
    assert Checker(source).check_from_source() == expected

def test_126():
    """Test logical OR with string operands"""
    source = """
func main() -> void {
    let x = "true" || "false";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('true'), ||, StringLiteral('false'))"
    assert Checker(source).check_from_source() == expected

def test_127():
    """Test unary plus on boolean"""
    source = """
func main() -> void {
    let x = +true;
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(+, BooleanLiteral(True))"
    assert Checker(source).check_from_source() == expected

def test_128():
    """Test unary minus on array"""
    source = """
func main() -> void {
    let x = -[1, 2, 3];
}
"""
    expected = "Type Mismatch In Expression: UnaryOp(-, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]))"
    assert Checker(source).check_from_source() == expected

def test_129():
    """Test empty array with explicit type"""
    source = """
func main() -> void {
    let arr: [int; 0] = [];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_130():
    """Test array size mismatch"""
    source = """
func main() -> void {
    let arr: [int; 3] = [1, 2];
}
"""
    expected = "Type Mismatch In Statement: VarDecl(arr, [int; 3], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_131():
    """Test nested array type mismatch"""
    source = """
func main() -> void {
    let arr = [[1, 2], ["a", "b"]];
}
"""
    expected = "Type Mismatch In Expression: ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([StringLiteral('a'), StringLiteral('b')])])"
    assert Checker(source).check_from_source() == expected

def test_132():
    """Test string comparison operators"""
    source = """
func main() -> void {
    let x = "apple" > "banana";
    let y = "cat" <= "dog";
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_133():
    """Test boolean comparison with ordering operators"""
    source = """
func main() -> void {
    let x = true > false;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(BooleanLiteral(True), >, BooleanLiteral(False))"
    assert Checker(source).check_from_source() == expected

def test_134():
    """Test array comparison"""
    source = """
func main() -> void {
    let x = [1, 2] == [1, 2];
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ==, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_135():
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

def test_136():
    """Test built-in str function with wrong argument type"""
    source = """
func main() -> void {
    let x = str([1, 2, 3]);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(str), [ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])])"
    assert Checker(source).check_from_source() == expected

def test_137():
    """Test built-in int function with valid string"""
    source = """
func main() -> void {
    let x = int("123");
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_138():
    """Test built-in float function with wrong argument"""
    source = """
func main() -> void {
    let x = float(true);
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(float), [BooleanLiteral(True)])"
    assert Checker(source).check_from_source() == expected

def test_139():
    """Test input function with arguments"""
    source = """
func main() -> void {
    let x = input("prompt");
}
"""
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(input), [StringLiteral('prompt')])"
    assert Checker(source).check_from_source() == expected

def test_140():
    """Test pipe with str function and wrong type"""
    source = """
func main() -> void {
    "hello" >> str;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('hello'), >>, Identifier(str))"
    assert Checker(source).check_from_source() == expected

def test_141():
    """Test pipe with print function"""
    source = """
func main() -> void {
    "Hello World" >> print;
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_142():
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

def test_143():
    """Test variable declaration without initialization"""
    source = """
func main() -> void {
    let x: int;
}
"""
    expected = "AST Generation Error: Variable declaration must have an initial value"
    assert Checker(source).check_from_source() == expected

def test_144():
    """Test constant declaration with array type"""
    source = """
const NUMBERS: [int; 3] = [1, 2, 3];
func main() -> void {
    let x = NUMBERS[0];
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_145():
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

def test_146():
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

def test_147():
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

def test_148():
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

def test_149():
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

def test_150():
    """Test continue in function without loop"""
    source = """
func test() -> void {
    continue;
}
func main() -> void {}
"""
    expected = "Must In Loop: ContinueStmt()"
    assert Checker(source).check_from_source() == expected

def test_151():
    """Test function parameter with same name as function"""
    source = """
func test(test: int) -> void {
    let x = test;
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_152():
    """Test main function with parameters"""
    source = """
func main(argc: int) -> void {
    let x = argc;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_153():
    """Test main function with return type int"""
    source = """
func main() -> int {
    return 0;
}
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_154():
    """Test multiple main functions"""
    source = """
func main() -> void {}
func main() -> void {}
"""
    expected = "Redeclared Function: main"
    assert Checker(source).check_from_source() == expected

def test_155():
    """Test assignment to array element with wrong type"""
    source = """
func main() -> void {
    let arr = [[1, 2], [3, 4]];
    arr[0][1] = "hello";
}
"""
    expected = "Type Mismatch In Statement: Assignment(ArrayAccessLValue(ArrayAccess(Identifier(arr), IntegerLiteral(0)), IntegerLiteral(1)), StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test_156():
    """Test complex arithmetic expression type checking"""
    source = """
func main() -> void {
    let x = 1 + 2 * 3.0 - 4 / 2;
    let y: int = x;
}
"""
    expected = "Type Mismatch In Statement: VarDecl(y, int, Identifier(x))"
    assert Checker(source).check_from_source() == expected

def test_157():
    """Test division result type"""
    source = """
func main() -> void {
    let x = 10 / 3;
    let y: float = x;
}
"""
    expected = "Type Mismatch In Statement: VarDecl(y, float, Identifier(x))"
    assert Checker(source).check_from_source() == expected

def test_158():
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

def test_159():
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

def test_160():
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

def test_161():
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

def test_162():
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

def test_163():
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

def test_164():
    """Test string concatenation in complex expression"""
    source = """
func main() -> void {
    let greeting = "Hello " + "World" + "!";
    let mixed = "Count: " + str(42);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_165():
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

def test_166():
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

def test_167():
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

def test_168():
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

def test_169():
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

def test_170():
    """Test complex boolean expression with wrong types"""
    source = """
func main() -> void {
    let condition = 1 < 2 && "true";
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(BinaryOp(IntegerLiteral(1), <, IntegerLiteral(2)), &&, StringLiteral('true'))"
    assert Checker(source).check_from_source() == expected

def test_171():
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

def test_172():
    """Test shadowing of parameter by local variable"""
    source = """
func test(x: int) -> void {
    let x = "shadow";
    let y = x + " variable";
}
func main() -> void {}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_173():
    """Test array of arrays with mixed inner sizes"""
    source = """
func main() -> void {
    let arr = [[1, 2], [3, 4, 5]];
}
"""
    expected = "Type Mismatch In Expression: ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)])])"
    assert Checker(source).check_from_source() == expected

def test_174():
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

def test_175():
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

def test_176():
    """Test pipe with built-in function having wrong arg count"""
    source = """
func main() -> void {
    5 >> print("extra");
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), >>, FunctionCall(Identifier(print), [StringLiteral('extra')]))"
    assert Checker(source).check_from_source() == expected

def test_177():
    """Test unary operators on complex expressions"""
    source = """
func main() -> void {
    let x = -(5 + 3);
    let y = !(true && false);
}
"""
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_178():
    """Test type annotation with wrong array element type"""
    source = """
func main() -> void {
    let arr: [string; 2] = [1, 2];
}
"""
    expected = "Type Mismatch In Statement: VarDecl(arr, [string; 2], ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))"
    assert Checker(source).check_from_source() == expected

def test_179():
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

def test_180():
    """Test invalid equality comparison between incompatible types"""
    source = """
func main() -> void {
    let result = "hello" == 42;
}
"""
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('hello'), ==, IntegerLiteral(42))"
    assert Checker(source).check_from_source() == expected

def test_181():
    """Test function return in wrong context"""
    source = """
func compute() -> int {
    if (true) {
        let x = 5;
    } else {
        return "wrong";
    }
    return 10;
}
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected