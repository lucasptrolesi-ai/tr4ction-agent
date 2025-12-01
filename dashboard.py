# dashboard.py
"""
Dashboard de acompanhamento do TR4CTION Agent.

- Lista respostas por founder e por etapa
- Ajuda mentores a verem o que já foi feito
"""

from collections import defaultdict
from typing import Dict, List
import csv
import io

import streamlit as st

from utils.data_manager import load_answers

st.set_page_config(
    page_title="TR4CTION – Dashboard",
    layout="wide",
    page_icon="📊",
)

st.title("📊 Dashboard – TR4CTION Agent (Q1)")

answers = load_answers()

if not answers:
    st.info("Nenhuma resposta registrada ainda. Use o app principal primeiro.")
    st.stop()

# ---------------------------
# Filtros
# ---------------------------
founders = sorted({row["founder_id"] for row in answers})
steps = sorted({row["step"] for row in answers})

col_f1, col_f2 = st.columns(2)
selected_founder = col_f1.selectbox("Filtrar por Founder ID", ["(todos)"] + founders)
selected_step = col_f2.selectbox("Filtrar por etapa", ["(todas)"] + steps)

filtered: List[Dict] = []
for row in answers:
    if selected_founder != "(todos)" and row["founder_id"] != selected_founder:
        continue
    if selected_step != "(todas)" and row["step"] != selected_step:
        continue
    filtered.append(row)

st.markdown(f"### Resultados filtrados: {len(filtered)} registros")

# ---------------------------
# Download em CSV
# ---------------------------
if filtered:
    output = io.StringIO()
    fieldnames = ["timestamp", "founder_id", "startup", "founder_name", "step", "answer"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(filtered)
    csv_bytes = output.getvalue().encode("utf-8")

    st.download_button(
        "⬇ Baixar respostas em CSV",
        data=csv_bytes,
        file_name="respostas_tr4ction.csv",
        mime="text/csv",
    )

# ---------------------------
# Agrupar por founder + step
# ---------------------------
grouped: Dict[str, List[Dict]] = defaultdict(list)
for row in filtered:
    key = f"{row['founder_name']} – {row['startup']} ({row['founder_id']})"
    grouped[key].append(row)

for header, rows in grouped.items():
    st.markdown(f"#### 👤 {header}")
    for r in rows:
        ts = r["timestamp"]
        step = r["step"]
        st.markdown(
            f"""
            <div style="padding:10px;border-radius:8px;background:#111827;margin-bottom:10px;">
              <div style="font-size:0.8rem;color:#9CA3AF;">{ts} · etapa: <strong>{step}</strong></div>
              <div style="margin-top:6px;white-space:pre-wrap;">{r['answer']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
