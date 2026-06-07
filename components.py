# -*- coding: utf-8 -*-
import streamlit as st
from typing import Any, Optional
import pandas as pd
from config import UIConfig, RiskLevels

class UIComponents:
    """Composants d'interface réutilisables"""
    
    def __init__(self, config: UIConfig = UIConfig()):
        self.config = config
    
    def render_header(self):
        """Rend le header personnalisé"""
        st.markdown(f"""
        <div class="main-header" style="background: {self.config.color_gradient};">
            <h1>{self.config.page_icon} {self.config.page_title}</h1>
            <p>Anticipez le désengagement et priorisez vos actions de rétention avec l'intelligence artificielle</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_metric_card(self, label: str, value: Any, trend: Optional[float] = None, color: Optional[str] = None):
        """Rend une carte métrique stylisée"""
        trend_html = ''
        if trend is not None and trend != 0:
            arrow = "📈" if trend > 0 else "📉"
            trend_color = "#28a745" if trend > 0 else "#dc3545"
            trend_html = f'<div style="font-size: 0.8rem; color: {trend_color};">{arrow} {abs(trend):.1f}%</div>'
        
        color_style = f'color: {color};' if color else ''
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="{color_style}">{value}</div>
            {trend_html}
        </div>
        """, unsafe_allow_html=True)
    
    def render_risk_badge(self, score: float) -> str:
        """Rend un badge de risque HTML"""
        label, badge_class, _ = RiskLevels.get_level(score)
        return f'<span class="{badge_class}">{label}</span>'
    
    def render_data_table(self, df: pd.DataFrame, max_rows: int = 15):
        """Rend un tableau de données stylisé"""
        st.markdown(df.head(max_rows).to_html(escape=False, index=False), unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Rend la barre latérale complète"""
        with st.sidebar:
            st.markdown("### ⚙️ Configuration")
            st.markdown("---")
            
            st.markdown(f"""
            <div style="text-align: center; margin: 1rem 0;">
                <div style="background: {self.config.primary_color}; width: 60px; height: 60px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                    <span style="font-size: 2rem;">🏦</span>
                </div>
                <p style="font-weight: 600; color: {self.config.primary_color};">BOA Togo</p>
                <p style="font-size: 0.8rem; color: #6c757d;">Direction de la Gestion des Risques</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            uploaded_file = st.file_uploader(
                "📂 Importer un fichier Excel",
                type=["xlsx", "xls"],
                help="Le fichier doit contenir les colonnes similaires au dataset d'entraînement."
            )
            
            st.markdown("---")
            st.markdown("""
            ### 📋 Format attendu
            - Colonnes standardisées
            - Données transactionnelles
            - Informations produits
            """)
            
            st.markdown("---")
            st.markdown("""
            <div style="font-size: 0.75rem; color: #6c757d; text-align: center;">
                <p>🔒 Données sécurisées<br>📊 Modèle XGBoost v1.0<br>🎯 Précision: 96%</p>
            </div>
            """, unsafe_allow_html=True)
            
            return uploaded_file

class CSSManager:
    """Gère les styles CSS dynamiques"""
    
    @staticmethod
    def load_custom_css(config: UIConfig):
        """Charge les CSS personnalisés"""
        st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            html, body, [class*="css"] {{
                font-family: 'Inter', sans-serif;
            }}
            
            .main-header {{
                background: {config.color_gradient};
                padding: 1.5rem 2rem;
                border-radius: 15px;
                margin-bottom: 2rem;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            
            .main-header h1 {{
                color: white !important;
                font-size: 2.2rem !important;
                font-weight: 700 !important;
                margin-bottom: 0.5rem !important;
            }}
            
            .main-header p {{
                color: rgba(255,255,255,0.9) !important;
                font-size: 1rem !important;
            }}
            
            .metric-card {{
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                border-radius: 15px;
                padding: 1.2rem;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                border: 1px solid rgba(0,0,0,0.05);
                text-align: center;
                transition: transform 0.2s ease;
                height: 120px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }}
            
            .metric-card:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            }}
            
            .metric-value {{
                font-size: 2rem;
                font-weight: 700;
                margin: 0.5rem 0;
            }}
            
            .metric-label {{
                font-size: 0.85rem;
                color: #6c757d;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
                margin-bottom: 0.5rem;
            }}
            
            .badge-sain {{
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                display: inline-block;
            }}
            
            .badge-modere {{
                background: linear-gradient(135deg, #fd7e14 0%, #ffc107 100%);
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                display: inline-block;
            }}
            
            .badge-critique {{
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
                display: inline-block;
                animation: pulse 1.5s infinite;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.7; }}
            }}
            
            .section-title {{
                font-size: 1.3rem;
                font-weight: 600;
                margin: 1.5rem 0 1rem 0;
                padding-bottom: 0.5rem;
                border-bottom: 3px solid {config.primary_color};
                display: inline-block;
            }}
            
            .upload-zone {{
                border: 2px dashed {config.primary_color};
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                background: rgba(26, 71, 42, 0.02);
                transition: all 0.3s ease;
            }}
            
            .upload-zone:hover {{
                background: rgba(26, 71, 42, 0.05);
                border-color: {config.secondary_color};
            }}
            
            .footer {{
                text-align: center;
                padding: 2rem;
                margin-top: 3rem;
                color: #6c757d;
                font-size: 0.8rem;
                border-top: 1px solid rgba(0,0,0,0.05);
            }}
            
            .stButton > button, .stDownloadButton > button {{
                background: {config.color_gradient};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0.5rem 1.5rem;
                font-weight: 500;
                transition: all 0.3s ease;
                width: 100%;
            }}
            
            .stButton > button:hover, .stDownloadButton > button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(26, 71, 42, 0.3);
            }}
            
            .stDataFrame {{
                border-radius: 10px;
                overflow: hidden;
            }}
        </style>
        """, unsafe_allow_html=True)