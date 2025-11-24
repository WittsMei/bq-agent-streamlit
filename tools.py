from google.cloud import bigquery
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from config import PROJECT_ID, BQ_LOCATION

# Initialize Client
bq_client = bigquery.Client(project=PROJECT_ID, location=BQ_LOCATION)

def get_table_schema(dataset_id, table_id):
    """Retrieve schema information for a BigQuery table."""
    table_ref = f"{PROJECT_ID}.{dataset_id}.{table_id}"
    try:
        table = bq_client.get_table(table_ref)
        schema_info = [f"- {field.name} ({field.field_type})" for field in table.schema]
        return "\n".join(schema_info)
    except Exception as e:
        return f"Error retrieving schema: {e}"

def execute_query(sql_query):
    """Executes the SQL query and returns a DataFrame."""
    try:
        query_job = bq_client.query(sql_query)
        return query_job.result().to_dataframe()
    except Exception as e:
        raise Exception(f"SQL Execution Failed: {str(e)}")

def visualize_data(result_df, title_context=""):
    """Generates a Matplotlib Figure object for the web UI."""
    if result_df is None or result_df.empty:
        return None

    numeric_cols = result_df.select_dtypes(include="number").columns
    if len(numeric_cols) == 0:
        return None

    # Create a figure specifically to return it (don't use global plt instance if possible)
    fig = plt.figure(figsize=(8, 4)) 
    
    if len(result_df) <= 20:
        x_col = result_df.columns[0]
        y_col = numeric_cols[0]
        sns.barplot(data=result_df, x=x_col, y=y_col, hue=x_col, legend=False, palette="viridis")
        plt.xticks(rotation=45, ha='right')
    else:
        for col in numeric_cols[:3]:
            plt.plot(result_df.index, result_df[col], marker='o', label=col)
        plt.legend()

    plt.title(f"Visualization: {title_context}")
    plt.tight_layout()
    
    # Close plot to free memory, but return the figure object
    plt.close(fig) 
    return fig