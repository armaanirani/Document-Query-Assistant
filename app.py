import streamlit as st
import os
import json
import hashlib
from datetime import datetime

import PyPDF2
from llama_index.core import Settings, Document, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

class DocumentQueryApp:
    def __init__(self):
        # Constants
        self.PERSIST_DIR = "./storage"
        self.DOCUMENTS_META_FILE = os.path.join(self.PERSIST_DIR, "documents_meta.json")
        self.QUERY_HISTORY_FILE = os.path.join(self.PERSIST_DIR, "query_history.json")
        
        # Ensure storage directory exists
        os.makedirs(self.PERSIST_DIR, exist_ok=True)
        
        # Initialize session state
        self._initialize_session_state()
        
        # Load existing document registry
        self._load_document_registry()
        self._load_query_history()
    
    def _initialize_session_state(self):
        """Initialize session state variables."""
        if "api_key" not in st.session_state:
            st.session_state.api_key = None
        
        if "documents_registry" not in st.session_state:
            st.session_state.documents_registry = {}
        
        if "query_history" not in st.session_state:
            st.session_state.query_history = []
        
        # OpenAI Model Selection
        if "selected_model" not in st.session_state:
            st.session_state.selected_model = "gpt-4o-mini"

    def _load_query_history(self):
        """Load query history from JSON file."""
        try:
            if os.path.exists(self.QUERY_HISTORY_FILE):
                with open(self.QUERY_HISTORY_FILE, 'r') as f:
                    loaded_history = json.load(f)
                    st.session_state.query_history = loaded_history
        except Exception as e:
            st.error(f"Error loading query history: {e}")
            st.session_state.query_history = []
    
    def _save_query_history(self):
        """Save query history to JSON file."""
        try:
            with open(self.QUERY_HISTORY_FILE, 'w') as f:
                json.dump(st.session_state.query_history, f, indent=4)
        except Exception as e:
            st.error(f"Error saving query history: {e}")
    
    def _load_document_registry(self):
        """Load document registry from JSON file."""
        try:
            if os.path.exists(self.DOCUMENTS_META_FILE):
                with open(self.DOCUMENTS_META_FILE, 'r') as f:
                    st.session_state.documents_registry = json.load(f)
        except Exception as e:
            st.error(f"Error loading document registry: {e}")
            st.session_state.documents_registry = {}
    
    def _save_document_registry(self):
        """Save document registry to JSON file."""
        try:
            with open(self.DOCUMENTS_META_FILE, 'w') as f:
                json.dump(st.session_state.documents_registry, f, indent=4)
        except Exception as e:
            st.error(f"Error saving document registry: {e}")
    
    def _generate_file_hash(self, file_content: bytes) -> str:
        """Generate a unique hash for a file."""
        return hashlib.md5(file_content).hexdigest()
    
    def _extract_pdf_text(self, pdf_file):
        """Extract text from PDF file."""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            st.error(f"Error extracting PDF text: {e}")
            return None
    
    def load_index(self):
        """Load or create vector store index."""
        storage_context = StorageContext.from_defaults(persist_dir=self.PERSIST_DIR)
        return load_index_from_storage(storage_context)
    
    def configure_settings(self, api_key: str):
        """Configure OpenAI settings with model selection."""
        Settings.llm = OpenAI(api_key=api_key, model=st.session_state.selected_model)
        Settings.embed_model = OpenAIEmbedding(api_key=api_key)
    
    def render_model_configuration(self):
        """Render model configuration."""
        
        # Model Selection
        st.subheader("Model Selection")
        available_models = [
            "gpt-4o-mini", 
            "gpt-4o", 
            "gpt-3.5-turbo", 
            "gpt-4-turbo"
        ]
        
        selected_model = st.selectbox(
            "Choose OpenAI Model", 
            available_models, 
            index=available_models.index(st.session_state.selected_model)
        )
        
        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
            self.configure_settings(st.session_state.api_key)
            st.rerun()

    def render_api_key_section(self):
        """Render API key input section."""
        if st.session_state.api_key is None:
            st.header("Set Your OpenAI API Key")
            api_key_input = st.text_input("Enter your OpenAI API key", type="password")
            
            if st.button("Set API Key"):
                st.session_state.api_key = api_key_input
                self.configure_settings(api_key_input)
                st.rerun()
        else:
            self.configure_settings(st.session_state.api_key)

    def render_history_section(self):
        """Render query history section with clearing and individual deletion options."""
        st.header("Query History")
        
        if st.session_state.query_history:
            # Display history with delete option
            for idx, entry in enumerate(reversed(st.session_state.query_history), 1):
                col1, col2 = st.columns([0.95, 0.05])
                
                with col1:
                    st.markdown(f"**Query {len(st.session_state.query_history) - idx + 1}:**")
                    st.write(f"Question: {entry['question']}")
                    st.write(f"Timestamp: {entry['timestamp']}")
                    with st.expander("View Response"):
                        st.markdown(entry['response'])
                
                with col2:
                    # Delete button with bin icon
                    if st.button(f"🗑️", key=f"delete_history_{idx}"):
                        del st.session_state.query_history[len(st.session_state.query_history) - idx]
                        self._save_query_history()
                        st.rerun()
                
                st.markdown("---")
            
            # Clear all history button
            if st.button("Clear All History", type="primary"):
                st.session_state.query_history = []
                self._save_query_history()
                st.success("Query history has been cleared.")
                st.rerun()
        else:
            st.write("No query history available.")
    
    def render_question_section(self, index):
        """Render question input and processing section."""
        
        # Check if documents exist
        if not st.session_state.documents_registry:
            st.warning("Please upload a document to start asking questions.")
            return
    
        st.subheader("Ask a Question")
        if prompt := st.chat_input("Enter your question here"):
            with st.spinner("Generating answer..."):
                query_engine = index.as_query_engine()
                response = query_engine.query(prompt)
                
                # Track detailed query history
                query_entry = {
                    'question': prompt,
                    'response': response.response,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.query_history.append(query_entry)
                
                # Limit history to last 50 entries
                if len(st.session_state.query_history) > 50:
                    st.session_state.query_history = st.session_state.query_history[-50:]
                
                # Save query history
                self._save_query_history()
                
                # Display response
                st.markdown("**Your Question:**")
                st.write(prompt)
                st.markdown("**Answer:**")
                st.markdown(response.response)
                
                # Display sources
                if response.source_nodes:
                    st.markdown("**Sources:**")
                    for node in response.source_nodes:
                        st.write(f"- {node.node.get_text()[:200]}...")
    
    def remove_document(self, index, filename: str):
        """Remove a specific document from the index and registry."""
        try:
            # Remove from document registry
            if filename in st.session_state.documents_registry:
                del st.session_state.documents_registry[filename]
                self._save_document_registry()
            
            # Rebuild the index without the removed document
            new_docs = [
                Document(text=doc.get_text(), metadata=doc.metadata) 
                for doc in index.docstore.docs.values() 
                if doc.metadata.get('filename') != filename
            ]
            
            # Create a new index
            new_index = VectorStoreIndex.from_documents(new_docs)
            new_index.storage_context.persist(persist_dir=self.PERSIST_DIR)
            
            st.success(f"Document '{filename}' removed successfully.")
            return new_index
        except Exception as e:
            st.error(f"Error removing document: {e}")
            return index

    def remove_all_documents(self, index):
        """Remove all documents from the index and registry."""
        try:
            # Clear document registry
            st.session_state.documents_registry.clear()
            self._save_document_registry()
            
            # Create an empty index
            new_index = VectorStoreIndex.from_documents([])
            new_index.storage_context.persist(persist_dir=self.PERSIST_DIR)
            
            st.success("All documents have been removed.")
            return new_index
        except Exception as e:
            st.error(f"Error removing all documents: {e}")
            return index
    
    def render_document_management(self, index):
        """Render document upload and management section."""
        
        # File uploader with unique key to reset
        st.subheader("Upload New Documents")
        uploaded_files = st.file_uploader(
            "Upload documents", 
            accept_multiple_files=True, 
            type=["txt", "pdf"],
            key=f"document_uploader_{len(st.session_state.documents_registry)}"
        )
        
        if uploaded_files and st.button("Upload Document"):
            # Track duplicate files
            duplicate_files = []
            new_files_to_process = []
            
            with st.spinner("Processing documents..."):
                for uploaded_file in uploaded_files:
                    # Read file content
                    file_content = uploaded_file.getvalue()
                    file_hash = self._generate_file_hash(file_content)
                    
                    # Check for duplicates
                    is_duplicate = any(
                        doc_info.get('hash') == file_hash 
                        for doc_info in st.session_state.documents_registry.values()
                    )
                    
                    if is_duplicate:
                        duplicate_files.append(uploaded_file.name)
                    else:
                        new_files_to_process.append((uploaded_file, file_content, file_hash))
                
                # Show warning for duplicate files
                if duplicate_files:
                    st.warning("Duplicate files detected:")
                    for dup_file in duplicate_files:
                        st.write(f"- {dup_file}")
                
                # Process new files
                for uploaded_file, file_content, file_hash in new_files_to_process:
                    try:
                        # Text extraction based on file type
                        if uploaded_file.type == "application/pdf":
                            text = self._extract_pdf_text(uploaded_file)
                        elif uploaded_file.type == "text/plain":
                            text = file_content.decode("utf-8")
                        else:
                            st.warning(f"Unsupported file type: {uploaded_file.type}")
                            continue
                        
                        if text:
                            doc = Document(text=text, metadata={"filename": uploaded_file.name})
                            index.insert(doc)
                            
                            # Update documents registry
                            st.session_state.documents_registry[uploaded_file.name] = {
                                "type": uploaded_file.type,
                                "size": len(file_content),
                                "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "hash": file_hash
                            }
                    
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                
                # Save document registry and persist index
                self._save_document_registry()
                index.storage_context.persist(persist_dir=self.PERSIST_DIR)
                
                st.success("Index updated successfully!")
                st.rerun()
        
        # Current documents display
        st.subheader("Uploaded Documents")
        
        if st.session_state.documents_registry:
            # Create a DataFrame-like table for documents
            doc_data = []
            for filename, doc_info in st.session_state.documents_registry.items():
                doc_data.append({
                    "Filename": filename,
                    "Date Added": doc_info.get('date_added', 'Unknown'),
                    "Size (KB)": f"{doc_info.get('size', 0) / 1024:.2f}",
                    "Type": doc_info.get('type', 'Unknown')
                })
            
            # Display table
            st.table(doc_data)
            
            # Document removal section
            col1, col2 = st.columns(2)
            
            with col1:
                doc_to_remove = st.selectbox(
                    "Select a document to remove", 
                    list(st.session_state.documents_registry.keys())
                )
                
                if st.button("Remove Selected Document"):
                    index = self.remove_document(index, doc_to_remove)
                    st.rerun()
            
            with col2:
                if st.button("Remove All Documents", type="primary"):
                    index = self.remove_all_documents(index)
                    st.rerun()
        else:
            st.write("No documents uploaded yet.")
    
    def run(self):
        """Main application runner."""
        st.title("📚 Document Query Assistant")
        
        # Render API key section if not set
        if not st.session_state.api_key:
            self.render_api_key_section()
        
        if st.session_state.api_key:
            # Load index first
            index = self.load_index()
            
            # Display current model at the top of the screen
            st.info(f"Current Model: {st.session_state.selected_model}")
            
            # Organize layout
            tab1, tab2, tab3, tab4 = st.tabs([
                "Query Documents", 
                "Manage Documents", 
                "Model Configuration",
                "Query History"
            ])
            
            with tab1:
                self.render_question_section(index)
            
            with tab2:
                self.render_document_management(index)
            
            with tab3:
                self.render_model_configuration()
            
            with tab4:
                self.render_history_section()

def main():
    app = DocumentQueryApp()
    app.run()

if __name__ == "__main__":
    main()