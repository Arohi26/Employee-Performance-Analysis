#liberaries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import seaborn as sns
import matplotlib.pyplot as plt

# to load employee data
df = pd.read_excel('employee_data.xlsx')

#  missing values
df.fillna({'Attendance': df['Attendance'].mean(),
           'Project_Completion': df['Project_Completion'].mean(),
           'Appraisal_Score': df['Appraisal_Score'].mean()}, inplace=True)

# Identify high and low performers
high_performers = df[df['Appraisal_Score'] >= df['Appraisal_Score'].quantile(0.75)]
low_performers = df[df['Appraisal_Score'] <= df['Appraisal_Score'].quantile(0.25)]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Distribution of Appraisal Scores
fig_appraisal = px.histogram(df, x='Appraisal_Score', nbins=10, title='Appraisal Score Distribution', color_discrete_sequence=['skyblue'])
fig_appraisal.update_layout(xaxis_title='Appraisal Score', yaxis_title='Count')

# Correlation 
corr = df[['Attendance','Project_Completion','Appraisal_Score']].corr()
fig_corr = go.Figure(data=go.Heatmap(
    z=corr.values,
    x=corr.columns,
    y=corr.columns,
    colorscale='Viridis',
    zmin=-1, zmax=1
))
fig_corr.update_layout(title='Correlation Heatmap')

# Attendance vs Appraisal Score 
fig_scatter = px.scatter(df, x='Attendance', y='Appraisal_Score', color='Department', size='Project_Completion',
                         title='Attendance vs Appraisal Score by Department')
 

fig_box = px.box(df, x='Department', y='Project_Completion', color='Department', title='Project Completion by Department')

# --- Seaborn/Matplotlib Visualization ---
plt.figure(figsize=(8,6))
sns.boxplot(data=df, x='Department', y='Appraisal_Score', palette='Set2')
plt.title("Appraisal Score Distribution by Department")
plt.tight_layout()
plt.savefig("seaborn_boxplot.png")   # save the plot as an image
plt.close()

# --- Dash Layout ---
app.layout = dbc.Container([
    html.H1("Employee Performance Dashboard", style={'textAlign':'center'}),
    dcc.Graph(figure=fig_appraisal),
    dcc.Graph(figure=fig_corr),
    dcc.Graph(figure=fig_scatter),
    dcc.Graph(figure=fig_box),

    html.H3("High Performers"),
    dbc.Table.from_dataframe(high_performers[['Employee_Name','Appraisal_Score']], striped=True, bordered=True, hover=True),

    html.H3("Low Performers"),
    dbc.Table.from_dataframe(low_performers[['Employee_Name','Appraisal_Score']], striped=True, bordered=True, hover=True),

    #  Add Seaborn plot here
    html.H3("Seaborn Visualization"),
    html.Img(src="seaborn_boxplot.png", style={'width': '70%', 'display': 'block', 'margin': 'auto'})
], fluid=True)


if __name__ == '__main__':
    app.run(debug=True)
