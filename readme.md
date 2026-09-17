# FellaRide Community Manager Dashboard

  A Streamlit hackathon prototype for FellaRide, a carpooling startup focused on solving the cold-start problem through
  community digital signals.

  The dashboard analyzes university-community posts to identify:

  - Potential Drivers
  - Potential Passengers
  - Community Connectors
  - Neutral users

  It visualizes shared locations and events in an interactive network graph, displays AI-classified community signals,
  and generates contextual outreach messages to help organizers coordinate carpooling for events like the Friday
  Hackathon.

  ## Features

  - Interactive community selector: MIT, S-VYASA, and RVCE
  - Mock social-signal dataset with Bengaluru locations
  - AI-powered persona classification using the OpenAI API
  - Network graph connecting users, locations, and shared events
  - Connector-focused outreach message generator
  - Offline fallback logic when no OpenAI API key is configured

  ## Tech Stack

  - Streamlit
  - Pandas
  - NetworkX
  - PyVis
  - OpenAI API
  - python-dotenv

  ## Run Locally

  ```bash
  pip install -r requirements.txt
  python3 -m streamlit run app.py

  Then open http://127.0.0.1:8501.

  ## API Key Setup

  Create a .env file:

  OPENAI_API_KEY=your_openai_api_key_here

  Without an API key, the app still works using local fallback classifications and outreach drafts.

