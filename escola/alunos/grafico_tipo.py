import matplotlib.pyplot as plt

# Tipos de testes (categorias)
tipos_de_testes = [
    "Integração de Unidades",
    "Carga",
    "Stress",
    "Aceitação",
    "Componente",
    "Integração de Sistema",
    "Interface de Usuário",
    "End-to-End"
]

# Casos de teste CT01 a CT10 e os tipos de testes em que apareceram
casos_por_teste = {
    "CT01": ["Integração de Unidades", "Aceitação", "Componente", "Integração de Sistema", "Interface de Usuário", "End-to-End"],
    "CT02": ["Integração de Unidades", "Aceitação", "Componente", "Integração de Sistema", "Interface de Usuário", "End-to-End"],
    "CT03": ["Integração de Unidades", "Aceitação", "Componente", "Integração de Sistema", "Interface de Usuário", "End-to-End"],
    "CT04": ["Integração de Unidades", "Aceitação", "Componente", "Interface de Usuário", "End-to-End"],
    "CT05": ["Integração de Unidades", "Aceitação", "Componente", "Interface de Usuário", "End-to-End"],
    "CT06": ["Integração de Unidades", "Carga", "Componente", "Integração de Sistema", "Interface de Usuário", "End-to-End"],
    "CT07": ["Integração de Unidades", "End-to-End"],
    "CT08": ["Integração de Unidades", "End-to-End"],
    "CT09": ["Carga", "Stress", "Integração de Sistema", "Interface de Usuário"],
    "CT10": ["Stress"]
}

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
