import logging
from typing import Optional, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_logger(name: str) -> logging.Logger:
    """Configure et retourne un logger"""
    return logging.getLogger(name)

def validate_dataframe(df: pd.DataFrame, required_cols: Optional[list] = None) -> bool:
    """Valide la structure du DataFrame"""
    if df is None or df.empty:
        logger.error("DataFrame vide ou null")
        return False
    
    if required_cols:
        missing = set(required_cols) - set(df.columns)
        if missing:
            logger.warning(f"Colonnes manquantes: {missing}")
            return False
    
    return True

def create_advanced_gauge(score: float, title: str = "Score de Risque") -> go.Figure:
    """Crée une jauge avancée avec indicateurs multiples"""
    
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'indicator'}, {'type': 'bar'}]],
        subplot_titles=(title, "Facteurs de risque"),
        column_widths=[0.6, 0.4]
    )
    
    # Jauge principale
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=score * 100,
            delta={'reference': 50, 'relative': True},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "darkred" if score > 0.7 else "orange" if score > 0.3 else "green"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "lightsalmon"},
                    {'range': [70, 100], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': score * 100
                }
            }
        ),
        row=1, col=1
    )
    
    # Graphique des facteurs (exemple)
    factors = ['Inactivité', 'Baisse flux', 'Clôtures', 'Non-équipement']
    values = [score, score*0.8, score*0.6, score*0.4]
    
    fig.add_trace(
        go.Bar(
            x=factors,
            y=values,
            marker_color=['#dc3545' if v > 0.7 else '#fd7e14' if v > 0.3 else '#28a745' for v in values],
            text=[f"{v:.1%}" for v in values],
            textposition='auto',
        ),
        row=1, col=2
    )
    
    fig.update_layout(height=300, showlegend=False)
    return fig

def format_currency(value: float) -> str:
    """Formate un nombre en FCFA"""
    return f"{value:,.0f} FCFA"

def format_percentage(value: float, decimals: int = 1) -> str:
    """Formate un nombre en pourcentage"""
    return f"{value:.{decimals}%}"

def get_timestamp() -> str:
    """Retourne un timestamp formaté"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")