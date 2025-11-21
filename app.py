import streamlit as st
import base64
import os
import re
from datetime import datetime
import pytz

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Aurum Scents",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. FUNÇÕES AUXILIARES (DATA) ---
def get_current_time():
    try:
        # Tenta pegar horário de SP/Brasil
        tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(tz)
        return now.strftime("%d.%m.%Y"), now.strftime("%H:%M")
    except:
        return datetime.now().strftime("%d.%m.%Y"), datetime.now().strftime("%H:%M")

# --- 3. CATÁLOGO ---
CATALOGO = {
    1: {"nome": "Angel Per F (100 ml)", "preco": 960.00, "desc": "Fragrância revolucionária e ousada, que combina notas doces, frutadas e sensuais com um fundo quente e envolvente."},
    2: {"nome": "Latafa Assad Bourbon (100 ml)", "preco": 470.00, "desc": "Oriental especiado quente, cremoso e bem envolvente — aquela vibe de noite fria, roupa escura e clima mais elegante."},
    3: {"nome": "Lattafa khamrah (100 ml)", "preco": 380.00, "desc": "Gourmand árabe bem cremoso, doce, quente e envolvente – lembra sobremesa sofisticada com especiarias e frutas secas.."},
    4: {"nome": "Fakhar Black (100 ml)", "preco": 380.00, "desc": "perfume âmbar aromático amadeirado, com cara de “cheiro de homem arrumado” 😄 – moderno, levemente adocicado, mas bem fresco e versátil."},
    5: {"nome": "L’Homme Lacoste (100 ml)", "preco": 380.00, "desc": "perfume amadeirado especiado fresco, com cara de homem arrumado, moderno e elegante – bem na linha “camisa social, tênis branco e relógio bonito” 😄."},
    6: {"nome": "Mercedes-Benz Black (100 ml)", "preco": 380.00, "desc": "Um perfume bem queridinho por quem gosta de baunilha cremosa com toque de incenso."},
    7: {"nome": "Silver Scent (100 ml)", "preco": 275.00, "desc": "Perfume oriental amadeirado bem marcante, com cara de perfume de balada/noite, daqueles que projetam e deixam rastro."},
    8: {"nome": "Scandal (80 ml)", "preco": 810.00, "desc": "Perfume chypre gourmand bem doce, melado e sensual, com cara de noite, festa e “mulher que quer chamar atenção. 😄"},
    9: {"nome": "Phantom Rabanne (100 ml)", "preco": 380.00, "desc": "Amadeirado aromático moderno, com cara de perfume de festa, balada e rolê noturno, mas que também dá pra usar no dia a dia se você curte algo mais chamativo."},
    10: {"nome": "Latafa Yara (10 ml)", "preco": 380.00, "desc": "um floral gourmand cremoso e atalcado, bem feminino, doce e confortável – tem cara de “cheiro de princesa”, aquele doce limpinho e aconchegant."},
    11: {"nome": "Phantom Paco Rabanne (100 ml)", "preco": 380.00, "desc": "amadeirado aromático moderno, com cheiro de lavanda cremosa com limão e baunilha – bem vibe balada/rolê, jovem e chamativo."},
    12: {"nome": "Club de Nuit Intense Man (100 ml)", "preco": 380.00, "desc": "amadeirado especiado com toques frutados cítricos, famoso por lembrar o estilo do Creed Aventus: cheiro de limão + abacaxi esfumaçado + madeiras + baunilh."},
    13: {"nome": "Animale Sexy (100 ml)", "preco": 380.00, "desc": "Floral frutado gourmand bem doce, cremoso e sensual, pensado pra aquela vibe mulher poderosa / femme fatale."},
    14: {"nome": "Calvin Klein Eternity (100 ml)", "preco": 430.00, "desc": "Um aromático fougère fresco e limpo, com aquela cara clássica de “cheiro de homem elegante, arrumado e discreto."}, 
    15: {"nome": "Miss Dior (100 ml)", "preco": 1040.00, "desc": "Um perfume floral âmbar romântico, elegante e bem feminino, com aquele ar de “bouquet de flores caro” e fundo cremosinho."},
    16: {"nome": "Olympea Rabanne (100 ml)", "preco": 380.00, "desc": "Um oriental floral com baunilha salgada, bem sensual, marcante e com cara de “deusa moderna” mesmo."},
}

# --- 4. CARREGAMENTO DE ARQUIVOS ---
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

# --- 5. INICIALIZAÇÃO ---
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

path_logo = os.path.join(path_base, "Logo.jpg")
if not os.path.exists(path_logo): path_logo = os.path.join(path_base, "Logo.png")
logo_b64 = get_img_as_base64(path_logo)
logo_src = f"data:image/jpeg;base64,{logo_b64}" if logo_b64 else ""

preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + (100 if preco_atual > 0 else 0)

# Dados Dinâmicos
data_hoje, hora_agora = get_current_time()

# --- 6. CSS DEFINITIVO ---
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
        font-size: 4rem; text-align: center; margin-bottom: 40px;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 10px rgba(0,0,0,0.8);
    }}

    /* LAYOUT */
    [data-testid="column"] {{ display: flex; flex-direction: column; justify-content: center; }}

    /* LOGOS LATERAIS */
    .side-logo-container {{ text-align: center; margin-bottom: 30px; }}
    .side-logo {{
        max-width: 130px;
        height: auto;
        filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.3));
    }}

    /* WIDGETS LATERAIS (Data/Apoio) */
    .widget-box {{
        margin-top: 20px; padding: 20px;
        border-top: 1px solid #333; border-bottom: 1px solid #333;
        text-align: center; color: #888; font-size: 0.9rem;
    }}
    .widget-title {{ color: #d4af37; font-family: 'Cinzel', serif; margin-bottom: 5px; font-size: 0.9rem; }}
    .widget-data {{ color: #fff; font-size: 1.1rem; letter-spacing: 1px; transition: 0.3s; }}
    .widget-data:hover {{ color: #d4af37; transform: scale(1.05); }}

    /* ESQUERDA */
    .left-panel {{ padding-right: 15px; border-right: 1px solid #333; text-align: justify; height: 100%; display: flex; flex-direction: column; justify-content: center; }}
    .panel-text {{ font-size: 1.1rem; color: #aaa; line-height: 1.7; margin-bottom: 20px; }}

    /* --- VISOR CENTRAL --- */
    .visor-wrapper {{
        position: relative; width: 100%; max-width: 900px;
        aspect-ratio: 16/9; margin: 0 auto 20px auto;
        background-image: {bg_visor_css}; background-size: cover; background-position: center;
        border-radius: 4px; box-shadow: 0 25px 50px rgba(0,0,0,0.9);
    }}
    
    .visor-mask {{
        position: absolute; top: 8%; left: 18.3%; width: 63.4%; height: 66%; 
        overflow: hidden; display: flex; align-items: flex-end; justify-content: center;
    }}

    .perfume-img {{
        height: 78%; width: auto;
        mix-blend-mode: multiply; filter: contrast(1.1) brightness(0.95);
        transition: transform 0.5s ease; margin-bottom: 4%;
        
        /* AJUSTE DE POSIÇÃO: 7% */
        margin-left: 7%; 
    }}
    .perfume-img:hover {{ transform: scale(1.75); mix-blend-mode: normal; }}

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
        background: linear-gradient(145deg, #111, #0a0a0a); padding: 35px; 
        border-radius: 10px; text-align: center; border: 1px solid #222;
        height: fit-content; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .wa-btn {{
        display: block; background: linear-gradient(45deg, #25d366, #128c7e); color: white;
        padding: 15px; border-radius: 50px; text-decoration: none; font-weight: bold; font-family: sans-serif;
        margin-top: 20px; transition: 0.3s; letter-spacing: 1px;
    }}
    .wa-btn:hover {{ transform: scale(1.05); color: white; box-shadow: 0 5px 15px rgba(37, 211, 102, 0.4); }}

    /* RODAPÉ */
    .final-footer {{
        text-align: center; margin-top: 60px; padding-top: 20px;
        border-top: 1px solid #222; color: #666; font-family: 'Playfair Display', serif; font-style: italic;
    }}
</style>
""", unsafe_allow_html=True)

# --- 7. ESTRUTURA DO LAYOUT ---
st.markdown('<div class="brand-title">AURUM SCENTS</div>', unsafe_allow_html=True)

col_L, col_C, col_R = st.columns([3, 6, 3], gap="small")

# ESQUERDA
with col_L:
    if logo_src:
        st.markdown(f"""<div class="side-logo-container"><img src="{logo_src}" class="side-logo"></div>""", unsafe_allow_html=True)
    
    # Widget de Apoio Digital (Substituindo Localização)
    st.markdown(f"""
    <div class="widget-box">
        <div class="widget-title">APOIO DIGITAL</div>
        <a href="https://www.instagram.com/helpdigitalti__bh/?igsh=MXc0dXJuZWFscTN6bA%3D%3D#" target="_blank" style="text-decoration:none;">
            <div class="widget-data" style="color: #d4af37; font-weight: bold;">Help Digital 🚀</div>
        </a>
    </div>
    """, unsafe_allow_html=True)
        
    st.markdown("""
    <div style="margin-top: 30px;">
        <h3 style="color:#d4af37; margin-bottom:20px;">A Essência do Luxo</h3>
        <p class="panel-text">Na Aurum Scents, a fragrância não é apenas um aroma, é uma assinatura invisível que define sua presença.</p>
        <p class="panel-text">Nossa curadoria busca os ingredientes mais raros do mundo para despertar os prazeres da fragrância em sua forma mais pura e sofisticada.</p>
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
        <div class="info-container" style="margin-top: 20px;">
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
    if logo_src:
        st.markdown(f"""<div class="side-logo-container"><img src="{logo_src}" class="side-logo"></div>""", unsafe_allow_html=True)

    # Widget de Data e Hora
    st.markdown(f"""
    <div class="widget-box">
        <div class="widget-title">DATA E HORA</div>
        <div class="widget-data">📅 {data_hoje} | 🕒 {hora_agora}</div>
    </div>
    """, unsafe_allow_html=True)

    msg = f"Olá Jerry! Tenho interesse no exclusivo {produto_atual['nome']}."
    link = f"https://wa.me/5531992051499?text={msg.replace(' ', '%20')}"
    
    st.markdown(f"""
    <div class="right-panel" style="margin-top: 30px;">
        <div style="color:#fff; margin-bottom:10px; letter-spacing:2px;">ATENDIMENTO EXCLUSIVO</div>
        <div class="contact-name" style="font-size:2rem; color:#d4af37; margin-bottom:5px;">JERRY</div>
        <div style="color:#888; font-size:0.9rem; font-style:italic;">Specialist Fragrance Consultant</div>
        <a href="{link}" target="_blank" class="wa-btn">FALAR NO WHATSAPP</a>
        <div style="margin-top:20px; color:#d4af37; font-weight:bold; letter-spacing:1px;">📞 (31) 99205-1499</div>
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
