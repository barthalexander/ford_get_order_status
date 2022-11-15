import requests

def send_pushover(config, status_object):
    requests.post("https://api.pushover.net/1/messages.json", data = {
        "token": config["PUSHOVER"]["APP_TOKEN"],
        "user": config["PUSHOVER"]["USER_KEY"],
        "message": "vmacsStatusDesc: " + status_object['order']['vmacsStatusDesc'] + "\n" + "vmacsStatusDate: " + status_object['order']['vmacsStatusDate']
    })