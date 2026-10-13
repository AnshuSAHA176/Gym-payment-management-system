from langchain.tools import tool
from .services import Services
import json
from typing import Optional

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

    @tool
    def get_overdue_members(
        name: Optional[str] = None,
        phone: Optional[str] = None,
        member_id: Optional[str] = None,
    ):
        """
    Retrieve members whose gym membership payments are overdue.

    Use this tool when the user asks:
    - Which members have overdue fees?
    - Does a specific member have unpaid or overdue payments?
    - Find overdue members by name, phone number, or member ID.
    - Check whether a particular member has overdue fees.

    Args:
        name: Optional member name to search for.
        phone: Optional phone number to identify or filter members.
        member_id: Optional unique ID of a specific member.

    Returns:
        str: JSON-formatted data containing overdue member records
        returned by the Django backend.

    Notes:
        - All arguments are optional.
        - Use the available identifying information to narrow the search.
        - If no arguments are provided, retrieve all overdue members
          supported by the backend endpoint.
        - This tool is read-only and does not modify payment records.
    """
        response = services.get_overdue_members(
            name=name, phone=phone, member_id=member_id
        )
        return json.dumps(response)

    return [get_monthly_collection, get_overdue_members]
