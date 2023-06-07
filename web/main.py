import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from pyFTS.partitioners import Grid
from pyFTS.models import chen
from pyFTS.benchmarks import Measures
from plotly.subplots import make_subplots

st.set_option('deprecation.showPyplotGlobalUse', False)

st.info("Created by: Muhammad Dzalhaqi (3321600023) - Applied Data Science (D4) PENS 2021")
st.title("Analisis Fuzzy Time Series Terhadap Ketersediaan Air Bersih dan Sanitasi di Seluruh Dunia")

# set browser tab title
st.markdown("## Dataset")

# Load data
df = pd.read_csv(
    'https://github.com/Dzalhaqi/pas-dm/blob/main/water-and-sanitation.csv?raw=true')
selected_data = df.copy()
selected_data = selected_data[[
    'Entity', 'Year',
    'Access to improved sanitation',
    'Access to basic sanitation services',
    'Access to limited sanitation services',
    'Access to unimproved sanitation facilities',
    'Open defecation (no sanitation facilities)',
    'Access to safely managed sanitation']].fillna(0)

entity_data = selected_data['Entity'].unique()
indicator_data = selected_data.columns[2:]
year_data = selected_data['Year'].unique()
indicator_data = np.append(indicator_data, 'All')

st.dataframe(selected_data)

with st.sidebar:
  st.markdown("### Configuration")
  entity = st.selectbox('Select Entity', entity_data, index=100)
  indicator = st.selectbox(
      'Select Indicator',
      indicator_data)


# Visualizations
st.markdown("## Visualisasi Data")
tab1, tab2 = st.tabs(["Line Chart of Spesific Entity Data",
                      "Column Chart of All Entity Data"])


with tab2:
  # show all entity based on selected indicator
  st.markdown("### Column Chart")

  title_column = ""

  # if indicator == 'All':
  #   year = st.selectbox('Select Year', year_data, index=0)

  #   num_indicators = len(indicator_data[:-1])
  #   num_cols = 1
  #   num_rows = (num_indicators + num_cols - 1) // num_cols

  #   # Filter data based on selected year
  #   filtered_data = selected_data[selected_data['Year'] == year]

  #   fig = make_subplots(rows=num_rows, cols=num_cols,
  #                       subplot_titles=indicator_data[:-1])

  #   for i, ind in enumerate(indicator_data[:-1]):
  #     fig.add_trace(go.Bar(
  #         x=filtered_data['Entity'],
  #         y=filtered_data[ind],
  #         name=ind,
  #         hovertemplate=
  #         '%{y:.2f}%',
  #     ), row=i + 1, col=1)

  #     fig.update_yaxes(title_text="Percentage",
  #                      tickformat=".2%", row=i + 1, col=1)
  #     fig.update_xaxes(title_text="Entity", row=i + 1, col=1)
  #     fig.update_layout(height=3000, margin=dict(t=100, b=100), row=i+1, col=1)

  #   fig.update_layout(
  #     title_text="Column Chart for All Indicators",
  #     # height=3000,
  #     barmode='stack',
  #     legend=dict(
  #       orientation="h",
  #       yanchor="bottom",
  #       y=-1.02,
  #       xanchor="right",
  #       x=0
  #     ),
  #     legend_title="Indicator"
  #   )

  #   title_column = f"Column Chart for All Indicators in {year}"

  if indicator == 'All':
    year = st.selectbox('Select Year', year_data, index=0)

    num_indicators = len(indicator_data[:-1])
    num_cols = 1
    # num_rows = (num_indicators + num_cols - 1) // num_cols
    num_rows = 6

    # Filter data based on selected year
    filtered_data = selected_data[selected_data['Year'] == year]

    # Adjust the height values as desired
    row_heights = [0.25] * num_indicators

    fig = make_subplots(rows=num_rows, cols=num_cols,
                        subplot_titles=indicator_data[:-1], row_heights=row_heights)

    for i, ind in enumerate(indicator_data[:-1]):
      fig.add_trace(go.Bar(
          x=filtered_data['Entity'],
          y=filtered_data[ind],
          name=ind,
          hovertemplate='<b>Percentage</b>: %{y:.2f}%<br>' +
          '<br><b>Entity</b>: %{x}<br>' +
          '<extra></extra>',
      ), row=i + 1, col=1)

      fig.update_yaxes(title_text="Percentage",
                       tickformat=".2%", row=i + 1, col=1)
      fig.update_xaxes(title_text="Entity", row=i + 1, col=1)

    fig.update_layout(
        title_text="Column Chart for All Indicators",
        height=5000,
        barmode='stack',
        # dont show legend
        showlegend=False
    )

    title_column = f"Column Chart for All Indicators in {year}"

  else:
    # Filter the data for the selected indicator
    filtered_data = selected_data[selected_data[indicator] != 0]

    # Create a bar chart for the selected indicator
    fig = px.bar(
        filtered_data,
        x='Entity',
        y=indicator,
        title=f"Column Chart for {indicator}",
        hover_data=['Entity', indicator],
        labels={'value': 'Percentage'}
    )

  fig.update_layout(
      xaxis=dict(
          tickangle=45,
          tickfont=dict(size=12),
          tickformat='%Y-%m-%d'
      ),
      yaxis=dict(
          title='Percentage',
          title_font=dict(size=12),
          tickfont=dict(size=12)
      ),
      title=f"{title_column}",
      xaxis_title="Entity",
      yaxis_title="Percentage",
      legend_title="Indicator",
      legend=dict(
          orientation="h",
          yanchor="bottom",
          y=-1.02,
          xanchor="right",
          x=1,
          font=dict(size=12)
      )
  )

  # Show the plot
  st.plotly_chart(fig)

with tab1:
  st.markdown("### Line Chart")

  title_line = ""

  fig = go.Figure()
  if indicator == 'All':
    for i in range(len(indicator_data) - 1):
      fig.add_trace(
          go.Scatter(
              showlegend=True,
              x=selected_data[selected_data['Entity'] == entity]['Year'],
              y=selected_data[selected_data['Entity']
                              == entity][indicator_data[i]],
              name=indicator_data[i],
              hovertemplate="Entity: " + entity + "<br>" +
              "Year: %{x}<br>" +
              "Indicator: " + indicator_data[i] + "<br>" +
              "Percentage: %{y}<br>" +
              "<extra></extra>"
          ),
      )

      title_line = f"Line Chart All Indicator of {entity}"

  else:
    fig.add_trace(
        go.Scatter(
            x=selected_data[selected_data['Entity'] == entity]['Year'],
            y=selected_data[selected_data['Entity'] == entity][indicator],
            mode='lines',
            name=indicator,
            hovertemplate="Entity: " + entity + "<br>" +
            "Year: %{x}<br>" +
            "Indicator: " + indicator + "<br>" +
            "Percentage: %{y}<br>" +
            "<extra></extra>"
        )
    )

    title_line = f"Line Chart {indicator.title()} of {entity}"

  fig.update_layout(
      xaxis=dict(
          tickangle=45,
          tickfont=dict(size=12),
          tickformat='%Y-%m-%d'
      ),
      yaxis=dict(
          title='Percentage',
          title_font=dict(size=12),
          tickfont=dict(size=12)
      ),
      title=f"{title_line}",
      xaxis_title="Year",
      yaxis_title="Percentage",
      legend_title="Indicator",
      legend=dict(
          orientation="h",
          yanchor="bottom",
          y=-1.02,
          xanchor="right",
          x=1,
          font=dict(size=12)
      )
  )

  # Show the plot
  st.plotly_chart(fig)

# Fuzzy Time Series

with st.sidebar:
  n_part = st.slider('Number of Partition', 1, 20, 10)

if indicator != 'All':

  st.markdown("## Hasil Pemodelan Fuzzy Time Series")
  fs = Grid.GridPartitioner(
      data=selected_data[selected_data['Entity'] == entity][indicator].values, npart=n_part)

  fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[25, 10])

  ax.set_ylim(-0.1, 0.1)
  ax.set_xlim(
      0, len(selected_data[selected_data['Entity'] == entity][indicator].values))
  ax.set_xlabel('Year', fontsize=20)
  ax.set_ylabel('Membership', fontsize=20)
  ax.tick_params(axis='x', labelsize=20)
  ax.tick_params(axis='y', labelsize=20)

  fs.plot(ax)
  ax.set_title(f"Membership of {indicator.title()} in {entity}", fontsize=30)
  st.pyplot(plt.show())

  data_model = selected_data[selected_data['Entity']
                             == entity][indicator].values
  model = chen.ConventionalFTS(partitioner=fs)
  model.fit(data_model)

  prediction = model.predict(data_model)
  actual = data_model
  fts_dates = selected_data[selected_data['Entity'] == entity]['Year'].values

  st.markdown("### FLR Model")
  st.code(model)

  st.markdown("### Prediction & Forecasting")

  tab1, tab2 = st.tabs(["Prediction", "Forecasting"])

  with tab1:
    # Plot between actual and preicted data using plotly
    st.markdown("#### Prediction")
    fig = go.Figure()

    # Add actual data
    fig.add_trace(go.Scatter(
        x=df['Year'], y=actual, mode='lines', name='Actual'))

    # Add forecast data
    fig.add_trace(go.Scatter(
        x=df['Year'], y=prediction, mode='lines', name='Prediction'))

    # Set layout
    fig.update_layout(
        title=f"Prediction {indicator.title()} of {entity}",
        xaxis_title="Year",
        yaxis_title="Percentage",
        legend_title="Indicator",
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=12),
            tickformat='%Y-%m-%d'
        ),
        yaxis=dict(
            title='Percentage',
            title_font=dict(size=12),
            tickfont=dict(size=12)
        ),
        legend=dict(
            x=1,
            y=0,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    )

    for i in range(len(fts_dates)):
      if i % 2 == 0:
        fig.add_shape(type='line', x0=fts_dates[i], y0=0, x1=fts_dates[i], y1=1, line=dict(
            color='black', width=1, dash='solid'))
      else:
        fig.add_shape(type='line', x0=fts_dates[i], y0=0, x1=fts_dates[i], y1=1, line=dict(
            color='black', width=1, dash='dash'))

    st.plotly_chart(fig)

  with tab2:
    st.markdown("#### Forecasting")

    # forecasting for 5 years
    forecasting = model.forecast(data_model, steps=5)
    start_year = int(df['Year'].iloc[-1]) + 1
    forecasting_dates = pd.date_range(
        start=f"{start_year}-01-01", periods=5, freq='Y').strftime("%Y").tolist()

    forecast_data = dict(zip(forecasting_dates, forecasting))

    # show the line chart with plotly
    fig = go.Figure()

    # forecast data
    fig.add_trace(go.Scatter(
        x=forecasting_dates, y=forecasting, mode='lines', name='Forecasting'))

    # set layout
    fig.update_layout(
        title=f"Forecasting {indicator.title()} of {entity}",
        xaxis_title="Year",
        yaxis_title="Percentage",
        legend_title="Indicator",
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=12),
            tickformat='%Y-%m-%d',
            dtick='Y1'
        ),
        yaxis=dict(
            title='Percentage',
            title_font=dict(size=12),
            tickfont=dict(size=12)
        ),
        legend=dict(
            x=1,
            y=0,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=12)
        )
    )

    # show hover template
    fig.update_traces(hovertemplate="Entity: " + entity + "<br>" +
                      "Year: %{x}<br>" +
                      "Percentage: %{y}<br>%" +
                      "<extra></extra>")

    st.plotly_chart(fig)

# Model performance

  st.markdown("### Model Performance")

  st.code(f" \
          RMSE: {Measures.rmse(actual, prediction)} \
          MAPE: {Measures.mape(actual, prediction)} \
          ")
