import json, requests
import flask
import os
# from flask import Flask, request

app = flask.Flask(__name__)
headers = {
    "Authorization": f"Bearer '{os.environ['AUTH_TOKEN']}'",
    "content-type": "application/json"}

@app.route("/", methods=["POST"])
def main():
    url_toggle = f"{os.environ['SYSTEM_IP']}/api/services/"
    url_states = f"{os.environ['SYSTEM_IP']}/api/states"
    header = flask.request.headers
    if header['Authorization'] == "some-key-here" and header["Content-Type"] == "application/json":
        switches, sensors, lights, media = ([] for i in range(4))
        data = json.loads(flask.request.data)
        state = data['state'].lower()
        entity = data['entity_id']
        _return = data['return']
        if _return != "":
            _return = int(_return) - 1
        get_enities_domains = requests.get(url_states, headers=headers)
        get_enities = json.loads(get_enities_domains.text)
        for val in get_enities:
            for key, val in val.items():
                if type(val) == str:
                    if val.startswith('sensor.'):
                        sensors.append(val)
                    if val.startswith('switch.'):
                        switches.append(val)
                    if val.startswith('light.'):
                        lights.append(val)
                    if val.startswith('media_player.'):
                        media.append(val)
        new_entity_sensors = [ string for string in sensors if entity in string]
        new_entity_lights = [ string for string in lights if entity in string]
        new_entity_switches = [ string for string in switches if entity in string ]
        new_entity_media = [ string for string in media if entity in string ]
        new_entity = new_entity_sensors + new_entity_switches + new_entity_lights + new_entity_media
        for entity in new_entity:
            if entity.startswith('light.'):
                new_url = url_toggle + "light/" + f"turn_{state}"
            if entity.startswith('switch.'):
                new_url = url_toggle + "switch/" + f"turn_{state}"
            if entity.startswith('sensor.'):
                new_url = url_toggle + "sensor/" + f"turn_{state}"
            if entity.startswith('media_player.'):
                new_url = url_toggle + "switch/" + f"turn_{state}"
        if _return == '':
            if len(new_entity) > 1:
                return {"data": new_entity}, 200
        if len(new_entity) == 1:
            payload = { "entity_id": [new_entity[_return]] }
            check_entity_state = url_states + "/" + new_entity[_return]
            print(payload)
            res = requests.get(check_entity_state, headers=headers)
            print(res)
            return {"data": new_entity}, 200
        if len(new_entity) == 0:
            return {"data": "Problem with entity payload"}, 404
        try:
            check_entity_state = url_states + "/" + new_entity[_return]
            res = requests.get(check_entity_state, headers=headers)
            payload = { "entity_id": [new_entity[_return]] }
            check_entity_state = json.loads(res.text)["state"]
            possible_state = ["on","off"]
                # return {"data": f'{new_entity}'}, 200
            if new_entity[_return] in lights or switches or media or sensors:
                if state in possible_state:
                    if check_entity_state != state:
                        respone = requests.post(new_url, json=payload, headers=headers)
                        if len(respone.text ) != []:
                            return {"data": f"{new_entity[_return]}\nchanged from *{json.loads(res.text)['state'].upper()}* to *{state.upper()}* 👏🏻 🥳 " }, 200
                        else:
                            return {"data": f"I dont know what to do with {entity} 🤷‍♂️ " }, 200
                    else:
                        return {"data": f"{new_entity[_return]} has already *{state.upper()}* 😅"}, 200
                else:
                    return {"data": "This entity state has not supported\nPlease try again 🙄"}, 404
            else:
                return {"data": "This entity dosne't exist !\nPlease try again 🙄"}, 404
        except Exception as e:
            print(e)
            return {"data": "Try again with correct values 🤷‍♂️ "}, 404
    else:
        return {"data": "Your Authorization faild 😱"}, 401

if __name__ == '__main__':
    app.run(debug=True)