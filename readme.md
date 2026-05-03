# 🛡️ SaaS Churn Shield: Health Score & Inteligência Preditiva

![Status do Projeto](https://img.shields.io/badge/Status-Finalizado-brightgreen)
![Data Science](https://img.shields.io/badge/Área-Data%20Science-blue)
![Business Focus](https://img.shields.io/badge/Foco-Regras%20de%20Negócio-gold)

Este projeto não é apenas um modelo de Machine Learning; é uma **estratégia de retenção de receita**. O objetivo foi transformar dados brutos de comportamento em uma lista de ações priorizadas para o time de Sucesso do Cliente (Customer Success), focando em salvar o faturamento de uma empresa SaaS.

---

## 🌐 Dashboard Interativo (Streamlit)

Para converter dados complexos em decisões rápidas, foi desenvolvido um dashboard interativo utilizando **Streamlit**. Esta ferramenta serve como a interface final para a equipe de **Customer Success**, permitindo uma operação baseada em dados (data-driven).

### ✨ Funcionalidades do Dashboard:
* **Monitorização de Saúde:** Visualização em tempo real da distribuição do *Health Score*.
* **Filtros de Prioridade:** Listagem imediata de clientes no estado "Crítico" com maior potencial de perda financeira.
* **Recomendações Inteligentes:** Sugestão automática de ações de retenção (ex: novos treinos, descontos ou consultoria) baseada nos serviços ativos do cliente.
* **Análise Financeira:** Cálculo automático do faturamento mensal em risco de acordo com os filtros aplicados.

🚀 **Entra na aplicação aqui:** [Clique para abrir o Dashboard Streamlit](http://localhost:8501/)

---

## 💼 O Desafio de Negócio

A empresa enfrentava um **Churn Rate de 26,54%**. O diagnóstico inicial revelou que estávamos perdendo os clientes com o maior ticket médio ($74,44), o que estava corroendo o **LTV (Lifetime Value)** da base.

> **Dor Identificada:** Clientes que não utilizavam suporte técnico tinham uma propensão massivamente maior ao cancelamento.

---

## 🛠️ Tecnologias & Ferramentas

* **Linguagem:** Python 3.x
* **Ambiente:** VS Code com Jupyter Notebooks (`.ipynb`)
* **Bibliotecas:** Pandas, Scikit-Learn, Seaborn, Matplotlib
* **Interface:** Streamlit (Dashboard Executivo)

---

## 🚀 O Projeto em Etapas

### 1. Data Wrangling & Limpeza Estratégica
Limpamos a base removendo ruídos e tratando tipagens financeiras.
* **Regra de Ouro:** Tratamos clientes com `Tenure = 0` como fase de Onboarding, separando-os da métrica de churn para não enviesar os resultados.

### 2. BI & Análise de Impacto
Exploramos os dados para encontrar correlações de valor. 

> ![Impacto do Suporte Técnico](../img/graficol1.png)

### 3. Engenharia do Health Score
Criamos o "coração" do projeto: um indicador de 0 a 100 que mede a saúde do cliente através da fórmula:

$$HealthScore = (Tenure \cdot 0.5) + (SupportUsage \cdot 0.3) - (MonthlyCharges \cdot 0.2)$$

> **INSIRA AQUI O SEU SEGUNDO GRÁFICO (Distribuição do Health Score)**
> ![Distribuição do Health Score](../img/graficol2.png)

### 4. Inteligência Preditiva (Machine Learning)
Treinamos um modelo de **Random Forest** focado em **Recall (70%)**.
* **Por que Recall?** Para o negócio, é melhor alertar sobre um cliente que talvez não saia (Falso Positivo) do que perder um cliente sem aviso prévio (Falso Negativo).

> **INSIRA AQUI O SEU TERCEIRO GRÁFICO (Impacto Financeiro)**
> ![Impacto Financeiro](../img/graficol3.png)

---

## 📈 Impacto Final e Actionability

Ao final, o sistema gerou uma lista de **2.298 clientes críticos** que representam um faturamento de **$172.171,30/mês**.

### 🖥️ Dashboard Streamlit
Para facilitar a operação, os dados foram integrados em um dashboard onde o time de Sucesso do Cliente pode:
1.  Visualizar os clientes com pior Health Score.
2.  Receber sugestões automáticas de ação (ex: Agendar Treinamento Técnico).
3.  Monitorar o faturamento total em risco.

---

## 📉 Resultados Obtidos

| Métrica | Valor |
| :--- | :--- |
| **Churn Rate Base Total** | 26.54% |
| **Churn Rate Grupo Crítico** | **36.73%** |
| **Recall do Modelo** | 70% |
| **Faturamento Protegido** | **$172.171,30** |

---

### 👨‍💻 Como Rodar o Projeto
1. Clone o repositório.
2. Instale as dependências: `pip install -r requirements.txt`.
3. Rode o notebook para ver a análise: `jupyter notebook`.
4. Inicie o dashboard: `streamlit run app.py`.

---
*Desenvolvido com foco em transformar dados em lucro.*