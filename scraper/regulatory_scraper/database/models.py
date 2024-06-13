import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY  
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum  

BasePostgres = declarative_base()
BaseSQLite = declarative_base()

class Jurisdiction(Enum):
    UK = "UK"
    EU = "EU"
    US = "US"

class DocumentBin(BaseSQLite):
    __tablename__ = 'documents_bin'

    id = Column(Integer, primary_key=True)
    file_url = Column(String, unique=True, nullable=False, index=True)

class DocumentChecksum(BasePostgres):
    __tablename__ = 'documents_checksums'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    checksum = Column(String, nullable=False)
    file_url = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

class Document(BasePostgres):
    __tablename__ = 'documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_url = Column(String, unique=True, nullable=False, index=True)
    file_s3_path = Column(String, nullable=False)
    regulation_body = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    keywords = Column(ARRAY(Text), nullable=False)
    jurisdiction = Column(SQLAlchemyEnum(Jurisdiction), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    category = relationship("Category", back_populates="documents")

class Category(BasePostgres):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

    documents = relationship("Document", back_populates="category")
