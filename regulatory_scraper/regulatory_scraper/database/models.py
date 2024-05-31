import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship

BaseSQLite = declarative_base()
BasePostgres = declarative_base()

class DocumentChecksum(BaseSQLite):
    __tablename__ = 'documents_checksums'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    checksum = Column(String, nullable=False)
    file_url = Column(String, unique=True, nullable=False)
    last_accessed = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())

class Document(BasePostgres):
    __tablename__ = 'documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_url = Column(String, unique=True, nullable=False)
    file_s3_path = Column(String, nullable=False)
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
