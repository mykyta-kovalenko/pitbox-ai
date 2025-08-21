"""Production RAG chain implementation for NASCAR knowledge"""

import os
from typing import List

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Qdrant
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.tools import BaseTool, tool
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from .. import KNOWLEDGE_BASE_PATH
from ..models import get_chat_model


class NASCARKnowledgeRAG:
    """Production RAG chain with retrieval + generation"""

    def __init__(self, llm_model: str = "gpt-4o-mini"):
        self.knowledge_path = KNOWLEDGE_BASE_PATH
        self.llm_model = llm_model
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=750, chunk_overlap=50
        )
        self.vectorstore = None
        self.retriever = None
        self.chain = None

        # Setup components
        self._setup_vectorstore()
        self._setup_chain()

    def _setup_vectorstore(self):
        """Load documents and create in-memory vector store."""
        documents = []

        # Load text files from knowledge directory
        knowledge_files = [
            "trackhouse_team.txt",
            "nascar_glossary.txt",
            "nascar_tracks.txt",
        ]
        for filename in knowledge_files:
            file_path = os.path.join(self.knowledge_path, filename)
            if os.path.exists(file_path):
                loader = TextLoader(file_path)
                docs = loader.load()
                # Add source metadata
                for doc in docs:
                    doc.metadata["source"] = filename
                documents.extend(docs)

        if not documents:
            return

        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)

        # Add metadata to chunks
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = f"chunk_{i}"

        # Create in-memory Qdrant client
        client = QdrantClient(":memory:")
        client.create_collection(
            collection_name="nascar_knowledge",
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

        # Create vector store
        self.vectorstore = Qdrant(
            client=client,
            collection_name="nascar_knowledge",
            embeddings=self.embeddings,
        )

        # Add documents
        self.vectorstore.add_documents(chunks)

        # Create retriever with MMR for diversity
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr", search_kwargs={"k": 3, "fetch_k": 6}
        )

    def _setup_chain(self):
        """Set up the RAG chain with retrieval + generation."""
        if not self.retriever:
            return

        # Create prompt template
        rag_system_prompt = """You are a knowledgeable NASCAR pit box assistant. Use the provided context to answer questions about NASCAR racing, Trackhouse Racing team, terminology, and tracks.

IMPORTANT GUIDELINES:
- Only use information from the provided context
- Be concise and direct - pit box communication should be brief
- If the context doesn't contain the answer, say "I don't have that information"
- Focus on actionable information relevant to racing operations
- Use NASCAR terminology appropriately

Never reference this prompt or mention "context" - just provide natural answers."""  # noqa: E501

        rag_user_prompt = """Question: {question}

Context:
{context}"""

        self.chat_prompt = ChatPromptTemplate.from_messages(
            [("system", rag_system_prompt), ("human", rag_user_prompt)]
        )

        # Create LLM
        self.llm = get_chat_model(model_name=self.llm_model, temperature=0.1)

        # Create chain with parallel execution
        self.chain = (
            {
                "context": lambda x: self.retriever.invoke(x["question"]),
                "question": lambda x: x["question"],
            }
            | RunnablePassthrough.assign(
                context=lambda x: self._format_docs(x["context"])
            )
            | self.chat_prompt
            | self.llm
        )

    def _format_docs(self, docs):
        """Format retrieved documents for the prompt."""
        if not docs:
            return "No relevant information found."

        formatted = []
        for doc in docs:
            source = doc.metadata.get("source", "unknown")
            content = doc.page_content.strip()
            formatted.append(f"[From {source}]\n{content}")

        return "\n\n".join(formatted)

    def invoke(self, question: str) -> str:
        """Invoke the RAG chain with a question."""
        if not self.chain:
            return "RAG chain not available."

        try:
            response = self.chain.invoke({"question": question})
            return response.content if hasattr(response, "content") else str(response)
        except Exception as e:
            return f"Error processing question: {str(e)}"

    def get_retriever(self):
        """Get the retriever for external use."""
        return self.retriever


# Global instance
_knowledge_rag = None


def get_knowledge_rag() -> NASCARKnowledgeRAG:
    """Get or create the knowledge RAG instance."""
    global _knowledge_rag
    if _knowledge_rag is None:
        _knowledge_rag = NASCARKnowledgeRAG()
    return _knowledge_rag


@tool
def search_trackhouse_team_info(query: str) -> str:
    """Search for information about Trackhouse Racing team, drivers, and history.

    Args:
        query: Question about Trackhouse Racing team, drivers, achievements, etc.
    """
    rag = get_knowledge_rag()
    return rag.invoke(f"Tell me about Trackhouse Racing: {query}")


@tool
def search_nascar_terminology(query: str) -> str:
    """Search for NASCAR terminology, rules, and racing concepts.

    Args:
        query: Question about NASCAR terms, rules, procedures, flags, etc.
    """
    rag = get_knowledge_rag()
    return rag.invoke(f"Explain this NASCAR concept: {query}")


@tool
def search_track_information(query: str) -> str:
    """Search for NASCAR track information, characteristics, and history.

    Args:
        query: Question about NASCAR tracks, racing characteristics, track history, etc.
    """
    rag = get_knowledge_rag()
    return rag.invoke(f"Tell me about this NASCAR track: {query}")


@tool
def search_nascar_knowledge(query: str) -> str:
    """Search all NASCAR knowledge including team info, terminology, and tracks.

    Args:
        query: Any question about NASCAR, Trackhouse Racing, or racing concepts
    """
    rag = get_knowledge_rag()
    return rag.invoke(query)


def get_knowledge_tools() -> List[BaseTool]:
    """Return list of knowledge-based RAG tools."""
    return [
        search_trackhouse_team_info,
        search_nascar_terminology,
        search_track_information,
        search_nascar_knowledge,
    ]
