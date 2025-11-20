import streamlit as st
import base64
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Aurum Scents",
    page_icon="⚜️",
    layout="centered", # Voltamos para centered para manter a classe
    initial_sidebar_state="collapsed"
)

# --- 2. DADOS DOS PRODUTOS (MUITO IMPORTANTE: NOMES EXATOS) ---
# Baseado no seu print: Pasta 'imagens', 'Perfume X.png' (P maiúsculo, espaço)
produtos = [
    {
        "nome": "Royal Elixir Gold",
        "imagem": "imagens/Perfume 1.png", 
        "preco": 299.90
    },
    {
        "nome": "Black Orchid Intense",
        "imagem": "imagens/Perfume 2.png", 
        "preco": 350.00
    },
    {
        "nome": "Velvet Santal Wood",
        "imagem": "imagens/Perfume 3.png", 
        "preco": 420.00
    },
     {
        "nome": "Imperial Amber",
        "imagem": "imagens/Perfume 4.png", 
        "preco": 380.00
    },
     {
        "nome": "Golden Oud",
        "imagem": "imagens/Perfume 5.png", 
        "preco": 450.00
    }
]

# --- 3. FUNÇÕES E DEBUG ---
def get_img_as_base64(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode('utf-8').replace('\n', '')

# Navegação
if 'idx' not in st.session_state:
    st.session_state.idx = 0

def proximo():
    if st.session_state.idx < len(produtos) - 1:
        st.session_state.idx += 1
    else:
        st.session_state.idx = 0

def anterior():
    if st.session_state.idx > 0:
        st.session_state.idx -= 1
    else:
        st.session_state.idx = len(produtos) - 1

# --- 4. CARREGAMENTO (COM VERIFICAÇÃO) ---
visor_path = "imagens/Visor.jpg"
visor_b64 = get_img_as_base64(visor_path)

produto_atual = produtos[st.session_state.idx]
img_path_atual = produto_atual["imagem"]
img_produto_b64 = get_img_as_base64(img_path_atual)

preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + 100.00

# --- DEBUG VISUAL (Para ajudar a achar o erro da imagem) ---
# Se a imagem do perfume não carregar, mostra um aviso na barra lateral
if not img_produto_b64:
    with st.sidebar:
        st.error(f"❌ ERRO: Não encontrei '{img_path_atual}'")
        st.warning("Arquivos encontrados na pasta 'imagens':")
        try:
            arquivos = os.listdir("imagens")
            st.write(arquivos)
        except:
            st.error("A pasta 'imagens' não foi encontrada.")

# --- 5. CSS DE LUXO (Refinado) ---
bg_visor_css = f"url('data:image/jpg;base64,{visor_b64}')" if visor_b64 else "none"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

    /* Fundo Preto Absoluto */
    .stApp {{
        background-color: #000000;
        color: #d4af37;
    }}
    
    /* Ajuste do container principal para ser maior */
    .block-container {{
        max-width: 900px !important;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }}

    /* TÍTULO */
    .brand-header {{
        text-align: center;
        margin-bottom: 30px;
    }}
    .brand-title {{
        font-family: 'Cinzel', serif;
        font-size: 3.5rem;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: 2px;
    }}
    .brand-sub {{
        font-family: 'Playfair Display', serif;
        color: #666;
        letter-spacing: 4px;
        font-size: 0.8rem;
        text-transform: uppercase;
        margin-top: 5px;
    }}

    /* VISOR */
    .visor-wrapper {{
        position: relative;
        width: 100%;
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }}

    .visor-frame {{
        position: relative;
        width: 100%; 
        max-width: 650px; /* Tamanho ideal para não ficar pequeno */
        aspect-ratio: 16/9; /* Ajuste para cortar um pouco do teto/chão da foto e focar no quadro */
        background-image: {bg_visor_css};
        background-size: cover; /* Cover faz 'zoom' na imagem para preencher */
        background-position: center;
        border-radius: 5px;
        box-shadow: 0 0 50px rgba(0,0,0,0.8);
    }}

    /* PERFUME - POSICIONAMENTO ABSOLUTO */
    .perfume-overlay {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -43%); /* Ajuste fino vertical */
        height: 55%; /* O perfume ocupa 55% da altura do quadro */
        width: auto;
        filter: drop-shadow(0 10px 15px rgba(0,0,0,0.7));
        transition: all 0.5s ease-in-out;
        z-index: 10;
    }}
    
    .perfume-overlay:hover {{
        transform: translate(-50%, -45%) scale(1.05);
    }}

    /* BOTÕES (Integrados e Próximos) */
    div.stButton > button {{
        background: transparent;
        border: 1px solid #333;
        color: #888;
        font-family: 'Cinzel', serif;
        font-size: 1.2rem;
        padding: 0.5rem 1rem;
        width: 100%;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        border-color: #d4af37;
        color: #d4af37;
        background: rgba(212, 175, 55, 0.1);
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.2);
    }}

    /* INFORMAÇÕES DO PRODUTO */
    .info-container {{
        text-align: center;
        margin-top: 10px;
    }}
    .prod-name {{
        font-family: 'Cinzel', serif;
        font-size: 2rem;
        color: #fff;
        margin-bottom: 5px;
    }}
    .price-box {{
        font-family: 'Playfair Display', serif;
    }}
    .old {{ text-decoration: line-through; color: #555; font-size: 1.1rem; margin-right: 10px; }}
    .new {{ color: #d4af37; font-size: 2.5rem; font-weight: 700; }}

    /* WHATSAPP FLUTUANTE */
    .wa-float {{
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #25d366;
        color: #fff;
        padding: 15px 30px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        box-shadow: 0 5px 20px rgba(0,0,0,0.5);
        z-index: 999;
        border: 1px solid #1da851;
        transition: 0.3s;
    }}
    .wa-float:hover {{
        transform: scale(1.05);
        color: white;
        box-shadow: 0 0 20px #25d366;
    }}
</style>
""", unsafe_allow_html=True)

# --- 6. LAYOUT VISUAL ---

# Header
st.markdown("""
    <div class="brand-header">
        <div class="brand-title">AURUM SCENTS</div>
        <div class="brand-sub">Luxury Fragrances</div>
    </div>
""", unsafe_allow_html=True)

# Área Principal (Visor + Botões laterais próximos)
col_E, col_C, col_D = st.columns([1, 10, 1]) # Coluna do meio bem larga

with col_C:
    # O Visor
    if not visor_b64:
        st.error("⚠️ Erro: 'imagens/Visor.jpg' não encontrado.")
    else:
        src = f"data:image/png;base64,{img_produto_b64}" if img_produto_b64 else ""
        # Se não tiver imagem, usa placeholder transparente para não quebrar layout
        if not src: src = "https://via.placeholder.com/150x300/000000/000000?text=." 
        
        st.markdown(f"""
        <div class="visor-wrapper">
            <div class="visor-frame">
                <img src="{src}" class="perfume-overlay">
            </div>
        </div>
        """, unsafe_allow_html=True)

# Controles de Navegação (Logo abaixo do visor, centralizados)
c1, c2, c3, c4 = st.columns([1, 2, 2, 1])
with c2:
    st.button("❮ ANTERIOR", on_click=anterior)
with c3:
    st.button("PRÓXIMO ❯", on_click=proximo)

# Informações e Preço
st.markdown(f"""
    <div class="info-container">
        <div class="prod-name">{produto_atual['nome']}</div>
        <div class="price-box">
            <span class="old">De R$ {preco_antigo:.2f}</span>
            <span class="new">R$ {preco_atual:.2f}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Botão WhatsApp
msg = f"Olá Jerry! Tenho interesse no perfume {produto_atual['nome']}."
link_wa = f"https://wa.me/5531992051499?text={msg.replace(' ', '%20')}"
st.markdown(f"""
    <a href="{link_wa}" target="_blank" class="wa-float">
        Falar com Jerry Bombeta 💬
    </a>
""", unsafe_allow_html=True)
