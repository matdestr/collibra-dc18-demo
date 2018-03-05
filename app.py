import json
import os
import requests

from flask import Flask
from flask import make_response
from flask import request

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "collibra.search":

        # get all parameters
        result = req.get("result")
        parameters = result.get("parameters")
        asset_name = parameters.get("asset")

        # rest call
        response = requests.request('GET',"https://53-dgc-nightly.collibra.com/rest/1.0/application/version")
        print("Status code: ", response.status_code)
        print("Response: ", response.text )


        return {
            "speech": response.text,
            "displayText": response.text,
            # "data": {},
            # "contextOut": [],
            "source": "apiai-collibra-dc18-demo"
        }

    else:
        return {}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
