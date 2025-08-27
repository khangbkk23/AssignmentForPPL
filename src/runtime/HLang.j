.source HLang.java
.class public HLang
.super java/lang/Object
.field static final LIMIT I
.method public static <clinit>()V
Label0:
	bipush 10
	putstatic HLang/LIMIT I
	return
Label1:
.limit stack 10
.limit locals 0
.end method

.method public static square(I)I
.var 0 is n I from Label0 to Label1
Label0:
	iload_0
	iload_0
	imul
	ireturn
Label1:
.limit stack 2
.limit locals 1
.end method

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
.var 1 is numbers [I from Label0 to Label1
	iconst_4
	newarray int
dup
	iconst_0
	iconst_1
iastore
dup
	iconst_1
	iconst_2
iastore
dup
	iconst_2
	iconst_3
iastore
dup
	iconst_3
	iconst_4
iastore
	astore_1
	ldc "Squares:"
	invokestatic io/print(Ljava/lang/String;)V
	aload_1
.var 2 is __arr_for_2 [I from Label0 to Label1
	astore_2
.var 3 is __idx_for_3 I from Label0 to Label1
	iconst_0
	istore_3
Label2:
	iload_3
	aload_2
arraylength
if_icmpge Label3
	aload_2
	iload_3
iaload
.var 4 is num I from Label0 to Label1
	istore 4
	iload 4
	getstatic HLang/LIMIT I
	if_icmpge Label9
	iconst_1
	goto Label10
Label9:
	iconst_0
Label10:
	ifle Label8
	iload 4
invokestatic io/int2str(I)Ljava/lang/String;
	ldc "^2 = "
	invokevirtual java/lang/String/concat(Ljava/lang/String;)Ljava/lang/String;
	iload 4
	invokestatic HLang/square(I)I
invokestatic io/int2str(I)Ljava/lang/String;
	invokevirtual java/lang/String/concat(Ljava/lang/String;)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	goto Label7
Label8:
Label7:
Label4:
iinc 3 1
	goto Label2
Label3:
	return
Label1:
.limit stack 18
.limit locals 5
.end method

.method public <init>()V
.var 0 is this LHLang; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
	return
Label1:
.limit stack 1
.limit locals 1
.end method
