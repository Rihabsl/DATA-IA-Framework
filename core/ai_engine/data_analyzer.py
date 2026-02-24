"""
data_analyzer.py
Utilise Claude pour analyser les problèmes de qualité des données
et suggérer des corrections concrètes.
"""
import os
import json
import anthropic
from dotenv import load_dotenv

load_dotenv()


class DataAnalyzer:
    """Analyse les rapports de qualité via Claude IA."""

    def __init__(self, model: str = 'claude-opus-4-6'):
        self.client = anthropic.Anthropic(
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        self.model = model

    def analyze(self, rapport_completude: dict,
                rapport_doublons: dict,
                rapport_anomalies: dict) -> dict:
        """
        Envoie tous les rapports à Claude et reçoit une analyse globale.
        """
        prompt = f"""
Tu es un expert en qualité des données (Data Quality Engineer).
Analyse ces rapports de qualité sur un dataset d'employés RH.

RAPPORT COMPLÉTUDE :
{json.dumps(rapport_completude, ensure_ascii=False, indent=2)}

RAPPORT DOUBLONS :
{json.dumps(rapport_doublons, ensure_ascii=False, indent=2)}

RAPPORT ANOMALIES :
{json.dumps(rapport_anomalies, ensure_ascii=False, indent=2)}

Réponds UNIQUEMENT avec un JSON valide :
{{
  "score_global": <nombre entre 0 et 100>,
  "niveau_risque": "critique|élevé|moyen|faible",
  "resume": "Résumé en 2 phrases simples pour un manager non technique",
  "problemes_prioritaires": [
    {{"rang": 1, "probleme": "...", "impact": "...", "correction": "..."}}
  ],
  "recommandations": ["recommandation 1", "recommandation 2", "recommandation 3"],
  "pret_production": true ou false
}}
"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            messages=[{'role': 'user', 'content': prompt}]
        )

        raw = response.content[0].text.strip()
        try:
            start = raw.find('{')
            end   = raw.rfind('}') + 1
            return json.loads(raw[start:end])
        except Exception:
            return {'erreur': raw}

    def format_report(self, analysis: dict) -> str:
        """Formate l'analyse en rapport lisible."""
        risk_colors = {
            'critique': '🔴',
            'élevé'   : '🟠',
            'moyen'   : '🟡',
            'faible'  : '🟢'
        }
        risk = analysis.get('niveau_risque', 'inconnu')
        icon = risk_colors.get(risk, '⚪')
        pret = '✅ OUI' if analysis.get('pret_production') else '❌ NON'

        lines = [
            f"\n{'='*55}",
            f"  ANALYSE IA — DATA QUALITY REPORT",
            f"{'='*55}",
            f"  Score global     : {analysis.get('score_global', 'N/A')}/100",
            f"  Niveau de risque : {icon} {risk.upper()}",
            f"  Prêt production  : {pret}",
            f"\n  RÉSUMÉ :",
            f"  {analysis.get('resume', 'N/A')}",
            f"\n  PROBLÈMES PRIORITAIRES :",
        ]

        for p in analysis.get('problemes_prioritaires', []):
            lines.append(f"\n  #{p.get('rang')} {p.get('probleme')}")
            lines.append(f"     Impact     : {p.get('impact')}")
            lines.append(f"     Correction : {p.get('correction')}")

        lines.append(f"\n  RECOMMANDATIONS :")
        for i, r in enumerate(analysis.get('recommandations', []), 1):
            lines.append(f"  {i}. {r}")

        lines.append(f"\n{'='*55}")
        return '\n'.join(lines)


if __name__ == '__main__':
    # Simuler des rapports sans avoir besoin de crédits
    rapport_completude = {
        'total_lignes': 102,
        'score': 60.0,
        'problemes': [
            {'colonne': 'email', 'manquants': 9, 'pourcentage': 8.82},
            {'colonne': 'departement', 'manquants': 24, 'pourcentage': 23.53}
        ]
    }
    rapport_doublons = {
        'total_lignes': 102,
        'score': 98.0,
        'doublons_exacts': 2,
        'doublons_cles': 2,
        'problemes': [{'type': 'Doublons exacts', 'nombre': 2}]
    }
    rapport_anomalies = {
        'total_lignes': 102,
        'score': 94.1,
        'problemes': [
            {'colonne': 'salaire', 'trop_bas': 6,
             'min_reel': 547.0, 'moyenne': 57307.94}
        ]
    }

    analyzer = DataAnalyzer()
    result   = analyzer.analyze(
        rapport_completude,
        rapport_doublons,
        rapport_anomalies
    )
    print(analyzer.format_report(result))