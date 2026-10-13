import requests


class Services:
    def __init__(self, base_url, access_token):
        self.base_url = base_url
        self.access_token = access_token

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def get_monthly_collection(
        self,
        start_date: str,
        end_date: str,
    ):

        response = requests.get(
            f"{self.base_url}payment/summary/",
            headers=self._headers(),
            params={
                "start_date": start_date,
                "end_date": end_date,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def get_overdue_members(
        self,
        name=None,
        phone=None,
        member_id=None,
    ):

        params = {}

        if name:
            params["name"] = name

        if phone:
            params["phone"] = phone

        if member_id:
            params["member_id"] = member_id

        
        response = requests.get(
            f"{self.base_url}members/overdue/", headers=self._headers(), params=params
        )
        response.raise_for_status()
        return response.json()
