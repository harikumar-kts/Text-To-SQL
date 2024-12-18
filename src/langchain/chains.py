from typing import List, Dict
from src.constants import *
from langchain_groq import ChatGroq
from langchain_core.prompts import load_prompt
from src.config.pydantic_class import SelectedTables, SQLQuery, IntentFilter
from langchain_community.utilities.sql_database import SQLDatabase


class LangChainFunctions:

    @staticmethod
    def desired_filter_identification(
        model: ChatGroq,
        user_question: str
    ):
        pass

    @staticmethod
    def table_selection(
        model: ChatGroq,
        user_question: str,
        db_connection: SQLDatabase
    ):
        table_selection_prompt_template = load_prompt(
            TABLE_SELECTION_PROMPT_TEMPLATE
        )
        structured_llm = model.with_structured_output(
            SelectedTables,
            method="json_mode"
        )
        table_selection_chain = table_selection_prompt_template | structured_llm
        db_info = db_connection.get_table_info()
        return table_selection_chain.invoke(
            {
                "query": user_question,
                "db_info": db_info
            }
        )

    @staticmethod
    def sql_query_generation(
        model: ChatGroq,
        user_question: str,
        selected_tables: List[str],
        db_connection: SQLDatabase
    ):
        query_generation_prompt_template = load_prompt(
            SQL_QUERY_GENERATION_TEMPLATE
        )
        structured_llm = model.with_structured_output(
            SQLQuery,
            method="json_mode"
        )
        query_generation_chain = query_generation_prompt_template | structured_llm
        return query_generation_chain.invoke(
            {
                "query": user_question,
                "tables": selected_tables,
                "db_info": db_connection.get_table_info(table_names=selected_tables)
            }
        )
    
    @staticmethod
    def sql_query_regenerate(
        model: ChatGroq,
        user_question: str,
        db_connection: SQLDatabase,
        query: str,
        runtime_error: str,
    ):
        query_regenerate_prompt_template = load_prompt(
            SQL_QUERY_REGENERATE_TEMPLATE
        )
        structured_llm = model.with_structured_output(
            SQLQuery,
            method="json_mode"
        )
        query_regenerate_chain = query_regenerate_prompt_template | structured_llm
        return query_regenerate_chain.invoke(
            {
                "user_question": user_question,
                "query": query,
                "db_info": db_connection.get_table_info(),
                "runtime_error": runtime_error
            }
        )

    @staticmethod
    def response_generate(
        model: ChatGroq,
        db_connection: SQLDatabase,
        user_question: str,
        query: str,
        selected_tables: List[str],
        sql_response: str,
        doc_text_content: Dict[str, str]
    ):
        doc_content = ""
        for key, value in doc_text_content.items():
            doc_content = doc_content + "/n" + value

        response_generation_prompt_template = load_prompt(
            RESPONSE_GENERATE_TEMPLATE
        )
        response_generation_chain = response_generation_prompt_template | model
        return response_generation_chain.invoke(
            {
                "user_question": user_question,
                "query_response": sql_response,
                "doc_content": doc_content
            }
        )
    
    @staticmethod
    def desired_filter_identification(
        model: ChatGroq,
        user_question: str,
        query: str,
        db_connection: SQLDatabase,
        sql_response: str,
    ):
        intent_filter_prompt_template = load_prompt(
            INTENT_FILTER_TEMPLATE
        )
        structured_llm = model.with_structured_output(
            IntentFilter,
            method="json_mode"
        )
        intent_filter_chain = intent_filter_prompt_template | structured_llm
        return intent_filter_chain.invoke(
            {
                "schema": db_connection.get_table_info(),
                "user_query": user_question,
                "query": query,
                "sql_response": sql_response
            }
        )        
