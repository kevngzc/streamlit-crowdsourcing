import pandas as pd
from pathlib import Path
from typing import Dict, Any

class DataManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_path = Path(config["DATA_PATH"])

    def create_sample_data(self) -> pd.DataFrame:
        df = pd.DataFrame({
            'country_name': ['Sample Country'],
            'name': ['Sample Location'],
            'heritage': [False],
            'description': ['Sample description'],
            'website': ['http://example.com'],
            'id': [1]
        })
        return df

    def load_data(self, create_if_missing: bool = False) -> pd.DataFrame:
        try:
            if not self.data_path.exists():
                if create_if_missing:
                    df = self.create_sample_data()
                    self.save_data(df)
                    return df
                return pd.DataFrame()

            df = pd.read_csv(self.data_path)
            if 'heritage' in df.columns:
                df['heritage'] = df['heritage'].map({'True': True, 'False': False, True: True, False: False})
            return df
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return pd.DataFrame()

    def save_data(self, df: pd.DataFrame) -> bool:
        try:
            self.data_path.parent.mkdir(parents=True, exist_ok=True)
            df_to_save = df.copy()
            if 'heritage' in df_to_save.columns:
                df_to_save['heritage'] = df_to_save['heritage'].astype(str)
            df_to_save.to_csv(self.data_path, index=False)
            return True
        except Exception as e:
            print(f"Error saving data: {str(e)}")
            return False

    def get_filtered_data(self, filter_col: str, filter_value: str) -> pd.DataFrame:
        df = self.load_data(create_if_missing=True)
        filtered = df[df[filter_col].str.lower() == filter_value.lower()].copy()
        return filtered

    def update_records(self, updated_df: pd.DataFrame, id_column: str = "id") -> bool:
        try:
            main_df = self.load_data(create_if_missing=True)
            
            if 'heritage' in updated_df.columns:
                updated_df['heritage'] = updated_df['heritage'].map({'True': True, 'False': False, True: True, False: False})
            
            for idx, row in updated_df.iterrows():
                mask = main_df[id_column] == row[id_column]
                if mask.any():
                    for col in updated_df.columns:
                        if col != id_column:
                            main_df.loc[mask, col] = row[col]
            
            return self.save_data(main_df)
        except Exception as e:
            print(f"Error updating records: {str(e)}")
            return False