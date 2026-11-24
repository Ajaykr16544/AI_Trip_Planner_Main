# AI Trip Planner

An AI-powered trip-planning app with a Streamlit chat interface and a FastAPI backend.

## How the application is connected

1. `streamlit_app.py` displays the chat UI and sends the question to the backend at `http://localhost:8000/query`.
2. `main.py` exposes the FastAPI `/query` endpoint.
3. `agent/agentic_workflow.py` builds the LangGraph agent, using the model and tools.
4. `utils/model_loader.py` reads the model settings from `config/config.yaml` and loads the selected provider.
5. The agent uses `prompt_library/` and the tools in `tools/` and `utils/` to prepare a travel plan.

The backend and frontend must both be running. A Groq API key is required to generate plans. Other API keys enable their respective live data tools.

## API keys

Create or update a `.env` file in the project root. Set at least `GROQ_API_KEY` to a valid Groq API key. Add any other keys you have for the optional weather, places/search, or currency tools. Keep `.env` private; do not commit API keys.

```dotenv
GROQ_API_KEY=your_groq_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
GPLACES_API_KEY=your_google_places_api_key
TAVILY_API_KEY=your_tavily_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
```

Only `GROQ_API_KEY` is needed for the configured language model; the other keys enable their corresponding live-data tools.

## Run on Windows

Run the setup commands once from the project root in PowerShell. Then start the backend and frontend in two separate PowerShell terminals, both opened in the project root.

### Install dependencies

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, allow it for the current terminal with `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate the environment again.

### Terminal 1: start the backend

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Check the backend at <http://127.0.0.1:8000/docs>.

### Terminal 2: start the frontend

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

Open the Streamlit URL printed in the terminal (normally <http://localhost:8501>) and submit a trip-planning question.


 & d:/AI_Trip_Planner-main/AI_Trip_Planner-main/env/Scripts/Activate.ps1
 python -m pip install uvicorn      
>> python -m uvicorn main:app --reload"# AI_Trip_Planner_Main" 
