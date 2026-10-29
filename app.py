import streamlit as st

st.set_page_config(
    page_title="Mobo - Análise de Lichias",
    page_icon="🍒",
    layout="wide",
)

# Esta configuração precisa acontecer antes de importar módulos do painel.
from dashboard.analysis import analyze_image, get_example_images, load_model
from dashboard.history import (
    build_selected_images,
    init_session_state,
    register_history_once,
)
from dashboard.media import load_css
from dashboard.layout import (
    render_example_buttons,
    render_header,
    render_image_card,
    render_mobo_shell,
)
from dashboard.history_ui import render_history_section
from dashboard.results import (
    render_comparison_cards,
    render_detailed_result,
    render_detailed_visualization,
    render_export_section,
)

load_css()
init_session_state()

model = load_model()
examples = get_example_images()

render_mobo_shell()
render_header()

workspace_col, result_col = st.columns([1.04, 0.96], gap="large")

with workspace_col:
    st.markdown(
        """
        <div class="mobo-card upload-intro">
            <div class="card-kicker">Entrada de imagem</div>
            <h2>Envie uma lichia para análise</h2>
            <p>Use uma foto em JPG ou PNG. A IA mantém a análise original e aplica apenas um limite visual na confiança exibida.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_files = st.file_uploader(
        "Escolha uma ou mais imagens",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )
    render_example_buttons(examples)

selected_images = build_selected_images(uploaded_files)
analysis_results = []
primary_result = None

if selected_images:
    analysis_results = [
        analyze_image(item["image"], item["name"], model)
        for item in selected_images
    ]
    primary_result = analysis_results[st.session_state.selected_analysis_index]
    register_history_once(primary_result)

with workspace_col:
    if selected_images and primary_result:
        st.markdown('<div class="section-title compact">Preview selecionado</div>', unsafe_allow_html=True)
        render_image_card(
            primary_result["processed_image"],
            "Imagem selecionada",
            primary_result["file_name"],
            "preview-card",
        )
    else:
        st.markdown(
            """
            <div class="mobo-card empty-upload">
                <div class="empty-icon">+</div>
                <strong>Aguardando imagem</strong>
                <span>O resultado aparece ao lado assim que uma foto for enviada ou um exemplo for escolhido.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

with result_col:
    if primary_result:
        render_detailed_result(primary_result)
    else:
        st.markdown(
            """
            <div class="mobo-card result-placeholder">
                <div class="card-kicker">Resultado da análise</div>
                <h2>Classe prevista</h2>
                <div class="confidence-placeholder">--.--%</div>
                <p>O painel mostrará maturação, confiança e mensagem explicativa sem alterar a resposta real do modelo.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

if analysis_results:
    if len(analysis_results) > 1:
        render_comparison_cards(analysis_results)
    render_detailed_visualization(primary_result)
    render_export_section(primary_result)

render_history_section()
