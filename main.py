import os

from bottle import (
    get,
    post,
    redirect,
    request,
    route,
    run,
    static_file,
    template,
    error,
    response,
    abort
)
import utils
import json


# Static Routes


@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")


# Dynamic routes


@route("/")
def index():
    this_section_template = "./templates/home.tpl"
    return template(
        "./pages/index.html",
        version=utils.get_version(),
        sectionTemplate=this_section_template,
        sectionData={},
    )


@route("/browse")
def browse():
    this_section_template = "./templates/browse.tpl"
    results=utils.get_shows(utils.AVAILABE_SHOWS)
    try:
        order = request.query['order']
        if order.lower() == 'name':
            results.sort(key=lambda s : s['name'])
        elif order.lower() == 'ratings':
            results.sort(key=lambda s : s['rating']['average'])
    except KeyError:
        print('error getting order query parameter')
    return template(
        "./pages/index.html",
        version=utils.get_version(),
        sectionTemplate=this_section_template,
        sectionData=results,
    )


@route("/search")
def get_search():
    this_section_template = "./templates/search.tpl"
    return template(
        "./pages/index.html",
        version=utils.get_version(),
        sectionTemplate=this_section_template,
        sectionData=utils.get_shows(utils.AVAILABE_SHOWS),
    )


@post("/search")
def post_search():
    search_value = request.forms.get("q")
    results = utils.search_episodes(search_value)
    this_section_template = "./templates/search_result.tpl"
    return template(
        "./pages/index.html",
        version=utils.get_version(),
        sectionTemplate=this_section_template,
        sectionData=search_value,
        query=search_value,
        results=results
    )


@route("/show/<showID>")
def show(showID):
    this_section_template = "./templates/show.tpl"
    result = []
    try:
        result = json.loads(utils.get_json_from_file(showID))
    except TypeError as e:
        print('no search results - ' + str(e.args))
        abort(404, 'Show Not Found')
        return
    return template(
        "./pages/index.html",
        version=utils.get_version(),
        sectionTemplate=this_section_template,
        sectionData=result,
    )


@route("/ajax/show/<showID>")
def ajax_route(showID):
    this_section_template = "./templates/show.tpl"
    result = json.loads(utils.get_json_from_file(showID))
    return template(this_section_template, result=result)


@route("/show/<showID>/episode/<episodeID>")
def episode(showID, episodeID):
    this_section_template = "./templates/episode.tpl"
    result = []
    try:
        result = utils.get_episode(showID, episodeID)
    except TypeError as e:
        print('no search results - ' + str(e.args))
        abort(404, 'Show / episode Not Found')
        return
    if 'episode not found' == str(result):
        abort(404, 'episode Not Found')

    return template(
        "./pages/index.html",
        version=utils.get_version(),
        sectionTemplate=this_section_template,
        sectionData=result,
    )


@route("/ajax/show/<showID>/episode/<episodeID>")
def episode(showID, episodeID):
    this_section_template = "./templates/episode.tpl"
    result = utils.get_episode(showID, episodeID)
    return template(this_section_template, result=result)


@error(404)
@error(500)
def return_error(error):
    this_section_template = "./templates/404.tpl"
    return template(
        "./pages/index.html",
        version=utils.get_version(),
        sectionTemplate=this_section_template,
        sectionData={},
    )


run(host="127.0.0.1", port=os.environ.get("PORT", 5000), reloader=True)
