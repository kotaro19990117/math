import streamlit as st
from realtime_slider import realtime_slider  # フロントで描画するコンポーネント

# --------------------------------------------------------
# ページ設定
# --------------------------------------------------------
st.set_page_config(
    page_title="２次関数ビジュアライザー",
    layout="wide"    # ★ ワイドレイアウト
)

st.title("２次関数ビジュアライザー")

# --------------------------------------------------------
# カスタムコンポーネントを左カラムに配置
# --------------------------------------------------------
left, right = st.columns([2, 1])  # ★ 2:1 の比率で分割

with left:
    vals = realtime_slider(
        a_init=1.0,
        b_init=0.0,
        c_init=0.0,
        xmin=-10,
        xmax=10,
        ymin=-100,
        ymax=100,
        key="quad_vis"
    )

# コンポーネントがまだ描画準備中の場合 None が返るのでフォールバック
if vals is None:
    vals = {"a": 1.0, "b": 0.0, "c": 0.0}

a = vals["a"]
b = vals["b"]
c = vals["c"]

# --------------------------------------------------------
# 右カラムで式をリアルタイム表示
# --------------------------------------------------------
with right:
    st.subheader("現在の式 (標準形)")

    def term(val: float, symbol: str, power: str = "") -> str:
        sign = "+" if val >= 0 else "-"
        return f" {sign} {abs(val):.1f}{symbol}{power}"

    latex = f"y ={term(a,'x','^2')}{term(b,'x')}{term(c,'')}"
    latex = latex.replace("+ -", "- ")   # "+ -" → "-"
    st.latex(latex)

    # 平方完成
    st.markdown("---")
    st.subheader("平方完成")

    if a != 0:
        p = -b / (2 * a)
        q = a * p**2 + b * p + c
        latex_completed = (
            f"y = {abs(a):.1f}(x {'-' if p >= 0 else '+'} {abs(p):.1f})^2 "
            f"{'+' if q >= 0 else '-'} {abs(q):.1f}"
        )
    else:
        p, q = 0, c
        latex_completed = f"y = {b:.1f}x {'+' if c >= 0 else '-'} {abs(c):.1f}"
    st.latex(latex_completed)

    # 因数分解
    st.markdown("---")
    st.subheader("因数分解")

    if a != 0:
        D = b**2 - 4 * a * c
        if abs(D) < 1e-10:
            x1 = -b / (2 * a)
            latex_factored = (
                f"y = {a:.1f}(x {'-' if x1 >= 0 else '+'} {abs(x1):.1f})^2"
            )
        elif D > 0:
            import numpy as np

            x1 = (-b + np.sqrt(D)) / (2 * a)
            x2 = (-b - np.sqrt(D)) / (2 * a)
            latex_factored = (
                f"y = {a:.1f}(x {'-' if x1 >= 0 else '+'} {abs(x1):.1f})"
                f"(x {'-' if x2 >= 0 else '+'} {abs(x2):.1f})"
            )
        else:
            latex_factored = "実数解なし"
    else:
        if abs(b) < 1e-10:
            latex_factored = f"y = {c:.1f}"
        else:
            x1 = -c / b
            latex_factored = (
                f"y = {b:.1f}(x {'-' if x1 >= 0 else '+'} {abs(x1):.1f})"
            )
    st.latex(latex_factored)

    # パラメータ値
    st.markdown("---")
    st.subheader("パラメータ値")
    st.write(f"a = {a:.1f}")
    st.write(f"b = {b:.1f}")
    st.write(f"c = {c:.1f}")
    if a != 0:
        st.write(f"頂点 ({p:.1f}, {q:.1f})")
