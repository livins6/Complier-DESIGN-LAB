"""
Lab 12 - Simple Code Generator
Generates assembly-like target code from Three-Address Code (TAC)
using a register descriptor and address descriptor.
"""

REGISTERS = ['R0', 'R1', 'R2', 'R3']

class CodeGenerator:
    def __init__(self):
        self.reg_desc  = {r: None for r in REGISTERS}   # reg -> var
        self.addr_desc = {}   # var -> location (reg or memory)
        self.code = []

    def get_reg(self, prefer=None):
        # Return free register, or preferred, or spill LRU
        if prefer and self.reg_desc[prefer] is None:
            return prefer
        for r in REGISTERS:
            if self.reg_desc[r] is None:
                return r
        # Spill first register
        r = REGISTERS[0]
        var = self.reg_desc[r]
        self.emit(f"ST  {r}, {var}")
        self.addr_desc[var] = var
        self.reg_desc[r] = None
        return r

    def load(self, var):
        # Already in a register?
        for r, v in self.reg_desc.items():
            if v == var:
                return r
        # Load from memory
        r = self.get_reg()
        self.emit(f"LD  {r}, {var}")
        self.reg_desc[r] = var
        self.addr_desc[var] = r
        return r

    def emit(self, instr):
        self.code.append(instr)

    def generate(self, tac):
        """
        tac: list of (result, op, arg1, arg2)
             op can be +,-,*,/  or 'assign' for copies
        """
        op_map = {'+':'ADD', '-':'SUB', '*':'MUL', '/':'DIV'}
        for result, op, arg1, arg2 in tac:
            if op == 'assign':
                r = self.load(arg1)
                # Store to result
                self.emit(f"ST  {r}, {result}")
                self.addr_desc[result] = result
            else:
                r1 = self.load(arg1)
                r2 = self.load(arg2) if arg2 else None
                r_res = self.get_reg()
                if r2:
                    self.emit(f"{op_map[op]:<4}{r_res}, {r1}, {r2}   ; {result} = {arg1} {op} {arg2}")
                self.reg_desc[r_res] = result
                self.addr_desc[result] = r_res
        # Store all live variables back
        for r, var in self.reg_desc.items():
            if var:
                self.emit(f"ST  {r}, {var}")

    def print_code(self):
        print("\n  Generated Target Code:")
        print("  " + "-" * 35)
        for line in self.code:
            print(f"    {line}")

if __name__ == "__main__":
    # Three-address code for: t1=b*c, t2=a+t1, t3=t2-d
    tac_examples = [
        {
            "desc": "a + b * c - d",
            "tac": [
                ('t1', '*', 'b', 'c'),
                ('t2', '+', 'a', 't1'),
                ('t3', '-', 't2', 'd'),
            ]
        },
        {
            "desc": "(a + b) * (c - d)",
            "tac": [
                ('t1', '+', 'a', 'b'),
                ('t2', '-', 'c', 'd'),
                ('t3', '*', 't1', 't2'),
            ]
        },
    ]

    for ex in tac_examples:
        print("\n" + "=" * 45)
        print(f"  Expression : {ex['desc']}")
        print("\n  Three-Address Code:")
        for r, op, a, b in ex['tac']:
            print(f"    {r} = {a} {op} {b}")
        cg = CodeGenerator()
        cg.generate(ex['tac'])
        cg.print_code()
