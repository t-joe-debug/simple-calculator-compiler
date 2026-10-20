# Grammar Test Cases & Verification Suite

These test cases test whether our Simple Calculator Language grammar works correctly.

---

## 1. Valid Test Cases (Should Pass)

### Test 1: Simple Assignment and Print
- **Input:**
  ```text
  x = 42;
  print(x);
  ```
- **Derivation:**
  - `StmtList` -> `Stmt StmtList`
  - `Stmt` -> `id = E ;` where `id = x`, `E -> T E' -> F T' E' -> num` (`42`)
  - Next `Stmt` -> `print ( E ) ;` where `E -> id` (`x`)
- **Expected Result:** Accepted. Valid program with 2 statements.

---

### Test 2: Operator Precedence (`*` over `+`)
- **Input:**
  ```text
  res = 2 + 3 * 4;
  ```
- **Parse Structure:**
  - `E` -> `T + T`
  - First `T` -> `2`
  - Second `T` -> `3 * 4`
- **Resulting AST:**
  ```text
       +
      / \
     2   *
        / \
       3   4
  ```
- **Value:** `2 + 12 = 14` (Multiplication happens first).
- **Expected Result:** Accepted.

---

### Test 3: Left-Associativity (`-` and `/`)
- **Input:**
  ```text
  val = 20 - 8 - 2;
  ```
- **Expected Structure:**
  - `(20 - 8) - 2` = `10`
  - Left-to-right evaluation.
- **Expected Result:** Accepted.

---

### Test 4: Parentheses Overriding Precedence
- **Input:**
  ```text
  ans = (2 + 3) * 4;
  ```
- **Parse Structure:**
  - Inside `( )`, `2 + 3` is parsed first as `E`.
  - Then multiplied by `4`.
- **Expected Result:** Accepted.

---

### Test 5: Multiple Variables and Comments
- **Input:**
  ```text
  # calculate area
  w = 5;
  h = 10;
  area = w * h;
  print(area);
  ```
- **Expected Result:** Accepted. Comments and newlines are skipped.

---

## 2. Invalid Test Cases (Should Detect Syntax Error)

### Test 6: Missing Semicolon
- **Input:**
  ```text
  x = 10
  print(x);
  ```
- **Error:** Missing `;` at the end of line 1.
- **Parser Action:** Fails in rule `Stmt -> id = E ;`.

---

### Test 7: Missing Closing Parenthesis in Print
- **Input:**
  ```text
  print(10 + 2;
  ```
- **Error:** Missing `)` before `;`.
- **Parser Action:** Fails in rule `Stmt -> print ( E ) ;`.

---

### Test 8: Two Operators in a Row
- **Input:**
  ```text
  a = 5 + * 3;
  ```
- **Error:** After `+`, an operand (`id`, `num`, or `(`) is expected, but found `*`.
- **Parser Action:** Fails in `F -> ( E ) | id | num`.

---

### Test 9: Number on Left Side of Assignment
- **Input:**
  ```text
  10 = x;
  ```
- **Error:** An assignment statement must begin with an `id`, not a number.
- **Parser Action:** Fails in `Stmt -> id = E ;`.

---

### Test 10: Missing Expression on Right Side
- **Input:**
  ```text
  a = ;
  ```
- **Error:** Expected an expression after `=`.
- **Parser Action:** Fails in `E -> T E'`.

---

### Test 11: Invalid Character
- **Input:**
  ```text
  a = 5 @ 2;
  ```
- **Error:** Character `@` is not a valid token.
- **Lexer Action:** Lexical error reported on character `@`.
