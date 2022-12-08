import os
import requests
from fastapi import HTTPException

backoffice_base_url = os.getenv("BACKOFFICE_BASE_URL")


def send_login_notification_to_backoffice(reg_method):
    url = backoffice_base_url + "/metrics/logins?method=" + reg_method
    response = requests.post(url=url)

    if response.ok:
        return response.json()
    raise HTTPException(
        status_code=response.status_code, detail=response.json()["detail"]
    )
