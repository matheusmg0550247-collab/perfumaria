import streamlit as st
import base64
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Aurum Scents - Perfumaria de Luxo",
    page_icon="⚜️",
    layout="centered"
)

# --- CONFIGURAÇÃO DOS PRODUTOS ---
# AJUSTADO: Nomes exatos conforme seu print (Pasta 'imagens' e espaços nos nomes)
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
    # Se quiser adicionar os outros (5, 6, etc), basta seguir o padrão acima
]

# --- FUNÇÕES UTILITÁRIAS ---

def get_img_as_base64(file_path):
    """Converte imagem para base64"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- GERENCIAMENTO DE NAVEGAÇÃO ---
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

# --- CARREGAMENTO DE RECURSOS ---

# 1. Carregar Fundo do Visor
# AJUSTADO: Pasta 'imagens' e extensão '.jpg'
visor_path = "imagens/Visor.jpg" 
visor_b64 = get_img_as_base64(visor_path)

# 2. Carregar Imagem do Produto Atual
produto_atual = produtos[st.session_state.idx]
img_produto_path = produto_atual["imagem"]
img_produto_b64 = get_img_as_base64(img_produto_path)

# 3. Cálculos
preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + 100.00

# --- ESTILIZAÇÃO CSS (FEIXE DE LUZ + LUXO) ---
bg_visor_css = f"url('data:image/jpg;base64,{visor_b64}')" if visor_b64 else "none"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

    .stApp {{
        background-color: #0a0a0a;
        color: #e5c15d;
    }}

    /* --- CABEÇALHO --- */
    .logo-container {{
        text-align: center;
        margin-bottom: 10px;
        padding-bottom: 10px;
        border-bottom: 1px solid #333;
    }}
    .brand-name {{
        font-family: 'Cinzel', serif;
        font-size: 3rem;
        font-weight: 700;
        color: #d4af37;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-shadow: 0 2px 10px rgba(212, 175, 55, 0.2);
    }}

    /* --- VISOR MÁGICO --- */
    .visor-stage {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 10px 0;
    }}
    
    .visor-frame {{
        position: relative;
        width: 100%;
        max-width: 450px; /* Tamanho controlado */
        aspect-ratio: 1 / 1.1;
        background-image: {bg_visor_css};
        background-color: #111;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden; /* Importante para o feixe de luz não vazar */
    }}

    /* --- EFEITO DE LUZ (FEIXE) --- */
    .light-beam {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        /* Gradiente radial simulando luz vindo de cima */
        background: radial-gradient(
            ellipse at top, 
            rgba(255, 230, 150, 0.25) 0%, 
            rgba(255, 215, 0, 0.05) 40%, 
            transparent 70%
        );
        z-index: 5;
        pointer-events: none;
        mix-blend-mode: screen;
    }}
    
    /* Brilho extra pulsante */
    @keyframes pulse-glow {{
        0% {{ opacity: 0.5; }}
        50% {{ opacity: 0.8; }}
        100% {{ opacity: 0.5; }}
    }}
    
    .light-spot {{
        position: absolute;
        top: 15%;
        width: 60%;
        height: 60%;
        background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 60%);
        z-index: 6;
        animation: pulse-glow 4s infinite ease-in-out;
    }}

    /* --- PERFUME --- */
    .perfume-display {{
        width: 52%; 
        height: auto;
        z-index: 10; /* Fica na frente da luz de fundo, mas atrás do brilho se quiser */
        filter: drop-shadow(0px 20px 20px rgba(0,0,0,0.8));
        transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        margin-top: -20px;
    }}
    .perfume-display:hover {{
        transform: scale(1.08);
    }}

    /* --- PREÇOS --- */
    .price-tag {{
        text-align: center;
        font-family: 'Playfair Display', serif;
        margin-top: 5px;
    }}
    .price-old {{
        color: #555;
        text-decoration: line-through;
        font-size: 1rem;
    }}
    .price-new {{
        color: #e5c15d;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 0 15px rgba(229, 193, 93, 0.4);
    }}
    .product-title {{
        font-family: 'Cinzel', serif;
        font-size: 1.4rem;
        color: #fff;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }}

    /* --- BOTÕES --- */
    div.stButton > button {{
        background-color: transparent;
        border: 1px solid #555;
        color: #aaa;
        font-family: 'Cinzel', serif;
        width: 100%;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        border-color: #e5c15d;
        color: #e5c15d;
        background-color: rgba(229, 193, 93, 0.05);
    }}

    /* --- FOOTER JERRY --- */
    .footer-box {{
        margin-top: 40px;
        padding: 25px;
        background: linear-gradient(to top, #111, #0a0a0a);
        border-top: 1px solid #333;
        text-align: center;
        border-radius: 8px;
    }}
    .contact-name {{
        font-family: 'Cinzel', serif;
        font-size: 1.8rem;
        color: #fff;
        margin: 5px 0;
    }}
    .whatsapp-btn {{
        display: inline-block;
        background: linear-gradient(45deg, #25D366, #128C7E);
        color: white !important;
        padding: 12px 30px;
        border-radius: 4px;
        text-decoration: none;
        font-weight: bold;
        font-family: sans-serif;
        margin-top: 15px;
        letter-spacing: 1px;
        box-shadow: 0 5px 15px rgba(37, 211, 102, 0.2);
    }}
    .whatsapp-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 211, 102, 0.4);
    }}
</style>
""", unsafe_allow_html=True)

# --- FRONT-END ---

# 1. Logo
st.markdown("""
    <div class="logo-container">
        <div class="brand-name">AURUM SCENTS</div>
        <div style="color:#666; font-size:0.8em; letter-spacing:3px;">LUXURY FRAGRANCES</div>
    </div>
""", unsafe_allow_html=True)

# 2. Visor com Feixe de Luz
if not visor_b64:
    st.error(f"⚠️ Ainda não encontrei: '{visor_path}'. Confira se a pasta no Github chama 'imagens' (com 'n') e o arquivo 'Visor.jpg'.")
else:
    src_img = f"data:image/png;base64,{img_produto_b64}" if img_produto_b64 else "https://via.placeholder.com/300x500/000000/FFFFFF?text=Imagem+Nao+Encontrada"
    
    st.markdown(f"""
        <div class="visor-stage">
            <div class="visor-frame">
                <div class="light-beam"></div>
                <div class="light-spot"></div>
                
                <img src="{src_img}" class="perfume-display">
            </div>
        </div>
    """, unsafe_allow_html=True)

# 3. Botões de Navegação
c1, c2, c3 = st.columns([1, 2, 1])
with c1:
    st.button("❮ VOLTAR", on_click=anterior)
with c3:
    st.button("AVANÇAR ❯", on_click=proximo)

# 4. Informações do Produto
st.markdown(f"""
    <div class="price-tag">
        <div class="product-title">{produto_atual['nome']}</div>
        <div class="price-old">De R$ {preco_antigo:.2f}</div>
        <div class="price-new">R$ {preco_atual:.2f}</div>
    </div>
""", unsafe_allow_html=True)

# 5. Footer
msg = f"Olá Jerry! Tenho interesse no perfume {produto_atual['nome']}."
link_wa = f"https://wa.me/5531992051499?text={msg.replace(' ', '%20')}"

st.markdown(f"""
    <div class="footer-box">
        <div style="color:#888; letter-spacing:1px; font-size:0.7em; margin-bottom:5px;">CONSULTOR EXCLUSIVO</div>
        <div class="contact-name">Jerry Bombeta</div>
        <div style="color:#d4af37;">(31) 99205-1499</div>
        <a href="{link_wa}" target="_blank" class="whatsapp-btn">
            COMPRAR NO WHATSAPP
        </a>
    </div>
""", unsafe_allow_html=True)
