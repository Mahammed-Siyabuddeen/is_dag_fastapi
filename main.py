from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dag import has_cycle
from typing import List, Dict
import logging
app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
origins=["http://localhost:3000"]
class DataModel(BaseModel):
     data:Dict[str, List[str]]
app.add_middleware(
    CORSMiddleware,
     allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

# @app.get('/pipelines/parse')
# def parse_pipeline(pipeline: str = Form(...)):
#     print("data in 1 function")
#     return {'status': 'parsed'}

@app.post('/pipelines/parse')
async def submit_data(response:DataModel):
    num_nodes=len(response.data)
    num_edges=sum(len(edges) for edges in response.data.values())
    
    response={
        "num_nodes":num_nodes,
        "num_edges":num_edges,
        "is_dag":has_cycle(response.data)
    }
    return response
