import pandas as pd
import random
from faker import Faker

fake = Faker('fr_FR')
random.seed(42)

def generate_employees(n=100):
    data = []
    for i in range(n):
        # Introduire intentionnellement des problèmes de qualité
        email = fake.email() if random.random() > 0.1 else None        # 10% manquants
        salary = random.randint(30000, 90000) if random.random() > 0.05 else random.randint(500, 1000)  # 5% aberrants
        dept = random.choice(['RH', 'IT', 'Finance', 'Marketing', None])  # quelques None

        data.append({
            'id'            : i + 1,
            'nom'           : fake.last_name(),
            'prenom'        : fake.first_name(),
            'email'         : email,
            'departement'   : dept,
            'salaire'       : salary,
            'date_embauche' : fake.date_between(start_date='-10y', end_date='today'),
            'actif'         : random.choice([True, False]),
        })

    # Ajouter des doublons intentionnels
    data.append(data[0].copy())
    data.append(data[1].copy())

    df = pd.DataFrame(data)
    df.to_csv('data/employees.csv', index=False)
    print(f" {len(df)} employés générés avec des problèmes de qualité intentionnels")
    print(f"   - Emails manquants : {df['email'].isna().sum()}")
    print(f"   - Doublons ajoutés : 2")
    print(f"   - Salaires aberrants : ~5%")
    return df

if __name__ == '__main__':
    generate_employees()