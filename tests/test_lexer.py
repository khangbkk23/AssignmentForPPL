from utils import Tokenizer

def test_001a():
    """Test basic identifier tokenization"""
    source = "abc"
    expected = "abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_002a():
    """Test keywords recognition"""
    source = "func main if else while for let const"
    expected = "func,main,if,else,while,for,let,const,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_003a():
    """Test integer literals"""
    source = "42 0 -17 007"
    expected = "42,0,-,17,007,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_004a():
    """Test float literals"""
    source = "3.14 -2.5 0.0 42. 5."
    expected = "3.14,-,2.5,0.0,42.,5.,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_005a():
    """Test boolean literals"""
    source = "true false"
    expected = "true,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_006a():
    """Test unclosed string literal error"""
    source = '"Hello World'
    expected = "Unclosed String: Hello World"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_007a():
    """Test illegal escape sequence error"""
    source = '"Hello \\x World"'
    expected = "Illegal Escape In String: Hello \\x World"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_008a():
    """Test error character (non-ASCII or invalid character)"""
    source = "let x = 5; @ invalid"
    expected = "let,x,=,5,;,Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_009a():
    """Test valid string literals with escape sequences"""
    source = '"Hello World" "Line 1\\nLine 2" "Quote: \\"text\\""'
    expected = "Hello World,Line 1\\nLine 2,Quote: \\\"text\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_009b():
    """Test string literals return content without quotes"""
    source = '"Hello World"'
    expected = "Hello World,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_009c():
    """Test empty string literal"""
    source = '""'
    expected = ",EOF"  # Empty string content
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_010a():
    """Test operators and separators"""
    source = "+ - * / % == != < <= > >= && || ! = -> >> ( ) [ ] { } , ; :"
    expected = "+,-,*,/,%,==,!=,<,<=,>,>=,&&,||,!,=,->,>>,(,),[,],{,},,,;,:,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
    
# Below testcases are customization belonging to Duy Khang as the require of Assignment 1

# Testing the comments inside code and comment line
def test_001():
    """Test skipping line comment at end of code"""
    source = "let x = 5; // this is a comment"
    expected = "let,x,=,5,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_002():
    """Test skipping full-line comment"""
    source = "// this is just a comment"
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_003():
    """Test block comment between declarations"""
    source = "let x = 10; /* comment */ const y = 20;"
    expected = "let,x,=,10,;,const,y,=,20,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_004():
    """Test block comment at start of file"""
    source = "/* start comment */ let x = 0;"
    expected = "let,x,=,0,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_005():
    """Test block comment at end of file"""
    source = "return 1; /* end comment */"
    expected = "return,1,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_006():
    """Test nested-looking comments"""
    source = "/* outer /* inner */ still outer */ let a = 1;"
    expected = "still,outer,*,/,let,a,=,1,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_007():
    """Test line comment after code"""
    source = "const val = 3; // assign constant"
    expected = "const,val,=,3,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_008():
    """Test line comment mixed with whitespace"""
    source = "  // comment with space\t\nlet a = 2;"
    expected = "let,a,=,2,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_009():
    """Test multi-line block comment"""
    source = "/* line1\nline2\nline3 */ let b = 4;"
    expected = "let,b,=,4,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_010():
    """Test multiple comments in one file"""
    source = """
        // Line comment
        let a = 1; /* inline block */ const b = 2; // trailing comment
    """
    expected = "let,a,=,1,;,const,b,=,2,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Testing for all standard verification of tokens

def test_011():
    """Test common text"""
    source = "Hello\nWorld"
    expected = "Hello,World,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
    
def test_011a():
    """Test common text"""
    source = "hello\tworld\nnew_line"
    expected = "hello,world,new_line,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected
    
def test_012():
    source = "let x1 = 42"
    expected = "let,x1,=,42,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected 

def test_013():
    """Test identifier with underscore"""
    source = "foo_bar"
    expected = "foo_bar,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_014():
    """Test integer literals"""
    source = "0 123 007"
    expected = "0,123,007,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_015():
    """Test float literals"""
    source = "3.14 0.0 .5 1. .25e10"
    expected = "3.14,0.0,.5,1.,.25e10,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_016():
    """Test keywords and identifiers"""
    source = "let x = 5"
    expected = "let,x,=,5,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_017():
    """Test operators"""
    source = "+ - * / % == != < <= > >= && || != ="
    expected = "+,-,*,/,%,==,!=,<,<=,>,>=,&&,||,!=,=,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_018():
    """Test punctuation"""
    source = "( ) [ ] { } , ; :"
    expected = "(,),[,],{,},,,;,:,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_019():
    """Test array literal"""
    source = "[1, 2, 3]"
    expected = "[,1,,,2,,,3,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_020():
    """Test empty array"""
    source = "[]"
    expected = "[,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_021():
    """Test simple func declaration"""
    source = "func main() -> void {}"
    expected = "func,main,(,),->,void,{,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_022():
    """Test return statement"""
    source = "return 1 + 2;"
    expected = "return,1,+,2,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_023():
    """Test if-else"""
    source = "if (x) { y; } else { z; }"
    expected = "if,(,x,),{,y,;,},else,{,z,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_024():
    """Test while loop"""
    source = "while (i < 10) { i = i + 1; }"
    expected = "while,(,i,<,10,),{,i,=,i,+,1,;,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_025():
    """Test for loop"""
    source = "for (i in arr) {}"
    expected = "for,(,i,in,arr,),{,},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_026():
    """Test break/continue"""
    source = "break; continue;"
    expected = "break,;,continue,;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_027():
    """Test nested block"""
    source = "{{{}}}"
    expected = "{,{,{,},},},EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_028():
    """Test escaped string"""
    source = '"Line\\n1\\tLine2"'
    expected = "Line\\n1\\tLine2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_029():
    """Test string with escaped quote"""
    source = '"He said: \\"Hi\\""'
    expected = "He said: \\\"Hi\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_030():
    """Test empty string"""
    source = ""
    expected = "EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_031():
    """Test single-line comment"""
    source = "// this is comment\nlet x = 1"
    expected = "let,x,=,1,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_032():
    """Test multi-line comment"""
    source = "/* comment */ let y = 2"
    expected = "let,y,=,2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_033():
    """Test long identifier"""
    source = "someVeryLongIdentifier123"
    expected = "someVeryLongIdentifier123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_034():
    """Test underscore only id"""
    source = "_ _abc"
    expected = "_,_abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_035():
    """Test digit in id"""
    source = "a1 a123"
    expected = "a1,a123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_036():
    """Test all keywords"""
    source = "let const func if else while for in return break continue true false"
    expected = "let,const,func,if,else,while,for,in,return,break,continue,true,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_037():
    """Test int and float"""
    source = "1.2e10 -3.4E-5 .5e+6"
    expected = "1.2e10,-,3.4E-5,.5e+6,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_038():
    """Test function call"""
    source = "foo(1, 2)"
    expected = "foo,(,1,,,2,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_039():
    """Test array access"""
    source = "arr[0]"
    expected = "arr,[,0,],EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_040():
    """Test multiple expressions"""
    source = "x = y + z * (a - b);"
    expected = "x,=,y,+,z,*,(,a,-,b,),;,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_041():
    """Test pipe operator"""
    source = "a >> b"
    expected = "a,>>,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_042():
    """Test string escape individual"""
    source = '"\\n" "\\t" "\\r" "\\\\" "\\\""'
    expected = "\\n,\\t,\\r,\\\\,\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_043():
    """Test string all escape"""
    source = '"Line\\nTab\\tCR\\rBackslash\\\\Quote\\\""'
    expected = "Line\\nTab\\tCR\\rBackslash\\\\Quote\\\",EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_044():
    """Test identifier invalid start"""
    source = "123abc"
    expected = "123,abc,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_045():
    """Test illegal escape start"""
    source = '"\\x123"'
    expected = "Illegal Escape In String: \\x123"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Testing with random content testcase
def test_046():
    """Test logical NOT operator"""
    source = "!true"
    expected = "!,true,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_047():
    """Test logical NOT with parenthesis"""
    source = "!(false)"
    expected = "!,(,false,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_048():
    """Test logical AND with literals"""
    source = "true && false"
    expected = "true,&&,false,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_049():
    """Test logical OR with literals"""
    source = "false || true"
    expected = "false,||,true,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_050():
    """Test nested logical expressions"""
    source = "true && false || true"
    expected = "true,&&,false,||,true,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_051():
    """Test combination of NOT and AND"""
    source = "!a && b"
    expected = "!,a,&&,b,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_052():
    """Test combination of NOT and OR"""
    source = "!x || y"
    expected = "!,x,||,y,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_053():
    """Test full boolean expression with parenthesis"""
    source = "!(a && b) || c"
    expected = "!,(,a,&&,b,),||,c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_054():
    """Test short-circuiting AND logic"""
    source = "(x > 0) && (y < 10)"
    expected = "(,x,>,0,),&&,(,y,<,10,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_055():
    """Test short-circuiting OR logic"""
    source = "(x == 0) || (y == 0)"
    expected = "(,x,==,0,),||,(,y,==,0,),EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_056():
    """Random valid content #01"""
    source = "X Y123 Z_9"
    expected = "X,Y123,Z_9,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_057():
    """Random valid content #02"""
    source = "HELLO world_99"
    expected = "HELLO,world_99,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_058():
    """Random valid content #03"""
    source = "main1 sub_2"
    expected = "main1,sub_2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_059():
    """Random valid content #04"""
    source = "Zed23 Kip_"
    expected = "Zed23,Kip_,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_060():
    """Random valid content #05"""
    source = "_1a _2b _3c"
    expected = "_1a,_2b,_3c,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_061():
    """Random valid content #06"""
    source = "Test_123 Value_456"
    expected = "Test_123,Value_456,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_062():
    """Random valid content #07"""
    source = "MaxValue MinValue"
    expected = "MaxValue,MinValue,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_063():
    """Random valid content #08"""
    source = "snake_case camelCase"
    expected = "snake_case,camelCase,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_064():
    """Random valid content #09"""
    source = "x1 y2 z3"
    expected = "x1,y2,z3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_065():
    """Random valid content #10"""
    source = "FOO bar123"
    expected = "FOO,bar123,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_066():
    """Random valid content #11"""
    source = "Count_1 Count_2"
    expected = "Count_1,Count_2,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_067():
    """Random valid content #12"""
    source = "ABC def GHI"
    expected = "ABC,def,GHI,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_068():
    """Random valid content #13"""
    source = "v1 v2 v3"
    expected = "v1,v2,v3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_069():
    """Random valid content #14"""
    source = "value_1 _value2 value_3"
    expected = "value_1,_value2,value_3,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_070():
    """Random valid content #15"""
    source = "_init _start _end"
    expected = "_init,_start,_end,EOF"
    assert Tokenizer(source).get_tokens_as_string() == expected

# Testing for the error recognization

def test_071():
    """Test unclosed string #01"""
    source = '"wvnYOPrymf\n'
    expected = "Unclosed String: wvnYOPrymf"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_072():
    """Test unclosed string #02"""
    source = '"WBuuP2'
    expected = "Unclosed String: WBuuP2"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_073():
    """Test unclosed string #03"""
    source = '"w9k0wmuR0\n'
    expected = "Unclosed String: w9k0wmuR0"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_074():
    """Test unclosed string #04"""
    source = '"jpwEo5l\n'
    expected = "Unclosed String: jpwEo5l"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_075():
    """Test unclosed string #05"""
    source = '"ZtDGOemgu\n'
    expected = "Unclosed String: ZtDGOemgu"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_076():
    """Test unclosed string #06"""
    source = '"j3ar E\n'
    expected = "Unclosed String: j3ar E"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_077():
    """Test unclosed string #07"""
    source = '"qYMci8Yr'
    expected = "Unclosed String: qYMci8Yr"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_078():
    """Test unclosed string #08"""
    source = '"Qr1HI'
    expected = "Unclosed String: Qr1HI"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_079():
    """Test unclosed string #09"""
    source = '"8l1krB\n'
    expected = "Unclosed String: 8l1krB"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_080():
    """Test unclosed string #10"""
    source = '"ama9CQro'
    expected = "Unclosed String: ama9CQro"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_081():
    """Test illegal escape string #01"""
    source = '"1oMZQXi\\1 more text"'
    expected = "Illegal Escape In String: 1oMZQXi\\1 more text"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_082():
    """Test illegal escape string #02"""
    source = '"kxRt4\\@ more text"'
    expected = "Illegal Escape In String: kxRt4\\@ more text"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_083():
    """Test illegal escape string #03"""
    source = '"1FV9\\` more text"'
    expected = "Illegal Escape In String: 1FV9\\` more text"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_084():
    """Test illegal escape string #04"""
    source = '"1bqlgb\\$ more text"'
    expected = "Illegal Escape In String: 1bqlgb\\$ more text"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_085():
    """Test illegal escape string #05"""
    source = '"OrV3ooc0\\2 more text"'
    expected = "Illegal Escape In String: OrV3ooc0\\2 more text"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_086():
    """Test illegal escape string #06"""
    source = '"0pzah\\^ more text"'
    expected = "Illegal Escape In String: 0pzah\\^ more text"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_87():
    """Test illegal escape string #07"""
    source = '"37pV \\3 more text"'
    expected = "Illegal Escape In String: 37pV \\3 more text"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_88():
    """Test illegal escape string #08"""
    source = '"ziqv0B\\& more text"'
    expected = "Illegal Escape In String: ziqv0B\\& more text"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_89():
    """Test illegal escape string #09"""
    source = '"gEhYENU1\\1 more text"'
    expected = "Illegal Escape In String: gEhYENU1\\1 more text"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_90():
    """Test illegal escape string #10"""
    source = '"DHpUB8\\& more text"'
    expected = "Illegal Escape In String: DHpUB8\\& more text"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_091():
    """Test ERROR_TOKEN with @"""
    source = "@"
    expected = "Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_092():
    """Test ERROR_TOKEN with #"""
    source = "#"
    expected = "Error Token #"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_093():
    """Test ERROR_TOKEN with Unicode character"""
    source = "🙂"
    expected = "Error Token 🙂"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_094():
    """Test ERROR_TOKEN with dollar sign"""
    source = "$"
    expected = "Error Token $"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_095():
    """Test ERROR_TOKEN with percent sign in invalid place"""
    source = "&"
    expected = "Error Token &"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_096():
    """Test ERROR_TOKEN with backtick"""
    source = "`"
    expected = "Error Token `"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_097():
    """Test ERROR_TOKEN with single quote"""
    source = "'"
    expected = "Error Token '"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_098():
    """Test ERROR_TOKEN with vertical bar (should not be confused with ||)"""
    source = "|"
    expected = "Error Token |"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_099():
    """Test ERROR_TOKEN with unicode math symbol"""
    source = "∆"
    expected = "Error Token ∆"
    assert Tokenizer(source).get_tokens_as_string() == expected

def test_100():
    """Test ERROR_TOKEN with multiple invalid chars"""
    source = "@#€"
    expected = "Error Token @"
    assert Tokenizer(source).get_tokens_as_string() == expected
