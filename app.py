import streamlit as st
import base64
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Aurum Scents",
    page_icon="⚜️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. DADOS DOS PRODUTOS (ATUALIZADO: SEM ESPAÇOS NOS NOMES) ---
# Conforme seu print: Pasta 'imagens', Arquivo 'PerfumeX.png'
produtos = [
    {
        "nome": "Royal Elixir Gold",
        "imagem": "imagens/Perfume1.png", 
        "preco": 299.90
    },
    {
        "nome": "Black Orchid Intense",
        "imagem": "imagens/Perfume2.png", 
        "preco": 350.00
    },
    {
        "nome": "Velvet Santal Wood",
        "imagem": "imagens/Perfume3.png", 
        "preco": 420.00
    },
     {
        "nome": "Imperial Amber",
        "imagem": "imagens/Perfume4.png", 
        "preco": 380.00
    },
    # Adicione os outros seguindo o padrão (Perfume5.png, etc.)
]

# --- 3. FUNÇÕES UTILITÁRIAS ---
def get_img_as_base64(file_path):
    # Função robusta para carregar imagens
    if not os.path.exists(file_path):
        # Se não achar, retorna None. O código lá embaixo lida com isso.
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    # .replace('\n', '') é essencial para imagens grandes não quebrarem o HTML
    return base64.b64encode(data).decode('utf-8').replace('\n', '')

# --- 4. NAVEGAÇÃO (GERENCIAMENTO DE ESTADO) ---
if 'idx' not in st.session_state:
    st.session_state.idx = 0

def proximo():
    if st.session_state.idx < len(produtos) - 1:
        st.session_state.idx += 1
    else:
        st.session_state.idx = 0 # Loop volta ao início

def anterior():
    if st.session_state.idx > 0:
        st.session_state.idx -= 1
    else:
        st.session_state.idx = len(produtos) - 1 # Loop vai pro final

# --- 5. CARREGAMENTO DOS ATIVOS ---
# Carrega o Visor
visor_path = "imagens/Visor.jpg"
visor_b64 = get_img_as_base64(visor_path)

# Carrega o Produto Atual
produto_atual = produtos[st.session_state.idx]
img_produto_b64 = get_img_as_base64(produto_atual["imagem"])

# Preços
preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + 100.00

# --- 6. CSS DE LUXO (ESTÉTICA REFINADA) ---
bg_visor_css = f"url('data:image/jpg;base64,{visor_b64}')" if visor_b64 else "none"

st.markdown(f"""
<style>
    /* Importar fontes elegantes */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

    /* Fundo Preto Absoluto e Cor Dourada Principal */
    .stApp {{
        background-color: #000000;
        color: #d4af37;
    }}
    
    /* Remove padding excessivo do topo */
    .block-container {{
        padding-top: 2rem;
    }}

    /* --- HEADER --- */
    .brand-header {{ text-align: center; margin-bottom: 25px; }}
    .brand-title {{
        font-family: 'Cinzel', serif;
        font-size: 3rem;
        /* Gradiente dourado no texto */
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0; letter-spacing: 3px;
    }}
    .brand-sub {{
        font-family: 'Playfair Display', serif; color: #888;
        letter-spacing: 4px; font-size: 0.75rem; margin-top: 8px;
    }}

    /* --- VISOR E IMAGEM --- */
    .visor-wrapper {{
        display: flex; justify-content: center; margin-bottom: 20px;
    }}
    .visor-frame {{
        position: relative;
        width: 100%; max-width: 600px;
        aspect-ratio: 16/9;
        background-image: {bg_visor_css};
        background-size: cover; background-position: center;
        border-radius: 4px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .perfume-overlay {{
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -45%); /* Centraliza na luz */
        height: 58%; width: auto;
        filter: drop-shadow(0 10px 15px rgba(0,0,0,0.6));
        transition: all 0.5s ease-in-out;
    }}
    .perfume-overlay:hover {{ transform: translate(-50%, -47%) scale(1.03); }}

    /* --- NOVOS BOTÕES DE LUXO --- */
    div.stButton > button {{
        background-color: transparent;
        border: 1px solid #d4af37; /* Borda dourada fina */
        color: #d4af37; /* Texto dourado */
        font-family: 'Cinzel', serif;
        font-size: 0.9rem;
        letter-spacing: 2px;
        padding: 0.6rem 1rem;
        width: 100%;
        transition: all 0.3s ease;
        text-transform: uppercase;
    }}
    div.stButton > button:hover {{
        background-color: rgba(212, 175, 55, 0.15); /* Fundo dourado sutil ao passar o mouse */
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3); /* Brilho externo */
        border-color: #fff;
        color: #fff;
    }}

    /* --- PREÇO E INFO --- */
    .info-container {{ text-align: center; margin-top: 15px; }}
    .prod-name {{
        font-family: 'Cinzel', serif; font-size: 1.8rem; color: #fff; margin-bottom: 10px;
    }}
    .price-box {{ font-family: 'Playfair Display', serif; }}
    .old {{ text-decoration: line-through; color: #666; font-size: 1.1rem; margin-right: 15px; }}
    .new {{ color: #d4af37; font-size: 2.8rem; font-weight: 700; }}

    /* --- WHATSAPP FLUTUANTE --- */
    .wa-float {{
        position: fixed; bottom: 25px; right: 25px;
        background: linear-gradient(45deg, #25d366, #128c7e);
        color: #fff; padding: 12px 25px; border-radius: 50px;
        text-decoration: none; font-weight: bold; font-family: sans-serif;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4); z-index: 99;
        border: 1px solid #25d366; transition: 0.3s;
    }}
    .wa-float:hover {{ transform: scale(1.05); color: white; box-shadow: 0 0 20px rgba(37, 211, 102, 0.6); }}
</style>
""", unsafe_allow_html=True)

# --- 7. RENDERIZAÇÃO DO LAYOUT ---

# Header
st.markdown("""
    <div class="brand-header">
        <div class="brand-title">AURUM SCENTS</div>
        <div class="brand-sub">LUXURY FRAGRANCES</div>
    </div>
""", unsafe_allow_html=True)

# Área Principal (Visor)
# Verifica se o visor carregou antes de tentar mostrar
if not visor_b64:
    st.error("⚠️ Erro: Não encontrei 'imagens/Visor.jpg'. Verifique a pasta no GitHub.")
else:
    # Se a imagem do perfume falhar, usa um placeholder transparente
    src = f"data:image/png;base64,{img_produto_b64}" if img_produto_b64 else "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    st.markdown(f"""
    <div class="visor-wrapper">
        <div class="visor-frame">
            <img src="{src}" class="perfume-overlay">
        </div>
    </div>
    """, unsafe_allow_html=True)

# Botões de Navegação (Centralizados abaixo do visor)
c1, c2, c3 = st.columns([1, 2, 1])
with c1:
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
    
