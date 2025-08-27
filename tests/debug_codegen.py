from src.utils.nodes import *
from utils import CodeGenerator
def test_debug_001():
    """Test basic variable declaration only (no array)"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(42))
        ])
    ])
    # Chỉ test tạo variable, không test print
    result = CodeGenerator().generate_and_run(ast)
    # Expected: không có lỗi, có thể output rỗng
    assert "error" not in result.lower()

def test_debug_002():
    """Test variable declaration and identifier access"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("x", IntType(), IntegerLiteral(42)),
            ExprStmt(Identifier("x"))  # Chỉ access identifier, không print
        ])
    ])
    result = CodeGenerator().generate_and_run(ast)
    assert "error" not in result.lower()

def test_debug_003():
    """Test boolean variable with explicit type"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("flag", BoolType(), BooleanLiteral(True)),
            ExprStmt(Identifier("flag"))
        ])
    ])
    result = CodeGenerator().generate_and_run(ast)
    assert "error" not in result.lower()

def test_debug_004():
    """Test simple array creation (no access)"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("arr", ArrayType(IntType(), 2), ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)]))
        ])
    ])
    result = CodeGenerator().generate_and_run(ast)
    assert "error" not in result.lower()

def test_debug_005():
    """Test array with explicit type annotation"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("nums", ArrayType(FloatType(), 2), ArrayLiteral([FloatLiteral(1.1), FloatLiteral(2.2)]))
        ])
    ])
    result = CodeGenerator().generate_and_run(ast)
    assert "error" not in result.lower()

def test_debug_006():
    """Test minimal working print"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [IntegerLiteral(42)]))
        ])
    ])
    result = CodeGenerator().generate_and_run(ast)
    assert result == "42"

def test_debug_007():
    """Test step by step: var -> identifier -> print"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("num", IntType(), IntegerLiteral(123))
        ])
    ])
    result1 = CodeGenerator().generate_and_run(ast)
    assert "error" not in result1.lower()
    
    # Nếu test trên pass, thử thêm identifier access
    ast2 = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("num", IntType(), IntegerLiteral(123)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("num")]))
        ])
    ])
    result2 = CodeGenerator().generate_and_run(ast2)
    assert result2 == "123"

def test_debug_008():
    """Test boolean literal directly (no variable)"""
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            ExprStmt(FunctionCall(Identifier("print"), [BooleanLiteral(True)]))
        ])
    ])
    result = CodeGenerator().generate_and_run(ast)
    assert result == "true"

def test_debug_009():
    """Test type inference vs explicit type"""
    # Với explicit type
    ast1 = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("flag1", BoolType(), BooleanLiteral(True)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("flag1")]))
        ])
    ])
    
    # Với type inference (None)
    ast2 = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("flag2", None, BooleanLiteral(True)),
            ExprStmt(FunctionCall(Identifier("print"), [Identifier("flag2")]))
        ])
    ])
    
    try:
        result1 = CodeGenerator().generate_and_run(ast1)
        print(f"Explicit type result: {result1}")
    except Exception as e:
        print(f"Explicit type error: {e}")
        
    try:
        result2 = CodeGenerator().generate_and_run(ast2)  
        print(f"Inferred type result: {result2}")
    except Exception as e:
        print(f"Inferred type error: {e}")

def test_debug_010():
    """Test array literal structure"""
    # Test nếu ArrayLiteral có elements hay value attribute
    try:
        arr_node = ArrayLiteral([IntegerLiteral(1), IntegerLiteral(2)])
        print(f"ArrayLiteral has elements: {hasattr(arr_node, 'elements')}")
        print(f"ArrayLiteral has value: {hasattr(arr_node, 'value')}")
        
        if hasattr(arr_node, 'elements'):
            print(f"elements content: {arr_node.elements}")
        if hasattr(arr_node, 'value'):
            print(f"value content: {arr_node.value}")
            
    except Exception as e:
        print(f"ArrayLiteral creation error: {e}")
        
    # Test with minimal array
    ast = Program([], [
        FuncDecl("main", [], VoidType(), [
            VarDecl("test_arr", ArrayType(IntType(), 1), ArrayLiteral([IntegerLiteral(99)]))
        ])
    ])
    result = CodeGenerator().generate_and_run(ast)
    print(f"Simple array result: {result}")

# Chạy các test này từng cái một để tìm điểm failure chính xác
if __name__ == "__main__":
    # Uncomment từng test để chạy riêng lẻ
    # test_debug_001()
    # test_debug_002() 
    # test_debug_003()
    # ...
    test_debug_010()  # Bắt đầu với test này để kiểm tra ArrayLiteral structure