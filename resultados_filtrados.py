import pandas as pd

# Carregar o arquivo CSV com os resultados da análise fundamentalista
file_path = 'resultados_analise_fundamentalista.csv'
df = pd.read_csv(file_path)

# Definir os critérios de filtragem
filtros = (df['P/VP'] < 1) & \
          (df['Lucro por Ação (LPA)'] > 0) & \
          (df['P/L'] >= -1) & (df['P/L'] <= 1) & \
          (df['Crescimento da Receita (%)'] > 0)

# Aplicar os filtros ao DataFrame
df_filtrado = df[filtros]

# Verificar se existem resultados após o filtro
if not df_filtrado.empty:
    # Salvar os resultados filtrados em um novo arquivo CSV
    output_file = 'resultados_filtrados.csv'
    df_filtrado.to_csv(output_file, index=False)
    print(f"Arquivo gerado: {output_file}")
else:
    print("Nenhum ticker atende aos critérios especificados.")

# Exibir os resultados filtrados
print("\nResultados filtrados:")
print(df_filtrado.to_string(index=False))
