from flask import Flask, request, flash, url_for, redirect, \
    render_template, abort, send_from_directory
from content_management import content
import bs4
import requests
from jinja2 import Environment

seasons = content()

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.route('/')
def index():
    root_url = 'http://www.randomsimpsonsquote.com'
    response = requests.get(root_url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    ##character = soup.select('#main > img')[0]['src']
    quote = soup.select('#main > blockquote')[0]
    return render_template('index.html', quote=quote)


@app.route("/episodes/season/<episode>")
def episodes(episode):
    return render_template('episodes.html', seasons=seasons['Season {0}'.format(episode)])

@app.route("/player/playback")
def playback():
    episode_title = request.args['episode_title']
    uri = request.args['url']
    thumb = request.args['thumb']
    return render_template('player.html', episode_title=episode_title, url=uri, thumb=thumb )



@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.template_filter()
def nodescript(e):
    try:
        if e.encode('utf-8').strip() == "":
            return 'Something should probably go here soon.'
    except:
        return 'Something should probably go here soon.'
    else:
        return e

app.jinja_env.filters['nodescript'] = nodescript


@app.template_filter()
def nothumb(b):
    if "wtso" not in b:
        return b
    else:
        return '/imgs/frontend/placeholder.png'

app.jinja_env.filters['nothumb'] = nothumb






if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=80)
