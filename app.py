import json
import os
import requests

from flask import Flask
from flask import make_response
from flask import request
from flask_ask import Ask, statement, question

# Flask app should start in global layout
app = Flask(__name__)
ask = Ask(app, '/webhook')


# Dialogflow Code
@app.route('/webhook', methods=['POST'])
def webhook():
    print("Webhook contacted successfully!")
    req = request.get_json(silent=True, force=True)

    # print("Request:")
    # print(json.dumps(req, indent=4))
    # comment to deploy

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):
    if req.get("result").get("action") == "collibra.search":

        print("SEARCH INTENT")

        # get all parameters
        result = req.get("result")
        parameters = result.get("parameters")
        contexts = result.get("contexts")
        asset_name = ""

        for c in contexts:
            if c.get("name") == "asset-known":
                asset_name = c.get("parameters").get("asset")

        if asset_name == "":
            asset_name = parameters.get("asset")

        print("Asset name: ", asset_name)

        # rest call to advanced connect
        # 200
        response = requests.request('GET', "https://53-dgc-nightly.collibra.com/rest/1.0/application/version")
        # 404
        # response = requests.request('GET', "https://thebest404pageeverredux.com/swf/indx.html")

        print("Status code: ", response.status_code)
        print("Response: ", response.text)

        if response.status_code == requests.codes.not_found:
            return {
                "speech": "Do you want to create it?",
                "displayText": "Do you want to create it?",
                "followupEvent": {
                    "name": "decide"
                }
            }

        else:
            return {
                "speech": response.text,
                "displayText": response.text,
                # "data": {},
                # "contextOut": [],
                "source": "apiai-collibra-dc18-demo"
            }
    elif req.get("result").get("action") == "collibra.decide":
        print("DECIDE INTENT")

        # get all parameters
        result = req.get("result")
        parameters = result.get("parameters")
        contexts = result.get("contexts")
        action = ""

        for c in contexts:
            if c.get("name") == "asset-known":
                action = c.get("parameters").get("action")

        if action == "":
            action = parameters.get("action")

        if action == "retry":
            return {
                "followupEvent": {
                    "name": "search"
                }
            }
        elif action == "create asset":
            return {
                "followupEvent": {
                    "name": "create-asset"
                }
            }

    elif req.get("result").get("action") == "collibra.create":
        print("CREATE INTENT")

        # get all parameters
        result = req.get("result")
        contexts = result.get("contexts")
        asset_name = ""
        context = ""
        for c in contexts:
            if c.get("name") == "asset-known":
                asset_name = c.get("parameters").get("asset")
                context = c.get("parameters").get("context")

        print("contexts: ", contexts)
        print("name: ", asset_name)
        print("context: ", context)

        # rest call to basic connect
        # response = requests.request('GET', "https://53-dgc-nightly.collibra.com/rest/1.0/application/version")
        # print("Status code: ", response.status_code)
        # print("Response: ", response.text)

        speech = "I have created the asset named " + asset_name + " in the context of " + context

        return {
            "speech": speech,
            "displayText": speech
        }




    else:
        return {}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
