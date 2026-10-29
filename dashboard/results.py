from datetime import datetime

import streamlit as st

from .layout import render_image_card
from .media import pil_image_to_data_uri
from .reports import make_report_image, pil_to_pdf_bytes, pil_to_png_bytes


def render_comparison_cards(analysis_results):
    st.markdown('<div class="section-title">Comparação das análises</div>', unsafe_allow_html=True)

    num_columns = min(len(analysis_results), 3)
    comparison_cols = st.columns(num_columns)

    for index, result in enumerate(analysis_results):
        col = comparison_cols[index % num_columns]
        with col:
            st.markdown(
                f"""
                <div class="mobo-card comparison-shell">
                    <div class="image-frame compact">
                        <img src="{pil_image_to_data_uri(result['processed_image'])}" alt="{result['file_name']}">
                    </div>
                    <div class="comparison-image-caption">{result['file_name']}</div>
                    <div class="comparison-card" style="border-left: 6px solid {result['style']['border']};">
                        <div class="comparison-title" style="color:{result['style']['border']};">
                            {result['predicted_class']}
                        </div>
                        <div class="comparison-text">
                            <strong>Confiança:</strong> {result['display_confidence']:.2%}<br>
                            {result['prediction_text']}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "Ver análise detalhada",
                key=f"select_analysis_{index}",
                width="stretch"
            ):
                st.session_state.selected_analysis_index = index
                st.rerun()

            if st.session_state.selected_analysis_index == index:
                st.markdown(
                    '<div class="selected-chip">Análise selecionada</div>',
                    unsafe_allow_html=True
                )


def render_detailed_result(primary_result):
    st.markdown(
        f"""
        <div class="mobo-card result-card" style="background-color:{primary_result['style']['bg']}; border-color:{primary_result['style']['border']};">
            <div class="card-kicker">Resultado da análise</div>
            <div class="result-title" style="color:{primary_result['style']['border']};">{primary_result['style']['title']}</div>
            <div class="result-text">
                <strong>Arquivo:</strong> {primary_result['file_name']}<br>
                <strong>Classe prevista:</strong> {primary_result['predicted_class']}<br>
                <strong>Confiança:</strong> {primary_result['display_confidence']:.2%}<br><br>
                {primary_result['prediction_text']}<br>
                {primary_result['style']['text']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_metric1, col_metric2 = st.columns(2)

    with col_metric1:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Classe prevista</div>
                <div class="metric-value">{primary_result['predicted_class']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_metric2:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Confiança</div>
                <div class="metric-value">{primary_result['display_confidence']:.2%}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.progress(float(primary_result["display_confidence"]))


def render_detailed_visualization(primary_result):
    st.markdown('<div class="section-title">Visualização detalhada</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        render_image_card(
            primary_result["processed_image"],
            "Preview",
            primary_result["file_name"],
            "visual-card",
        )

    with col2:
        render_image_card(
            primary_result["heatmap_image"],
            "Heatmap",
            "Atenção visual da IA",
            "visual-card",
        )

    with st.expander("Como interpretar o heatmap"):
        st.write(
            "O heatmap destaca as regiões da imagem que mais influenciaram a decisão do modelo. "
            "Áreas mais quentes tendem a indicar onde a rede concentrou mais atenção para classificar a lichia."
        )


def render_export_section(primary_result):
    st.markdown('<div class="section-title">Exportação</div>', unsafe_allow_html=True)

    report_image = make_report_image(
        original_image=primary_result["processed_image"],
        heatmap_image=primary_result["heatmap_image"],
        predicted_class=primary_result["predicted_class"],
        confidence=primary_result["confidence"],
        timestamp_text=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )

    png_buffer = pil_to_png_bytes(report_image)
    pdf_buffer = pil_to_pdf_bytes(report_image)

    export_left, export_col1, export_col2, export_right = st.columns([0.26, 0.24, 0.24, 0.26])

    with export_col1:
        st.download_button(
            label="↓ Baixar PNG",
            data=png_buffer,
            file_name="analise_lichia.png",
            mime="image/png",
            width="stretch"
        )

    with export_col2:
        st.download_button(
            label="↓ Baixar PDF",
            data=pdf_buffer,
            file_name="analise_lichia.pdf",
            mime="application/pdf",
            width="stretch"
        )
