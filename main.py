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
)
import utils

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


@route("/")
def index():
    thisSectionTemplate = "./templates/home.tpl"
    return template(
        "./pages/index.html",
        version=utils.getVersion(),
        sectionTemplate=thisSectionTemplate,
        sectionData={},
    )

@error(404)
def return_error(error):
    return template("./templates/404")

run(host="127.0.0.1", port=os.environ.get("PORT", 5000), reloader=True)

