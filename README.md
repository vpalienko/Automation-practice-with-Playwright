# Playwright and Python practice
**Software to be tested:** https://coffee-cart.app/

### Installation:
1. Install python 3.10 or higher
2. Activate virtual environment
3. Install all dependencies: `pip install -r requirements.txt`
4. Install Playwright browsers: `playwright install`

### Run tests:
run `pytest` to run all tests in the project

run `pytest -m smoke` to run smoke tests only

run `pytest -m feature` to run feature tests only

By default, tests are run in headed mode (to run tests in headless mode, remove `--headed` in `pytest.ini -> addopts`).

run with `--slowmo 500` to slow down tests by 500 milliseconds

run with `--numprocesses auto` to run tests in parallel

run with `--verbose` to get detailed output