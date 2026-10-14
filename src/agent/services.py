import requests


class Services:
    def __init__(self, base_url, access_token):
        self.base_url = base_url.rstrip("/") + "/"
        self.access_token = access_token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _get(self, endpoint, params=None):
        response = requests.get(
            f"{self.base_url}{endpoint}",
            headers=self._headers(),
            params=params or {},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def get_monthly_collection(self, start_date: str, end_date: str):
        return self._get(
            "payment/summary/",
            {
                "start_date": start_date,
                "end_date": end_date,
            },
        )

    def get_overdue_members(self, name=None, phone=None, member_id=None):
        params = {
            key: value
            for key, value in {
                "name": name,
                "phone": phone,
                "member_id": member_id,
            }.items()
            if value
        }
        return self._get("members/overdue/", params)

    def search_members(self, name=None, phone=None, member_id=None):
        params = {
            key: value
            for key, value in {
                "name": name,
                "phone": phone,
                "member_id": member_id,
            }.items()
            if value
        }
        return self._get("members/", params)

    def get_member_payment_history(
        self,
        name=None,
        phone=None,
        member_id=None,
        start_date=None,
        end_date=None,
    ):
        params = {}

        if member_id:
            params["member"] = member_id
        elif name:
            params["search"] = name
        elif phone:
            params["search"] = phone

        if start_date:
            params["start_date"] = start_date

        if end_date:
            params["end_date"] = end_date

        return self._get("payment/", params)
