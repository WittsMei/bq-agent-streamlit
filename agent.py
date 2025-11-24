import vertexai
from vertexai.preview.generative_models import GenerativeModel
from config import PROJECT_ID, LOCATION, DATASETS
from tools import get_table_schema, execute_query, visualize_data

class BigQueryAgent:
    def __init__(self):
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        self.model = GenerativeModel("gemini-2.5-pro")
        self.context = self._build_dataset_context()

    def _build_dataset_context(self):
        context = "Available datasets:\n"
        for name, info in DATASETS.items():
            context += f"\n{name}:\n"
            context += f"  Table: `{PROJECT_ID}.{info['dataset_id']}.{info['table_id']}`\n"
            context += f"  Description: {info['description']}\n"
            context += f"  Schema:\n{get_table_schema(info['dataset_id'], info['table_id'])}\n"
        return context

    def process_request(self, user_question, enable_plot=True):
        """
        Main entry point for the ADK Web Interface.
        Returns a dictionary with 'answer', 'sql', and optional 'plot'.
        """
        # 1. Generate SQL
        sql_prompt = f"""
        You are an expert data analyst.
        {self.context}
        User Question: "{user_question}"
        Generate a valid BigQuery SQL query. Return ONLY the SQL query (no markdown, no backticks).
        """
        
        sql_response = self.model.generate_content(sql_prompt)
        sql_query = sql_response.text.strip().replace("```sql", "").replace("```", "").strip()

        # 2. Execute SQL
        try:
            df = execute_query(sql_query)
        except Exception as e:
            return {"answer": f"Error executing query: {e}", "sql": sql_query}

        # 3. Generate Answer
        answer_prompt = f"""
        User asked: "{user_question}"
        Data returned:
        {df.to_string()}
        Provide a concise, natural language answer with numbers and insights.
        """
        answer_res = self.model.generate_content(answer_prompt)
        
        # 4. Generate Plot (if applicable)
        fig = None
        if enable_plot:
        # Only run the visualization logic if the user wants it
            fig = visualize_data(df, user_question)

        return {
            "answer": answer_res.text.strip(),
            "sql": sql_query,
            "dataframe": df,
            "plot": fig 
        }

# Instantiate the agent to be imported by ADK
agent_instance = BigQueryAgent()