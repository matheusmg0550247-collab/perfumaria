import streamlit as st
import os

# --- Configuração Simples ---
st.set_page_config(page_title="Teste de Imagens", layout="centered")

st.title("🕵️‍♂️ Modo de Teste: Imagens Diretas")
st.write("Este modo remove todo o design para testar se o Streamlit consegue ler os arquivos na pasta.")
st.divider()

# --- DADOS DOS PRODUTOS (A mesma lista que estávamos usando) ---
produtos = [
    {
        "nome": "Royal Elixir Gold",
        "imagem": "imagens/Perfume1.png", 
    },
    {
        "nome": "Black Orchid Intense",
        "imagem": "imagens/Perfume2.png", 
    },
    {
        "nome": "Velvet Santal Wood",
        "imagem": "imagens/Perfume3.png", 
    },
    {
        # ESTE ERA O QUE ESTAVA QUEBRADO NO SEU PRINT
        "nome": "Imperial Amber",
        "imagem": "imagens/Perfume4.png", 
    },
]

# --- LOOP DE TESTE ---
# Vamos passar por cada produto e tentar mostrar a imagem sem truques de CSS
for p in produtos:
    st.header(f"Testando: {p['nome']}")
    
    caminho_arquivo = p['imagem']
    st.write(f"📂 Caminho definido no código: `{caminho_arquivo}`")

    # 1. Verifica se o arquivo existe no sistema
    if os.path.exists(caminho_arquivo):
        st.success("✅ OK: O Python encontrou o arquivo.")
        
        # 2. Tenta mostrar a imagem usando o comando nativo do Streamlit
        try:
            st.image(caminho_arquivo, width=300, caption=p['nome'])
        except Exception as e:
            st.error(f"❌ O arquivo existe, mas o Streamlit não conseguiu abrir. Erro: {e}")
            
    else:
        st.error("❌ ERRO FATAL: Arquivo NÃO encontrado.")
        st.warning("Dica: Verifique letras maiúsculas/minúsculas. 'Perfume4.png' é diferente de 'perfume4.png'.")
        
        # Mostra o que tem na pasta para ajudar
        try:
            pasta = os.path.dirname(caminho_arquivo)
            conteudo = os.listdir(pasta)
            st.info(f"Conteúdo real da pasta '{pasta}': {conteudo}")
        except:
            st.error("Nem a pasta 'imagens' foi encontrada.")

    st.divider()
