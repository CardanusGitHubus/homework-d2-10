import os
import sentry_sdk
import auth_params

from logger import logger  # импортируем объект логгера из файла
from bottle import Bottle, route, run, request
from sentry_sdk.integrations.bottle import BottleIntegration

sentry_sdk.init(
    dsn=auth_params.SENTRY_DSN,
    integrations=[BottleIntegration()]
)

app = Bottle()  # создаем объект приложения bottle


@app.route("/")
def main_page():
    return '''
        <div style="margin: 20px auto; width: 300px; border: 1px solid black; display: flex; flex-wrap: wrap">
            <form style="margin: 10px auto; width: 45%" action="/success" method="GET">
                <input style="width: 100%" value="success" type="submit" />
            </form>
            <form style="margin: 10px auto; width: 45%" action="/fail" method="get">
                <input style="width: 100%" value="fail" type="submit" />
            </form>
        </div>
    '''


@app.route("/success")
def success_response():
    logger.info(request.headers.get("User-Agent"))
    return "test that automatic deploy from github to heroku works"


@app.route("/fail")
def fail_response():
    logger.error("Everything is in fire!")
    raise RuntimeError("fail response")


if os.environ.get("APP_LOCATION") == "heroku":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3,
    )
else:
    app.run(host="localhost", port=8080, debug=True)
