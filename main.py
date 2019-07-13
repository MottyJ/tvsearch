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
    print("in index")
    thisSectionTemplate = "./templates/home.tpl"
    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData={},
    )


@route("/browse")
def browse():
    print("in browse")
    thisSectionTemplate = "./templates/browse.tpl"
    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData=utils.getShows(utils.AVAILABE_SHOWS),
    )


@route("/search")
def get_search():
    print("in get_search")
    thisSectionTemplate = "./templates/search.tpl"
    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData=utils.getShows(utils.AVAILABE_SHOWS),
    )


@post("/search")
def post_search():
    print("in post_search")
    search_value = request.forms.get("q")
    print("in post_search, " + search_value)
    results = utils.search_episodes(search_value)
    thisSectionTemplate = "./templates/search_result.tpl"
    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData=search_value,
        query=search_value,
        results=results
    )


@route("/show/<showID>")
@route("/ajax/show/<showID>")
def show(showID):
    print("in post_search")
    print("showID: " + showID)
    thisSectionTemplate = "./templates/show.tpl"
    result = []
    try:
        result = json.loads(utils.getJsonFromFile(showID))
    except TypeError as e:
        print('no search results - ' + str(e.args))
        abort(404,'Show Not Found')
        return

    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData=result,
    )


# @route("/ajax/show/<showID>")
# def ajax_route(showID):
#     print("in ajax_route")
#     print("showID: " + showID)
#     thisSectionTemplate = "./templates/show.tpl"
#     result = json.loads(utils.getJsonFromFile(showID))
#     print(result)
#     return template(
#         "./pages/index.html",
#         version=utils.getVersion(),
#         sectionTemplate=thisSectionTemplate,
#         sectionData=result,
#     )

@route("/ajax/show/<showID>/episode/<episodeID>")
@route("/show/<showID>/episode/<episodeID>")
def episode(showID, episodeID):
    print("in episode, showID {} episodeID {}".format(showID,episodeID))
    thisSectionTemplate = "./templates/episode.tpl"
    result = []
    try:
        result = utils.get_episode(showID, episodeID)
    except TypeError as e:
        print('no search results - ' + str(e.args))
        abort(404,'Show / episode Not Found')
        return
    if 'episode not found' == str(result):
        abort(404, 'episode Not Found')

    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData=result,
    )

# @route("/ajax/show/<showID>/episode/<episodeID>")
# def episode(showID, episodeID):
#     print("in episode")
#     thisSectionTemplate = "./templates/episode.tpl"
#     result = utils.get_episode(showID, episodeID)
#     return template(
#         "./pages/index.html",
#         version=utils.getVersion(),
#         sectionTemplate=thisSectionTemplate,
#         sectionData=result,
#     )


@error(404)
def return_error(error):
    print("in return_error")
    thisSectionTemplate = "./templates/404.tpl"
    # result = json.loads(utils.getJsonFromFile(showID))
    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData={},
    )


run(host="127.0.0.1", port=os.environ.get("PORT", 5000), reloader=True)

