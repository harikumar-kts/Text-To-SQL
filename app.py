import os
import mlflow
import uvicorn
import mlflow.langchain
from pydantic import BaseModel
from fastapi import FastAPI, Depends

from src.model.load import Models
from src.tools.database import Database
from src.langgraph.graph import create_retrieval_graph
from src.tools.elasticsearch import ElasticSearch
from src.config.manager import ConfigurationManager

import warnings
warnings.filterwarnings("ignore")
mlflow.set_experiment("Text2SQL Tracing")

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = "TEXT2SQL"

class InputSchema(BaseModel):
    question: str


class OutputSchema(BaseModel):
    status: int
    question: str
    response: str


app = FastAPI(
    title="LangGraph Server",
    version="0.1",
    description="SQL Knowledgebase retrieval API Server"
)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Initialization(metaclass=SingletonMeta):
    def __init__(self):
        self.config = ConfigurationManager()
        self.db_config = self.config.get_database_config()
        self.llm_config = self.config.get_llm_model_config()
        self.embedding_config = self.config.get_embedding_config()
        self.elasticsearch_config = self.config.get_elasticsearch_config()
        
        self.db = self.initialize_db()
        self.llm = self.initialize_llm_model()
        self.embedding = self.initialize_embedding_models()
        self.es_client = self.initialize_elasticsearch_client()
    
    def initialize_db(self):
        print("Loading DB Connection ..........")
        db = Database.client_initialization(
            db_config=self.db_config
        )
        return db

    def initialize_llm_model(self):
        print("Loading LLM Model ..........")
        return Models.llm_model_connection(
            llm_config=self.llm_config
        )

    def initialize_embedding_models(self):
        print("Loading Embedding Model ..........")
        return Models.embedding_model_connection(
            embed_config=self.embedding_config
        )

    def initialize_elasticsearch_client(self):
        print("Elasticsearch Client Initializing ..........")
        return ElasticSearch.client_initialization(
            elastic_config=self.elasticsearch_config
        )


def initialization_process():
    initial_obj = Initialization()
    return initial_obj


def get_workflow_app(obj=Depends(initialization_process)):
    if not hasattr(get_workflow_app, "workflow_app"):
        get_workflow_app.workflow_app = create_retrieval_graph(
            db_client=obj.db,
            llm_model=obj.llm,
            embedding_model=obj.embedding,
            es_client=obj.es_client,
        )
        print("LangGraph Workflow Created ..........")
    return get_workflow_app.workflow_app


@app.post('/predict', response_model=OutputSchema)
async def knowledge_base_retrieval(data: InputSchema, workflow_app=Depends(get_workflow_app)):
    # mlflow.langchain.autolog(log_traces=True)
    result = await workflow_app.ainvoke(
            {
                "user_question": data.question
            },
            {"recursion_limit": 10}
        )
    return OutputSchema(
        status=200,
        question=str(result.get('user_question', '')),
        response=str(result.get('final_response', '')),
    )

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
