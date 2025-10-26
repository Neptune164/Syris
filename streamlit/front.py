import streamlit as st
import requests
import pandas as pd
import pytz

st.set_page_config(page_title="Weather Forecast Viewer", page_icon="⛅", layout="centered")
st.title("⛅ Weather Forecast Viewer")

API_URL = "http://127.0.0.1:5050/predict"
method = "GET"

go = st.button("reflash")

def fetch_payload(url: str):
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def parse_to_df(payload: dict) -> pd.DataFrame:
    dt_map = payload.get("datetime", {})
    tp_map = payload.get("temperature", {})

    keys = sorted(dt_map.keys(), key=lambda k: int(k))

    df = pd.DataFrame({
        "datetime_ms": [dt_map[k] for k in keys],
        "temperature": [tp_map.get(k, None) for k in keys],
    })

    df["datetime"] = (
        pd.to_datetime(df["datetime_ms"], unit="ms", utc=True)
          .dt.tz_convert(pytz.timezone("America/New_York"))
    )

    return df[["datetime", "temperature"]]

chart_ph = st.empty()
table_ph = st.empty()
stats_ph = st.empty()
error_ph = st.empty()

if go:
    try:
        payload = fetch_payload(API_URL)
        df = parse_to_df(payload)

        if df.empty:
            st.warning("No data returned.")
        else:
            latest = df.iloc[-1]
            c1, c2, c3 = st.columns(3)
            c1.metric("Latest Temperature (°C)", f"{latest['temperature']:.2f}")
            c2.metric("Highest (°C)", f"{df['temperature'].max():.2f}")
            c3.metric("Lowest (°C)", f"{df['temperature'].min():.2f}")

            chart_ph.line_chart(df.set_index("datetime")[["temperature"]])

            table_ph.dataframe(df, use_container_width=True)

    except Exception as e:
        error_ph.error(f"Request or parsing failed: {e}")
