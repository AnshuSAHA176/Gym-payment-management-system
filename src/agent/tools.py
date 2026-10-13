from langchain.tools import tool
from .services import Services
import json

BASE_URL = "http://127.0.0.1:8000/"


def Tools(access_token):

    services = Services(base_url=BASE_URL, access_token=access_token)
  
    @tool
    def get_monthly_collection(start_date: str, end_date: str):
        """
        Get gym payment collection statistics for a date range.

        Use this tool when the user asks about collection totals
        for a particular month or period.

        Examples:
        - September 2026: start_date="2026-09-01",
        end_date="2026-09-30"
        - October 2026: start_date="2026-10-01",
        end_date="2026-10-31"

        Args:
            start_date: Start date in YYYY-MM-DD format.
            end_date: End date in YYYY-MM-DD format.

        Returns:
            JSON-formatted collection statistics.
        """
        response = services.get_monthly_collection(start_date, end_date)
        return json.dumps(response)


    return [get_monthly_collection]