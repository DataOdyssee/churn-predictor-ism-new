from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

@dataclass(frozen=True)
class ModelConfig:
    """Configuration du modèle ML"""
    model_path: Path = Path('model_attrition_xgb.json')
    scaler_path: Path = Path('robust_scaler.pkl')
    risk_thresholds: Tuple[float, float] = (0.3, 0.7)
    model_accuracy: float = 0.96
    
@dataclass(frozen=True)
class UIConfig:
    """Configuration de l'interface"""
    page_title: str = "BOA Togo - Scoring Attrition"
    page_icon: str = "🏦"
    layout: str = "wide"
    primary_color: str = "#1a472a"
    secondary_color: str = "#2d6a4f"
    accent_color: str = "#20c997"
    warning_color: str = "#fd7e14"
    danger_color: str = "#dc3545"
    
    @property
    def color_gradient(self) -> str:
        return f"linear-gradient(135deg, {self.primary_color} 0%, {self.secondary_color} 100%)"

class RiskLevels:
    """Niveaux de risque standardisés"""
    LOW = ("🟢 Sain", "badge-sain", 0.3)
    MEDIUM = ("🟠 Alerte Modérée", "badge-modere", 0.7)
    HIGH = ("🔴 Alerte Critique", "badge-critique", 1.0)
    
    @classmethod
    def get_level(cls, score: float) -> tuple:
        if score < cls.LOW[2]:
            return cls.LOW
        elif score < cls.MEDIUM[2]:
            return cls.MEDIUM
        return cls.HIGH