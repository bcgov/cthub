import ctypes
import threading


class TaskTimeoutException(Exception):
    pass


def timeout(time):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            current_thread_id = threading.current_thread().ident

            def throw_timeout():
                ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_ulong(current_thread_id),
                    ctypes.py_object(TaskTimeoutException),
                )

            t = threading.Timer(time, throw_timeout)
            t.start()
            try:
                func(*args, **kwargs)
                t.cancel()
            except Exception as ex:
                t.cancel()
                raise ex

        return wrapped

    return wrapper
