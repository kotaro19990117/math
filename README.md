# ２次関数ビジュアライザー  
ブラウザ上の **スライダー** を動かすと、同じくブラウザ上で **２次関数のグラフ** がリアルタイムに描画される Streamlit アプリです。  
グラフは Plotly.js、UI は React＋Vite で実装した **カスタムコンポーネント** 内で完結するため、Python 側の再計算を最小限に抑え、滑らかな操作感を実現しています。

---

## デモ
![demo](docs/demo.gif) <!-- スクリーンキャストを置く場合 -->

---

## 特長
* **完全クライアント描画**  
  - グラフ・スライダーはすべて React / Plotly.js で実行  
  - Python へは数値だけを返すためカクつきが少ない
* **高校数学風の座標軸**  
  - 太い黒軸・矢印・添字（x, y）  
  - メモリを軸線のすぐ近くに配置
* **カスタマイズが簡単**  
  - \(a\), \(b\), \(c\) の初期値や軸範囲を Python から渡すだけ  
  - JSX のレイアウトやスタイルを変更して再ビルドすれば即反映

---

## 1. ディレクトリ構成


my_project/
├─ app.py # Streamlit 本体
├─ realtime_slider/ # カスタムコンポーネント
│ ├─ init.py # Python ラッパー
│ └─ frontend/
│ ├─ src/ # React + Plotly.js ソース
│ │ └─ index.jsx
│ ├─ index.html # マウントポイント (<div id="root">)
│ ├─ vite.config.js
│ └─ dist/ # npm run build で自動生成
└─ venv/ # Python 仮想環境



---

## 2. セットアップ手順

### 2-1. Python 側

python -m venv venv
source venv/bin/activate
pip install streamlit numpy


### 2-2. フロントエンド側

bash
cd realtime_slider/frontend
npm install # React, Plotly, Vite などを取得
npm run build # dist/ に成果物生成

---

## 3. 使い方（クイックスタート）

bash
① 仮想環境を起動（未作成の場合は README 上部の手順で作成）
source venv/bin/activate # Windows の場合は venv\Scripts\activate
② カスタムコンポーネントがビルド済みでない場合
cd realtime_slider/frontend
npm run build # dist/ が作成される
cd ../../ # プロジェクトのルートへ戻る
③ Streamlit アプリを起動
streamlit run app.py


ブラウザ (http://localhost:8501) が自動で開き、スライダーを動かすと係数 \(a,\,b,\,c\) がリアルタイムに反映された２次関数のグラフが表示されます。

---

## 4. カスタマイズガイド

| カスタマイズ内容 | 変更箇所 |
| :-- | :-- |
| スライダーの初期値・範囲 | `app.py` 内の `st.slider()` 引数 |
| 軸の表示範囲・目盛り | `frontend/src/index.jsx` の `layout` オブジェクト |
| カラーテーマ | `frontend/src/index.jsx` の CSS in JS or グローバル CSS |
| ラベリング言語 | `README.md`／`app.py`／`index.jsx` の文言 |

> React コンポーネント側を編集したあとは  
> `cd realtime_slider/frontend && npm run dev`  
> でホットリロードしながら開発できます。

---

## 5. よくある質問 (FAQ)

**Q. コンポーネントが読み込まれず空白になります。**  
A. `npm run build` が成功して dist/ にバンドルが生成されたか確認してください。ブラウザの DevTools で 404 が出ていないかも要チェックです。

**Q. numpy が見つからないエラーが出ます。**  
A. 仮想環境が有効化されていない、または `pip install -r requirements.txt` が漏れている可能性があります。

---

## 6. ライセンス

