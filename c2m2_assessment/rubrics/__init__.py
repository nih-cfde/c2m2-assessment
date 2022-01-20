from pathlib import Path
rubrics = [f.stem for f in (Path(__file__).parent).glob('[!_]*.py')]