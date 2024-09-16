import requests

class Transaction:
    def __init__(self, api):
        self.api = api
        self.has_sent = False

    def getToken(self, path, point, prediction):
        response = requests.post(self.api + path, json={
            "stationId": 1,
            "point": point,
            "prediction": prediction
        })
        print("status =>", response.status_code)
        if response.status_code == 200:
            data = response.json()
            print(response)
            if data:
                url = "https://liff.line.me/2006195168-xRdLbMlv?token=" + data["token"]
                return url
        return None

    def sendNotify(self, path, binId):
        if not self.has_sent:
            try:
                response = requests.post(self.api + path, json={
                    "stationId": 1,
                    "binId": binId
                })
                print(response.status_code)
                if response.status_code == 200:
                    print(response)
                    data = response.json()
                    return data
            except requests.exceptions.RequestException as e:
                print(f"Error sendNotify: {e}")
                return None

if __name__ == '__main__':
    x = Transaction("https://apibkkbinplus.vercel.app")

    # Uncomment and test getToken if needed
    token_url = x.getToken("/create-transaction", 10, {'ok'})
    # print(f"Token URL: {token_url}")

    # Make sure the API expects a single binId value if that’s the case
    #notify = x.sendNotify("/send-notify", [1])  # Assuming API expects a single binId
    print(notify)
