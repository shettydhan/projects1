"""
Data processing and cleaning service
"""
import pandas as pd
import logging
from pathlib import Path
from typing import Tuple, Dict
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Service for processing and cleaning data"""
    
    def __init__(self):
        self.df: pd.DataFrame = None
        self.stats: Dict = {}
    
    def load_file(self, file_path: str) -> pd.DataFrame:
        """Load Excel or CSV file"""
        try:
            file_path = Path(file_path)
            
            if file_path.suffix.lower() == '.csv':
                self.df = pd.read_csv(file_path)
                logger.info(f"Loaded CSV file: {file_path.name}")
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                self.df = pd.read_excel(file_path)
                logger.info(f"Loaded Excel file: {file_path.name}")
            else:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
            return self.df
        
        except Exception as e:
            logger.error(f"Error loading file: {str(e)}")
            raise
    
    def clean_data(self) -> pd.DataFrame:
        """Clean and standardize data"""
        try:
            if self.df is None:
                raise ValueError("No data loaded. Call load_file() first.")
            
            initial_rows = len(self.df)
            
            # 1. Remove completely empty rows
            self.df = self.df.dropna(how='all')
            
            # 2. Remove duplicate rows
            duplicates_count = self.df.duplicated().sum()
            self.df = self.df.drop_duplicates()
            
            # 3. Strip whitespace from string columns
            string_columns = self.df.select_dtypes(include=['object']).columns
            for col in string_columns:
                self.df[col] = self.df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
            
            # 4. Convert date columns (look for common date column names)
            date_columns = [col for col in self.df.columns if 'date' in col.lower()]
            for col in date_columns:
                try:
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                except Exception as e:
                    logger.warning(f"Could not convert {col} to datetime: {str(e)}")
            
            # 5. Standardize column names (remove extra spaces, lowercase)
            self.df.columns = [col.strip().replace('  ', ' ') for col in self.df.columns]
            
            # 6. Fill numeric NaN with 0 (optional - can be customized)
            numeric_columns = self.df.select_dtypes(include=['int64', 'float64']).columns
            for col in numeric_columns:
                self.df[col] = self.df[col].fillna(0)
            
            final_rows = len(self.df)
            
            # Store statistics
            self.stats = {
                'initial_rows': initial_rows,
                'final_rows': final_rows,
                'removed_rows': initial_rows - final_rows,
                'duplicates_removed': duplicates_count,
                'columns': len(self.df.columns),
                'column_names': list(self.df.columns)
            }
            
            logger.info(f"Data cleaned: {initial_rows} -> {final_rows} rows")
            return self.df
        
        except Exception as e:
            logger.error(f"Error cleaning data: {str(e)}")
            raise
    
    def generate_summary(self) -> pd.DataFrame:
        """Generate summary statistics"""
        try:
            if self.df is None:
                raise ValueError("No data loaded.")
            
            summary_data = {
                'Metric': [],
                'Value': []
            }
            
            # Basic stats
            summary_data['Metric'].append('Total Rows')
            summary_data['Value'].append(len(self.df))
            
            summary_data['Metric'].append('Total Columns')
            summary_data['Value'].append(len(self.df.columns))
            
            summary_data['Metric'].append('Missing Values')
            summary_data['Value'].append(self.df.isnull().sum().sum())
            
            # Numeric column statistics
            numeric_cols = self.df.select_dtypes(include=['int64', 'float64']).columns
            for col in numeric_cols:
                summary_data['Metric'].append(f'{col} - Mean')
                summary_data['Value'].append(round(self.df[col].mean(), 2))
                
                summary_data['Metric'].append(f'{col} - Sum')
                summary_data['Value'].append(round(self.df[col].sum(), 2))
            
            summary_df = pd.DataFrame(summary_data)
            return summary_df
        
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise
    
    def save_to_csv(self, output_path: str) -> str:
        """Save processed data to CSV"""
        try:
            if self.df is None:
                raise ValueError("No data to save.")
            
            self.df.to_csv(output_path, index=False)
            logger.info(f"Data saved to: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
            raise
    
    def get_stats(self) -> Dict:
        """Get processing statistics"""
        return self.stats
    
    def process_file(self, input_path: str, output_path: str) -> Tuple[str, Dict]:
        """
        Complete processing pipeline: load -> clean -> save
        Returns: (output_path, stats)
        """
        try:
            # Load file
            self.load_file(input_path)
            
            # Clean data
            self.clean_data()
            
            # Save to output
            self.save_to_csv(output_path)
            
            return output_path, self.get_stats()
        
        except Exception as e:
            logger.error(f"Error in processing pipeline: {str(e)}")
            raise


# Example usage
if __name__ == "__main__":
    processor = DataProcessor()
    
    # Test with sample data
    sample_data = {
        'Name': ['John Doe', 'Jane Smith', '  Bob  ', 'John Doe'],
        'Age': [30, 25, None, 30],
        'Email': ['john@test.com', 'jane@test.com', 'bob@test.com', 'john@test.com'],
        'Salary': [50000, 60000, 55000, 50000]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('test_input.csv', index=False)
    
    output_file, stats = processor.process_file('test_input.csv', 'test_output.csv')
    print(f"Processed file saved to: {output_file}")
    print(f"Stats: {stats}")
