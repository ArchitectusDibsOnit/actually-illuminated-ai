# async_utils.py

import gradio as gr
import traceback

def async_wrapper(fn):
    """
    Wraps a function for Gradio to handle loading and errors.
    Use as:
        wrapped_fn = async_wrapper(original_fn)
    """
    def wrapped(*args, status=gr.Status(), **kwargs):
        try:
            status.loading()
            result = fn(*args, **kwargs)
            status.success("✅ Done.")
            return result
        except Exception as e:
            tb = traceback.format_exc()
            status.error(f"⚠️ Error: {e}")
            print(tb)
            return None
        finally:
            status.clear()
    return wrapped
