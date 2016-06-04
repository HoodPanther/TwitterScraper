# import markdown
from flaskext.markdown import Markdown
from flask import Flask
from flask import render_template
# from flask import Markup

app = Flask(__name__)
Markdown(app)

@app.route('/')
def index():
    content = """
Twitter Scraper
===============

* [Last 24 hours](#Last24HOurs)
* [Full](#Full)

<a name="Last24Hours">Last 24 hours</a>
-------------

![alt text](\static\plot_24_hours.png "Last 24 hours")

<a name="Full">Full</a>
----

![alt text](\static\plot_full.png "Full")


<!---


<img src="\static\plot_24_hours.png" alt="Last 24 hours" style="width: 50%;"/>
<img src="\static\plot_full.png" alt="Full" style="width: 50%;"/>
--->


"""
    # content = Markup(markdown.markdown(content))
    return render_template('index.html', **locals())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
