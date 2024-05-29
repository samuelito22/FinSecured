from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
#from database import DatabaseManager

class DocVectorizePipeline:
    def __init__(self):
        self.document = None
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=80)
        self.embeddings = HuggingFaceEmbeddings()
        self.chunks = None
        #self.db_manager = DatabaseManager()

    def load_pdf_document(self, pdf_doc):
        loader = PyPDFLoader(pdf_doc)
        self.document = loader.load()[0]

    def split_into_chunks(self):
        self.chunks = self.text_splitter.split_documents([self.document])

    def vectorize_chunks(self):
        for chunk in self.chunks:
            embedding = self.embeddings.embed_query(chunk.page_content)
            #self.db_manager.insert_embedding(chunk.page_content, embedding)