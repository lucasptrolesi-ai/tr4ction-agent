import streamlit as st
from utils.data_manager import load_data

st.title("📊 Dashboard Administrativo - TR4CTION")

data = load_data()

if not data:
    st.warning("Ainda não há founders registrados.")
else:
    st.subheader("Founders cadastrados")

    rows = []
    for fid, info in data.items():
        rows.append([
            fid,
            info["startup"],
            info["founder_name"],
            info["step"],
            info["last_update"]
        ])

    st.table({
        "ID": [r[0] for r in rows],
        "Startup": [r[1] for r in rows],
        "Founder": [r[2] for r in rows],
        "Etapa Atual": [r[3] for r in rows],
        "Última Atividade": [r[4] for r in rows]
    })

    st.subheader("🔎 Consultar Founder")

    selected = st.selectbox("Selecione um founder:", list(data.keys()))

    if selected:
        info = data[selected]

        st.write(f"### Startup: **{info['startup']}**")
        st.write(f"### Founder: **{info['founder_name']}**")
        st.write(f"### Etapa atual: `{info['step']}`")
        st.write("---")

        st.write("## Respostas")
        for etapa, texto in info["answers"].items():
            st.write(f"### {etapa.upper()}")
            st.write(texto)
            st.write("---")

        st.download_button(
            "📄 Baixar trilha em TXT",
            data="\n\n".join([f"{k}\n{text}" for k, text in info["answers"].items()]),
            file_name=f"{info['founder_name']}_trilha.txt"
        )
