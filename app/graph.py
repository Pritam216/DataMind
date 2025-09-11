from langgraph.graph import END, StateGraph

from app.nodes import load_data, missing_data, show_stat, plot_graphs, analysis_node, can_not_EDA, route_after_missing_data
from app.pydantic_classes import DataMindState

graph = StateGraph(DataMindState)

graph.add_node("load_data", load_data)
graph.add_node("missing_data", missing_data)
graph.add_node("show_stat", show_stat)
graph.add_node("plot_graphs", plot_graphs)
graph.add_node("analysis_node", analysis_node)
graph.add_node("can_not_EDA", can_not_EDA)

graph.set_entry_point("load_data")

graph.add_edge("load_data", "missing_data")
graph.add_conditional_edges(
    "missing_data",
    route_after_missing_data,
    {
        "show_stat": "show_stat",
        "can_not_EDA": "can_not_EDA"
    }
)

graph.add_edge("show_stat", "plot_graphs")
graph.add_edge("plot_graphs", "analysis_node")
graph.add_edge("analysis_node", END)
graph.add_edge("can_not_EDA", END)

app = graph.compile()

if __name__ == "__main__":
    result = app.invoke({"data_path": "data/whitewines.csv"})
    print("\n=== Final State ===")
    print(result)
