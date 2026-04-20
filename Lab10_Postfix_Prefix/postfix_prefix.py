"""
Lab 10 - Intermediate Code Generation: Postfix and Prefix
"""

# ── Simple expression parser ──────────────────────────────────────────────────
# Supports: +  -  *  /  ^  and parentheses
# Precedence: ^ > * / > + -

PREC = {'+':1, '-':1, '*':2, '/':2, '^':3}
RIGHT_ASSOC = {'^'}

def tokenize(expr):
    tokens, i = [], 0
    while i < len(expr):
        if expr[i].isspace(): i += 1; continue
        if expr[i].isalnum():
            j = i
            while j < len(expr) and expr[j].isalnum(): j += 1
            tokens.append(expr[i:j]); i = j
        else:
            tokens.append(expr[i]); i += 1
    return tokens

def to_postfix(expr):
    """Infix → Postfix (Shunting-Yard)"""
    out, stack = [], []
    for tok in tokenize(expr):
        if tok not in PREC and tok not in '()':
            out.append(tok)
        elif tok == '(':
            stack.append(tok)
        elif tok == ')':
            while stack and stack[-1] != '(': out.append(stack.pop())
            stack.pop()
        else:
            while (stack and stack[-1] in PREC and
                   ((tok not in RIGHT_ASSOC and PREC[stack[-1]] >= PREC[tok]) or
                    (tok in RIGHT_ASSOC and PREC[stack[-1]] > PREC[tok]))):
                out.append(stack.pop())
            stack.append(tok)
    while stack: out.append(stack.pop())
    return ' '.join(out)

def to_prefix(expr):
    """Infix → Prefix (reverse shunting-yard)"""
    tokens = tokenize(expr)[::-1]
    flipped = {'(': ')', ')': '('}
    tokens = [flipped.get(t, t) for t in tokens]
    out, stack = [], []
    for tok in tokens:
        if tok not in PREC and tok not in '()':
            out.append(tok)
        elif tok == '(':
            stack.append(tok)
        elif tok == ')':
            while stack and stack[-1] != '(': out.append(stack.pop())
            stack.pop()
        else:
            while (stack and stack[-1] in PREC and
                   ((tok in RIGHT_ASSOC and PREC[stack[-1]] >= PREC[tok]) or
                    (tok not in RIGHT_ASSOC and PREC[stack[-1]] > PREC[tok]))):
                out.append(stack.pop())
            stack.append(tok)
    while stack: out.append(stack.pop())
    return ' '.join(reversed(out))

def eval_postfix(expr):
    """Evaluate a postfix expression (numeric only)."""
    stack = []
    for tok in expr.split():
        if tok.lstrip('-').isdigit():
            stack.append(float(tok))
        else:
            b, a = stack.pop(), stack.pop()
            stack.append({'+':a+b,'-':a-b,'*':a*b,'/':a/b,'^':a**b}[tok])
    return stack[0]

if __name__ == "__main__":
    exprs = [
        "a + b * c",
        "a + b * c - d / e",
        "(a + b) * (c - d)",
        "a ^ b ^ c",
        "3 + 4 * 2",
    ]
    print(f"  {'Infix':<25} {'Postfix':<30} {'Prefix'}")
    print("  " + "-" * 75)
    for e in exprs:
        print(f"  {e:<25} {to_postfix(e):<30} {to_prefix(e)}")

    print("\n  Postfix Evaluation (numeric):")
    for e in ["3 + 4 * 2", "(3 + 4) * 2"]:
        pf = to_postfix(e)
        print(f"  {e} = {int(eval_postfix(pf))}   (postfix: {pf})")
