"""
reporter.py
Lance tous les checks et génère le rapport final.
"""
import pandas as pd
from core.checks.completeness import CompletenessChecker
from core.checks.duplicates   import DuplicatesChecker
from core.checks.anomalies    import AnomaliesChecker


class DataQualityReporter:
    """Lance tous les checks et produit un rapport global."""

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df       = pd.read_csv(csv_path)
        self.rapports = {}

    def run_all_checks(self):
        print(f"\n Fichier analysé : {self.csv_path}")
        print(f" {len(self.df)} lignes chargées\n")

        # Check 1 — Complétude
        print(" Vérification 1/3 — Complétude...")
        c = CompletenessChecker(
            required_columns=['nom', 'prenom', 'email', 'departement', 'salaire']
        )
        self.rapports['completude'] = c.check(self.df)
        print(c.summary())

        # Check 2 — Doublons
        print(" Vérification 2/3 — Doublons...")
        d = DuplicatesChecker(key_columns=['nom', 'prenom', 'email'])
        self.rapports['doublons'] = d.check(self.df)
        print(d.summary())

        # Check 3 — Anomalies
        print(" Vérification 3/3 — Anomalies...")
        a = AnomaliesChecker(
            numeric_columns={'salaire': {'min': 20000, 'max': 150000}}
        )
        self.rapports['anomalies'] = a.check(self.df)
        print(a.summary())

        # Score global
        scores = [
            self.rapports['completude']['score'],
            self.rapports['doublons']['score'],
            self.rapports['anomalies']['score'],
        ]
        score_global = round(sum(scores) / len(scores), 1)

        print(f"\n{'='*50}")
        print(f"  SCORE GLOBAL DE QUALITÉ : {score_global}/100")
        if score_global >= 90:
            print("   Données prêtes pour la production")
        elif score_global >= 70:
            print("  🟡 Corrections recommandées avant production")
        else:
            print("  🔴 Données NON prêtes — corrections urgentes")
        print(f"{'='*50}\n")

        return self.rapports


if __name__ == '__main__':
    reporter = DataQualityReporter('data/employees.csv')
    reporter.run_all_checks()