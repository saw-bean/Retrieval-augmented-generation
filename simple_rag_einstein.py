#!/usr/bin/env python3
"""
Simple RAG Model for Albert Einstein Biography
"""

from typing import List, Dict, Any
from datetime import datetime
# PDF processing
from PyPDF2 import PdfReader
# Import configuration
from config import *

class SimpleRAGSystem: #Simple RAG system for question answering
    
    def __init__(self):
        self.chunks = []
        
        self.mistral_api_key = MISTRAL_API_KEY
        self._initialize_llm()
    
    def _initialize_llm(self):# Initialize the language model
        try:
            # Import Mistral client
            from mistralai.client import MistralClient
            
            # Initialize Mistral client
            self.mistral_client = MistralClient(api_key=self.mistral_api_key)
            print(f" LLM initialized successfully with model: {MODEL_NAME}")
            
        except ImportError as e:
            print(f" Missing dependency: {e}")
            print(" Install required packages: pip install mistralai")
            self.mistral_client = None
            
        except Exception as e:
            print(f" Error initializing LLM: {e}")
            print(" You can still use the retrieval system without LLM")
            self.mistral_client = None
        
    def extract_pdf_text(self, pdf_path: str) -> str: #Extract text from PDF file
   
        try:
            reader = PdfReader(pdf_path)
            text = ""
            
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page_text
            
            print(f" Extracted {len(text)} characters from PDF")
            return text
            
        except Exception as e:
            print(f" Error extracting PDF: {e}")
            return ""
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]: #Split text into chunks

        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                if last_period > chunk_size * 0.7:  # If period is in last 30% of chunk
                    chunk = chunk[:last_period + 1]
                    end = start + last_period + 1
            
            chunks.append(chunk.strip())
            start = end - overlap
            
            if start >= len(text):
                break
        
        print(f" Created {len(chunks)} text chunks")
        return chunks
    
    def simple_similarity_search(self, query: str, chunks: List[str], top_k: int = 3) -> List[str]:
        """Simple similarity search using keyword matching with improved matching"""
        # Expand query words to include synonyms and related terms
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Add synonyms for common terms
        synonyms = {
            'born': ['birth', 'born', 'birthday'],
            'died': ['death', 'died', 'passed'],
            'work': ['worked', 'job', 'career', 'professor', 'university'],
            'equation': ['formula', 'theory', 'e=mc2', 'relativity'],
            'einstein': ['albert', 'einstein'],
            'albert': ['albert', 'einstein']
        }
        
        # Expand query words with synonyms
        expanded_words = set(query_words)
        for word in query_words:
            if word in synonyms:
                expanded_words.update(synonyms[word])
        
        print(f" Searching for: {query}")
        #print(f" Expanded query words: {expanded_words}")
        
        chunk_scores = []
        
        for i, chunk in enumerate(chunks):
            chunk_lower = chunk.lower()
            chunk_words = set(chunk_lower.split())
            
            # Calculate overlap with expanded words
            overlap = len(expanded_words.intersection(chunk_words))
            
            # Bonus points for exact phrase matches
            if query_lower in chunk_lower:
                overlap += 5
            
            # Bonus points for key terms
            if 'birth' in chunk_lower and 'born' in query_lower:
                overlap += 3
            if 'death' in chunk_lower and 'died' in query_lower:
                overlap += 3
            
            chunk_scores.append((overlap, i, chunk))
            
            # Debug: show matches for first few chunks
            # if i < 3:
            #     print(f"  Chunk {i}: {overlap} matches - {list(expanded_words.intersection(chunk_words))}")
        
        # Sort by score (descending) and return top_k
        chunk_scores.sort(reverse=True)
        selected_chunks = [chunk for score, i, chunk in chunk_scores[:top_k] if score > 0]
        
        # print(f" Found {len(selected_chunks)} relevant chunks")
        # if selected_chunks:
        #     print(f" Best chunk preview: {selected_chunks[0][:200]}...")
        
        return selected_chunks
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """Answer a question using simple retrieval"""
        print(f"\n Question: {question}")
        print("-" * 50)
        
        if not self.chunks:
            return {
                "question": question,
                "answer": "No document chunks available. Please process the PDF first.",
                "context": [],
                "timestamp": datetime.now().isoformat()
            }
        
        # Retrieve relevant context
        relevant_chunks = self.simple_similarity_search(question, self.chunks, TOP_K)
        
        if not relevant_chunks:
            return {
                "question": question,
                "answer": "I couldn't find any relevant information to answer this question.",
                "context": [],
                "timestamp": datetime.now().isoformat()
            }
        
        # Combine context documents
        #context_text = "\n\n".join(relevant_chunks)
        
        # Try to use LLM if available
        if hasattr(self, 'mistral_client') and self.mistral_client:
            try:
                # Format the prompt with context and question
                formatted_prompt = PROMPT_TEMPLATE.format(
                    context=context_text,
                    question=question
                )
                
                # Create chat message
                from mistralai.models.chat_completion import ChatMessage
                messages = [
                    ChatMessage(role="user", content=formatted_prompt)
                ]
                
                # Make API call
                chat_response = self.mistral_client.chat(
                    model=MODEL_NAME,
                    messages=messages,
                    temperature=TEMPERATURE
                )
                
                answer = chat_response.choices[0].message.content
                print(f" AI Answer: {answer}")
                
                return {
                    "question": question,
                    "answer": answer,
                    "context": relevant_chunks,
                    "timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                print(f" Error generating AI answer: {e}")
                print(" Falling back to context-only mode")
        
        # Fallback: simple answer generation
        answer = f"Based on the document, here's what I found:\n\n{context_text[:500]}..."
        
        print(f" Answer: {answer}")
        
        return {
            "question": question,
            "answer": answer,
            "context": relevant_chunks,
            "timestamp": datetime.now().isoformat()
        }
    
    def process_document(self, pdf_path: str = PDF_PATH) -> bool:
        """Process the PDF document"""
        print(" Processing document...")
        
        text = self.extract_pdf_text(pdf_path)
        if not text:
            return False
        
        self.chunks = self.chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        
        if self.chunks:
            #print(f"\n Sample chunk (first 200 chars):\n{self.chunks[0][:200]}...")
            return True
        
        return False
    
    # def batch_questions(self, questions: List[str]) -> List[Dict[str, Any]]:
    #     """Answer multiple questions in batch"""
    #     results = []
        
    #     for i, question in enumerate(questions, 1):
    #         print(f"\n Processing question {i}/{len(questions)}")
    #         result = self.answer_question(question)
    #         results.append(result)
        
    #     return results

def interactive_qa(rag_system: SimpleRAGSystem):
    """Interactive question-answering interface"""
    print("\n Interactive Einstein RAG System")
    print("=" * 50)
    print("Ask questions about Albert Einstein!")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            question = input(" Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print(" Goodbye!")
                break
            
            if not question:
                continue
            
            result = rag_system.answer_question(question)
            
            print(f"\n Answer: {result['answer']}")
            
            # show_context = input("\n Show context? (y/n): ").strip().lower()
            # if show_context == 'y':
                # print("\n Retrieved Context:")
                # for i, doc in enumerate(result['context'], 1):
                #     print(f"\n--- Document {i} ---")
                #     print(doc[:500] + "..." if len(doc) > 500 else doc)
            
            print("\n" + "-" * 50)
            
        except KeyboardInterrupt:
            print("\n Goodbye!")
            break
        except Exception as e:
            print(f" Error: {e}")

def main():
    """Main function to run the simple RAG system"""
    print(" Starting Simple Einstein RAG System")
    print("=" * 50)
    
    # Initialize RAG system
    rag_system = SimpleRAGSystem()
    
    # Process the document
    if not rag_system.process_document():
        print(" Failed to process document. Exiting.")
        return
    
    # Ask if user wants to see chunks
    # Test questions
    # test_questions = [
    #     "When was Albert Einstein born?",
    #     "What is Einstein's most famous equation?",
    #     "Where did Einstein work during his career?",
    #     "What was Einstein's contribution to physics?",
    #     "When did Einstein die?"
    # ]
    
    # print("\n Testing RAG System with Sample Questions")
    # print("=" * 60)
    
    # Test all questions
    # all_results = rag_system.batch_questions(test_questions)
    
    # Display results
    # for i, result in enumerate(all_results, 1):
    #     print(f"\n Question {i}: {result['question']}")
    #     print(f" Answer: {result['answer']}")
    #     print(f" Context documents: {len(result['context'])}")
    #     print("-" * 40)
    
    # # Display results summary
    # print(f"\n Processed {len(all_results)} questions successfully")
    
    # Start interactive mode
    print("\n🎯 Starting Interactive Mode...")
    interactive_qa(rag_system)

if __name__ == "__main__":
    main() 