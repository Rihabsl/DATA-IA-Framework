"""
completeness.py
Vérifie les valeurs manquantes dans un DataFrame.
"""
import pandas as pd


class CompletenessChecker:
    """Vérifie que toutes les colonnes obligatoires sont remplies."""

    def __init__(self, required_columns: list):
        self.required_columns = required_columns
        self.results = {}

    def check(self, df: pd.DataFrame) -> dict:
        """
        Analyse les valeurs manquantes.
        Retourne un rapport détaillé par colonne.
        """
        total_rows = len(df)
        issues = []

        for col in self.required_columns:
            if col not in df.columns:
                issues.append({
                    'colonne'   : col,
                    'probleme'  : 'Colonne absente du fichier',
                    'manquants' : total_rows,
                    'pourcentage': 100.0
                })
                continue

            missing = df[col].isna().sum()
            pct = round((missing / total_rows) * 100, 2)

            if missing > 0:
                issues.append({
                    'colonne'    : col,
                    'probleme'   : 'Valeurs manquantes',
                    'manquants'  : int(missing),
                    'pourcentage': pct
                })

        self.results = {
            'total_lignes' : total_rows,
            'colonnes_verifiees': len(self.required_columns),
            'problemes'    : issues,
            'score'        : round(100 - (len(issues) / len(self.required_columns) * 100), 1)
        }
        return self.results

    def summary(self) -> str:
        """Affiche un résumé lisible dans le terminal."""
        if not self.results:
            return "Aucune vérification effectuée."
        lines = [
            f"\n{'='*50}",
            f"  RAPPORT COMPLÉTUDE",
            f"{'='*50}",
            f"  Lignes analysées : {self.results['total_lignes']}",
            f"  Score qualité    : {self.results['score']}%",
            f"  Problèmes trouvés: {len(self.results['problemes'])}",
        ]
        for p in self.results['problemes']:
            lines.append(f"\n  Colonne '{p['colonne']}'")
            lines.append(f"     {p['probleme']} : {p['manquants']} ({p['pourcentage']}%)")
        lines.append(f"\n{'='*50}")
        return '\n'.join(lines)


if __name__ == '__main__':
    df = pd.read_csv('data/employees.csv')
    checker = CompletenessChecker(
        required_columns=['nom', 'prenom', 'email', 'departement', 'salaire']
    )
    checker.check(df)
    print(checker.summary())