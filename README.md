# KnowledgeGraphRAG Demo with Graphiti

A Streamlit-based web application for text parsing and chunk analysis, demonstrating advanced document processing capabilities with interactive visualizations.

## 🚀 Features

- **Multi-format Support**: Process both text (.txt, .md) and PDF files
- **Advanced PDF Parsing**: Integrated with LlamaParse for high-quality PDF extraction
- **Intelligent Chunking**: Configurable text chunking with adjustable size and overlap parameters
- **Interactive Analytics**: Real-time visualization of chunk statistics and distributions
- **Modern UI**: Clean, responsive interface built with Streamlit

## 📋 Pages

### 🏠 Homepage
- Welcome screen with project overview
- Navigation to available features

### 📊 Chunk Analysis
- File upload interface for text and PDF documents
- Configurable chunking parameters (size: 256-5048 chars, overlap: 0-512 chars)
- Real-time chunk processing with progress indicators
- Interactive dashboard with:
  - Chunk metrics (total count, average/max/min length)
  - Length distribution histogram
  - Position-based scatter plot
  - Expandable chunk previews

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Text Processing**: 
  - Chonkie (chunking)
  - LlamaParse (PDF parsing)
- **Visualization**: Plotly
- **Data Processing**: Pandas

## 📦 Installation
### Docker Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/nlp4everyone/KnowledgeGraphRAG.git
   cd KnowledgeGraphRAG
   ```

2. **Set up environment variables**
   ```bash
   cp .env.sample .env
   ```
   Edit `.env` and add your LlamaParse API key:
   ```
   LLAMAPARSE_API_KEY=your_api_key_here
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker compose up --build
   ```

4. **Access the application**
   Open `http://localhost:8501` in your browser


## 🔧 Configuration
### Chunking Parameters
- **Chunk Size**: 256-5048 characters (default: 1024)
- **Chunk Overlap**: 0-512 characters (default: 128)

## 📁 Project Structure

```
KnowledgeGraphRAG/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── docker-compose.yml             # Docker configuration
├── Dockerfile                     # Docker image definition
├── .env.sample                    # Environment variables template
├── pages/                         # Streamlit pages
│   ├── home/
│   │   └── home_page.py          # Homepage component
│   └── chunking/
│       └── chunking_analysis.py  # Chunk analysis interface
└── src/                          # Source code
    ├── core/
    │   └── config.py             # Application configuration
    ├── schemas/
    │   └── chunking/             # Data models for chunking
    └── services/
        ├── chunkers/
        │   └── chonkie_chunker.py # Text chunking service
        └── parsers/
            ├── base.py           # Base parser interface
            └── pdf/
                ├── llamaparse_parser.py    # LlamaParse implementation
                └── undatasio_parser.py    # Alternative PDF parser
```

## 🚀 Usage

1. **Upload a File**: Use the file uploader to select a text (.txt, .md) or PDF file
2. **Configure Chunking**: Adjust chunk size and overlap parameters using the sliders
3. **Process Chunks**: Click "Process Chunks" to analyze the document
4. **View Results**: Explore the interactive dashboard with chunk statistics and visualizations

## 🆘 Troubleshooting

### Common Issues

1. **LlamaParse API Key Error**
   - Ensure your `.env` file contains a valid `LLAMAPARSE_API_KEY`
   - Verify your API key is active and has sufficient credits

2. **PDF Processing Fails**
   - Check that the PDF file is not corrupted
   - Ensure the file size is within reasonable limits (< 50MB recommended)

