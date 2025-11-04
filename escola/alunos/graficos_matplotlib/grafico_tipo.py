import matplotlib.pyplot as plt

# Tipos de testes (categorias)
tipos_de_testes = [
    "Unitarios",
    "CRUD",
    "RN",
    "Carga",
    "Stress",
]

# Casos de teste CT01 a CT10 e os tipos de testes em que apareceram
casos_por_teste = {
    "CT01": ["Unitarios", "RN"],
    "CT02": ["Unitarios"],
    "CT03": ["Unitarios", "RN"],
    "CT04": ["Unitarios", "RN"],
    "CT05": ["Unitarios", "Carga", "Stress"],
    "CT06": ["Carga", "Stress"],
    "CT07": ["Carga", "Stress"],
    "CT08": ["Carga", "Stress"],
    "CT09": ["Carga", "Stress"],
    "CT10": ["Carga", "Stress"],
    "CT11": ["CRUD"]
}

# Mapeamento de cores por tipo de teste
cores = {
    "Unitarios": "#4e79a7",
    "CRUD": "#f28e2b",
    "Carga": "#e15759",
    "RN": "#76b7b2",
    "Stress": "#59a14f",
}

# Organizar dados para o gráfico
casos = list(casos_por_teste.keys())
valores_por_tipo = {tipo: [] for tipo in tipos_de_testes}

for ct in casos:
    presentes = casos_por_teste[ct]
    for tipo in tipos_de_testes:
        valores_por_tipo[tipo].append(1 if tipo in presentes else 0)

# Criar gráfico de barras empilhadas
plt.figure(figsize=(12, 7))
base = [0] * len(casos)

for tipo in tipos_de_testes:
    valores = valores_por_tipo[tipo]
    plt.bar(casos, valores, bottom=base, label=tipo, color=cores[tipo])
    base = [sum(x) for x in zip(base, valores)]

# Personalizações
plt.title("Cobertura dos Tipos de Testes por Caso de Teste")
plt.xlabel("Casos de Teste")
plt.ylabel("Quantidade de Tipos de Teste Aplicados")
plt.legend(title="Tipos de Teste", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(axis="y", linestyle="--", alpha=0.5)

# Mostrar gráfico
plt.show()
