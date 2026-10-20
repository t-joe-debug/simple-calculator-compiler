# Grammar Transformations & Derivations

  **Top-Down Predictive LL(1) Parsing**.

---

## 1. Why We Need Grammar Transformations

Top-down recursive descent parsers cannot handle:
1. **Ambiguity:** An ambiguous grammar creates more than one parse tree for the same input string (e.g. `id + id * id`).
2. **Left Recursion:** If a grammar has $A \to A\alpha$, calling `A()` will call `A()` again immediately without consuming any input, causing an infinite loop.
3. **Common Prefixes:** If two productions start with the same symbol, the parser cannot decide which rule to choose with 1 lookahead symbol.

---

## 2. Step 1: Removing Ambiguity & Adding Precedence

### Natural Ambiguous Grammar:
```text
E -> E + E | E - E | E * E | E / E | ( E ) | id | num
```
For input `id + id * id`, this grammar produces 2 parse trees:
- Tree 1: `(id + id) * id`
- Tree 2: `id + (id * id)`

### Unambiguous Grammar (Stratification):
We divide the grammar into three levels:
- `E` for `+` and `-` (lowest precedence, left associative)
- `T` for `*` and `/` (medium precedence, left associative)
- `F` for `( )`, `id`, `num` (highest precedence)

```text
E -> E + T | E - T | T
T -> T * F | T / F | F
F -> ( E ) | id | num
```

---

## 3. Step 2: Eliminating Left Recursion

From our course notes:
$$\text{If } A \to A\alpha \mid \beta$$
$$\text{Replace with: } A \to \beta A' \quad \text{and} \quad A' \to \alpha A' \mid \varepsilon$$

### Applying to $E$:
Here $A = E$, $\alpha_1 = + T$, $\alpha_2 = - T$, $\beta = T$:
```text
E  -> T E'
E' -> + T E'
    | - T E'
    | ε
```

### Applying to $T$:
Here $A = T$, $\alpha_1 = * F$, $\alpha_2 = / F$, $\beta = F$:
```text
T  -> F T'
T' -> * F T'
    | / F T'
    | ε
```

### Production for $F$:
$F$ has no left recursion:
```text
F -> ( E )
   | id
   | num
```

---

## 4. Step 3: Checking Left Factoring

Left factoring is needed when rules have common prefixes:
$$A \to \alpha\beta_1 \mid \alpha\beta_2 \implies A \to \alpha A', \quad A' \to \beta_1 \mid \beta_2$$

Let us check our statement rules:
```text
Stmt -> id = E ;
      | print ( E ) ;
```
- Rule 1 starts with `id`.
- Rule 2 starts with `print`.

Since `id` and `print` are different tokens, there are **no common prefixes**. No left factoring is needed.

---

## 5. Step 4: Computing FIRST and FOLLOW Sets

### Rules from Slides:
- **Rule 1:** $\text{FIRST}(a) = \{a\}$ for terminal $a$.
- **Rule 2:** If $X \to \varepsilon$, then $\varepsilon \in \text{FIRST}(X)$.
- **Rule 3:** For start symbol, place $\$$ in $\text{FOLLOW}(\text{Start})$.
- **Rule 4:** If $A \to \alpha B \beta$, then $\text{FIRST}(\beta) \setminus \{\varepsilon\} \subseteq \text{FOLLOW}(B)$. If $\beta \Rightarrow^* \varepsilon$, then $\text{FOLLOW}(A) \subseteq \text{FOLLOW}(B)$.

### Computed FIRST Sets:
- $\text{FIRST}(F) = \{ (, \text{id}, \text{num} \}$
- $\text{FIRST}(T') = \{ *, /, \varepsilon \}$
- $\text{FIRST}(T) = \text{FIRST}(F) = \{ (, \text{id}, \text{num} \}$
- $\text{FIRST}(E') = \{ +, -, \varepsilon \}$
- $\text{FIRST}(E) = \text{FIRST}(T) = \{ (, \text{id}, \text{num} \}$
- $\text{FIRST}(Stmt) = \{ \text{id}, \text{print} \}$
- $\text{FIRST}(StmtList) = \{ \text{id}, \text{print}, \varepsilon \}$
- $\text{FIRST}(Program) = \{ \text{id}, \text{print}, \$ \}$

### Computed FOLLOW Sets:
- $\text{FOLLOW}(Program) = \{ \$ \}$
- $\text{FOLLOW}(StmtList) = \{ \$ \}$
- $\text{FOLLOW}(Stmt) = \{ \text{id}, \text{print}, \$ \}$
- $\text{FOLLOW}(E) = \{ ;, ) \}$
- $\text{FOLLOW}(E') = \text{FOLLOW}(E) = \{ ;, ) \}$
- $\text{FOLLOW}(T) = \{ +, -, ;, ) \}$
- $\text{FOLLOW}(T') = \text{FOLLOW}(T) = \{ +, -, ;, ) \}$
- $\text{FOLLOW}(F) = \{ *, /, +, -, ;, ) \}$

---

## 6. Step 5: LL(1) Parsing Table for Expressions

Using our course procedure to fill table $M[\text{Non-Terminal}, \text{Terminal}]$:

| Non-Terminal | `id` | `num` | `+` | `-` | `*` | `/` | `(` | `)` | `;` | `$` |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **E** | $E \to T E'$ | $E \to T E'$ | | | | | $E \to T E'$ | | | |
| **E'** | | | $E' \to + T E'$ | $E' \to - T E'$ | | | | $E' \to \varepsilon$ | $E' \to \varepsilon$ | |
| **T** | $T \to F T'$ | $T \to F T'$ | | | | | $T \to F T'$ | | | |
| **T'** | | | $T' \to \varepsilon$ | $T' \to \varepsilon$ | $T' \to * F T'$ | $T' \to / F T'$ | | $T' \to \varepsilon$ | $T' \to \varepsilon$ | |
| **F** | $F \to \text{id}$ | $F \to \text{num}$ | | | | | $F \to ( E )$ | | | |

**Result:** Every cell contains at most one rule. Therefore, this grammar is **strictly LL(1)** and can be parsed with zero backtracking.
