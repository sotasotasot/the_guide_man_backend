from flask import Flask, url_for, render_template, redirect
from flask import request, jsonify
from flask_cors import CORS
import aiohttp
import asyncio

url = "https://deliverysupport.stg.pioneerapis.com/"
api_key = "PAK1 Credential=zPsJKOJCxNbkpddLbLoZ Signature=6a75i625tzfqok3mchxe79831o2t5u0gccl9np0eyf3mq61e29megt8ml3f2htky"

json_data = {
    "userID": "testUser",
    "pointinfo": {
        "start": {
            "lat": 35.93241737968212,
            "lon": 139.47167252901303
        },
        "destination": {
            "lat": 35.93241737968212,
            "lon": 139.47167252901303,
            "alongside": False,
            "info": [
                {
                    "key": "address",
                    "value": "川越市"
                }
            ]
        },
        "wayPoints": [
            {
                "kind": "stopover",
                "lat": 35.93241737968212,
                "lon": 139.47167252901303,
                "alongside": False,
                "stayTime": 30
            }
        ]
    },
    "setTime": {
        "type": 0,
        "time": "2020-01-01T08:30+09:00"
    },
    "options": {
        "priority": "recommended",
        "useToll": True,
        "useHighway": True,
        "useFerry": True,
        "useSmartIC": True,
        "careJam": True,
        "careRegulation": True,
        "careTimeRegulation": True
    },
    "vehicleInfo": {
        "type": 0,
        "ratesClass": 0,
        "etc": 0,
        "width": 178,
        "height": 153,
        "weight": 1480,
        "dangerousLoaded": False
    },
    "needDrawData": True
}

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"\
    + "<a href=" + url_for("test", args="test") +"> test page </a>" 

@app.route("/test/<args>", methods=["GET"])
def test(args):
    return  "<p>" + str(args) + "<p>"\
        + "<a href=" + url_for("hello_world") + "> top page </a>"

@app.route("/sample", methods=["GET", "POST"])
def sample():
    # post request時
    if request.method == 'POST':
        keyword = request.form["keyword"]
        return redirect(url_for("test", args=keyword))
    return render_template("sample.html")

async def make_async_request():
    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization': api_key,
            'Content-Type': 'application/json',
            'PEC-Traffic-ProviderKey': 'none',
            'PEC-Traffic-ProviderUserID': "testUser",
        }
        async with session.post(url + "/navicore/calcRoute", headers=headers, json=json_data) as response:
            return await response.json()

@app.route('/api', methods=['GET'])
def api():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(make_async_request())
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True, host='localhost')

# from flask import Flask, url_for, render_template, redirect
# from flask import request, jsonify
# from flask_cors import CORS
# import requests
# import json
# import asyncio

# url = "https://deliverysupport.stg.pioneerapis.com/"
# api_key = "PAK1 Credential=zPsJKOJCxNbkpddLbLoZ Signature=6a75i625tzfqok3mchxe79831o2t5u0gccl9np0eyf3mq61e29megt8ml3f2htky"

# json_data = {
#   "userID": "testUser",
#   "pointinfo": {
#     "start": {
#       "lat": 35.93241737968212,
#       "lon": 139.47167252901303
#     },
#     "destination": {
#       "lat": 35.93241737968212,
#       "lon": 139.47167252901303,
#       "alongside": False,
#       "info": [
#         {
#           "key": "address",
#           "value": "川越市"
#         }
#       ]
#     },
#     "wayPoints": [
#       {
#         "kind": "stopover",
#         "lat": 35.93241737968212,
#         "lon": 139.47167252901303,
#         "alongside": False,
#         "stayTime": 30
#       }
#     ]
#   },
#   "setTime": {
#     "type": 0,
#     "time": "2020-01-01T08:30+09:00"
#   },
#   "options": {
#     "priority": "recommended",
#     "useToll": True,
#     "useHighway": True,
#     "useFerry": True,
#     "useSmartIC": True,
#     "careJam": True,
#     "careRegulation": True,
#     "careTimeRegulation": True
#   },
#   "vehicleInfo": {
#     "type": 0,
#     "ratesClass": 0,
#     "etc": 0,
#     "width": 178,
#     "height": 153,
#     "weight": 1480,
#     "dangerousLoaded": False
#   },
#   "needDrawData": True
# }

# app = Flask(__name__)
# CORS(app)

# @app.route("/", methods=["GET"])
# def hello_world():
#     return "<p>Hello, World!</p>"\
#     + "<a href=" + url_for("test", args="test") +"> test page </a>" 

# @app.route("/test/<args>", methods=["GET"])
# def test(args):
#     return  "<p>" + str(args) + "<p>"\
#         + "<a href=" + url_for("hello_world") + "> top page </a>"

# @app.route("/sample", methods=["GET", "POST"])
# def sample():
#    # post request時
#     if request.method == 'POST':
#         keyword = request.form["keyword"]
#         return redirect(url_for("test", args = keyword))
#     return render_template("sample.html")

# @app.route('/api', methods=['GET'])
# async def api():
#     try:
#         async with app.app_context():
#             headers = {
#                 'Authorization': "pio_hack_20231208",
#                 'Content-Type': 'application/json',
#                 'PEC-Traffic-ProviderKey': 'none',
#                 'PEC-Traffic-ProviderUserID': "testUser",
#             }
#             json_data = jsonify(json_data)
#             response = await requests.post(url + "/navicore/calcRoute", headers=headers, data=json.dumps(json_data))
#             print(response)

#         return jsonify(response.json())
#     except Exception as e:
#         return jsonify({'error': str(e)})
   


# if __name__ == "__main__":
#   app.run(debug=True, host='localhost')