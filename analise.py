import yfinance as yf
import pandas as pd
from IPython.display import display

# Carregar o arquivo CSV com os tickers
file_path = 'b3_stocks.csv'
df = pd.read_csv(file_path)

# Verificar se a coluna 'Ticker' está presente
if 'Ticker' in df.columns:
    tickers = df['Ticker'].tolist()  # Listar todos os tickers

    # Inicializar lista para armazenar os resultados
    resultados = []

    for ticker in tickers:
        # Obter os dados do ticker usando yfinance
        try:
            stock = yf.Ticker(ticker)

            # Buscar dados financeiros relevantes
            lpa = stock.info.get('trailingEps')  # Lucro por Ação (LPA)
            preco = stock.history(period="1d")['Close'][0]  # Preço atual da ação
            financials = stock.financials
            valor_patrimonial_por_acao = stock.info.get('bookValue')  # Valor patrimonial por ação (VP)

            # Verificar se financials não está vazio
            if not financials.empty:
                receita_atual = financials.loc['Total Revenue'][0]  # Receita Atual
                receita_anterior = financials.loc['Total Revenue'][1]  # Receita Anterior
            else:
                receita_atual = receita_anterior = None

            # Calcular P/L
            pl = preco / lpa if lpa else None

            # Calcular P/VP
            p_vp = preco / valor_patrimonial_por_acao if valor_patrimonial_por_acao else None

            # Calcular Crescimento da Receita
            if receita_atual and receita_anterior:
                crescimento_receita = ((receita_atual - receita_anterior) / receita_anterior) * 100
            else:
                crescimento_receita = None

            # Adicionar os resultados na lista
            resultados.append({
                'Ticker': ticker,
                'Lucro por Ação (LPA)': lpa,
                'P/L': pl,
                'P/VP': p_vp,
                'Crescimento da Receita (%)': crescimento_receita
            })

        except Exception as e:
            print(f"Erro ao obter dados para {ticker}: {e}")

    # Converter os resultados em um DataFrame
    resultados_df = pd.DataFrame(resultados)

    # Salvar os resultados em um novo arquivo CSV
    resultados_csv_path = 'resultados_analise_fundamentalista.csv'
    resultados_df.to_csv(resultados_csv_path, index=False)

    print("Análise fundamentalista concluída. Resultados salvos em 'resultados_analise_fundamentalista.csv'.")

    # Exibir o conteúdo do arquivo CSV em forma de tabela
    try:
        # Carregar o arquivo CSV gerado e exibir a tabela
        resultados_carregados = pd.read_csv(resultados_csv_path)
        print("\nResultados da análise fundamentalista:")
        display(resultados_carregados)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{resultados_csv_path}' não foi encontrado.")

else:
    print("Erro: A coluna 'Ticker' não foi encontrada no arquivo CSV.")
