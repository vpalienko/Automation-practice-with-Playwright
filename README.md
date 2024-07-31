# Playwright and Python practice
**Software to be tested:** https://coffee-cart.app/

### Installation:
1. install python 3.10 or higher
2. activate virtual environment
3. install all dependencies: `pip install -r requirements.txt`
4. install Playwright browsers: `playwright install`

### Run tests
run `pytest` to run all tests in the project

run `pytest -m smoke` to run smoke tests only

run `pytest -m feature` to run feature tests only

run with `--headed` to run tests in headed mode (headless mode is set by default)

run with `--numprocesses auto` to run tests in parallel