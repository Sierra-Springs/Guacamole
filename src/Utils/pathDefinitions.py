from pathlib import Path
import os


projectPath = Path(os.path.dirname(__file__)).parent.parent

dataPath = projectPath / "Data"
edgesPath = dataPath / "edges.data"
nodesPath = dataPath / "nodes.data"

authPath = projectPath / "auth.json"

csvPath = dataPath / "SP12022topics.csv"
