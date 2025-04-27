import streamlit as st
from realtime_slider import realtime_slider  # 既存カスタムコンポーネント

# ========================================================
# 1) グローバル CSS を 1 度だけ注入
# ========================================================
def inject_global_css():
    st.markdown(
        """
        <style>
        /* ========== 共通 ========== */
        .stApp {
            font-family: "Segoe UI", Meiryo, sans-serif;
        }
        /* ---------- ヘッダー ---------- */
        .nav-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 32px;
            box-sizing: border-box;
            background: linear-gradient(90deg,#ff9c4b 0%,#ff6a8f 100%);
            box-shadow: 0 2px 4px rgba(0,0,0,.15);
            z-index: 10000;
        }
        .nav-title {
            font-size: 20px;
            font-weight: 700;
            color: #fff;
            white-space: nowrap;
        }
        .nav-menu {
            display: flex;
            gap: 28px;
        }
        .nav-link {
            color: #fff;
            font-weight: 600;
            text-decoration: none;
            transition: opacity .2s;
        }
        .nav-link:hover { opacity: .7; }

        /* ---------- 広告バナー ---------- */
        .ad-footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            height: 64px;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(90deg,#42c7ff 0%,#5effb1 100%);
            box-shadow: 0 -2px 4px rgba(0,0,0,.15);
            z-index: 9998;
        }
        .ad-footer img {
            height: 100%;
            width: auto;
            object-fit: contain;
        }

        /* ---------- コピーライト ---------- */
        .copyright-bar {
            position: fixed;
            left: 0;
            bottom: 64px;         /* 広告バナーの真上に固定 */
            width: 100%;
            height: 28px;
            background: rgba(0,0,0,.8);
            color: #fff;
            font-size: 12px;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }

        /* ---------- 本体の余白調整 ---------- */
        .stApp > div:first-child {
            padding-top: 80px;    /* header 64 + α */
            padding-bottom: 108px;/* footer 64 + copy 28 + α */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ========================================================
# 2) ヘッダー / フッター / コピーライト描画関数
# ========================================================
def render_navbar():
    st.markdown(
        """
        <header class="nav-header">
            <span class="nav-title">数学教材素材</span>
            <nav class="nav-menu">
                <a href="#" class="nav-link">数学 I</a>
                <a href="#" class="nav-link">数学 II</a>
                <a href="#" class="nav-link">数学 III</a>
                <a href="#" class="nav-link">数学 A</a>
                <a href="#" class="nav-link">数学 B</a>
                <a href="#" class="nav-link">数学 C</a>
            </nav>
        </header>
        """,
        unsafe_allow_html=True
    )

def render_footer_ad(img_url: str, link: str = "#"):
    st.markdown(
        f"""
        <div class="ad-footer">
            <a href="{link}" target="_blank" rel="noopener">
                <img src="{img_url}" alt="footer banner">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_copyright(text="© 2025 kotaro19990117"):
    st.markdown(
        f'<div class="copyright-bar">{text}</div>',
        unsafe_allow_html=True
    )

# ========================================================
# 3) ページ設定 & バー呼び出し
# ========================================================
st.set_page_config(page_title="VisualStudyMath", layout="wide")
inject_global_css()
render_navbar()
render_footer_ad(
    img_url="https://placehold.co/468x60?text=Ad+Sample",
    link="https://example.com"
)
render_copyright()

# ========================================================
# 4) 既存アプリ本体
# ========================================================
st.markdown(
    """
    <div style="text-align: right; margin: 20px 0;">
        <span style="font-size: 2em;">
    """, 
    unsafe_allow_html=True
)
st.latex(r"\Large y = ax^2 + bx + c")
st.markdown("</span></div>", unsafe_allow_html=True)

left, right = st.columns([1.2, 1])

with left:
    vals = realtime_slider(
        a_init=1.0, b_init=0.0, c_init=0.0,
        xmin=-10, xmax=10, ymin=-100, ymax=100,
        key="quad_vis"
    )
if vals is None:
    vals = {"a": 1.0, "b": 0.0, "c": 0.0}
a, b, c = vals["a"], vals["b"], vals["c"]

with right:
    st.subheader("現在の式 (標準形)")

    def term(v, sym, pw=""):
        s = "+" if v >= 0 else "-"
        return f" {s} {abs(v):.1f}{sym}{pw}"

    st.latex(f"y ={term(a,'x','^2')}{term(b,'x')}{term(c,'')}".replace("+ -", "- "))

    # --- 平方完成 ------------------------------------------------
    st.markdown("---")
    st.subheader("平方完成")

    if abs(a) > 1e-10:                         # 2 次項がある場合
        p = -b / (2 * a)
        q = a * p**2 + b * p + c
        sq = f"y = {a:.1f}\\left(x {'-' if p >= 0 else '+'} {abs(p):.1f}\\right)^2 " \
             f"{'+' if q >= 0 else '-'} {abs(q):.1f}"
        st.latex(sq)
    else:                                      # 1 次以下
        st.latex(f"y = {b:.1f}x {'+' if c >= 0 else '-'} {abs(c):.1f}")

    # --- 因数分解 ------------------------------------------------
    st.markdown("---")
    st.subheader("因数分解")

    if abs(a) < 1e-10:                         # 一次式または定数
        if abs(b) < 1e-10:
            st.latex(f"y = {c:.1f}")
        else:
            x0 = -c / b
            st.latex(f"y = {b:.1f}\\left(x {'-' if x0 >= 0 else '+'} {abs(x0):.1f}\\right)")
    else:
        import numpy as np
        D = b**2 - 4 * a * c
        if abs(D) < 1e-10:                     # 重解
            x0 = -b / (2 * a)
            st.latex(f"y = {a:.1f}\\left(x {'-' if x0 >= 0 else '+'} {abs(x0):.1f}\\right)^2")
        elif D > 0:                            # 実数解 2 つ
            x1 = (-b + np.sqrt(D)) / (2 * a)
            x2 = (-b - np.sqrt(D)) / (2 * a)
            fact = f"y = {a:.1f}\\left(x {'-' if x1 >= 0 else '+'} {abs(x1):.1f}\\right)" \
                   f"\\left(x {'-' if x2 >= 0 else '+'} {abs(x2):.1f}\\right)"
            st.latex(fact)
        else:                                  # 実数解なし
            st.write("実数解なし（因数分解不可）")