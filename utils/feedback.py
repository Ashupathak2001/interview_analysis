def provide_feedback(sentiment, emotion_data, quality):
    feedback = []

    # Feedback based on sentiment
    if sentiment == "negative":
        feedback.append(
            "Your response reflects a negative tone. Try to use more positive language and emphasize your strengths."
        )
    elif sentiment == "neutral":
        feedback.append(
            "Your response has a neutral tone. Adding enthusiasm or positivity can make your answers more engaging."
        )
    elif sentiment == "positive":
        feedback.append(
            "Great job maintaining a positive tone! This creates a strong impression during interviews."
        )

    # Feedback based on quality
    if quality == "low":
        feedback.append(
            "Your response lacks detail and structure. Provide more examples or elaborate on key points to improve."
        )
    elif quality == "medium":
        feedback.append(
            "Your response is decent but could benefit from more specific details and a structured approach."
        )
    elif quality == "high":
        feedback.append(
            "Excellent response! It's well-detailed and demonstrates a clear understanding of the topic."
        )

    # Feedback based on emotions
    if emotion_data:
        dominant_emotion = max(emotion_data, key=emotion_data.get)
        if dominant_emotion in ["neutral", "sad", "fear", "disgust"]:
            feedback.append(
                "Your facial expressions appear subdued. Smiling and maintaining eye contact can convey confidence."
            )
        elif dominant_emotion in ["happy", "surprise"]:
            feedback.append(
                "Your expressions show enthusiasm, which is great for engaging with interviewers. Keep it up!"
            )
        else:
            feedback.append(
                "Try to keep a balanced and confident demeanor during your responses."
            )
    else:
        feedback.append(
            "Facial expressions could not be analyzed. Ensure your face is clearly visible during the session."
        )

    # Combine and return feedback
    return " ".join(feedback)
