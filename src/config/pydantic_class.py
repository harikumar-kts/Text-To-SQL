from typing import List
from pydantic import BaseModel, Field

class SelectedTables(BaseModel):
    """List of selected tables"""
    tables: List[str] = Field(description="List of table name")
    reasoning: str = Field(description="Reason for choosing the table")


class SQLQuery(BaseModel):
    """Response SQL Query"""
    query: str = Field(description="SQL query")


class IntentFilter(BaseModel):
    """Query intent keys"""
    projects: List[str] = Field(description="List of project")
    