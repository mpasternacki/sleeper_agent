Sleeper Agent
=============

The Sleeper Agent is a Python library that, when loaded, allows
inspecting live state with gdb.

It supports CPython version 2.6 and 2.7.

The library is developed at https://github.com/mpasternacki/sleeper_agent

Its unit tests run automatically at http://travis-ci.org/mpasternacki/sleeper_agent

Usage
-----

When initializing your Python code, just import the module:

    import sleeper_agent
   
There is nothing more to do. The sleeper agent is loaded, and it does
nothing.

When you want to peek into what your code is doing, just attach _gdb_
to it and activate the agent. Below is the example of activating the
agent on an _ipython_ session. Note that one of the threads has the
function `sleeper_agent._get_state_info` in its stack trace - this is
just appended to this thread's stack, and the information is harmless.

    $ gdb -p PID
    (gdb) printf "%s", sleeper_agent_state()
    ### Thread 4326428672:
      File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 525, in __bootstrap
        self.__bootstrap_inner()
      File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 552, in __bootstrap_inner
        self.run()
      File "<string>", line 2, in run
      File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/IPython/core/history.py", line 61, in needs_sqlite
        return f(*a,**kw)
      File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/IPython/core/history.py", line 647, in run
        self.history_manager.save_flag.wait()
      File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 404, in wait
        self.__cond.wait(timeout)
      File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 244, in wait
        waiter.acquire()
    
    
    ### Thread 140735285004640:
      File "/Library/Frameworks/Python.framework/Versions/2.7/bin/ipython", line 8, in <module>
        load_entry_point('ipython==0.12', 'console_scripts', 'ipython')()
      File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/IPython/frontend/terminal/ipapp.py", line 403, in launch_new_instance
        app.start()
      File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/IPython/frontend/terminal/ipapp.py", line 377, in start
        self.shell.mainloop()
      File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/IPython/frontend/terminal/interactiveshell.py", line 290, in mainloop
        self.interact(display_banner=display_banner)
      File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/IPython/frontend/terminal/interactiveshell.py", line 368, in interact
        line = self.raw_input(prompt)
      File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/IPython/frontend/terminal/interactiveshell.py", line 436, in raw_input
        line = py3compat.str_to_unicode(self.raw_input_original(prompt))
      File "sleeper_agent.py", line 7, in _get_state_info
        for thread_id, frame in sys._current_frames().items() )

Internals
---------

The library is composed of two pieces: a Python introspection module,
and some C glue.

Python module, `sleeper_agent.py`, defines one function named
`_get_state_info`. This function takes no arguments, and returns
program state as string. Currently, the state is list of threads and
their respective backtraces.

Python module also imports the C module `_sleeper_agent_activation` to
load the glue.

The core of the C module is the `char * sleeper_agent_state(void)`
function. It acquires the GIL, calls out to
`sleeper_agent._get_state_info` Python function, and returns its
result as a C string, which can be then printed from _gdb_.

The C module also exports the `sleeper_agent_state_pyobject` function
to Python as `sleeper_agent_state`. This function calls the C
`sleeper_agent_state` function, and returns its result as a Python
string, thus completing the cycle.

So, a smoke check for particular pieces without actually resorting to
use _gdb_ would look like this:

    >>> import sleeper_agent
    >>> sleeper_agent._get_state_info()
    '### Thread 140735285004640:\n  File "<stdin>", line 1, in <module>\n  File "sleeper_agent.py", line 15, in _get_state_info\n    for thread_id, frame in sys._current_frames().items() )\n'
    >>> sleeper_agent._sleeper_agent_activation.sleeper_agent_state()
    '### Thread 140735285004640:\n  File "<stdin>", line 1, in <module>\n  File "sleeper_agent.py", line 15, in _get_state_info\n    for thread_id, frame in sys._current_frames().items() )\n'
    >>> sleeper_agent._sleeper_agent_activation.sleeper_agent_state() == sleeper_agent._get_state_info()
    True
    >>> 

Acknowledgements
----------------

Some of the code and ideas have been inspired by Leonardo Rochael
Almeida's talk at Europython 2012,
[https://ep2012.europython.eu/conference/talks/sys_current_frames-take-real-time-x-rays-of-your-software-for-fun-and-performance](`sys._current_frames()`:
Take real-time X-rays of your software for fun and performance.)

Other ideas
-----------

The returned info can be extended to include locals and globals on
each call stack level.

The call info can also be used to perform statistical profiling, by
semi-regularly dumping the stack somewhere to be analyzed later on.

Code can be expanded to interactively talk with Python and explore the
stack levels. This would need storing the stack trace objects, and
probably also some scripting on the gdb side to have a usable
interface. Maybe some pieces of pdb code could be reused for that.
