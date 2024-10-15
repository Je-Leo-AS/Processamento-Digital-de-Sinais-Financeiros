import MetaTrader5 as mt5
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta

# Conectar ao MetaTrader 5
if not mt5.initialize():
    st.error(f"Falha ao conectar ao MT5: {mt5.last_error()}")
    mt5.shutdown()

# Função para buscar dados históricos da ação
def obter_dados_acao(symbol, timeframe, n_candles):
    data = mt5.copy_rates_from_pos(symbol, timeframe, 0, n_candles)
    if data is None:
        st.error(f"Erro ao obter dados: {mt5.last_error()}")
        return None
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# Sidebar para escolher o ativo e o período
st.sidebar.title("Configurações")
ativo = st.sidebar.text_input("Símbolo do ativo", value="PETR4")
timeframe = st.sidebar.selectbox("Timeframe", ["M1", "M5", "H1", "D1"])
n_candles = st.sidebar.slider("Número de candles", 10, 500, 100)

# Converter timeframe para o formato MT5
timeframes = {"M1": mt5.TIMEFRAME_M1, "M5": mt5.TIMEFRAME_M5,
              "H1": mt5.TIMEFRAME_H1, "D1": mt5.TIMEFRAME_D1}
timeframe_mt5 = timeframes[timeframe]

# Obter os dados da ação selecionada
df = obter_dados_acao(ativo, timeframe_mt5, n_candles)

if df is not None:
    # Mostrar tabela de dados
    st.write(f"Dados de {ativo}")
    st.dataframe(df)

    # Gráfico de preços (Plotly)
    fig = px.line(df, x='time', y='close', title=f"Preço de Fechamento - {ativo}")
    st.plotly_chart(fig)

# Desconectar do MT5 ao final
mt5.shutdown()
