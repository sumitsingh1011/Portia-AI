AI Auditor
│
├── agent/                   # Entry point scripts and orchestration configs
│   ├── auditor.yaml         # Portia orchestration configuration
│   └── run.py               # Script to launch full audit pipeline
│
├── app/                     # High-level orchestration and agent wrappers
│   ├── auditor.py           # Core auditing logic integrated with Portia
│   └── auditor_agent.py     # Agent interface for auditing workflows
│
├── audit_service/           # Core microservice implementing audit checks
│   ├── adapters/            # Gemini and Portia adapter integrations
│   ├── audit_checks/        # Modules for PII, toxicity, hallucination checks
│   ├── core.py              # Orchestration glue code for audit pipeline
│   ├── models/              # Trained ML models for toxicity and bias detection
│   ├── routers/             # FastAPI endpoints for audit requests
│   └── services/            # Client libraries and supporting services
│
├── dashboard/               # Streamlit-based interactive dashboard for demos
│   └── app.py               # Dashboard UI implementation
│
├── harmful-classifier/      # ML model training and dataset preprocessing
│
├── integrations/            # Integrations like Slack notifications, Notion logging
│
├── requirements.txt         # Python dependencies
├── README.md                # This documentation file
└── pyproject.toml           # Project metadata and build configuration


   Quick Start

Clone the repo

git clone https://github.com/your-username/your-repo.git
cd your-repo


Set up virtual environment

python -m venv venv
venv\Scripts\activate  # On Windows


Install dependencies

pip install -r requirements.txt


Add environment variables
Create a .env file in root with your API keys:

GEMINI_API_KEY=your_gemini_api_key


Run auditor CLI

python agent/run.py --config agent/auditor.yaml


Launch dashboard

streamlit run dashboard/app.py 
