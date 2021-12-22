# This is a sample Python script.
import requests
import json
import datetime
import os
import yaml

def run():
    # Read parameters
    with open("./config.yml", 'r') as fl:
        cfg = yaml.safe_load(fl)
        url = cfg['home_work_1']['url']
        endpoint_api = cfg['home_work_1']['endpoint_api']
        date_start = cfg['home_work_1']['date_start']
        date_end = cfg['home_work_1']['date_end']
        endpoint_auth = cfg['home_work_1']['endpoint_auth']
        username = cfg['home_work_1']['username']
        password = cfg['home_work_1']['password']

    # Generate date range
    start = datetime.datetime.strptime(date_start, "%Y-%m-%d")
    end = datetime.datetime.strptime(date_end, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]

    # ---------------------------------------------------------------
    headers = {"content-type": "application/json"}
    data = {"username": username, "password": password}
    r = requests.post(url+endpoint_auth, headers=headers, data=json.dumps(data))
    token = r.json()['access_token']

    headers = {"content-type": "application/json", "Authorization": "JWT " + token}
    base_dir = "./Home_Work_1/"
    for date in date_generated:
        date_str = date.strftime("%Y-%m-%d")
        print(date_str)
        data = {"date": date_str}
        reply = requests.get(url+endpoint_api, headers=headers, data=json.dumps(data))
        if reply.status_code != 404:
            os.makedirs(os.path.join(base_dir, date_str), exist_ok=True)
            with open(os.path.join(base_dir, date_str, 'data.json'), 'w') as json_file:
                json_file.write(reply.text)
            print(reply.text)
    print("END!!!")

if __name__ == '__main__':
    run()