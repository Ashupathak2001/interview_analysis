# InterviewPro: AI Response Analyzer

InterviewPro is an AI-powered application designed to simulate mock interviews, analyze responses, and provide personalized feedback. The application leverages advanced AI models to help users refine their answers and track progress over time.

---

## Features
- **Mock Interview Sessions:**
  - Choose topics and answer pre-defined questions.
  - Record audio and video for real-time analysis.
- **AI-Driven Feedback:**
  - Assess relevance, clarity, depth, and communication.
  - Generate detailed feedback and improved answers using Cohere's API.
- **Performance Metrics:**
  - Sentiment analysis and facial expression evaluation.
  - Overall scores and key phrase extraction.
- **Progress Tracking:**
  - Interactive bar and radar charts for visualizing progress.
  - Data export and summary views.
- **Customizable Settings:**
  - Reset progress and toggle dark mode.

---

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Install requirements
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

3. Run the application:
```bash
streamlit run app.py
```

### Prerequisites
- Python 3.8+
- Environment variable `COHERE_API_KEY` (from Cohere)
- FFmpeg (for audio-video processing)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd InterviewPro
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Cohere API key:
   ```env
   COHERE_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. **Start the Application:** Open the app in your browser via Streamlit's local URL.
2. **Mock Interviews:** Navigate to the "Interview Practice" tab to select topics and answer questions.
3. **Analyze Responses:** Receive immediate feedback and scores after each session.
4. **Track Progress:** Use the "Progress Tracker" tab to visualize performance.
5. **Settings:** Reset data or submit feedback using the "Settings" tab.

---

## Contributing
1. Fork the repository.
2. Create a new feature branch.
3. Submit a pull request with detailed changes.

---

## License
This project is open-sourced under the MIT License. See the `LICENSE` file for more information.

---

## Acknowledgments
- Cohere API for text generation and analysis.
- Plotly for creating dynamic visualizations.
- Streamlit for building the interactive user interface.



