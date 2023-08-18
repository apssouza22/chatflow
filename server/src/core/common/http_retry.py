import logging
import time
from random import random

logger = logging.getLogger(__name__)


def retry_with_exponential_backoff(
        backoff_in_seconds: float = 1,
        max_retries: int = 10,
        errors: tuple = (Exception,),
):
    """
    Decorator to retry a function with exponential backoff.
    :param backoff_in_seconds: The initial backoff in seconds.
    :param max_retries: The maximum number of retries.
    :param errors: The errors to catch retry on.
    """

    def decorator(function):
        def wrapper(*args, **kwargs):
            # Initialize variables
            num_retries = 0

            # Loop until a successful response or max_retries is hit or an
            # exception is raised
            while True:
                try:
                    return function(*args, **kwargs)

                # Retry on specified errors
                except errors as e:
                    # Check if max retries has been reached
                    if num_retries > max_retries:
                        raise Exception(f"Maximum number of retries ({max_retries}) exceeded.")

                    # Increment the delay
                    sleep_time = backoff_in_seconds * 2 ** num_retries + random()

                    # Sleep for the delay
                    logger.warning(
                        "%s - %s, retry %s in %s seconds...",
                        e.__class__.__name__,
                        e.message,
                        function.__name__,
                        "{0:.2f}".format(sleep_time),
                    )
                    time.sleep(sleep_time)

                    # Increment retries
                    num_retries += 1

        return wrapper

    return decorator
