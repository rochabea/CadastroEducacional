import matplotlib.pyplot as plt

# Mapeamento de cores por tipo de teste
cores = {
    "Integração de Unidades": "#4e79a7",
    "Carga": "#f28e2b",
    "Stress": "#e15759",
    "Aceitação": "#76b7b2",
    "Componente": "#59a14f",
    "Integração de Sistema": "#edc948",
    "Interface de Usuário": "#b07aa1",
    "End-to-End": "#ff9da7"
}

# Dados
ids = ['CT01', 'CT02', 'CT03', 'CT04', 'CT05', 'CT06', 'CT07', 'CT08', 'CT09', 'CT10']
cobertura_percentual = [75, 75, 75, 50, 50, 75, 25, 25, 50, 12.5]

# Tipos de teste correspondentes
tipos_teste = [
    "Componente", "Componente", "Integração de Unidades",
    "Interface de Usuário", "Interface de Usuário", "Integração de Sistema",
    "Stress", "Stress", "Aceitação", "Carga"
]

# Cores para cada barra
cores_barras = [cores[tipo] for tipo in tipos_teste]

# Gráfico
plt.figure(figsize=(10, 6))
bars = plt.bar(ids, cobertura_percentual, color=cores_barras)
plt.title("Cobertura por Caso de Teste (CT01 a CT10)")
plt.xlabel("ID do Caso de Teste")
plt.ylabel("Cobertura em % dos Tipos de Teste")

# Adiciona os valores nas barras
for bar, perc in zip(bars, cobertura_percentual):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f"{perc}%", ha='center', va='bottom')

plt.ylim(0, 110)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
