# import markdown
from flaskext.markdown import Markdown
from flask import Flask
from flask import render_template
# from flask import Markup
import utils

app = Flask(__name__)
Markdown(app)


@app.route('/')
def index():
    content = utils.build_page()
    return render_template('index.html', **locals())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
