import sqlite3

# Função para criar o banco de dados e inserir os tickers de ações
def create_database():
    conn = sqlite3.connect('b3_stocks.db')  # Substitua 'seu_banco_de_dados.db' pelo nome do seu banco de dados SQLite
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS acoes (ticker TEXT)")

    # Insira os tickers de ações na tabela 'acoes'
    tickers = ["SPYI", "AGNC", "CSSEP", "ARR", "CSSEN", "ARLP"]  # Exemplo de tickers de ações
    for ticker in tickers:
        cursor.execute("INSERT INTO acoes (ticker) VALUES (?)", (ticker,))

    conn.commit()
    conn.close()

# Função para obter os tickers de ações do banco de dados SQLite
def get_tickers_from_database():
    conn = sqlite3.connect('b3_stocks.db')  # Substitua 'seu_banco_de_dados.db' pelo nome do seu banco de dados SQLite
    cursor = conn.cursor()
    cursor.execute("SELECT ticker FROM acoes")
    tickers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tickers

# Restante do código
import yfinance as yf

# Função para filtrar os critérios desejados
def filter_stocks(tickers):
    for ticker in tickers:
        data = yf.Ticker(ticker).history(period="1y")
        if len(data) < 252:  # Se houver menos de 252 dias de dados, pule para a próxima ação
            continue

        pct_change_12m = (data['Close'][-1] - data['Close'][0]) / data['Close'][0] * 100
        pb_ratio = yf.Ticker(ticker).info.get('priceToBook')
        div_yield = yf.Ticker(ticker).info.get('dividendYield')
        price = data['Close'][-1]

        if pct_change_12m > 0 and pb_ratio is not None and pb_ratio < 1 and div_yield is not None and div_yield > 0.10 and price < 15:
            print(f"Ticker: {ticker}")
            print(f"Percent Change 12m: {pct_change_12m}")
            print(f"P to VP: {pb_ratio}")
            print(f"Dividend Yield: {div_yield}")
            print(f"Price: {price}")
            print("----------------------")

# Criar o banco de dados e inserir os tickers de ações
create_database()

# Consultar o banco de dados para obter a lista de tickers de ações
tickers = get_tickers_from_database()

# Filtrar ações com base nos critérios especificados e imprimir informações
filter_stocks(tickers)
