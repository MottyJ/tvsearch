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
    response
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
    thisSectionTemplate = "./templates/home.tpl"
    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData={},
    )


@route("/browse")
def browse():
    thisSectionTemplate = "./templates/browse.tpl"
    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData=utils.getShows(utils.AVAILABE_SHOWS),
    )

@route("/search")
def browse():
    thisSectionTemplate = "./templates/search.tpl"
    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData=utils.getShows(utils.AVAILABE_SHOWS),
    )

@post("/search")
def post_search():
    search_value = request.forms.get("q")
    print("in post_search, " + search_value)

# @route("/show/<showID>")
# def show(showID):
#     thisSectionTemplate = "./templates/show.tpl"
#     result = json.loads(utils.getJsonFromFile(showID))
#     return template(
#         "./pages/index.html",
#         version=utils.getVersion(),
#         sectionTemplate=thisSectionTemplate,
#         sectionData=result,
#     )

@route("/ajax/show/<showID>")
def ajax_route(showID):
    thisSectionTemplate = "./templates/show.tpl"
    result = json.loads(utils.getJsonFromFile(showID))
    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData=result,
    )


@error(404)
def return_error(error):
    thisSectionTemplate = "./templates/404.tpl"
    # result = json.loads(utils.getJsonFromFile(showID))
    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData={},
    )


run(host="127.0.0.1", port=os.environ.get("PORT", 5000), reloader=True)

