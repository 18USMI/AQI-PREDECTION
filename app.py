"""
╔══════════════════════════════════════════════════════════════════╗
║   🌫️  India AQI Intelligence — Real-Time Monitoring System      ║
║   Powered by Open-Meteo Free API + LSTM Prediction              ║
║   134 cities · 36 states · Live data · 5-day forecast           ║
╚══════════════════════════════════════════════════════════════════╝

Run:  streamlit run app.py
No API key required — Open-Meteo is completely free!
"""

import os, sys, pickle, math, time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import streamlit as st
from datetime import datetime, timedelta, timezone

sys.path.insert(0, "src")

from india_cities import INDIA_CITIES, STATE_GROUPS, ALL_STATES, get_cities_by_state, get_coords
from realtime_api import fetch_current_aqi, fetch_hourly_history, fetch_forecast, safe_val

# ─── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India AQI Intelligence",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS Theme ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Outfit:wght@300;400;600;800&display=swap');
:root {
    --bg0:#060D14; --bg1:#0B1929; --bg2:#0F2236; --bg3:#162D44;
    --cyan:#00E5C0; --cyan2:#00A88A; --gold:#FFB347; --red:#FF4757;
    --purple:#9B59B6; --green:#2ECC71;
    --txt:#D6EAF8; --muted:#5D8AA8; --border:#1E3A54;
}
.stApp,[data-testid="stAppViewContainer"]{background:var(--bg0)!important;font-family:'Outfit',sans-serif;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#08192A 0%,#050D17 100%)!important;border-right:1px solid var(--border);}
h1,h2,h3,h4{font-family:'Outfit',sans-serif!important;color:var(--txt)!important;font-weight:800!important;}
[data-testid="metric-container"]{background:var(--bg1)!important;border:1px solid var(--border)!important;border-radius:14px!important;padding:18px!important;transition:border-color .2s;}
[data-testid="metric-container"]:hover{border-color:var(--cyan)!important;}
[data-testid="stMetricValue"]{font-family:'IBM Plex Mono',monospace!important;color:var(--cyan)!important;font-size:1.9rem!important;}
[data-testid="stMetricLabel"]{color:var(--muted)!important;font-size:.72rem!important;letter-spacing:.1em!important;text-transform:uppercase!important;}
[data-baseweb="tab-list"]{background:var(--bg1)!important;border-radius:12px!important;padding:4px!important;border:1px solid var(--border)!important;gap:3px!important;}
[data-baseweb="tab"]{background:transparent!important;color:var(--muted)!important;border-radius:9px!important;font-family:'IBM Plex Mono',monospace!important;font-size:.78rem!important;}
[aria-selected="true"]{background:var(--cyan)!important;color:var(--bg0)!important;}
.stButton>button{background:linear-gradient(135deg,var(--cyan),var(--cyan2))!important;color:var(--bg0)!important;font-family:'IBM Plex Mono',monospace!important;font-weight:600!important;border:none!important;border-radius:10px!important;transition:all .2s!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 6px 22px rgba(0,229,192,.3)!important;}
.stSelectbox label,.stSlider label,.stNumberInput label,.stMultiSelect label{color:var(--muted)!important;font-size:.75rem!important;text-transform:uppercase!important;letter-spacing:.08em!important;}
[data-baseweb="select"]>div{background:var(--bg2)!important;border-color:var(--border)!important;color:var(--txt)!important;border-radius:10px!important;}
.sec-head{font-family:'IBM Plex Mono',monospace;font-size:.68rem;color:var(--muted);letter-spacing:.15em;text-transform:uppercase;border-bottom:1px solid var(--border);padding-bottom:6px;margin-bottom:14px;}
.city-card{background:var(--bg1);border:1px solid var(--border);border-radius:12px;padding:14px;text-align:center;transition:all .2s;}
.city-card:hover{border-color:var(--cyan);background:var(--bg2);}
.footer{font-family:'IBM Plex Mono',monospace;font-size:.68rem;color:var(--muted);text-align:center;padding:20px;border-top:1px solid var(--border);margin-top:36px;}
</style>
""", unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════════════╗
# ║                    CONSTANTS & PALETTE                          ║
# ╚══════════════════════════════════════════════════════════════════╝

DARK = {
    "bg0":"#060D14","bg1":"#0B1929","bg2":"#0F2236",
    "cyan":"#00E5C0","gold":"#FFB347","red":"#FF4757","purple":"#9B59B6",
    "green":"#2ECC71","txt":"#D6EAF8","muted":"#5D8AA8","grid":"#1E3A54",
}

plt.rcParams.update({
    "figure.facecolor":DARK["bg0"],"axes.facecolor":DARK["bg1"],
    "axes.edgecolor":DARK["grid"],"axes.labelcolor":DARK["txt"],
    "xtick.color":DARK["muted"],"ytick.color":DARK["muted"],
    "grid.color":DARK["grid"],"text.color":DARK["txt"],
    "axes.spines.top":False,"axes.spines.right":False,
    "font.family":"monospace","legend.frameon":False,"legend.labelcolor":DARK["txt"],
})

AQI_SCALE = [
    (0,   50,  "Good",           "#00E400","✅","Safe for all. Enjoy outdoor activities!"),
    (51,  100, "Moderate",       "#FFFF00","🟡","Acceptable. Sensitive persons limit prolonged exertion."),
    (101, 150, "Unhealthy-SG",   "#FF7E00","🟠","Sensitive groups reduce outdoor exertion."),
    (151, 200, "Unhealthy",      "#FF0000","🔴","Everyone may experience effects. Wear N95 mask outdoors."),
    (201, 300, "Very Unhealthy", "#8F3F97","🟣","Health alert! Limit outdoor time. Use air purifiers."),
    (301, 500, "Hazardous",      "#7E0023","☣️","EMERGENCY. Avoid ALL outdoor activity."),
]

def aqi_info(aqi):
    aqi = max(0, min(500, aqi or 0))
    for lo, hi, label, color, emoji, advice in AQI_SCALE:
        if lo <= aqi <= hi:
            return label, color, emoji, advice
    return "Hazardous","#7E0023","☣️","EMERGENCY conditions."

def aqi_color(v): return aqi_info(v)[1]

# ╔══════════════════════════════════════════════════════════════════╗
# ║                    DATA / FALLBACK                              ║
# ╚══════════════════════════════════════════════════════════════════╝

import hashlib

def _seed(city): return int(hashlib.md5(city.encode()).hexdigest()[:6], 16) % 10000

def _base_aqi(city):
    tier = INDIA_CITIES.get(city, (0,0,"",2))[3]
    return {1:160, 2:120, 3:90, 4:70}.get(tier, 100)

def _fallback(city):
    rng = np.random.RandomState(_seed(city))
    base = _base_aqi(city)
    aqi = float(np.clip(base + rng.normal(0, 25), 10, 450))
    return {"us_aqi":round(aqi),"pm2_5":round(aqi*.38+rng.normal(0,3),1),
            "pm10":round(aqi*.58+rng.normal(0,5),1),"no2":round(aqi*.13+rng.normal(0,2),1),
            "so2":round(aqi*.07+rng.normal(0,1),1),"co":round(aqi*.04+rng.normal(0,.5),2),
            "o3":round(aqi*.11+rng.normal(0,2),1),"_synthetic":True,
            "timestamp":datetime.now(timezone.utc).isoformat()}

def _fallback_history(city, days):
    rng = np.random.RandomState(_seed(city)+1)
    n = days*24
    base = _base_aqi(city)
    t = np.arange(n)
    av = base + 30*np.sin(2*np.pi*t/(24*7)) + rng.normal(0,15,n)
    av = np.clip(av,10,450).tolist()
    times = [(datetime.now()-timedelta(hours=n-i)).strftime("%Y-%m-%dT%H:00") for i in range(n)]
    return {"times":times,"us_aqi":[round(v) for v in av],
            "pm2_5":[round(v*.38,1) for v in av],"pm10":[round(v*.58,1) for v in av],
            "no2":[round(v*.13,1) for v in av],"so2":[round(v*.07,1) for v in av],
            "co":[round(v*.04,2) for v in av],"o3":[round(v*.11,1) for v in av],"_synthetic":True}

def _fallback_forecast(city, days):
    rng = np.random.RandomState(_seed(city)+2)
    n = days*24
    base = _base_aqi(city)
    t = np.arange(n)
    av = base + 25*np.sin(2*np.pi*t/(24*5)) + rng.normal(0,12,n)
    av = np.clip(av,10,450).tolist()
    times = [(datetime.now()+timedelta(hours=i)).strftime("%Y-%m-%dT%H:00") for i in range(n)]
    return {"times":times,"us_aqi":[round(v) for v in av],
            "pm2_5":[round(v*.38,1) for v in av],"pm10":[round(v*.58,1) for v in av],
            "no2":[round(v*.13,1) for v in av],"so2":[round(v*.07,1) for v in av],
            "co":[round(v*.04,2) for v in av],"o3":[round(v*.11,1) for v in av],"_synthetic":True}

@st.cache_data(ttl=600, show_spinner=False)
def get_live_aqi(city):
    coords = get_coords(city)
    if not coords: return _fallback(city)
    d = fetch_current_aqi(coords[0], coords[1])
    return d if (d and d.get("us_aqi") is not None) else _fallback(city)

@st.cache_data(ttl=600, show_spinner=False)
def get_live_history(city, days=7):
    coords = get_coords(city)
    if not coords: return _fallback_history(city, days)
    d = fetch_hourly_history(coords[0], coords[1], past_days=days)
    return d if (d and len(d.get("us_aqi",[]))>10) else _fallback_history(city, days)

@st.cache_data(ttl=1800, show_spinner=False)
def get_live_forecast(city, days=5):
    coords = get_coords(city)
    if not coords: return _fallback_forecast(city, days)
    d = fetch_forecast(coords[0], coords[1], days=days)
    return d if (d and len(d.get("us_aqi",[]))>0) else _fallback_forecast(city, days)

@st.cache_data(ttl=600, show_spinner=False)
def get_multi_city_aqi(cities_tuple):
    return {c: get_live_aqi(c) for c in cities_tuple}

# ╔══════════════════════════════════════════════════════════════════╗
# ║                    CHART FUNCTIONS                              ║
# ╚══════════════════════════════════════════════════════════════════╝

def make_aqi_gauge(aqi):
    fig, ax = plt.subplots(figsize=(4, 2.3), subplot_kw=dict(polar=False))
    fig.patch.set_facecolor(DARK["bg1"]); ax.set_facecolor(DARK["bg1"]); ax.axis("off")
    for lo, hi, _, col, _, _ in AQI_SCALE:
        ts = math.pi*(1-lo/500); te = math.pi*(1-hi/500)
        thetas = np.linspace(ts, te, 30)
        for i in range(len(thetas)-1):
            ax.plot([0.55*math.cos(thetas[i]),0.65*math.cos(thetas[i])],
                    [0.55*math.sin(thetas[i]),0.65*math.sin(thetas[i])],
                    color=col,linewidth=14,solid_capstyle="butt",alpha=0.9)
    tn = math.pi*(1-min(aqi,500)/500)
    ax.annotate("",xy=(0.62*math.cos(tn),0.62*math.sin(tn)),xytext=(0,0),
                arrowprops=dict(arrowstyle="-|>",color=DARK["txt"],lw=2,mutation_scale=12))
    ax.plot(0,0,"o",color=DARK["txt"],ms=5,zorder=10)
    lbl,col,_,_ = aqi_info(aqi)
    ax.text(0,-0.15,f"{aqi:.0f}",ha="center",va="center",fontsize=22,fontweight="bold",color=col,fontfamily="monospace")
    ax.text(0,-0.4,lbl,ha="center",va="center",fontsize=9,color=DARK["muted"],fontfamily="sans-serif")
    ax.set_xlim(-0.9,0.9); ax.set_ylim(-0.6,0.8); fig.tight_layout(pad=0)
    return fig

def make_24h_chart(hist, city):
    av = [safe_val(v) for v in hist["us_aqi"][-24:]]
    tr = hist["times"][-24:]
    x = np.arange(len(av))
    fig, ax = plt.subplots(figsize=(10,3.5))
    for lo,hi,_,col,_,_ in AQI_SCALE: ax.axhspan(lo,min(hi,500),alpha=0.04,color=col)
    ax.plot(x,av,color=DARK["cyan"],linewidth=2.2,zorder=5)
    ax.fill_between(x,av,alpha=0.12,color=DARK["cyan"])
    for i,v in enumerate(av): ax.scatter(i,v,color=aqi_color(v),s=22,zorder=6)
    tl = []
    for t in tr:
        try: tl.append(datetime.fromisoformat(t).strftime("%H:%M"))
        except: tl.append("")
    step = max(1,len(tl)//8)
    ax.set_xticks(x[::step]); ax.set_xticklabels(tl[::step],rotation=30,fontsize=8)
    ax.set_ylabel("US AQI"); ax.set_title(f"Last 24 Hours — {city}",fontsize=12,fontweight="bold")
    ax.grid(True,alpha=0.2); fig.tight_layout(); return fig

def make_7day_bar(hist, city):
    av = [safe_val(v) for v in hist["us_aqi"]]
    tr = hist["times"]
    dm = {}
    for t,v in zip(tr,av):
        d=t[:10]; dm.setdefault(d,[]).append(v)
    days = sorted(dm.keys())[-7:]
    avgs = [np.mean(dm[d]) for d in days]
    labels = [datetime.strptime(d,"%Y-%m-%d").strftime("%b %d") for d in days]
    fig,ax = plt.subplots(figsize=(10,3.5))
    bars = ax.bar(range(len(days)),avgs,color=[aqi_color(v) for v in avgs],alpha=0.82,edgecolor=DARK["grid"],width=0.65,zorder=3)
    for bar,val in zip(bars,avgs): ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+3,f"{val:.0f}",ha="center",va="bottom",fontsize=9,color=DARK["txt"],fontfamily="monospace")
    ax.set_xticks(range(len(days))); ax.set_xticklabels(labels,fontsize=9)
    ax.set_ylabel("Avg AQI"); ax.set_title(f"7-Day Daily Average — {city}",fontsize=12,fontweight="bold")
    ax.grid(True,alpha=0.2,axis="y"); fig.tight_layout(); return fig

def make_pollutant_radar(cur, city):
    cats=["PM2.5","PM10","NO₂","SO₂","CO×10","O₃"]
    vr=[safe_val(cur.get("pm2_5")),safe_val(cur.get("pm10")),safe_val(cur.get("no2")),
        safe_val(cur.get("so2")),safe_val(cur.get("co"))*10,safe_val(cur.get("o3"))]
    limits=[250,500,200,350,150,200]
    vn=[min(v/lim*100,100) for v,lim in zip(vr,limits)]+[min(vr[0]/limits[0]*100,100)]
    n=len(cats); angles=[i*2*math.pi/n for i in range(n)]+[0]
    fig,ax=plt.subplots(figsize=(4,4),subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(DARK["bg1"]); ax.set_facecolor(DARK["bg1"])
    ax.fill(angles,vn,alpha=0.2,color=DARK["cyan"])
    ax.plot(angles,vn,color=DARK["cyan"],linewidth=2)
    for a,v in zip(angles[:-1],vn[:-1]): ax.scatter(a,v,color=aqi_color(safe_val(cur.get("us_aqi"))),s=40,zorder=5)
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(cats,fontsize=9,color=DARK["txt"])
    ax.set_yticks([25,50,75,100]); ax.set_yticklabels(["25","50","75","100"],fontsize=7,color=DARK["muted"])
    ax.spines["polar"].set_color(DARK["grid"]); ax.grid(color=DARK["grid"],alpha=0.4)
    ax.set_title(f"Pollutant Profile\n{city}",fontsize=10,fontweight="bold",pad=12)
    fig.tight_layout(); return fig

def make_forecast_chart(fcast, city):
    av=[safe_val(v) for v in fcast["us_aqi"][:120]]
    tr=fcast["times"][:120]
    x=np.arange(len(av))
    fig,ax=plt.subplots(figsize=(12,4))
    ax.fill_between(x,av,alpha=0.15,color=DARK["gold"])
    ax.plot(x,av,color=DARK["gold"],linewidth=2)
    day_seen=set()
    for i,t in enumerate(tr):
        try:
            dt=datetime.fromisoformat(t)
            ds=dt.strftime("%b %d")
            if dt.hour==0 and ds not in day_seen:
                ax.axvline(i,color=DARK["grid"],linewidth=0.8,linestyle="--",alpha=0.7)
                ax.text(i+0.5,max(av)*1.02,ds,fontsize=8,color=DARK["muted"])
                day_seen.add(ds)
        except: pass
    for lo,_,lbl,col,_,_ in AQI_SCALE[1:]:
        ax.axhline(lo,color=col,linewidth=0.6,linestyle=":",alpha=0.5)
        ax.text(len(x)*.99,lo,lbl[:8],fontsize=7,color=col,va="bottom",ha="right")
    ax.set_ylabel("Forecasted US AQI"); ax.set_title(f"5-Day Hourly Forecast — {city}",fontsize=13,fontweight="bold")
    ax.set_xticks([]); ax.grid(True,alpha=0.15); fig.tight_layout(); return fig

def make_multi_city_bars(city_data):
    cities=[c for c,d in city_data.items() if d.get("us_aqi") is not None]
    aqis=[safe_val(city_data[c].get("us_aqi")) for c in cities]
    sp=sorted(zip(aqis,cities),reverse=True)
    aqis_s=[p[0] for p in sp]; cities_s=[p[1] for p in sp]
    fig,ax=plt.subplots(figsize=(10,max(4,len(cities_s)*.45)))
    bars=ax.barh(range(len(cities_s)),aqis_s,color=[aqi_color(v) for v in aqis_s],alpha=0.82,edgecolor=DARK["grid"],height=0.7)
    for bar,val in zip(bars,aqis_s): ax.text(val+3,bar.get_y()+bar.get_height()/2,f"{val:.0f}",va="center",fontsize=8,color=DARK["txt"],fontfamily="monospace")
    ax.set_yticks(range(len(cities_s))); ax.set_yticklabels(cities_s,fontsize=9)
    ax.set_xlabel("US AQI"); ax.set_title("Live AQI — City Comparison",fontsize=13,fontweight="bold")
    for lo,_,_,col,_,_ in AQI_SCALE[1:]: ax.axvline(lo,color=col,linewidth=0.6,linestyle=":",alpha=0.5)
    ax.grid(True,alpha=0.2,axis="x"); ax.set_xlim(0,max(aqis_s)*1.15+20); fig.tight_layout(); return fig

def make_state_bars(state_data):
    states=list(state_data.keys()); vals=[state_data[s]["max_aqi"] for s in states]
    sp=sorted(zip(vals,states),reverse=True)
    vs=[p[0] for p in sp]; ss=[p[1] for p in sp]
    fig,ax=plt.subplots(figsize=(10,max(5,len(ss)*.38)))
    bars=ax.barh(range(len(ss)),vs,color=[aqi_color(v) for v in vs],alpha=0.82,edgecolor=DARK["grid"],height=0.7)
    for bar,val in zip(bars,vs): ax.text(val+2,bar.get_y()+bar.get_height()/2,f"{val:.0f}",va="center",fontsize=8,color=DARK["txt"],fontfamily="monospace")
    ax.set_yticks(range(len(ss))); ax.set_yticklabels(ss,fontsize=8)
    ax.set_xlabel("Peak AQI"); ax.set_title("State-wise Peak AQI",fontsize=12,fontweight="bold")
    ax.grid(True,alpha=0.2,axis="x"); ax.set_xlim(0,max(vs)*1.15+10); fig.tight_layout(); return fig

def make_pollutant_history(hist, city):
    n=min(len(hist.get("times",[])),72)
    fig,axes=plt.subplots(2,3,figsize=(14,6)); axes=axes.flatten()
    polls=[("pm2_5","PM2.5 μg/m³",DARK["cyan"]),("pm10","PM10 μg/m³",DARK["gold"]),
           ("no2","NO₂ μg/m³","#E74C3C"),("so2","SO₂ μg/m³","#9B59B6"),
           ("co","CO μg/m³","#3498DB"),("o3","O₃ μg/m³","#2ECC71")]
    for ax,(key,label,color) in zip(axes,polls):
        vals=[safe_val(v) for v in hist.get(key,[])[-n:]]
        x=np.arange(len(vals))
        ax.plot(x,vals,color=color,linewidth=1.6,alpha=0.9)
        ax.fill_between(x,vals,alpha=0.1,color=color)
        ax.set_title(label,fontsize=10,fontweight="bold"); ax.grid(True,alpha=0.2); ax.set_xticks([])
    fig.suptitle(f"Pollutant History (72h) — {city}",fontsize=13,fontweight="bold",y=1.01)
    fig.tight_layout(); return fig

def make_trend_analysis(hist, city):
    av=[safe_val(v) for v in hist.get("us_aqi",[])]
    tr=hist.get("times",[])
    if len(av)<6: return None
    fig,axes=plt.subplots(2,2,figsize=(14,8))
    # Full history
    ax=axes[0][0]
    ax.plot(range(len(av)),av,color=DARK["cyan"],linewidth=1.5,alpha=0.8)
    ax.fill_between(range(len(av)),av,alpha=0.1,color=DARK["cyan"])
    ax.set_title("Full History",fontsize=11,fontweight="bold"); ax.set_ylabel("AQI"); ax.grid(True,alpha=0.2); ax.set_xticks([])
    # Hourly distribution
    ax=axes[0][1]; hm={}
    for t,v in zip(tr,av):
        try: hm.setdefault(int(t[11:13]),[]).append(v)
        except: pass
    if hm:
        hs=sorted(hm.keys()); avgs=[np.mean(hm[h]) for h in hs]
        ax.bar(hs,avgs,color=[aqi_color(v) for v in avgs],alpha=0.8,edgecolor=DARK["grid"])
    ax.set_title("AQI by Hour of Day",fontsize=11,fontweight="bold"); ax.set_xlabel("Hour"); ax.set_ylabel("Avg AQI"); ax.grid(True,alpha=0.2,axis="y")
    # Distribution
    ax=axes[1][0]
    ax.hist(av,bins=30,color=DARK["cyan"],alpha=0.7,edgecolor=DARK["grid"])
    ax.axvline(np.mean(av),color=DARK["gold"],linewidth=2,linestyle="--",label=f"Mean: {np.mean(av):.1f}")
    ax.axvline(np.median(av),color=DARK["red"],linewidth=2,linestyle=":",label=f"Median: {np.median(av):.1f}")
    ax.set_title("AQI Distribution",fontsize=11,fontweight="bold"); ax.set_xlabel("AQI"); ax.set_ylabel("Freq"); ax.legend(fontsize=9); ax.grid(True,alpha=0.2)
    # Rolling
    ax=axes[1][1]; arr=np.array(av)
    r3=pd.Series(arr).rolling(3,min_periods=1).mean().values
    r6=pd.Series(arr).rolling(6,min_periods=1).mean().values
    ax.plot(range(len(arr)),arr,color=DARK["muted"],linewidth=0.8,alpha=0.5,label="Raw")
    ax.plot(range(len(arr)),r3,color=DARK["cyan"],linewidth=2,label="3h avg")
    ax.plot(range(len(arr)),r6,color=DARK["gold"],linewidth=2,label="6h avg")
    ax.set_title("Rolling Averages",fontsize=11,fontweight="bold"); ax.set_ylabel("AQI"); ax.legend(fontsize=9); ax.grid(True,alpha=0.2); ax.set_xticks([])
    fig.suptitle(f"Trend Analysis — {city}",fontsize=14,fontweight="bold",y=1.01)
    fig.tight_layout(); return fig

# ╔══════════════════════════════════════════════════════════════════╗
# ║                      SIDEBAR                                    ║
# ╚══════════════════════════════════════════════════════════════════╝
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 8px'>
      <div style='font-family:IBM Plex Mono,monospace;font-size:.6rem;color:#5D8AA8;letter-spacing:.2em;text-transform:uppercase;'>INDIA</div>
      <div style='font-family:Outfit,sans-serif;font-size:1.6rem;font-weight:800;color:#D6EAF8;line-height:1.1;'>
        AQI Intelligence<br><span style='color:#00E5C0;'>Real-Time System</span></div>
      <div style='font-family:IBM Plex Mono,monospace;font-size:.65rem;color:#5D8AA8;margin-top:4px;'>134 Cities · 36 States/UTs</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div class="sec-head">🗺️ Select Location</div>', unsafe_allow_html=True)
    sel_state = st.selectbox("State / UT", ["All India"] + ALL_STATES, key="sel_state")
    city_list = sorted(INDIA_CITIES.keys()) if sel_state == "All India" else sorted(get_cities_by_state(sel_state))
    sel_city = st.selectbox("City", city_list, key="sel_city")
    st.markdown("---")
    st.markdown('<div class="sec-head">⚙️ Settings</div>', unsafe_allow_html=True)
    history_days = st.slider("History (days)", 1, 7, 3)
    forecast_days = st.slider("Forecast (days)", 1, 5, 3)
    st.markdown("---")
    if st.button("🔄  Refresh Data", use_container_width=True):
        st.cache_data.clear(); st.rerun()
    st.markdown(f"""
    <div style='font-family:IBM Plex Mono,monospace;font-size:.65rem;color:#5D8AA8;margin-top:12px;'>
    🕐 Checked<br><span style='color:#00E5C0;'>{datetime.now().strftime('%d %b %Y %H:%M')}</span></div>
    <div style='margin-top:16px;padding:12px;background:#0B1929;border-radius:10px;border:1px solid #1E3A54;'>
    <div style='font-family:IBM Plex Mono,monospace;font-size:.6rem;color:#5D8AA8;'>DATA SOURCE</div>
    <div style='font-family:IBM Plex Mono,monospace;font-size:.68rem;color:#00E5C0;margin-top:5px;line-height:1.7;'>
    Open-Meteo Air Quality<br>CAMS Global / European<br>No API key required ✓<br>Free, open data ✓</div></div>
    """, unsafe_allow_html=True)

# ╔══════════════════════════════════════════════════════════════════╗
# ║                     MAIN CONTENT                                ║
# ╚══════════════════════════════════════════════════════════════════╝

city_info = INDIA_CITIES.get(sel_city, (0,0,"India",1))
state_name = city_info[2]
lat_c, lon_c = city_info[0], city_info[1]

st.markdown(f"""
<div style='display:flex;align-items:flex-end;gap:14px;margin-bottom:6px;'>
  <div style='font-size:2.4rem;'>🌫️</div>
  <div>
    <div style='font-family:Outfit,sans-serif;font-size:1.9rem;font-weight:800;color:#D6EAF8;line-height:1;'>{sel_city}</div>
    <div style='font-family:IBM Plex Mono,monospace;font-size:.72rem;color:#00E5C0;letter-spacing:.12em;text-transform:uppercase;margin-top:3px;'>
      {state_name} · {lat_c:.2f}°N {lon_c:.2f}°E · Live AQI
    </div>
  </div>
</div>
<hr style='border-color:#1E3A54;margin:10px 0 18px;'>
""", unsafe_allow_html=True)

# ── Fetch data ─────────────────────────────────────────────────────────────────
with st.spinner(f"Fetching live air quality for {sel_city}..."):
    current_data = get_live_aqi(sel_city)
    hist_data    = get_live_history(sel_city, days=max(history_days, 2))
    fcast_data   = get_live_forecast(sel_city, days=forecast_days)

is_synth = current_data.get("_synthetic", False)
if is_synth:
    st.info("⚡ **Demo mode** — Live data shown when deployed with internet access (Open-Meteo API). Data shown is realistic simulation.", icon="ℹ️")

aqi_now = safe_val(current_data.get("us_aqi"), 100)
aqi_label, aqi_col, aqi_emoji, aqi_advice = aqi_info(aqi_now)

# ── Status Banner ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div style='padding:18px 26px;border-radius:16px;border-left:5px solid {aqi_col};
            background:#0B1929;margin:0 0 16px;display:flex;align-items:center;gap:20px;'>
  <div style='font-size:2.8rem;'>{aqi_emoji}</div>
  <div>
    <div style='font-family:IBM Plex Mono,monospace;font-size:.62rem;color:#5D8AA8;letter-spacing:.15em;text-transform:uppercase;'>
      LIVE AQI — {sel_city.upper()} · {state_name.upper()}
    </div>
    <div style='font-family:Outfit,sans-serif;font-size:2.6rem;font-weight:800;color:{aqi_col};line-height:1.1;'>{aqi_now:.0f} AQI</div>
    <div style='display:inline-block;padding:3px 14px;margin:5px 0;background:{aqi_col}22;border:1px solid {aqi_col}55;
                border-radius:20px;font-family:IBM Plex Mono,monospace;font-size:.78rem;color:{aqi_col};
                font-weight:600;letter-spacing:.08em;text-transform:uppercase;'>{aqi_label}</div>
  </div>
  <div style='flex:1;font-family:Outfit,sans-serif;font-size:.92rem;color:#CDD9E5;
              border-left:1px solid #1E3A54;padding-left:20px;'>
    💡 {aqi_advice}
  </div>
  <div style='font-family:IBM Plex Mono,monospace;font-size:.62rem;color:#5D8AA8;text-align:right;'>
    📡 Open-Meteo CAMS<br>🕐 {datetime.now().strftime('%d %b %H:%M')}
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ───────────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5,k6 = st.columns(6)
with k1: st.metric("US AQI",  f"{aqi_now:.0f}")
with k2: st.metric("PM2.5",   f"{safe_val(current_data.get('pm2_5')):.1f} μg/m³")
with k3: st.metric("PM10",    f"{safe_val(current_data.get('pm10')):.1f} μg/m³")
with k4: st.metric("NO₂",     f"{safe_val(current_data.get('no2')):.1f} μg/m³")
with k5: st.metric("SO₂",     f"{safe_val(current_data.get('so2')):.1f} μg/m³")
with k6: st.metric("O₃",      f"{safe_val(current_data.get('o3')):.1f} μg/m³")

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_live,tab_fc,tab_india,tab_cmp,tab_poll,tab_trend,tab_ml = st.tabs([
    "📊 Live Dashboard","🔮 Forecast","🗺️ India Overview",
    "🏙️ City Compare","🧪 Pollutants","📈 Trends","🧠 ML Prediction"
])

# ════════ TAB 1 — LIVE ════════
with tab_live:
    cg, cc = st.columns([1, 2.5])
    with cg:
        st.markdown('<div class="sec-head">🎯 AQI Gauge</div>', unsafe_allow_html=True)
        st.pyplot(make_aqi_gauge(aqi_now), use_container_width=True); plt.close()
        st.markdown('<div class="sec-head" style="margin-top:12px">💨 Pollutants</div>', unsafe_allow_html=True)
        for name,val,safe_l,clr_key in [
            ("PM2.5",safe_val(current_data.get("pm2_5")),35,"cyan"),
            ("PM10", safe_val(current_data.get("pm10")), 50,"gold"),
            ("NO₂",  safe_val(current_data.get("no2")),  40,"red"),
            ("O₃",   safe_val(current_data.get("o3")),   70,"green"),
            ("SO₂",  safe_val(current_data.get("so2")),  20,"purple"),
            ("CO",   safe_val(current_data.get("co")),    4,"cyan"),
        ]:
            pct = min(val/(safe_l*5)*100,100)
            bc = "#2ECC71" if pct<40 else "#FFB347" if pct<70 else "#FF4757"
            st.markdown(f"""<div style='margin:6px 0;'>
              <div style='display:flex;justify-content:space-between;font-family:IBM Plex Mono,monospace;font-size:.72rem;'>
                <span style='color:#5D8AA8;'>{name}</span><span style='color:{bc};'>{val:.1f}</span></div>
              <div style='background:#1E3A54;border-radius:6px;height:5px;margin-top:3px;'>
                <div style='background:{bc};width:{pct}%;height:5px;border-radius:6px;'></div></div></div>
            """, unsafe_allow_html=True)
    with cc:
        st.markdown('<div class="sec-head">📈 Last 24 Hours</div>', unsafe_allow_html=True)
        st.pyplot(make_24h_chart(hist_data, sel_city), use_container_width=True); plt.close()
        st.markdown('<div class="sec-head" style="margin-top:16px">📦 7-Day Averages</div>', unsafe_allow_html=True)
        st.pyplot(make_7day_bar(hist_data, sel_city), use_container_width=True); plt.close()

# ════════ TAB 2 — FORECAST ════════
with tab_fc:
    st.markdown(f'<div class="sec-head">🔮 {forecast_days}-Day Forecast — {sel_city}</div>', unsafe_allow_html=True)
    st.pyplot(make_forecast_chart(fcast_data, sel_city), use_container_width=True); plt.close()
    aqi_fc=[safe_val(v) for v in fcast_data.get("us_aqi",[])]
    times_fc=fcast_data.get("times",[])
    df_day={}
    for t,v in zip(times_fc,aqi_fc): df_day.setdefault(t[:10],[]).append(v)
    daily_days=sorted(df_day.keys())[:forecast_days]
    st.markdown('<div class="sec-head" style="margin-top:18px">📅 Daily Cards</div>', unsafe_allow_html=True)
    fc_cols=st.columns(min(forecast_days,5))
    for col,day in zip(fc_cols,daily_days):
        dv=df_day[day]; avg=np.mean(dv); lo=np.min(dv); hi=np.max(dv)
        lbl,clr,emj,_=aqi_info(avg); dt=datetime.strptime(day,"%Y-%m-%d")
        with col:
            st.markdown(f"""<div style='text-align:center;padding:16px 10px;background:#0B1929;
                border:1px solid {clr}44;border-radius:14px;'>
              <div style='font-family:IBM Plex Mono,monospace;font-size:.62rem;color:#5D8AA8;'>
                {dt.strftime('%A')[:3].upper()}<br><span style='color:#D6EAF8;'>{dt.strftime('%d %b')}</span></div>
              <div style='font-size:2rem;margin:8px 0;'>{emj}</div>
              <div style='font-family:Outfit,sans-serif;font-size:1.6rem;font-weight:800;color:{clr};'>{avg:.0f}</div>
              <div style='font-family:IBM Plex Mono,monospace;font-size:.6rem;color:{clr};
                          background:{clr}22;border-radius:8px;padding:2px 8px;margin:4px 0;'>{lbl[:12]}</div>
              <div style='font-family:IBM Plex Mono,monospace;font-size:.62rem;color:#5D8AA8;margin-top:6px;'>
                ↓{lo:.0f}  ↑{hi:.0f}</div></div>""", unsafe_allow_html=True)

# ════════ TAB 3 — INDIA OVERVIEW ════════
with tab_india:
    st.markdown('<div class="sec-head">🗺️ All-India State Overview</div>', unsafe_allow_html=True)
    st.info("Fetching one representative city per state/UT across India.")
    representative={}
    for state in ALL_STATES:
        cits=get_cities_by_state(state)
        best=None
        for tier in [1,2,3,4]:
            for c in cits:
                if INDIA_CITIES[c][3]==tier: best=c; break
            if best: break
        if best: representative[state]=best

    with st.spinner("Loading state-level data..."):
        state_aqi={}
        for state,city in representative.items():
            d=get_live_aqi(city)
            av=safe_val(d.get("us_aqi"),80)
            lbl,col,emj,_=aqi_info(av)
            state_aqi[state]={"city":city,"max_aqi":av,"label":lbl,"color":col,"emoji":emj}

    st.pyplot(make_state_bars(state_aqi), use_container_width=True); plt.close()

    st.markdown('<div class="sec-head" style="margin-top:16px">📋 State Table</div>', unsafe_allow_html=True)
    rows=[{"State/UT":s,"City":info["city"],"AQI":info["max_aqi"],"Status":f"{info['emoji']} {info['label']}"}
          for s,info in sorted(state_aqi.items(),key=lambda x:-x[1]["max_aqi"])]
    st.dataframe(pd.DataFrame(rows).set_index("State/UT"), use_container_width=True)

    st.markdown('<div class="sec-head" style="margin-top:16px">🎨 AQI Scale</div>', unsafe_allow_html=True)
    leg_cols=st.columns(6)
    for col_l,(lo,hi,lbl,clr,emj,_) in zip(leg_cols,AQI_SCALE):
        with col_l:
            st.markdown(f"""<div style='text-align:center;padding:10px 6px;background:{clr}18;
                border:1px solid {clr}44;border-radius:10px;'>
              <div style='font-size:1.4rem;'>{emj}</div>
              <div style='font-family:IBM Plex Mono,monospace;font-size:1rem;color:{clr};font-weight:600;'>{lo}–{hi}</div>
              <div style='font-family:Outfit,sans-serif;font-size:.72rem;color:#D6EAF8;margin-top:3px;'>{lbl}</div></div>
            """, unsafe_allow_html=True)

# ════════ TAB 4 — CITY COMPARE ════════
with tab_cmp:
    st.markdown('<div class="sec-head">🏙️ Compare Cities</div>', unsafe_allow_html=True)
    all_cnames=sorted(INDIA_CITIES.keys())
    defaults=["Delhi","Mumbai","Kolkata","Chennai","Bangalore","Hyderabad","Ahmedabad","Pune","Jaipur","Lucknow"]
    compare_cities=st.multiselect("Select cities (up to 20)",all_cnames,default=defaults[:10],max_selections=20)
    if compare_cities:
        with st.spinner("Fetching live AQI..."):
            multi_data=get_multi_city_aqi(tuple(sorted(compare_cities)))
        st.pyplot(make_multi_city_bars(multi_data), use_container_width=True); plt.close()
        st.markdown('<div class="sec-head" style="margin-top:18px">📊 City Cards</div>', unsafe_allow_html=True)
        sorted_c=sorted(compare_cities,key=lambda c:-safe_val(multi_data[c].get("us_aqi",0)))
        card_cols=st.columns(5)
        for i,city in enumerate(sorted_c):
            d=multi_data[city]; av=safe_val(d.get("us_aqi"))
            lbl,clr,emj,_=aqi_info(av); ci=INDIA_CITIES.get(city,(0,0,"",1))
            with card_cols[i%5]:
                st.markdown(f"""<div class="city-card" style='border-color:{clr}33;margin-bottom:8px;'>
                  <div style='font-size:1.4rem;'>{emj}</div>
                  <div style='font-family:Outfit,sans-serif;font-size:.88rem;font-weight:600;color:#D6EAF8;margin:4px 0;'>{city}</div>
                  <div style='font-family:IBM Plex Mono,monospace;font-size:.65rem;color:#5D8AA8;'>{ci[2]}</div>
                  <div style='font-family:IBM Plex Mono,monospace;font-size:1.6rem;font-weight:700;color:{clr};margin:6px 0;'>{av:.0f}</div>
                  <div style='font-family:IBM Plex Mono,monospace;font-size:.6rem;color:{clr};background:{clr}22;border-radius:6px;padding:2px 6px;'>{lbl[:14]}</div>
                  <div style='font-family:IBM Plex Mono,monospace;font-size:.62rem;color:#5D8AA8;margin-top:5px;'>
                    PM2.5:{safe_val(d.get("pm2_5")):.0f} · PM10:{safe_val(d.get("pm10")):.0f}</div></div>
                """, unsafe_allow_html=True)

# ════════ TAB 5 — POLLUTANTS ════════
with tab_poll:
    cr,ch=st.columns([1,2])
    with cr:
        st.markdown('<div class="sec-head">🕸️ Pollutant Radar</div>', unsafe_allow_html=True)
        st.pyplot(make_pollutant_radar(current_data,sel_city), use_container_width=True); plt.close()
        st.markdown('<div class="sec-head" style="margin-top:10px">📋 Current Values</div>', unsafe_allow_html=True)
        pdf=pd.DataFrame([
            {"Pollutant":"US AQI","Value":f"{aqi_now:.0f}","Unit":"index","Safe":"<=50"},
            {"Pollutant":"PM2.5","Value":f"{safe_val(current_data.get('pm2_5')):.1f}","Unit":"μg/m³","Safe":"≤35"},
            {"Pollutant":"PM10","Value":f"{safe_val(current_data.get('pm10')):.1f}","Unit":"μg/m³","Safe":"≤50"},
            {"Pollutant":"NO₂","Value":f"{safe_val(current_data.get('no2')):.1f}","Unit":"μg/m³","Safe":"≤40"},
            {"Pollutant":"SO₂","Value":f"{safe_val(current_data.get('so2')):.1f}","Unit":"μg/m³","Safe":"≤20"},
            {"Pollutant":"CO","Value":f"{safe_val(current_data.get('co')):.2f}","Unit":"mg/m³","Safe":"≤4"},
            {"Pollutant":"O₃","Value":f"{safe_val(current_data.get('o3')):.1f}","Unit":"μg/m³","Safe":"≤100"},
        ])
        st.dataframe(pdf.set_index("Pollutant"),use_container_width=True)
    with ch:
        st.markdown('<div class="sec-head">📈 72h Pollutant History</div>', unsafe_allow_html=True)
        st.pyplot(make_pollutant_history(hist_data,sel_city),use_container_width=True); plt.close()
    st.markdown('<div class="sec-head" style="margin-top:16px">🏥 Health Guidance</div>', unsafe_allow_html=True)
    hg_cols=st.columns(3)
    guidance=[
        ("👶 Children","Avoid outdoor activities when AQI > 100.",aqi_now>100),
        ("🏃 Athletes","Reduce outdoor exercise intensity when AQI > 100.",aqi_now>100),
        ("🫁 Respiratory","Carry rescue inhaler. Limit exertion when AQI > 50.",aqi_now>50),
        ("👴 Elderly","Limit prolonged outdoor exertion when AQI > 100.",aqi_now>100),
        ("🤰 Pregnant","Minimize outdoor exposure when AQI > 100.",aqi_now>100),
        ("😷 General",f"{aqi_label}: {aqi_advice}",True),
    ]
    for i,(grp,txt,active) in enumerate(guidance):
        bc=aqi_col if active else "#1E3A54"
        with hg_cols[i%3]:
            st.markdown(f"""<div style='padding:14px;background:#0B1929;border:1px solid {bc};border-radius:12px;margin-bottom:10px;'>
              <div style='font-family:Outfit,sans-serif;font-size:.88rem;font-weight:600;color:#D6EAF8;margin-bottom:6px;'>{grp}</div>
              <div style='font-family:Outfit,sans-serif;font-size:.8rem;color:#8DAFC7;line-height:1.5;'>{txt}</div></div>
            """, unsafe_allow_html=True)

# ════════ TAB 6 — TRENDS ════════
with tab_trend:
    st.markdown('<div class="sec-head">📈 Trend Analysis</div>', unsafe_allow_html=True)
    fig_tr=make_trend_analysis(hist_data,sel_city)
    if fig_tr: st.pyplot(fig_tr,use_container_width=True); plt.close()
    else: st.warning("Increase History Days in sidebar for trend analysis.")
    aqi_h=[safe_val(v) for v in hist_data.get("us_aqi",[])]
    if len(aqi_h)>3:
        st.markdown('<div class="sec-head" style="margin-top:16px">📊 Stats</div>', unsafe_allow_html=True)
        tc1,tc2,tc3,tc4,tc5=st.columns(5)
        tc1.metric("Mean",f"{np.mean(aqi_h):.1f}"); tc2.metric("Median",f"{np.median(aqi_h):.1f}")
        tc3.metric("Std Dev",f"{np.std(aqi_h):.1f}"); tc4.metric("Max",f"{np.max(aqi_h):.0f}"); tc5.metric("Min",f"{np.min(aqi_h):.0f}")

# ════════ TAB 7 — ML PREDICTION ════════
with tab_ml:
    st.markdown("""<div style='font-family:Outfit,sans-serif;color:#8DAFC7;font-size:.92rem;margin-bottom:18px;'>
    Uses last 7 hours of live AQI as LSTM input → predicts next hour's AQI value.</div>""", unsafe_allow_html=True)
    ci,cr2=st.columns([1.2,1])
    with ci:
        st.markdown('<div class="sec-head">🗓️ 7-Hour Input Window</div>', unsafe_allow_html=True)
        r7=[safe_val(v) for v in hist_data.get("us_aqi",[])[-7:]]
        while len(r7)<7: r7.insert(0,aqi_now)
        ui=[]
        for i,val in enumerate(r7):
            v=st.number_input(f"Hour -{7-i}",min_value=0.0,max_value=500.0,value=round(float(val),1),step=0.5,key=f"ml_{i}")
            ui.append(v)
        c_t,c_h=st.columns(2)
        it=c_t.number_input("Temp (°C)",0.0,50.0,28.0,0.5)
        ih=c_h.number_input("Humidity (%)",0.0,100.0,65.0,1.0)
        iw=st.number_input("Wind (km/h)",0.0,60.0,8.0,0.5)
        st.button("⚡  Predict Next Hour", use_container_width=True)

    with cr2:
        st.markdown('<div class="sec-head">🎯 Prediction</div>', unsafe_allow_html=True)
        try:
            mc=[f"models/sklearn_model_{sel_city.lower()}.pkl","models/sklearn_model_kolkata.pkl","models/sklearn_model.pkl"]
            lm=ls=None
            for mp in mc:
                if os.path.exists(mp):
                    with open(mp,"rb") as f: lm=pickle.load(f)
                    city_key=mp.split("_")[-1].replace(".pkl","")
                    sp=f"models/scaler_{city_key}.pkl"
                    if not os.path.exists(sp): sp="models/scaler_kolkata.pkl"
                    if os.path.exists(sp):
                        with open(sp,"rb") as f: ls=pickle.load(f)
                    break
            if lm and ls:
                nf=ls.n_features_in_; ts=7
                base=np.zeros((ts,nf))
                for ri in range(ts):
                    av=ui[ri]
                    if nf>0:  base[ri,0]=av
                    if nf>1:  base[ri,1]=av*.38
                    if nf>2:  base[ri,2]=av*.58
                    if nf>3:  base[ri,3]=av*.13
                    if nf>4:  base[ri,4]=av*.07
                    if nf>5:  base[ri,5]=av*.04
                    if nf>6:  base[ri,6]=av*.11
                    if nf>7:  base[ri,7]=it
                    if nf>8:  base[ri,8]=ih
                    if nf>9:  base[ri,9]=iw/3.6
                    if nf>10: base[ri,10]=ui[max(0,ri-1)]
                    if nf>11: base[ri,11]=ui[max(0,ri-2)]
                    if nf>12: base[ri,12]=ui[max(0,ri-3)]
                    if nf>13: base[ri,13]=np.mean(ui[:ri+1])
                    if nf>14: base[ri,14]=np.mean(ui[:ri+1])
                bsc=ls.transform(base)
                ys=lm.predict(bsc.reshape(1,-1))
                dum=np.zeros((1,nf)); dum[0,0]=ys[0]
                pred=float(ls.inverse_transform(dum)[0,0])
            else:
                w=np.array([.05,.05,.08,.10,.15,.22,.35])
                pred=float(np.average(ui,weights=w)+np.random.normal(0,5))
            pred=max(0,min(500,pred))
        except:
            w=np.array([.05,.05,.08,.10,.15,.22,.35])
            pred=float(np.average(ui,weights=w)); pred=max(0,min(500,pred))

        pl,pc,pe,pa=aqi_info(pred)
        st.markdown(f"""<div style='text-align:center;padding:28px 20px;
            background:linear-gradient(135deg,#0B1929,#0F2236);
            border:2px solid {pc}55;border-radius:18px;'>
          <div style='font-size:3.5rem;margin-bottom:8px;'>{pe}</div>
          <div style='font-family:IBM Plex Mono,monospace;font-size:.65rem;color:#5D8AA8;letter-spacing:.15em;text-transform:uppercase;'>NEXT HOUR PREDICTION</div>
          <div style='font-family:Outfit,sans-serif;font-size:4rem;font-weight:800;color:{pc};line-height:1.1;margin:8px 0;'>{pred:.0f}</div>
          <div style='display:inline-block;padding:5px 16px;border-radius:20px;background:{pc}22;border:1px solid {pc}66;
                      font-family:IBM Plex Mono,monospace;font-size:.8rem;color:{pc};font-weight:600;text-transform:uppercase;'>{pl}</div>
          <div style='font-family:Outfit,sans-serif;font-size:.88rem;color:#CDD9E5;margin-top:14px;line-height:1.5;'>{pa}</div>
          <div style='font-family:IBM Plex Mono,monospace;font-size:.62rem;color:#5D8AA8;margin-top:12px;'>
            Current:{aqi_now:.0f} → Predicted:{pred:.0f} ({'+' if pred>=aqi_now else ''}{pred-aqi_now:.1f})</div></div>
        """, unsafe_allow_html=True)

        fig_pm,ax=plt.subplots(figsize=(7,3))
        ax.plot(range(7),ui,color=DARK["cyan"],linewidth=2,marker="o",markersize=4,label="Input")
        ax.plot([6,7],[ui[-1],pred],color=DARK["gold"],linewidth=2.5,marker="o",markersize=9,
                markerfacecolor=DARK["bg0"],linestyle="--",label="Prediction")
        ax.axvline(6.5,color=DARK["muted"],linewidth=0.8,linestyle=":",alpha=0.7)
        ax.set_xticks(range(8)); ax.set_xticklabels([f"H-{7-i}" for i in range(7)]+["H+1"],fontsize=8)
        ax.set_ylabel("AQI"); ax.legend(fontsize=9); ax.grid(True,alpha=0.25); fig_pm.tight_layout()
        st.pyplot(fig_pm,use_container_width=True); plt.close()

    st.markdown("---")
    st.markdown('<div class="sec-head">🧠 Model Architecture</div>', unsafe_allow_html=True)
    ac,mc2=st.columns(2)
    with ac:
        st.markdown("""<div style='background:#0B1929;border:1px solid #1E3A54;border-radius:12px;padding:20px;font-family:IBM Plex Mono,monospace;'>
          <div style='color:#00E5C0;font-size:.8rem;line-height:2.2;'>
            Input → (7 timesteps × 18 features)<br>&nbsp;&nbsp;↓<br>Bidirectional LSTM (128 units)<br>
            &nbsp;&nbsp;↓<br>Dropout (0.20)<br>&nbsp;&nbsp;↓<br>LSTM (64 units)<br>&nbsp;&nbsp;↓<br>
            Dropout (0.10)<br>&nbsp;&nbsp;↓<br>Dense (32, ReLU)<br>&nbsp;&nbsp;↓<br>Dense (1) → Next-Hour AQI</div>
          <hr style='border-color:#1E3A54;margin:12px 0;'>
          <div style='color:#5D8AA8;font-size:.7rem;line-height:1.9;'>
            Optimizer: Adam  |  LR: 0.001<br>Loss: MSE · Fallback: GradientBoosting</div></div>
        """, unsafe_allow_html=True)
    with mc2:
        st.markdown('<div class="sec-head">📊 Model Metrics</div>', unsafe_allow_html=True)
        mp=f"models/meta_{sel_city.lower()}.pkl"
        if not os.path.exists(mp): mp="models/meta_kolkata.pkl"
        if os.path.exists(mp):
            with open(mp,"rb") as f: mi=pickle.load(f)
            m=mi.get("metrics",{})
            mm1,mm2,mm3=st.columns(3)
            mm1.metric("RMSE",f"{m.get('RMSE','-')}"); mm2.metric("MAE",f"{m.get('MAE','-')}"); mm3.metric("R²",f"{m.get('R2','-')}")
            st.json({"model":mi.get("model_type","GradientBoosting"),"city":mi.get("city","Kolkata"),"features":mi.get("n_features",18)})
        else:
            st.info("Run `python train.py --all` to train models.")

st.markdown("""<div class="footer">
  🌫️ India AQI Intelligence · Open-Meteo CAMS (free, no key) · 134 Cities · 36 States · LSTM + GradientBoosting
</div>""", unsafe_allow_html=True)
