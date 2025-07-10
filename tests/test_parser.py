from utils import Parser

def test_001():
    """Test basic function declaration"""
    source = """func main() -> void {};"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_002():
    """Test function with parameters"""
    source = """func add(a: int, b: int) -> int { return a + b; };"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_003():
    """Test variable declaration with type annotation"""
    source = """func main() -> void { let x: int = 42; };"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_004():
    """Test variable declaration with type inference"""
    source = """func main() -> void { let name = "Alice"; };"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_005():
    """Test constant declaration"""
    source = """const PI: float = 3.14159; func main() -> void {};"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_006():
    """Test if-else statement"""
    source = """func main() -> void { 
        if (x > 0) { 
            print("positive"); 
        } else { 
            print("negative"); 
        }
    };"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_007():
    """Test while loop"""
    source = """func main() -> void { 
        let i = 0;
        while (i < 10) { 
            i = i + 1; 
        }
    };"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_008():
    """Test for loop with array"""
    source = """func main() -> void { 
        let numbers = [1, 2, 3, 4, 5];
        for (num in numbers) { 
            print(str(num)); 
        }
    };"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_009():
    """Test array declaration and access"""
    source = """func main() -> void { 
        let arr: [int; 3] = [1, 2, 3];
        let first = arr[0];
        arr[1] = 42;
    };"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_010():
    """Test complex expression with pipeline operator"""
    source = """func main() -> void { 
        let result = data >> process >> validate >> transform;
        let calculation = 5 >> add(3) >> multiply(2);
    };"""
    expected = "success"
    assert Parser(source).parse() == expected
    
def test_nt():
    """Test multi-dimensional array access with expression"""
    source = """
    func add(a: int, b: int) -> int {
        return a + b;
    }

    func foo() -> int {
        return 42;
    }

    func main() -> void {
        let matrix: [[int; 3]; 2] = [[1, 2, 3], [4, 5, 6]];
        let abc = 10;
        let xyz = 5;
        let result = matrix[1][2] + abc / xyz * foo() + 1235 % add(3, 4);
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected
    
# Testcases below are customized by Duy Khang as the requirement of Assignment 1

def test_001():
    """Test variable declaration with explicit type and string value"""
    source = """const name: string = "HLang";"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_002():
    """Test variable declaration with negative float"""
    source = """const x = -4.56;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_003():
    """Test variable declaration with array of strings"""
    source = """const greetings: [string; 2] = ["hi", "hello"];"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_004():
    """Test variable declaration"""
    source = """let z: string = "oops";"""
    Parser(source).parse()

def test_005():
    """Test variable declaration with expression value"""
    source = """const area = 3.14 * 2 * 2;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_006():
    """Test constant declaration with string value and no explicit type"""
    source = """const greeting = "Hello";"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_007():
    """Test constant declaration with array of integers"""
    source = """const numbers: [int; 3] = [1, 2, 3];"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_008():
    """Test constant declaration with boolean value and explicit type"""
    source = """const isActive: bool = true;"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_009():
    """Test constant declaration missing assignment (should fail)"""
    source = """const failedConst: int;"""
    Parser(source).parse()

def test_010():
    """Test multiple constant declarations inside block"""
    source = """
    func main() -> void {
        const a = 1;
        const b: float = 2.0;
        const msg = "block";
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_011():
    """Test variable declaration with function call expression"""
    source ="""
    func checkInput() -> bool {
        return true;
    }

    func main() -> void {
        let valid: bool = checkInput();
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_012():
    """Test shadowing variable in inner block"""
    source = """
    func main() -> void {
        let x = 10;
        {
            let x = "hello";
            print(x);
        }
        print(x);
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_013():
    """Test variable declaration with data type annotation"""
    source = """
    func main() -> void {
        let msg: int = 100;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_014():
    """Test variable declaration using arithmetic expression"""
    source = """
    func main() -> void {
        let area = 3.14 * 2 * 2;
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_015():
    """Test variable declaration inside nested block"""
    source = """
    func main() -> void {
        {
            let x = 5;
            {
                let y = x + 2;
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_016():
    """Test function declaration #6"""
    source = """func t8Sr(sEZpEf: int) -> int {
        let x = sEZpEf + 1;
        return x;
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_017():
    """Test function declaration #7"""
    source = """func mNAd(a: int) -> int {
        if (a > 0) { return a; }
        else { return -a; }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_018():
    """Test function declaration #8"""
    source = """func yWN7cy(x: int) -> int {
        while (x > 0) {
            x = x - 1;
        }
        return x;
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_019():
    """Test function declaration #9"""
    source = """func uQwU(x: int) -> int {
        for (i in arr) {
            if (i > x) {
                return i;
            }
        }
        return 0;
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_020():
    """Test function declaration #10"""
    source = """
    func op3cl(n: int) -> int {
        let sum = 0;
        while (n > 0) {
            sum = sum + n;
            n = n - 1;
        }
        return sum;
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

# IF-ELSE STRUCTURES

def test_021():
    """Test if-else structure"""
    source = """
    func main() -> bool {
        let x = 5;
        let y: int = 0;
        if (x > 0) {
            y = x;
        } else {
            y = -x;
        }
        return (y >= x);
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_022():
    """Test if with nested if inside function"""
    source = """
    func main() -> void {
        if (a > b) { 
            if (a > c) { 
                let max = a; 
            } 
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_023():
    """Test if with block only inside function"""
    source = """
    func main() -> void {
        if (true) { 
            let flag = false; 
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_024():
    """Test if-else with boolean expressions inside function"""
    source = """
    func main() -> void {
        if (x > 0 && y < 10) { 
            let valid = true; 
        } else { 
            let valid = false; 
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_025():
    """Test if-else with function call in condition inside function"""
    source = """
    func main() -> void {
        if (check(x)) { 
            let ok = 1; 
        } else { 
            let ok = 0; 
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_026():
    """Test if with assignment in block inside function"""
    source = """
    func main() -> void {
        if (z == 0) {
            result = 1;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_027():
    """Test if-else multiple levels inside function"""
    source = """
    func main() -> void {
        if (a < b) {
            let min = a;
        } else if (b < c) {
            let min = b;
        } else {
            let min = c;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_028():
    """Test if-else with arithmetic expressions inside function"""
    source = """
    func main() -> void {
        if ((a + b) > (c - d)) {
            let win = true;
        } else {
            let win = false;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_029():
    """Test if with comparison inside function"""
    source = """
    func main() -> void {
        if (name == "admin") {
            access = true;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_030():
    """Test if-else with multiple statements inside function"""
    source = """
    func main() -> void {
        if (valid) {
            let result = 10;
            let status = true;
        } else {
            let result = 0;
            let status = false;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_031():
    """Test if inside function"""
    source = """
    func check() -> bool {
        if (flag) { return true; }
        else { return false; }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_032():
    """Test if inside while (inside func)"""
    source = """
    func main() -> void {
        while (i < 10) {
            if (i % 2 == 0) { continue; }
            i = i + 1;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_033():
    """Test if with array access (inside func)"""
    source = """
    func main() -> void {
        if (arr[0] > 5) {
            let head = arr[0];
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_034():
    """Test if with nested block (inside func)"""
    source = """
    func main() -> void {
        if (true) {
            {
                let x = 0;
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_035():
    """Test if in for-loop (inside func)"""
    source = """
    func main() -> void {
        for (i in arr) {
            if (i != 0) {
                let inv = 1 / i;
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_036():
    """Test empty else block (inside func)"""
    source = """
    func main() -> void {
        if (x > 0) {
            y = x;
        } else { }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_037():
    """Test if with multiple expressions (inside func)"""
    source = """
    func main() -> void {
        if (x + y > z) {
            let total = x + y;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_038():
    """Test if with constant boolean (inside func)"""
    source = """
    func main() -> void {
        if (false) {
            let never = true;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_039():
    """Test if with return"""
    source = """
    func check() -> int {
        if (x == 0) { return 1; }
        return 0;
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_040():
    """Test if-else with let shadowing inside function"""
    source = """
    func main() -> void {
        if (x > 0) {
            let x = 5;
        } else {
            let x = -5;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_041():
    """Test while loop inside function"""
    source = """
    func main() -> void {
        while (i < 5) {
            let temp = i;
            i = i + 1;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_042():
    """Test while with nested if inside function"""
    source = """
    func main() -> void {
        while (true) {
            if (x == 1) {
                break;
            }
            x = x + 1;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_043():
    """Test while with return inside"""
    source = """
    func repeat() -> int {
        while (true) {
            return 0;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_044():
    """Test while with block assignment inside function"""
    source = """
    func main() -> void {
        while (ready) {
            let done = false;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_045():
    """Test while with nested loop inside function"""
    source = """
    func main() -> void {
        while (a < b) {
            while (b < c) {
                break;
            }
            a = a + 1;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_046():
    """Test while with logical condition inside function"""
    source = """
    func main() -> void {
        while (x > 0 && y < 100) {
            x = x - 1;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_047():
    """Test while with function call in condition inside function"""
    source = """
    func main() -> void {
        while (hasNext()) {
            process();
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_048():
    """Test while with continue inside function"""
    source = """
    func main() -> void {
        while (i < 10) {
            if (i % 2 == 0) { continue; }
            i = i + 1;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_049():
    """Test while with array access inside function"""
    source = """
    func main() -> void {
        while (arr[i] != 0) {
            i = i + 1;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

def test_050():
    """Test deeply nested array operations"""
    source = """
    func main() -> int {
        let hyperCube: [[[[int; 2]; 2]; 2]; 2] = [
            [
                [[[1, 2], [3, 4]], [[5, 6], [7, 8]]],
                [[[9, 10], [11, 12]], [[13, 14], [15, 16]]]
            ],
            [
                [[[17, 18], [19, 20]], [[21, 22], [23, 24]]],
                [[[25, 26], [27, 28]], [[29, 30], [31, 32]]]
            ]
        ];
        hyperCube[1][0][1][0] = 500;
        return hyperCube[1][0][1][0];
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected
    
def test_051():
    """Test for loop with simple iteration"""
    source = """
    func main() -> void {
        for (i in items) {
            let total = total + i;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_052():
    """Test for loop with type annotation"""
    source = """
    func main() -> void {
        for (i in arr) {
            let squared: int = i * i;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_053():
    """Test for loop with nested if"""
    source = """
    func main() -> void {
        for (x in xs) {
            if (x > 0) {
                let pos = true;
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_054():
    """Test for loop with block and multiple statements"""
    source = """
    func main() -> void {
        for (i in numbers) {
            let doubled = i * 2;
            print(doubled);
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_055():
    """Test for loop with array access"""
    source = """
    func main() -> void {
        for (index in [1, 2, 3]) {
            let value = index * 2;
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_056():
    """Test nested for and if-else with break"""
    source = """
    func main() -> void {
        for (i in arr) {
            if (i == 0) {
                break;
            } else {
                let x = i;
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_057():
    """Test nested while inside for loop with continue"""
    source = """
    func main() -> void {
        for (i in arr) {
            while (i < 5) {
                i = i + 1;
                if (i % 2 == 0) {
                    continue;
                }
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_058():
    """Test if-else inside while inside for"""
    source = """
    func main() -> void {
        for (n in nums) {
            while (n > 0) {
                if (n == 1) {
                    break;
                } else {
                    n = n - 1;
                }
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_059():
    """Test deeply nested control flow"""
    source = """
    func main() -> void {
        for (i in list) {
            if (i > 0) {
                while (i < 10) {
                    if (i == 5) {
                        break;
                    }
                    i = i + 1;
                }
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected


def test_060():
    """Test mixed continue and break in for-if-while"""
    source = """
    func main() -> void {
        for (x in data) {
            if (x == 0) {
                continue;
            }
            while (x < 100) {
                x = x + 1;
                if (x == 50) {
                    break;
                }
            }
        }
    }
    """
    expected = "success"
    assert Parser(source).parse() == expected

# ------------------ SYNTAX ERROR TESTS ------------------

def test_061():
    """Test missing '(' in for loop"""
    source = """
    func main() -> void {
        for i in arr) { let x = 0; }
    }
    """
    Parser(source).parse()

def test_062():
    """Test missing semicolon in variable declaration"""
    source = """
    func main() -> void {
        let x = 5
    }
    """
    Parser(source).parse()

def test_063():
    """Test unmatched brackets"""
    source = """
    func main() -> void {
        let x = [1, 2, 3;
    }
    """
    Parser(source).parse()

def test_064():
    """Test function missing return type"""
    source = """
    func foo(x: int) { return x; }
    """
    Parser(source).parse()

def test_065():
    """Test function missing parameter colon"""
    source = """
    func foo(x int) -> int {
        return x;
    }
    """
    Parser(source).parse()

def test_066():
    """Test if statement missing closing parenthesis"""
    source = """
    func main() -> void {
        if (x < 10 { let y = 2; }
    }
    """
    Parser(source).parse()

def test_067():
    """Test while with missing ')'"""
    source = """
    func main() -> void {
        while (x < 10 { x = x + 1; }
    }
    """
    Parser(source).parse()

def test_068():
    """Test assignment missing '='"""
    source = """
    func main() -> void {
        let x 5;
    }
    """
    Parser(source).parse()

def test_069():
    """Test return statement without semicolon"""
    source = """
    func main() -> void {
        return 10
    }
    """
    Parser(source).parse()

def test_070():
    """Test break outside loop"""
    source = """func main() -> void { break; }"""
    Parser(source).parse()


def test_071():
    """Test continue outside loop"""
    source = """func main() -> void { continue; }"""
    Parser(source).parse()


def test_072():
    """Test block missing closing brace"""
    source = """func main() -> void { let x = 5; """
    Parser(source).parse()


def test_073():
    """Test nested block missing open brace"""
    source = """func main() -> void { if (x) let y = 3; }"""
    Parser(source).parse()


def test_074():
    """Test wrong function keyword"""
    source = """fnc main() -> int { return 1; }"""
    Parser(source).parse()


def test_075():
    """Test duplicated else"""
    source = """func main() -> void {
        if (x) { let x = 1; } else else { let y = 2; }
    }"""
    Parser(source).parse()


def test_076():
    """Test missing expression in assignment"""
    source = """func main() -> void { let x = ; }"""
    Parser(source).parse()


def test_077():
    """Test wrong arrow in function"""
    source = """func main() => int { return 1; }"""
    Parser(source).parse()


def test_078():
    """Test missing block in function"""
    source = """func main() -> int return 1;"""
    Parser(source).parse()


def test_079():
    """Test broken array declaration"""
    source = """func main() -> void { let x: [int; ] = [1, 2, 3]; }"""
    Parser(source).parse()


def test_080():
    """Test invalid pipeline syntax"""
    source = """func main() -> void { let result = x >> ; }"""
    Parser(source).parse()


def test_081():
    """Test nested if-else inside while"""
    source = """func main() -> void {
        while (x < 5) {
            if (x % 2 == 0) { x = x + 1; }
            else { x = x * 2; }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_082():
    """Test function with multiple parameters"""
    source = """func sum(a: int, b: int) -> int { return a + b; }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_083():
    """Test pipeline expression"""
    source = """func main() -> void {
        let result = getData() >> filter() >> map();
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_084():
    """Test nested function calls"""
    source = """func main() -> void {
        let x = foo(bar(baz()));
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_085():
    """Test array access"""
    source = """func main() -> void {
        let x = arr[2];
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_086():
    """Test return in function with expression"""
    source = """func test() -> int { return 5 * (2 + 1); }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_087():
    """Test boolean logic"""
    source = """func main() -> void {
        let ok = (x > 5) && (y < 10) || !z;
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_088():
    """Test variable with type annotation"""
    source = """func main() -> void {
        let name: string = "Alice";
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_089():
    """Test constant declaration"""
    source = """const pi: float = 3.14;"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_090():
    """Test array literal with empty content"""
    source = """func main() -> void {
        let a = [];
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_091():
    """Test missing semicolon (invalid)"""
    source = """func main() -> void { let x = 10 }"""
    Parser(source).parse()


def test_092():
    """Test function missing arrow return type"""
    source = """func test() int { return 5; }"""
    Parser(source).parse()


def test_093():
    """Test void function with early return"""
    source = """
    func printPositive(x: int) -> void {
        if (x <= 0) {
            return;
        }
        print("Positive");
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_094():
    """Test invalid parameter list (missing colon)"""
    source = """func add(a int, b: int) -> int { return a + b; }"""
    Parser(source).parse()


def test_095():
    """Test mismatched braces in function"""
    source = """func broken() -> void { let x = 1; """
    Parser(source).parse()


def test_096():
    """Test direct recursion in factorial"""
    source = """
    func factorial(n: int) -> int {
        if (n <= 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_097():
    """Test indirect recursion isEven/isOdd"""
    source = """
    func isEven(n: int) -> bool {
        if (n == 0) {
            return true;
        }
        return isOdd(n - 1);
    }
    func isOdd(n: int) -> bool {
        if (n == 0) {
            return false;
        }
        return isEven(n - 1);
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_098():
    """Test array mutation inside function"""
    source = """
    func fill(arr: [int; 3]) -> void {
        arr[0] = 1;
        arr[1] = 2;
        arr[2] = 3;
    }"""
    expected = "success"
    assert Parser(source).parse() == expected


def test_099():
    """Test variable shadowing in nested block"""
    source = """
    func main() -> void {
        let x = 10;
        {
            let x = "hello";
            print(x);
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected

def test_100():
    """Test block scoping with nested declarations"""
    source = """
    func main() -> void {
        let x = 10;
        {
            let x = 20;
            {
                let y = x + 5;
            }
        }
    }"""
    expected = "success"
    assert Parser(source).parse() == expected
