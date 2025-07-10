from utils import ASTGenerator


def test_001a():
    """Test basic constant declaration AST generation"""
    source = "const x: int = 42;"
    expected = "Program(consts=[ConstDecl(x, int, IntegerLiteral(42))])"
    # Just check that it doesn't return an error
    assert str(ASTGenerator(source).generate()) == expected


def test_002a():
    """Test function declaration AST generation"""
    source = "func main() -> void {}"
    expected = "Program(funcs=[FuncDecl(main, [], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_003a():
    """Test function with parameters AST generation"""
    source = "func add(a: int, b: int) -> int { return a + b; }"
    expected = "Program(funcs=[FuncDecl(add, [Param(a, int), Param(b, int)], int, [ReturnStmt(BinaryOp(Identifier(a), +, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_004a():
    """Test multiple declarations AST generation"""
    source = """const PI: float = 3.14;
    func square(x: int) -> int { return x * x; }"""
    expected = "Program(consts=[ConstDecl(PI, float, FloatLiteral(3.14))], funcs=[FuncDecl(square, [Param(x, int)], int, [ReturnStmt(BinaryOp(Identifier(x), *, Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_005a():
    """Test variable declaration with type inference"""
    source = """func main() -> void { let name = "Alice"; }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(name, StringLiteral('Alice'))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_006a():
    """Test if-else statement AST generation"""
    source = """func main() -> void { 
        if (x > 0) { 
            return x;
        } else { 
            return 0;
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(condition=BinaryOp(Identifier(x), >, IntegerLiteral(0)), then_stmt=BlockStmt([ReturnStmt(Identifier(x))]), else_stmt=BlockStmt([ReturnStmt(IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_007a():
    """Test while loop AST generation"""
    source = """func main() -> void { 
        while (i < 10) { 
            i = i + 1; 
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [WhileStmt(BinaryOp(Identifier(i), <, IntegerLiteral(10)), BlockStmt([Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_008a():
    """Test array operations AST generation"""
    source = """func main() -> void { 
        let arr = [1, 2, 3];
        let first = arr[0];
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(arr, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)])), VarDecl(first, ArrayAccess(Identifier(arr), IntegerLiteral(0)))])])"
    assert str(ASTGenerator(source).generate()) == expected


def test_009a():
    """Test pipeline operator AST generation"""
    source = """func main() -> void { 
        let result = data >> process;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, BinaryOp(Identifier(data), >>, Identifier(process)))])])"
    assert str(ASTGenerator(source).generate()) == expected

# The 100 testcases below are modified by Duy Khang to complete the requirements of Assignment 2
from utils import ASTGenerator

# Tests 1-10: Basic Declarations
def test_001():
    """Test basic constant declaration"""
    source = "const x: int = 42;"
    expected = "Program(consts=[ConstDecl(x, int, IntegerLiteral(42))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_002():
    """Test constant declaration with float"""
    source = "const PI: float = 3.14159;"
    expected = "Program(consts=[ConstDecl(PI, float, FloatLiteral(3.14159))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_003():
    """Test constant declaration with string"""
    source = """const NAME: string = "Hello World";"""
    expected = """Program(consts=[ConstDecl(NAME, string, StringLiteral('Hello World'))])"""
    assert str(ASTGenerator(source).generate()) == expected

def test_004():
    """Test constant declaration with boolean true"""
    source = "const FLAG: bool = true;"
    expected = "Program(consts=[ConstDecl(FLAG, bool, BooleanLiteral(True))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_005():
    """Test constant declaration with boolean false"""
    source = "const DISABLED: bool = false;"
    expected = "Program(consts=[ConstDecl(DISABLED, bool, BooleanLiteral(False))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_006():
    """Test multiple constant declarations"""
    source = """const A: int = 10;
    const B: float = 2.5;"""
    expected = "Program(consts=[ConstDecl(A, int, IntegerLiteral(10)), ConstDecl(B, float, FloatLiteral(2.5))])"
    assert str(ASTGenerator(source).generate()) == expected

def test_007():
    """Test variable declaration with type"""
    source = """func main() -> void {
        let x: int = 5;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, int, IntegerLiteral(5))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_008():
    """Test variable declaration without initial value"""
    source = """func main() -> void {
        let x: int;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, int, None)])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_009():
    """Test variable declaration with type inference"""
    source = """func main() -> void {
        let name = "Alice";
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(name, StringLiteral('Alice'))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_010():
    """Test multiple variable declarations"""
    source = """func main() -> void {
        let x: int = 10;
        let y: float = 3.14;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, int, IntegerLiteral(10)), VarDecl(y, float, FloatLiteral(3.14))])])"
    assert str(ASTGenerator(source).generate()) == expected

# Tests 11-20: Function Declarations
def test_011():
    """Test simple function declaration"""
    source = "func main() -> void {}"
    expected = "Program(funcs=[FuncDecl(main, [], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_012():
    """Test function with single parameter"""
    source = "func square(x: int) -> int { return x * x; }"
    expected = "Program(funcs=[FuncDecl(square, [Param(x, int)], int, [ReturnStmt(BinaryOp(Identifier(x), *, Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_013():
    """Test function with multiple parameters"""
    source = "func add(a: int, b: int) -> int { return a + b; }"
    expected = "Program(funcs=[FuncDecl(add, [Param(a, int), Param(b, int)], int, [ReturnStmt(BinaryOp(Identifier(a), +, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_014():
    """Test function with mixed parameter types"""
    source = "func process(name: string, age: int, score: float) -> bool { return true; }"
    expected = "Program(funcs=[FuncDecl(process, [Param(name, string), Param(age, int), Param(score, float)], bool, [ReturnStmt(BooleanLiteral(True))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_015():
    """Test function returning different types"""
    source = """func getName() -> string { return "John"; }"""
    expected = "Program(funcs=[FuncDecl(getName, [], string, [ReturnStmt(StringLiteral('John'))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_016():
    """Test function with array parameter"""
    source = "func sum(arr: int[5]) -> int { return 0; }"
    expected = "Program(funcs=[FuncDecl(sum, [Param(arr, ArrayType(int, 5))], int, [ReturnStmt(IntegerLiteral(0))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_017():
    """Test function with multiple array parameters"""
    source = "func merge(a: int[3], b: float[2]) -> void {}"
    expected = "Program(funcs=[FuncDecl(merge, [Param(a, ArrayType(int, 3)), Param(b, ArrayType(float, 2))], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_018():
    """Test multiple function declarations"""
    source = """func add(x: int, y: int) -> int { return x + y; }
    func multiply(x: int, y: int) -> int { return x * y; }"""
    expected = "Program(funcs=[FuncDecl(add, [Param(x, int), Param(y, int)], int, [ReturnStmt(BinaryOp(Identifier(x), +, Identifier(y)))]), FuncDecl(multiply, [Param(x, int), Param(y, int)], int, [ReturnStmt(BinaryOp(Identifier(x), *, Identifier(y)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_019():
    """Test function with complex body"""
    source = """func calculate(x: int) -> int {
        let result: int = x * 2;
        return result + 1;
    }"""
    expected = "Program(funcs=[FuncDecl(calculate, [Param(x, int)], int, [VarDecl(result, int, BinaryOp(Identifier(x), *, IntegerLiteral(2))), ReturnStmt(BinaryOp(Identifier(result), +, IntegerLiteral(1)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_020():
    """Test function with empty return"""
    source = """func doSomething() -> void {
        return;
    }"""
    expected = "Program(funcs=[FuncDecl(doSomething, [], void, [ReturnStmt(None)])])"
    assert str(ASTGenerator(source).generate()) == expected

# Tests 21-30: Type System
def test_021():
    """Test all primitive types"""
    source = """func test(a: int, b: float, c: bool, d: string) -> void {}"""
    expected = "Program(funcs=[FuncDecl(test, [Param(a, int), Param(b, float), Param(c, bool), Param(d, string)], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_022():
    """Test 2D array (matrix): 2 rows, 3 columns each"""
    source = """func test() -> void {
        let matrix: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];
    }"""
    expected = "Program(funcs=[FuncDecl(test, [], void, [VarDecl(matrix, [[int; 3]; 2], ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3)]), ArrayLiteral([IntegerLiteral(4), IntegerLiteral(5), IntegerLiteral(6)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_023():
    """Test 3D array: 2 layers, 3 rows, 4 columns each"""
    source = """func test() -> void {
        let cube: [[[int; 4]; 3]; 2] = [
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
            [[13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]
        ];
    }"""
    expected = "Program(funcs=[FuncDecl(test, [], void, [VarDecl(cube, [[[int; 4]; 3]; 2], ArrayLiteral([ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4)]), ArrayLiteral([IntegerLiteral(5), IntegerLiteral(6), IntegerLiteral(7), IntegerLiteral(8)]), ArrayLiteral([IntegerLiteral(9), IntegerLiteral(10), IntegerLiteral(11), IntegerLiteral(12)])]), ArrayLiteral([ArrayLiteral([IntegerLiteral(13), IntegerLiteral(14), IntegerLiteral(15), IntegerLiteral(16)]), ArrayLiteral([IntegerLiteral(17), IntegerLiteral(18), IntegerLiteral(19), IntegerLiteral(20)]), ArrayLiteral([IntegerLiteral(21), IntegerLiteral(22), IntegerLiteral(23), IntegerLiteral(24)])])]))])])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_024():
    """Test jagged arrays (arrays of different-sized arrays)"""
    source = """func test() -> void {
        let jagged: [[int; 2]; 3] = [[1, 2], [3, 4], [5, 6]];
    }"""
    expected = "Program(funcs=[FuncDecl(test, [], void, [VarDecl(jagged, [[int; 2]; 3], ArrayLiteral([ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]), ArrayLiteral([IntegerLiteral(3), IntegerLiteral(4)]), ArrayLiteral([IntegerLiteral(5), IntegerLiteral(6)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_025():
    """Test mixed type multidimensional arrays"""
    source = """func test() -> void {
        let mixed: [[float; 2]; 2] = [[1.5, 2.5], [3.5, 4.5]];
    }"""
    expected = "Program(funcs=[FuncDecl(test, [], void, [VarDecl(mixed, [[float; 2]; 2], ArrayLiteral([ArrayLiteral([FloatLiteral(1.5), FloatLiteral(2.5)]), ArrayLiteral([FloatLiteral(3.5), FloatLiteral(4.5)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_026():
    """Test large array size"""
    source = "func test(arr: int[100]) -> void {}"
    expected = "Program(funcs=[FuncDecl(test, [Param(arr, ArrayType(int, 100))], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_027():
    """Test array size 1"""
    source = "func test(arr: int[1]) -> void {}"
    expected = "Program(funcs=[FuncDecl(test, [Param(arr, ArrayType(int, 1))], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_028():
    """Test multiple array types"""
    source = "func test(a: int[5], b: float[3], c: bool[2]) -> void {}"
    expected = "Program(funcs=[FuncDecl(test, [Param(a, ArrayType(int, 5)), Param(b, ArrayType(float, 3)), Param(c, ArrayType(bool, 2))], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_029():
    """Test void return type"""
    source = "func test() -> void {}"
    expected = "Program(funcs=[FuncDecl(test, [], void, [])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_030():
    """Test optional type specification"""
    source = """func main() -> void {
        let x = 42;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(x, None, IntegerLiteral(42))])])"
    assert str(ASTGenerator(source).generate()) == expected

# Tests 31-40: Statements
def test_031():
    """Test simple assignment"""
    source = """func main() -> void {
        x = 10;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [Assignment(IdLValue(x), IntegerLiteral(10))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_032():
    """Test array element assignment"""
    source = """func main() -> void {
        arr[0] = 42;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [Assignment(ArrayAccess(Identifier(arr), IntegerLiteral(0)), IntegerLiteral(42))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_033():
    """Test multi-dimensional array assignment"""
    source = """func main() -> void {
        matrix[1][2] = 5;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [Assignment(ArrayAccess(ArrayAccess(Identifier(matrix), IntegerLiteral(1)), IntegerLiteral(2)), IntegerLiteral(5))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_034():
    """Test if statement"""
    source = """func main() -> void {
        if (x > 0) {
            return x;
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(BinaryOp(Identifier(x), >, IntegerLiteral(0)), BlockStmt([ReturnStmt(Identifier(x))]), [], None)])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_035():
    """Test if-else statement"""
    source = """func main() -> void {
        if (x > 0) {
            return x;
        } else {
            return 0;
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(BinaryOp(Identifier(x), >, IntegerLiteral(0)), BlockStmt([ReturnStmt(Identifier(x))]), [], BlockStmt([ReturnStmt(IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_036():
    """Test if-elseif-else statement"""
    source = """func main() -> void {
        if (x > 0) {
            return 1;
        } else if (x < 0) {
            return -1;
        } else {
            return 0;
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [IfStmt(BinaryOp(Identifier(x), >, IntegerLiteral(0)), BlockStmt([ReturnStmt(IntegerLiteral(1))]), [(BinaryOp(Identifier(x), <, IntegerLiteral(0)), BlockStmt([ReturnStmt(IntegerLiteral(-1))]))], BlockStmt([ReturnStmt(IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_037():
    """Test while loop"""
    source = """func main() -> void {
        while (i < 10) {
            i = i + 1;
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [WhileStmt(BinaryOp(Identifier(i), <, IntegerLiteral(10)), BlockStmt([Assignment(IdLValue(i), BinaryOp(Identifier(i), +, IntegerLiteral(1)))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_038():
    """Test for loop"""
    source = """func main() -> void {
        for (item in collection) {
            print(item);
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ForStmt(item, Identifier(collection), BlockStmt([ExprStmt(FunctionCall(Identifier(print), [Identifier(item)]))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_039():
    """Test break statement"""
    source = """func main() -> void {
        while (true) {
            break;
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [WhileStmt(BooleanLiteral(true), BlockStmt([BreakStmt()]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_040():
    """Test continue statement"""
    source = """func main() -> void {
        for (i in range) {
            continue;
        }
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [ForStmt(i, Identifier(range), BlockStmt([ContinueStmt()]))])])"
    assert str(ASTGenerator(source).generate()) == expected

# Tests 41-50: Expression Operations
def test_041():
    """Test arithmetic addition"""
    source = """func main() -> void {
        let result = a + b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), +, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_042():
    """Test arithmetic subtraction"""
    source = """func main() -> void {
        let result = a - b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), -, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_043():
    """Test arithmetic multiplication"""
    source = """func main() -> void {
        let result = a * b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), *, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_044():
    """Test arithmetic division"""
    source = """func main() -> void {
        let result = a / b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), /, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_045():
    """Test arithmetic modulo"""
    source = """func main() -> void {
        let result = a % b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), %, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_046():
    """Test comparison equal"""
    source = """func main() -> void {
        let result = a == b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), ==, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_047():
    """Test comparison not equal"""
    source = """func main() -> void {
        let result = a != b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), !=, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_048():
    """Test comparison less than"""
    source = """func main() -> void {
        let result = a < b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), <, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_049():
    """Test comparison greater than"""
    source = """func main() -> void {
        let result = a > b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), >, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_050():
    """Test comparison less than or equal"""
    source = """func main() -> void {
        let result = a <= b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), <=, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

# Tests 51-60: Complex Expressions
def test_051():
    """Test comparison greater than or equal"""
    source = """func main() -> void {
        let result = a >= b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), >=, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_052():
    """Test logical AND"""
    source = """func main() -> void {
        let result = a && b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), &&, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_053():
    """Test logical OR"""
    source = """func main() -> void {
        let result = a || b;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(Identifier(a), ||, Identifier(b)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_054():
    """Test unary negation"""
    source = """func main() -> void {
        let result = -x;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, UnaryOp(-, Identifier(x)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_055():
    """Test unary logical NOT"""
    source = """func main() -> void {
        let result = !flag;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, UnaryOp(!, Identifier(flag)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_056():
    """Test complex arithmetic expression"""
    source = """func main() -> void {
        let result = a + b * c - d / e;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(BinaryOp(Identifier(a), +, BinaryOp(Identifier(b), *, Identifier(c))), -, BinaryOp(Identifier(d), /, Identifier(e))))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_057():
    """Test parenthesized expression"""
    source = """func main() -> void {
        let result = (a + b) * c;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), *, Identifier(c)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_058():
    """Test nested parentheses"""
    source = """func main() -> void {
        let result = ((a + b) * c) / d;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), *, Identifier(c)), /, Identifier(d)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_059():
    """Test mixed logical and arithmetic"""
    source = """func main() -> void {
        let result = (a + b) > c && d < e;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, BinaryOp(BinaryOp(BinaryOp(Identifier(a), +, Identifier(b)), >, Identifier(c)), &&, BinaryOp(Identifier(d), <, Identifier(e))))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_060():
    """Test multiple unary operators"""
    source = """func main() -> void {
        let result = --x;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, None, UnaryOp(-, UnaryOp(-, Identifier(x))))])])"
    assert str(ASTGenerator(source).generate()) == expected

# Tests 61-70: Arrays and Function Calls
def test_061():
    """Test array literal"""
    source = """func main() -> void {
        let arr = [1, 2, 3, 4, 5];
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(arr, None, ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2), IntegerLiteral(3), IntegerLiteral(4), IntegerLiteral(5)]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_062():
    """Test empty array literal"""
    source = """func main() -> void {
        let arr = [];
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(arr, None, ArrayLiteral([]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_063():
    """Test array access"""
    source = """func main() -> void {
        let element = arr[0];
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(element, None, ArrayAccess(Identifier(arr), IntegerLiteral(0)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_064():
    """Test multi-dimensional array access"""
    source = """func main() -> void {
        let element = matrix[1][2];
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(element, None, ArrayAccess(ArrayAccess(Identifier(matrix), IntegerLiteral(1)), IntegerLiteral(2)))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_065():
    """Test function call with no arguments"""
    source = """func main() -> void {
        let result = getValue();
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, FunctionCall(Identifier(getValue), []))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_066():
    """Test function call with single argument"""
    source = """func main() -> void {
        let result = square(5);
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, FunctionCall(Identifier(square), [IntegerLiteral(5)]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_067():
    """Test function call with multiple arguments"""
    source = """func main() -> void {
        let result = add(10, 20);
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, FunctionCall(Identifier(add), [IntegerLiteral(10), IntegerLiteral(20)]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_068():
    """Test nested function calls"""
    source = """func main() -> void {
        let result = add(square(3), multiply(2, 4));
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, FunctionCall(Identifier(add), [FunctionCall(Identifier(square), [IntegerLiteral(3)]), FunctionCall(Identifier(multiply), [IntegerLiteral(2), IntegerLiteral(4)])]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_069():
    """Test function call with array access"""
    source = """func main() -> void {
        let result = process(arr[0]);
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, FunctionCall(Identifier(process), [ArrayAccess(Identifier(arr), IntegerLiteral(0))]))])])"
    assert str(ASTGenerator(source).generate()) == expected

def test_070():
    """Test array of function calls"""
    source = """func main() -> void {
        let arr = [getValue(), getValue(), getValue()];
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(arr, ArrayLiteral([FunctionCall(Identifier(getValue), []), FunctionCall(Identifier(getValue), []), FunctionCall(Identifier(getValue), [])]))])])"
    assert str(ASTGenerator(source).generate()) == expected

# Tests 71-80: Pipeline Operations
def test_071():
    """Test simple pipeline"""
    source = """func main() -> void {
        let result = data >> process;
    }"""
    expected = "Program(funcs=[FuncDecl(main, [], void, [VarDecl(result, BinaryOp(Identifier(data), >>, Identifier(process)))])])"
    assert str(ASTGenerator(source).generate()) == expected