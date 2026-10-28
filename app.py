import os
import sqlite3
import uuid
import streamlit as st

# Tenta importar folium para o mapa interativo
try:
    import folium
    from streamlit_folium import st_folium

    HAS_FOLIUM = True
except ImportError:
    HAS_FOLIUM = False

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Sabedoria Local | Conexão Sênior",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- DIRETÓRIO DE IMAGENS ---
IMAGE_DIR = "images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)


# --- CONFIGURAÇÃO OTIMIZADA DO BANCO DE DADOS COM CACHE ---
@st.cache_resource
def get_connection():
    return sqlite3.connect("sabedoria_local.db", check_same_thread=False)


conn = get_connection()
cursor = conn.cursor()

# Tabela de Mestres
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS mestres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        genero TEXT NOT NULL,
        idade INTEGER,
        bairro TEXT NOT NULL,
        categoria TEXT NOT NULL,
        experiencia TEXT NOT NULL,
        contato TEXT NOT NULL,
        foto_perfil TEXT
    )
"""
)
conn.commit()

# Tabela de Avaliações
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mestre_id INTEGER,
        nota INTEGER,
        comentario TEXT,
        FOREIGN KEY(mestre_id) REFERENCES mestres(id)
    )
"""
)
conn.commit()

# Migrações seguras de colunas
try:
    cursor.execute("ALTER TABLE mestres ADD COLUMN genero TEXT DEFAULT 'Masculino'")
    conn.commit()
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE mestres ADD COLUMN foto_perfil TEXT")
    conn.commit()
except sqlite3.OperationalError:
    pass

# Popula automaticamente com os profissionais de teste caso esteja vazio
cursor.execute("SELECT COUNT(*) FROM mestres")
if cursor.fetchone()[0] == 0:
    mestres_iniciais = [
        (
            "Carlos Eduardo Silveira",
            "Masculino",
            68,
            "Centro (Joaçaba)",
            "Construção, Reformas e Instalações",
            "Engenheiro Civil aposentado com 35 anos de experiência em laudos estruturais e pequenas reformas.",
            "49991112233",
            "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=200&q=80",
        ),
        (
            "Maria Helena Farias",
            "Feminino",
            64,
            "Fraron (Herval d'Oeste)",
            "Acompanhamento e Companhia (Idosos/Passeios)",
            "Aposentada dedicada, com excelente histórico em conversação, companhia e caminhadas leves.",
            "49992223344",
            "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80",
        ),
        (
            "João Batista de Souza",
            "Masculino",
            71,
            "Vila Kennedy (Joaçaba)",
            "Consertos e Marcenaria",
            "Marceneiro com 45 anos de ofício. Restauração de móveis antigos e pequenos reparos em casa.",
            "49993334455",
            "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80",
        ),
        (
            "Ana Lúcia Ramos",
            "Feminino",
            63,
            "Centro (Luzerna)",
            "Apoio Escolar, Alfabetização e Reforço",
            "Professora aposentada de Matemática e Física. Reforço escolar especializado e muita paciência.",
            "49994445566",
            "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80",
        ),
        (
            "Roberto Siqueira",
            "Masculino",
            67,
            "Anhangá (Joaçaba)",
            "Serviços Domésticos e Tarefas Práticas (Mercado/Farmácia)",
            "Disponível para ajudar nas compras do supermercado, farmácia e pequenas diligências na cidade.",
            "49995556677",
            "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80",
        ),
        (
            "Terezinha da Costa",
            "Feminino",
            66,
            "Jardim das Hortênsias",
            "Culinarista, Marmitas Caseiras e Pães",
            "Produção sob encomenda de bolos caseiros, pães, cucas e marmitas com gostinho de comida de vó.",
            "49996667788",
            "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=200&q=80",
        ),
        (
            "Clara Conceição Martins",
            "Feminino",
            63,
            "Centro (Joaçaba)",
            "Saúde, Enfermagem e Cuidado Geriátrico",
            "Enfermeira aposentada. Auxílio em aferição de pressão, controle de medicamentos e curativos.",
            "49997778899",
            "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80",
        ),
        (
            "Carmen Lúcia Bohn",
            "Feminino",
            65,
            "Centro (Joaçaba)",
            "Costura, Consertos e Artesanato",
            "Artesã especialista em tricô, crochê, ajustes de roupas e enxovais feitos à mão.",
            "49998889900",
            "https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?auto=format&fit=crop&w=200&q=80",
        ),
        (
            "Valdemar de Oliveira",
            "Masculino",
            72,
            "Santa Terezinha",
            "Consertos e Marcenaria",
            "Relojoeiro e restaurador de relógios antigos. Precisão em pequenos mecanismos e caixas de música.",
            "49991234567",
            "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?auto=format&fit=crop&w=200&q=80",
        ),
        (
            "Irene Zortea",
            "Feminino",
            62,
            "Flor da Serra",
            "Jardinagem e Cuidados com Plantas",
            "Jardinagem afetiva, podas leves e consultoria de plantas ornamentais para residências.",
            "49997654321",
            "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?auto=format&fit=crop&w=200&q=80",
        ),
    ]
    cursor.executemany(
        """
        INSERT INTO mestres (nome, genero, idade, bairro, categoria, experiencia, contato, foto_perfil)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        mestres_iniciais,
    )
    conn.commit()

    cursor.executemany(
        """
        INSERT INTO avaliacoes (mestre_id, nota, comentario)
        VALUES (?, ?, ?)
    """,
        [
            (1, 5, "Ótimo atendimento e profissional exemplar."),
            (1, 5, "Serviço impecável e pontual."),
            (2, 5, "Muito atenciosa e carinhosa com minha mãe."),
            (3, 4, "Excelente trabalho em marcenaria."),
        ],
    )
    conn.commit()

# --- LISTA DE CATEGORIAS ---
LISTA_CATEGORIAS = [
    "Acompanhamento e Companhia (Idosos/Passeios)",
    "Saúde, Enfermagem e Cuidado Geriátrico",
    "Serviços Domésticos e Tarefas Práticas (Mercado/Farmácia)",
    "Culinarista, Marmitas Caseiras e Pães",
    "Apoio Escolar, Alfabetização e Reforço",
    "Construção, Reformas e Instalações",
    "Consertos e Marcenaria",
    "Costura, Consertos e Artesanato",
    "Organização de Lares e Documentos",
    "Jardinagem e Cuidados com Plantas",
    "Outras Orientações e Consultorias",
]

# --- ESTILIZAÇÃO CSS (CORREÇÃO TOTAL DE CONTRASTE NAS ABAS) ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff;
        color: #2d3748;
    }
    .block-container {
        padding-top: 3.5rem !important;
    }
    h1, h2, h3 {
        font-family: 'Georgia', serif;
        color: #1a365d;
    }
    
    label p, .stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label, .stFileUploader label {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    input, textarea, select, div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border-color: #cbd5e1 !important;
        border-radius: 8px !important;
    }
    input:focus, textarea:focus, div[data-baseweb="select"] > div:focus-within {
        border-color: #16a34a !important;
        box-shadow: 0 0 0 2px rgba(22, 163, 74, 0.15) !important;
    }

    /* CORREÇÃO DEFINITIVA DO TEXTO DAS ABAS (TABS) PARA ALTO CONTRASTE */
    div[data-baseweb="tab-list"] button p {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    div[data-baseweb="tab-list"] button[aria-selected="true"] p {
        color: #16a34a !important;
        font-weight: 700 !important;
    }
    div[data-baseweb="tab-list"] button[aria-selected="true"]::after {
        border-bottom-color: #16a34a !important;
    }

    [data-testid="stFileUploader"] {
        background-color: #f8fafc !important;
        border: 2px dashed #cbd5e1 !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    [data-testid="stFileUploader"] section {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small, [data-testid="stFileUploader"] div {
        color: #334155 !important;
    }

    div.stButton > button {
        background-color: #f8fafc !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
        padding: 0.4rem 0.2rem !important;
        font-size: 0.9rem !important;
    }
    div.stButton > button:hover {
        background-color: #f0fdf4 !important;
        border-color: #16a34a !important;
        color: #166534 !important;
    }

    .hero-card-visual {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        padding: 35px 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1e3a8a;
        margin: 5px 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
    }

    .card-mestre {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04);
        margin-bottom: 25px;
        transition: all 0.3s ease;
    }
    .card-mestre:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.08);
        border-color: #86efac;
    }
    .card-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 16px;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 12px;
    }
    .avatar-img {
        width: 70px;
        height: 70px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #16a34a;
    }
    .badge-senior {
        background-color: #f0fdf4;
        color: #166534;
        font-size: 11px;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 4px;
        border: 1px solid #bbf7d0;
    }
    .btn-whatsapp {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background-color: #16a34a;
        color: white !important;
        text-decoration: none;
        padding: 10px 16px;
        border-radius: 10px;
        font-weight: 600;
        font-size: 14px;
        width: 100%;
        margin-top: 15px;
        box-shadow: 0 4px 6px rgba(22, 163, 74, 0.2);
    }
    .btn-whatsapp:hover {
        background-color: #15803d;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- CABEÇALHO COM LOGO E MENU DE BOTÕES SUPERIORES (NOMES OTIMIZADOS) ---
col_logo, col_b1, col_b2, col_b3, col_b4, col_b5, col_b6, col_b7 = st.columns(
    [2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
)

with col_logo:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 2.2rem;">🌿</span>
            <div>
                <h1 style="margin: 0; font-size: 1.7rem; color: #166534;">Sabedoria Local</h1>
                <p style="margin: 0; font-size: 0.8rem; color: #4b5563; letter-spacing: 1px;">CONEXÃO SÊNIOR • JOAÇABA</p>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

if "menu_ativo" not in st.session_state:
    st.session_state.menu_ativo = "🏠 Início"

with col_b1:
    if st.button("🏠 Início", use_container_width=True):
        st.session_state.menu_ativo = "🏠 Início"
with col_b2:
    if st.button("🔍 Buscar", use_container_width=True):
        st.session_state.menu_ativo = "🔍 Buscar"
with col_b3:
    if st.button("➕ Cadastrar", use_container_width=True):
        st.session_state.menu_ativo = "➕ Cadastrar"
with col_b4:
    if st.button("📋 Listar", use_container_width=True):
        st.session_state.menu_ativo = "📋 Listar"
with col_b5:
    if st.button("⭐ Avaliar", use_container_width=True):
        st.session_state.menu_ativo = "⭐ Avaliar"
with col_b6:
    if st.button("🗺️ Mapa", use_container_width=True):
        st.session_state.menu_ativo = "🗺️ Mapa"
with col_b7:
    if st.button("📊 Painel", use_container_width=True):
        st.session_state.menu_ativo = "📊 Painel"

st.write("---")

cursor.execute("SELECT COUNT(*) FROM mestres")
total_cadastrados = cursor.fetchone()[0]

menu = st.session_state.menu_ativo


# ==========================================
# FUNÇÃO render_card() COM URL PURA E SQL LIMPO
# ==========================================
def render_card(
    mestre_id,
    nome,
    idade,
    genero,
    bairro,
    categoria,
    experiencia,
    contato,
    foto_perfil,
):
    if foto_perfil:
        if not foto_perfil.startswith("http") and os.path.exists(
            os.path.join(IMAGE_DIR, foto_perfil)
        ):
            img_src = os.path.join(IMAGE_DIR, foto_perfil)
        else:
            img_src = foto_perfil
    else:
        img_src = (
            "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80"
            if genero == "Feminino"
            else "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=200&q=80"
        )

    cursor.execute(
        """
        SELECT AVG(nota), COUNT(*)
        FROM avaliacoes
        WHERE mestre_id = ?
    """,
        (mestre_id,),
    )
    res_av = cursor.fetchone()
    media_nota = res_av[0] if res_av and res_av[0] is not None else 5.0
    total_av = res_av[1] if res_av and res_av[1] is not None else 0

    cursor.execute(
        """
        SELECT comentario
        FROM avaliacoes
        WHERE mestre_id = ?
        ORDER BY id DESC
        LIMIT 1
    """,
        (mestre_id,),
    )
    res_com = cursor.fetchone()
    comentario_recente = (
        res_com[0] if res_com and res_com[0] else "Excelente profissional."
    )

    estrelas = "⭐" * int(round(media_nota))

    numero = "".join(filter(str.isdigit, contato))
    link_zap = (
        f"https://wa.me/55{numero}"
        f"?text=Olá%20{nome},%20encontrei%20seu%20perfil%20no%20portal%20Sabedoria%20Local."
    )

    st.markdown(
        f"""
        <div class="card-mestre">
            <div class="card-header">
                <img src="{img_src}" class="avatar-img">
                <div>
                    <h3 style="margin: 0; font-size: 18px; color: #1e293b;">{nome}, {idade} anos</h3>
                    <span class="badge-senior">⭐ Mestre Especialista Verificado</span>
                    <p style="margin: 4px 0 0 0; font-size: 13px; color: #64748b;">📍 {bairro}</p>
                </div>
            </div>
            <div style="font-size: 14px; color: #16a34a; font-weight: bold; margin-bottom: 6px;">
                {estrelas} {round(media_nota, 1)} <span style="font-size: 12px; color: #64748b; font-weight: normal;">({total_av} avaliações)</span>
            </div>
            <div style="font-size: 14px; color: #334155; margin-bottom: 8px;"><b>🛠️ Categoria:</b> {categoria}</div>
            <div style="
                background:#f8fafc;
                padding:10px;
                border-radius:8px;
                border-left:3px solid #16a34a;
                margin-top:6px;
                font-size: 13px;
                color: #475569;
            ">
                "{experiencia}"
            </div>
            <div style="font-size: 12px; color: #64748b; margin-top: 8px; font-style: italic;">
                💬 "{comentario_recente}"
            </div>
            <a href="{link_zap}" target="_blank" class="btn-whatsapp">
                💬 Conversar pelo WhatsApp
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================
# ABA 0: INÍCIO / APRESENTAÇÃO E SOBRE O PROJETO
# ==========================================
if menu == "🏠 Início":
    col_img, col_txt = st.columns([1, 1.3], vertical_alignment="center")

    with col_img:
        st.markdown(
            """
            <div class="hero-card-visual">
                <span style="font-size: 3rem;">🧓👵</span>
                <h3 style="color: #166534; margin: 15px 0 10px 0;">Longevidade Ativa</h3>
                <p style="color: #15803d; font-size: 0.95rem; margin: 0; line-height: 1.5;">
                    "Envelhecer com autonomia, dignidade, gerando renda extra e transmitindo conhecimento para as novas gerações."
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col_txt:
        st.markdown(
            """
            <div style="padding-left: 10px;">
                <h4 style="color: #16a34a; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 1.5px; margin-bottom: 5px;">CONFORTO, DIGNIDADE & PROPÓSITO</h4>
                <h2 style="font-size: 2.2rem; color: #1a365d; margin-top: 0; line-height: 1.2;">Uma ponte de respeito entre a sabedoria sênior e a nossa comunidade</h2>
                <p style="color: #4b5563; font-size: 1.05rem; line-height: 1.6;">
                    Com acessibilidade simples e foco na <b>economia prateada</b>, conectamos profissionais aposentados que desejam se manter ativos a famílias e vizinhos em Joaçaba e região que buscam serviços de confiança.
                </p>
                <p style="color: #4b5563; font-size: 1.05rem; line-height: 1.6;">
                    <b>Idosos ativos possuem melhor qualidade de vida, autonomia e bem-estar.</b> Aqui, cada ano de experiência é valorizado.
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.write("---")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Mestres Cadastrados</div>
                <div class="metric-value">{total_cadastrados} Profissionais</div>
                <div style="font-size: 0.8rem; color: #16a34a; margin-top: 4px;">↑ Ativos na Região</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Abrangência Regional</div>
                <div class="metric-value">Joaçaba & Região</div>
                <div style="font-size: 0.8rem; color: #16a34a; margin-top: 4px;">↑ Herval / Luzerna</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Propósito Social</div>
                <div class="metric-value">Economia Prateada</div>
                <div style="font-size: 0.8rem; color: #16a34a; margin-top: 4px;">↑ Longevidade Ativa</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.write("---")

    st.markdown("### 📚 Sobre o Projeto & Fundamentação Acadêmica")
    st.write(
        "Este sistema foi desenvolvido como parte da Prática Profissional e Inserção Comunitária, unindo tecnologia e impacto social real."
    )

    t1, t2, t3 = st.tabs(
        ["🥈 Economia Prateada", "🌍 ODS da ONU", "🎯 Objetivo Social"]
    )

    with t1:
        st.markdown(
            """
            #### O que é a Economia Prateada?
            A **Economia Prateada** engloba o mercado gerado pelo envelhecimento demográfico e a crescente parcela da população com 60 anos ou mais. 
            Em Joaçaba e região, a terceira idade representa um patrimônio humano inestimável. O projeto **Sabedoria Local** enxerga este público não como passivo, mas como agentes ativos de inovação social, geradores de renda e pilares de sabedoria prática.
        """
        )

    with t2:
        st.markdown(
            """
            #### Alinhamento com os Objetivos de Desenvolvimento Sustentável (ODS)
            * **ODS 8 - Trabalho Decente e Crescimento Econômico:** Promover políticas sustentáveis que apoiem a atividade produtiva, a geração de renda e a inclusão de trabalhadores seniores no mercado local.
            * **ODS 10 - Redução das Desigualdades:** Combater o isolamento social, a exclusão digital e etária, garantindo igualdade de oportunidades para idosos ativos que desejam continuar contribuindo com a sociedade.
        """
        )

    with t3:
        st.markdown(
            """
            #### Impacto Comunitário em Joaçaba e Região
            * **Para os Mestres (Seniores):** Resgate da autoestima, complementação de renda e manutenção do protagonismo social.
            * **Para a Comunidade:** Acesso facilitado a serviços de altíssima confiança, realizados por profissionais experientes de Joaçaba, Herval d'Oeste e Luzerna.
        """
        )


# ==========================================
# ABA 1: BUSCAR ESPECIALISTA
# ==========================================
elif menu == "🔍 Buscar":
    st.markdown("### 🔍 Encontre o Profissional Ideal na Região")
    st.write(
        "Selecione a categoria desejada ou informe o bairro para localizar um especialista sênior próximo a você."
    )

    col1, col2 = st.columns(2)
    with col1:
        categorias_filtro = ["Todas as Categorias"] + LISTA_CATEGORIAS
        filtro_cat = st.selectbox("Filtrar por Categoria:", categorias_filtro)
    with col2:
        filtro_bairro = st.text_input(
            "Filtrar por Bairro (Ex: Centro, Herval):"
        )

    if st.button(
        "🔍 Pesquisar Especialistas", type="primary", use_container_width=True
    ):
        query = "SELECT id, nome, idade, genero, bairro, categoria, experiencia, contato, foto_perfil FROM mestres WHERE 1=1"
        params = []

        if filtro_cat != "Todas as Categorias":
            query += " AND categoria = ?"
            params.append(filtro_cat)

        if filtro_bairro:
            query += " AND bairro LIKE ?"
            params.append(f"%{filtro_bairro}%")

        cursor.execute(query, params)
        resultados = cursor.fetchall()

        st.write("---")
        if resultados:
            st.success(
                f"Encontramos **{len(resultados)}** especialista(s) disponível(eis) para atendimento."
            )
            cols = st.columns(3)
            for i, r in enumerate(resultados):
                m_id, nome, idade, genero, bairro, cat, exp, contato, foto = r
                with cols[i % 3]:
                    render_card(
                        m_id,
                        nome,
                        idade,
                        genero,
                        bairro,
                        cat,
                        exp,
                        contato,
                        foto,
                    )
        else:
            st.warning(
                "Nenhum profissional encontrado com esses filtros na região."
            )

# ==========================================
# ABA 2: CADASTRAR COMO MESTRE (COM UUID ANTI-SOBRESCRIÇÃO)
# ==========================================
elif menu == "➕ Cadastrar":
    st.markdown("### ➕ Seja um Mestre na Rede Sabedoria Local")
    st.info(
        "✨ Requisito legal de idade: Mulheres (62 anos ou mais) | Homens (65 anos ou mais). Mantenha-se ativo, gere renda extra e compartilhe sua história com a comunidade de Joaçaba!"
    )
    st.write("---")

    with st.form("form_cadastro_institucional"):
        col_f1, col_f2 = st.columns(2)

        with col_f1:
            nome_input = st.text_input("Nome Completo:")
            genero_input = st.selectbox("Sexo:", ["Feminino", "Masculino"])
            idade_input = st.number_input(
                "Sua Idade:", min_value=40, max_value=110, value=65
            )
            bairro_input = st.text_input(
                "Bairro em Joaçaba ou Região (Ex: Centro):"
            )

        with col_f2:
            cat_input = st.selectbox(
                "Área de Atuação Principal:", LISTA_CATEGORIAS
            )
            exp_input = st.text_area(
                "Resumo da Experiência Profissional:",
                placeholder="Ex: Aposentada, ofereço companhia, conversas e auxílio em tarefas do dia a dia...",
                height=100,
            )
            contato_input = st.text_input(
                "WhatsApp de Contato (Com DDD, ex: 49999999999):"
            )
            foto_arquivo = st.file_uploader(
                "Escolha a foto de perfil (Opcional):",
                type=["png", "jpg", "jpeg"],
            )

        st.write("---")
        enviar = st.form_submit_button(
            "Validar e Concluir Meu Cadastro", type="primary"
        )

        if enviar:
            idade_valida = True
            if genero_input == "Feminino" and idade_input < 62:
                idade_valida = False
                msg = "Para o cadastro feminino, a idade mínima é de 62 anos."
            elif genero_input == "Masculino" and idade_input < 65:
                idade_valida = False
                msg = "Para o cadastro masculino, a idade mínima é de 65 anos."

            if not idade_valida:
                st.error(f"⚠️ {msg}")
            elif nome_input and bairro_input and exp_input and contato_input:
                caminho_foto = None
                if foto_arquivo is not None:
                    nome_arquivo = f"{uuid.uuid4()}_{foto_arquivo.name}"
                    caminho_foto = os.path.join(IMAGE_DIR, nome_arquivo)
                    with open(caminho_foto, "wb") as f:
                        f.write(foto_arquivo.getbuffer())
                    caminho_foto = nome_arquivo

                cursor.execute(
                    """
                    INSERT INTO mestres (nome, genero, idade, bairro, categoria, experiencia, contato, foto_perfil)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        nome_input,
                        genero_input,
                        idade_input,
                        bairro_input,
                        cat_input,
                        exp_input,
                        contato_input,
                        caminho_foto,
                    ),
                )
                conn.commit()
                st.success(
                    "🎉 Cadastro realizado com sucesso! Você já faz parte da nossa rede de mestres."
                )
            else:
                st.error("Por favor, preencha todos os campos obrigatórios.")

# ==========================================
# ABA 3: LISTAR TODOS OS MESTRES
# ==========================================
elif menu == "📋 Listar":
    st.markdown("### 📋 Diretório Completo de Especialistas na Região")
    st.write(
        "Conheça todos os profissionais seniores cadastrados prontos para ajudar a comunidade."
    )

    cursor.execute(
        "SELECT id, nome, idade, genero, bairro, categoria, experiencia, contato, foto_perfil FROM mestres"
    )
    todos = cursor.fetchall()

    if todos:
        cols = st.columns(3)
        for i, r in enumerate(todos):
            m_id, nome, idade, genero, bairro, cat, exp, contato, foto = r
            with cols[i % 3]:
                render_card(
                    m_id, nome, idade, genero, bairro, cat, exp, contato, foto
                )
    else:
        st.info("Ainda não há profissionais cadastrados.")

# ==========================================
# ABA 4: AVALIAR UM MESTRE
# ==========================================
elif menu == "⭐ Avaliar":
    st.markdown("### ⭐ Avalie o Atendimento de um Mestre")
    st.write(
        "Deixe sua nota e comentário para ajudar a manter a excelência e confiança na comunidade."
    )
    st.write("---")

    cursor.execute("SELECT id, nome, categoria, bairro FROM mestres")
    lista_mestres = cursor.fetchall()

    if lista_mestres:
        dict_mestres = {
            f"{m[1]} ({m[2]} - {m[3]})": m[0] for m in lista_mestres
        }
        escolha_mestre = st.selectbox(
            "Selecione o Profissional:", list(dict_mestres.keys())
        )
        mestre_selecionado_id = dict_mestres[escolha_mestre]

        with st.form("form_avaliacao"):
            nota_input = st.slider(
                "Nota (de 1 a 5 estrelas):", min_value=1, max_value=5, value=5
            )
            comentario_input = st.text_area(
                "Comentário / Depoimento:",
                placeholder="Ex: Ótimo atendimento, muito pontual e atencioso...",
            )

            enviar_av = st.form_submit_button(
                "Enviar Avaliação", type="primary"
            )

            if enviar_av:
                if comentario_input:
                    cursor.execute(
                        "INSERT INTO avaliacoes (mestre_id, nota, comentario) VALUES (?, ?, ?)",
                        (mestre_selecionado_id, nota_input, comentario_input),
                    )
                    conn.commit()
                    st.success(
                        "⭐ Avaliação registrada com sucesso! Obrigado por fortalecer nossa rede."
                    )
                else:
                    st.error("Por favor, preencha o comentário.")
    else:
        st.info("Não há mestres cadastrados para avaliar.")

# ==========================================
# ABA 5: MAPA INTERATIVO DE ATENDIMENTO
# ==========================================
elif menu == "🗺️ Mapa":
    st.markdown("### 🗺️ Mapa de Atendimento Regional")
    st.write(
        "Visualize a distribuição geográfica dos profissionais cadastrados em Joaçaba e região."
    )
    st.write("---")

    if HAS_FOLIUM:
        coordenadas_bairros = {
            "Centro": [-27.1775, -51.5033],
            "Fraron": [-27.1850, -51.5150],
            "Vila Kennedy": [-27.1700, -51.4950],
            "Anhangá": [-27.1650, -51.5100],
            "Santa Terezinha": [-27.1900, -51.4900],
            "Flor da Serra": [-27.1750, -51.5200],
            "Minas Brasil": [-27.1800, -51.4850],
            "Herval d'Oeste": [-27.1833, -51.4833],
            "Luzerna": [-27.1261, -51.4697],
            "Cruzeiro do Sul": [-27.1720, -51.5050],
            "Jardim das Hortênsias": [-27.1680, -51.5120],
            "Vila Corduta": [-27.1810, -51.4980],
        }

        mapa_joacaba = folium.Map(
            location=[-27.1775, -51.5033],
            zoom_start=14,
            tiles="CartoDB positron",
        )

        cursor.execute("SELECT nome, bairro, categoria, contato FROM mestres")
        registros_mapa = cursor.fetchall()

        for nome, bairro, cat, contato in registros_mapa:
            coords = [-27.1775, -51.5033]
            for b_chave, b_val in coordenadas_bairros.items():
                if b_chave.lower() in bairro.lower():
                    coords = b_val
                    break

            folium.Marker(
                location=coords,
                popup=f"<b>{nome}</b><br>🛠️ {cat}<br>📍 {bairro}",
                tooltip=nome,
                icon=folium.Icon(color="green", icon="user", prefix="fa"),
            ).add_to(mapa_joacaba)

        st_folium(mapa_joacaba, width=1100, height=500)
    else:
        st.info(
            "Biblioteca `folium` e `streamlit-folium` não detectadas. Exibindo lista de bairros atendidos:"
        )
        cursor.execute("SELECT DISTINCT bairro FROM mestres")
        bairros = cursor.fetchall()
        for b in bairros:
            st.write(f"📍 {b[0]}")

# ==========================================
# ABA 6: PAINEL / INDICADORES
# ==========================================
elif menu == "📊 Painel":
    st.markdown("### 📊 Painel de Indicadores da Economia Prateada")
    st.write(
        "Métricas e análises em tempo real do ecossistema de longevidade ativa em Joaçaba e região."
    )
    st.write("---")

    cursor.execute("SELECT idade, categoria, bairro FROM mestres")
    dados_mestres = cursor.fetchall()

    if dados_mestres:
        total_m = len(dados_mestres)
        soma_idades = sum([row[0] for row in dados_mestres if row[0]])
        media_idade = round(soma_idades / total_m, 1) if total_m > 0 else 0

        cat_counts = {}
        bairro_counts = {}
        for idade, cat, bairro in dados_mestres:
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
            bairro_counts[bairro] = bairro_counts.get(bairro, 0) + 1

        d1, d2, d3 = st.columns(3)
        with d1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Total de Mestres</div>
                    <div class="metric-value">{total_m} Profissionais</div>
                    <div style="font-size: 0.8rem; color: #16a34a; margin-top: 4px;">Ativos na plataforma</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with d2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Média de Idade</div>
                    <div class="metric-value">{media_idade} Anos</div>
                    <div style="font-size: 0.8rem; color: #16a34a; margin-top: 4px;">Experiência comprovada</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        with d3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Áreas de Atuação</div>
                    <div class="metric-value">{len(cat_counts)} Categorias</div>
                    <div style="font-size: 0.8rem; color: #16a34a; margin-top: 4px;">Serviços diversificados</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.write("---")

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("#### 🛠️ Profissionais por Categoria")
            st.bar_chart(cat_counts)

        with col_g2:
            st.markdown("#### 📍 Concentração por Bairro")
            st.bar_chart(bairro_counts)
    else:
        st.info("Ainda não há dados suficientes para gerar o dashboard.")

# --- RODAPÉ INSTITUCIONAL ---
st.write("---")
st.markdown(
    """
    <div style="text-align: center; color: #6b7280; font-size: 0.9rem; padding: 20px 0;">
        <p><b>Sabedoria Local — Conexão Sênior Joaçaba</b></p>
        <p style="font-size: 0.8rem; color: #9ca3af;">Promovendo a Economia Prateada, a Longevidade Ativa e a Inclusão Social na Região.</p>
    </div>
""",
    unsafe_allow_html=True,
)