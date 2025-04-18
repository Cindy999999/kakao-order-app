import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.title("📦 카카오톡 발주 → 엑셀 변환기")

st.markdown("카카오톡 발주 메시지를 아래에 붙여넣고 엑셀로 저장하세요.")

text_input = st.text_area("✂️ 여기에 메시지를 붙여넣으세요", height=300)

def parse_orders(text):
    blocks = re.split(r"\n\s*\n", text.strip())
    orders = []

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 4:
            continue

        product = lines[1].strip()
        contact_line = lines[3].strip()

        contact_match = re.search(r'(\D+)(01[016789]-\d{3,4}-\d{4})(.*)', contact_line)
        if contact_match:
            receiver = contact_match.group(1).strip()
            phone = contact_match.group(2).strip()
            store = contact_match.group(3).strip()
        else:
            receiver = phone = store = ""

        address = lines[4].strip() if len(lines) >= 5 else ""

        orders.append({
            "제품명": product,
            "수령인": receiver,
            "매장명": store,
            "연락처": phone,
            "주소": address
        })

    return pd.DataFrame(orders)

if st.button("📥 엑셀로 저장"):
    if text_input.strip():
        df = parse_orders(text_input)
        if not df.empty:
            st.success("✅ 발주 정보가 추출되었습니다.")
            st.dataframe(df)

            towrite = BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            st.download_button(
                label="📤 엑셀 다운로드",
                data=towrite,
                file_name="발주내역.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("⚠️ 발주 정보를 추출할 수 없습니다. 메시지 형식을 확인해주세요.")
    else:
        st.warning("⚠️ 메시지를 입력해주세요.")
