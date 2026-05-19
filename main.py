

import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# ----------------------------------------
# LOAD MODEL + TRAINING COLUMNS
# ----------------------------------------

model = joblib.load("best_model.pkl")

training_columns = joblib.load("training_columns.pkl")


# ----------------------------------------
# AGE GROUP FUNCTION
# ----------------------------------------

def get_age_group(age):

    if 18 <= age <= 25:
        return '18-25'

    elif 26 <= age <= 35:
        return '26-35'

    elif 36 <= age <= 45:
        return '36-45'

    elif 46 <= age <= 55:
        return '46-55'

    else:
        return '56-70'


# ----------------------------------------
# PREDICTION FUNCTION
# ----------------------------------------

def predict_price(data):

    # Convert input into dataframe
    df = pd.DataFrame([data])

    # ----------------------------------------
    # CREATE AGE GROUP
    # ----------------------------------------

    df['age_group'] = df['age'].apply(get_age_group)

    # Drop age column
    df.drop('age', axis=1, inplace=True)

    # ----------------------------------------
    # CF_AB_SCORE
    # ----------------------------------------

    frequency_map = {
        '0-2 times': 1,
        '3-4 times': 2,
        '5-7 times': 3
    }

    awareness_map = {
        '0 to 1': 1,
        '2 to 4': 2,
        'above 4': 3
    }

    df['frequency_score'] = df['consume_frequency(weekly)'].map(frequency_map)

    df['awareness_score'] = df['awareness_of_other_brands'].map(awareness_map)

    df['cf_ab_score'] = (
        df['frequency_score'] /
        (df['awareness_score'] + df['frequency_score'])
    ).round(2)

    # ----------------------------------------
    # ZAS SCORE
    # ----------------------------------------

    zone_map = {
        'Rural': 1,
        'Semi-Urban': 2,
        'Urban': 3,
        'Metro': 4
    }

    income_map = {
        'Not Reported': 0,
        '<10L': 1,
        '10L- 15L': 2,
        '16L- 25L': 3,
        '26L- 35L': 4,
        '>35L': 5
    }

    df['zone_score'] = df['zone'].map(zone_map)

    df['income_score'] = df['income_levels'].map(income_map)

    df['zas_score'] = df['zone_score'] * df['income_score']

    # ----------------------------------------
    # BSI
    # ----------------------------------------

    df['bsi'] = (
        (df['current_brand'] != 'Established') &
        (
            (df['reasons_for_choosing_brands'] == 'Price') |
            (df['reasons_for_choosing_brands'] == 'Quality')
        )
    ).astype(int)

    # ----------------------------------------
    # DROP TEMPORARY SCORE COLUMNS
    # ----------------------------------------

    df.drop(
        ['frequency_score',
         'awareness_score',
         'zone_score',
         'income_score'],
        axis=1,
        inplace=True
    )

    # ----------------------------------------
    # LABEL ENCODING
    # ----------------------------------------

    label_encode_cols = [
        'age_group',
        'income_levels',
        'health_concerns',
        'consume_frequency(weekly)',
        'preferable_consumption_size'
    ]

    # Recreate notebook-style encoding
    for col in label_encode_cols:

        le = LabelEncoder()

        df[col] = le.fit_transform(df[col])

    # ----------------------------------------
    # ONE HOT ENCODING
    # ----------------------------------------

    df = pd.get_dummies(df, drop_first=True)

    # ----------------------------------------
    # ALIGN COLUMNS
    # ----------------------------------------

    df = df.reindex(columns=training_columns, fill_value=0)

    # ----------------------------------------
    # PREDICTION
    # ----------------------------------------

    prediction = model.predict(df)[0]

    # ----------------------------------------
    # REVERSE TARGET ENCODING
    # ----------------------------------------

    price_range_map = {
        0: '100-150',
        1: '200-250',
        2: '150-200',
        3: '50-100'
    }

    return price_range_map[prediction]

