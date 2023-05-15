# -*- coding: utf-8 -*-
"""
Created on Mon May  8 18:45:10 2023

@author: LENOVO
"""

import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Dash(__name__)

# membuat fungsi untuk membuat WordCloud
def create_wordcloud(data):
    text = ' '.join(data)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(16, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

app.layout = html.Div([
        html.H1(children='Pilpres 2024', style={'textAlign':'center'}),
        html.Div(children='data diambil dari bulan Januari sampai bulan April tahun 2023 ', style={'textAlign':'center'}),
        html.Label('Pilih media sosial'),
        dcc.Dropdown(
            options=[
                {
                    "label": "facebook",
                    "value":"C:/Users/LENOVO/OneDrive/Documents/learn/Dash/survey_fb_pilpres.csv",
                },
                {
                    "label": "instagram",
                    "value":"C:/Users/LENOVO/OneDrive/Documents/learn/Dash/survey_ig_pilpres.csv",
                },
                {
                    "label": "twitter",
                    "value": "C:/Users/LENOVO/OneDrive/Documents/learn/Dash/survey_tw_pilpres.csv",
                },
            ],
            value="C:/Users/LENOVO/OneDrive/Documents/learn/Dash/survey_fb_pilpres.csv",
            id="data-select",
        ),
        html.Br(),
        html.Div([
            html.Img(id='wordcloud', width=800, height=400)
        ], style={'textAlign': 'center'}),
        html.Br(),
        dash_table.DataTable(
            id="my-table-promises",
            page_size=10,
            style_cell={
                'textAlign': 'left',
                'maxWidth': '200px',  # menetapkan lebar maksimum untuk sel
                'overflow': 'hidden',  # membatasi konten yang melebihi lebar maksimum
                'textOverflow': 'ellipsis',  # memotong konten yang melebihi lebar maksimum
            }
        ),
    ]
)

@app.callback(
    Output("wordcloud", "src"),
    Input("data-select", "value"),
)
def update_wordcloud(value):
    df = pd.read_csv(value)
    return create_wordcloud(df['body'].tolist())

@app.callback(
    Output("my-table-promises", "data"),
    Input("data-select", "value"),
)
def update_table(value):
    df = pd.read_csv(value)
    df = df.rename(columns={'href': 'url', 'body': 'description'})  # mengubah nama kolom
    return df.to_dict('records')

if __name__ == "__main__":
    app.run_server(debug=True)


