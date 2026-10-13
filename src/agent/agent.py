from langgraph.graph import StateGraph,START,END,add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel
from typing import Annotated
from .llm import get_model
from .tools import Tools

model = get_model()
class State(BaseModel):
    messages : Annotated[list,add_messages]

def get_agent(access_token):

    tools = Tools(access_token=access_token)
    model_with_tool = model.bind_tools(tools=tools)

    def agent(state:State):
        return {"messages":[model_with_tool.invoke(state.messages)]}

    graph_builder = StateGraph(State)

    graph_builder.add_node('agent',agent)
    graph_builder.add_node('tools',ToolNode(tools))
    graph_builder.add_edge(START,'agent')
    graph_builder.add_conditional_edges('agent',tools_condition)
    graph_builder.add_edge('tools','agent')

    return graph_builder.compile()