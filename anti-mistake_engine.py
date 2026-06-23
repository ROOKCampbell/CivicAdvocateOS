import logging

# Configure basic logging to display errors clearly in the console
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class AntiMistakeEngine:
    """A conceptual engine to prevent, catch, and handle errors in your code."""

    def __init__(self):
        # Keep a list of errors for debugging later
        self.error_log = []

    def validate_input(self, user_input, expected_type):
        """
        Prevents mistakes by ensuring inputs match expected formats.
        """
        if not isinstance(user_input, expected_type):
            error_msg = f"Validation failed: Expected {expected_type.__name__}, got {type(user_input).__name__}."
            logging.warning(error_msg)
            return False
        return True

    def safe_execute(self, func, *args, **kwargs):
        """
        Catches runtime mistakes so the program doesn't crash.
        Wraps the execution in a try-except block.
        """
        try:
            # Attempt to run the target function with the provided arguments
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # If a mistake happens, catch it, log it, and return None
            error_msg = f"Caught a mistake in '{func.__name__}': {str(e)}"
            self.error_log.append(error_msg)
            logging.error(error_msg)
            return None

# ==========================================
# Implementation Instructions & Example Use
# ==========================================

# 1. Let's define a function that is prone to making a mistake (division by zero)
def divide_numbers(a, b):
    return a / b

# 2. Initialize our engine
engine = AntiMistakeEngine()

print("--- Testing Input Validation ---")
# Let's check if the user accidentally passed a string instead of a number
is_valid_1 = engine.validate_input(10, int)       # Will pass quietly
is_valid_2 = engine.validate_input("ten", int)    # Will trigger a warning

print("\n--- Testing Safe Execution ---")
# Normally, dividing by zero would crash your entire app. 
# With the engine, it catches the error and keeps the app alive.
print("Attempting to divide 10 by 2...")
success_result = engine.safe_execute(divide_numbers, 10, 2)
print(f"Result: {success_result}")

print("\nAttempting to divide 10 by 0...")
failed_result = engine.safe_execute(divide_numbers, 10, 0)
print(f"Result: {failed_result}")
