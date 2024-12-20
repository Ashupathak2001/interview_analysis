import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from datetime import datetime
import os
import cohere
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Utility Imports (Assumed to be in separate files)
from utils.video_audio import record_audio_video, analyze_facial_expressions
from utils.analysis import analyze_response, generate_score
from utils.feedback import provide_feedback
from utils.data_handling import load_questions, save_progress, get_feedback_summary

def initialize_cohere_client():
    """Initialize Cohere client with API key."""
    try:
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            st.warning("Cohere API key not found.")
            return None
        return cohere.Client(cohere_api_key)
    except Exception as e:
        st.error(f"Cohere initialization error: {e}")
        return None

def check_answer_quality_with_cohere(question, response):
    """Evaluate answer quality using Cohere."""
    co = initialize_cohere_client()
    if not co:
        return {"error": "Cohere client not initialized"}
    
    try:
        evaluation_prompt = f"""Evaluate this interview answer:

Question: {question}
Answer: {response}

Assess:
1. Relevance to question
2. Clarity 
3. Depth
4. Example usage
5. Professional communication

Provide score (0-100) and brief feedback."""

        response = co.generate(
            prompt=evaluation_prompt,
            model='command-xlarge-nightly',
            max_tokens=300,
            temperature=0.3
        )
        
        # Extract Cohere's analysis
        cohere_analysis = response.generations[0].text.strip()
        
        # Basic score extraction
        import re
        score_match = re.search(r'Score:\s*(\d+)', cohere_analysis)
        score = int(score_match.group(1)) if score_match else 0
        
        return {
            "score": score,
            "detailed_feedback": cohere_analysis
        }
    except Exception as e:
        st.error(f"Cohere API error: {e}")
        return {"error": str(e)}

def generate_improved_answer_with_cohere(question, original_response):
    """Generate improved answer using Cohere."""
    co = initialize_cohere_client()
    if not co:
        return "Unable to generate improved answer."
    
    try:
        improvement_prompt = f"""Improve this interview answer:

Question: {question}
Original Answer: {original_response}

Create a more professional version that:
- Directly addresses the question
- Uses clear language
- Provides specific examples
- Shows professional communication"""

        response = co.generate(
            prompt=improvement_prompt,
            model='command-xlarge-nightly',
            max_tokens=300,
            temperature=0.7
        )
        
        return response.generations[0].text.strip()
    except Exception as e:
        st.error(f"Cohere API error: {e}")
        return f"Error generating improved answer: {e}"

def create_progress_visualization(summary):
    """Create interactive progress visualizations."""
    st.subheader("Performance Visualization")
    
    if summary:
        topics = list(summary.keys())
        scores = [summary[topic]['average_score'] for topic in topics]
        
        df = pd.DataFrame({
            'Topics': topics,
            'Scores': scores
        })
        
        # Bar Chart
        fig1 = px.bar(
            df, 
            x='Topics', 
            y='Scores', 
            title="Average Performance by Topic",
            labels={'Scores': 'Average Score'},
            color='Scores',
            color_continuous_scale="Viridis"
        )
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='lightgray')
        )
        st.plotly_chart(fig1)
        
        # Radar Chart 
        fig2 = go.Figure(data=go.Scatterpolar(
            r=scores,
            theta=topics,
            fill='toself'
        ))
        fig2.update_layout(
            title="Multidimensional Performance Radar",
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        )
        st.plotly_chart(fig2)

def main():
    # Page Configuration
    st.set_page_config(
        page_title="InterviewPro: AI Response Analyzer",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="auto"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    :root {
        --primary-color: #FF4B4B;
        --secondary-color: #4A4A4A;
        --background-color: #F4F4F4;
    }
    .stButton>button {
        background-color: var(--primary-color) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown(
        "<h1 style='text-align: center; color: var(--primary-color);'>🚀 InterviewPro: AI Response Analyzer</h1>", 
        unsafe_allow_html=True
    )
    
    # Tabbed Navigation
    tab1, tab2, tab3 = st.tabs(["Interview Practice", "Progress Tracker", "Settings"])
    
    with tab1:
        st.header("Mock Interview Session")
        
        # Question Selection
        questions = load_questions()
        col1, col2 = st.columns(2)
        
        with col1:
            selected_topic = st.selectbox("Select a topic:", list(questions.keys()))
        with col2:
            question = st.selectbox("Select a question:", questions[selected_topic])
        
        # Interview Start Button
        if st.button("Start Mock Interview", type="primary"):
            st.info("Answer the question within 60 seconds:")
            st.markdown(f"**Question**: {question}")
            
            # Recording and Analysis
            with st.spinner('Recording and analyzing...'):
                frames, transcription = record_audio_video(duration=60)
                
                if frames is None or transcription is None:
                    st.error("Recording failed. Please check your camera and microphone.")
                else:
                    # Original Analysis
                    emotion_data = analyze_facial_expressions(frames)
                    sentiment, key_phrases, quality = analyze_response(transcription)
                    score = generate_score(sentiment, emotion_data, transcription)
                    feedback = provide_feedback(sentiment, emotion_data, quality)
                    
                    # Cohere Quality Check
                    cohere_quality = check_answer_quality_with_cohere(question, transcription)
                    
                    # Results Display
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Transcription")
                        st.write(transcription)
                        
                        # st.subheader("Emotion Analysis")
                        # for emotion, intensity in emotion_data.items():
                        #     st.progress(min(1.0, max(0.0, intensity)), text=f"{emotion}: {intensity:.2%}")
                        
                        st.subheader("Performance Metrics")
                        st.metric("Overall Score", f"{score:.2f}/100")
                        st.metric("Sentiment", sentiment)
                    
                    with col2:
                        
                        st.subheader("Cohere AI Assessment")
                        if 'score' in cohere_quality:
                            st.metric("Cohere Score", f"{cohere_quality.get('score', 0)}/100")
                        
                        st.write(f"**Key Phrases**: {', '.join(key_phrases)}")
                        st.write(f"**Quality**: {quality}")
                    
                    # Feedback and Improvement Sections
                    st.subheader("Personalized Feedback")
                    st.info(feedback)
                    
                    # Cohere Detailed Feedback
                    if 'detailed_feedback' in cohere_quality:
                        st.subheader("Cohere Detailed Feedback")
                        st.write(cohere_quality['detailed_feedback'])
                    
                    # Save Progress
                    save_progress(selected_topic, question, score, feedback)
                    st.success("Progress saved successfully!")
    
    with tab2:
        st.header("Your Progress and Feedback Summary")
        
        summary = get_feedback_summary()
        
        if summary:
            create_progress_visualization(summary)
            
            # Progress Table
            progress_df = pd.read_csv('progress.csv')
            st.dataframe(
                progress_df.style.highlight_max(subset=['score'], color='lightgreen')
            )
        else:
            st.write("No progress data available yet.")
    
    with tab3:
        st.header("Application Settings")
        
        # Theme Toggle
        st.subheader("UI Theme")
        theme = st.toggle("Dark Mode")
        
        # Data Management
        st.subheader("Data Management")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Reset Progress Data", type="secondary"):
                if os.path.exists('progress.csv'):
                    os.remove('progress.csv')
                st.success("Progress data reset successfully!")
        
        with col2:
            st.subheader("Provide Feedback")
            feedback = st.text_area("Share your thoughts")
            if st.button("Submit Feedback"):
                st.success("Thank you for your feedback!")

if __name__ == "__main__":
    main()
