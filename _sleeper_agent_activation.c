#include <Python.h>

/* Return result of sleeper_agent._get_state_info() as a C string */
char * sleeper_agent_state(void)
{
     char *rv = NULL;
     PyGILState_STATE gstate;

     gstate = PyGILState_Ensure();
     rv = PyString_AsString(
          PyObject_Call(
               PyObject_GetAttrString(
                    PyImport_ImportModule("sleeper_agent"),
                    "_get_state_info"),
               Py_BuildValue("()"), NULL));
     PyGILState_Release(gstate);

     return rv;
}

/* Return sleeper_agent_state() as Python string, for testing and fun */
static PyObject *
sleeper_agent_state_pyobject(PyObject *self, PyObject *args)
{
     return Py_BuildValue("s", sleeper_agent_state());
}

static PyMethodDef SleeperAgentMethods[] = {
     {"sleeper_agent_state",  sleeper_agent_state_pyobject, METH_VARARGS,
      "Return the sleeper agent state as a Python string."},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
init_sleeper_agent_activation(void)
{
     (void) Py_InitModule("_sleeper_agent_activation", SleeperAgentMethods);
}
