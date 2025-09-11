import os
import pandas as pd

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_core.output_parsers import JsonOutputParser
from langchain_tavily import TavilySearch

from langgraph.graph import END

from app.pydantic_classes import DataMindState
from app.prompts import supervisor_node, show_stat_node, plot_graph_node, analysis_node_prompt

from dotenv import load_dotenv
load_dotenv()

tavily_search = TavilySearch(k=3)   

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.5,
    api_key=os.getenv("GEMINI_API_KEY")
)

tools = [tavily_search]
llm_with_tools = llm.bind_tools(tools=tools)

output_parser = JsonOutputParser()

def load_data(state: DataMindState):
    file_path = state.data_path
    data = pd.read_csv(file_path)
    state.data = data
    print(f"Loaded data with shape {data.shape}")
    return {'data': data}


def missing_data(state: DataMindState):
    print("Entering missing_data ...")
    considerable_data = create_csv_agent(llm, state.data_path, verbose=True, allow_dangerous_code=True)
    result = considerable_data.invoke(supervisor_node)
    state.missing_data_result = result['output']
    return {"missing_data_result": result['output']}

def route_after_missing_data(state: DataMindState):
    """
    This function routes the graph based on the missing_data_result.
    It returns "show_stat" if there is no considerable missing data,
    otherwise it returns "can_not_EDA".
    """
    result = state.missing_data_result.lower().strip()
    if result == 'no':
        print("No considerable missing data. Proceeding to EDA...")
        return "show_stat"
    else: 
        print("Considerable missing data detected. Exiting EDA...")
        return "can_not_EDA"

def can_not_EDA(state: DataMindState):
    print("The data has no considerable amount of data to perform EDA.")
    print("Thanks for using our service.")
    return state

def show_stat(state: DataMindState):
    print("Entering show_stat ...")
    df = state.data
    stats_markdown = df.describe().to_markdown()
    final_prompt = show_stat_node.format(
        data = df,
        stats_markdown=stats_markdown
    )
    response = llm.invoke(final_prompt)
    state.stat_data = response.content
    
    print("\n=== Dataset Statistics from LLM ===")
    print(response.content)
    
    return {"stat_data": response.content}

def plot_graphs(state: DataMindState):
    print("Entering plot_graphs ...")
    df = state.data
    stat_data= state.stat_data
    agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True, handle_parsing_errors=True)
    final_prompt=plot_graph_node.format(
        data = df,
        stat_data = stat_data
    )
    response = agent.invoke({"input": final_prompt})
    state.graph_data = response["output"]

    print("\n=== Graph Summary from LLM ===")
    print(response["output"])

    output_dir = "graphs_figs"
    os.makedirs(output_dir, exist_ok=True)

    return {"graph_data": response['output']}


def analysis_node(state: DataMindState):
    print("Entering analysis_node ...")
    response = llm_with_tools.invoke(analysis_node_prompt.format(
        columns=list(state.data.columns),
        stat_data=state.stat_data,
        graph_data=state.graph_data
    ))
    
    state.analysis_summary = response.content
    print("\n=== Analysis Summary ===")
    print(state.analysis_summary)
    return {"analysis_summary": response.content}
