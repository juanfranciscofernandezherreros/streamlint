import streamlit as st
from rag_system import query_rag, get_retriever_info

st.set_page_config(page_title="Asistente Legal RAG", page_icon="⚖️", layout="wide")

st.title("⚖️ Sistema RAG - Asistente Legal")
st.divider()

# 1. Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Sidebar
with st.sidebar:
    st.header("📋 Info")
    try:
        info = get_retriever_info()
        st.info(f"**Retriever:** {info['tipo']}")
    except:
        st.warning("Retriever no inicializado.")
        
    if st.button("🗑️ Limpiar Historial", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 3. LÓGICA DE PROCESAMIENTO (Antes de dibujar las columnas) ---
if prompt := st.chat_input("Consulta legal..."):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generar respuesta
    # Nota: No dibujamos aquí, solo procesamos datos
    with st.spinner("Consultando jurisprudencia..."):
        response, docs = query_rag(prompt)
        # Guardar respuesta del asistente con sus documentos
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response, 
            "docs": docs
        })
    # Forzamos rerun para que las columnas lean el nuevo session_state desde el inicio
    st.rerun()

# --- 4. RENDERIZADO DE INTERFAZ ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat")
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

with col2:
    st.subheader("📄 Fuentes")
    # Buscamos el último mensaje que sea del asistente Y tenga documentos
    last_assistant_msg = next(
        (m for m in reversed(st.session_state.messages) 
         if m["role"] == "assistant" and "docs" in m), 
        None
    )

    if last_assistant_msg:
        # Verificamos si hay documentos en la lista
        if not last_assistant_msg["docs"]:
            st.write("No se encontraron fragmentos relevantes para esta consulta.")
        else:
            for doc in last_assistant_msg["docs"]:
                # Usamos el fragmento y la fuente para el título del expander
                with st.expander(f"📍 Doc {doc['fragmento']} - {doc['fuente']}"):
                    st.caption(f"**Página:** {doc['pagina']}")
                    st.markdown("---")
                    st.text(doc['contenido'])
    else:
        st.info("Haz una consulta para ver las fuentes relacionadas.")