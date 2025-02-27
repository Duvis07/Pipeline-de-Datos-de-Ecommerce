from collections import namedtuple
from enum import Enum
from typing import Callable, Dict, List

import pandas as pd
from pandas import DataFrame, read_sql
from sqlalchemy import text, inspect
from sqlalchemy.engine.base import Engine

from src.config import QUERIES_ROOT_PATH

QueryResult = namedtuple("QueryResult", ["query", "result"])


class QueryEnum(Enum):
    """This class enumerates all the queries that are available"""

    DELIVERY_DATE_DIFFERECE = "delivery_date_difference"
    GLOBAL_AMMOUNT_ORDER_STATUS = "global_ammount_order_status"
    REVENUE_BY_MONTH_YEAR = "revenue_by_month_year"
    REVENUE_PER_STATE = "revenue_per_state"
    TOP_10_LEAST_REVENUE_CATEGORIES = "top_10_least_revenue_categories"
    TOP_10_REVENUE_CATEGORIES = "top_10_revenue_categories"
    REAL_VS_ESTIMATED_DELIVERED_TIME = "real_vs_estimated_delivered_time"
    ORDERS_PER_DAY_AND_HOLIDAYS_2017 = "orders_per_day_and_holidays_2017"
    GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP = "get_freight_value_weight_relationship"


def read_query(query_name: str) -> str:
    """Read the query from the file.

    Args:
        query_name (str): The name of the file.

    Returns:
        str: The query.
    """
    with open(f"{QUERIES_ROOT_PATH}/{query_name}.sql", "r") as f:
        sql_file = f.read()
        sql = text(sql_file)
    return sql


def query_delivery_date_difference(database: Engine) -> QueryResult:
    """Get the query for delivery date difference.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for delivery date difference.
    """
    query_name = QueryEnum.DELIVERY_DATE_DIFFERECE.value
    query = read_query(QueryEnum.DELIVERY_DATE_DIFFERECE.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_global_ammount_order_status(database: Engine) -> QueryResult:
    """Get the query for global amount of order status.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for global percentage of order status.
    """
    query_name = QueryEnum.GLOBAL_AMMOUNT_ORDER_STATUS.value
    query = read_query(QueryEnum.GLOBAL_AMMOUNT_ORDER_STATUS.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_revenue_by_month_year(database: Engine) -> QueryResult:
    """Get the query for revenue by month year.

    Args:
        database (Engine): Database connection.

    Returns:
        Query: The query for revenue by month year.
    """
    query_name = QueryEnum.REVENUE_BY_MONTH_YEAR.value
    query = read_query(QueryEnum.REVENUE_BY_MONTH_YEAR.value)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_revenue_per_state(database: Engine) -> QueryResult:
    """Query revenue per state.

    Args:
        database (Engine): Database connection.

    Returns:
        QueryResult: Query result with revenue per state.
    """
    query_name = "revenue_per_state"
    query = read_query(query_name)
    
    # Verificar que las tablas necesarias existan
    inspector = inspect(database)
    required_tables = ['olist_orders', 'olist_order_items', 'olist_customers']
    existing_tables = inspector.get_table_names()
    
    for table in required_tables:
        if table not in existing_tables:
            raise ValueError(f"La tabla {table} no existe en la base de datos")
            
    # Ejecutar la consulta
    result = read_sql(query, database)
    
    return QueryResult(query=query_name, result=result)


def query_top_10_least_revenue_categories(database: Engine) -> QueryResult:
    """Query top 10 least revenue categories.

    Args:
        database (Engine): Database connection.

    Returns:
        QueryResult: Query result with top 10 least revenue categories.
    """
    query_name = "top_10_least_revenue_categories"
    query = read_query(query_name)
    
    # Verificar que las tablas necesarias existan
    inspector = inspect(database)
    required_tables = [
        'olist_orders', 
        'olist_order_items', 
        'olist_products',
        'product_category_name_translation'
    ]
    existing_tables = inspector.get_table_names()
    
    for table in required_tables:
        if table not in existing_tables:
            raise ValueError(f"La tabla {table} no existe en la base de datos")
    
    # Ejecutar la consulta
    result = read_sql(query, database)
    
    return QueryResult(query=query_name, result=result)


def query_top_10_revenue_categories(database: Engine) -> QueryResult:
    """Query top 10 revenue categories.

    Args:
        database (Engine): Database connection.

    Returns:
        QueryResult: Query result with top 10 revenue categories.
    """
    query_name = "top_10_revenue_categories"
    query = read_query(query_name)
    
    # Verificar que las tablas necesarias existan
    inspector = inspect(database)
    required_tables = [
        'olist_orders', 
        'olist_order_items', 
        'olist_products',
        'product_category_name_translation'
    ]
    existing_tables = inspector.get_table_names()
    
    for table in required_tables:
        if table not in existing_tables:
            raise ValueError(f"La tabla {table} no existe en la base de datos")
    
    # Ejecutar la consulta
    result = read_sql(query, database)
    
    return QueryResult(query=query_name, result=result)


def query_real_vs_estimated_delivered_time(database: Engine) -> QueryResult:
    """Query real vs estimated delivered time.

    Args:
        database (Engine): Database connection.

    Returns:
        QueryResult: Query result with real vs estimated delivered time.
    """
    query_name = "real_vs_estimated_delivered_time"
    query = read_query(query_name)
    
    # Verificar que las tablas necesarias existan
    inspector = inspect(database)
    required_tables = ['olist_orders']
    existing_tables = inspector.get_table_names()
    
    for table in required_tables:
        if table not in existing_tables:
            raise ValueError(f"La tabla {table} no existe en la base de datos")
    
    # Ejecutar la consulta
    result = read_sql(query, database)
    
    return QueryResult(query=query_name, result=result)


def query_freight_value_weight_relationship(database: Engine) -> QueryResult:
    """Get the freight_value weight relation for delivered orders.

    In this particular query, we want to evaluate if exists a correlation between
    the weight of the product and the value paid for delivery.

    We will use olist_orders, olist_order_items, and olist_products tables alongside
    some Pandas magic to produce the desired output: A table that allows us to
    compare the order total weight and total freight value.

    Of course, you could also do this with pure SQL statements but we would like
    to see if you've learned correctly the pandas' concepts seen so far.

    Args:
        database (Engine): Database connection.

    Returns:
        QueryResult: The query for freight_value vs weight data.
    """
    query_name = "get_freight_value_weight_relationship"
    query = read_query(query_name)
    
    # Verificar que las tablas necesarias existan
    inspector = inspect(database)
    required_tables = [
        'olist_orders', 
        'olist_order_items', 
        'olist_products'
    ]
    existing_tables = inspector.get_table_names()
    
    for table in required_tables:
        if table not in existing_tables:
            raise ValueError(f"La tabla {table} no existe en la base de datos")
    
    # Ejecutar la consulta
    result = read_sql(query, database)
    
    return QueryResult(query=query_name, result=result)


def query_orders_per_day_and_holidays_2017(database: Engine) -> QueryResult:
    """
    Query to get the number of orders per day and holidays in 2017.
    Args:
        database (Engine): The database engine.
    Returns:
        QueryResult: The query result.
    """
    query_name = "orders_per_day_and_holidays_2017"
    query = read_query(query_name)
    
    try:
        # Execute query to get orders per day
        result_df = pd.read_sql_query(query, database)
        
        # Get holidays for 2017
        holidays_2017 = get_public_holidays(2017)
        
        # Convert date strings to datetime
        result_df['date'] = pd.to_datetime(result_df['date'])
        holidays_2017['date'] = pd.to_datetime(holidays_2017['date'])
        
        # Add holiday column
        result_df['holiday'] = result_df['date'].isin(holidays_2017['date'])
        
        log.info(f"Query {query_name} executed successfully")
        return QueryResult(query=query_name, result=result_df)
        
    except Exception as e:
        log.error(f"Error executing query {query_name}: {str(e)}")
        raise


def get_all_queries() -> List[Callable[[Engine], QueryResult]]:
    """Get all queries.

    Returns:
        List[Callable[[Engine], QueryResult]]: A list of all queries.
    """
    return [
        query_delivery_date_difference,
        query_global_ammount_order_status,
        query_revenue_by_month_year,
        query_revenue_per_state,
        query_top_10_least_revenue_categories,
        query_top_10_revenue_categories,
        query_real_vs_estimated_delivered_time,
        query_orders_per_day_and_holidays_2017,
        query_freight_value_weight_relationship,
    ]


def run_queries(database: Engine) -> Dict[str, DataFrame]:
    """Transform data based on the queries. For each query, the query is executed and
    the result is stored in the dataframe.

    Args:
        database (Engine): Database connection.

    Returns:
        Dict[str, DataFrame]: A dictionary with keys as the query file names and
        values the result of the query as a dataframe.
    """
    results = {}
    queries = get_all_queries()

    for query in queries:
        try:
            # Obtener el nombre de la consulta de la función
            query_name = query.__name__.replace('query_', '')
            print(f"\nEjecutando consulta: {query_name}")
            
            # Verificar que las tablas necesarias existan
            inspector = inspect(database)
            tables = inspector.get_table_names()
            print(f"Tablas disponibles: {tables}")
            
            # Ejecutar la consulta
            query_result = query(database)
            
            if isinstance(query_result.result, DataFrame):
                if query_result.result.empty:
                    print(f"Advertencia: La consulta {query_name} devolvió un resultado vacío")
                else:
                    print(f"Consulta {query_name} completada. Filas: {len(query_result.result)}")
            else:
                print(f"Advertencia: La consulta {query_name} no devolvió un DataFrame")
            
            results[query_result.query] = query_result.result
            
        except Exception as e:
            print(f"Error ejecutando consulta {query_name}: {str(e)}")
            raise
