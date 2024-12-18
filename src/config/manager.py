from src.constants import RUNTIME_CONFIG_FILE_PATH
from src.utils.helper_functions import read_yaml_file
from src.entity.entity_config import ElasticSearchConfig, LLMConfig, EmbeddingModelConfig, DatabaseConfig


class ConfigurationManager:
    def __init__(self, params_file_path=RUNTIME_CONFIG_FILE_PATH) -> None:
        self.config = read_yaml_file(params_file_path)

    def get_database_config(self) -> DatabaseConfig:
        return DatabaseConfig(
            host=self.config.Database.host,
            name=self.config.Database.name,
            username=self.config.Database.username,
            password=self.config.Database.password,
            odbc_driver=self.config.Database.odbc_driver,
            trusted_server_certificate=self.config.Database.trusted_server_certificate,
            encrypt=self.config.Database.encrypt,
        )

    def get_elasticsearch_config(self) -> ElasticSearchConfig:
        return ElasticSearchConfig(
            user_id=self.config.ElasticSearch.user_id,
            password=self.config.ElasticSearch.password,
            hosts=self.config.ElasticSearch.hosts,
            certificate_path=self.config.ElasticSearch.certificate_path,
        )

    def get_llm_model_config(self) -> LLMConfig:
        return LLMConfig(
            top_p=self.config.LLM.top_p,
            temperature=self.config.LLM.temperature,
            api_key=self.config.LLM.api_key,
            base_url=self.config.LLM.base_url,
            model_name=self.config.LLM.model_name,
        )

    def get_embedding_config(self) -> EmbeddingModelConfig:
        return EmbeddingModelConfig(
            model_name=self.config.Embedding.model_name,
        )
