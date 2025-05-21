import pandas as pd
from pathlib import Path
import os

def load_data():
    """Load and combine solar data from multiple countries with robust path handling
    
    Returns:
        pd.DataFrame: Combined dataframe with solar metrics and country info
        
    Raises:
        FileNotFoundError: If data files are missing
        ValueError: If data validation fails
    """
    
    possible_data_dirs = [
       
        Path(__file__).parent.parent.parent / "data",  
        Path(__file__).parent.parent / "data",        
        Path(__file__).parent / "data",                
        
        
        Path("/mount/src/solar-challenge-week1/data"),
        Path("/app/solar-challenge-week1/data")
    ]

    country_files = {
        'benin': 'benin-malanville_clean.csv',
        'sierra_leone': 'sierraleone-bumbuna_clean.csv',
        'togo': 'togo_dapaong_clean.csv'
    }

    dfs = []
    found_data_dir = None

    
    for data_dir in possible_data_dirs:
        try:
            
            test_file = data_dir / country_files['benin']
            if test_file.exists():
                found_data_dir = data_dir
                print(f"Found data directory at: {data_dir}")
                break
        except Exception:
            continue

    if not found_data_dir:
        searched_paths = "\n".join([str(p) for p in possible_data_dirs])
        raise FileNotFoundError(
            f"Could not find data files in any of these locations:\n{searched_paths}\n"
            f"Required files: {list(country_files.values())}"
        )

    
    for country, filename in country_files.items():
        filepath = found_data_dir / filename
        
        try:
            df = pd.read_csv(filepath)
            
            
            if df.empty:
                raise ValueError(f"File '{filename}' is empty")
                
            
            required_columns = ['GHI', 'DNI', 'DHI']
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing columns in {filename}: {missing_cols}")

           
            df['Country'] = country.replace('_', ' ').title()
            dfs.append(df)
            
        except Exception as e:
            raise Exception(f"Error processing {filename}: {str(e)}")

    
    combined_df = pd.concat(dfs, ignore_index=True)

    
    loaded_countries = combined_df['Country'].unique()
    expected_countries = ['Benin', 'Sierra Leone', 'Togo']
    if set(loaded_countries) != set(expected_countries):
        raise ValueError(
            f"Country mismatch. Loaded: {loaded_countries}, Expected: {expected_countries}"
        )

    return combined_df

def get_region_stats(df):
    """Calculate regional statistics for solar metrics
    
    Args:
        df: Combined dataframe from load_data()
        
    Returns:
        pd.DataFrame: Statistics by country sorted by GHI
    """
    if df.empty:
        return pd.DataFrame()
        
    stats = df.groupby(['Country']).agg({
        'GHI': ['mean', 'median', 'std'],
        'DNI': ['mean', 'median'],
        'DHI': ['mean', 'median']
    }).sort_values(('GHI', 'mean'), ascending=False)
    
    
    stats.columns = ['_'.join(col).strip() for col in stats.columns.values]
    return stats.reset_index()



if __name__ == "__main__":
    print("Testing data loading...")
    try:
        df = load_data()
        print("✅ Data loaded successfully!")
        print(f"Total records: {len(df)}")
        print(f"Countries found: {df['Country'].unique()}")
        print("\nRegional stats:")
        print(get_region_stats(df))
    except Exception as e:
        print(f"❌ Error: {str(e)}")