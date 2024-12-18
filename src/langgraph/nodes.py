from typing import Dict
from src.langgraph.state import GraphState
from src.langchain.chains import LangChainFunctions
from src.tools.database import load_base64_attachment
from src.tools.decoder import extract_text_from_base64
from src.utils.helper_functions import read_documents_in_folder

class RetrievalGraphNode:

    def __init__(self, db_client, llm_model, embedding_model, es_client):
        self.db_client = db_client
        self.es_client = es_client
        self.llm_model = llm_model
        self.embedding_model = embedding_model

    def table_selection(self, state: GraphState) -> Dict:
        response = LangChainFunctions.table_selection(
            model=self.llm_model,
            db_connection=self.db_client,
            user_question=state["user_question"],
        )
        return {"selected_tables": response.tables}
    
    def sql_query_generation(self, state: GraphState) -> Dict:
        response = LangChainFunctions.sql_query_generation(
            model=self.llm_model,
            db_connection=self.db_client,
            selected_tables=state["selected_tables"],
            user_question=state["user_question"]
        )
        return {"sql_query": response.query}
    
    def sql_query_execution(self, state: GraphState) -> Dict:
        try:
            response = self.db_client.run(
                state["sql_query"], 
                include_columns=True
            )
            return {"sql_query_response": response, "sql_query_error_msg": None}
        except Exception as e:
            sql_query_error_msg = state["sql_query_error_msg"].append(str(e))
            return {"sql_query_error_msg": sql_query_error_msg}

    def sql_query_regenerate(self, state: GraphState) -> Dict:
        response = LangChainFunctions.sql_query_regenerate(
            model=self.llm_model,
            user_question=state["user_question"],
            db_connection=self.db_client, 
            query=state["sql_query"],
            runtime_error=state["runtime_error"]
        )
        return {"sql_query": response.query, "sql_query_error_msg": None}
        
    @staticmethod
    def should_continue(state: GraphState):
        sql_query_error_msg = state.get("sql_query_error_msg")
        if sql_query_error_msg is None:
            return "No_Error"
        else:
            return "Error"
    
    def natural_response_creation(self, state: GraphState) -> Dict:
        response = LangChainFunctions.response_generate(
            model=self.llm_model,
            db_connection=self.db_client,
            user_question=state["user_question"],
            query=state["sql_query"],
            selected_tables=state["selected_tables"],
            sql_response=state["sql_query_response"],
            doc_text_content=state["doc_text_content"]
        )
        return {"final_response": response.content}

    def intent_filter_creation(self, state: GraphState) -> Dict:
        response = LangChainFunctions.desired_filter_identification(
            model=self.llm_model,
            user_question=state["user_question"],
            query=state["sql_query"],
            db_connection=self.db_client,
            sql_response=state["sql_query_response"]
        )
        return {"filtered_projects": response.projects}
    
    def parse_project_attachments(self, state: GraphState) -> Dict:
        base64_attachment = load_base64_attachment.invoke(
            {
                "projects": state["filtered_projects"]
            }
        )
        for _file in base64_attachment:
            if _file["pyAttachStream"] != None:
                extract_text_from_base64.invoke(
                    {
                        "base64_data": _file["pyAttachStream"],
                        "output_file_path": _file["pxAttachName"]
                    }
                )
        doc_content = read_documents_in_folder()

        return {"doc_text_content": doc_content}
        

    