import os

from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

def build_query(fd, query):
    query_items = query.split("|")
    res = map(lambda v: v.strip(), fd)
    print(res)
    print(query_items)
    for item in query_items:
        split_item = item.split(":")
        cmd = split_item[0]

        if cmd == "filter":
            arg = split_item[1]
            res = filter(lambda  v, txt=arg: txt in v, res)

        if cmd == "map":
            arg = split_item[1]
            res = map(lambda v, idx=arg: v.split(" ")[idx], res)

        if cmd == "unique":
            res = set(res)


        print(list(res))


@app.route("/perform_query")
def perform_query():
    try:
        query = request.args["query"]
        file_name = request.args["file_name"]
    except KeyError:
        raise BadRequest

    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return BadRequest(description=f"{file_name} was not found")

    with open(file_path) as fd:
        res = build_query(fd, query)
        content = ''
    return app.response_class(content, content_type="text/plain")

    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат


"""from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
"""