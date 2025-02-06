import streamlit as st
import pandas as pd
import numpy as np

from style import apply_style, COLORS
from utils import load_data, calculate_statistics, calculate_correlations, perform_statistical_test
from visualization import (create_time_series, create_distribution_plot,
                         create_correlation_heatmap, create_comparison_plot)
from analysis import analyze_time_series, calculate_summary_metrics

# Page configuration
st.set_page_config(
    page_title="Data Analysis Tool",
    page_icon="📊",
    layout="wide"
)

# Apply custom styling
apply_style()

# Main title
st.title("📊 Academic Data Analysis Tool")
st.markdown("---")

# Load data
try:
    data = load_data()
    st.success("Data loaded successfully!")
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Sidebar
st.sidebar.header("Analysis Options")
analysis_type = st.sidebar.selectbox(
    "Select Analysis Type",
    ["Overview", "Time Series Analysis", "Statistical Analysis", "Comparative Analysis"]
)

# Main content
if analysis_type == "Overview":
    st.header("Dataset Overview")

    # Data description
    st.markdown("""
    ### About the Dataset
    This dataset contains three time series variables:
    - **Variable1**: First measurement series
    - **Variable2**: Second measurement series
    - **Variable3**: Third measurement series

    Each variable contains numerical measurements in scientific notation format.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Data Preview")
        st.dataframe(data)

    with col2:
        st.subheader("Descriptive Statistics")
        st.dataframe(calculate_statistics(data))

    st.subheader("Time Series Visualization")
    st.plotly_chart(create_time_series(data, "Time Series Plot"), use_container_width=True)

elif analysis_type == "Time Series Analysis":
    st.header("Time Series Analysis")

    # Time series visualization
    st.plotly_chart(create_time_series(data, "Detailed Time Series Analysis"), use_container_width=True)

    # Distribution analysis
    st.subheader("Distribution Analysis")
    st.plotly_chart(create_distribution_plot(data, "Variable Distributions"), use_container_width=True)

    # Time series metrics
    st.subheader("Time Series Metrics")
    analysis_results = analyze_time_series(data)

    for var, results in analysis_results.items():
        st.markdown(f"**{var}**")
        cols = st.columns(3)
        cols[0].metric("Trend Slope", f"{results['trend']['slope']:.4f}")
        cols[1].metric("Seasonality", f"{results['seasonality']['autocorrelation']:.4f}")
        cols[2].metric("Mean Variation", f"{results['stationarity']['mean_variation']:.4f}")

        # Display stationarity status
        st.markdown(f"**Stationarity Status:** {'Stationary' if results['stationarity']['is_stationary'] else 'Non-stationary'}")

elif analysis_type == "Statistical Analysis":
    st.header("Statistical Analysis")

    # Correlation analysis
    st.subheader("Correlation Analysis")
    corr_matrix = calculate_correlations(data)
    st.plotly_chart(create_correlation_heatmap(corr_matrix), use_container_width=True)

    # Summary metrics
    st.subheader("Summary Metrics")
    metrics = calculate_summary_metrics(data)

    for var, metric in metrics.items():
        st.markdown(f"**{var}**")
        cols = st.columns(4)
        cols[0].metric("Mean", f"{metric['mean']:.4f}")
        cols[1].metric("Std Dev", f"{metric['std']:.4f}")
        cols[2].metric("Range", f"{metric['range']:.4f}")
        cols[3].metric("IQR", f"{metric['iqr']:.4f}")

elif analysis_type == "Comparative Analysis":
    st.header("Comparative Analysis")

    # Analysis type selection
    compare_type = st.radio(
        "Select comparison type:",
        ["Variable Comparison", "Sample Analysis"],
        horizontal=True
    )

    if compare_type == "Variable Comparison":
        # Variable selection
        var1 = st.selectbox("Select First Variable", data.columns)
        var2 = st.selectbox("Select Second Variable", data.columns)

        if var1 != var2:
            # Comparison visualization
            st.plotly_chart(create_comparison_plot(
                data[var1], data[var2], var1, var2
            ), use_container_width=True)

            # Statistical comparison
            st.subheader("Statistical Comparison")
            stats_results = perform_statistical_test(data[var1], data[var2])

            cols = st.columns(3)
            cols[0].metric("t-statistic", f"{stats_results['t_statistic']:.4f}")
            cols[1].metric("p-value", f"{stats_results['p_value']:.4f}")
            cols[2].metric("Effect Size", f"{stats_results['effect_size']:.4f}")

            # Interpretation
            st.markdown("### Interpretation")
            if stats_results['p_value'] < 0.05:
                st.markdown("🔍 There is a statistically significant difference between the variables")
            else:
                st.markdown("🔍 No statistically significant difference detected")
        else:
            st.warning("Please select different variables for comparison")
    else:
        # Sample Analysis
        st.subheader("Sample vs Full Data Analysis")

        # Sample size selection
        sample_size = st.slider("Select sample size (% of data)", 10, 90, 30)
        selected_var = st.selectbox("Select Variable for Sampling", data.columns)

        # Generate sample
        sample_indices = np.random.choice(len(data), size=int(len(data) * sample_size/100), replace=False)
        sample_data = data.iloc[sample_indices][selected_var]
        full_data = data[selected_var]

        # Display comparison
        st.plotly_chart(create_comparison_plot(
            sample_data, full_data, f"Sample ({sample_size}%)", "Full Dataset"
        ), use_container_width=True)

        # Statistical comparison
        st.subheader("Sample vs Population Statistics")
        cols = st.columns(2)

        sample_stats = {
            "Mean": np.mean(sample_data),
            "Std Dev": np.std(sample_data),
            "Median": np.median(sample_data)
        }

        full_stats = {
            "Mean": np.mean(full_data),
            "Std Dev": np.std(full_data),
            "Median": np.median(full_data)
        }

        cols[0].markdown("#### Sample Statistics")
        for stat, value in sample_stats.items():
            cols[0].metric(stat, f"{value:.4f}")

        cols[1].markdown("#### Full Dataset Statistics")
        for stat, value in full_stats.items():
            cols[1].metric(stat, f"{value:.4f}")