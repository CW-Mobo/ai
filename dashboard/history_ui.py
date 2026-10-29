import streamlit as st


def render_history_section():
    st.markdown('<div class="section-title">Histórico de previsões</div>', unsafe_allow_html=True)

    if st.session_state.history:
        history_cols = st.columns(min(len(st.session_state.history), 3))
        for index, item in enumerate(st.session_state.history):
            with history_cols[index % len(history_cols)]:
                st.markdown(
                    f"""
                    <div class="history-card">
                        <strong>{item['predicted_class']}</strong>
                        <span>{item['file_name']}</span>
                        <span>Confiança: {item['confidence']}</span>
                        <small>{item['time']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.markdown(
            '<div class="empty-state">Nenhuma previsão registrada ainda.</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="history-clear-spacer"></div>', unsafe_allow_html=True)
    clear_left, clear_action, clear_right = st.columns([0.36, 0.28, 0.36])
    with clear_action:
        if st.button("Limpar histórico", width="stretch"):
            st.session_state.history = []
            st.session_state.last_history_key = None
            st.rerun()
