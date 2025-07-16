This creates a .venv folder in your project directory.
python -m venv .venv

Activate it
.venv\Scripts\activate

VS Code will usually detect .venv automatically. If not:
Ctrl+Shift+P → Python: Select Interpreter → .venv

Install dependencies:
pip install -r requirements.txt

Then check that flask is installed there:
pip list

Run:
python -m src.app
