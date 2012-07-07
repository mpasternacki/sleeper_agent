import sleeper_agent
import unittest

try:
    unittest.TestCase.assertIn
except AttributeError:
    import unittest2 as unittest

# WARNING: some assertions depend on specific line numbers in this
#          file. Please take care when updating the test cases.

class SleeperAgentSmokeTest(unittest.TestCase):
    "Basic tests that the functions can be called and don't return garbage."

    def test_python__get_state_info(self):
        "_get_state_info() should return something sane."
        state_info = sleeper_agent._get_state_info()
        self.assertIn("test_python__get_state_info", state_info)
        self.assertIn('test.py", line 17', state_info)
        self.assertNotIn("test_c_sleeper_agent_state", state_info)
        self.assertNotIn('test.py", line 25', state_info)

    def test_c_sleeper_agent_state(self):
        "C extension's sleeper_agent_state() should return something sane."
        state_info = sleeper_agent._sleeper_agent_activation.sleeper_agent_state()
        self.assertIn("test_c_sleeper_agent_state", state_info)
        self.assertIn('test.py", line 25', state_info)
        self.assertNotIn("test_python__get_state_info", state_info)
        self.assertNotIn('test.py", line 17', state_info)

    def test_python_and_c_functions_return_same_string(self):
        "_get_state_info() and sleeper_agent_state() should return the same value."
        # WARNING: the two function calls should be on the same line,
        #          otherwise they won't match.
        py_bt, c_bt = \
               sleeper_agent._get_state_info(), sleeper_agent._sleeper_agent_activation.sleeper_agent_state()
        self.assertEqual(py_bt, c_bt)
