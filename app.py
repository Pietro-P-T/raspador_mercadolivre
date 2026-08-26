# app.py
# app.py
import streamlit as st
from scraper import buscar_livros

# Inicializa as chaves de session_state ANTES de qualquer uso
if "meus_livros" not in st.session_state:
    st.session_state.meus_livros = None

if "pagina_grafico" not in st.session_state:
    st.session_state.pagina_grafico = 0

st.markdown(
    """
    <style>
    @keyframes rainbow {
        0% { color: red; }
        16% { color: orange; }
        33% { color: yellow; }
        50% { color: green; }
        66% { color: blue; }
        83% { color: indigo; }
        100% { color: violet; }
    }
    .rainbow-text {
        font-size: 3rem;
        font-weight: bold;
        animation: rainbow 4s infinite linear;
    }
    </style>
    <h1 class="rainbow-text">Buscador de Livros</h1>
    """,
    unsafe_allow_html=True,
)

st.write(
    ":yellow[***Procurando algum livro no books to scrape?***]\n\n"
    "*Busque por eles e veja o que há de melhor*!"
)

# Ao clicar, salva o DataFrame retornado dentro da chave 'meus_livros'
if st.button("**Buscar Livros Irados**"):
    with st.spinner("Buscando..."):
        st.session_state.meus_livros = buscar_livros()
        st.session_state.pagina_grafico = (
            0  # reinicia a página do gráfico a cada nova busca
        )

# Verifica a chave correta da memória 'meus_livros'
if st.session_state.meus_livros is not None:
    df_resultado = st.session_state.meus_livros

    if df_resultado.empty:
        st.warning("Nenhum livro encontrado.")
    else:
        st.markdown("### 📋 Lista de Livros Disponíveis")
        st.dataframe(df_resultado, use_container_width=True)

        st.markdown("### 📊 Comparação de Preços")

        livros_por_pagina = 20
        total_paginas = -(-len(df_resultado) // livros_por_pagina)  # arredonda pra cima

        inicio = st.session_state.pagina_grafico * livros_por_pagina
        fim = inicio + livros_por_pagina
        df_pagina = df_resultado.iloc[inicio:fim]

        st.bar_chart(data=df_pagina, x="Título", y="Preço", color="#0C5CF0")

        coluna_esquerda, coluna_meio, coluna_direita = st.columns([1, 2, 1])

        with coluna_esquerda:
            if st.button("◀ Anterior", disabled=(st.session_state.pagina_grafico == 0)):
                st.session_state.pagina_grafico -= 1
                st.rerun()

        with coluna_meio:
            st.write(f"Página {st.session_state.pagina_grafico + 1} de {total_paginas}")

        with coluna_direita:
            if st.button(
                "Próxima ▶",
                disabled=(st.session_state.pagina_grafico >= total_paginas - 1),
            ):
                st.session_state.pagina_grafico += 1
                st.rerun()
