import sys, traceback
import _sleeper_agent_activation

def _get_state_info():
    """Return state of current process, as a string.

    Returns a formatted list of threads known to the Python
    interpreter, together with their stack traces.

    One of the threads will have this function call *appended* to its
    original stack trace. I still don't know how to get rid of that."""
    return "\n\n".join(
        "### Thread {0}:\n{1}".format(
            thread_id, ''.join(traceback.format_stack(frame)))
        for thread_id, frame in sys._current_frames().items() )
