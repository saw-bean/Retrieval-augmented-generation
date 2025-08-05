#!/usr/bin/env python3
"""
View chunks created by the RAG system
"""

from simple_rag_einstein import SimpleRAGSystem

def view_chunks():
    """Display all chunks created from the PDF"""
    print("🔍 Viewing PDF Chunks")
    print("=" * 50)
    
    # Initialize RAG system
    rag_system = SimpleRAGSystem()
    
    # Process the document
    if not rag_system.process_document():
        print("❌ Failed to process document.")
        return
    
    print(f"\n📊 Total chunks created: {len(rag_system.chunks)}")
    print("=" * 50)
    
    # Display all chunks
    for i, chunk in enumerate(rag_system.chunks):
        print(f"\n📄 CHUNK {i+1}/{len(rag_system.chunks)}")
        print("-" * 40)
        print(f"Length: {len(chunk)} characters")
        print("Content:")
        print(chunk)
        print("=" * 50)
        
        # Ask if user wants to continue
        if i < len(rag_system.chunks) - 1:  # Not the last chunk
            response = input(f"\nContinue to next chunk? (y/n/q to quit): ").strip().lower()
            if response in ['n', 'q', 'quit']:
                break

def view_chunk_summary():
    """Show a summary of all chunks"""
    print("📋 Chunk Summary")
    print("=" * 50)
    
    # Initialize RAG system
    rag_system = SimpleRAGSystem()
    
    # Process the document
    if not rag_system.process_document():
        print("❌ Failed to process document.")
        return
    
    print(f"\n📊 Total chunks: {len(rag_system.chunks)}")
    print("=" * 50)
    
    # Show summary of each chunk
    for i, chunk in enumerate(rag_system.chunks):
        print(f"\n📄 Chunk {i+1}:")
        print(f"   Length: {len(chunk)} characters")
        print(f"   Preview: {chunk[:100]}...")
        print(f"   Contains: {chunk.count('Einstein')} mentions of 'Einstein'")
        print(f"   Contains: {chunk.count('Albert')} mentions of 'Albert'")

def search_chunks():
    """Search for specific content in chunks"""
    print("🔍 Search Chunks")
    print("=" * 50)
    
    # Initialize RAG system
    rag_system = SimpleRAGSystem()
    
    # Process the document
    if not rag_system.process_document():
        print("❌ Failed to process document.")
        return
    
    while True:
        search_term = input("\n🔍 Enter search term (or 'quit' to exit): ").strip()
        
        if search_term.lower() in ['quit', 'q', 'exit']:
            break
        
        if not search_term:
            continue
        
        print(f"\n🔍 Searching for: '{search_term}'")
        print("-" * 40)
        
        found = False
        for i, chunk in enumerate(rag_system.chunks):
            if search_term.lower() in chunk.lower():
                found = True
                print(f"\n📄 Found in Chunk {i+1}:")
                print(f"   Length: {len(chunk)} characters")
                print(f"   Preview: {chunk[:200]}...")
                print("-" * 30)
        
        if not found:
            print(f"❌ '{search_term}' not found in any chunk")

if __name__ == "__main__":
    print("🔍 Chunk Viewer for Einstein RAG System")
    print("=" * 50)
    print("Choose an option:")
    print("1. View all chunks (full content)")
    print("2. View chunk summary")
    print("3. Search chunks")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            view_chunks()
        elif choice == "2":
            view_chunk_summary()
        elif choice == "3":
            search_chunks()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.") 