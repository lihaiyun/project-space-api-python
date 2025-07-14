This creates a .venv folder in your project directory.
python -m venv .venv

Activate it
.venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

VS Code will usually detect .venv automatically. If not:
Ctrl+Shift+P → Python: Select Interpreter → .venv

Then check that flask is installed there:
pip list
