import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np

def create_time_series(data, title):
    """Create an interactive time series plot"""
    fig = go.Figure()

    for column in data.columns:
        fig.add_trace(go.Scatter(
            y=data[column],
            name=column,
            mode='lines',
            line=dict(width=1)
        ))

    fig.update_layout(
        title=title,
        template='simple_white',
        xaxis_title='Time Point',
        yaxis_title='Value',
        height=500,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    return fig

def create_distribution_plot(data, title):
    """Create distribution plots for each variable"""
    fig = go.Figure()

    for column in data.columns:
        fig.add_trace(go.Histogram(
            x=data[column],
            name=column,
            opacity=0.7,
            nbinsx=30
        ))

    fig.update_layout(
        title=title,
        template='simple_white',
        barmode='overlay',
        height=400,
        xaxis_title='Value',
        yaxis_title='Count'
    )
    return fig

def create_correlation_heatmap(corr_matrix):
    """Create a correlation heatmap"""
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
        text=np.round(corr_matrix, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        hoverongaps=False
    ))

    fig.update_layout(
        title='Correlation Heatmap',
        template='simple_white',
        height=400
    )
    return fig

def create_comparison_plot(data1, data2, label1, label2):
    """Create a box plot comparing two datasets"""
    fig = go.Figure()

    fig.add_trace(go.Box(
        y=data1,
        name=label1,
        boxpoints='outliers'
    ))

    fig.add_trace(go.Box(
        y=data2,
        name=label2,
        boxpoints='outliers'
    ))

    fig.update_layout(
        title=f'Comparison: {label1} vs {label2}',
        template='simple_white',
        height=400,
        yaxis_title='Value'
    )
    return fig