# Data Quality Framework with AI

[![CI](https://github.com/Rihabsl/data-quality-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/Rihabsl/data-quality-framework/actions)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Framework automatisé de contrôle qualité des données RH, combinant des règles métier et l'analyse par IA (Claude d'Anthropic).

---

## Fonctionnalités

| Module | Description |
|--------|-------------|
| Complétude | Détecte les valeurs manquantes dans les colonnes obligatoires |
| Doublons | Identifie les lignes dupliquées sur les colonnes clés |
| Anomalies | Détecte les valeurs aberrantes (ex: salaire de 500 euros) |
| Analyse IA | Claude explique les problèmes et suggère des corrections |
| Score global | Note la qualité des données de 0 à 100 |

---

## Démarrage rapide
```bash
git clone https://github.com/Rihabsl/data-quality-framework.git
cd data-quality-framework
python -m venv venv && venv\Scripts\Activate.ps1
pip install -r requirements.txt
python data/generate_data.py
python -m core.reporter
```

---

## Architecture
```
data-quality-framework/
├── core/
│   ├── checks/
│   │   ├── completeness.py   <- valeurs manquantes
│   │   ├── duplicates.py     <- doublons
│   │   └── anomalies.py      <- valeurs aberrantes
│   ├── ai_engine/
│   │   └── data_analyzer.py  <- analyse IA via Claude
│   └── reporter.py           <- rapport global
├── data/
│   └── generate_data.py      <- génère les données de test
├── tests/
│   └── test_data_quality.py  <- 9 tests pytest
└── .github/workflows/ci.yml  <- pipeline CI/CD
```

---

## Exemple de résultat
```
Fichier analysé : data/employees.csv
102 lignes chargées

Completude    : 60%  -- 9 emails manquants, 24 departements manquants
Doublons      : 98%  -- 2 doublons detectes
Anomalies     : 94%  -- 6 salaires aberrants (ex: 547 euros)

SCORE GLOBAL : 84/100
Corrections recommandées avant production
```

---

## Lancer les tests
```bash
pytest tests/ -v
# 9 passed in 4.03s
```

---

## Stack technique

- Python 3.11 — langage principal
- pandas / numpy — analyse des données
- Claude API (Anthropic) — analyse IA des problèmes
- pytest — tests automatisés
- GitHub Actions — CI/CD automatique
- Faker — génération de données fictives réalistes

---

## Lien avec les besoins entreprise

Ce projet répond directement aux besoins d'un Data Quality Engineer :
- Identifier et évaluer les problèmes de qualité des données
- Automatiser les tests de qualité
- Documenter les problèmes trouvés
- Suggérer des corrections concrètes via IA