IRAPUATO, REIMAGINED — Streamlit website

FILES
- app.py: the website code
- IRAPUATO_REIMAGINED_Database.xlsx: the database
- requirements.txt: Python libraries to install

IMPORTANT
The code reads ONLY the first worksheet ("Data") from the Excel database.
Keep app.py and the Excel file in the same folder.

SET UP IN VS CODE
1. Install Python 3.10 or newer.
2. Open this folder in Visual Studio Code.
3. Open the VS Code terminal.
4. Run: python -m venv .venv
5. Activate the environment:
   Windows PowerShell: .venv\Scripts\Activate.ps1
   macOS/Linux: source .venv/bin/activate
6. Run: pip install -r requirements.txt
7. Open app.py and replace YOUTUBE_VIDEO_URL with your actual YouTube URL.
8. Run: streamlit run app.py

The app will open in your browser, usually at http://localhost:8501.

ABOUT THE INTERACTIVE FUTURE EXPLORER
The sliders let visitors choose priorities for water, green/public spaces, and climate resilience.
The app then changes the narrative to help them explore the selected pathway. This is deliberately
qualitative: it is NOT a scientific model, official forecast, or calculated prediction.

CHARTS
The charts use the historical figures stored in the Data worksheet:
- Water-service coverage: municipality and rural areas (Census 2020)
- Water concession and extraction volumes (2020 figures cited in municipal planning)
- Well status (municipal planning document)
- Reported vegetation-area change (2000–2018)

These figures are not live data. The website displays their original dates and source notes.
