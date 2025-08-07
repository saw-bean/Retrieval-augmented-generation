# Einstein RAG System

A simple yet robust Retrieval-Augmented Generation (RAG) system for answering questions about Albert Einstein using his biography PDF.

## 🚀 Quick Start

### Option 1: Automatic Installation
```bash
# Make the install script executable
chmod +x install.sh

# Run the installation script
./install.sh
```

### Option 2: Manual Installation
```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Set up configuration
cp config_template.py config.py
# Edit config.py and add your Mistral API key

# 3. Run the system
python3 simple_rag_einstein.py
```

## 📋 What the System Does

1. **Extracts text** from the Albert Einstein biography PDF
2. **Chunks the text** into manageable pieces
3. **Performs keyword-based search** with synonym expansion
4. **Retrieves relevant context** using simple similarity matching
5. **Answers questions** using AI-powered generation

## 🎯 Features

- ✅ **Simple Python script** - No complex setup required
- ✅ **PDF processing** - Automatically extracts and processes PDF content
- ✅ **Keyword-based search** - Efficient retrieval using word matching and synonyms
- ✅ **AI-powered answers** - Uses Mistral Large for intelligent responses
- ✅ **Interactive mode** - Ask questions in real-time
- ✅ **Batch processing** - Test multiple questions at once
- ✅ **Results export** - Saves answers to JSON files

## 📁 Files

- `simple_rag_einstein.py` - Main RAG system
- `config.py` - Configuration file with API keys (create from template)
- `config_template.py` - Template for configuration
- `requirements.txt` - Python dependencies
- `Albert-Einstein-Biography.pdf` - Source document
- `view_chunks.py` - Utility to view and search document chunks
- `einstein_simple_rag_results_*.json` - Results files (created automatically)

## 🔧 Configuration

The system uses these default settings (easily modifiable in the code):

- **Chunk size**: 1000 characters
- **Chunk overlap**: 200 characters
- **Top-k retrieval**: 3 documents
- **LLM**: Mistral Large (via Mistral AI API)

## 💡 Usage Examples

### Run the complete system:
```bash
python simple_rag_einstein.py
```

### Sample questions the system can answer:
- "When was Albert Einstein born?"
- "What is Einstein's most famous equation?"
- "Where did Einstein work during his career?"
- "What was Einstein's contribution to physics?"
- "When did Einstein die?"

## 🎮 Interactive Mode

After running the script, you'll enter interactive mode where you can:
- Ask any question about Einstein
- See AI-generated answers
- View the source context used
- Type 'quit' to exit

## 📊 Output

The system provides:
- Real-time question answering
- JSON export of all results
- Context retrieval information
- Performance feedback

## 🔍 How It Works

1. **Document Processing**: PDF → Text → Chunks
2. **Keyword Search**: Question → Word matching with synonyms
3. **Retrieval**: Question → Relevant chunks based on word overlap
4. **Generation**: Context + Question → AI answer

## 🛠️ Troubleshooting

- **PDF not found**: Make sure `Albert-Einstein-Biography.pdf` is in the same directory
- **API errors**: Check your internet connection and API key in `config.py`
- **Config not found**: Copy `config_template.py` to `config.py` and add your API key
- **Memory issues**: Reduce chunk size in the configuration
- **Slow performance**: Processing time depends on PDF size and chunk settings

## 📈 Performance

- **Document processing**: ~5-15 seconds (depends on PDF size)
- **Question answering**: ~1-3 seconds per question
- **Memory usage**: Low (no vector database required)

## 🎉 Ready to Use!

The system is designed to be simple, robust, and educational. Just run the script and start asking questions about Albert Einstein! 