"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (you can keep these; new schemas are added below):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# --------------------------------------------------
# Learning Notes App Schemas (used by the application)
# --------------------------------------------------

class Context(BaseModel):
    """
    Contexts collection schema
    Collection name: "context"
    Represents a topic/category for grouping notes.
    """
    name: str = Field(..., description="Display name of the context/topic")
    description: Optional[str] = Field(None, description="Short description")
    language: Optional[str] = Field(None, description="Language code for this context, e.g., 'en', 'de'")

class Note(BaseModel):
    """
    Notes collection schema
    Collection name: "note"
    Represents a single learning note that can be used for flashcards/quizzes.
    """
    title: str = Field(..., description="Short title or question")
    content: str = Field(..., description="Detailed explanation or answer")
    context_id: Optional[str] = Field(None, description="ID of the related context")
    language: Optional[str] = Field(None, description="Language code, e.g., 'en', 'de'")
    tags: List[str] = Field(default_factory=list, description="List of tag strings")
    source: Optional[str] = Field(None, description="Optional source or link")
    hint: Optional[str] = Field(None, description="Optional hint for learning modes")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
