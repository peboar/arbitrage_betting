import pandas as pd
from pathlib import Path
sport = "football"


path = Path(__file__).parent / sport
webb = "bethard"
pd.set_option('display.max_columns', 5000)
pd.set_option('display.max_rows', 5000)
pd.set_option('expand_frame_repr', False)
filename = path / (webb + "_" + sport)
a=pd.read_pickle(filename, compression='infer', storage_options=None)
print(a)