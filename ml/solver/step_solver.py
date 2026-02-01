import ast
import operator


OPS = {
    ast.Add: ("+", operator.add),
    ast.Sub: ("-", operator.sub),
    ast.Mult: ("*", operator.mul),
    ast.Div: ("/", operator.truediv),
    ast.Pow: ("^", operator.pow),
}


def solve_with_steps(expr: str):
    """
    Solve a math expression and return:
    - result
    - step-by-step explanation
    """

    steps = []

    def eval_node(node):
        if isinstance(node, ast.Num):
            return node.n

        if isinstance(node, ast.BinOp):
            left = eval_node(node.left)
            right = eval_node(node.right)
            op_symbol, op_func = OPS[type(node.op)]

            result = op_func(left, right)
            steps.append(f"{left} {op_symbol} {right} = {result}")
            return result

        raise ValueError("Unsupported expression")

    try:
        tree = ast.parse(expr, mode="eval")
        result = eval_node(tree.body)
        return result, steps
    except Exception as e:
        return None, [f"Error solving expression: {e}"]
