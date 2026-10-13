from langchain.tools import tool
from .services import Services
import json

BASE_URL = "http://127.0.0.1:8000/"


def Tools(access_token):

    services = Services(base_url=BASE_URL, access_token=access_token)
    @tool
    def get_monthly_collection():
        """
        Retrieve the gym's monthly payment collection statistics.

        Use this tool when the user asks about:
        - Total money collected during the current month.
        - Monthly payment collection statistics.
        - How much the gym earned from recorded payments.
        - The number of payments or collection totals for the month.

        Returns:
            str: JSON-serialized collection statistics returned by
                the Django backend.

        Note:
            This tool only retrieves information. It does not create,
            update, or delete payment records.
        """
        response = services.get_monthly_collection()
        return json.dumps(response)

    return [get_monthly_collection]