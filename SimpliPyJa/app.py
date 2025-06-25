
from flask import Flask, request, render_template_string
import io
import sys

# Import the parser (this also imports the lexer)
import simplipyja_parser

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SimpliPy-Ja Web Interpreter</title>
    <style>
        body { font-family: sans-serif; padding: 2rem; background: #f4f4f4; }
        textarea { width: 100%; height: 200px; }
        pre { background: #eee; padding: 1rem; white-space: pre-wrap; }
        button { padding: 0.5rem 1rem; }
    </style>
</head>
<body>
    <h1>SimpliPy-Ja Web Interpreter</h1>
    <form method="post">
        <textarea name="code" placeholder="Type SimpliPy-Ja code here...">{{ code }}</textarea><br><br>
        <button type="submit">Run</button>
    </form>
    {% if output %}
        <h3>Output:</h3>
        <pre>{{ output }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    code = ""
    if request.method == "POST":
        code = request.form.get("code", "")
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        try:
            simplipyja_parser.variables.clear()  # Reset state
            simplipyja_parser.parser.parse(code)
        except Exception as e:
            print(f"Error: {e}")
        sys.stdout = old_stdout
        output = redirected_output.getvalue()
    return render_template_string(HTML_TEMPLATE, code=code, output=output)

if __name__ == "__main__":
    app.run(debug=True)
