import os
from typing import Optional
import streamlit.components.v1 as components

# dist フォルダへの絶対パス
_frontend_path = os.path.join(
    os.path.dirname(__file__), "frontend", "dist"
)

_slider = components.declare_component(
    "realtime_slider",
    path=_frontend_path
)

# ★ 新しいシグネチャ
def realtime_slider(
    a_init: float = 1.0,
    b_init: float = 0.0,
    c_init: float = 0.0,
    xmin: float = -10.0,
    xmax: float = 10.0,
    ymin: float = -100.0,
    ymax: float = 100.0,
    key: Optional[str] = None,
) -> Optional[dict]:
    """
    ２次関数の係数スライダー＋Plotly グラフを
    クライアント側で描画するコンポーネント。

    Returns
    -------
    Optional[dict]
        {"a": float, "b": float, "c": float} が返る。
        まだ iframe がロード中のときは None。
    """
    return _slider(
        a_init=a_init,
        b_init=b_init,
        c_init=c_init,
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        default=None,   # ← 初回は Python 側でフォールバック
        key=key,
    )
