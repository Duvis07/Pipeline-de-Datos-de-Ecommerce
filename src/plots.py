import matplotlib
import matplotlib.pyplot as plt

import plotly.express as px
import seaborn as sns

from pandas import DataFrame


def plot_revenue_by_month_year(df: DataFrame, year: int):
    """Plot revenue by month in a given year

    Args:
        df (DataFrame): Dataframe with revenue by month and year query result
        year (int): It could be 2016, 2017 or 2018
    """
    matplotlib.rc_file_defaults()
    sns.set_style(style=None, rc=None)

    _, ax1 = plt.subplots(figsize=(12, 6))

    sns.lineplot(data=df[f"Year{year}"], marker="o", sort=False, ax=ax1)
    ax2 = ax1.twinx()

    sns.barplot(data=df, x="month", y=f"Year{year}", alpha=0.5, ax=ax2)
    ax1.set_title(f"Revenue by month in {year}")

    plt.show()


def plot_real_vs_predicted_delivered_time(df: DataFrame, year: int):
    """Plot real vs predicted delivered time by month in a given year

    Args:
        df (DataFrame): Dataframe with real vs predicted delivered time by month and
                        year query result
        year (int): It could be 2016, 2017 or 2018
    """
    matplotlib.rc_file_defaults()
    sns.set_style(style=None, rc=None)

    _, ax1 = plt.subplots(figsize=(12, 6))

    sns.lineplot(data=df[f"Year{year}_real_time"], marker="o", sort=False, ax=ax1)
    ax1.twinx()
    g = sns.lineplot(
        data=df[f"Year{year}_estimated_time"], marker="o", sort=False, ax=ax1
    )
    g.set_xticks(range(len(df)))
    g.set_xticklabels(df.month.values)
    g.set(xlabel="month", ylabel="Average days delivery time", title="some title")
    ax1.set_title(f"Average days delivery time by month in {year}")
    ax1.legend(["Real time", "Estimated time"])

    plt.show()


def plot_global_amount_order_status(df: DataFrame):
    """Plot global amount of order status

    Args:
        df (DataFrame): Dataframe with global amount of order status query result
    """
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["estado_pedido"]]

    wedges, autotexts = ax.pie(df["Cantidad"], textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Order Status",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("Order Status Total")

    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    # Guardar el gráfico
    plt.savefig('global_amount_order_status.png')
    plt.close()


def plot_revenue_per_state(df: DataFrame):
    """Plot revenue per state

    Args:
        df (DataFrame): Dataframe with revenue per state query result
    """
    fig = px.treemap(
        df, path=["customer_state"], values="Revenue", width=800, height=400
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def plot_top_10_least_revenue_categories(df: DataFrame):
    """Plot top 10 least revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 least revenue categories query result
    """
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["Category"]]

    revenue = df["Revenue"]
    wedges, autotexts = ax.pie(revenue, textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Top 10 Revenue Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")
    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    ax.set_title("Top 10 Least Revenue Categories ammount")

    plt.show()


def plot_top_10_revenue_categories_ammount(df: DataFrame):
    """Plot top 10 revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 revenue categories query result
    """
    # Plotting the top 10 revenue categories ammount
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["Category"]]

    revenue = df["Revenue"]
    wedges, autotexts = ax.pie(revenue, textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Top 10 Revenue Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")
    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    ax.set_title("Top 10 Revenue Categories ammount")

    plt.show()


def plot_top_10_revenue_categories(df: DataFrame):
    """Plot top 10 revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 revenue categories query result
    """
    fig = px.treemap(df, path=["Category"], values="Num_order", width=800, height=400)
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def plot_freight_value_weight_relationship(df: DataFrame):
    """Plot freight value weight relationship

    Args:
        df (DataFrame): Dataframe with freight value weight relationship query result
    """
    plt.figure(figsize=(10, 6))
    
    # Crear scatter plot usando seaborn
    sns.scatterplot(data=df, x='total_weight', y='freight_value', alpha=0.5)
    
    # Añadir línea de regresión para ver la tendencia
    sns.regplot(data=df, x='total_weight', y='freight_value', 
                scatter=False, color='red', line_kws={'linestyle': '--'})
    
    # Personalizar el gráfico
    plt.title('Relación entre Peso Total y Valor del Flete')
    plt.xlabel('Peso Total del Pedido (g)')
    plt.ylabel('Valor del Flete (R$)')
    
    # Ajustar márgenes
    plt.tight_layout()
    
    # Guardar el gráfico
    plt.savefig('freight_value_weight_relationship.png')
    plt.close()


def plot_delivery_date_difference(df: DataFrame):
    """Plot delivery date difference

    Args:
        df (DataFrame): Dataframe with delivery date difference query result
    """
    plt.figure(figsize=(10, 6))
    
    sns.barplot(data=df, x="Diferencia_Entrega", y="Estado").set(
        title="Diferencia Entre Fecha Estimada y Fecha Real de Entrega por Estado"
    )
    
    plt.xlabel("Diferencia en Días")
    plt.ylabel("Estado")
    
    # Ajustar márgenes
    plt.tight_layout()
    
    # Guardar el gráfico
    plt.savefig('delivery_date_difference.png')
    plt.close()


def plot_order_amount_per_day_with_holidays(df: DataFrame):
    """Plot order amount per day with holidays

    Args:
        df (DataFrame): Dataframe with order amount per day with holidays query result
    """
    plt.figure(figsize=(15, 6))
    
    # Crear el gráfico de línea para la cantidad de pedidos
    plt.plot(df['date'], df['order_count'], label='Pedidos por día', color='blue')
    
    # Marcar los días festivos con puntos rojos
    holidays = df[df['holiday']]
    plt.scatter(holidays['date'], holidays['order_count'], 
               color='red', label='Días festivos', zorder=5)
    
    # Personalizar el gráfico
    plt.title('Cantidad de Pedidos por Día en 2017 (Días Festivos Marcados)')
    plt.xlabel('Fecha')
    plt.ylabel('Cantidad de Pedidos')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Ajustar márgenes
    plt.tight_layout()
    
    # Guardar el gráfico
    plt.savefig('orders_per_day_with_holidays.png')
    plt.close()
