import json
import csv

# Load predefined questions
def load_questions():
    return {
        "HR Questions": [
            "Tell me about yourself.",
            "What are your strengths and weaknesses?",
            "Why do you want to work for this company?",
            "Where do you see yourself in 5 years?",
            "How do you handle stress and pressure?"
        ],
        "OOPs Concepts": [
            "What is object-oriented programming?",
            "Explain the four pillars of object-oriented programming.",
            "What is the difference between abstraction and encapsulation?",
            "Describe the concept of inheritance in object-oriented programming.",
            "How does polymorphism work in object-oriented programming?"
        ],
        "Python": [
            "What are the key features of Python?",
            "Explain the difference between lists and tuples in Python.",
            "How does memory management work in Python?",
            "What is the GIL in Python?",
            "Explain the use of decorators in Python."
        ],
        "Data Structures": [
            "What is the difference between a stack and a queue?",
            "Explain the concept of a binary search tree.",
            "What is a hash table and how does it work?",
            "Describe the time complexity of common sorting algorithms.",
            "What is the difference between a linked list and an array?"
        ],
        "Machine Learning": [
            "What is the difference between supervised and unsupervised learning?",
            "Explain the concept of overfitting and how to prevent it.",
            "What is the difference between classification and regression?",
            "Describe the k-means clustering algorithm.",
            "What is the purpose of cross-validation in machine learning?"
        ],
        "Web Development": [
            "What is the difference between GET and POST HTTP methods?",
            "Explain the concept of RESTful APIs.",
            "What is CORS and why is it important?",
            "Describe the differences between SQL and NoSQL databases.",
            "What are the key principles of responsive web design?"
        ]
    }

# Save progress along with feedback and scores
def save_progress(topic, question, score, feedback):
    """
    Save the user's progress in both JSON and CSV formats.
    """
    # Create data directory if it doesn't exist
    # Path("data").mkdir(exist_ok=True)
    
    # Load existing progress
    progress = track_progress()
    
    # Ensure the topic exists in the progress dictionary
    progress.setdefault(topic, [])
    
    # Add the new progress record
    progress[topic].append({
        "question": question,
        "score": float(score),  # Ensure score is float
        "feedback": feedback.strip('"\'')  # Remove any quotes
    })
    
    # Save to JSON file
    with open("progress.json", "w", encoding='utf-8') as f:
        json.dump(progress, f, indent=4)

    # Save to CSV file
    with open("progress.csv", "w", encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["topic", "question", "score", "feedback"])
        for topic_name, records in progress.items():
            for record in records:
                writer.writerow([
                    topic_name,
                    record["question"],
                    record["score"],
                    record["feedback"]
                ])

def track_progress():
    """
    Load the progress data from the CSV file, or return an empty dictionary if the file doesn't exist.
    """
    try:
        progress = {}
        with open("progress.csv", "r", encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                topic = row["topic"]
                progress.setdefault(topic, [])
                progress[topic].append({
                    "question": row["question"],
                    "score": float(row["score"]),
                    "feedback": row["feedback"]
                })
        return progress
    except FileNotFoundError:
        return {}

# Retrieve detailed feedback summary
# Enhanced get_feedback_summary with missing key handling
def get_feedback_summary():
    """
    Generate a summary of feedback and scores for all topics and questions.
    Handles missing feedback keys gracefully.
    """
    progress = track_progress()
    summary = {}

    for topic, records in progress.items():
        total_score = 0
        feedback_list = []
        for record in records:
            total_score += record["score"]
            # Handle missing feedback key
            feedback_list.append(f"- {record.get('feedback', 'No feedback available for this response.')}")
        
        # Calculate average score per topic
        average_score = total_score / len(records) if records else 0
        summary[topic] = {
            "average_score": round(average_score, 2),
            "feedback": feedback_list,
        }
    
    return summary
