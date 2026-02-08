import requests
import json
import datetime


webhook_url = "YOUR_URL_HERE"

def send_webhook(run_time: str, num_runs: int, task_name: int, img):

    if True:

        payload = {
            
        "username": "Milky Way Cookie",
        "avatar_url": "https://i.pinimg.com/736x/f6/6a/72/f66a723e8c68fecc5bbbdca927fc4888.jpg",
        "embeds": [
            {
            "title": "mettaneko.ru",
            "description": "",
            "color": 3447003,
            "fields": [
                {
                "name": "🕒 Время работы",
                "value": run_time,
                "inline": True
                },

                {
                "name": "🔁 Общее количество матчей",
                "value": num_runs,
                "inline": True
                },
                {
                "name": "⚙️ Текущая задача",
                "value": task_name
                }
            ],
            "image": {
                "url": "attachment://screenshot.png",
            },
            "thumbnail": {
                "url": "https://media1.tenor.com/m/m0KNx_D9YKoAAAAC/dio-the-world.gif",
            },
            "footer": {
                "text": f"mettaneko.ru | Время работы: {run_time}"
            },
            "timestamp": datetime.datetime.utcnow().isoformat()
            }
        ]
        }
        files = {
            "file": ("screenshot.png", img, "image/png")  # name must match attachment:// name
    
        }

        

        response = requests.post(webhook_url, data={"payload_json": json.dumps(payload)}, files=files)
        #print(response.status_code, response.text)
    else:
        print("Error, no wins or losses detected")
