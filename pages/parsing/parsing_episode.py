import logging

import streamlit as st
import asyncio
import json
from src.services.parsers.episode import FactParser
from src.services.llm.helper import get_langchain_client
from src.schemas.llm.provider import Provider

st.set_page_config(
    page_title="Parsing Episode",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Parsing Episode")
st.markdown("---")

# Check if chunk_data exists in session state
if 'chunk_data' not in st.session_state or not st.session_state.chunk_data:
    st.warning("You need to parse pdf first")
    st.info("Please go to the Chunk Analysis page to upload and process a PDF file first.")
else:
    st.success(f"Found {len(st.session_state.chunk_data)} chunks ready for parsing")
    
    # Display chunk information
    st.header("Available Chunks")
    
    # Show chunk summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Chunks", len(st.session_state.chunk_data))
    with col2:
        total_chars = sum(chunk['length'] for chunk in st.session_state.chunk_data)
        st.metric("Total Characters", total_chars)
    with col3:
        avg_length = total_chars / len(st.session_state.chunk_data)
        st.metric("Average Chunk Length", f"{avg_length:.0f}")
    
    # Chunk selection
    st.subheader("Select Chunks to Parse")
    
    # Add option to select all or individual chunks
    select_all = st.checkbox("Select All Chunks", value=True)
    
    if select_all:
        selected_chunks = list(range(len(st.session_state.chunk_data)))
    else:
        selected_chunks = st.multiselect(
            "Choose chunks to parse:",
            options=list(range(len(st.session_state.chunk_data))),
            format_func=lambda x: f"Chunk {x+1} ({st.session_state.chunk_data[x]['length']} chars)",
            default=list(range(len(st.session_state.chunk_data)))
        )
    
    if selected_chunks:
        st.info(f"Selected {len(selected_chunks)} chunks for parsing")
        
        # Show preview of selected chunks
        with st.expander("Preview Selected Chunks"):
            for chunk_idx in selected_chunks[:3]:  # Show first 3
                chunk = st.session_state.chunk_data[chunk_idx]
                st.write(f"**Chunk {chunk_idx + 1}:**")
                st.text_area(f"Content", chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text'], 
                           height=100, key=f"preview_{chunk_idx}")
            if len(selected_chunks) > 3:
                st.info(f"... and {len(selected_chunks) - 3} more chunks")
    
    # LLM Configuration
    st.header("LLM Configuration")
    
    # Load LLM config
    try:
        from src.utils.config_loader import TomlConfigLoader
        config_loader = TomlConfigLoader()
        llm_config = config_loader.get_llm_config()
        # Default provider
        default_provider = llm_config.get("default").get("provider")

        # Provider selection
        provider_options = [Provider.OPENAI, Provider.ANTHROPIC, Provider.GEMINI, Provider.GROQ]
        provider_names = [p.value.capitalize() for p in provider_options]

        # Define index
        index = provider_names.index(str(default_provider).capitalize())
        col1, col2 = st.columns(2)
        with col1:
            selected_provider_name = st.selectbox("Select LLM Provider:", provider_names, index = index)
            selected_provider = provider_options[provider_names.index(selected_provider_name)]
        
        with col2:
            # Get available models for selected provider
            provider_key = selected_provider.value.lower()
            provider_config = llm_config.get("llm_providers", {}).get(provider_key, {})
            available_models = provider_config.get("available_models", [provider_config.get("default_model", "gpt-3.5-turbo")])
            
            selected_model = st.selectbox("Select Model:", available_models)
        
        # Parse button
        if st.button("🚀 Parse Selected Chunks", type="primary"):
            with st.spinner("Initializing LLM and parsing chunks..."):
                try:
                    # Get LLM client
                    llm = get_langchain_client(selected_provider, model=selected_model)
                    
                    # Parse each selected chunk
                    all_results = []
                    
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    # logging.error(f"Length: {len(st.session_state.chunk_data)}")
                    # logging.error(f"Length: {st.session_state.chunk_data}")

                    chunks = [chunk.get("text") for chunk in st.session_state.chunk_data]

                    results = asyncio.run(FactParser.parse(llm = llm,
                                                           contents = chunks))
                    
                    # Store results in session state
                    st.session_state.parsing_results = results
                    
                    st.success(f"Successfully parsed {len(chunks)} chunks!")
                    
                except Exception as e:
                    st.error(f"Error during parsing: {str(e)}")
                    st.exception(e)
    except Exception as e:
        pass
    # Display results if available
    if 'parsing_results' in st.session_state and st.session_state.parsing_results:
        st.markdown("---")
        st.header("Parsing Results")

        results = st.session_state.parsing_results
        
        # Prepare data for data editor
        editor_data = []
        for chunk_idx, semantic_facts in enumerate(results):
            if semantic_facts and semantic_facts.data:
                for fact in semantic_facts.data:
                    editor_data.append({
                        'index': len(editor_data) + 1,
                        'content': fact.content,
                        'description': fact.description,
                        'chunk_index': chunk_idx + 1
                    })
        
        if editor_data:
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Facts Extracted", len(editor_data))
            with col2:
                chunks_with_facts = len([r for r in results if r and r.data])
                st.metric("Chunks with Facts", chunks_with_facts)
            with col3:
                avg_facts = len(editor_data) / len(results) if results else 0
                st.metric("Average Facts per Chunk", f"{avg_facts:.1f}")
            
            # Display data editor
            st.subheader("Extracted Facts")
            edited_data = st.data_editor(
                editor_data,
                column_config={
                    "index": st.column_config.NumberColumn("Index", width="small"),
                    "content": st.column_config.TextColumn("Content", width="large"),
                    "description": st.column_config.TextColumn("Description", width="large"),
                    "chunk_index": st.column_config.NumberColumn("Chunk Index", width="small")
                },
                hide_index=True,
                width="stretch",
                num_rows="dynamic"
            )
            
            logging.error(edited_data)
        else:
            st.warning("No facts were extracted from the chunks.")
    else:
        # Navigation help
        st.markdown("---")
        st.header("Next Steps")
        st.markdown("""
        To use this page:
        1. Navigate to the **Chunk Analysis** page using the sidebar
        2. Upload a PDF file and process it to generate chunks
        3. Return to this **Parsing Episode** page to extract facts from the chunks
        """)
