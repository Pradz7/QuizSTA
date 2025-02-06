import pandas as pd
import numpy as np
from scipy import stats

def load_data():
    """Load and preprocess the data"""
    try:
        df = pd.aread_csv('attached_assets/selamat.csv', header=None)
        # Process data: Each row represents a different variable
        # First 3 rows contain actual data, rest are empty or duplicates
        data = df.iloc[:3].T
        data.columns = ['Variable1', 'Variable2', 'Variable3']
        return data
    except Exception as e:
        raise Exception(f"Error loading data: {str(e)}")

def calculate_statistics(data):
    """Calculate descriptive statistics for the dataset"""
    stats_dict = {
        'Mean': data.mean(),
        'Median': data.median(),
        'Std Dev': data.std(),
        'Min': data.min(),
        'Max': data.max(),
        'Skewness': data.skew(),
        'Kurtosis': data.kurtosis()
    }
    return pd.DataFrame(stats_dict).round(4)

def calculate_correlations(data):
    """Calculate correlations between variables"""
    return data.corr()

def perform_statistical_test(data1, data2):
    """Perform statistical comparison between two datasets"""
    t_stat, p_value = stats.ttest_ind(data1, data2)
    effect_size = np.abs(data1.mean() - data2.mean()) / np.sqrt((data1.var() + data2.var()) / 2)
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'effect_size': effect_size
    }