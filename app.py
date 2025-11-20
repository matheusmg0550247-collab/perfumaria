import streamlit as st
import base64
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA (AGORA EM WIDE/LARGURA TOTAL) ---
st.set_page_config(
    page_title="Aurum Scents",
    page_icon="⚜️",
    layout="wide",  # <--- MUDANÇA AQUI: Usa a tela toda
    initial_sidebar_state="collapsed"
)

# --- 2. DADOS DOS PRODUTOS ---
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
    }
]

# --- 3. FUNÇÕES ---
def get_img_as_base64(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    # .replace('\n', '') garante que não quebra o HTML
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

# --- 4. CARREGAMENTO DE IMAGENS ---
visor_path = "imagens/Visor.jpg"
visor_b64 = get_img_as_base64(visor_path)

produto_atual = produtos[st.session_state.idx]
img_produto_b64 = get_img_as_base64(produto_atual["imagem"])

preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + 100.00

# --- 5. CSS (ESTILO E POSICIONAMENTO) ---
bg_visor_css = f"url('data:image/jpg;base64,{visor_b64}')" if visor_b64 else "none"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

    /* Fundo Geral */
    .stApp {{
        background-color: #050505;
        color: #d4af37;
    }}
    
    /* Remove margens padrão do Streamlit para aproveitar espaço */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 100% !important;
    }}

    /* --- VISOR --- */
    .visor-container {{
        position: relative;
        width: 100%;
        /* Altura fixa para garantir que o visor apareça inteiro */
        height: 70vh; 
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    .visor-frame {{
        position: relative;
        height: 100%;
        aspect-ratio: 9/13; /* Proporção aproximada da imagem do visor */
        background-image: {bg_visor_css};
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        /* Sombra para dar profundidade na tela */
        filter: drop-shadow(0 0 30px rgba(212, 175, 55, 0.1));
    }}

    /* --- PERFUME (CORREÇÃO DE POSIÇÃO) --- */
    .perfume-overlay {{
        position: absolute;
        /* Centraliza exatamente no meio do visor */
        top: 48%; 
        left: 50%;
        transform: translate(-50%, -50%);
        
        /* Tamanho do perfume em relação ao visor */
        width: 55%; 
        height: auto;
        
        z-index: 10;
        filter: drop-shadow(0 15px 20px rgba(0,0,0,0.6));
        transition: all 0.5s ease;
    }}
    
    .perfume-overlay:hover {{
        transform: translate(-50%, -52%) scale(1.05); /* Sobe um pouquinho ao passar o mouse */
    }}

    /* --- TEXTOS --- */
    .brand-title {{
        font-family: 'Cinzel', serif;
        font-size: 4vw; /* Tamanho responsivo */
        text-align: center;
        color: #d4af37;
        margin-bottom: 0;
        text-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
    }}
    
    .product-name {{
        font-family: 'Cinzel', serif;
        font-size: 2rem;
        color: #fff;
        text-align: center;
        margin-top: 1rem;
    }}
    
    .price-box {{
        text-align: center;
        font-family: 'Playfair Display', serif;
    }}
    
    .old-price {{ text-decoration: line-through; color: #666; font-size: 1.2rem; }}
    .new-price {{ color: #d4af37; font-size: 3rem; font-weight: bold; }}

    /* --- BOTÕES --- */
    div.stButton > button {{
        background: transparent;
        border: 1px solid #444;
        color: #888;
        width: 100%;
        height: 100%;
        padding: 20px 0;
        font-family: 'Cinzel', serif;
        font-size: 1.2rem;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        border-color: #d4af37;
        color: #d4af37;
        background: rgba(212, 175, 55, 0.05);
    }}

    /* --- CONTATO --- */
    .whatsapp-float {{
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #25d366;
        color: #FFF;
        border-radius: 50px;
        padding: 15px 25px;
        text-decoration: none;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        z-index: 100;
        font-family: sans-serif;
        border: 2px solid #1da851;
        transition: 0.3s;
    }}
    .whatsapp-float:hover {{
        transform: scale(1.1);
        color: white;
    }}

</style>
""", unsafe_allow_html=True)

# --- 6. LAYOUT (GRID) ---

# Título
st.markdown('<div class="brand-title">AURUM SCENTS</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; color:#888; letter-spacing:4px; margin-bottom:20px;">LUXURY FRAGRANCES</div>', unsafe_allow_html=True)

# Grid Principal: 3 Colunas (Botão Esq | Visor Central | Botão Dir)
# A coluna do meio (5) é bem maior que as laterais (1)
col_esq, col_meio, col_dir = st.columns([1, 4, 1], gap="large")

# Coluna Esquerda (Botão Voltar - Alinhado verticalmente ao meio usando CSS seria complexo, 
# então usamos espaço em branco 'write' para empurrar pra baixo se precisar, ou deixamos no topo)
with col_esq:
    st.write("") 
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.button("❮ ANTERIOR", on_click=anterior, use_container_width=True)

# Coluna do Meio (O Visor)
with col_meio:
    if not visor_b64:
        st.error("⚠️ Erro: Visor.jpg não encontrado na pasta imagens.")
    else:
        # Monta a imagem do perfume
        src_img = f"data:image/png;base64,{img_produto_b64}" if img_produto_b64 else ""
        
        # HTML Limpo para evitar quebra
        html_visor = f"""
        <div class="visor-container">
            <div class="visor-frame">
                <img src="{src_img}" class="perfume-overlay">
            </div>
        </div>
        """
        st.markdown(html_visor, unsafe_allow_html=True)
        
        # Informações logo abaixo do visor
        st.markdown(f"""
            <div class="product-name">{produto_atual['nome']}</div>
            <div class="price-box">
                <span class="old-price">De R$ {preco_antigo:.2f}</span><br>
                <span class="new-price">R$ {preco_atual:.2f}</span>
            </div>
        """, unsafe_allow_html=True)

# Coluna Direita (Botão Avançar)
with col_dir:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.button("PRÓXIMO ❯", on_click=proximo, use_container_width=True)


# --- 7. BOTÃO FLUTUANTE DO WHATSAPP (Fixo no canto da tela) ---
msg = f"Olá Jerry! Tenho interesse no perfume {produto_atual['nome']} de R$ {preco_atual}."
link_wa = f"https://wa.me/5531992051499?text={msg.replace(' ', '%20')}"

st.markdown(f"""
    <a href="{link_wa}" target="_blank" class="whatsapp-float">
        Falar com Jerry Bombeta 💬
    </a>
""", unsafe_allow_html=True)

# Footer discreto
st.markdown("<div style='text-align:center; margin-top:50px; color:#333;'>Aurum Scents © 2025</div>", unsafe_allow_html=True)
        
