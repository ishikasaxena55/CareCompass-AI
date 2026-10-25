# 🩺 CareCompass AI

### AI-Powered Healthcare Navigation Assistant

CareCompass AI is a healthcare navigation project designed to help users explore healthcare resources and receive guidance through an easy-to-use web interface. The project combines a web-based frontend with a Python backend to support healthcare navigation functionality.

## ✨ Features

- 🏥 **Healthcare Navigation:** Helps users navigate healthcare-related resources.
- 🤖 **AI-Assisted Guidance:** Designed to support healthcare navigation through backend functionality.
- 🌐 **Web-Based Interface:** Simple interface built with HTML, CSS, and JavaScript.
- ⚙️ **Python Backend:** Uses Python and FastAPI for API functionality.
- 📊 **Dataset Integration:** Includes a healthcare triage dataset for project development.
- 👩‍⚕️ **Caregiver Resources:** Includes a caregiver data file to support the project's resource-related functionality.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| HTML5 | Webpage structure |
| CSS3 | Styling and layout |
| JavaScript | Frontend functionality |
| Python | Backend logic |
| FastAPI | API framework |
| Uvicorn | ASGI server |
| JSONL | Dataset storage |
| CSV | Caregiver data storage |

## 📁 Project Structure

```text
CareCompass-AI/
│
├── index.html
├── style.css
├── script.js
├── main.py
├── requirements.txt
├── triage_dataset.jsonl
├── caregivers.csv
├── carecompass.db
└── README.md
```

*Note: The dataset, database, and caregiver files should only be included in the repository if they contain no sensitive or personally identifiable information.*

## 🚀 Getting Started

### Prerequisites

Install the following before running the project locally:

- Python 3.10 or a compatible version
- Git
- A modern web browser

### 1. Clone the Repository

```bash
git clone https://github.com/ishikasaxena55/CareCompass-AI.git
```

### 2. Open the Project Directory

```bash
cd CareCompass-AI
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Backend

```bash
uvicorn main:app --reload
```

The backend should be available at:

```text
http://127.0.0.1:8000
```

If the FastAPI application is configured to expose interactive API documentation, you can visit:

```text
http://127.0.0.1:8000/docs
```

### 5. Open the Frontend

Open `index.html` in your browser to view the website.

**Important:** The frontend API URL must point to the running backend. For local development, the API endpoint may be configured as:

```javascript
const API_URL = "http://127.0.0.1:8000/navigate";
```

For an online deployment, replace this with the deployed backend's URL.

## ☁️ Deployment

The frontend and backend may require separate deployment configurations.

- **Frontend:** Can be deployed as a static website using Vercel.
- **Backend:** Requires a hosting setup that supports the project's FastAPI application.

After deployment, configure the frontend API URL to point to the publicly accessible backend.

## 🔒 Privacy and Security

- Do not commit passwords, API keys, access tokens, or private credentials.
- Do not upload real patient records or sensitive medical information.
- Review database and dataset files before making the repository public.
- Configure appropriate security controls before collecting or processing user data.

## ⚠️ Medical Disclaimer

CareCompass AI is an educational and developmental project. It is not a substitute for professional medical advice, diagnosis, or treatment.

Do not use this project as the sole basis for medical decisions or emergency triage. Always consult qualified healthcare professionals for medical concerns. In an emergency, contact your local emergency services.

## 🎯 Project Goal

The goal of CareCompass AI is to explore how web technologies and AI-assisted functionality can make healthcare navigation more accessible and user-friendly.

## 👩‍💻 Author

**Ishika Saxena**

GitHub: [@ishikasaxena55](https://github.com/ishikasaxena55)

## 📄 License

No license has been specified yet. Add an appropriate open-source license before permitting others to reuse, modify, or distribute this project.
