import time
import random
import functools

class MaxRetriesExceededError(Exception):
    """
    Raised when the maximum number of retry attempts is exceeded.
    """
    def __init__(self, attempts, last_exception):
        self.attempts = attempts
        self.last_exception = last_exception
        message = (
            f"Operation failed after {attempts} attempts. "
            f"Last error: {last_exception}"
        )
        super().__init__(message)


def retry_with_backoff(max_attempts, base_delay=1.0, jitter=0.1):
    """
    A decorator factory for retrying a function with validation, exponential
    backoff, jitter, and custom exceptions.
    """

    # ---- Factory Input Validation ----
    if not isinstance(max_attempts, int) or max_attempts <= 0:
        raise ValueError("max_attempts must be an integer greater than 0")

    if not isinstance(base_delay, (int, float)) or base_delay < 0:
        raise ValueError("base_delay must be a non-negative number")

    if not isinstance(jitter, (int, float)) or jitter < 0:
        raise ValueError("jitter must be a non-negative number")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    # ---- Attempt function execution ----
                    return func(*args, **kwargs)

                except Exception as e:
                    last_exception = e

                    # ---- If final attempt, raise custom exception ----
                    if attempt == max_attempts:
                        raise MaxRetriesExceededError(
                            attempts=attempt,
                            last_exception=e
                        ) from e

                    # ---- Exponential Backoff + Jitter ----
                    delay = base_delay * (2 ** (attempt - 1))
                    delay += random.uniform(0, jitter)

                    time.sleep(delay)

        return wrapper
    return decorator

@retry_with_backoff(max_attempts=3, base_delay=1, jitter=0.5)
def flaky_api():
    print("Calling API...")
    raise ConnectionError("API temporarily unavailable")

try:
    flaky_api()
except MaxRetriesExceededError as e:
    print("FINAL ERROR:", e)
    print("Attempts:", e.attempts)
    print("Root cause:", e.last_exception)