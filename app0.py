import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# IRAPUATO, REIMAGINED — refreshed visual version
# Uses the updated workbook and locally supplied 2050 scenarios.
# ============================================================
st.set_page_config(page_title="IRAPUATO, REIMAGINED", page_icon="🌱", layout="wide", initial_sidebar_state="collapsed")
BASE = Path(__file__).parent
DATABASE_FILE = "IRAPUATO_REIMAGINED_Data.xlsx"
YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v=e0cehcrWnb8"  # Keep the team video unchanged.
SCENARIO_A = BASE / "future_a_2050.jpeg"
SCENARIO_B = BASE / "future_b_2050.jpeg"

DARK = "#101411"
LIME = "#B8F34A"
PAPER = "#F5F6F0"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=DM+Sans:wght@400;500;600;700&display=swap');
html, body, [class*="css"] {{ font-family:'DM Sans',sans-serif; }}
.stApp {{ background:{PAPER}; color:{DARK}; }}
h1,h2,h3,h4 {{ font-family:'Barlow Condensed',sans-serif!important; text-transform:uppercase; letter-spacing:-.6px; }}
h1 {{ font-size:clamp(2.4rem,5vw,4.7rem)!important; line-height:.95!important; }}
h2 {{ font-size:clamp(1.8rem,3vw,3rem)!important; }}
.block-container {{ padding-top:1.25rem; padding-bottom:2.5rem; max-width:1280px; }}
.hero {{ background:linear-gradient(100deg,rgba(9,14,10,.92),rgba(9,14,10,.55)),linear-gradient(135deg,#273d18,#111); color:white; border-radius:24px; padding:clamp(1.8rem,5vw,4rem); min-height:300px; border:1px solid #28352a; position:relative; overflow:hidden; }}
.hero:after {{ content:'2050'; position:absolute; right:-1rem; bottom:-4rem; font:900 clamp(8rem,24vw,21rem)/.8 'Barlow Condensed'; color:rgba(184,243,74,.09); pointer-events:none; }}
.hero-kicker {{ color:{LIME}; font-size:.76rem; font-weight:800; letter-spacing:3px; }}
.hero-title {{ font:900 clamp(3rem,8vw,7.5rem)/.82 'Barlow Condensed'; letter-spacing:-2px; margin:.7rem 0 1rem; }}
.hero-title span {{ color:{LIME}; }} .hero-sub {{ max-width:680px; color:#e8ebe4; font-size:1.05rem; line-height:1.65; }}
.eyebrow {{ color:#5d781f; letter-spacing:2px; font-size:.75rem; font-weight:800; margin-bottom:.25rem; }}
.card {{ background:white; border:1px solid #e3e7dc; border-radius:18px; padding:1.15rem 1.3rem; height:100%; box-shadow:0 5px 18px rgba(17,24,15,.035); }}
.card h3 {{ margin-top:.25rem; }}
.pop-card {{ background:{DARK}; color:white; border-radius:18px; padding:1.2rem; border:1px solid #29342b; height:100%; }}
.pop-card .number {{ font:800 3rem/.9 'Barlow Condensed'; color:{LIME}; }}
.pill {{ display:inline-block; border:1px solid #d6e3bd; color:#49621b; background:#f1f8e6; padding:.25rem .65rem; border-radius:99px; font-size:.72rem; font-weight:800; letter-spacing:1px; }}
.section-banner {{ background:#e8efdc; border:1px solid #d4dfc2; border-radius:16px; padding:1rem 1.25rem; }}
.scenario {{ border-radius:20px; overflow:hidden; border:1px solid #dce2d6; background:white; }}
.scenario-title {{ padding:1rem 1.2rem .5rem; }}
.metric-note,.source-line {{ color:#666b61; font-size:.8rem; }}
div[data-testid="stMetric"] {{ background:white; border:1px solid #e1e5da; padding:12px 14px; border-radius:14px; }}
.stButton button {{ border-radius:999px!important; font-weight:800!important; }}
.stTabs [data-baseweb="tab-list"] {{ gap:7px; }} .stTabs [data-baseweb="tab"] {{ border-radius:999px; padding:7px 14px; }}
[data-testid="stImage"] img {{ border-radius:16px; }}
a {{ color:#47651c!important; font-weight:700; }}
footer {{ visibility:hidden; }}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_database(path_string):
    path = BASE / path_string
    if not path.exists(): raise FileNotFoundError(f"Missing workbook: {path.name}. Keep it beside app.py.")
    data = pd.read_excel(path, sheet_name=0)
    required = ["ID", "Section", "Topic", "Information", "Source", "Link"]
    missing = [c for c in required if c not in data.columns]
    if missing: raise ValueError("Missing columns: " + ", ".join(missing))
    data = data[required].dropna(subset=["Topic", "Information"]).copy()
    for col in required[1:]: data[col] = data[col].fillna("").astype(str).str.strip()
    return data

try: db = load_database(DATABASE_FILE)
except Exception as e:
    st.error(f"Database loading error: {e}"); st.stop()

def record(topic):
    m = db[db.Topic.str.contains(topic, case=False, na=False)]
    return m.iloc[0] if not m.empty else None

def records(section): return db[db.Section.str.lower() == section.lower()]

def content_card(r, source=True):
    if r is None: return
    st.markdown(f'<div class="card"><div class="eyebrow">{r["Section"].upper()}</div><h3>{r["Topic"]}</h3></div>', unsafe_allow_html=True)
    st.write(r["Information"])
    if source:
        st.caption(f'Source: {r["Source"]}')
        if r["Link"].startswith("http"): st.markdown(f'[OPEN SOURCE ↗]({r["Link"]})')

def mini_card(title, body, tag="2050"):
    st.markdown(f'<div class="pop-card"><div class="pill">{tag}</div><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)

nav = st.radio("NAVIGATION", ["HOME", "THE CHALLENGE", "THE FUTURE", "THE CHANGE", "YOUR IMPACT", "ABOUT US"], horizontal=True, label_visibility="collapsed")

# HOME
if nav == "HOME":
    st.markdown(f'''<div class="hero"><div class="hero-kicker">A LOCAL PROJECT · A SHARED FUTURE</div><div class="hero-title">IRAPUATO,<br><span>REIMAGINED.</span></div><p class="hero-sub">What could our city become by 2050? Explore the challenges, compare possible futures, and discover how today's decisions can shape tomorrow.</p><span class="pill">EXPLORE THE CITY'S FUTURE ↓</span></div>''', unsafe_allow_html=True)
    st.write("")
    c1,c2 = st.columns([1.35,1], gap="large")
    with c1:
        st.image(str(SCENARIO_A), width=740)
        st.caption("FUTURE A · A BETTER TOMORROW — an illustrative vision, not a forecast.")
    with c2:
        st.markdown('<div class="section-banner"><div class="eyebrow">THE BIG QUESTION</div><h2>What will Irapuato look like in 2050?</h2></div>', unsafe_allow_html=True)
        st.write(record("Main question")["Information"])
        st.markdown("### Our focus")
        cols=st.columns(3)
        for c,label,emoji in zip(cols,["CLEAN WATER","SUSTAINABLE CITIES","CLIMATE ACTION"],["💧","🏙️","🌎"]):
            with c: st.markdown(f'<div class="pop-card"><div style="font-size:1.8rem">{emoji}</div><b>{label}</b></div>',unsafe_allow_html=True)
    st.markdown("## THE FUTURE IS A CHOICE")
    x,y=st.columns(2)
    with x: mini_card("A BETTER TOMORROW", "Sustainable decisions, protected green spaces, and a city ready to adapt.", "FUTURE A")
    with y: mini_card("A WORLD UNCHANGED", "What if today's environmental challenges continue into the future?", "FUTURE B")
    st.markdown("## WHY THIS PROJECT?")
    c1,c2=st.columns(2)
    with c1: content_card(record("Project goal"))
    with c2: content_card(record("Project concept"))
    st.caption("Independent student project · Not an official municipal government website.")

# THE CHALLENGE
elif nav == "THE CHALLENGE":
    st.markdown('<div class="eyebrow">01 / UNDERSTAND THE PRESENT</div>',unsafe_allow_html=True)
    st.title("OUR CITY. OUR CHALLENGES.")
    st.write("Explore local information about water, urban development, green spaces, waste, and environmental resilience.")
    topics=["All local topics","Water","Green spaces & biodiversity","Urban planning","Air quality & waste","Climate & resilience"]
    filt=st.selectbox("CHOOSE A TOPIC",topics)
    local=records("Local Context")
    patterns={"Water":"water|groundwater|aquifer", "Green spaces & biodiversity":"green|park|protected|vegetation|biodiversity|natural", "Urban planning":"urban|mobility|territorial|participatory", "Air quality & waste":"air|waste|plastic|burning", "Climate & resilience":"climate|resilien|risk"}
    filtered=local if filt==topics[0] else local[local.Topic.str.contains(patterns[filt],case=False,na=False)]
    # compact photo feature, not a giant full-width image
    c1,c2=st.columns([1,1.25],gap="large")
    with c1: st.image(str(SCENARIO_B if filt in ["Air quality & waste","Climate & resilience"] else SCENARIO_A), width=460)
    with c2:
        st.markdown('<div class="section-banner"><div class="eyebrow">LOCAL CONTEXT</div><h2>Evidence, not assumptions.</h2></div>',unsafe_allow_html=True)
        st.write("The following information is drawn from the updated project database. Historical figures are labeled with their year; they are not live measurements.")
        st.markdown('<span class="pill">FILTERED TOPIC: '+filt.upper()+'</span>',unsafe_allow_html=True)
    st.markdown("## EXPLORE THE RESEARCH")
    for start in range(0,len(filtered),2):
        cols=st.columns(2,gap="medium")
        for col,(_,r) in zip(cols,filtered.iloc[start:start+2].iterrows()):
            with col:
                with st.container(border=True): content_card(r)
    st.markdown("## LOCAL DATA VISUALS")
    st.caption("Charts show historical information included in the project research, not current/live data.")
    tabs=st.tabs(["WATER ACCESS","GROUNDWATER","WELLS","VEGETATION"])
    with tabs[0]:
        d=pd.DataFrame({"Area":["Municipality","Rural areas"],"Water service coverage (%)":[98.61,94.94]})
        fig=px.bar(d,x="Area",y="Water service coverage (%)",text="Water service coverage (%)",range_y=[0,105],title="Water-service coverage · Census 2020")
        fig.update_traces(texttemplate="%{text:.2f}%",textposition="outside")
        fig.update_layout(template="plotly_white",margin=dict(l=10,r=10,t=50,b=15),showlegend=False)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":True})
        r=record("Water service coverage"); st.caption(f'Source: {r["Source"]} · 2020 data')
    with tabs[1]:
        d=pd.DataFrame({"Measure":["Extraction reported","Concession volume"],"Volume (million m³/year)":[37,58.3]})
        fig=px.bar(d,x="Measure",y="Volume (million m³/year)",text="Volume (million m³/year)",title="Groundwater volumes reported for 2020")
        fig.update_traces(texttemplate="%{text:.1f} million m³",textposition="outside")
        fig.update_layout(template="plotly_white",margin=dict(l=10,r=10,t=50,b=15),showlegend=False)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":True})
        r=record("Water extraction data"); st.caption(f'Source: {r["Source"]} · historical figures')
    with tabs[2]:
        d=pd.DataFrame({"Well status":["Working","Reserve","Not working"],"Count":[81,10,11]})
        fig=px.pie(d,names="Well status",values="Count",hole=.56,title="Well status cited in municipal planning")
        fig.update_traces(textinfo="label+percent")
        fig.update_layout(template="plotly_white",margin=dict(l=10,r=10,t=50,b=15))
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":True})
        r=record("Water extraction data"); st.caption(f'Source: {r["Source"]}')
    with tabs[3]:
        d=pd.DataFrame({"Period":["2000–2018"],"Reported vegetation change (%)":[-15]})
        fig=px.bar(d,x="Period",y="Reported vegetation change (%)",text="Reported vegetation change (%)",title="Reported vegetation loss · 2000–2018")
        fig.update_traces(texttemplate="%{text:.0f}%",textposition="outside")
        fig.update_layout(template="plotly_white",margin=dict(l=10,r=10,t=50,b=15),showlegend=False)
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":True})
        r=record("Vegetation loss"); st.caption(f'Source: {r["Source"]} · historical period')
    st.info("Some statistics refer to past years. Always read the source and date before interpreting them.")

# FUTURE
elif nav == "THE FUTURE":
    st.markdown('<div class="eyebrow">02 / EXPLORE POSSIBLE TOMORROWS</div>',unsafe_allow_html=True)
    st.title("2050 FUTURE EXPLORER")
    st.write("Two visions of Irapuato. Switch between them and compare what different decisions could mean.")
    st.warning("Illustrative scenarios only — these are not official predictions, scientific forecasts, or real future statistics.")
    # Two compact scenario image cards at the top: the provided images are used as-is.
    a,b=st.columns(2,gap="large")
    with a:
        st.markdown('<div class="scenario"><div class="scenario-title"><span class="pill">FUTURE A</span><h2>A BETTER TOMORROW</h2></div></div>',unsafe_allow_html=True)
        st.image(str(SCENARIO_A),width=600)
        st.write(record("Scenario A — Irapuato with sustainable decisions")["Information"])
    with b:
        st.markdown('<div class="scenario"><div class="scenario-title"><span class="pill">FUTURE B</span><h2>A WORLD UNCHANGED</h2></div></div>',unsafe_allow_html=True)
        st.image(str(SCENARIO_B),width=600)
        st.write(record("Scenario B — Challenges continue")["Information"])
    st.markdown("## SWITCH THE SCENARIO")
    choice=st.segmented_control("Choose scenario",["FUTURE A · SUSTAINABLE DECISIONS","FUTURE B · CHALLENGES CONTINUE"],default="FUTURE A · SUSTAINABLE DECISIONS")
    if choice.startswith("FUTURE A"):
        selected_img=SCENARIO_A; selected_record=record("Scenario A — Irapuato with sustainable decisions"); indicators=[record("Scenario A — Indicator: Water stewardship"),record("Scenario A — Indicator: Green and public spaces"),record("Scenario A — Indicator: Climate and environmental resilience")]
        st.markdown('<div class="section-banner"><h2>FUTURE A / A BETTER TOMORROW</h2><p>What if we act today?</p></div>',unsafe_allow_html=True)
    else:
        selected_img=SCENARIO_B; selected_record=record("Scenario B — Challenges continue"); indicators=[record("Scenario B — Indicator: Water pressure"),record("Scenario B — Indicator: Green-space pressure"),record("Scenario B — Indicator: Environmental resilience")]
        st.markdown('<div class="section-banner"><h2>FUTURE B / A WORLD UNCHANGED</h2><p>What if we do not act enough?</p></div>',unsafe_allow_html=True)
    left,right=st.columns([1,1.2],gap="large")
    with left: st.image(str(selected_img),width=520)
    with right:
        st.markdown("### SCENARIO DETAILS")
        content_card(selected_record,source=True)
        st.markdown("### THREE INDICATORS")
        for item in indicators:
            with st.expander(item["Topic"]): st.write(item["Information"])
    st.markdown("## COMPARE THE TWO PATHWAYS")
    c1,c2=st.columns(2)
    with c1:
        st.markdown('<div class="pop-card"><span class="pill">FUTURE A</span><h3>Decisions create change</h3></div>',unsafe_allow_html=True)
        for topic in ["Scenario A — Indicator: Water stewardship","Scenario A — Indicator: Green and public spaces","Scenario A — Indicator: Climate and environmental resilience"]:
            with st.expander(topic): st.write(record(topic)["Information"])
    with c2:
        st.markdown('<div class="pop-card"><span class="pill">FUTURE B</span><h3>Challenges continue</h3></div>',unsafe_allow_html=True)
        for topic in ["Scenario B — Indicator: Water pressure","Scenario B — Indicator: Green-space pressure","Scenario B — Indicator: Environmental resilience"]:
            with st.expander(topic): st.write(record(topic)["Information"])
    st.caption(record("Scenario disclaimer")["Information"])

# THE CHANGE
elif nav == "THE CHANGE":
    st.markdown('<div class="eyebrow">03 / TURN IDEAS INTO ACTION</div>',unsafe_allow_html=True)
    st.title("THE FUTURE DOESN'T CHANGE BY ITSELF.")
    st.write("Ideas, habits, community initiatives, and public decisions can all help shape a more sustainable city.")
    categories=["Water","Green spaces","Waste","Air","Mobility","Community"]
    icons=["💧","🌳","♻️","🌬️","🚲","🤝"]
    action_rows=records("Take Action")
    cols=st.columns(3,gap="medium")
    for i,(_,r) in enumerate(action_rows.iterrows()):
        with cols[i%3]:
            with st.container(border=True):
                st.markdown(f'<div style="font-size:1.8rem">{icons[i%len(icons)]}</div><div class="eyebrow">ACTION {i+1:02}</div><h3>{r["Topic"]}</h3>',unsafe_allow_html=True)
                st.write(r["Information"])
                st.caption(r["Source"])
                if r["Link"].startswith("http"): st.markdown(f'[LEARN MORE ↗]({r["Link"]})')

# IMPACT
elif nav == "YOUR IMPACT":
    st.markdown('<div class="eyebrow">04 / YOUR CHOICE MATTERS</div>',unsafe_allow_html=True)
    st.title("WHAT FUTURE WILL YOU HELP CREATE?")
    st.write("Choose up to three commitments. This is a reflection activity, not a measurement of your environmental impact.")
    options=["I will learn more about water in my community.","I will reduce unnecessary waste.","I will help care for shared green spaces.","I will share reliable information about a local issue.","I will learn how to participate in my community."]
    chosen=st.multiselect("MY COMMITMENTS",options,max_selections=3)
    if chosen:
        st.markdown('<div class="section-banner"><div class="eyebrow">MY 2050 ACTION CARD</div><h2>Small steps. Shared future.</h2></div>',unsafe_allow_html=True)
        for item in chosen: st.markdown(f'<div class="card">✓ &nbsp;{item}</div>',unsafe_allow_html=True)
        st.caption("Small actions help. Structural challenges also require planning, public services, investment, and collective responsibility.")
    else: st.info("Choose one or more actions to create your personal action list.")
    st.markdown("## EVERYONE HAS A ROLE")
    content_card(record("Change requires collaboration"))

# ABOUT
elif nav == "ABOUT US":
    st.markdown('<div class="eyebrow">05 / THE PEOPLE BEHIND THE PROJECT</div>',unsafe_allow_html=True)
    st.title("MADE FOR OUR CITY.")
    c1,c2=st.columns([1,1.15],gap="large")
    with c1: st.image(str(SCENARIO_A),width=500)
    with c2:
        content_card(record("About the project"))
        st.markdown("### OUR STORY")
        st.write("We chose Irapuato because the future of a city begins with understanding the place we call home. Through research, data, and interactive storytelling, we want to make local sustainability challenges easier to explore and discuss.")
    st.markdown("## MEET THE TEAM")
    content_card(record("Project team"))
    st.markdown("## OUR VIDEO")
    st.video(YOUTUBE_VIDEO_URL)  # unchanged as requested
    st.markdown("[OPEN VIDEO ON YOUTUBE ↗](https://youtu.be/e0cehcrWnb8)")
    st.markdown("## SOURCES & TRANSPARENCY")
    for _,r in db[["Source","Link"]].drop_duplicates().iterrows():
        if r["Link"].startswith("http"): st.markdown(f'- [{r["Source"]}]({r["Link"]})')
    for topic in ["Scenario disclaimer","Local data disclaimer","Source and attribution policy"]:
        with st.expander(topic): st.write(record(topic)["Information"])

st.markdown("---")
st.markdown(f'<div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:#697066;font-size:.8rem"><span><b>IRAPUATO, REIMAGINED.</b> · THE FUTURE IS OURS.</span><span>Student project · Source-attributed information</span></div>',unsafe_allow_html=True)
