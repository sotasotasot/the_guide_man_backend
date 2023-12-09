from flask import Flask, url_for, render_template, redirect
from flask import request, jsonify
from flask_cors import CORS
import requests
import json
import asyncio
import aiohttp

url = "https://deliverysupport.stg.pioneerapis.com/"
api_key = "PAK1 Credential=zPsJKOJCxNbkpddLbLoZ Signature=6a75i625tzfqok3mchxe79831o2t5u0gccl9np0eyf3mq61e29megt8ml3f2htky"

depo = {
      "lat": 35.007992,
      "lon": 135.775486,
    }

kiyomizu = {
        "lat": 34.9946662,
        "lon": 135.7820861
      }

yasaka = {
        "lat": 35.0036559,
        "lon": 135.760529
      }

ponto = {
        "lat": 35.0042777,
        "lon": 135.7685495
      }


def get_json_route(start, dest):
    return {
        "userID": "testUser",
        "pointinfo": {
            "start": start,
            "destination": dest,
        },
        "setTime": {
            "type": 0,
            "time": "2023-01-01T08:30+09:00"
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

json_data = {
  "userID": "testUser",
  "pointinfo": {
    "start": {
      "lat": 35.93241737968212,
      "lon": 139.47167252901303
    },
    "destination": {
      "lat": 35.7348,
      "lon": 139.7077,
      "alongside": False,
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
    "time": "2023-01-01T08:30+09:00"
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

json_routing = {
  "map_region": "jp",
  "user_id": "testUser",
  "delivery_start_time": "2020-01-01T14:30+09:00",
  "delivery_end_time": "2020-01-01T18:30+09:00",
  "depot": {
    "unique_id": "depot",
    "address": {
      "latitude": 35.007992,
      "longitude": 135.775486,
    }
  },
  "locations": [
    {
      "unique_id": "kiyomizu",
      "address": {
        "latitude": 34.9946662,
        "longitude": 135.7820861
      },
    },
    {
      "unique_id": "yasaka",
      "address": {
        "latitude": 35.0036559,
        "longitude": 135.760529
      },
    },
    {
      "unique_id": "pontocho",
      "address": {
        "latitude": 35.0042777,
        "longitude": 135.7685495
      },
    },
  ],
  "search_condition": {
    "use_care_traffic": False,
    "use_care_regulation": False,
    "use_care_time_regulation": True,
    "use_alongside": False,
    "use_toll": False,
    "use_hwy": False,
    "use_ferry": False,
    "use_smart_ic": False
  },
  "need_draw_data": True
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
        return redirect(url_for("test", args = keyword))
    return render_template("sample.html")

async def make_async_request(target, json):
    async with aiohttp.ClientSession() as session:
        headers = {
            'Authorization': api_key,
            'Content-Type': 'application/json',
            'PEC-Traffic-ProviderKey': 'none',
            'PEC-Traffic-ProviderUserID': "testUser",
        }
        async with session.post(url + target, headers=headers, json=json) as response:
            return await response.json()

@app.route('/api', methods=['GET'])
def api():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(make_async_request("/navicore/calcRoute", get_json_route(yasaka, kiyomizu)))
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/hidden', methods=['GET'])
def get_routing_all():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        order = {"depo_ponto.json":(depo, ponto), "ponto_yasaka.json":(ponto, yasaka), "yasaka_kiyomzu.json":(yasaka, kiyomizu)}
        for i, (key, (start, dest)) in enumerate(order.items()):
            if i!=2:
                continue
            print(key)
            response = loop.run_until_complete(make_async_request("/navicore/calcRoute", get_json_route(depo, ponto)))
            with open("data/"+key, 'w') as f:
                json.dump(response, f)
        return "success"
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/vehicle', methods=['GET'])
def api_vehicle():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(make_async_request("/caerus/vehiclerouting/v1/order", json_routing))
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
  app.run(debug=True, host='localhost')
