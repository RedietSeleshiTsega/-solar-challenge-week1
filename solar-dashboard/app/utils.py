import pandas as pd
from pathlib import Path

def load_data():
    current_dir = Path(__file__).parent
    data_dir = current_dir.parent.parent / "data"

    country_files = {
        'benin': 'benin-malanville_clean.csv',
        'sierra_leone': 'sierraleone-bumbuna_clean.csv',
        'togo': 'togo_dapaong_clean.csv'
    }

    dfs = []

    for country, filename in country_files.items():
        filepath = data_dir / filename
        if not filepath.exists():
            available_files = [f.name for f in data_dir.glob('*.csv')]
            raise FileNotFoundError(
                f"Data file '{filename}' not found in {data_dir}.\n"
                f"Available files: {available_files}"
            )

        df = pd.read_csv(filepath)
        if df.empty:
            raise ValueError(f"File '{filename}' is empty")

        df['Country'] = country.replace('_', ' ').title()
        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)

    loaded_countries = combined_df['Country'].unique()
    expected_countries = ['Benin', 'Sierra Leone', 'Togo']
    if set(loaded_countries) != set(expected_countries):
        raise ValueError(
            f"Country mismatch. Loaded: {loaded_countries}, Expected: {expected_countries}"
        )

    return combined_df

def get_region_stats(df):
    region_cols = ['GHI', 'DNI', 'DHI']
    stats = df.groupby(['Country'])[region_cols].mean().reset_index()
    stats = stats.sort_values(by='GHI', ascending=False)
    return stats
