from pathlib import Path

RUNTIME_CONFIG_FILE_PATH = Path("./params/runtime.yml")

TABLE_SELECTION_PROMPT_TEMPLATE = "prompts/TableSelection.yml"
SQL_QUERY_GENERATION_TEMPLATE = "prompts/SQLQueryGeneration.yml"
SQL_QUERY_REGENERATE_TEMPLATE = "prompts/SQLQueryRegenerate.yml"
RESPONSE_GENERATE_TEMPLATE = "prompts/ResponseGenerate.yml"
INTENT_FILTER_TEMPLATE = "prompts/IntentFilter.yml"