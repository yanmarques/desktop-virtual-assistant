def decorate_with_callback(fn, callback):
    def callback_wrapper(*args):
        return fn(*(*args, callback()))
    return callback_wrapper
