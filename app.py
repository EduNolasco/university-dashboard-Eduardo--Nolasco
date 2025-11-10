import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title='University Dashboard', layout='wide')

df = pd.read_csv('university_student_data.csv')

def find_col(possible):
    for p in possible:
        for c in df.columns:
            if p.lower() == c.lower() or p.lower() in c.lower():
                return c
    return None

year_col = find_col(['year','academic_year'])
term_col = find_col(['term','semester'])
dept_col = find_col(['department','dept'])
ret_col = find_col(['retention','retention_rate'])
sat_col = find_col(['satisfaction','satisfaction_score'])

st.title('University Student Analytics Dashboard')

st.sidebar.header('Filters')
years = ['All'] + sorted(df[year_col].unique().tolist())
year_sel = st.sidebar.selectbox('Year', years)
depts = ['All'] + sorted(df[dept_col].unique().tolist())
dept_sel = st.sidebar.selectbox('Department', depts)
terms = ['All'] + sorted(df[term_col].unique().tolist())
term_sel = st.sidebar.selectbox('Term', terms)

data = df.copy()
if year_sel != 'All':
    data = data[data[year_col]==year_sel]
if dept_sel != 'All':
    data = data[data[dept_col]==dept_sel]
if term_sel != 'All':
    data = data[data[term_col]==term_sel]

col1, col2, col3 = st.columns(3)
col1.metric('Avg Retention', f"{data[ret_col].mean():.2f}")
col2.metric('Avg Satisfaction', f"{data[sat_col].mean():.2f}")
col3.metric('Records', len(data))

st.subheader('Retention Rate Trends')
fig, ax = plt.subplots()
sns.lineplot(data=df.groupby(year_col)[ret_col].mean().reset_index(), x=year_col, y=ret_col, marker='o', ax=ax)
st.pyplot(fig)

st.subheader('Satisfaction by Year')
fig2, ax2 = plt.subplots()
sns.barplot(data=df.groupby(year_col)[sat_col].mean().reset_index(), x=year_col, y=sat_col, ax=ax2)
st.pyplot(fig2)

st.subheader('Satisfaction: Spring vs Fall')
fig3, ax3 = plt.subplots()
sns.boxplot(data=df, x=term_col, y=sat_col, ax=ax3)
st.pyplot(fig3)
