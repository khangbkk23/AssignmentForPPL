from utils import Checker


def test_001a():
    """Test a valid program that should pass all checks"""
    source = """
const PI: float = 3.14;
func main() -> void {
    let x: int = 5;
    let y = x + 1;
};
"""
    expected = "Static checking passed"
    # Just check that it doesn't return an error
    assert Checker(source).check_from_source() == expected

def test_002a():
    """Test redeclared variable error"""
    source = """
func main() -> void {
    let x: int = 5;
    let x: int = 10;
};
"""
    expected = "Redeclared Variable: x"
    assert Checker(source).check_from_source() == expected

def test_003a():
    """Test undeclared identifier error"""
    source = """
func main() -> void {
    let x = y + 1;
};
"""
    expected = "Undeclared Identifier: y"
    assert Checker(source).check_from_source() == expected

def test_004a():
    """Test type mismatch error"""
    source = """
func main() -> void {
    let x: int = "hello";
};
"""
    expected = "Type Mismatch In Statement: VarDecl(x, int, StringLiteral('hello'))"
    assert Checker(source).check_from_source() == expected

def test_005a():
    """Test no main function error"""
    source = """
func hello() -> void {
    let x: int = 5;
};
"""
    expected = "No Entry Point"
    assert Checker(source).check_from_source() == expected

def test_006a():
    """Test break not in loop error"""
    source = """
func main() -> void {
    break;
};
"""
    expected = "Must In Loop: BreakStmt()"
    assert Checker(source).check_from_source() == expected


    """
    =============================================================================================
    """
    def test_000():
    """Pipeline lồng với biểu thức tính toán"""
    source = """
    func double(x: int) -> int { return x * 2; }
    func toStr(x: int) -> string { return "v=" + "x"; }

    func main() -> void {
        let result = (1 + 2 * 3) >> double >> toStr;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_001():
    """Nested if-else if-else with shadowed return"""
    source = """
    func check(x: int) -> int {
        if (x > 0) {
            if (x > 100) {
                return 1;
            } else if (x > 50) {
                return 2;
            } else {
                return 3;
            }
        } else {
            return 0;
        }
    }

    func main() -> void {
        let r = check(99);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_002():
    """Pipeline nested in another function call"""
    source = """
    func inc(x: int) -> int { return x + 1; }
    func add(x: int, y: int) -> int { return x + y; }

    func main() -> void {
        let r = add(inc(1 >> inc), 5);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_003():
    """Function with early returns in loops"""
    source = """
    func firstEven(arr: [int; 5]) -> int {
        for (x in arr) {
            if (x % 2 == 0) {
                return x;
            }
        }
        return -1;
    }

    func main() -> void {
        let a = [1, 3, 5, 8, 9];
        let r = firstEven(a);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_004():
    """Function with recursive call in loop"""
    source = """
    func fact(n: int) -> int {
        if (n == 0) { return 1; }
        return n * fact(n - 1);
    }

    func main() -> void {
        for (i in [1, 2, 3]) {
            let x = fact(i);
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_005():
    """Pipeline with function returning array"""
    source = """
    func build() -> [int; 3] { return [4, 5, 6]; }
    func sum3(arr: [int; 3]) -> int { return arr[0] + arr[1] + arr[2]; }

    func main() -> void {
        let r = build() >> sum3;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_006():
    """Shadow const with variable"""
    source = """
    const PI: float = 3.14;
    func main() -> void {
        let PI: int = 10;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_007():
    """Variable declared then shadowed inside if"""
    source = """
    func main() -> void {
        let x = 1;
        if (true) {
            let x = 2;
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_008():
    """Pipeline with return inside loop body"""
    source = """
    func shout(s: string) -> string { return s + "!"; }
    func toUpper(s: string) -> string { return s; }

    func process(words: [string; 3]) -> string {
        for (w in words) {
            return w >> toUpper >> shout;
        }
        return "";
    }

    func main() -> void {
        let w = ["a", "b", "c"];
        let result = process(w);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_009():
    """Using break to skip return in some path"""
    source = """
    func f(x: int) -> int {
        while (true) {
            break;
        }
        return x;
    }
    func main() -> void {
        let x = f(1);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_010():
    """Nested pipeline with mixed arguments"""
    source = """
    func add(x: int, y: int) -> int { return x + y; }
    func double(x: int) -> int { return x * 2; }

    func main() -> void {
        let r = 5 >> add(3) >> double;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_011():
    """Recursive fibonacci with if-else return"""
    source = """
    func fib(n: int) -> int {
        if (n <= 1) { return n; }
        return fib(n-1) + fib(n-2);
    }

    func main() -> void {
        let x = fib(5);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_012():
    """Return only in some if branches"""
    source = """
    func check(x: int) -> int {
        if (x == 0) {
            return 0;
        } else if (x == 1) {
            return 1;
        } else {
            return 2;
        }
    }

    func main() -> void {
        let r = check(2);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_013():
    """Nested function definitions and calls"""
    source = """
    func square(x: int) -> int { return x * x; }
    func add(x: int, y: int) -> int { return x + y; }

    func main() -> void {
        let result = square(add(2, 3));
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_014():
    """Pipeline with function returning float"""
    source = """
    func toFloat(x: int) -> float { return 1.0 * x; }
    func half(x: float) -> float { return x / 2.0; }

    func main() -> void {
        let result = 10 >> toFloat >> half;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_015():
    """Function returning array passed to another"""
    source = """
    func gen() -> [int; 3] { return [1, 2, 3]; }
    func sum(a: [int; 3]) -> int { return a[0] + a[1] + a[2]; }

    func main() -> void {
        let s = gen() >> sum;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_016():
    """Early return inside while loop with condition"""
    source = """
    func findEven(arr: [int; 4]) -> int {
        let i = 0;
        while (i < 4) {
            if (arr[i] % 2 == 0)  { return arr[i]; }
            i = i + 1;
        }
        return -1;
    }

    func main() -> void {
        let a = [1, 3, 5, 6];
        let r = findEven(a);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_017():
    """Multiple shadowing in different scopes"""
    source = """
    func main() -> void {
        let x = 1;
        if (true) {
            let x = 2;
            if (true) {
                let x = 3;
            }
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_018():
    """Break and return inside nested loop"""
    source = """
    func find() -> int {
        for (x in [1,2,3]) {
            while (true) {
                break;
            }
        }
        return 0;
    }

    func main() -> void {
        let r = find();
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_019():
    """Pipeline with string transformation chain"""
    source = """
    func trim(s: string) -> string { return s; }
    func upper(s: string) -> string { return s; }
    func addDot(s: string) -> string { return s + "."; }

    func main() -> void {
        let s = " hello " >> trim >> upper >> addDot;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_020():
    """Function with all return in nested if/else"""
    source = """
    func complex(x: int) -> int {
        if (x < 0) {
            return -1;
        } else {
            if (x == 0) {
                return 0;
            } else {
                return 1;
            }
        }
    }

    func main() -> void {
        let r = complex(10);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_021():
    """Pipeline using function call with multiple params"""
    source = """
    func join(a: string, b: string) -> string { return a + b; }

    func main() -> void {
        let result = "Hi" >> join("!");
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_022():
    """Array access with type match and bounds check"""
    source = """
    func main() -> void {
        let a = [10, 20, 30];
        let x: int = a[1];
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_023():
    """Return only in else branch should raise error"""
    source = """
    func f(x: int) -> int {
        if (x > 0) {
        } else {
            return x;
        }
    }

    func main() -> void {
        let r = f(3);
    }
    """
    expected = "Type Mismatch In Statement: FuncDecl(f, [Param(x, int)], int, [IfStmt(condition=BinaryOp(Identifier(x), >, IntegerLiteral(0)), then_stmt=BlockStmt([]), else_stmt=BlockStmt([ReturnStmt(Identifier(x))]))])"
    assert Checker(source).check_from_source() == expected

def test_024():
    """Function returning void used in pipeline should fail"""
    source = """
    func say(x: string) -> void {}

    func main() -> void {
        let r = "hi" >> say;
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(r, BinaryOp(StringLiteral('hi'), >>, Identifier(say)))"
    assert Checker(source).check_from_source() == expected

def test_025():
    """Array element assign with wrong type"""
    source = """
    func main() -> void {
        let a: [int; 3] = [1, 2, 3];
        a[1] = "hello";
    }
    """
    expected = "Type Mismatch In Statement: Assignment(..."
    assert Checker(source).check_from_source().startswith("Type Mismatch In Statement")

def test_026():
    """Recursive even check with modulo"""
    source = """
    func even(x: int) -> bool {
        if (x == 0) { return true; }
        if (x == 1) { return false; }
        return even(x - 2);
    }

    func main() -> void {
        let r = even(4);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_027():
    """Pipeline chain with inferred types"""
    source = """
    func plus1(x: int) -> int { return x + 1; }
    func times3(x: int) -> int { return x * 3; }

    func main() -> void {
        let result = 4 >> plus1 >> times3;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_028():
    """Deeply nested if-else with returns"""
    source = """
    func classify(x: int) -> string {
        if (x > 0) {
            if (x < 10) { return "small"; }
            else { return "large"; }
        } else {
            return "non-positive";
        }
    }

    func main() -> void {
        let c = classify(5);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_029():
    """Array passed into pipeline function"""
    source = """
    func sum3(arr: [int; 3]) -> int { return arr[0] + arr[1] + arr[2]; }

    func main() -> void {
        let x = [10, 20, 30] >> sum3;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_030():
    """Pipeline with nested calls and binary op"""
    source = """
    func mul(x: int, y: int) -> int { return x * y; }
    func inc(x: int) -> int { return x + 1; }
    func main() -> void {
        let r = (2 + 3) >> inc >> mul(2);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_031():
    """Recursive factorial with condition"""
    source = """
    func fact(n: int) -> int {
        if (n <= 1) {
            return 1;
        } else {
            return n * fact(n - 1);
        }
    }

    func main() -> void {
        let x = fact(5);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_032():
    """Pipeline with function expecting array as 1st param"""
    source = """
    func get(arr: [int; 3], idx: int) -> int { return arr[idx]; }

    func main() -> void {
        let arr = [1,2,3];
        let x = arr >> get(2);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_033():
    """Early return from nested while with if"""
    source = """
    func find5(arr: [int; 5]) -> int {
        let i = 0;
        while (i < 5) {
            if (arr[i] == 5) {
                return 5;
            }
            i = i + 1;
        }
        return -1;
    }

    func main() -> void {
        let a = [1,2,3,4,5];
        let r = find5(a);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_034():
    """Nested loop, break, and return"""
    source = """
    func main() -> void {
        for (x in [1,2,3]) {
            while (true) {
                break;
            }
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_035():
    """Multiple if-else returns"""
    source = """
    func classify(n: int) -> string {
        if (n < 0) {
            return "negative";
        } else if (n == 0) {
            return "zero";
        } else {
            return "positive";
        }
    }

    func main() -> void {
        let s = classify(5);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_036():
    """Deep pipeline with mix of types"""
    source = """
    func toStr(x: int) -> string { return "v=" + "x"; }
    func addDot(s: string) -> string { return s + "."; }

    func main() -> void {
        let r = 100 >> toStr >> addDot;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_037():
    """Shadow parameter in inner block"""
    source = """
    func f(x: int) -> int {
        if (true) {
            let x = 10;
            return x;
        } else {
            return 0;
        }
    }

    func main() -> void {
        let r = f(1);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_038():
    """If-else chain with only one return (should fail)"""
    source = """
    func f(x: int) -> int {
        if (x > 0) {
            return x;
        }
    }

    func main() -> void {
        let x = f(2);
    }
    """
    expected = "Type Mismatch In Statement: FuncDecl(f, ..."
    assert Checker(source).check_from_source().startswith("Type Mismatch In Statement")

def test_039():
    """Function with no return (should fail)"""
    source = """
    func f(x: int) -> int {}

    func main() -> void {
        let x = f(1);
    }
    """
    expected = "Type Mismatch In Statement: FuncDecl(f, ..."
    assert Checker(source).check_from_source().startswith("Type Mismatch In Statement")

def test_040():
    """Function with return inside for loop with condition"""
    source = """
    func containsZero(arr: [int; 3]) -> bool {
        for (x in arr) {
            if (x == 0) {
                return true;
            }
        }
        return false;
    }

    func main() -> void {
        let result = containsZero([0,1,2]);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_041():
    """Multiple function calls with correct args"""
    source = """
    func f(x: int) -> int { return x * 2; }
    func g(x: int) -> int { return f(x) + 1; }

    func main() -> void {
        let r = g(3);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_042():
    """Pass function return into pipeline"""
    source = """
    func base() -> int { return 5; }
    func double(x: int) -> int { return x * 2; }

    func main() -> void {
        let r = base() >> double;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_043():
    """Invalid pipeline target (not function)"""
    source = """
    func main() -> void {
        let x = 5 >> 10;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(5), >>, IntegerLiteral(10))"
    assert Checker(source).check_from_source() == expected

def test_044():
    """Function with inferred return from nested ifs"""
    source = """
    func f(x: int) -> int {
        if (x > 10) {
            if (x < 20) {
                return x;
            } else {
                return x * 2;
            }
        } else {
            return -1;
        }
    }

    func main() -> void {
        let y = f(15);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_045():
    """Function using multiple return types (should fail)"""
    source = """
    func f(x: int) -> int {
        if (x > 0) {
            return x;
        } else {
            return "wrong";
        }
    }

    func main() -> void {
        let y = f(1);
    }
    """
    expected = "Type Mismatch In Statement: ReturnStmt(StringLiteral('wrong'))"
    assert Checker(source).check_from_source() == expected

def test_046():
    """Pipeline chain with functions of different return types"""
    source = """
    func intToStr(x: int) -> string { return "n=" + "x"; }
    func shout(s: string) -> string { return s + "!"; }

    func main() -> void {
        let r = 9 >> intToStr >> shout;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_047():
    """Void function in middle of pipeline (should fail)"""
    source = """
    func speak(x: string) -> void {}
    func up(s: string) -> string { return s; }

    func main() -> void {
        let r = "hi" >> speak >> up;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(BinaryOp(StringLiteral('hi'), >>, Identifier(speak)), >>, Identifier(up))"
    assert Checker(source).check_from_source() == expected

def test_048():
    """Complex nested if-else return mix"""
    source = """
    func choose(x: int) -> int {
        if (x < 0) {
            return -1;
        } else {
            if (x % 2 == 0) {
                return 0;
            } else {
                return 1;
            }
        }
    }

    func main() -> void {
        let y = choose(3);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_049():
    """Function returning wrong type in pipeline (should fail)"""
    source = """
    func f(x: int) -> bool { return true; }
    func g(x: int) -> int { return x + 1; }

    func main() -> void {
        let r = 5 >> f >> g;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(BinaryOp(IntegerLiteral(5), >>, Identifier(f)), >>, Identifier(g))"
    assert Checker(source).check_from_source() == expected

def test_050():
    """Multiple shadowed variables and nested scopes"""
    source = """
    func main() -> void {
        let x = 1;
        if (true) {
            let x = 2;
            while (true) {
                let x = 3;
                break;
            }
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_051():
    """Recursive even check with bool return"""
    source = """
    func isEven(n: int) -> bool {
        if (n == 0) {
            return true;
        } else if (n == 1) {
            return false;
        } else {
            return isEven(n - 2);
        }
    }

    func main() -> void {
        let res = isEven(6);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_052():
    """Pipeline with mixed literal and call expressions"""
    source = """
    func wrap(x: string) -> string { return "[" + x + "]"; }
    func main() -> void {
        let s = ("hello" + "!") >> wrap;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_053():
    """Loop with return and break mixed"""
    source = """
    func findFirstEven(arr: [int; 4]) -> int {
        for (x in arr) {
            if (x % 2 == 0) {
                return x;
            }
            break;
        }
        return -1;
    }

    func main() -> void {
        let a = [1,3,4,5];
        let r = findFirstEven(a);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_054():
    """Pipeline with function returning array"""
    source = """
    func gen() -> [int; 2] { return [7, 8]; }
    func sum2(a: [int; 2]) -> int { return a[0] + a[1]; }

    func main() -> void {
        let result = gen() >> sum2;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_055():
    """Nested return in if-else, missing else (should fail)"""
    source = """
    func f(x: int) -> int {
        if (x > 0) {
            if (x < 5) {
                return 1;
            }
        } else {
            return -1;
        }
    }

    func main() -> void {
        let r = f(2);
    }
    """
    expected = "Type Mismatch In Statement: FuncDecl(f, ..."
    assert Checker(source).check_from_source().startswith("Type Mismatch In Statement")

def test_056():
    """Function returning string through pipeline chain"""
    source = """
    func step1(x: int) -> string { return "v=" + "x"; }
    func step2(s: string) -> string { return s + "!"; }

    func main() -> void {
        let r = 3 >> step1 >> step2;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_057():
    """Wrong number of args in pipeline call (should fail)"""
    source = """
    func add(x: int, y: int) -> int { return x + y; }

    func main() -> void {
        let r = 3 >> add;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(IntegerLiteral(3), >>, Identifier(add))"
    assert Checker(source).check_from_source() == expected

def test_058():
    """Recursive fibonacci with correct return logic"""
    source = """
    func fib(n: int) -> int {
        if (n <= 1) {
            return n;
        } else {
            return fib(n-1) + fib(n-2);
        }
    }

    func main() -> void {
        let x = fib(6);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_059():
    """Return value from nested pipeline computation"""
    source = """
    func times2(x: int) -> int { return x * 2; }
    func str(x: int) -> string { return "n=" + "x"; }

    func main() -> void {
        let r = (1 + 2) >> times2 >> str;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_060():
    """Recursive factorial with check"""
    source = """
    func fact(n: int) -> int {
        if (n == 0) { return 1; }
        return n * fact(n - 1);
    }

    func main() -> void {
        let r = fact(4);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_061():
    """Shadowing in loop and if block"""
    source = """
    func main() -> void {
        let x = 1;
        for (x in [2,3]) {
            if (true) {
                let x = 5;
            }
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_062():
    """Invalid: void return type used in expression"""
    source = """
    func speak(msg: string) -> void {}
    func main() -> void {
        let x = "hi" >> speak;
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(x, BinaryOp(StringLiteral('hi'), >>, Identifier(speak)))"
    assert Checker(source).check_from_source() == expected

def test_063():
    """Multiple break inside nested loops"""
    source = """
    func main() -> void {
        for (i in [1,2,3]) {
            while (true) {
                if (i > 1) { break; }
            }
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_064():
    """Deep nested pipeline with math"""
    source = """
    func inc(x: int) -> int { return x + 1; }
    func sqr(x: int) -> int { return x * x; }

    func main() -> void {
        let result = ((1 + 2) * 3) >> inc >> sqr;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_065():
    """Call function with wrong number of args"""
    source = """
    func sum(x: int, y: int) -> int { return x + y; }

    func main() -> void {
        let a = sum(1);
    }
    """
    expected = "Type Mismatch In Expression: FunctionCall(Identifier(sum), [IntegerLiteral(1)])"
    assert Checker(source).check_from_source() == expected

def test_066():
    """Assign void return value to variable"""
    source = """
    func say(s: string) -> void {}

    func main() -> void {
        let x: void = say("hello");
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(x, void, FunctionCall(Identifier(say), [StringLiteral('hello')]))"
    assert Checker(source).check_from_source() == expected

def test_067():
    """Pipeline chaining with multiple params"""
    source = """
    func add(x: int, y: int) -> int { return x + y; }
    func mul(x: int) -> int { return x * 2; }

    func main() -> void {
        let res = 4 >> add(3) >> mul;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_068():
    """Return only in inner else branch (should fail)"""
    source = """
    func test(x: int) -> int {
        if (x > 0) {
            if (x < 10) {}
            else { return 1; }
        } else {
            return 0;
        }
    }

    func main() -> void {
        let y = test(3);
    }
    """
    expected = "Type Mismatch In Statement: FuncDecl(test, [Param(x, int)], int, [...])"
    assert Checker(source).check_from_source().startswith("Type Mismatch In Statement")

def test_069():
    """Correct function with nested condition return"""
    source = """
    func test(x: int) -> int {
        if (x > 0) {
            if (x > 5) { return 1; }
            else { return 2; }
        } else {
            return 0;
        }
    }

    func main() -> void {
        let r = test(7);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_070():
    """Nested if-else with return in all paths"""
    source = """
    func grade(score: int) -> string {
        if (score >= 90) { return "A"; }
        else {
            if (score >= 80) { return "B"; }
            else if (score >= 70) { return "C"; }
            else { return "F"; }
        }
    }
    func main() -> void {
        let g = grade(85);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_071():
    """Function computing max of array"""
    source = """
    func max(arr: [int; 5]) -> int {
        let m = arr[0];
        for (x in arr) {
            if (x > m) { m = x; }
        }
        return m;
    }
    func main() -> void {
        let a = [3, 8, 2, 7, 4];
        let r = max(a);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_072():
    """Multi-param function in pipeline"""
    source = """
    func wrap(s: string, pre: string, post: string) -> string {
        return pre + s + post;
    }
    func main() -> void {
        let r = "msg" >> wrap("[", "]");
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_073():
    """Incorrect type in pipeline (should fail)"""
    source = """
    func double(x: int) -> int { return x * 2; }
    func main() -> void {
        let s = "abc" >> double;
    }
    """
    expected = "Type Mismatch In Expression: BinaryOp(StringLiteral('abc'), >>, Identifier(double))"
    assert Checker(source).check_from_source() == expected

def test_074():
    """Valid: nested call with shadowed name"""
    source = """
    func main() -> void {
        let print = 5;
        {
            let print = 10;
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_075():
    """Recursive GCD"""
    source = """
    func gcd(a: int, b: int) -> int {
        if (b == 0) { return a; }
        return gcd(b, a % b);
    }
    func main() -> void {
        let r = gcd(48, 18);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_076():
    """While with condition false from start"""
    source = """
    func main() -> void {
        while (false) {
            let x = 5;
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_077():
    """Break used correctly inside loop"""
    source = """
    func find(arr: [int; 3]) -> int {
        for (x in arr) {
            if (x == 2) { break; }
        }
        return 1;
    }
    func main() -> void {
        let a = [1, 2, 3];
        let r = find(a);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_078():
    """Const with valid global scope"""
    source = """
    const ID: int = 101;
    func main() -> void {
        let x = ID;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_079():
    """Assign void type function result (should fail)"""
    source = """
    func act() -> void {}
    func main() -> void {
        let r = act();
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(r, FunctionCall(Identifier(act), []))"
    assert Checker(source).check_from_source() == expected

def test_080():
    """Check inferred array type"""
    source = """
    func main() -> void {
        let a = [1, 2, 3];
        let b: int = a[1];
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_081():
    """Function declared but never used"""
    source = """
    func add(x: int, y: int) -> int { return x + y; }
    func main() -> void {
        let a = 5;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_082():
    """Nested if-else missing return (should fail)"""
    source = """
    func choose(x: int) -> int {
        if (x > 0) {
            if (x < 10) {}
            else { return 2; }
        } else { return 0; }
    }
    func main() -> void {
        let r = choose(5);
    }
    """
    expected = "Type Mismatch In Statement: FuncDecl(choose, [Param(x, int)], int, [...])"
    assert Checker(source).check_from_source().startswith("Type Mismatch In Statement")

def test_083():
    """Correct inferred type for array function"""
    source = """
    func squareEach(arr: [int; 3]) -> [int; 3] {
        return [arr[0]*arr[0], arr[1]*arr[1], arr[2]*arr[2]];
    }
    func main() -> void {
        let a = [2,3,4];
        let r = squareEach(a);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_084():
    """Array out of bounds (semantic ignores)"""
    source = """
    func main() -> void {
        let a = [1,2,3];
        let x = a[5];
    }
    """
    expected = "Type Mismatch In Statement: ArrayAccess(Identifier(a), IntegerLiteral(5))"
    assert Checker(source).check_from_source() == expected  # Assuming runtime check

def test_085():
    """Pipeline with nested call and math"""
    source = """
    func double(x: int) -> int { return x * 2; }
    func dec(x: int) -> int { return x - 1; }

    func main() -> void {
        let r = (3 + 4) >> double >> dec;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_086():
    """Return based on loop exit"""
    source = """
    func detect(arr: [int; 3]) -> int {
        for (x in arr) {
            if (x == 9) { return 1; }
        }
        return 0;
    }
    func main() -> void {
        let a = [1,2,9];
        let x = detect(a);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_087():
    """Invalid: assign array to int"""
    source = """
    func main() -> void {
        let a = [1,2,3];
        let b: int = a;
    }
    """
    expected = "Type Mismatch In Statement: VarDecl(b, int, Identifier(a))"
    assert Checker(source).check_from_source() == expected

def test_088():
    """Incorrect return structure in nested condition"""
    source = """
    func f(x: int) -> int {
        if (x > 0) {
            if (x == 1) { return 1; }
        } else {
            return 2;
        }
    }
    func main() -> void {
        let y = f(3);
    }
    """
    expected = "Type Mismatch In Statement: FuncDecl(f, [Param(x, int)], int, [...])"
    assert Checker(source).check_from_source().startswith("Type Mismatch In Statement")

def test_089():
    """Function with early return then fallback"""
    source = """
    func check(x: int) -> int {
        if (x == 1) { return 10; }
        return 0;
    }
    func main() -> void {
        let r = check(1);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_090():
    """Mutually recursive functions with condition"""
    source = """
    func isEven(n: int) -> bool {
        if (n == 0) { return true; } else { return isOdd(n - 1); }
    }

    func isOdd(n: int) -> bool {
        if (n == 0) { return false; } else { return isEven(n - 1); }
    }

    func main() -> void {
        let x = isEven(10);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_091():
    """Pipeline through inferred variable then used"""
    source = """
    func f(x: int) -> int { return x + 1; }
    func g(x: int) -> int { return x * 2; }

    func main() -> void {
        let temp = 3 >> f;
        let final = temp >> g;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_092():
    """Array of arrays used in loop"""
    source = """
    func main() -> void {
        let matrix = [[1,2], [3,4]];
        for (row in matrix) {
            for (val in row) {
                let x = val;
            }
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_093():
    """Shadow function name with variable inside block"""
    source = """
    func printVal(x: int) -> void {}

    func main() -> void {
        if (true) {
            let printVal = 100;
        }
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_094():
    """Loop with complex return in each branch"""
    source = """
    func sumFirstEven(arr: [int; 4]) -> int {
        let i = 0;
        while (i < 4) {
            if (arr[i] % 2 == 0) { return arr[i]; } else { i = i + 1; }
        }
        return -1;
    }

    func main() -> void {
        let a = [1, 3, 5, 6];
        let x = sumFirstEven(a);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_095():
    """Function returning function result from another"""
    source = """
    func square(x: int) -> int { return x * x; }
    func compute(x: int) -> int { return square(x); }

    func main() -> void {
        let r = compute(4);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_096():
    """Multiple return paths with mixed if else"""
    source = """
    func choose(x: int) -> int {
        if (x == 1) { return 1; } else {
            if (x == 2) { return 2; } else { return 3; }
        }
    }

    func main() -> void {
        let x = choose(2);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_097():
    """Check bool in pipeline type check"""
    source = """
    func negate(x: bool) -> bool { return !x; }

    func main() -> void {
        let b = true >> negate;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_098():
    """Multiple parameters in pipeline with math"""
    source = """
    func operate(x: int, y: int) -> int { return x * y; }

    func main() -> void {
        let r = 5 >> operate(3);
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_099():
    """Pipeline with function call returning array"""
    source = """
    func build() -> [int; 2] { return [5, 6]; }
    func head(arr: [int; 2]) -> int { return arr[0]; }

    func main() -> void {
        let result = build() >> head;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected

def test_100():
    """Pipeline with deeply nested calls"""
    source = """
    func trim(s: string) -> string { return s; }
    func upper(s: string) -> string { return s; }
    func addExcl(s: string) -> string { return s + "!"; }

    func main() -> void {
        let result = "hello" >> trim >> upper >> addExcl;
    }
    """
    expected = "Static checking passed"
    assert Checker(source).check_from_source() == expected