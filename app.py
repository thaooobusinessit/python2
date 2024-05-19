import streamlit as st
import pandas as pd
from streamlit_space import space
import plotly.express as px
import numpy as np
import datetime

# Load the dataset into a pandas DataFrame
df = pd.read_csv("datasets\student-scores.csv")
# Define columns to be converted to "Yes" or "No"
boolean_columns = ['part_time_job']

# Function to map boolean values to "Yes" or "No"
def map_boolean_to_text(value):
    if value:
        return 'Yes'
    else:
        return 'No'

# Apply the function to boolean columns
for col in boolean_columns:
    df[col] = df[col].apply(map_boolean_to_text)
selected_columns = ['first_name', 'gender', 'absence_days', 'part_time_job', 'weekly_self_study_hours', 'math_score']
df_selected = df[selected_columns]

# Sidebar
with st.sidebar:
    st.markdown("Author: **Hoang Thanh Thao**") # Change name of author here
    st.write("Date: ", datetime.date.today())
    st.text("Description: This is an Interactive Web Application for \nanalyzing student math scores.")
    st.text("This application allows you to explore the performance of \nsenior students in mathematics based on various factors \nsuch as gender, part-time job engagement, absence days, \nand weekly self-study hours.")
    #Modify description
# Main content
st.title("Student Performance Analysis")
st.markdown("We analyze the **Student Scores** dataset to understand the performance of senior students in mathematics.")
st.divider()

# Display dataset information
st.header("Dataset Information")
st.markdown(
"""
- **Description**: Dataset that stores information about the performance of senior students of a (very large) fictional high school at the end of their final semester.
- **Variables**:
    1. **first_name**: The first name of a student.
    2. **math_score**: The score obtained by a student in the subject of mathematics (0 - 100).
    3. **gender**: The gender of a student.
    4. **absence_days**: The total count of days the student was not present in class due to various reasons.
    5. **part_time_job**: This indicates whether a student is engaged in a part-time job. Taking a part-time job can have an effect on grades.
    6. **weekly_self_study_hours**: This represents the number of hours a student spends on self-study each week. It indicates the amount of time the student dedicates to independent learning and studying outside of class.
"""
)

st.dataframe(df_selected, width = 700)


# Subject-wise Scores
st.header("Scores Analysis by Selected Category")
st.text("We explore the scores of students based on a selected category.")

tab1, tab2 = st.tabs(["General relation", "Counts"])

with tab1:
    col1, col2 = st.columns([1,3])

    with col1:
        space(lines=10)
        category_mapping = {
            'gender': 'Gender',
            'part_time_job' : 'Part-time Job',
            'absence_days': 'Absence Days',
        }
        by_what = st.radio(
            "Choose a category:",
            ['gender', 'part_time_job', 'absence_days'],
            format_func=lambda x: category_mapping[x],
            key="r1"
        )
    with col2:
        fig1 = px.bar(df, x = by_what, y = "math_score", color = by_what,
                    labels={by_what: category_mapping[by_what], "math_score": "Math Score"},
                    title = f"Average Math Score by {category_mapping[by_what]}")
        st.plotly_chart(fig1, theme = "streamlit", use_container_width=True)
        
    fig1a = px.scatter(df, x = "weekly_self_study_hours", y = "math_score", color = by_what,
                    labels={"weekly_self_study_hours": "Weekly Self-study Hours", "math_score": "Math Score"},
                    # size = "math_score", 
                    marginal_x="histogram", marginal_y="histogram",
                    title = "Math Scores vs Self-study Hours")
    st.plotly_chart(fig1a, theme = "streamlit", use_container_width=True)
        
    fig1b = px.line(df, x="weekly_self_study_hours", y="math_score", 
                labels={"weekly_self_study_hours": "Weekly Self-study Hours", "math_score": "Math Score"},
                color=by_what, facet_col=by_what, facet_col_wrap=3)
    st.plotly_chart(fig1b, theme="streamlit", use_container_width=False, height=800)
with tab2:
    category_mapping = {
    'gender': 'Gender',
    'part_time_job' : 'Part-time Job',
    'absence_days': 'Absence Days',
    }
    # Display the values in the select box
    options = list(category_mapping.values())
    selected_option = st.selectbox("Choose a category:", options)

    # Get the corresponding key for the selected option
    by_what_2 = [key for key, value in category_mapping.items() if value == selected_option][0]

    tbr = st.slider("Choose a range for Math Score:", 
                    df['math_score'].min(), df['math_score'].max(), (0, 100)
                    )
    st.write("Math Score Range:", tbr)

    dff = df[(df['math_score'] >= tbr[0]) & (df['math_score'] <= tbr[1])]
    df2 = pd.crosstab(index=dff[by_what_2], columns="count")

    col1, col2 = st.columns(2)
    with col1:
        if not df2.empty:
            fig2 = px.bar(df2, x=df2.index, y="count", text_auto=True, title="In frequency")
            st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
        else:
            st.write("No data available for the selected range.")
    with col2:
        if not df2.empty:
            fig3 = px.pie(df2, values = "count", names = df2.index, hole = 0.4, title = "In percentage")
            st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
        else:
            st.write("No data available for the selected range.")
    