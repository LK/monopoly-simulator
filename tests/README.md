# Testing framework
unittest:
  - Write tests in classes that inherit from unittest.TestCase
  - Write each test in a method prefixed with 'test_'
  - Run tests in a module with one of the following:
      `python -m unittest module`
      `pythom -m unittest module.Classname`
      `python -m unittest module.Classname.test_method`


# Automated Testing
Nose/Sniffer:
  - Nose is a test runner, which searches for tests using either the nose or unittest framework, and runs them.
  - Sniffer is an auto-runner for nose, which runs nose upon detecting modified files.

How to install nose/sniffer:
  - pip install nose
  - pip install sniffer
  - Add executables 'nosetests' and 'sniffer' to your $PATH

How to run nose/sniffer:
  - Execute the nose test runner with 'nosetests'
  - Start sniffer with 'sniffer', which will run the nose automatically when files have been modified
  - *Note*: For tests to run properly, you need to have $PYTHONPATH set to the root of the project. This way it can find the dependencies it imports
