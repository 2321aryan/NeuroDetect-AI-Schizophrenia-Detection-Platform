from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Set
import json
import random
import uuid
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Symptom Checklist AI", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Question Database - Comprehensive mental health symptom questions
SYMPTOM_QUESTIONS = {
    "schizophrenia": [
        {
            "id": "sch_1",
            "question": "Do you hear voices that others cannot hear?",
            "category": "hallucinations",
            "severity_weight": 0.9,
            "follow_up": ["sch_2", "sch_3"]
        },
        {
            "id": "sch_2",
            "question": "Do you see things that others cannot see?",
            "category": "hallucinations",
            "severity_weight": 0.8,
            "follow_up": ["sch_4", "sch_5"]
        },
        {
            "id": "sch_3",
            "question": "Do you believe that people are plotting against you or trying to harm you?",
            "category": "delusions",
            "severity_weight": 0.9,
            "follow_up": ["sch_6", "sch_7"]
        },
        {
            "id": "sch_4",
            "question": "Do you believe you have special powers or abilities that others don't have?",
            "category": "delusions",
            "severity_weight": 0.7,
            "follow_up": ["sch_8"]
        },
        {
            "id": "sch_5",
            "question": "Do you find it difficult to organize your thoughts or speak clearly?",
            "category": "disorganized_thinking",
            "severity_weight": 0.6,
            "follow_up": ["sch_9", "sch_10"]
        },
        {
            "id": "sch_6",
            "question": "Do you feel like your thoughts are being controlled by external forces?",
            "category": "delusions",
            "severity_weight": 0.8,
            "follow_up": ["sch_11"]
        },
        {
            "id": "sch_7",
            "question": "Do you have difficulty showing emotions or facial expressions?",
            "category": "negative_symptoms",
            "severity_weight": 0.5,
            "follow_up": ["sch_12", "sch_13"]
        },
        {
            "id": "sch_8",
            "question": "Do you find it hard to start or complete tasks?",
            "category": "negative_symptoms",
            "severity_weight": 0.6,
            "follow_up": ["sch_14"]
        },
        {
            "id": "sch_9",
            "question": "Do you feel disconnected from reality or like things around you are not real?",
            "category": "depersonalization",
            "severity_weight": 0.7,
            "follow_up": ["sch_15"]
        },
        {
            "id": "sch_10",
            "question": "Do you have trouble concentrating or paying attention?",
            "category": "cognitive",
            "severity_weight": 0.5,
            "follow_up": ["sch_16"]
        }
    ],
    "depression": [
        {
            "id": "dep_1",
            "question": "Do you feel sad, empty, or hopeless most of the day?",
            "category": "mood",
            "severity_weight": 0.8,
            "follow_up": ["dep_2", "dep_3"]
        },
        {
            "id": "dep_2",
            "question": "Have you lost interest or pleasure in activities you used to enjoy?",
            "category": "anhedonia",
            "severity_weight": 0.9,
            "follow_up": ["dep_4", "dep_5"]
        },
        {
            "id": "dep_3",
            "question": "Do you have trouble sleeping or sleep too much?",
            "category": "sleep",
            "severity_weight": 0.6,
            "follow_up": ["dep_6"]
        },
        {
            "id": "dep_4",
            "question": "Do you feel tired or have little energy most days?",
            "category": "fatigue",
            "severity_weight": 0.7,
            "follow_up": ["dep_7"]
        },
        {
            "id": "dep_5",
            "question": "Do you have thoughts of death or suicide?",
            "category": "suicidal_thoughts",
            "severity_weight": 1.0,
            "follow_up": ["dep_8"]
        }
    ],
    "anxiety": [
        {
            "id": "anx_1",
            "question": "Do you experience excessive worry or anxiety about various things?",
            "category": "generalized_anxiety",
            "severity_weight": 0.8,
            "follow_up": ["anx_2", "anx_3"]
        },
        {
            "id": "anx_2",
            "question": "Do you have sudden attacks of fear or panic?",
            "category": "panic_attacks",
            "severity_weight": 0.9,
            "follow_up": ["anx_4"]
        },
        {
            "id": "anx_3",
            "question": "Do you avoid certain situations due to fear or anxiety?",
            "category": "avoidance",
            "severity_weight": 0.7,
            "follow_up": ["anx_5"]
        },
        {
            "id": "anx_4",
            "question": "Do you experience physical symptoms like rapid heartbeat or sweating when anxious?",
            "category": "physical_symptoms",
            "severity_weight": 0.6,
            "follow_up": ["anx_6"]
        }
    ],
    "bipolar": [
        {
            "id": "bip_1",
            "question": "Do you experience periods of unusually high energy and activity?",
            "category": "mania",
            "severity_weight": 0.8,
            "follow_up": ["bip_2", "bip_3"]
        },
        {
            "id": "bip_2",
            "question": "Do you feel like you need less sleep than usual during these periods?",
            "category": "mania",
            "severity_weight": 0.7,
            "follow_up": ["bip_4"]
        },
        {
            "id": "bip_3",
            "question": "Do you talk faster or more than usual during these periods?",
            "category": "mania",
            "severity_weight": 0.6,
            "follow_up": ["bip_5"]
        }
    ],
    "ocd": [
        {
            "id": "ocd_1",
            "question": "Do you have unwanted, intrusive thoughts that cause distress?",
            "category": "obsessions",
            "severity_weight": 0.8,
            "follow_up": ["ocd_2", "ocd_3"]
        },
        {
            "id": "ocd_2",
            "question": "Do you feel compelled to perform certain behaviors or rituals?",
            "category": "compulsions",
            "severity_weight": 0.9,
            "follow_up": ["ocd_4"]
        },
        {
            "id": "ocd_3",
            "question": "Do these thoughts or behaviors interfere with your daily life?",
            "category": "interference",
            "severity_weight": 0.7,
            "follow_up": ["ocd_5"]
        }
    ]
}

# Additional follow-up questions
FOLLOW_UP_QUESTIONS = {
    "sch_11": {
        "id": "sch_11",
        "question": "Do you believe that your thoughts are being broadcast to others?",
        "category": "delusions",
        "severity_weight": 0.9
    },
    "sch_12": {
        "id": "sch_12",
        "question": "Do you have difficulty maintaining relationships with friends and family?",
        "category": "social_functioning",
        "severity_weight": 0.6
    },
    "sch_13": {
        "id": "sch_13",
        "question": "Do you prefer to be alone most of the time?",
        "category": "negative_symptoms",
        "severity_weight": 0.5
    },
    "sch_14": {
        "id": "sch_14",
        "question": "Do you have difficulty with daily activities like cooking or cleaning?",
        "category": "functional_impairment",
        "severity_weight": 0.7
    },
    "sch_15": {
        "id": "sch_15",
        "question": "Do you feel like you're living in a dream or that the world around you is not real?",
        "category": "depersonalization",
        "severity_weight": 0.8
    },
    "sch_16": {
        "id": "sch_16",
        "question": "Do you have trouble remembering recent events or conversations?",
        "category": "cognitive",
        "severity_weight": 0.6
    },
    "dep_6": {
        "id": "dep_6",
        "question": "Do you have changes in your appetite or weight?",
        "category": "appetite",
        "severity_weight": 0.5
    },
    "dep_7": {
        "id": "dep_7",
        "question": "Do you feel worthless or guilty about things?",
        "category": "self_worth",
        "severity_weight": 0.7
    },
    "dep_8": {
        "id": "dep_8",
        "question": "Have you made plans or attempted to harm yourself?",
        "category": "suicidal_behavior",
        "severity_weight": 1.0
    },
    "anx_5": {
        "id": "anx_5",
        "question": "Do you experience anxiety in social situations?",
        "category": "social_anxiety",
        "severity_weight": 0.7
    },
    "anx_6": {
        "id": "anx_6",
        "question": "Do you have difficulty controlling your worry?",
        "category": "worry_control",
        "severity_weight": 0.6
    },
    "bip_4": {
        "id": "bip_4",
        "question": "Do you feel more confident or powerful than usual during these periods?",
        "category": "mania",
        "severity_weight": 0.7
    },
    "bip_5": {
        "id": "bip_5",
        "question": "Do you engage in risky behaviors during these periods?",
        "category": "mania",
        "severity_weight": 0.8
    },
    "ocd_4": {
        "id": "ocd_4",
        "question": "Do you spend more than an hour per day on these behaviors?",
        "category": "compulsions",
        "severity_weight": 0.8
    },
    "ocd_5": {
        "id": "ocd_5",
        "question": "Do you feel temporary relief after performing these behaviors?",
        "category": "compulsions",
        "severity_weight": 0.6
    }
}

# Response options
RESPONSE_OPTIONS = ["yes", "no", "not sure", "i don't know"]

# Session storage
sessions = {}

class SessionData(BaseModel):
    session_id: str
    answers: Dict[str, str] = {}
    current_question: Optional[str] = None
    asked_questions: Set[str] = set()
    condition_scores: Dict[str, float] = {}
    start_time: datetime
    last_activity: datetime

class QuestionRequest(BaseModel):
    session_id: str

class AnswerRequest(BaseModel):
    session_id: str
    question_id: str
    answer: str

class AnalysisRequest(BaseModel):
    session_id: str

def calculate_next_question(session_data: SessionData) -> Optional[Dict]:
    """Intelligently select the next question based on previous answers"""
    
    # If no questions asked yet, start with high-priority questions
    if not session_data.asked_questions:
        return get_priority_question()
    
    # Analyze current answers to determine condition likelihood
    condition_scores = analyze_condition_likelihood(session_data.answers)
    session_data.condition_scores = condition_scores
    
    # Find the most likely condition
    most_likely_condition = max(condition_scores.items(), key=lambda x: x[1])[0]
    
    # Get questions for the most likely condition
    available_questions = []
    
    # Add questions from the most likely condition
    if most_likely_condition in SYMPTOM_QUESTIONS:
        for question in SYMPTOM_QUESTIONS[most_likely_condition]:
            if question["id"] not in session_data.asked_questions:
                available_questions.append(question)
    
    # Add follow-up questions based on current answers
    for question_id, answer in session_data.answers.items():
        if answer in ["yes", "not sure"]:
            # Find questions that have this as a follow-up
            for condition_questions in SYMPTOM_QUESTIONS.values():
                for question in condition_questions:
                    if question_id in question.get("follow_up", []):
                        follow_up_id = question_id
                        if follow_up_id in FOLLOW_UP_QUESTIONS:
                            follow_up_q = FOLLOW_UP_QUESTIONS[follow_up_id]
                            if follow_up_q["id"] not in session_data.asked_questions:
                                available_questions.append(follow_up_q)
    
    # If no specific follow-ups, add questions from other conditions
    if not available_questions:
        for condition, questions in SYMPTOM_QUESTIONS.items():
            for question in questions:
                if question["id"] not in session_data.asked_questions:
                    available_questions.append(question)
    
    # Sort by severity weight and return the highest priority question
    if available_questions:
        available_questions.sort(key=lambda x: x["severity_weight"], reverse=True)
        return available_questions[0]
    
    return None

def get_priority_question() -> Dict:
    """Get a high-priority screening question"""
    priority_questions = [
        SYMPTOM_QUESTIONS["schizophrenia"][0],  # Hearing voices
        SYMPTOM_QUESTIONS["depression"][0],     # Sadness
        SYMPTOM_QUESTIONS["anxiety"][0],        # Excessive worry
    ]
    return random.choice(priority_questions)

def analyze_condition_likelihood(answers: Dict[str, str]) -> Dict[str, float]:
    """Analyze answers to determine likelihood of different conditions"""
    
    condition_scores = {
        "schizophrenia": 0.0,
        "depression": 0.0,
        "anxiety": 0.0,
        "bipolar": 0.0,
        "ocd": 0.0
    }
    
    # Score each answer
    for question_id, answer in answers.items():
        if answer == "yes":
            # Find the question and add its weight
            for condition, questions in SYMPTOM_QUESTIONS.items():
                for question in questions:
                    if question["id"] == question_id:
                        condition_scores[condition] += question["severity_weight"]
                        break
            
            # Check follow-up questions
            if question_id in FOLLOW_UP_QUESTIONS:
                follow_up = FOLLOW_UP_QUESTIONS[question_id]
                condition_scores[condition] += follow_up["severity_weight"] * 0.5
        
        elif answer == "not sure":
            # Add partial weight for uncertain answers
            for condition, questions in SYMPTOM_QUESTIONS.items():
                for question in questions:
                    if question["id"] == question_id:
                        condition_scores[condition] += question["severity_weight"] * 0.3
                        break
    
    # Normalize scores
    max_score = max(condition_scores.values()) if condition_scores.values() else 1
    if max_score > 0:
        for condition in condition_scores:
            condition_scores[condition] = condition_scores[condition] / max_score
    
    return condition_scores

def generate_analysis(session_data: SessionData) -> Dict:
    """Generate comprehensive analysis based on all answers"""
    
    answers = session_data.answers
    condition_scores = session_data.condition_scores
    
    # Count responses
    yes_count = sum(1 for answer in answers.values() if answer == "yes")
    no_count = sum(1 for answer in answers.values() if answer == "no")
    not_sure_count = sum(1 for answer in answers.values() if answer == "not sure")
    dont_know_count = sum(1 for answer in answers.values() if answer == "i don't know")
    
    # Determine primary condition
    primary_condition = max(condition_scores.items(), key=lambda x: x[1])
    
    # Generate severity assessment
    total_questions = len(answers)
    positive_symptoms = yes_count + (not_sure_count * 0.5)
    severity_percentage = (positive_symptoms / total_questions) * 100 if total_questions > 0 else 0
    
    if severity_percentage >= 70:
        severity_level = "High"
        risk_level = "High"
    elif severity_percentage >= 40:
        severity_level = "Moderate"
        risk_level = "Moderate"
    else:
        severity_level = "Low"
        risk_level = "Low"
    
    # Generate specific insights
    insights = []
    
    # Schizophrenia insights
    if condition_scores["schizophrenia"] > 0.6:
        schizo_symptoms = []
        for q_id, answer in answers.items():
            if answer in ["yes", "not sure"]:
                for question in SYMPTOM_QUESTIONS["schizophrenia"]:
                    if question["id"] == q_id:
                        schizo_symptoms.append(question["category"])
                        break
        
        if "hallucinations" in schizo_symptoms:
            insights.append("Hallucinatory experiences detected - may indicate psychotic symptoms")
        if "delusions" in schizo_symptoms:
            insights.append("Delusional thinking patterns observed - requires professional evaluation")
        if "negative_symptoms" in schizo_symptoms:
            insights.append("Negative symptoms present - may affect daily functioning")
    
    # Depression insights
    if condition_scores["depression"] > 0.6:
        dep_symptoms = []
        for q_id, answer in answers.items():
            if answer in ["yes", "not sure"]:
                for question in SYMPTOM_QUESTIONS["depression"]:
                    if question["id"] == q_id:
                        dep_symptoms.append(question["category"])
                        break
        
        if "suicidal_thoughts" in dep_symptoms:
            insights.append("CRITICAL: Suicidal thoughts detected - immediate professional help needed")
        if "anhedonia" in dep_symptoms:
            insights.append("Loss of interest in activities - common in depression")
    
    # Anxiety insights
    if condition_scores["anxiety"] > 0.6:
        insights.append("Anxiety symptoms present - may benefit from anxiety management techniques")
    
    # Generate recommendations
    recommendations = []
    
    if risk_level == "High":
        recommendations.append("Immediate consultation with a mental health professional is strongly recommended")
        recommendations.append("Consider reaching out to a crisis hotline if experiencing severe symptoms")
    elif risk_level == "Moderate":
        recommendations.append("Schedule an appointment with a mental health professional for evaluation")
        recommendations.append("Consider speaking with your primary care physician")
    else:
        recommendations.append("Continue monitoring symptoms and seek help if they worsen")
        recommendations.append("Consider preventive mental health check-ups")
    
    return {
        "session_id": session_data.session_id,
        "analysis_timestamp": datetime.now().isoformat(),
        "questions_answered": total_questions,
        "response_breakdown": {
            "yes": yes_count,
            "no": no_count,
            "not_sure": not_sure_count,
            "dont_know": dont_know_count
        },
        "condition_scores": condition_scores,
        "primary_condition": {
            "condition": primary_condition[0],
            "confidence": round(primary_condition[1] * 100, 1)
        },
        "severity_assessment": {
            "level": severity_level,
            "percentage": round(severity_percentage, 1),
            "risk_level": risk_level
        },
        "insights": insights,
        "recommendations": recommendations,
        "next_steps": [
            "Share this analysis with a mental health professional",
            "Keep a symptom diary to track changes over time",
            "Consider lifestyle changes that support mental health",
            "Build a support network of friends and family"
        ]
    }

@app.post("/start-session")
async def start_session():
    """Start a new symptom checklist session"""
    session_id = str(uuid.uuid4())
    
    session_data = SessionData(
        session_id=session_id,
        start_time=datetime.now(),
        last_activity=datetime.now()
    )
    
    sessions[session_id] = session_data
    
    # Get first question
    first_question = get_priority_question()
    session_data.current_question = first_question["id"]
    session_data.asked_questions.add(first_question["id"])
    
    return {
        "session_id": session_id,
        "question": {
            "id": first_question["id"],
            "text": first_question["question"],
            "category": first_question["category"],
            "options": RESPONSE_OPTIONS
        },
        "progress": {
            "current": 1,
            "estimated_total": 30
        }
    }

@app.post("/get-question")
async def get_question(request: QuestionRequest):
    """Get the next question for the session"""
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[request.session_id]
    session_data.last_activity = datetime.now()
    
    # If we have a current question, return it
    if session_data.current_question:
        question_id = session_data.current_question
        
        # Find the question
        for condition_questions in SYMPTOM_QUESTIONS.values():
            for question in condition_questions:
                if question["id"] == question_id:
                    return {
                        "session_id": request.session_id,
                        "question": {
                            "id": question["id"],
                            "text": question["question"],
                            "category": question["category"],
                            "options": RESPONSE_OPTIONS
                        },
                        "progress": {
                            "current": len(session_data.asked_questions),
                            "estimated_total": 30
                        }
                    }
        
        # Check follow-up questions
        if question_id in FOLLOW_UP_QUESTIONS:
            question = FOLLOW_UP_QUESTIONS[question_id]
            return {
                "session_id": request.session_id,
                "question": {
                    "id": question["id"],
                    "text": question["question"],
                    "category": question["category"],
                    "options": RESPONSE_OPTIONS
                },
                "progress": {
                    "current": len(session_data.asked_questions),
                    "estimated_total": 30
                }
            }
    
    # Get next intelligent question
    next_question = calculate_next_question(session_data)
    
    if not next_question:
        # No more questions, session complete
        return {
            "session_id": request.session_id,
            "status": "complete",
            "message": "All relevant questions have been answered. Ready for analysis."
        }
    
    session_data.current_question = next_question["id"]
    session_data.asked_questions.add(next_question["id"])
    
    return {
        "session_id": request.session_id,
        "question": {
            "id": next_question["id"],
            "text": next_question["question"],
            "category": next_question["category"],
            "options": RESPONSE_OPTIONS
        },
        "progress": {
            "current": len(session_data.asked_questions),
            "estimated_total": 30
        }
    }

@app.post("/submit-answer")
async def submit_answer(request: AnswerRequest):
    """Submit an answer to the current question"""
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if request.answer not in RESPONSE_OPTIONS:
        raise HTTPException(status_code=400, detail="Invalid answer option")
    
    session_data = sessions[request.session_id]
    session_data.last_activity = datetime.now()
    
    # Store the answer
    session_data.answers[request.question_id] = request.answer
    
    # Clear current question to get next one
    session_data.current_question = None
    
    return {
        "session_id": request.session_id,
        "status": "answer_received",
        "message": "Answer recorded successfully"
    }

@app.post("/analyze")
async def analyze_session(request: AnalysisRequest):
    """Generate comprehensive analysis of the session"""
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[request.session_id]
    
    if len(session_data.answers) < 5:
        raise HTTPException(status_code=400, detail="Need at least 5 answers for analysis")
    
    # Generate analysis
    analysis = generate_analysis(session_data)
    
    return analysis

@app.get("/health")
def health_check():
    return {"status": "ok"}
#@app.get("/health")
#async def health_check():
#    """Health check endpoint"""
#    return {
#        "status": "Symptom Checklist AI is running",
#        "version": "2.0.0",
#        "active_sessions": len(sessions),
#        "timestamp": datetime.now().isoformat()
#    }

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "Session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Symptom Checklist AI on http://0.0.0.0:8001 ...")
    uvicorn.run(app, host="0.0.0.0", port=8001) 