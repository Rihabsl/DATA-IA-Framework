"""
duplicates.py
Détecte les doublons dans un DataFrame.
"""
import pandas as pd


class DuplicatesChecker:
    """Détecte les lignes dupliquées dans les données."""

    def __init__(self, key_columns: list):
        self.key_columns = key_columns
        self.results = {}

    def check(self, df: pd.DataFrame) -> dict:
        """
        Détecte les doublons sur les colonnes clés.
        """
        total_rows = len(df)

        # Doublons exacts sur toutes les colonnes
        full_duplicates = df.duplicated().sum()

        # Doublons sur les colonnes clés uniquement
        key_duplicates = df.duplicated(subset=self.key_columns).sum()
        duplicate_rows = df[df.duplicated(subset=self.key_columns, keep=False)]

        issues = []
        if full_duplicates > 0:
            issues.append({
                'type'   : 'Doublons exacts',
                'nombre' : int(full_duplicates),
                'detail' : 'Lignes identiques sur toutes les colonnes'
            })

        if key_duplicates > 0:
            issues.append({
                'type'   : 'Doublons sur colonnes clés',
                'nombre' : int(key_duplicates),
                'detail' : f"Colonnes : {', '.join(self.key_columns)}"
            })

        self.results = {
            'total_lignes'     : total_rows,
            'doublons_exacts'  : int(full_duplicates),
            'doublons_cles'    : int(key_duplicates),
            'lignes_dupliquees': duplicate_rows.to_dict('records') if len(duplicate_rows) < 20 else [],
            'problemes'        : issues,
            'score'            : round(100 - (full_duplicates / total_rows * 100), 1)
        }
        return self.results

    def summary(self) -> str:
        if not self.results:
            return "Aucune vérification effectuée."
        lines = [
            f"\n{'='*50}",
            f"  RAPPORT DOUBLONS",
            f"{'='*50}",
            f"  Lignes analysées  : {self.results['total_lignes']}",
            f"  Score qualité     : {self.results['score']}%",
            f"  Doublons exacts   : {self.results['doublons_exacts']}",
            f"  Doublons sur clés : {self.results['doublons_cles']}",
        ]
        for p in self.results['problemes']:
            lines.append(f"\n  {p['type']}")
            lines.append(f"     {p['detail']} — {p['nombre']} ligne(s)")
        if not self.results['problemes']:
            lines.append("\n  Aucun doublon détecté !")
        lines.append(f"\n{'='*50}")
        return '\n'.join(lines)


if __name__ == '__main__':
    df = pd.read_csv('data/employees.csv')
    checker = DuplicatesChecker(key_columns=['nom', 'prenom', 'email'])
    checker.check(df)
    print(checker.summary())