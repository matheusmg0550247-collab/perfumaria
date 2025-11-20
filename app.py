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
# Certifique-se que as imagens dos perfumes também estão na pasta 'images'
produtos = [
    {
        "nome": "Royal Elixir Gold",
        "imagem": "images/perfume1.png", 
        "preco": 299.90
    },
    {
        "nome": "Black Orchid Intense",
        "imagem": "images/perfume2.png", 
        "preco": 350.00
    },
    {
        "nome": "Velvet Santal Wood",
        "imagem": "images/perfume3.png", 
        "preco": 420.00
    },
]

# --- FUNÇÕES UTILITÁRIAS ---

def get_img_as_base64(file_path):
    """Converte imagem para base64 para usar no HTML/CSS"""
    # Verifica se o arquivo existe antes de tentar abrir
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- GERENCIAMENTO DE ESTADO (NAVEGAÇÃO) ---
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
# CORREÇÃO AQUI: Agora ele busca dentro da pasta 'images/'
visor_path = "images/Visor.png" 

# Nota de segurança: Se o seu arquivo for .jpg, mude a linha acima para "images/Visor.jpg"
visor_b64 = get_img_as_base64(visor_path)

# 2. Carregar Imagem do Produto Atual
produto_atual = produtos[st.session_state.idx]
img_produto_path = produto_atual["imagem"]
img_produto_b64 = get_img_as_base64(img_produto_path)

# 3. Cálculos de Preço
preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + 100.00

# --- ESTILIZAÇÃO CSS (LUXO / OLD MONEY) ---
bg_visor_css = f"url('data:image/png;base64,{visor_b64}')" if visor_b64 else "none"
bg_color_fallback = "#2c2c2c" if not visor_b64 else "transparent"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

    .stApp {{
        background-color: #0e0e0e;
        color: #e5c15d;
    }}

    /* LOGO */
    .logo-container {{
        text-align: center;
        margin-bottom: 20px;
        padding-bottom: 20px;
        border-bottom: 1px solid #333;
    }}
    .brand-name {{
        font-family: 'Cinzel', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin: 0;
    }}
    .brand-subtitle {{
        font-family: 'Playfair Display', serif;
        font-size: 1rem;
        color: #888;
        letter-spacing: 2px;
        margin-top: -5px;
    }}

    /* VISOR */
    .visor-stage {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }}
    
    .visor-frame {{
        position: relative;
        width: 100%;
        max-width: 500px;
        aspect-ratio: 1 / 1.1; 
        background-image: {bg_visor_css};
        background-color: {bg_color_fallback};
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .perfume-display {{
        width: 50%; 
        height: auto;
        z-index: 10;
        filter: drop-shadow(0px 15px 10px rgba(0,0,0,0.6));
        transition: transform 0.5s ease;
        margin-top: -5%;
    }}
    
    /* PREÇO */
    .price-tag {{
        text-align: center;
        font-family: 'Playfair Display', serif;
        margin-top: 15px;
    }}
    .price-old {{
        color: #666;
        text-decoration: line-through;
        font-size: 1.2rem;
    }}
    .price-new {{
        color: #e5c15d;
        font-size: 2.8rem;
        font-weight: 700;
        text-shadow: 0px 0px 15px rgba(229, 193, 93, 0.3);
    }}
    .product-title {{
        font-family: 'Cinzel', serif;
        font-size: 1.5rem;
        color: #fff;
        margin-bottom: 5px;
    }}

    /* BOTÕES */
    div.stButton > button {{
        background-color: transparent;
        border: 1px solid #e5c15d;
        color: #e5c15d;
        font-family: 'Cinzel', serif;
        width: 100%;
        border-radius: 0px;
    }}
    div.stButton > button:hover {{
        background-color: #e5c15d;
        color: #000;
        border-color: #fff;
    }}

    /* FOOTER JERRY */
    .footer-box {{
        margin-top: 50px;
        padding: 30px;
        background: linear-gradient(180deg, rgba(20,20,20,0) 0%, rgba(30,30,30,1) 100%);
        border-top: 1px solid #333;
        text-align: center;
        border-radius: 10px;
    }}
    .contact-name {{
        font-family: 'Cinzel', serif;
        font-size: 2rem;
        color: #fff;
        margin: 10px 0;
    }}
    .whatsapp-btn {{
        display: inline-block;
        background-color: #25D366;
        color: white;
        padding: 12px 30px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        font-family: sans-serif;
        margin-top: 10px;
    }}
    .whatsapp-btn:hover {{
        background-color: #1ebd59;
        color: white !important;
        text-decoration: none;
    }}
</style>
""", unsafe_allow_html=True)

# --- RENDERIZAÇÃO (FRONT-END) ---

# 1. Header
st.markdown("""
    <div class="logo-container">
        <div class="brand-name">AURUM SCENTS</div>
        <div class="brand-subtitle">ESSÊNCIA E SOFISTICAÇÃO</div>
    </div>
""", unsafe_allow_html=True)

# 2. Visor
if not visor_b64:
    # Mensagem de erro mais clara caso o arquivo ainda não seja encontrado
    st.error(f"⚠️ Erro: Não encontrei o arquivo '{visor_path}'. Verifique se o nome está exato (Visor.png vs Visor.jpg) dentro da pasta images.")
else:
    src_img = f"data:image/png;base64,{img_produto_b64}" if img_produto_b64 else "https://via.placeholder.com/300x500/000000/FFFFFF?text=Sem+Imagem"
    
    st.markdown(f"""
        <div class="visor-stage">
            <div class="visor-frame">
                <img src="{src_img}" class="perfume-display">
            </div>
        </div>
    """, unsafe_allow_html=True)

# 3. Navegação
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.button("❮ ANTERIOR", on_click=anterior)
with col3:
    st.button("PRÓXIMO ❯", on_click=proximo)

# 4. Info Produto
st.markdown(f"""
    <div class="price-tag">
        <div class="product-title">{produto_atual['nome']}</div>
        <div class="price-old">De R$ {preco_antigo:.2f}</div>
        <div class="price-new">R$ {preco_atual:.2f}</div>
    </div>
""", unsafe_allow_html=True)

# 5. Footer
msg = f"Olá Jerry! Gostaria de comprar o perfume {produto_atual['nome']}."
link_wa = f"https://wa.me/5531992051499?text={msg.replace(' ', '%20')}"

st.markdown(f"""
    <div class="footer-box">
        <div style="color:#888; letter-spacing:2px; font-size:0.8em;">ATENDIMENTO EXCLUSIVO</div>
        <div class="contact-name">Jerry Bombeta</div>
        <div style="color:#d4af37; font-weight:bold;">📞 (31) 99205-1499</div>
        <br>
        <a href="{link_wa}" target="_blank" class="whatsapp-btn">
            COMPRAR AGORA PELO WHATSAPP
        </a>
    </div>
""", unsafe_allow_html=True)
