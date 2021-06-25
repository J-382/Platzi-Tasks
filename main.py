#Flask imports
from flask import render_template
from flask_login.utils import login_required
from config import create_app, ip

#OS imports
import unittest

app = create_app()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.route('/app')
@login_required
def main_app():
    return render_template("mail.html")

@app.errorhandler(404)
def not_foud(error):
    return render_template("404.html")

if __name__ == '__main__':
    run_kwargs = {
    'host': ip, 
    'debug': True
    }
    app.run(**run_kwargs)