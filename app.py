"""FellaRide Community Manager Dashboard."""

from pathlib import Path
import tempfile

import networkx as nx
import pandas as pd
from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components

from ai_engine import categorize_persona, generate_outreach
from mock_data import generate_mock_posts

st.set_page_config(page_title="FellaRide Community Manager", page_icon="🚗", layout="wide")


@st.cache_data(show_spinner=False)
def load_posts() -> pd.DataFrame:
    return generate_mock_posts()


@st.cache_data(show_spinner=False)
def enrich_posts(posts: pd.DataFrame) -> pd.DataFrame:
    enriched = posts.copy()
    classified = enriched["Post_Text"].apply(categorize_persona)
    enriched[["AI Persona", "AI Reasoning"]] = pd.DataFrame(classified.tolist(), index=enriched.index)
    return enriched


def build_network(posts: pd.DataFrame) -> str:
    graph = nx.Graph()
    for row in posts.itertuples(index=False):
        username = row.Username
        location = row.Stated_Location
        graph.add_node(username, label=username.replace("u/", ""), group="User", title=f"{row.Upvotes} upvotes")
        graph.add_node(location, label=location, group="Location", title="Shared location")
        graph.add_edge(username, location, title="Lives / commutes here")
        if "friday hackathon" in row.Post_Text.lower():
            event = "Friday Hackathon"
            graph.add_node(event, label=event, group="Event", title="Shared event")
            graph.add_edge(username, event, title="Mentioned event")

    network = Network(height="510px", width="100%", bgcolor="#0E172A", font_color="#F8FAFC", notebook=False, cdn_resources="in_line")
    network.from_nx(graph)
    network.set_options('''
    {"groups": {"User": {"color": "#60A5FA", "shape": "dot"}, "Location": {"color": "#34D399", "shape": "box"}, "Event": {"color": "#FBBF24", "shape": "diamond"}},
      "physics": {"barnesHut": {"gravitationalConstant": -12000, "springLength": 145}, "minVelocity": 0.75}}
    ''')
    html_path = Path(tempfile.gettempdir()) / "fellaride_network.html"
    network.save_graph(str(html_path))
    return html_path.read_text(encoding="utf-8")


st.title("🚗 FellaRide Community Manager Dashboard")
st.caption("Discover early carpool adopters in micro-communities through public digital signals.")

with st.sidebar:
    st.header("Community scope")
    community = st.selectbox("Target community", ["MIT", "S-VYASA", "RVCE"])
    st.success(f"Monitoring: {community}")
    st.caption("Demo data is anonymized and synthetic.")

posts = load_posts()
with st.spinner("Mapping community signals..."):
    enriched_posts = enrich_posts(posts)

drivers = (enriched_posts["AI Persona"] == "Potential Driver").sum()
passengers = (enriched_posts["AI Persona"] == "Potential Passenger").sum()
connectors = (enriched_posts["AI Persona"] == "Connector").sum()
col1, col2, col3 = st.columns(3)
col1.metric("Potential drivers", drivers)
col2.metric("Potential passengers", passengers)
col3.metric("Community connectors", connectors)

st.header("1. Community mobility network")
st.caption("Blue = users · Green = locations · Gold = shared event")
components.html(build_network(enriched_posts), height=530, scrolling=False)

st.header("2. AI-classified community signals")
st.dataframe(
    enriched_posts[["Username", "Post_Text", "Upvotes", "Stated_Location", "AI Persona", "AI Reasoning"]],
    use_container_width=True,
    hide_index=True,
    column_config={"Post_Text": st.column_config.TextColumn(width="large"), "AI Reasoning": st.column_config.TextColumn(width="large")},
)

st.header("3. Intervention generator")
event = st.selectbox("Upcoming event", ["Friday Hackathon", "Fall Career Fair", "Campus Concert"])
if st.button("Generate Outreach", type="primary"):
    connector_rows = enriched_posts[enriched_posts["AI Persona"] == "Connector"]
    connector_names = connector_rows["Username"].tolist()
    locations = connector_rows["Stated_Location"].unique().tolist()
    with st.spinner("Drafting a contextual message..."):
        message = generate_outreach(event, connector_names, locations)
    st.success("Outreach draft ready")
    st.text_area("Message for community connectors", value=message, height=140)
