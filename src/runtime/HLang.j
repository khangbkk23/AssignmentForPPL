.source HLang.java
.class public HLang
.super java/lang/Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
.var 1 is mixed [[F from Label0 to Label1
	iconst_2
anewarray [F
dup
	iconst_0
	iconst_2
	newarray float
dup
	iconst_0
	fconst_1
fastore
dup
	iconst_1
	fconst_2
fastore
aastore
dup
	iconst_1
	iconst_2
	newarray float
dup
	iconst_0
	ldc 3.1000
fastore
dup
	iconst_1
	ldc 4.2000
fastore
aastore
	astore_1
	aload_1
	iconst_0
aaload
	iconst_0
faload
	invokestatic io/float2str(F)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
	return
Label1:
.limit stack 23
.limit locals 2
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
