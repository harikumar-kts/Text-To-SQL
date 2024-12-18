from langgraph.graph import END, StateGraph
from src.langgraph.state import GraphState
from src.langgraph.nodes import RetrievalGraphNode

def create_retrieval_graph(db_client, llm_model, embedding_model, es_client):

    graph = StateGraph(GraphState)
    node = RetrievalGraphNode(db_client, llm_model, embedding_model, es_client)

    graph.add_node("Table Selection", node.table_selection)
    graph.add_node("Query Generation", node.sql_query_generation)
    graph.add_node("Intent Filter", node.intent_filter_creation)
    graph.add_node("Query Regenerate", node.sql_query_regenerate)
    graph.add_node("Query Execution", node.sql_query_execution)
    graph.add_node("Parse Attachments", node.parse_project_attachments)
    graph.add_node("Response Generation", node.natural_response_creation)

    graph.set_entry_point("Table Selection")
    graph.add_edge("Table Selection", "Query Generation")
    graph.add_edge("Query Generation", "Query Execution")
    graph.add_conditional_edges(
        "Query Execution",
        node.should_continue,
        {
            "No_Error": "Intent Filter",
            "Error": "Query Regenerate"
        }
    )
    graph.add_edge("Query Regenerate", "Query Execution")
    graph.add_edge("Intent Filter", "Parse Attachments")
    graph.add_edge("Parse Attachments", "Response Generation")
    graph.add_edge("Response Generation", END)

    workflow = graph.compile(checkpointer=False)

    return workflow
