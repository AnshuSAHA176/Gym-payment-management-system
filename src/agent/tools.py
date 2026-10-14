
from langchain.tools import tool
from .services import Services
from typing import Optional
import json

BASE_URL = "http://127.0.0.1:8000/"


def Tools(access_token):
    """
    Create the tools available to the gym management AI assistant.

    These tools retrieve payment collection statistics, overdue members,
    member details, and member payment history from the Django backend.

    Args:
        access_token: JWT access token used to authenticate API requests.

    Returns:
        list: LangChain tools available to the AI agent.
    """
    services = Services(
        base_url=BASE_URL,
        access_token=access_token,
    )

    @tool
    def get_monthly_collection(start_date: str, end_date: str):
        """
        Retrieve payment collection statistics for a date range.

        Use this tool when the gym owner asks:
        - How much money was collected during a period?
        - What was the collection total for a particular month?
        - How much was collected between two dates?

        Args:
            start_date: Inclusive start date in YYYY-MM-DD format.
            end_date: Inclusive end date in YYYY-MM-DD format.

        Returns:
            JSON-formatted collection statistics from the backend.

        Example:
            September 2026:
            start_date="2026-09-01"
            end_date="2026-09-30"
        """
        response = services.get_monthly_collection(
            start_date,
            end_date,
        )
        return json.dumps(response)

    @tool
    def get_overdue_members(
        name: Optional[str] = None,
        phone: Optional[str] = None,
        member_id: Optional[str] = None,
    ):
        """
        Retrieve gym members whose payments are overdue.

        Use this tool when the gym owner asks:
        - Who has overdue membership fees?
        - Which members need to pay their fees?
        - Does a particular member have overdue payments?
        - Find overdue members by name, phone, or member ID.

        Args:
            name: Optional member name to filter the results.
            phone: Optional member phone number.
            member_id: Optional unique member identifier.

        Returns:
            JSON-formatted overdue member records from the backend.

        Notes:
            All arguments are optional. Use the available identifying
            information to narrow the search. If no filters are provided,
            the backend determines which overdue members are returned.

            Only report overdue status based on the backend response.
            This tool does not modify payment records.
        """
        response = services.get_overdue_members(
            name=name,
            phone=phone,
            member_id=member_id,
        )
        return json.dumps(response)

    @tool
    def search_members(
        name: Optional[str] = None,
        phone: Optional[str] = None,
        member_id: Optional[str] = None,
    ):
        """
        Search for gym members using their identifying information.

        Use this tool when the gym owner asks:
        - Find a member by name.
        - Look up a member by phone number.
        - Find a member using their unique ID.
        - Retrieve member details before checking payment history.

        Args:
            name: Optional member name to search for.
            phone: Optional member phone number.
            member_id: Optional unique member identifier.

        Returns:
            JSON-formatted member data returned by the backend.

        Notes:
            All arguments are optional. Use the information provided
            by the owner to narrow the search. If multiple members match,
            do not assume they are the same person.

            This tool is read-only and does not modify member records.
        """
        result = services.search_members(
        name=name,
        phone=phone,
        member_id=member_id,
    )

    # Limit results to 10 members.
        if isinstance(result, list):
            result = result[:10]

        return json.dumps(result)


    @tool
    def get_member_payment_history(
        name: Optional[str] = None,
        phone: Optional[str] = None,
        member_id: Optional[str] = None,
    ):
        """
        Retrieve payment history for a gym member using their name,
        phone number, or member ID.

        Use this tool to review previous payments or verify recorded
        payment transactions.

        Args:
            name: Optional member name.
            phone: Optional member phone number.
            member_id: Optional unique member identifier.

        Returns:
            JSON-formatted payment history from the backend.

        Notes:
            - Use available identifying information to find the member.
            - Do not claim a payment was made unless records confirm it.
            - Empty results do not prove that a member never paid.
            - This tool is read-only and does not modify payment records.
        """
        response = services.get_member_payment_history(
            name=name,
            phone=phone,
            member_id=member_id,
        )
        return json.dumps(response)


    return [
        get_monthly_collection,
        get_overdue_members,
        search_members,
        get_member_payment_history,
    ]
