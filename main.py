# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import asyncio
# from document_processor import DocumentProcessor
# from vector_store import VectorStore
# from llm_processor import LLMProcessor
#
# app = FastAPI(title="HackRx 6.0 Query-Retrieval System")
#
# class QueryRequest(BaseModel):
#     documents: str  # URL to the document
#     questions: list[str]
#
# class Answer(BaseModel):
#     question: str
#     answer: str
#     rationale: dict
#
# class QueryResponse(BaseModel):
#     answers: list[Answer]
#
# # Initialize components
# doc_processor = DocumentProcessor(chunk_size=512, chunk_overlap=50)
# vector_store = VectorStore()
# llm_processor = LLMProcessor()
#
# @app.post("/hackrx/run", response_model=QueryResponse)
# async def process_queries(request: QueryRequest):
#     try:
#         # Process document from URL
#         document_chunks = doc_processor.process_document_from_url(request.documents)
#         vector_store.add_documents(document_chunks)
#
#         answers = []
#         for question in request.questions:
#             relevant_contexts = vector_store.similarity_search(question, k=5)
#             answer, rationale = llm_processor.generate_answer(question, relevant_contexts)
#             answers.append(Answer(question=question, answer=answer, rationale=rationale))
#
#         return QueryResponse(answers=answers)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from document_processor import DocumentProcessor
from vector_store import VectorStore
from llm_processor import LLMProcessor

app = FastAPI(title="HackRx 6.0 Query-Retrieval System")


class QueryRequest(BaseModel):
    documents: str
    questions: list[str]


class QueryResponse(BaseModel):
    answers: list[str]


doc_processor = DocumentProcessor(chunk_size=512, chunk_overlap=50)
vector_store = VectorStore()
llm_processor = LLMProcessor()


@app.post("/hackrx/run", response_model=QueryResponse)
async def process_queries(request: QueryRequest):
    try:
        document_chunks = doc_processor.process_document_from_url(request.documents)
        vector_store.add_documents(document_chunks)

        answers = []
        for question in request.questions:
            relevant_contexts = vector_store.similarity_search(question, k=5)
            answer, _ = llm_processor.generate_answer(question, relevant_contexts)
            answers.append(answer)

        return QueryResponse(answers=answers)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
