from typing import List, Dict
from typing_extensions import TypedDict

class GraphState(TypedDict):
    user_question: str
    selected_tables: List[str]
    selected_columns: List[str]
    sql_query: str
    sql_query_error_msg: List[str]
    sql_query_response: str
    filtered_projects: List[str]
    final_response: str
    doc_text_content: Dict[str, str]
    