import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="카카오톡 발주 변환기", layout="centered")

st.title("🥡 카카오톡 발주 내용 → 엑셀 변환기")

uploaded_file = st.file_uploader("카카오톡에서 복사한 발주 내용을 .txt 파일로 저장해서 업로드하세요", type="txt")

def parse_order_text(text):
    # 정규식을 사용하여 발주 내용 파싱
    pattern = r"(\d{1,2}/\d{1,2})\s+(.+?)\s+(\d+)\s+개"
    matches = re.findall(pattern, text)

    data = []
    for match in matches:
        date, item, qty = match
        data.append({"날짜": date, "품목": item, "수량": int(qty)})

    return pd.DataFrame(data)

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    df = parse_order_text(text)

    st.subheader("📋 발주 목록")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 엑셀(CSV)로 다운로드",
        data=csv,
        file_name="order_list.csv",
        mime="text/csv"
    )

