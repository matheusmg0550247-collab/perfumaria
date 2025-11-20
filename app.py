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

# --- 2. CATÁLOGO (Preços e Descrições) ---
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

# --- 3. VARREDURA DE ARQUIVOS ---
def carregar_produtos_automaticamente():
    produtos_encontrados = []
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_imagens = os.path.join(pasta_atual, "imagens")
    
    if not os.path.exists(pasta_imagens):
        # Tenta achar se o nome da pasta estiver diferente
        pasta_imagens = os.path.join(pasta_atual, "images")
        if not os.path.exists(pasta_imagens):
             st.error("❌ Pasta 'imagens' não encontrada.")
             return []

    arquivos = os.listdir(pasta_imagens)
    
    def extrair_numero(texto):
        nums = re.findall(r'\d+', texto)
        return int(nums[0]) if nums else 999

    # Filtra e ordena arquivos de perfume
    arquivos_validos = [f for f in arquivos if "perfume" in f.lower() and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    arquivos_ordenados = sorted(arquivos_validos, key=extrair_numero)

    ids_processados = set() 

    for arquivo in arquivos_ordenados:
        numero = extrair_numero(arquivo)
        if numero in ids_processados: continue
        if numero > 16: continue # Limita aos 16 do catálogo
            
        dados = CATALOGO.get(numero, {"nome": f"Perfume {numero}", "preco": 0.00, "desc": "Fragrância exclusiva."})
        
        produtos_encontrados.append({
            "id": numero,
            "nome": dados["nome"],
            "arquivo": os.path.join(pasta_imagens, arquivo),
            "preco": dados["preco"],
            "desc": dados["desc"]
        })
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

# Busca Visor na pasta correta
path_base = os.path.dirname(produtos[0]["arquivo"]) # Pega a mesma pasta dos perfumes
path_visor = os.path.join(path_base, "Visor.jpg")
if not os.path.exists(path_visor): path_visor = os.path.join(path_base, "Visor.png")
visor_b64 = get_img_as_base64(path_visor)

preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + (100 if preco_atual > 0 else 0)

# --- 5. CSS DE LUXO (COM MÁSCARA DE RECORTE) ---
bg_visor_css = f"url('data:image/png;base64,{visor_b64}')" if visor_b64 else "#222"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
    
    /* Reset e Fundo */
    .stApp {{ background-color: #050505; color: #d4af37; }}
    .block-container {{ padding-top: 2rem; max-width: 1200px !important; }}
    
    /* TIPOGRAFIA GLOBAL */
    h1, h2, h3 {{ font-family: 'Cinzel', serif !important; text-transform: uppercase; letter-spacing: 3px; }}
    p, div {{ font-family: 'Playfair Display', serif; }}

    /* HEADER */
    .brand-title {{
        font-size: 4.5rem; text-align: center; margin-bottom: 40px;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }}

    /* --- VISOR COM MÁSCARA (O SEGREDO) --- */
    .visor-wrapper {{
        position: relative; width: 100%; max-width: 900px; /* Visor Gigante */
        aspect-ratio: 16/9; margin: 0 auto 30px auto;
        background-image: {bg_visor_css}; background-size: cover; background-position: center;
        border-radius: 8px; box-shadow: 0 30px 60px rgba(0,0,0,0.9);
    }}
    
    /* Esta é a "caixa invisível" que corta o perfume */
    .visor-light-zone {{
        position: absolute;
        /* Essas porcentagens definem a área exata da luz na sua imagem do visor */
        top: 8%; left: 18.5%; width: 63%; height: 78%;
        overflow: hidden; /* CORTA TUDO QUE SAIR DAQUI */
        display: flex; align-items: flex-end; justify-content: center; /* Alinha o perfume na base */
    }}

    /* O perfume dentro da zona de luz */
    .perfume-img {{
        height: 85%; /* Ocupa 85% da altura da luz */
        width: auto;
        mix-blend-mode: multiply; /* Truque para JPG com fundo branco */
        filter: contrast(1.1) brightness(0.95) drop-shadow(0 10px 15px rgba(0,0,0,0.5));
        transition: transform 0.5s ease;
        margin-bottom: 2%; /* Pequeno ajuste para não tocar na base de madeira */
    }}
    .perfume-img:hover {{ transform: scale(1.05); mix-blend-mode: normal; }}

    /* --- DETALHES DO PRODUTO (Abaixo do visor) --- */
    .details-section {{ text-align: center; margin-top: 40px; padding-bottom: 40px; border-bottom: 1px solid #222; }}
    .prod-name {{ font-family: 'Cinzel', serif; font-size: 3rem; color: #fff; margin-bottom: 10px; }}
    .prod-desc {{ color: #aaa; font-style: italic; font-size: 1.2rem; margin-bottom: 20px; }}
    .price-box {{ }}
    .old {{ text-decoration: line-through; color: #555; font-size: 1.4rem; margin-right: 15px; }}
    .new {{ color: #d4af37; font-size: 3.5rem; font-weight: 700; text-shadow: 0 0 20px rgba(212, 175, 55, 0.3); }}

    /* BOTÕES DE NAVEGAÇÃO */
    div.stButton > button {{
        background: transparent; border: 1px solid #d4af37; color: #d4af37;
        font-family: 'Cinzel', serif; width: 100%; padding: 1rem; 
        text-transform: uppercase; letter-spacing: 3px; font-size: 0.9rem; transition: 0.3s;
    }}
    div.stButton > button:hover {{
        background: rgba(212, 175, 55, 0.2); color: #fff; border-color: #fff; box-shadow: 0 0 25px rgba(212, 175, 55, 0.4);
    }}

    /* --- RODAPÉ DE LUXO (História + Contato) --- */
    .footer-section {{ margin-top: 50px; display: flex; gap: 40px; align-items: center; }}
    .footer-story {{ flex: 1; text-align: justify; color: #aaa; line-height: 1.8; padding-right: 30px; border-right: 1px solid #222; }}
    .footer-contact {{ flex: 0.8; text-align: center; background: linear-gradient(145deg, #111, #0a0a0a); padding: 40px; border-radius: 12px; border: 1px solid #222; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }}
    .contact-name {{ font-size: 2.2rem; color: #d4af37; margin: 15px 0; }}
    .wa-btn {{
        display: inline-block; background: linear-gradient(45deg, #25d366, #128c7e); color: white;
        padding: 15px 35px; border-radius: 50px; text-decoration: none; font-weight: bold; font-family: sans-serif;
        margin-top: 25px; letter-spacing: 1px; box-shadow: 0 10px 20px rgba(37, 211, 102, 0.2); transition: 0.3s;
    }}
    .wa-btn:hover {{ transform: translateY(-3px); box-shadow: 0 15px 30px rgba(37, 211, 102, 0.4); color: white !important; }}
</style>
""", unsafe_allow_html=True)

# --- 6. ESTRUTURA DO LAYOUT VERTICAL ---

# 1. Título
st.markdown('<div class="brand-title">AURUM SCENTS</div>', unsafe_allow_html=True)

# 2. Visor Principal (O Herói da página)
if not visor_b64:
    st.error("⚠️ Visor não encontrado na pasta de imagens.")
else:
    # Define a imagem (ou um pixel transparente se falhar)
    src = f"data:image/png;base64,{img_produto_b64}" if img_produto_b64 else "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    # HTML com a nova estrutura de MÁSCARA (.visor-light-zone)
    st.markdown(f"""
    <div class="visor-wrapper">
        <div class="visor-light-zone">
            <img src="{src}" class="perfume-img">
        </div>
    </div>
    """, unsafe_allow_html=True)

# 3. Navegação e Detalhes (Abaixo do Visor)
# Colunas para centralizar os botões e deixá-los mais estreitos
cb1, cb2, cb3 = st.columns([1.5, 2, 1.5])
with cb1: st.button("❮ ANTERIOR", on_click=anterior)
with cb3: st.button("PRÓXIMO ❯", on_click=proximo)

st.markdown(f"""
<div class="details-section">
    <div class="prod-name">{produto_atual['nome']}</div>
    <div class="prod-desc">— {produto_atual['desc']} —</div>
    <div class="price-box">
        <span class="old">De R$ {preco_antigo:.2f}</span>
        <span class="new">R$ {preco_atual:.2f}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Rodapé de Luxo (História e Contato lado a lado)
msg = f"Olá Jerry! Tenho interesse no {produto_atual['nome']}."
link_wa = f"https://wa.me/5531992051499?text={msg.replace(' ', '%20')}"

st.markdown(f"""
<div class="footer-section">
    <div class="footer-story">
        <h3>A Essência do Luxo</h3>
        <p>Na Aurum Scents, acreditamos que uma fragrância não é apenas um aroma, é uma assinatura invisível, uma memória líquida.</p>
        <p>Nossa curadoria busca os ingredientes mais raros e as composições mais sofisticadas para despertar os prazeres da fragrância em sua forma mais pura. Cada frasco em nossa vitrine é uma promessa de distinção e elegância atemporal.</p>
    </div>
    <div class="footer-contact">
        <div style="color:#fff; letter-spacing:2px; font-size:0.9rem;">ATENDIMENTO EXCLUSIVO</div>
        <div class="contact-name">Jerry Bombeta</div>
        <div style="color:#888; font-style:italic;">Specialist Fragrance Consultant</div>
        <a href="{link_wa}" target="_blank" class="wa-btn">FALAR NO WHATSAPP</a>
        <div style="margin-top:25px; color:#d4af37; font-weight:bold;">📞 (31) 99205-1499</div>
    </div>
</div>
""", unsafe_allow_html=True)
