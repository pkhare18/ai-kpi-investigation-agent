import pandas as pd
import sys,os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data_processor import load_data

if __name__=="__main__":
    df=load_data()
    OUT_FILE = "sample_data/last12m_taxi_data.csv"
    df.to_csv(OUT_FILE,index=False)
    print ("csv saved")
