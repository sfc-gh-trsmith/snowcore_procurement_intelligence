"""
Data Loader utilities for Snowcore Procurement Intelligence
Handles Snowflake connections and data fetching with caching.
"""

import streamlit as st
from snowflake.snowpark import Session
import pandas as pd
from typing import Optional

from utils.query_registry import get_query


@st.cache_resource
def get_session() -> Session:
    """Get or create Snowpark session."""
    try:
        # Running in Snowflake Streamlit
        from snowflake.snowpark.context import get_active_session
        return get_active_session()
    except:
        # Running locally - use connection from secrets
        if hasattr(st, 'secrets') and 'snowflake' in st.secrets:
            return Session.builder.configs(st.secrets['snowflake']).create()
        else:
            st.error("No Snowflake connection available")
            return None


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data(query_name: str, **params) -> pd.DataFrame:
    """
    Load data using a registered query.
    
    Args:
        query_name: Name of the query in the registry
        **params: Parameters to substitute in the query
        
    Returns:
        DataFrame with query results
    """
    session = get_session()
    if session is None:
        return pd.DataFrame()
    
    query = get_query(query_name)
    
    # Substitute parameters if provided
    for key, value in params.items():
        query = query.replace(f':{key}', f"'{value}'")
    
    try:
        return session.sql(query).to_pandas()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=300)
def load_custom_query(query: str) -> pd.DataFrame:
    """Execute a custom query and return results."""
    session = get_session()
    if session is None:
        return pd.DataFrame()
    
    try:
        return session.sql(query).to_pandas()
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame()


def format_currency(value: float, currency: str = 'USD') -> str:
    """Format a number as currency."""
    if pd.isna(value):
        return '-'
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.2f}K"
    else:
        return f"${value:,.2f}"


def format_number(value: float) -> str:
    """Format a number with thousand separators."""
    if pd.isna(value):
        return '-'
    return f"{value:,.0f}"


def format_percent(value: float) -> str:
    """Format a number as percentage."""
    if pd.isna(value):
        return '-'
    return f"{value:.1f}%"


def get_risk_color(risk_level: str) -> str:
    """Get color for risk level."""
    colors = {
        'CRITICAL': '#FF0000',
        'HIGH': '#FF6B6B',
        'MEDIUM': '#FFD93D',
        'LOW': '#6BCB77',
    }
    return colors.get(risk_level, '#808080')


def get_risk_rgb(risk_level: str) -> list:
    """Get RGB color for risk level (for PyDeck)."""
    colors = {
        'CRITICAL': [255, 0, 0, 200],
        'HIGH': [255, 107, 107, 200],
        'MEDIUM': [255, 217, 61, 200],
        'LOW': [107, 203, 119, 200],
    }
    return colors.get(risk_level, [128, 128, 128, 200])
