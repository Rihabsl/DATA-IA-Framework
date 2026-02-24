"""
Tests automatisés pour le Data Quality Framework.
"""
import pytest
import pandas as pd
from core.checks.completeness import CompletenessChecker
from core.checks.duplicates   import DuplicatesChecker
from core.checks.anomalies    import AnomaliesChecker


@pytest.fixture
def df_propre():
    """Dataset sans aucun problème."""
    return pd.DataFrame({
        'id'          : [1, 2, 3],
        'nom'         : ['Martin', 'Dupont', 'Bernard'],
        'prenom'      : ['Alice', 'Bob', 'Claire'],
        'email'       : ['alice@test.com', 'bob@test.com', 'claire@test.com'],
        'departement' : ['IT', 'RH', 'Finance'],
        'salaire'     : [50000, 60000, 55000],
    })


@pytest.fixture
def df_problemes():
    """Dataset avec des problèmes intentionnels."""
    return pd.DataFrame({
        'id'          : [1, 2, 3, 3],
        'nom'         : ['Martin', 'Dupont', 'Bernard', 'Bernard'],
        'prenom'      : ['Alice', 'Bob', 'Claire', 'Claire'],
        'email'       : ['alice@test.com', None, 'claire@test.com', 'claire@test.com'],
        'departement' : ['IT', None, 'Finance', 'Finance'],
        'salaire'     : [50000, 600, 55000, 55000],
    })


# ── TESTS COMPLÉTUDE ──────────────────────────────────────────
class TestCompleteness:

    def test_donnees_propres_score_100(self, df_propre):
        """Un dataset propre doit avoir un score de 100%."""
        c = CompletenessChecker(['nom', 'prenom', 'email', 'departement'])
        result = c.check(df_propre)
        assert result['score'] == 100.0
        assert len(result['problemes']) == 0

    def test_detecte_valeurs_manquantes(self, df_problemes):
        """Doit détecter les emails et départements manquants."""
        c = CompletenessChecker(['nom', 'prenom', 'email', 'departement'])
        result = c.check(df_problemes)
        assert len(result['problemes']) > 0
        colonnes_problemes = [p['colonne'] for p in result['problemes']]
        assert 'email' in colonnes_problemes

    def test_score_diminue_avec_manquants(self, df_problemes):
        """Le score doit être inférieur à 100 si des valeurs manquent."""
        c = CompletenessChecker(['nom', 'prenom', 'email', 'departement'])
        result = c.check(df_problemes)
        assert result['score'] < 100.0


# ── TESTS DOUBLONS ────────────────────────────────────────────
class TestDuplicates:

    def test_donnees_propres_zero_doublons(self, df_propre):
        """Un dataset propre ne doit avoir aucun doublon."""
        d = DuplicatesChecker(key_columns=['nom', 'prenom', 'email'])
        result = d.check(df_propre)
        assert result['doublons_exacts'] == 0

    def test_detecte_doublons(self, df_problemes):
        """Doit détecter les lignes dupliquées."""
        d = DuplicatesChecker(key_columns=['nom', 'prenom', 'email'])
        result = d.check(df_problemes)
        assert result['doublons_exacts'] > 0

    def test_score_parfait_sans_doublons(self, df_propre):
        """Score doit être 100% sans doublons."""
        d = DuplicatesChecker(key_columns=['nom', 'prenom'])
        result = d.check(df_propre)
        assert result['score'] == 100.0


# ── TESTS ANOMALIES ───────────────────────────────────────────
class TestAnomalies:

    def test_salaires_normaux_aucune_anomalie(self, df_propre):
        """Des salaires normaux ne doivent pas déclencher d'alerte."""
        a = AnomaliesChecker({'salaire': {'min': 20000, 'max': 150000}})
        result = a.check(df_propre)
        assert len(result['problemes']) == 0

    def test_detecte_salaire_aberrant(self, df_problemes):
        """Un salaire de 600€ doit être détecté comme aberrant."""
        a = AnomaliesChecker({'salaire': {'min': 20000, 'max': 150000}})
        result = a.check(df_problemes)
        assert len(result['problemes']) > 0
        assert result['problemes'][0]['trop_bas'] > 0

    def test_score_diminue_avec_anomalies(self, df_problemes):
        """Le score doit baisser en présence d'anomalies."""
        a = AnomaliesChecker({'salaire': {'min': 20000, 'max': 150000}})
        result = a.check(df_problemes)
        assert result['score'] < 100.0