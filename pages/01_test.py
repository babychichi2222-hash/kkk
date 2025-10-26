import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- 설정 ---
st.set_page_config(
    page_title="최근 10년간 미국 시가총액 상위 10개 그룹 주가 시각화",
    layout="wide",
)

# 시가총액 기준 상위 10개 그룹의 티커 (최근 10년간의 대표성을 고려하여 선정)
TICKERS = [
    "AAPL",   # Apple
    "MSFT",   # Microsoft
    "GOOGL",  # Alphabet (Google)
    "AMZN",   # Amazon
    "NVDA",   # NVIDIA
    "META",   # Meta Platforms (Facebook)
    "TSLA",   # Tesla
    "BRK-B",  # Berkshire Hathaway
    "JPM",    # JPMorgan Chase
    "XOM",    # Exxon Mobil
]

# 캐시를 사용하여 데이터 로드 속도 향상
@st.cache_data
def load_data(tickers, start_date, end_date):
    """
    지정된 티커 목록에 대한 주식 데이터를 다운로드하고 전처리합니다.
    """
    st.write(f"--- 📊 {len(tickers)}개 그룹의 주식 데이터를 다운로드 중입니다. ---")
    data = yf.download(tickers, start=start_date, end=end_date)
    
    # 'Adj Close' (수정 종가) 데이터만 선택
    df = data['Adj Close'].copy()
    
    # 컬럼 이름을 회사명으로 변경 (선택 사항)
    ticker_names = {
        "AAPL": "Apple",
        "MSFT": "Microsoft",
        "GOOGL": "Alphabet (Google)",
        "AMZN": "Amazon",
        "NVDA": "NVIDIA",
        "META": "Meta Platforms",
        "TSLA": "Tesla",
        "BRK-B": "Berkshire Hathaway",
        "JPM": "JPMorgan Chase",
        "XOM": "Exxon Mobil",
    }
    df.columns = [ticker_names.get(col, col) for col in df.columns]
    
    return df

# --- Streamlit 앱 본문 ---
st.title("📈 최근 10년간 미국 시가총액 상위 10개 그룹 주가 시각화")
st.markdown("---")

# 현재 날짜 설정
end_date = datetime.now()
# 10년 전 날짜 설정
start_date_default = end_date - timedelta(days=10*365) 

# --- 사이드바: 사용자 입력 섹션 ---
st.sidebar.header("설정 옵션")

# 1. 날짜 범위 선택 (10년 전부터 현재까지)
date_range = st.sidebar.date_input(
    "기간을 선택하세요:",
    value=(start_date_default, end_date),
    max_value=end_date,
    format="YYYY/MM/DD"
)

# 날짜 유효성 검사
if len(date_range) == 2:
    start_dt = date_range[0].strftime('%Y-%m-%d')
    end_dt = date_range[1].strftime('%Y-%m-%d')
else:
    st.error("시작일과 종료일을 모두 선택해주세요.")
    st.stop()
    
# 2. 회사 선택
selected_companies = st.sidebar.multiselect(
    "시각화할 회사를 선택하세요:",
    options=list(load_data(TICKERS, start_dt, end_dt).columns),
    default=list(load_data(TICKERS, start_dt, end_dt).columns)[:5]  # 기본값으로 상위 5개 선택
)

# 데이터 로드
try:
    df_stock = load_data(TICKERS, start_dt, end_dt)
except Exception as e:
    st.error(f"주식 데이터 로드 중 오류 발생: {e}")
    st.stop()


# --- 시각화 섹션 ---
if not selected_companies:
    st.warning("왼쪽 사이드바에서 시각화할 회사를 하나 이상 선택해주세요.")
else:
    # 선택된 회사만 필터링
    df_plot = df_stock[selected_companies].dropna()

    # --- 1. 원본 주가 그래프 시각화 (Line Chart) ---
    st.header("1. 원본 주가 (수정 종가)")
    st.line_chart(df_plot)
    
    st.markdown("---")

    # --- 2. 정규화된 (Normalized) 주가 그래프 시각화 (Plotly) ---
    st.header("2. 정규화된 주가 (성장률 비교)")
    st.markdown("각 회사의 주가를 시작일($100$)을 기준으로 정규화하여 **성장률**을 비교합니다.")

    # 정규화: (현재 주가 / 시작일 주가) * 100
    df_normalized = (df_plot / df_plot.iloc[0]) * 100

    # Plotly 시각화를 위한 데이터 구조 변경 (melt)
    df_normalized_reset = df_normalized.reset_index()
    df_melted = df_normalized_reset.melt(
        id_vars='Date',
        value_vars=selected_companies,
        var_name='Company',
        value_name='Normalized Price ($100 = Start Date)'
    )

    # Plotly Line Chart 생성
    fig = px.line(
        df_melted,
        x='Date',
        y='Normalized Price ($100 = Start Date)',
        color='Company',
        title='주가 성장률 비교 (시작일을 100으로 정규화)',
        hover_data={"Date": "|%Y/%m/%d"},
        template="plotly_white"
    )

    # Y축 포맷 변경 (달러 표시, 쉼표)
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    # 레이아웃 조정
    fig.update_layout(
        legend_title_text='회사',
        xaxis_title="날짜",
        yaxis_title="정규화된 주가 (시작일 = $100$)",
    )

    # Streamlit에 Plotly 그래프 표시
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")

    # --- 데이터 테이블 표시 ---
    st.header("데이터 테이블 (원본 주가)")
    st.dataframe(df_plot.style.format("${:,.2f}"))
