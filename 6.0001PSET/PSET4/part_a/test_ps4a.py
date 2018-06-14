# for running unit tests on 6.00/6.0001/6.0002 student code

import unittest
import ps4a as student

# A class that inherits from unittest.TestCase, where each function
# is a test you want to run on the student's code. For a full description
# plus a list of all the possible assert methods you can use, see the
# documentation: https://docs.python.org/3/library/unittest.html#unittest.TestCase
class TestPS4A(unittest.TestCase):
    ### test representation
    def test_data_representation(self):

        student_t1 = student.tree1
        student_t2 = student.tree2
        student_t3 = student.tree3

        # # check lengths
        tree_length_msg = "Your list for %s has length %s, but should be length %s."
        self.assertEqual(len(student_t1), 2, tree_length_msg % ('tree1', len(student.tree1), 2))
        self.assertEqual(len(student_t2), 2, tree_length_msg % ('tree2', len(student.tree2), 2))
        self.assertEqual(len(student_t3), 3, tree_length_msg % ('tree3', len(student.tree3), 3))

        # check children
        self.assertEqual(student_t1[0], [1,10], "The left subtree of tree1 is incorrect.")
        self.assertEqual(student_t1[1], 2, "The right subtree of tree1 is incorrect.")
        self.assertEqual(student_t2[0], [15,9], "The left subtree of tree2 is incorrect.")
        self.assertEqual(student_t2[1], [[9,7],10], "The right subtree of tree2 is incorrect.")
        self.assertEqual(student_t3[0], [12], "The left subtree of tree3 is incorrect.")
        self.assertEqual(student_t3[1], [2,4,2], "The right subtree of tree3 is incorrect.")

    ### tests for add_tree
    def test_mul_example_trees(self):
        expected_1 = 20
        expected_2 = 85050
        expected_3 = 1152

        actual_1 = student.mul_tree([[1,10],2])
        actual_2 = student.mul_tree([[15,9],[[9,7],10]])
        actual_3 = student.mul_tree([[12],[2,4,2],[6]])

        self.assertEqual(actual_1, expected_1, "Expected add(tree1) to be 20, but got %s" % actual_1)
        self.assertEqual(actual_2, expected_2, "Expected add(tree2) to be 85050, but got %s" % actual_2)
        self.assertEqual(actual_3, expected_3, "Expected add(tree3) to be 1152, but got %s" % actual_3)

    ### tests for operate_tree
    def test_op_add_example_trees(self):

        def addem(a,b):
            """
            Example operator function.
            Takes in two integers, returns their sum.
            """
            return a + b

        expected_1 = 13
        expected_2 = 50
        expected_3 = 26

        actual_1 = student.operate_tree([[1,10],2], addem, 0)
        actual_2 = student.operate_tree([[15,9],[[9,7],10]], addem, 0)
        actual_3 = student.operate_tree([[12],[2,4,2],[6]], addem, 0)

        self.assertEqual(actual_1, expected_1, "Expected operate_tree(tree1, addem, 0) to be 13, but got %s" % actual_1)
        self.assertEqual(actual_2, expected_2, "Expected operate_tree(tree2, addem, 0) to be 50, but got %s" % actual_2)
        self.assertEqual(actual_3, expected_3, "Expected operate_tree(tree3, addem, 0) to be 26, but got %s" % actual_3)

    def test_op_prod_example_trees(self):

        def prod(a,b):
            """
            Example operator function.
            Takes in two integers, returns their product.
            """
            return a * b

        expected_1 = 20
        expected_2 = 85050
        expected_3 = 1152

        actual_1 = student.operate_tree([[1,10],2], prod, 1)
        actual_2 = student.operate_tree([[15,9],[[9,7],10]], prod, 1)
        actual_3 = student.operate_tree([[12],[2,4,2],[6]], prod, 1)

        self.assertEqual(actual_1, expected_1, "Expected operate_tree(tree1, prod, 1) to be 20, but got %s" % actual_1)
        self.assertEqual(actual_2, expected_2, "Expected operate_tree(tree2, prod, 1) to be 85050, but got %s" % actual_2)
        self.assertEqual(actual_3, expected_3, "Expected operate_tree(tree3, prod, 1) to be 1152, but got %s" % actual_3)


    def test_op_search_odd_example_trees(self):

        expected_1 = True
        expected_2 = True
        expected_3 = False

        actual_1 = student.operate_tree([[1,10],2], student.search_odd, False)
        actual_2 = student.operate_tree([[15,9],[[9,7],10]], student.search_odd, True)
        actual_3 = student.operate_tree([[12],[2,4,2],[6]], student.search_odd, False)

        self.assertEqual(actual_1, expected_1, "Expected operate_tree(tree1, search_odd, False) to be True, but got %s" % actual_1)
        self.assertEqual(actual_2, expected_2, "Expected operate_tree(tree2, search_odd, False) to be True, but got %s" % actual_2)
        self.assertEqual(actual_3, expected_3, "Expected operate_tree(tree3, search_odd, False) to be False, but got %s" % actual_3)


# Dictionary mapping function names from the above TestCase class to
# the point value each test is worth.
point_values = {
	'test_data_representation' : 0,
	'test_mul_example_trees' : 0.5,
	'test_op_add_example_trees' : 0.5,
	'test_op_prod_example_trees' : 0.5,
	'test_op_search_odd_example_trees': 0.5
}

# Subclass to track a point score and appropriate
# grade comment for a suit of unit tests
class Results_600(unittest.TextTestResult):

    # We override the init method so that the Result object
    # can store the score and appropriate test output.
    def __init__(self, *args, **kwargs):
        super(Results_600, self).__init__(*args, **kwargs)
        self.output = []
        self.points = 2

    def addFailure(self, test, err):
        test_name = test._testMethodName
        msg = str(err[1])
        self.handleDeduction(test_name, msg)
        super(Results_600, self).addFailure(test, err)

    def addError(self, test, err):
        test_name = test._testMethodName
        self.handleDeduction(test_name, None)
        super(Results_600, self).addError(test, err)

    def handleDeduction(self, test_name, message):
        point_value = point_values[test_name]
        if message is None:
            message = 'Your code produced an error on test %s.' % test_name
        self.output.append('[-%s]: %s' % (point_value, message))
        self.points -= point_value

    def getOutput(self):
        if len(self.output) == 0:
            return "All correct!"
        return '\n'.join(self.output)

    def getPoints(self):
        return self.points

if __name__ == '__main__':

	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(TestPS4A))
	result = unittest.TextTestRunner(verbosity=2, resultclass=Results_600).run(suite)

	output = result.getOutput()
	points = result.getPoints()

	# weird bug with rounding
	if points < .1:
		points = 0

	print("\nProblem Set 4A Unit Test Results:")
	print(output)
	print("Points: %s/2\n" % points)
