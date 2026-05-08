import pandas as pd
import os
 
DATA_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
LOCAL_PATH = "sample_data/yellow_tripdata_2023-01.parquet"
ZONE_LOOKUP_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"
 
def load_zone_lookup():
    print (pd.read_csv(ZONE_LOOKUP_URL).head(5))
    return pd.read_csv(ZONE_LOOKUP_URL)
 
def download_data():
    if not os.path.exists(LOCAL_PATH):
        print("Downloading dataset...")
        df = pd.read_parquet(DATA_URL)
        df.to_parquet(LOCAL_PATH)
        print("Saved locally!")
    else:
        print("Dataset already exists.")
 
def load_data():
    download_data()
 
    df = pd.read_parquet(LOCAL_PATH)
 
    # Reduce size
    df = df.sample(n=50000, random_state=42)
 
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["date"] = df["tpep_pickup_datetime"].dt.date
 
    zones = load_zone_lookup()
 
    df = df.merge(
        zones,
        left_on="PULocationID",
        right_on="LocationID",
        how="left"
    )
 
    return df

def compute_kpis(df):
    daily_trips = df.groupby("date").size()
 
    avg_fare = df["fare_amount"].mean()
 
    df["hour"] = df["tpep_pickup_datetime"].dt.hour
    trips_by_hour = df.groupby("hour").size()
 
    top_zones = df["Zone"].value_counts().head(5)
 
    return {
        "daily_trips": daily_trips,
        "avg_fare": avg_fare,
        "trips_by_hour": trips_by_hour,
        "top_zones": top_zones
    }

if __name__=="__main__":
    df=load_data()
    print(df.head())

    kpis = compute_kpis(df)