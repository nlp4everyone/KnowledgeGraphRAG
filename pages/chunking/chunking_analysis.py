# Streamlit
import streamlit as st
# Chunking
from src.services.chunkers.chonkie_chunker import ChonkieChunkingService
from src.schemas.chunking.chunking_config import ChonkieChunkingConfig
# Plotly
import plotly.express as px
# Dependencies
from io import StringIO
import asyncio, tempfile, os
# Loader
from src.utils.config_loader import TomlConfigLoader

# Define config loader
config_loader = TomlConfigLoader()
# Load chunking config
chunking_config = config_loader.get_chunking_config()
# Load pdf parser config
pdfparser_config = config_loader.get_pdfparser_config()

def get_pdf_parser():
    if 'pdf_parser' not in st.session_state:
        try:
            from src.services.parsers.pdf import LlamaParseParser
            return LlamaParseParser(num_worker = int(pdfparser_config.get("llamaparse").get("num_workers")),
                                    verbose = bool(pdfparser_config.get("llamaparse").get("verbose")))
        except ValueError as e:
            st.error("Please ensure LLAMAPARSE_API_KEY is set in your .env file")
            return None
        except Exception as e:
            st.error(f"Failed to initialize PDF parser: {str(e)}")
            return None
    return None

st.set_page_config(
    page_title="Chunk Analysis",
    page_icon="📄",
    layout="wide"
)

st.title("Chunk Analysis")
st.markdown("---")

# File upload section
st.header("Upload File")
uploaded_file = st.file_uploader(
    "Choose a file",
    type=['txt', 'pdf'],
    help="Upload your file for parsing",
    max_upload_size=50,
    accept_multiple_files =False
)

# Process uploaded file
if uploaded_file is not None:
    st.success(f"File uploaded successfully: {uploaded_file.name}")
    
    # Initialize session state for storing parsed content
    if 'text_content' not in st.session_state:
        st.session_state.text_content = None
        st.session_state.file_processed = False
    
    # Read file content based on type (only once)
    if not st.session_state.file_processed:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        try:
            if file_extension == 'txt':  # txt, md
                stringio = StringIO(uploaded_file.read().decode("utf-8"))
                st.session_state.text_content = stringio.read()
                st.session_state.file_processed = True
                
            elif file_extension == 'pdf':
                # Handle PDF with temporary file
                temp_file_path = None
                try:
                    # Create temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                        temp_file.write(uploaded_file.read())
                        temp_file_path = temp_file.name
                    
                    # Parse PDF using asyncio with spinner
                    with st.spinner("Parsing PDF file...", show_time=True):
                        pdf_parser = get_pdf_parser()
                        if pdf_parser is not None:
                            content, documents = asyncio.run(pdf_parser.parse(file_input=temp_file_path, lazy_load=False))
                            st.session_state.text_content = content
                            st.session_state.file_processed = True
                    
                except Exception as e:
                    st.error(f"Error processing PDF file: {str(e)}")
                    st.session_state.text_content = ""
                    st.session_state.file_processed = True
                    
                finally:
                    # Clean up temporary file
                    if temp_file_path and os.path.exists(temp_file_path):
                        try:
                            os.unlink(temp_file_path)
                        except OSError as e:
                            st.warning(f"Could not delete temporary file: {e}")
            else:
                st.error(f"Unsupported file type: {file_extension}")
                st.session_state.text_content = ""
                st.session_state.file_processed = True
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.session_state.text_content = ""
            st.session_state.file_processed = True

    # Show file preview if content is available
    if st.session_state.text_content is not None:
        # Debug: Show content length
        st.info(f"Content loaded: {len(st.session_state.text_content)} characters")
        
        # Only show preview and chunk config if there's actual content
        if len(st.session_state.text_content) > 0:
            st.subheader("File Preview")
            st.text_area("Content", st.session_state.text_content[:1000] + "..." if len(st.session_state.text_content) > 1000 else st.session_state.text_content, height=200)
            
            # Chunk configuration section
            st.header("Chunk Configuration")
            col1, col2 = st.columns(2)

            with col1:
                chunk_size = st.slider("Chunk Size",
                                       min_value = chunking_config.get("chunking").get("min_chunk_size"),
                                       max_value = chunking_config.get("chunking").get("max_chunk_size"),
                                       value = chunking_config.get("chunking").get("default_chunk_size"),
                                       step = chunking_config.get("chunking").get("chunk_size_step"),
                                       help = "Size of each chunk in characters")

            with col2:
                chunk_overlap = st.slider("Chunk Overlap",
                                          min_value = chunking_config.get("chunking").get("min_chunk_overlap"),
                                          max_value = chunking_config.get("chunking").get("max_chunk_overlap"),
                                          value = chunking_config.get("chunking").get("default_chunk_overlap"),
                                          step = chunking_config.get("chunking").get("chunk_overlap_step"),
                                          help="Overlap between chunks in characters")

            # Display configuration
            st.info(f"Current configuration: Chunk Size = {chunk_size}, Chunk Overlap = {chunk_overlap}")
            
            # Chunking simulation (only when button is pressed)
            if st.button("Process Chunks"):
                # Validate that text_content is not empty
                if st.session_state.text_content is None or len(st.session_state.text_content) == 0:
                    st.error("Cannot process chunks: No text content available.")
                    st.stop()

                # Import chunking service
                chunker_service = ChonkieChunkingService(config=ChonkieChunkingConfig(chunk_size = chunk_size,
                                                                                      chunk_overlap = chunk_overlap,
                                                                                      min_characters_per_chunk = chunking_config.get("chonkie").get("min_characters_per_chunk"),
                                                                                      min_sentences_per_chunk = chunking_config.get("chonkie").get("min_sentences_per_chunk"),
                                                                                      tokenizer = chunking_config.get("chonkie").get("tokenizer")))
                
                # Chunking
                chunk_texts = chunker_service.split_text(st.session_state.text_content)

                # Store chunk data in session state for analysis
                chunk_data = []
                for i, text in enumerate(chunk_texts, 1):
                    chunk_data.append({
                        'chunk_id': i,
                        'text': text,
                        'length': len(text),
                        'preview': text[:50] + "..." if len(text) > 50 else text
                    })
                st.session_state.chunk_data = chunk_data
                
                st.subheader(f"Generated Chunks ({len(chunk_texts)} total)")
                
                for i, chunk in enumerate(chunk_texts[:5]):  # Show first 5 chunks
                    with st.expander(f"Chunk {i+1} (Length: {len(chunk)})"):
                        st.text_area(f"Chunk {i+1} Content", chunk, height=150, key=f"chunk_{i}")
                
                if len(chunk_texts) > 5:
                    st.info(f"Showing first 5 of {len(chunk_texts)} chunks")
                
                # Chunk Analysis Section
                st.markdown("---")
                st.header("Chunk Analysis Dashboard")
                
                # Metrics section
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Chunks", len(chunk_data))
                
                with col2:
                    avg_length = sum([chunk['length'] for chunk in chunk_data]) / len(chunk_data)
                    st.metric("Average Length", f"{avg_length:.0f}")
                
                with col3:
                    max_length = max([chunk['length'] for chunk in chunk_data])
                    st.metric("Max Length", max_length)
                
                with col4:
                    min_length = min([chunk['length'] for chunk in chunk_data])
                    st.metric("Min Length", min_length)
                
                # Visualization section
                st.subheader("Visualizations")
                
                # Chunk length distribution
                col1, col2 = st.columns(2)
                with col1:
                    fig1 = px.histogram(
                        chunk_data,
                        x='length',
                        nbins=20,
                        title="Chunk Length Distribution"
                    )
                    fig1.update_layout(height=400)
                    st.plotly_chart(fig1, width='stretch')
                
                with col2:
                    fig2 = px.scatter(
                        chunk_data,
                        x='chunk_id',
                        y='length',
                        title="Chunk Length by Position",
                        labels={'chunk_id': 'Chunk Number', 'length': 'Length (characters)'}
                    )
                    fig2.update_layout(height=400)
                    st.plotly_chart(fig2, width='stretch')
        else:
            st.warning("No content found in the uploaded file. Please try uploading a different file.")
else:
    st.info("Please upload a file to begin processing.")
    # Clear session state when no file is uploaded
    if 'text_content' in st.session_state:
        del st.session_state.text_content
    if 'file_processed' in st.session_state:
        del st.session_state.file_processed

