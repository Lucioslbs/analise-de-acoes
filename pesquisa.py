import yfinance as yf
import pandas as pd

# Lista fictícia de tickers do índice Bovespa
tickers = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBAS3.SA', 'ABEV3.SA', 'BBDC4.SA', 'B3SA3.SA', 'ITSA4.SA', 'JBSS3.SA', 'MGLU3.SA']

# Dicionário para armazenar os dados
data = {
    'Ticker': [],
    'P/L': [],
    'P/VP': [],
    'ROE': [],
    'DY': [],
    'Margem Liquida': [],
    'Crescimento Receita': []
}

for ticker in tickers:
    stock = yf.Ticker(ticker)
    info = stock.info

    # Verificar se a chave existe antes de adicionar para evitar KeyErrors
    pl = info.get('trailingPE')
    pvp = info.get('priceToBook')
    roe = info.get('returnOnEquity')
    dy = info.get('dividendYield')
    margem_liquida = info.get('profitMargins')
    crescimento_receita = info.get('revenueGrowth')

    # Continuar apenas se todos os dados necessários estiverem disponíveis
    if all([pl, pvp, roe, dy, margem_liquida, crescimento_receita]):
        data['Ticker'].append(ticker)
        data['P/L'].append(pl)  # P/L
        data['P/VP'].append(pvp)  # P/VP
        data['ROE'].append(roe * 100)  # ROE em porcentagem
        data['DY'].append(dy * 100)  # DY em porcentagem
        data['Margem Liquida'].append(margem_liquida * 100)  # Margem Líquida em porcentagem
        data['Crescimento Receita'].append(crescimento_receita * 100)  # Crescimento Receita em porcentagem

# Criar DataFrame
df = pd.DataFrame(data)

# Mostrar dados coletados antes da filtragem
print("Dados coletados:")
print(df)

# Aplicar filtros
filtered_df = df[(df['P/L'] < 10) &
                 (df['P/VP'] < 1) &
                 (df['ROE'] > 5) &
                 (df['DY'] > 7) &
                 (df['Margem Liquida'] > 3) &
                 (df['Crescimento Receita'] > 10)]

# Mostrar o resultado
print("Dados filtrados:")
print(filtered_df)
