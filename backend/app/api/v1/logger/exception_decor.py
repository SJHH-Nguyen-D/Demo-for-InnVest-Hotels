def exception(logger):
    """
    A decorator that wraps the passed in function and logs exceptions should one occur.
    This exception is for the main table builder functions.

    :param logger: The logging object
    :return: Decorator object
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                # log the exception
                err = f"There was an error when running {func.__name__}. Inspect /var/log/apogee.log for more details."
                logger.exception(err)
                # Raise the exception in the terminal traceback
                raise Exception

        return wrapper

    return decorator
