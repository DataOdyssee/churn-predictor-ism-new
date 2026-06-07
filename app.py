# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from config import UIConfig, ModelConfig
from components import UIComponents, CSSManager
from scoring_engine import ScoringEngine
from utils import setup_logger, validate_dataframe, format_percentage, get_timestamp

# Initialisation
logger = setup_logger(__name__)
ui_config = UIConfig()
model_config = ModelConfig()

# Configuration page
st.set_page_config(
    page_title=ui_config.page_title,
    page_icon=ui_config.page_icon,
    layout=ui_config.layout,
    initial_sidebar_state="expanded"
)

# Chargement CSS
CSSManager.load_custom_css(ui_config)

# Initialisation des composants
ui = UIComponents(ui_config)
scoring_engine = ScoringEngine(model_config)

def render_metrics(df_results: pd.DataFrame):
    """Rend les métriques principales"""
    total = len(df_results)
    sains = len(df_results[df_results['Niveau_Risque'] == '🟢 Sain'])
    alertes = len(df_results[df_results['Niveau_Risque'] == '🟠 Alerte Modérée'])
    critiques = len(df_results[df_results['Niveau_Risque'] == '🔴 Alerte Critique'])
    
    # Utiliser des conteneurs avec des couleurs explicites
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1rem; 
                        border-radius: 10px; 
                        text-align: center;
                        color: white;">
                <div style="font-size: 0.8rem; opacity: 0.9;">👥 TOTAL CLIENTS</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0; color: white;">{total:,}</div>
                <div style="font-size: 0.7rem;">Portefeuille analysé</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                        padding: 1rem; 
                        border-radius: 10px; 
                        text-align: center;
                        color: white;">
                <div style="font-size: 0.8rem; opacity: 0.9;">🟢 CLIENTS SAINS</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">{sains:,}</div>
                <div style="font-size: 0.7rem;">{sains/total*100:.1f}% du portefeuille</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #fd7e14 0%, #ffc107 100%); 
                        padding: 1rem; 
                        border-radius: 10px; 
                        text-align: center;
                        color: white;">
                <div style="font-size: 0.8rem; opacity: 0.9;">🟠 ALERTE MODÉRÉE</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">{alertes:,}</div>
                <div style="font-size: 0.7rem;">À surveiller</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
                        padding: 1rem; 
                        border-radius: 10px; 
                        text-align: center;
                        color: white;">
                <div style="font-size: 0.8rem; opacity: 0.9;">🔴 ALERTE CRITIQUE</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">{critiques:,}</div>
                <div style="font-size: 0.7rem;">Action immédiate</div>
            </div>
            """, 
            unsafe_allow_html=True
        )

def render_charts(df_results: pd.DataFrame):
    """Rend les graphiques d'analyse"""
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist = px.histogram(
            df_results, x='Score_Risque', nbins=50,
            title="Distribution des Scores de Risque",
            labels={'Score_Risque': 'Probabilité d\'Inactivité', 'count': 'Nombre de clients'},
            color_discrete_sequence=[ui_config.primary_color]
        )
        fig_hist.add_vline(x=0.3, line_dash="dash", line_color="orange", annotation_text="Seuil Alerte")
        fig_hist.add_vline(x=0.7, line_dash="dash", line_color="red", annotation_text="Seuil Critique")
        fig_hist.update_layout(plot_bgcolor='white', height=400)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        risk_counts = df_results['Niveau_Risque'].value_counts()
        fig_pie = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            title="Répartition par Niveau de Risque",
            color_discrete_sequence=['#28a745', '#fd7e14', '#dc3545'],
            hole=0.4
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

def render_top_risks(df_results: pd.DataFrame):
    """Rend le top 15 des clients à risque"""
    st.markdown('<div class="section-title">🎯 TOP 15 CLIENTS À RISQUE ÉLEVÉ</div>', 
                unsafe_allow_html=True)
    
    top_risks = df_results.nlargest(15, 'Score_Risque')[['Client_ID', 'Score_Risque', 'Niveau_Risque']].copy()
    top_risks['Score_Risque'] = top_risks['Score_Risque'].apply(format_percentage)
    
    # Application des badges
    def apply_badge(row):
        score = float(row['Score_Risque'].strip('%')) / 100
        return ui.render_risk_badge(score)
    
    top_risks['Niveau_Risque'] = top_risks.apply(apply_badge, axis=1)
    
    ui.render_data_table(top_risks)

def main():
    """Point d'entrée principal"""
    ui.render_header()
    
    uploaded_file = ui.render_sidebar()
    
    if uploaded_file is not None:
        try:
            # Chargement et traitement
            with st.spinner("📊 Traitement des données en cours..."):
                df_raw = pd.read_excel(uploaded_file, sheet_name='Data')
                df_raw.columns = df_raw.columns.str.strip()
                df_raw.replace('NULL', np.nan, inplace=True)
                
                if not validate_dataframe(df_raw):
                    st.error("Format de données invalide")
                    return
                
                # Scoring
                df_results = scoring_engine.predict(df_raw)
            
            # Affichage des résultats
            render_metrics(df_results)
            render_charts(df_results)
            render_top_risks(df_results)
            
            # Export
            st.markdown('<div class="section-title">💾 EXPORT DES DONNÉES</div>', 
                       unsafe_allow_html=True)
            
            csv_data = df_results[['Client_ID', 'Score_Risque', 'Niveau_Risque']].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger la liste des clients à risque (CSV)",
                data=csv_data,
                file_name=f"clients_a_risque_{get_timestamp()}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        except Exception as e:
            logger.error(f"Erreur: {e}")
            st.error(f"❌ Une erreur s'est produite : {str(e)}")
            st.info("💡 Vérifiez que le fichier Excel a la structure attendue.")
    
    else:
        # État initial
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div class="upload-zone">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
                <h3>Bienvenue sur la plateforme de scoring</h3>
                <p>Chargez un fichier Excel contenant les données clients<br>pour générer une analyse prédictive complète.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div class="footer">
        <p>BOA Togo - Direction de la Gestion des Risques | Modèle XGBoost - Précision {model_config.model_accuracy:.0%} | Données confidentielles</p>
        <p style="font-size: 0.7rem;">© 2026 - Tous droits réservés</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()