from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .agent import get_agent
from rest_framework import status


class AgentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        access_token = self._get_token(request)
        agent = get_agent(access_token=access_token)
        try:
            messages = request.data["messages"]
        except KeyError:
            return Response(
                {"error": "please enter a valid messages"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = agent.invoke({"messages": [messages]})
        return Response(
            {
                "response":result['messages'][-1].content
            }
        )

    def _get_token(self, request):
        auth_header = request.headers.get(
            "Authorization",
            "",
        )

        return auth_header.replace("Bearer ", "")
