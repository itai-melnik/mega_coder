
import sys
from io import StringIO

# Redirect stdout to capture print output for the first print statement.
old_stdout = sys.stdout
mystdout = StringIO()
sys.stdout = mystdout

# Prints "Hello, World!" to the captured stdout.
print("Hello, World!")

# Restore stdout to its original state.
sys.stdout = old_stdout

# Assert that the captured output is indeed "Hello, World!".
assert mystdout.getvalue().strip() == "Hello, World!", "The first print output is incorrect"

# The print function returns None. This line will print to the actual console.
print_return_value = print("This print also returns None")
# Assert that the return value of print() is None.
assert print_return_value is None, "The print function should return None"

# Test ZeroDivisionError handling.
try:
    x = 1 / 0  # This will raise a ZeroDivisionError
    # If the exception is not raised, this assertion will fail.
    assert False, "ZeroDivisionError was expected but not raised"
except ZeroDivisionError:
    # This block executes if ZeroDivisionError is caught.
    print("Caught expected ZeroDivisionError.")
    # Assert that the error was indeed caught.
    assert True, "ZeroDivisionError was not caught as expected"

# Example of a correct assertion.
assert 1 + 1 == 2, "1 + 1 should equal 2"

# Another test for ZeroDivisionError handling, demonstrating successful capture.
try:
    result = 1 / 0  # This will raise a ZeroDivisionError
    # If the exception is not raised, this assertion will fail.
    assert False, "ZeroDivisionError was expected but not raised in the second instance"
except ZeroDivisionError:
    # This block executes if ZeroDivisionError is caught.
    print("Successfully handled ZeroDivisionError from the last statement.")
    # Assert that the error was handled.
    assert True, "The final ZeroDivisionError was not handled"
