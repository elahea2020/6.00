# Problem Set 4A
# Name: Elaheh Ahmadi
# Collaborators: N/A
# Time Spent: 1:30
# Late Days Used: 0

# Part A0: Data representation
# Fill out the following variables correctly.
# If correct, the tests named data_representation should pass.
tree1 = [[1, 10], 2]
tree2 = [[15, 9], [[9, 7], 10]]
tree3 = [[12], [2, 4, 2], [6]]


# Part A1: Multiplication on tree leaves

def mul_tree(tree):
    """
    Recursively computes the product of all tree leaves.
    Returns an integer representing the product.

    Inputs
       tree: A list (potentially containing sublists) that
       represents a tree structure.
    Outputs
       total: An int equal to the product of all leaves of the tree.

    """
    # The base case that should return 1 to avoid changing the product
    if len(tree) == 0:
        return 1
    # If the left child of the tree is a leave the function should return the product of the value of the leave times
    # the product of the rest of the tree
    elif type(tree[0]) == int:
        return tree[0] * mul_tree(tree[1:])
    # If the left most child is also a tree then the function should multiply the result of the left child and the
    #  rest of the tree
    else:
        return mul_tree(tree[0])*mul_tree(tree[1:])





# Part A2: Arbitrary operations on tree leaves

def addem(a,b):
    """
    Example operator function.
    Takes in two integers, returns their sum.
    """
    return a + b


def prod(a,b):
    """
    Example operator function.
    Takes in two integers, returns their product.
    """
    return a * b


def operate_tree(tree, op, base_case):
    """
    Recursively runs a given operation on tree leaves.
    Return type depends on the specific operation.

    Inputs
       tree: A list (potentially containing sublists) that
       represents a tree structure.
       op: A function that takes in two inputs and returns the
       result of a specific operation on them.
       base_case: What the operation should return as a result
       in the base case (i.e. when the tree is empty).
    """
    if len(tree) == 0:
        return base_case
    # If the left child of the tree is a leave the function should return the result of the function op on the value of
    # the leave and the function of the operate_tree
    elif type(tree[0]) == int:
        return op(tree[0], operate_tree(tree[1:], op, base_case))
    # If the left most child is also a tree then the function should return the result of the op function on the
    # operate_tree on the most left child and the rest of the tree
    else:
        return op(operate_tree(tree[0], op,base_case), operate_tree(tree[1:], op, base_case))

# Part A3: Searching a tree


def search_odd(a, b):
    """
    Operator function that searches for odd values within its inputs.

    Inputs
        a, b: integers or booleans
    Outputs
        True if either input is equal to True or odd, and False otherwise
    """
    # Here I accounted all of the different base cases that might occur and will return True or False if there was an
    #  odd integer or not.
    if type(a) == bool and type(b) == bool:
        return a or b
    elif type(a) == bool and type(b) == int:
        return a or (b % 2 == 1)
    elif type(a) == int and type(b) == bool:
        return b or (a % 2 == 1)
    elif type(a) == int and type(b) == int:
        return (a % 2 == 1) or (b % 2 == 1)


if __name__ == '__main__':
    # You can use this part for your own testing and debugging purposes.
    # Do not erase the pass statement below.
    # tree4 = [[15, 9], [[9, 7], 11]]
    # print(operate_tree(tree2,search_odd,False))
    # print(operate_tree(tree3,search_odd,False))
    # print(operate_tree(tree1,search_odd,False))
    # print(operate_tree(tree4,search_odd,False))
    mul_tree(tree1)