import os
import unittest

# Configure app to use the testing configuration
if not "CONFIG_PATH" in os.environ:
    os.environ["CONFIG_PATH"] = "fight_simulator.config.TestingConfig"

class fight_simulation_test(unittest.TestCase):
    def test_calc_win_perc(self):
        pass

    def test_calc_new_win_perc(self):
        pass

if __name__ == "__main__":
    unittest.main()
