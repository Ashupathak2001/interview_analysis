import cv2
import numpy as np
import streamlit as st
import threading
import queue
import pyaudio
import wave
import time
import os
import sys
import speech_recognition as sr

class VideoRecorder:
    def __init__(self):
        # Additional error handling for face detection model
        try:
            # Check if OpenCV cascade file exists
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            if not os.path.exists(cascade_path):
                st.error(f"Cascade file not found: {cascade_path}")
                self.face_cascade = None
            else:
                self.face_cascade = cv2.CascadeClassifier(cascade_path)
        except Exception as e:
            st.error(f"Error loading face cascade: {e}")
            self.face_cascade = None

        self.video_capture = None
        self.is_recording = False
        self.frames = []

    def initialize_capture(self):
        """
        Safely initialize video capture with multiple backend attempts
        """
        # List of potential camera backends
        backends = [
            # cv2.CAP_DSHOW,  # DirectShow (Windows)
            # cv2.CAP_MSMF,   # Microsoft Media Foundation
            cv2.CAP_V4L2,   # Video4Linux2 (Linux)
            cv2.CAP_ANY     # Any available backend
        ]

        for backend in backends:
            try:
                # Try each backend
                self.video_capture = cv2.VideoCapture(0, backend)
                
                # Verify capture is opened
                if not self.video_capture.isOpened():
                    st.warning(f"Failed to open camera with backend {backend}")
                    continue

                # Set capture properties
                self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
                self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
                
                return True
            except Exception as e:
                st.error(f"Error initializing capture with backend {backend}: {e}")
        
        st.error("Could not initialize video capture. Check camera connections.")
        return False

    def start_recording(self):
        """Start video capture with robust initialization"""
        # Ensure previous capture is released
        if self.video_capture:
            self.video_capture.release()

        # Initialize capture
        if not self.initialize_capture():
            return False

        self.is_recording = True
        self.frames = []
        return True

    def stop_recording(self):
        """Stop video capture safely"""
        if self.video_capture:
            self.video_capture.release()
        self.is_recording = False
        return self.frames

    def detect_and_draw_faces(self, frame):
        """Detect and draw faces on the frame with error handling"""
        if self.face_cascade is None:
            return frame, False

        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Equalize histogram to improve detection
            gray = cv2.equalizeHist(gray)
            
            # Detect faces with more lenient parameters
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.3,  # Increased from 1.1
                minNeighbors=3,   # Reduced from 5
                minSize=(30, 30)
            )
            
            # Draw rectangles around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            return frame, len(faces) > 0
        
        except Exception as e:
            st.error(f"Face detection error: {e}")
            return frame, False

def record_audio_video(duration=60):
    """
    Record audio and video with comprehensive error handling
    
    Args:
        duration (int): Recording duration in seconds
    
    Returns:
        tuple: (video_frames, transcription)
    """
    # Prevent potential memory leaks by clearing any existing cv2 windows
    cv2.destroyAllWindows()

    # Video Recording Setup
    video_recorder = VideoRecorder()
    
    # Attempt to start recording
    if not video_recorder.start_recording():
        st.error("Failed to start video recording. Check camera permissions and connections.")
        return None, None
    
    # Audio Recording Setup
    audio_recorder = sr.Recognizer()
    audio_source = sr.Microphone()
    audio_queue = queue.Queue()

    def record_audio_thread():
        """Thread for recording audio"""
        try:
            with audio_source as source:
                audio_recorder.adjust_for_ambient_noise(source)
                audio_data = audio_recorder.listen(source, timeout=duration)
                audio_queue.put(audio_data)
        except Exception as e:
            st.error(f"Audio recording error: {e}")
            audio_queue.put(None)


    # Streamlit video display
    video_display = st.empty()
    start_time = time.time()
    frames_captured = 0

    # Start audio recording in a separate thread
    audio_thread = threading.Thread(target=record_audio_thread)
    audio_thread.start()
    
    try:
        while time.time() - start_time < duration:
            # Capture frame
            ret, frame = video_recorder.video_capture.read()
            
            if not ret:
                st.warning("Frame capture failed. Retrying...")
                time.sleep(0.1)
                continue
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect and draw faces
            frame_with_faces, faces_detected = video_recorder.detect_and_draw_faces(frame)
            
            # Convert frame to RGB for Streamlit
            frame_rgb = cv2.cvtColor(frame_with_faces, cv2.COLOR_BGR2RGB)
            
            # Display frame
            video_display.image(frame_rgb, channels="RGB")
            
            # Store frame
            video_recorder.frames.append(frame)
            frames_captured += 1
            
            # Optional: Break if no frames captured
            if frames_captured > duration * 10:  # Assuming ~10 fps
                break
        
        # Stop recording
        final_frames = video_recorder.stop_recording()
        
        # Basic transcription placeholder
        transcription = ""
        audio_thread.join()
        recorded_audio = audio_queue.get()

        st.success(f"Recording complete. Captured {frames_captured} frames.")
        if recorded_audio:
            try:
                transcription = audio_recorder.recognize_google(recorded_audio)
                st.success(f"Transcription: {transcription}")
            except sr.UnknownValueError:
                st.warning("Could not understand audio")
            except sr.RequestError as e:
                st.error(f"Could not request results; {e}")
        
        
        return final_frames, transcription
    
    except Exception as e:
        st.error(f"Unexpected error during recording: {e}")
        return None, None
    finally:
        # Ensure resources are released
        cv2.destroyAllWindows()

# Placeholder for facial expression analysis (removed)
def analyze_facial_expressions(frames):
    return {}