import React, { useState, useEffect, useRef } from "react";
import { createRoot } from "react-dom/client";
import Plotly from "plotly.js-dist-min";
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib";

function QuadVisualizer({ args }) {
  /* --- 受け取るパラメータ・デフォルト ------------------------- */
  const {
    a_init = 1.0,
    b_init = 0.0,
    c_init = 0.0,
    xmin   = -10,
    xmax   =  10,
    ymin   = -100,          // ★ 追加：固定したい y 軸範囲
    ymax   =  100
  } = args ?? {};

  /* --- React state ------------------------------------------- */
  const [a, setA] = useState(a_init);
  const [b, setB] = useState(b_init);
  const [c, setC] = useState(c_init);

  /* --- Plotly 描画 ------------------------------------------- */
  const plotRef = useRef(null);

  useEffect(() => {
    /* x, y データ生成 */
    const x = Array.from({ length: 400 }, (_, i) =>
      xmin + (xmax - xmin) * i / 399
    );
    const y = x.map(v => a * v * v + b * v + c);

    /* 折れ線トレース */
    const trace = {
      x,
      y,
      mode: "lines",
      line: { color: "royalblue", width: 3 }
    };

    /* 軸設定を固定 */
    const layout = {
      margin: { l: 50, r: 30, t: 30, b: 50 },
      xaxis: {
        range: [xmin, xmax],
        zeroline: true,
        zerolinecolor: '#888',
        gridcolor: '#eee',
        showline: true,
        linecolor: 'black',
        linewidth: 2,
        showspikes: false,
        title: {
          text: "x",
          standoff: 15,        // 軸から離す距離を調整
          font: { size: 16 }
        },
        tickmode: "array",
        tickvals: [...Array(11)].map((_, i) => xmin + (xmax - xmin) * i / 10),
        ticktext: [...Array(11)].map((_, i) => (xmin + (xmax - xmin) * i / 10).toFixed(1)),
        tickfont: { size: 12 },
        side: "bottom",
        showticklabels: true,
        mirror: true           // 上側の軸線も表示
      },
      yaxis: {
        range: [ymin, ymax],
        zeroline: true,
        zerolinecolor: '#888',
        gridcolor: '#eee',
        showline: true,
        linecolor: 'black',
        linewidth: 2,
        showspikes: false,
        title: {
          text: "y",
          standoff: 15,
          font: { size: 16 }
        },
        tickmode: "array",
        tickvals: [...Array(11)].map((_, i) => ymin + (ymax - ymin) * i / 10),
        ticktext: [...Array(11)].map((_, i) => (ymin + (ymax - ymin) * i / 10).toFixed(1)),
        tickfont: { size: 12 },
        side: "left",
        showticklabels: true,
        mirror: true
      },
      showlegend: false,
      height: 500,            // 高さを少し増やす
      width: 600,            // 幅も調整
      plot_bgcolor: 'white',
      paper_bgcolor: 'white'
    };

    /* 既に描画済みなら react で差し替え */
    if (plotRef.current?.data) {
      Plotly.react(plotRef.current, [trace], layout);
    } else {
      Plotly.newPlot(plotRef.current, [trace], layout, { responsive: true });
    }

    /* iframe 高さを通知 */
    Streamlit.setFrameHeight();
  }, [a, b, c, xmin, xmax, ymin, ymax]);

  /* --- Streamlit へ値を返す ---------------------------------- */
  useEffect(() => {
    Streamlit.setComponentValue({ a, b, c });
  }, [a, b, c]);

  /* --- UI（スライダー + グラフ） ------------------------------ */
  const labelStyle = { 
    width: 60, 
    fontWeight: "bold",
    fontSize: "1.1em",
    color: "#444"
  };
  
  const sliderStyle = { 
    flex: 1,
    margin: "0 12px",
    cursor: "pointer"
  };

  const valueStyle = {
    width: 50,
    textAlign: "right",
    fontSize: "1.1em",
    color: "#444",
    fontFamily: "monospace"
  };

  const slider = (label, value, setter) => (
    <div style={{ 
      display: "flex", 
      alignItems: "center", 
      marginBottom: 12,
      padding: "6px 0"
    }}>
      <span style={labelStyle}>{label}</span>
      <input
        type="range"
        min={-10}
        max={10}
        step={0.1}
        value={value}
        style={sliderStyle}
        onChange={e => setter(parseFloat(e.target.value))}
      />
      <span style={valueStyle}>{value.toFixed(1)}</span>
    </div>
  );

  return (
    <div style={{ width: "100%" }}>
      {slider("a", a, setA)}
      {slider("b", b, setB)}
      {slider("c", c, setC)}
      <div ref={plotRef} style={{ marginTop: 20 }} />
    </div>
  );
}

/* ------------- マウント --------------------------------------- */
const Connected = withStreamlitConnection(QuadVisualizer);
createRoot(document.getElementById("root")).render(<Connected />);