import streamlit as st
import base64
import os
import re

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Aurum Scents",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CATÁLOGO ---
CATALOGO = {
    1: {"nome": "Royal Elixir Gold", "preco": 299.90, "desc": "Notas de ouro, mel e especiarias raras."},
    2: {"nome": "Black Orchid Intense", "preco": 350.00, "desc": "Orquídea negra profunda e misteriosa."},
    3: {"nome": "Velvet Santal Wood", "preco": 420.00, "desc": "Sândalo aveludado com toque de couro."},
    4: {"nome": "Imperial Amber", "preco": 380.00, "desc": "Âmbar imperial com raspas cítricas."},
    5: {"nome": "Club de Nuit Intense", "preco": 250.00, "desc": "Cítrico amadeirado marcante e viril."},
    6: {"nome": "Midnight Saffron", "preco": 310.00, "desc": "Açafrão noturno com fundo de tabaco."},
    7: {"nome": "Oceanic Leather", "preco": 275.00, "desc": "Couro italiano com brisa marinha."},
    8: {"nome": "Rose of Dubai", "preco": 340.00, "desc": "Rosas damascenas colhidas ao amanhecer."},
    9: {"nome": "Emerald Vetiver", "preco": 290.00, "desc": "Vetiver fresco com notas verdes vibrantes."},
    10: {"nome": "Golden Tobacco", "preco": 450.00, "desc": "Folhas de tabaco cubano e baunilha."},
    11: {"nome": "Pure Musk Absolute", "preco": 220.00, "desc": "Almíscar puro, limpo e sofisticado."},
    12: {"nome": "Celestial Oud", "preco": 550.00, "desc": "Oud raro envelhecido em barris de carvalho."},
    13: {"nome": "Spice Route", "preco": 260.00, "desc": "Pimenta rosa, cardamomo e noz-moscada."},
    14: {"nome": "Vanilla Noir", "preco": 280.00, "desc": "Baunilha negra de Madagascar defumada."},
    15: {"nome": "Cedar & Cognac", "preco": 330.00, "desc": "Cedro nobre banhado em conhaque envelhecido."},
    16: {"nome": "Majestic Iris", "preco": 360.00, "desc": "Íris atalcada com fundo amadeirado suave."},
}

# --- 3. FUNÇÕES DE CARREGAMENTO ---
def carregar_produtos_automaticamente():
    produtos_encontrados = []
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_imagens = os.path.join(pasta_atual, "imagens")
    if not os.path.exists(pasta_imagens):
        pasta_imagens = os.path.join(pasta_atual, "images")
        if not os.path.exists(pasta_imagens): return []

    arquivos = os.listdir(pasta_imagens)
    def extrair_numero(texto):
        nums = re.findall(r'\d+', texto)
        return int(nums[0]) if nums else 999

    arquivos_validos = [f for f in arquivos if "perfume" in f.lower() and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    arquivos_ordenados = sorted(arquivos_validos, key=extrair_numero)
    ids_processados = set()

    for arquivo in arquivos_ordenados:
        numero = extrair_numero(arquivo)
        if numero in ids_processados or numero > 16: continue
        dados = CATALOGO.get(numero, {"nome": f"Perfume {numero}", "preco": 0.00, "desc": "Fragrância exclusiva."})
        produtos_encontrados.append({"id": numero, "nome": dados["nome"], "arquivo": os.path.join(pasta_imagens, arquivo), "preco": dados["preco"], "desc": dados["desc"]})
        ids_processados.add(numero)
    return produtos_encontrados

def get_img_as_base64(caminho):
    if not caminho or not os.path.exists(caminho): return None
    try:
        with open(caminho, "rb") as f: data = f.read()
        return base64.b64encode(data).decode('utf-8')
    except: return None

# --- 4. INICIALIZAÇÃO ---
produtos = carregar_produtos_automaticamente()
if not produtos: st.stop()

if 'idx' not in st.session_state: st.session_state.idx = 0
def proximo(): st.session_state.idx = (st.session_state.idx + 1) % len(produtos)
def anterior(): st.session_state.idx = (st.session_state.idx - 1 + len(produtos)) % len(produtos)

produto_atual = produtos[st.session_state.idx]
img_produto_b64 = get_img_as_base64(produto_atual["arquivo"])
path_base = os.path.dirname(produtos[0]["arquivo"])
path_visor = os.path.join(path_base, "Visor.jpg")
if not os.path.exists(path_visor): path_visor = os.path.join(path_base, "Visor.png")
visor_b64 = get_img_as_base64(path_visor)
preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + (100 if preco_atual > 0 else 0)

# --- 5. CSS DEFINITIVO (AJUSTE FINO DE POSIÇÃO) ---
bg_visor_css = f"url('data:image/png;base64,{visor_b64}')" if visor_b64 else "#222"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
    
    .stApp {{ background-color: #000000; color: #d4af37; }}
    .block-container {{ padding-top: 2rem; max-width: 1400px !important; }}
    
    h1, h3, .prod-name, .contact-name {{ font-family: 'Cinzel', serif !important; text-transform: uppercase; letter-spacing: 2px; }}
    p, div {{ font-family: 'Playfair Display', serif; }}

    /* HEADER */
    .brand-title {{
        font-size: 4rem; text-align: center; margin-bottom: 50px;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 10px rgba(0,0,0,0.8);
    }}

    /* LAYOUT */
    [data-testid="column"] {{ display: flex; flex-direction: column; justify-content: center; }}

    /* ESQUERDA */
    .left-panel {{ padding-right: 30px; border-right: 1px solid #222; text-align: justify; height: 100%; display: flex; flex-direction: column; justify-content: center; }}
    .panel-text {{ font-size: 1.1rem; color: #aaa; line-height: 1.8; margin-bottom: 20px; }}

    /* --- VISOR CENTRAL --- */
    .visor-wrapper {{
        position: relative; width: 100%; max-width: 850px;
        aspect-ratio: 16/9; margin: 0 auto 25px auto;
        background-image: {bg_visor_css}; background-size: cover; background-position: center;
        border-radius: 4px; box-shadow: 0 25px 50px rgba(0,0,0,0.9);
    }}
    
    /* MÁSCARA */
    .visor-mask {{
        position: absolute;
        top: 8%; left: 18.3%; width: 63.4%; 
        height: 66%; 
        overflow: hidden;
        display: flex; align-items: flex-end; justify-content: center; /* Centraliza horizontalmente */
    }}

    .perfume-img {{
        /* AJUSTE 1: Reduzi a altura de 85% para 78% para dar respiro no topo */
        height: 78%; 
        width: auto;
        mix-blend-mode: multiply;
        filter: contrast(1.1) brightness(0.95);
        transition: transform 0.5s ease;
        /* AJUSTE 2: Aumentei a margem inferior para levantar o perfume da base */
        margin-bottom: 4%; 
    }}
    .perfume-img:hover {{ transform: scale(1.05); mix-blend-mode: normal; }}

    /* INFO E BOTOES */
    .info-container {{ text-align: center; }}
    .prod-name {{ font-size: 2.5rem; color: #fff; margin-bottom: 5px; }}
    .prod-desc {{ color: #888; font-style: italic; margin-bottom: 15px; }}
    .old {{ text-decoration: line-through; color: #555; font-size: 1.3rem; margin-right: 15px; }}
    .new {{ color: #d4af37; font-size: 3rem; font-weight: 700; }}

    div.stButton > button {{
        background: transparent; border: 1px solid #d4af37; color: #d4af37;
        font-family: 'Cinzel', serif; width: 100%; padding: 0.8rem; letter-spacing: 2px; text-transform: uppercase; white-space: nowrap;
    }}
    div.stButton > button:hover {{ background: rgba(212, 175, 55, 0.15); color: #fff; border-color: #fff; }}

    /* DIREITA */
    .right-panel {{
        background: linear-gradient(145deg, #111, #0a0a0a); padding: 40px; 
        border-radius: 10px; text-align: center; border: 1px solid #222;
        height: fit-content;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .wa-btn {{
        display: block; background: linear-gradient(45deg, #25d366, #128c7e); color: white;
        padding: 15px; border-radius: 50px; text-decoration: none; font-weight: bold; font-family: sans-serif;
        margin-top: 25px; transition: 0.3s; letter-spacing: 1px;
    }}
    .wa-btn:hover {{ transform: scale(1.05); color: white; box-shadow: 0 5px 15px rgba(37, 211, 102, 0.4); }}

    /* RODAPÉ */
    .final-footer {{
        text-align: center; margin-top: 80px; padding-top: 30px;
        border-top: 1px solid #222; color: #666; font-family: 'Playfair Display', serif; font-style: italic;
    }}
</style>
""", unsafe_allow_html=True)

# --- 6. ESTRUTURA DO LAYOUT ---
st.markdown('<div class="brand-title">AURUM SCENTS</div>', unsafe_allow_html=True)

col_L, col_C, col_R = st.columns([3, 6, 3], gap="large")

# ESQUERDA
with col_L:
    st.markdown("""
    <div class="left-panel">
        <h3 style="color:#d4af37; margin-bottom:25px;">A Essência do Luxo</h3>
        <p class="panel-text">Na Aurum Scents, a fragrância não é apenas um aroma, é uma assinatura invisível que define sua presença.</p>
        <p class="panel-text">Nossa curadoria busca os ingredientes mais raros do mundo para despertar os prazeres da fragrância em sua forma mais pura e sofisticada.</p>
        <p class="panel-text" style="margin-top:20px; font-size:0.9rem; color:#888;">Cada frasco em nossa vitrine é uma promessa de distinção e elegância atemporal.</p>
    </div>
    """, unsafe_allow_html=True)

# CENTRO
with col_C:
    src = f"data:image/png;base64,{img_produto_b64}" if img_produto_b64 else "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    st.markdown(f"""
    <div class="visor-wrapper">
        <div class="visor-mask">
            <img src="{src}" class="perfume-img">
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2, 0.1, 1.2]) 
    with c1: st.button("❮ ANTERIOR", on_click=anterior, use_container_width=True)
    with c3: st.button("PRÓXIMO ❯", on_click=proximo, use_container_width=True)

    st.markdown(f"""
        <div class="info-container" style="margin-top: 25px;">
            <div class="prod-name">{produto_atual['nome']}</div>
            <div class="prod-desc">— {produto_atual['desc']} —</div>
            <div class="price-box">
                <span class="old">De R$ {preco_antigo:.2f}</span>
                <span class="new">R$ {preco_atual:.2f}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# DIREITA
with col_R:
    msg = f"Olá Jerry! Tenho interesse no exclusivo {produto_atual['nome']}."
    link = f"https://wa.me/5531992051499?text={msg.replace(' ', '%20')}"
    st.markdown(f"""
    <div class="right-panel">
        <div style="color:#fff; margin-bottom:10px; letter-spacing:2px;">ATENDIMENTO EXCLUSIVO</div>
        <div class="contact-name" style="font-size:2rem; color:#d4af37; margin-bottom:5px;">JERRY BOMBETA</div>
        <div style="color:#888; font-size:0.9rem; font-style:italic;">Specialist Fragrance Consultant</div>
        <a href="{link}" target="_blank" class="wa-btn">FALAR NO WHATSAPP</a>
        <div style="margin-top:25px; color:#d4af37; font-weight:bold; letter-spacing:1px;">📞 (31) 99205-1499</div>
    </div>
    """, unsafe_allow_html=True)

# --- 7. RODAPÉ ---
st.markdown("""
<div class="final-footer">
    "O perfume é a forma mais intensa da memória. Ele é o acessório invisível e definitivo da moda, que anuncia sua chegada e prolonga sua partida."
    <br><br>
    AURUM SCENTS — Redefinindo a Perfumaria de Nicho.
</div>
""", unsafe_allow_html=True)
