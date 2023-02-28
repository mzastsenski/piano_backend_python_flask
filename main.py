from flask import Flask, redirect, render_template

app = Flask(__name__, static_url_path="/", static_folder="templates")
import crud
import authentication


@app.route("/")
def main():
      return render_template('index.html')


@app.errorhandler(404)
def http_error_handler404(err):
    return redirect("/")


@app.errorhandler(500)
def http_error_handler500(err):
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5002)