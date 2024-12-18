from langchain_groq import ChatGroq
from src.entity.entity_config import LLMConfig, EmbeddingModelConfig
from sentence_transformers import SentenceTransformer


class Models:

    @staticmethod
    def llm_model_connection(llm_config: LLMConfig) -> ChatGroq:
        return ChatGroq(
            api_key=llm_config.api_key,
            temperature=llm_config.temperature,
            model_name=llm_config.model_name
        )

    @staticmethod
    def embedding_model_connection(embed_config: EmbeddingModelConfig) -> SentenceTransformer:
        return SentenceTransformer(
            model_name_or_path=embed_config.model_name,
            trust_remote_code=True
        )
