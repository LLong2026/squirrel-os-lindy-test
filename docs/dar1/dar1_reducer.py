#!/usr/bin/env python3
"""DAR-1 — Deterministic Algebra Reducer v1.0

Translates a restricted subset of service/playbook-style JavaScript into a
canonical algebraic step-relation form. Pure function of the input text:
same input, same output, every time. Checksums prove it.

Honesty contract (the anti-Rosetta clause):
  - Constructs outside the supported subset are REJECTED with an explicit
    UNSUPPORTED error naming the construct. Never a canned or approximate
    output. A rejected reduction is a correct answer, not a failure.

Supported subset:
  - exactly one function
  - pre-loop `let`/`const` declarations (state initialization)
  - exactly ONE `while` loop (the step relation)
  - inside the loop: declarations, assignments, x++/x+=, queue push/shift,
    if / if-else (max 4 combined cases)
  - a single `return` after the loop (the result)

Canonical operators: head(), tail(), len(), append(), ∧ ∨ ¬ = ≠ < ≤ > ≥
"""
import sys

class Unsupported(Exception):
    pass

# ---------------- tokenizer ----------------
PUNCT = ['===','!==','==','!=','<=','>=','&&','||','++','+=',
         '(',')','{','}',';',',','.','<','>','=','+','-','*','/','[',']','!']

def tokenize(src):
    toks = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c.isspace():
            i += 1
            continue
        if c.isalpha() or c == '_':
            j = i
            while j < n and (src[j].isalnum() or src[j] == '_'):
                j += 1
            toks.append(('id', src[i:j]))
            i = j
            continue
        if c.isdigit():
            j = i
            while j < n and src[j].isdigit():
                j += 1
            toks.append(('num', src[i:j]))
            i = j
            continue
        if c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 1
            toks.append(('str', src[i+1:j]))
            i = j + 1
            continue
        for p in PUNCT:
            if src.startswith(p, i):
                toks.append(('p', p))
                i += len(p)
                break
        else:
            raise Unsupported(f"unexpected character {c!r}")
    toks.append(('eof', ''))
    return toks

# ---------------- parser (recursive descent) ----------------
KEYWORDS = {'function','let','const','while','if','else','return'}

class Parser:
    def __init__(self, toks):
        self.toks = toks
        self.i = 0

    def peek(self):
        return self.toks[self.i]

    def next(self):
        t = self.toks[self.i]
        self.i += 1
        return t

    def at(self, val):
        return self.toks[self.i][1] == val

    def expect(self, val):
        t = self.next()
        if t[1] != val:
            raise Unsupported(f"expected {val!r}, got {t[1]!r}")

    # ---- statements ----
    def parse_program(self):
        t = self.peek()
        if t[1] != 'function':
            raise Unsupported("input must be a single function")
        fn = self.parse_function()
        if self.peek()[0] != 'eof':
            raise Unsupported("trailing content after function")
        return fn

    def parse_function(self):
        self.expect('function')
        name = self.next()[1]
        self.expect('(')
        params = []
        while not self.at(')'):
            params.append(self.next()[1])
            if self.at(','):
                self.next()
        self.expect(')')
        body = self.parse_block()
        return {'name': name, 'params': params, 'body': body}

    def parse_block(self):
        self.expect('{')
        stmts = []
        while not self.at('}'):
            stmts.append(self.parse_stmt())
        self.expect('}')
        return stmts

    def parse_stmt(self):
        t = self.peek()
        if t[1] in ('let', 'const'):
            self.next()
            var = self.next()[1]
            init = None
            if self.at('='):
                self.next()
                init = self.parse_expr()
            self.expect(';')
            return {'type': 'decl', 'var': var, 'init': init}
        if t[1] == 'while':
            self.next()
            self.expect('(')
            cond = self.parse_expr()
            self.expect(')')
            body = self.parse_block()
            return {'type': 'while', 'cond': cond, 'body': body}
        if t[1] == 'if':
            return self.parse_if()
        if t[1] == 'return':
            self.next()
            e = None
            if not self.at(';'):
                e = self.parse_expr()
            self.expect(';')
            return {'type': 'return', 'expr': e}
        if t[1] == 'function':
            raise Unsupported("nested functions not supported")
        e = self.parse_expr()
        self.expect(';')
        return {'type': 'exprstmt', 'expr': e}

    def parse_if(self):
        self.expect('if')
        self.expect('(')
        cond = self.parse_expr()
        self.expect(')')
        then = self.parse_block()
        els = None
        if self.at('else'):
            self.next()
            if self.at('if'):
                els = [self.parse_if()]
            else:
                els = self.parse_block()
        return {'type': 'if', 'cond': cond, 'then': then, 'els': els}

    # ---- expressions ----
    def parse_expr(self):
        lhs = self.parse_or()
        if self.at('='):
            self.next()
            rhs = self.parse_expr()
            return {'type': 'assign', 'target': lhs, 'value': rhs}
        if self.at('++'):
            self.next()
            return {'type': 'postinc', 'target': lhs}
        if self.at('+='):
            self.next()
            rhs = self.parse_expr()
            return {'type': 'addeq', 'target': lhs, 'value': rhs}
        return lhs

    def parse_or(self):
        e = self.parse_and()
        while self.at('||'):
            self.next()
            e = {'type': 'bin', 'op': '||', 'l': e, 'r': self.parse_and()}
        return e

    def parse_and(self):
        e = self.parse_eq()
        while self.at('&&'):
            self.next()
            e = {'type': 'bin', 'op': '&&', 'l': e, 'r': self.parse_eq()}
        return e

    def parse_eq(self):
        e = self.parse_rel()
        while self.peek()[1] in ('==', '===', '!=', '!=='):
            op = self.next()[1]
            e = {'type': 'bin', 'op': op, 'l': e, 'r': self.parse_rel()}
        return e

    def parse_rel(self):
        e = self.parse_add()
        while self.peek()[1] in ('<', '>', '<=', '>='):
            op = self.next()[1]
            e = {'type': 'bin', 'op': op, 'l': e, 'r': self.parse_add()}
        return e

    def parse_add(self):
        e = self.parse_mul()
        while self.peek()[1] in ('+', '-'):
            op = self.next()[1]
            e = {'type': 'bin', 'op': op, 'l': e, 'r': self.parse_mul()}
        return e

    def parse_mul(self):
        e = self.parse_unary()
        while self.peek()[1] in ('*', '/'):
            op = self.next()[1]
            e = {'type': 'bin', 'op': op, 'l': e, 'r': self.parse_unary()}
        return e

    def parse_unary(self):
        if self.at('!'):
            self.next()
            return {'type': 'un', 'op': '!', 'e': self.parse_unary()}
        return self.parse_postfix()

    def parse_postfix(self):
        e = self.parse_primary()
        while True:
            if self.at('.'):
                self.next()
                prop = self.next()[1]
                e = {'type': 'member', 'obj': e, 'prop': prop}
            elif self.at('('):
                self.next()
                args = []
                while not self.at(')'):
                    args.append(self.parse_expr())
                    if self.at(','):
                        self.next()
                self.expect(')')
                e = {'type': 'call', 'callee': e, 'args': args}
            elif self.at('['):
                raise Unsupported("indexing [...] not supported in DAR-1 subset")
            else:
                break
        return e

    def parse_primary(self):
        t = self.peek()
        if t[0] == 'num':
            self.next()
            return {'type': 'num', 'v': t[1]}
        if t[0] == 'str':
            self.next()
            return {'type': 'str', 'v': t[1]}
        if t[1] == '(':
            self.next()
            e = self.parse_expr()
            self.expect(')')
            return e
        if t[0] == 'id':
            if t[1] in KEYWORDS:
                raise Unsupported(f"unexpected keyword {t[1]!r} in expression")
            self.next()
            return {'type': 'id', 'name': t[1]}
        raise Unsupported(f"unexpected token {t[1]!r}")

# ---------------- AST analysis ----------------
def walk(node, fn):
    if isinstance(node, dict):
        fn(node)
        for v in node.values():
            walk(v, fn)
    elif isinstance(node, list):
        for v in node:
            walk(v, fn)

def classify(fn):
    arrays, assigned, members = set(), set(), set()
    def visit(n):
        t = n.get('type')
        if t == 'member':
            if n['prop'] in ('length', 'push', 'shift') and n['obj'].get('type') == 'id':
                arrays.add(n['obj']['name'])
        elif t in ('assign', 'postinc', 'addeq'):
            if n['target'].get('type') == 'id':
                assigned.add(n['target']['name'])
            else:
                raise Unsupported("assignment to a property is outside the DAR-1 subset")
    walk(fn['body'], visit)
    return arrays, assigned

# ---------------- rendering ----------------
SUB = 'ₜ'
BINOP = {'&&': ' ∧ ', '||': ' ∨ ', '==': ' = ', '===': ' = ',
         '!=': ' ≠ ', '!==': ' ≠ ', '<': ' < ', '<=': ' ≤ ',
         '>': ' > ', '>=': ' ≥ ', '+': ' + ', '-': ' - ',
         '*': ' · ', '/': ' / '}

def render(node, env, params):
    t = node['type']
    if t == 'num':
        return node['v']
    if t == 'str':
        return f"\"{node['v']}\""
    if t == 'id':
        name = node['name']
        if name in env:
            return env[name]
        if name in params:
            return name
        return name + SUB
    if t == 'member':
        obj = render(node['obj'], env, params)
        if node['prop'] == 'length':
            return f"len({obj})"
        return f"{obj}.{node['prop']}"
    if t == 'bin':
        l = render(node['l'], env, params)
        r = render(node['r'], env, params)
        return f"({l}{BINOP[node['op']]}{r})"
    if t == 'un':
        return f"¬({render(node['e'], env, params)})"
    if t == 'call':
        c = node['callee']
        if c['type'] == 'id':
            args = ', '.join(render(a, env, params) for a in node['args'])
            return f"{c['name']}({args})"
        raise Unsupported(f"method call .{c.get('prop')}() in an expression is outside the subset")
    raise Unsupported(f"expression node {t!r} outside subset")

# ---------------- reduction ----------------
def reduce_js(src):
    fn = Parser(tokenize(src)).parse_program()
    params = set(fn['params'])
    arrays, assigned = classify(fn)
    body = fn['body']

    whiles = [s for s in body if s['type'] == 'while']
    returns = [s for s in body if s['type'] == 'return']
    if len(whiles) != 1:
        raise Unsupported("exactly ONE while loop is required (the step relation)")
    if len(returns) != 1 or body[-1]['type'] != 'return':
        raise Unsupported("a single return after the loop is required")
    if returns[0] is not body[-1]:
        raise Unsupported("return must be the final statement")
    w = whiles[0]
    idx = body.index(w)
    pre = body[:idx]
    post = body[idx+1:-1]
    if post:
        raise Unsupported("no statements allowed between the loop and the return")
    for s in pre:
        if s['type'] != 'decl' or s['init'] is None:
            raise Unsupported("pre-loop statements must be initialized declarations")

    # state variables
    pre_vars = [s['var'] for s in pre]
    state_arrays = [a for a in arrays]
    state_scalars = [v for v in pre_vars if v not in arrays] + \
                    [v for v in sorted(assigned - set(pre_vars) - arrays)]
    state_order = state_arrays + state_scalars
    if not state_order:
        raise Unsupported("no state variables found")

    # init section
    init_env = {}
    inits = []
    for s in pre:
        expr = render(s['init'], init_env, params)
        init_env[s['var']] = expr
        inits.append(f"{s['var']}₀ = {expr}")
    for v in state_order:
        if v not in init_env:
            if v in params:
                inits.append(f"{v}₀ = {v}")
            else:
                raise Unsupported(f"state variable {v!r} is never initialized")

    # guard (evaluated at time t, before the step)
    guard_env = {v: v + SUB for v in state_order}
    guard = render(w['cond'], guard_env, params)

    # process the loop body
    intermediates = []          # (symbol, definition)
    def base_env():
        return {}

    def process_stmts(stmts, env):
        """Process straight-line stmts into env. Locals get symbol names."""
        for s in stmts:
            if s['type'] == 'decl':
                if s['init'] is None:
                    raise Unsupported(f"declaration of {s['var']} without initializer")
                init = s['init']
                if (init['type'] == 'call' and init['callee'].get('type') == 'member'
                        and init['callee']['prop'] == 'shift'):
                    q = init['callee']['obj']
                    if q['type'] != 'id':
                        raise Unsupported("shift() on a non-variable is outside the subset")
                    qname = q['name']
                    cur = env.get(qname, qname + SUB)
                    sym = s['var'] + SUB
                    intermediates.append((sym, f"head({cur})"))
                    env[s['var']] = sym
                    env[qname] = f"tail({cur})"
                else:
                    sym = s['var'] + SUB
                    intermediates.append((sym, render(init, env, params)))
                    env[s['var']] = sym
            elif s['type'] == 'exprstmt':
                e = s['expr']
                if e['type'] == 'assign':
                    tgt = e['target']
                    if tgt['type'] != 'id':
                        raise Unsupported("assignment target must be a variable")
                    env[tgt['name']] = render(e['value'], env, params)
                elif e['type'] == 'postinc':
                    tgt = e['target']
                    if tgt['type'] != 'id':
                        raise Unsupported("++ target must be a variable")
                    cur = env.get(tgt['name'], tgt['name'] + SUB)
                    env[tgt['name']] = f"({cur} + 1)"
                elif e['type'] == 'addeq':
                    tgt = e['target']
                    if tgt['type'] != 'id':
                        raise Unsupported("+= target must be a variable")
                    cur = env.get(tgt['name'], tgt['name'] + SUB)
                    env[tgt['name']] = f"({cur} + {render(e['value'], env, params)})"
                elif e['type'] == 'call' and e['callee'].get('type') == 'member':
                    if e['callee']['prop'] == 'push':
                        q = e['callee']['obj']
                        if q['type'] != 'id':
                            raise Unsupported("push() on a non-variable is outside the subset")
                        qname = q['name']
                        cur = env.get(qname, qname + SUB)
                        val = render(e['args'][0], env, params) if e['args'] else '_'
                        env[qname] = f"append({cur}, {val})"
                    elif e['callee']['prop'] == 'shift':
                        raise Unsupported("bare shift() statement discards data; bind it instead")
                    else:
                        raise Unsupported(f"method call .{e['callee']['prop']}() outside subset")
                else:
                    raise Unsupported("statement has no algebraic meaning in the subset")
            else:
                raise Unsupported(f"statement type {s['type']!r} inside the loop is outside subset")

    # split common prefix vs if-branches
    loop_body = w['body']
    has_if = any(s['type'] == 'if' for s in loop_body)

    env_c = {}
    cases = [('⊤', {})]

    # walk body, expanding ifs
    def process_all(stmts, cases):
        common = []
        for s in stmts:
            if s['type'] == 'if':
                # flush common stmts into every case
                for g, e in cases:
                    process_stmts(common, e)
                common = []
                new = []
                for g, e in cases:
                    cond = render(s['cond'], e, params)
                    e_then = dict(e)
                    process_stmts(s['then'], e_then)
                    new.append((f"({g} ∧ {cond})" if g != '⊤' else f"({cond})", e_then))
                    e_else = dict(e)
                    if s['els']:
                        process_stmts(s['els'], e_else)
                    new.append((f"({g} ∧ ¬({cond}))" if g != '⊤' else f"(¬({cond}))", e_else))
                if len(new) > 4:
                    raise Unsupported("more than 4 combined if-branches is outside subset")
                cases = new
            else:
                common.append(s)
        for g, e in cases:
            process_stmts(common, e)
        return cases

    if has_if:
        cases = process_all(loop_body, cases)
    else:
        process_stmts(loop_body, env_c)

    # ---- emit ----
    out = []
    out.append(f"map: {fn['name']}")
    state_desc = ', '.join(f"{v} ({'sequence' if v in arrays else 'scalar'})" for v in state_order)
    out.append(f"state: {state_desc}")
    out.append("init:  " + ' ; '.join(inits))
    out.append(f"guard: Gₜ ≡ {guard}")

    # intermediates defined in the common path
    seen = set()
    common_intermediates = []
    if not has_if:
        common_intermediates = list(intermediates)
    else:
        # intermediates recorded during case processing: keep those from the
        # first case (common prefix order is identical across cases)
        for sym, d in intermediates:
            if sym not in seen:
                seen.add(sym)
                common_intermediates.append((sym, d))

    if has_if:
        # star-intermediates for state vars changed on the common path:
        # derive from the ⊤-base before first if = min over case envs of
        # values that appear in every case identically AND differ from vₜ
        base = {}
        for v in state_order:
            vals = {e.get(v, v + SUB) for g, e in cases}
            if len(vals) == 1:
                base[v] = vals.pop()
        for sym, d in common_intermediates:
            out.append(f"{sym} = {d}")
        for v in state_order:
            if v in base and base[v] != v + SUB:
                out.append(f"{v}ₜ* = {base[v]}")
                for g, e in cases:
                    if e.get(v, v + SUB) == base[v]:
                        e[v] = f"{v}ₜ*"
        out.append("cases:")
        for g, e in cases:
            updates = ' ; '.join(
                f"{v}ₜ₊₁ = {e.get(v, v + SUB)}" for v in state_order)
            out.append(f"  {g} : {updates}")
    else:
        for sym, d in common_intermediates:
            out.append(f"{sym} = {d}")
        updates = ' ; '.join(
            f"{v}ₜ₊₁ = {env_c.get(v, v + SUB)}" for v in state_order)
        out.append(f"step: {updates}")

    out.append("termination: τ = min{ t ≥ 0 : ¬Gₜ }")
    ret_env = {v: f"{v}_τ" for v in state_order}
    ret_expr = fn['body'][-1]['expr']
    if ret_expr is None:
        raise Unsupported("return without a value is outside subset")
    result = render(ret_expr, ret_env, params)
    out.append(f"result: {result}")
    return '\n'.join(out)


def main():
    if len(sys.argv) != 2:
        print("usage: dar1_reducer.py <file.js>")
        sys.exit(2)
    src = open(sys.argv[1], encoding='utf-8').read()
    try:
        print(reduce_js(src))
    except Unsupported as e:
        print(f"UNSUPPORTED: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
