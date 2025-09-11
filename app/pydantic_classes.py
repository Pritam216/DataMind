from typing import TypedDict, List, Annotated, Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict
import pandas as pd
import os

DATA_DIR='data'
PLOT_DIR='plot'

data_path = 'diabetes.csv'

DATA_PATH=os.path.join(DATA_DIR, data_path)

class DataMindState(BaseModel):
    data_path: str
    data: Optional[pd.DataFrame] = None
    stat_data: Optional[str] = ""       
    graph_data: Optional[str] = ""      
    analysis_summary: Optional[str] = ""
    missing_data_result: Optional[str] = ""

    model_config = ConfigDict(arbitrary_types_allowed=True)

class MissingDataAnalysis(DataMindState):
    """In this class llm will decide if there is a huge missing data or not """
    missingdata : str = Field(description="If there is a huge missing data then return only yes otherwise return no")

