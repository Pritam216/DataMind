from langchain_core.prompts import ChatPromptTemplate

supervisor_node = ChatPromptTemplate(
    messages=['In the given data, determine the percentage of missing values for each column. If any column has more than 20% missing values, respond with "yes". Otherwise, respond with "no".']
)

show_stat_node = ChatPromptTemplate(
    messages=["""
    You are a data analysis bot. Your only task is to generate a statistical summary of a DataFrame and a list of key plot types.
    
    Generate the output in the following format exactly:

    ---STATISTICAL_SUMMARY_START---
    {stats_markdown}
    ---STATISTICAL_SUMMARY_END---
    
    generate a summary on the statistics of the data {data} by analyzing it carefully.
    """]
)

plot_graph_node = ChatPromptTemplate(
    messages = ["""
    You are a data visualization assistant. Your task is to generate **atleast** 5 most important and useful graphs according to the given data and save the interactive Plotly diagram as a PNG file - 
                
    you need to consider all the rows of the data must from here {data} don't create data on your own
                
    you can plot these graphs eg. boxplot, scatterplot, violin plot, pie chart, histograms, 3Dplot, box plot etc. not all these but according to the data.

    Follow these steps precisely:
                1. analyze the data carefully {data}
                2. analyze the stistics research carefully {stat_data}
                3. now make a list of the plot names of **atleast 5 most important and useful graphs according to the given data**(for example box plot for COLUMN_NAME_1, scatterplot for COLUMN_NAME_2 and so on)
                4. Generate Python codes to create a Plotly graphs for the lists Store the figures in a variable named `fig`
                5. Save the figures as a PNG file. Use `fig.write_image()` for this purpose. The file should be named using the chosen column names(e.g., 'your_chosen_column.png'). Save it in the "graphs_figs" directory.
                6. Your final answer must be the exact string file path to the saved PNG file. Do not include any other text, explanation, or conversational phrases.
                7. summarize with some points.
    """
])

analysis_node_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert data analyst. Your job is to analyze the provided dataset statistics and a generated plot, then provide a comprehensive summary."),
    ("human", """
    Based on the following dataset statistics and a generated plot, provide a detailed analysis.

    **Dataset Statistics:**
    {stat_data}

    **Analysis of Plots:**
    A plot has been generated and saved at the following path: {graph_data}
    Please provide observations from the plot, such as the distribution, outliers, or any notable patterns.

    ---

    **Analysis Report:**
    Please provide a professional, in-depth summary of the data, including:
    1.  An overview of the dataset.
    2.  Key insights from the descriptive statistics (e.g., central tendencies, spread, outliers).
    3.  A dedicated section for **Observations from Plots**.

    ---

    **Suitable ML Algorithms:**
    Based on the analysis and the nature of the dataset, please suggest suitable machine learning algorithms.

    For example:
    -   **Classification:** K-Nearest Neighbors, Support Vector Machine, Logistic Regression
    -   **Regression:** Linear Regression, Decision Tree Regressor
    """)
])
