import streamlit as st

from .media import image_to_base64, pil_image_to_data_uri
from .settings import LOGO_PATH


def render_mobo_shell():
    logo_base64 = image_to_base64(LOGO_PATH)
    logo_html = (
        f'<img src="data:image/png;base64,{logo_base64}" class="mobo-logo" alt="MOBO">'
        if logo_base64
        else '<div class="mobo-logo-text">mobo</div>'
    )
    menu_items = [
        ("⌂", "Home"),
        ("⚙", "Braço Mecânico"),
        ("✦", "Análise IA"),
        ("◔", "Dashboard"),
        ("⌁", "Sensores"),
        ("▤", "Relatórios"),
        ("●", "Alertas"),
        ("☼", "Previsão Colheita"),
        ("◉", "Perfil"),
        ("⊕", "Terreno"),
        ("↳", "Logout"),
    ]
    menu_html = "".join(
        f'<div class="mobo-nav-item"><span>{icon}</span><strong>{label}</strong></div>'
        for icon, label in menu_items
    )
    st.markdown(
        f"""
        <aside class="mobo-sidebar">
            <div class="mobo-logo-wrap">{logo_html}</div>
            <nav class="mobo-nav">{menu_html}</nav>
        </aside>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        """
        <header class="mobo-header">
            <div>
                <div class="eyebrow">MOBO IA</div>
                <h1>Identificação de Maturação</h1>
            </div>
            <div class="top-actions" aria-label="Ações rápidas">
                <div class="theme-toggle" aria-label="Alternar tema">
                    <span class="theme-symbol">
                        <svg viewBox="0 0 24 24" aria-hidden="true">
                            <circle cx="12" cy="12" r="3.7"></circle>
                            <path d="M12 2.6v2M12 19.4v2M5.4 5.4l1.45 1.45M17.15 17.15l1.45 1.45M2.6 12h2M19.4 12h2M5.4 18.6l1.45-1.45M17.15 6.85l1.45-1.45"></path>
                        </svg>
                    </span>
                    <span class="theme-thumb"></span>
                    <span class="theme-symbol dark">
                        <svg viewBox="0 0 24 24" aria-hidden="true">
                            <path d="M20.2 15.6A7.9 7.9 0 0 1 8.4 3.8a6.5 6.5 0 1 0 11.8 11.8Z"></path>
                        </svg>
                    </span>
                </div>
                <div class="top-icon profile-icon" aria-label="Perfil">
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <circle cx="12" cy="8.2" r="3.3"></circle>
                        <path d="M5.2 20.2c.85-3.65 3.25-5.5 6.8-5.5s5.95 1.85 6.8 5.5"></path>
                    </svg>
                </div>
                <div class="top-icon notification-icon" aria-label="Notificações">
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M18 9.4a6 6 0 0 0-12 0c0 5.4-2.2 6.45-3 8.15h18c-.8-1.7-3-2.75-3-8.15"></path>
                        <path d="M14.3 20.2a2.55 2.55 0 0 1-4.6 0"></path>
                    </svg>
                    <span class="notification-dot"></span>
                </div>
            </div>
        </header>
        """,
        unsafe_allow_html=True,
    )


def render_example_buttons(examples):
    st.markdown('<div class="section-title compact">Teste rápido</div>', unsafe_allow_html=True)
    example_cols = st.columns(3)

    with example_cols[0]:
        if "Exemplo madura" in examples and st.button("Usar exemplo madura", width="stretch"):
            st.session_state.selected_example = examples["Exemplo madura"]
            st.session_state.selected_analysis_index = 0

    with example_cols[1]:
        if "Exemplo não madura" in examples and st.button("Usar exemplo não madura", width="stretch"):
            st.session_state.selected_example = examples["Exemplo não madura"]
            st.session_state.selected_analysis_index = 0

    with example_cols[2]:
        if st.button("Remover exemplo selecionado", width="stretch"):
            st.session_state.selected_example = None
            st.session_state.selected_analysis_index = 0


def render_image_card(image, title, caption=None, card_class="visual-card"):
    caption_html = f'<div class="image-caption">{caption}</div>' if caption else ""
    st.markdown(
        f"""
        <div class="mobo-card {card_class}">
            <div class="visual-card-title">{title}</div>
            <div class="image-frame">
                <img src="{pil_image_to_data_uri(image)}" alt="{title}">
            </div>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
