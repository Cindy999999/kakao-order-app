import re
import pandas as pd
from flask import Flask, request, send_file, render_template_string
from io import BytesIO

app = Flask(__name__)

# 🧠 매장 이름 정규화 매핑
STORE_NAME_MAP = {
    "베하일산": "베이비하우스 일산",
    "베하천안": "베이비하우스 천안",
    "베이비하우스 전주점": "베이비하우스 전주",
    "베플덕이": "베이비플러스 일산덕이",
    "베파진천": "베이비파크 진천",
    "베네파주": "베네피아 파주",
    "구로베네피아": "베네피아 구로",
    "에이블": "에이블",
    "순천베하": "베이비하우스 순천",
    "베이비하우스 대구": "베이비하우스 대구",
    "베이비하우스 포항": "베이비하우스 포항",
    "베이비하우스 영통": "베이비하우스 영통",
    "포레스트": "포레스트"
}

# 📦 제품명과 제품코드를 매핑 (간단 예시)
PRODUCT_CODE_MAP = {
    "미카 360": "6MC0400027",
    "미카 프로 에코": "6MC0400005",
    "오이스터3 샴페인 샌드": "6OY0100006",
    "OY3 플러스 샴페인 샌드": "6OY0100006"
}

# 📌 정규식 기반 파서
def parse_order(text: str):
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    rows = []

    i = 0
    while i < len(lines):
        store = STORE_NAME_MAP.get(lines[i], lines[i])
        i += 1

        # 제품
        product_line = lines[i]
        product_name = re.sub(r"\(.*?\)|\d+년형", "", product_line).strip(" -").strip()
        product_code = ""
        for name, code in PRODUCT_CODE_MAP.items():
            if name in product_name:
                product_code = code
                break
        i += 1

        # 수령인 + 연락처
        name_phone = lines[i]
        match = re.match(r"(.+?)\s*[-:]?\s*(01[0-9][-]?\d{3,4}[-]?\d{4})", name_phone)
        if match:
            receiver = match.group(1).strip()
            phone = match.group(2).strip()
        else:
            receiver, phone = "", ""
        i += 1

        # 주소
        address = lines[i] if i < len(lines) else ""
        i += 1

        rows.append({
            "매장명": store,
            "제품명": product_name,
            "제품코드": product_code,
            "수령인": receiver,
            "연락처": phone,
            "주소": address
        })

    return pd.DataFrame(rows)


# 🌐 웹 UI
HTML = '''
<h1>📦 카카오톡 발주 ➜ 엑셀 변환기</h1>
<p>카카오톡 발주 메시지를 아래에 붙여넣고 엑셀로 저장하세요.</p>
<form method="post">
  <textarea name="message" rows="15" cols="80" placeholder="여기에 메시지를 붙여넣으세요"></textarea><br><br>
  <input type="submit" value="엑셀로 저장">
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']
        df = parse_order(message)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        return send_file(output, download_name='orders.xlsx', as_attachment=True)
    return render_template_string(HTML)


if __name__ == '__main__':
    app.run(debug=True)

