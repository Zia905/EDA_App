import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
from pandas_profiling import ProfileReport
import streamlit as st
from streamlit_pandas_profiling import st_profile_report

# Function to load data based on file format
def load_data(uploaded_file):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        else:
            raise ValueError("Unsupported file format. Please upload CSV or XLSX files.")
        return df

# Set up the web app's header and background color
st.markdown(
    """
    <style>
    .main {
        background-color: #0a192f;
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
    }
    .header {
        background-color: #4a86e8;
        color: #ffffff;
        padding: 20px;
        font-size: 30px;
        text-align: center;
        border-radius: 10px;
    }
    .subheader {
        background-color: #007bff;
        color: #ffffff;
        padding: 10px;
        font-size: 24px;
        text-align: center;
        border-radius: 5px;
    }
    .warning {
        background-color: #ffcc00;
        color: #333333;
        padding: 10px;
        font-size: 18px;
        text-align: center;
        border-radius: 5px;
    }
    .info {
        background-color: #33cc33;
        color: #ffffff;
        padding: 10px;
        font-size: 18px;
        text-align: center;
        border-radius: 5px;
    }
    @keyframes move {
        0% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-5px);
        }
        100% {
            transform: translateY(0);
        }
    }
    .moving-text {
        animation: move 2s infinite;
    }
    .example-btn {
        margin-top: 20px;
        margin-bottom: 20px;
        color: #ffffff;
        background-color: #ff6600; /* Bright orange color for button */
        border-radius: 5px;
    }
    .example-btn:hover {
        background-color: #ff8800; /* Slightly darker shade on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set up the web app's header and example data button
st.markdown(
    """<div class="main">
    <div class="header">
    <p><b><span style="font-size: 48px;">DataWonderscape</span></b></p>
    <p><b>Exploratory Data Analysis Web Application</b></p>
    <p>This App is primarily designed for Desktop Site </p>
    </div>
    <p class="moving-text" style="text-align: center; font-size: 24px;">Data need a story to tell a story</p>
    </div>""",
    unsafe_allow_html=True,
)


# Sidebar: Upload data
with st.sidebar.header("Upload your dataset"):
    uploaded_file = st.sidebar.file_uploader("Click here to upload your file (CSV or XLSX)", type=(['csv', 'xlsx']))

# "Use Example Data" button on the main page

if st.button("Try Example Data", key="example_data"):
    # Generate example data
    age = np.random.randint(low=18, high=65, size=100)
    gender = np.random.choice(['Male', 'Female'], size=100)
    income = np.random.randint(low=20000, high=100000, size=100)
    education = np.random.choice(['High school', 'Bachelor\'s', 'Master\'s', 'Doctoral'], size=100)
    occupation = np.random.choice(['Engineer', 'Salesperson', 'Manager', 'Teacher'], size=100)

    # Combine the data arrays into a pandas DataFrame
    df = pd.DataFrame({
        'age': age,
        'gender': gender,
        'income': income,
        'education': education,
        'occupation': occupation
    })

    # Display the example data DataFrame
    st.subheader("Example Data")
    st.write(df)
    st.write("---")

    # Generate a profiling report using pandas_profiling
    pr = ProfileReport(df, explorative=True)

    # Display the pandas_profiling report for example data
    st.subheader("Profiling Report for Example Data")
    st_profile_report(pr)

    # Continue with the same EDA analysis as above (Correlation Heatmap, Histogram, Count Plot, etc.)
    # Add additional EDA operations for the
    # Continue with the same EDA analysis as above (Correlation Heatmap, Histogram, Count Plot, etc.)
    # Add additional EDA operations for the example data
    # ...

    # Finally, you can add some insights or conclusions about the example data.
    # ...

    # Add a link to go back to the main page
    st.write("---")
    st.markdown(
        """<div style="text-align: center;">
        <a href="/"><button class="example-btn" style="color: #000000;">Back to Main Page</button></a>
        </div>""",
        unsafe_allow_html=True,
    )

# Profiling report and EDA analysis
if uploaded_file is not None:
    # Load the uploaded data
    df = load_data(uploaded_file)

    # Generate a profiling report using pandas_profiling
    pr = ProfileReport(df, explorative=True)

    # Display the input DataFrame
    st.header("**Input DataFrame**")
    st.write(df)
    st.write("---")

    # Display the total number of samples in the data
    num_samples = len(df)
    st.write(f"Total number of samples: {num_samples}")
    st.write("---")

    # Display the pandas_profiling report
    st.header("**Profiling Report**")
    st_profile_report(pr)

    # EDA Analysis
    st.header("**Exploratory Data Analysis**")

    # Summary Statistics
    st.subheader("Summary Statistics")
    st.write(df.describe())

    # Correlation Heatmap using Plotly
    st.subheader("Correlation Heatmap")
    fig_corr = px.imshow(df.corr(), color_continuous_scale='Viridis', title="Correlation Heatmap")
    st.plotly_chart(fig_corr)

    # Histogram using Plotly
    st.subheader("Histogram")
    selected_column = st.selectbox("Select a column for the histogram", df.select_dtypes(include=np.number).columns)
    fig_hist = px.histogram(df, x=selected_column, nbins=20, title=f"Histogram of {selected_column}")
    st.plotly_chart(fig_hist)

    # Count plot for categorical data using Plotly
    st.subheader("Count Plot (Categorical)")
    selected_column = st.selectbox("Select a categorical column for the count plot", df.select_dtypes(include='object').columns)
    fig_count_plot = px.histogram(df, x=selected_column, color_discrete_sequence=px.colors.qualitative.Set2, title=f"Count Plot of {selected_column}")
    st.plotly_chart(fig_count_plot)

    # Box plot for numerical columns using Plotly
    st.subheader("Box Plot")
    selected_column = st.selectbox("Select a column for the box plot", df.select_dtypes(include=np.number).columns)
    fig_boxplot = px.box(df, y=selected_column, title=f"Box Plot of {selected_column}")
    st.plotly_chart(fig_boxplot)


# Add a placeholder for empty space to push the footer to the bottom
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

# Center the footer sentence
st.markdown('<div class="center-content">', unsafe_allow_html=True)


# Close the centering div
st.markdown('</div>', unsafe_allow_html=True)


# Unveil the Hidden Insights - Explore Your Data with EDA Delight!
st.markdown('<p align="center" class="footer-text" style="font-style: italic; font-family: cursive; font-size: 18px;">Unveil the Hidden Insights - Explore Your Data with EDA Delight!</p>', unsafe_allow_html=True)



