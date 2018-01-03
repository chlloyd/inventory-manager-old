from flask import g


def after_request(f):
    """Defer the calling of a function until where a response object is available

    Args:
        f (function): Function to defer. Function should take a Response object as an argument.

    Returns:
        function: Returns the function.

    See Also:
        http://flask.pocoo.org/docs/0.12/patterns/deferredcallbacks/#deferred-callbacks

    """
    if not hasattr(g, 'after_request_callbacks'):
        g.after_request_callbacks = []

    g.after_request_callbacks.append(f)
    return f
