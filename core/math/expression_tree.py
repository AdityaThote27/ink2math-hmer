# core/hmer/math/expression_tree.py

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def to_infix(self):
        # Leaf node (digit)
        if self.left is None and self.right is None:
            return str(self.value)

        # Internal node (operator)
        left_expr = self.left.to_infix()
        right_expr = self.right.to_infix()
        return f"({left_expr}{self.value}{right_expr})"


def precedence(op):
    if op == '+':
        return 1
    if op == '*':
        return 2
    return 0


def build_expression_tree(symbols, debug=False):
    """
    Converts a symbol list like ['3', '+', '4', '*', '5']
    into an AST respecting operator precedence.
    """

    operands = []
    operators = []

    def apply_operator():
        op = operators.pop()
        right = operands.pop()
        left = operands.pop()
        node = Node(op, left, right)
        operands.append(node)

        if debug:
            print(f"[AST] Applied operator: {op}")

    for sym in symbols:
        if sym.isdigit():
            operands.append(Node(sym))
            if debug:
                print(f"[AST] Pushed operand: {sym}")

        elif sym in ['+', '*']:
            while (
                operators
                and precedence(operators[-1]) >= precedence(sym)
            ):
                apply_operator()

            operators.append(sym)
            if debug:
                print(f"[AST] Pushed operator: {sym}")

    while operators:
        apply_operator()

    return operands[0]
