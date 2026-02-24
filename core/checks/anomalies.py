"""
anomalies.py
Détecte les valeurs aberrantes dans un DataFrame.
"""
import pandas as pd
import numpy as np


class AnomaliesChecker:
    """Détecte les valeurs aberrantes dans les colonnes numériques."""

    def __init__(self, numeric_columns: dict):
        """
        Args:
            numeric_columns: dict avec min/max attendus
            ex: {'salaire': {'min': 20000, 'max': 150000}}
        """
        self.numeric_columns = numeric_columns
        self.results = {}

    def check(self, df: pd.DataFrame) -> dict:
        total_rows = len(df)
        issues = []

        for col, limits in self.numeric_columns.items():
            if col not in df.columns:
                continue

            col_data = pd.to_numeric(df[col], errors='coerce')

            # Méthode 1 — vérification min/max
            too_low  = (col_data < limits['min']).sum()
            too_high = (col_data > limits['max']).sum()

            # Méthode 2 — détection statistique (IQR)
            Q1  = col_data.quantile(0.25)
            Q3  = col_data.quantile(0.75)
            IQR = Q3 - Q1
            outliers_iqr = ((col_data < Q1 - 1.5*IQR) |
                           (col_data > Q3 + 1.5*IQR)).sum()

            if too_low > 0 or too_high > 0:
                issues.append({
                    'colonne'     : col,
                    'trop_bas'    : int(too_low),
                    'trop_haut'   : int(too_high),
                    'outliers_iqr': int(outliers_iqr),
                    'min_attendu' : limits['min'],
                    'max_attendu' : limits['max'],
                    'min_reel'    : float(col_data.min()),
                    'max_reel'    : float(col_data.max()),
                    'moyenne'     : round(float(col_data.mean()), 2),
                })

        self.results = {
            'total_lignes': total_rows,
            'problemes'   : issues,
            'score'       : round(100 - (sum(
                p['trop_bas'] + p['trop_haut'] for p in issues
            ) / total_rows * 100), 1)
        }
        return self.results

    def summary(self) -> str:
        if not self.results:
            return "Aucune vérification effectuée."
        lines = [
            f"\n{'='*50}",
            f"  RAPPORT ANOMALIES",
            f"{'='*50}",
            f"  Lignes analysées : {self.results['total_lignes']}",
            f"  Score qualité    : {self.results['score']}%",
        ]
        for p in self.results['problemes']:
            lines.append(f"\n  Colonne '{p['colonne']}'")
            lines.append(f"     Valeur min réelle : {p['min_reel']} (attendu >= {p['min_attendu']})")
            lines.append(f"     Valeur max réelle : {p['max_reel']} (attendu <= {p['max_attendu']})")
            lines.append(f"     Trop bas  : {p['trop_bas']} valeur(s)")
            lines.append(f"     Trop haut : {p['trop_haut']} valeur(s)")
            lines.append(f"     Outliers IQR : {p['outliers_iqr']} valeur(s)")
            lines.append(f"     Moyenne   : {p['moyenne']}")
        if not self.results['problemes']:
            lines.append("\n  Aucune anomalie détectée !")
        lines.append(f"\n{'='*50}")
        return '\n'.join(lines)


if __name__ == '__main__':
    df = pd.read_csv('data/employees.csv')
    checker = AnomaliesChecker(
        numeric_columns={
            'salaire': {'min': 20000, 'max': 150000}
        }
    )
    checker.check(df)
    print(checker.summary())