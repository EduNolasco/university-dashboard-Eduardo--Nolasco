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
dept_col = find_col(['department','dept','program','faculty'])
ret_col = find_col(['retention','retention_rate'])
sat_col = find_col(['satisfaction','satisfaction_score'])

st.title('University Student Analytics Dashboard')

st.sidebar.header('Filters')

# --- Si no hay columna de departamento, usa un valor genérico ---
if dept_col is None:
    df['Department'] = 'General'
    dept_col = 'Department'

years = ['All'] + sorted(df[year_col].dropna().unique().tolist()) if year_col else ['All']
depts = ['All'] + sorted(df[dept_col].dropna().unique().tolist())
terms = ['All'] + sorted(df[term_col].dropna().unique().tolist()) if term_col else ['All']

year_sel = st.sidebar.selectbox('Year', years)
dept_sel = st.sidebar.selectbox('Department', depts)
term_sel = st.sidebar.selectbox('Term', terms)

data = df.copy()
if year_col and year_sel != 'All':
    data = data[data[year_col]==year_sel]
if dept_sel != 'All':
    data = data[data[dept_col]==dept_sel]
if term_col and term_sel != 'All':
    data = data[data[term_col]==term_sel]

col1, col2, col3 = st.columns(3)
if ret_col and sat_col:
    col1.metric('Avg Retention', f"{data[ret_col].mean():.2f}")
    col2.metric('Avg Satisfaction', f"{data[sat_col].mean():.2f}")
else:
    col1.metric('Records', len(data))
col3.metric('Records', len(data))

st.subheader('Retention Rate Trends')
if ret_col and year_col:
    fig, ax = plt.subplots()
    sns.lineplot(data=df.groupby(year_col)[ret_col].mean().reset_index(), x=year_col, y=ret_col, marker='o', ax=ax)
    st.pyplot(fig)
else:
    st.info("Retention data not available.")

st.subheader('Satisfaction by Year')
if sat_col and year_col:
    fig2, ax2 = plt.subplots()
    sns.barplot(data=df.groupby(year_col)[sat_col].mean().reset_index(), x=year_col, y=sat_col, ax=ax2)
    st.pyplot(fig2)
else:
    st.info("Satisfaction data not available.")

st.subheader('Satisfaction: Spring vs Fall')
if sat_col and term_col:
    fig3, ax3 = plt.subplots()
    sns.boxplot(data=df, x=term_col, y=sat_col, ax=ax3)
    st.pyplot(fig3)
else:
    st.info("Term or satisfaction data not available.")
