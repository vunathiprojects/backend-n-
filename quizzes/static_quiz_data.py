"""
Static Quiz Data for 7th Class Subjects
This module contains pre-defined quiz questions for Mathematics and Science subjects
"""

# Static Quiz Data for 7th Class
STATIC_QUIZZES = {
    "mathematics": {
        "subject_name": "Mathematics",
        "class": "7th",
        "topics": {
            "integers": {
                "topic_name": "Integers",
                "description": "Understanding positive and negative numbers",
                "questions": [
                    {
                        "question_id": 1,
                        "question_text": "What is the sum of -15 and 23?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "8", "is_correct": True},
                            {"option_id": "b", "option_text": "-8", "is_correct": False},
                            {"option_id": "c", "option_text": "38", "is_correct": False},
                            {"option_id": "d", "option_text": "-38", "is_correct": False}
                        ],
                        "explanation": "To add -15 and 23: -15 + 23 = 8"
                    },
                    {
                        "question_id": 2,
                        "question_text": "Which of the following is the smallest integer?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "-5", "is_correct": False},
                            {"option_id": "b", "option_text": "-10", "is_correct": True},
                            {"option_id": "c", "option_text": "0", "is_correct": False},
                            {"option_id": "d", "option_text": "3", "is_correct": False}
                        ],
                        "explanation": "Among the given options, -10 is the smallest integer."
                    },
                    {
                        "question_id": 3,
                        "question_text": "What is the product of -4 and 6?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "24", "is_correct": False},
                            {"option_id": "b", "option_text": "-24", "is_correct": True},
                            {"option_id": "c", "option_text": "10", "is_correct": False},
                            {"option_id": "d", "option_text": "-10", "is_correct": False}
                        ],
                        "explanation": "When multiplying a negative and positive number: -4 × 6 = -24"
                    },
                    {
                        "question_id": 4,
                        "question_text": "Arrange in ascending order: -3, 0, -7, 2, -1",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "-7, -3, -1, 0, 2", "is_correct": True},
                            {"option_id": "b", "option_text": "2, 0, -1, -3, -7", "is_correct": False},
                            {"option_id": "c", "option_text": "-1, -3, -7, 0, 2", "is_correct": False},
                            {"option_id": "d", "option_text": "0, -1, -3, -7, 2", "is_correct": False}
                        ],
                        "explanation": "Ascending order means from smallest to largest: -7, -3, -1, 0, 2"
                    },
                    {
                        "question_id": 5,
                        "question_text": "What is the absolute value of -12?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "-12", "is_correct": False},
                            {"option_id": "b", "option_text": "12", "is_correct": True},
                            {"option_id": "c", "option_text": "0", "is_correct": False},
                            {"option_id": "d", "option_text": "24", "is_correct": False}
                        ],
                        "explanation": "Absolute value is always positive. |−12| = 12"
                    }
                ]
            },
            "fractions": {
                "topic_name": "Fractions and Decimals",
                "description": "Understanding fractions, decimals, and their operations",
                "questions": [
                    {
                        "question_id": 6,
                        "question_text": "What is 3/4 + 1/4?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "4/8", "is_correct": False},
                            {"option_id": "b", "option_text": "1", "is_correct": True},
                            {"option_id": "c", "option_text": "4/4", "is_correct": False},
                            {"option_id": "d", "option_text": "2/4", "is_correct": False}
                        ],
                        "explanation": "3/4 + 1/4 = 4/4 = 1"
                    },
                    {
                        "question_id": 7,
                        "question_text": "Convert 0.75 to a fraction in its simplest form.",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "75/100", "is_correct": False},
                            {"option_id": "b", "option_text": "3/4", "is_correct": True},
                            {"option_id": "c", "option_text": "7/10", "is_correct": False},
                            {"option_id": "d", "option_text": "15/20", "is_correct": False}
                        ],
                        "explanation": "0.75 = 75/100 = 3/4 (simplified)"
                    },
                    {
                        "question_id": 8,
                        "question_text": "What is 2/3 × 3/4?",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "6/12", "is_correct": False},
                            {"option_id": "b", "option_text": "1/2", "is_correct": True},
                            {"option_id": "c", "option_text": "5/7", "is_correct": False},
                            {"option_id": "d", "option_text": "6/7", "is_correct": False}
                        ],
                        "explanation": "2/3 × 3/4 = 6/12 = 1/2"
                    },
                    {
                        "question_id": 9,
                        "question_text": "Which is greater: 0.6 or 2/3?",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "0.6", "is_correct": False},
                            {"option_id": "b", "option_text": "2/3", "is_correct": True},
                            {"option_id": "c", "option_text": "They are equal", "is_correct": False},
                            {"option_id": "d", "option_text": "Cannot be determined", "is_correct": False}
                        ],
                        "explanation": "2/3 = 0.666... which is greater than 0.6"
                    },
                    {
                        "question_id": 10,
                        "question_text": "What is 1/2 ÷ 1/4?",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "1/8", "is_correct": False},
                            {"option_id": "b", "option_text": "2", "is_correct": True},
                            {"option_id": "c", "option_text": "1/4", "is_correct": False},
                            {"option_id": "d", "option_text": "4", "is_correct": False}
                        ],
                        "explanation": "1/2 ÷ 1/4 = 1/2 × 4/1 = 4/2 = 2"
                    }
                ]
            },
            "algebra": {
                "topic_name": "Algebra Basics",
                "description": "Introduction to variables and simple equations",
                "questions": [
                    {
                        "question_id": 11,
                        "question_text": "If x + 5 = 12, what is the value of x?",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "7", "is_correct": True},
                            {"option_id": "b", "option_text": "17", "is_correct": False},
                            {"option_id": "c", "option_text": "6", "is_correct": False},
                            {"option_id": "d", "option_text": "8", "is_correct": False}
                        ],
                        "explanation": "x + 5 = 12, so x = 12 - 5 = 7"
                    },
                    {
                        "question_id": 12,
                        "question_text": "What is 3x when x = 4?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "7", "is_correct": False},
                            {"option_id": "b", "option_text": "12", "is_correct": True},
                            {"option_id": "c", "option_text": "34", "is_correct": False},
                            {"option_id": "d", "option_text": "43", "is_correct": False}
                        ],
                        "explanation": "3x = 3 × 4 = 12"
                    },
                    {
                        "question_id": 13,
                        "question_text": "Simplify: 2x + 3x",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "5x", "is_correct": True},
                            {"option_id": "b", "option_text": "6x", "is_correct": False},
                            {"option_id": "c", "option_text": "5x²", "is_correct": False},
                            {"option_id": "d", "option_text": "6x²", "is_correct": False}
                        ],
                        "explanation": "2x + 3x = (2 + 3)x = 5x"
                    },
                    {
                        "question_id": 14,
                        "question_text": "If 2y - 3 = 7, what is y?",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "5", "is_correct": True},
                            {"option_id": "b", "option_text": "2", "is_correct": False},
                            {"option_id": "c", "option_text": "10", "is_correct": False},
                            {"option_id": "d", "option_text": "4", "is_correct": False}
                        ],
                        "explanation": "2y - 3 = 7, so 2y = 10, therefore y = 5"
                    },
                    {
                        "question_id": 15,
                        "question_text": "What is the coefficient of x in the expression 5x + 2?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "5", "is_correct": True},
                            {"option_id": "b", "option_text": "2", "is_correct": False},
                            {"option_id": "c", "option_text": "x", "is_correct": False},
                            {"option_id": "d", "option_text": "7", "is_correct": False}
                        ],
                        "explanation": "The coefficient of x is the number multiplied by x, which is 5"
                    }
                ]
            }
        }
    },
    "science": {
        "subject_name": "Science",
        "class": "7th",
        "topics": {
            "nutrition": {
                "topic_name": "Nutrition in Plants and Animals",
                "description": "Understanding how plants and animals obtain and process food",
                "questions": [
                    {
                        "question_id": 16,
                        "question_text": "What is the process by which plants make their own food?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "Respiration", "is_correct": False},
                            {"option_id": "b", "option_text": "Photosynthesis", "is_correct": True},
                            {"option_id": "c", "option_text": "Digestion", "is_correct": False},
                            {"option_id": "d", "option_text": "Transpiration", "is_correct": False}
                        ],
                        "explanation": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to make glucose (food)."
                    },
                    {
                        "question_id": 17,
                        "question_text": "Which gas do plants absorb from the atmosphere during photosynthesis?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "Oxygen", "is_correct": False},
                            {"option_id": "b", "option_text": "Nitrogen", "is_correct": False},
                            {"option_id": "c", "option_text": "Carbon dioxide", "is_correct": True},
                            {"option_id": "d", "option_text": "Hydrogen", "is_correct": False}
                        ],
                        "explanation": "Plants absorb carbon dioxide from the atmosphere and use it along with water and sunlight to make food."
                    },
                    {
                        "question_id": 18,
                        "question_text": "What is the main function of the small intestine?",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "Storage of food", "is_correct": False},
                            {"option_id": "b", "option_text": "Absorption of nutrients", "is_correct": True},
                            {"option_id": "c", "option_text": "Production of bile", "is_correct": False},
                            {"option_id": "d", "option_text": "Mechanical digestion", "is_correct": False}
                        ],
                        "explanation": "The small intestine is the main site for absorption of nutrients from digested food into the bloodstream."
                    },
                    {
                        "question_id": 19,
                        "question_text": "Which of the following is a parasitic plant?",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "Sunflower", "is_correct": False},
                            {"option_id": "b", "option_text": "Cuscuta", "is_correct": True},
                            {"option_id": "c", "option_text": "Rose", "is_correct": False},
                            {"option_id": "d", "option_text": "Mango", "is_correct": False}
                        ],
                        "explanation": "Cuscuta (dodder) is a parasitic plant that derives its nutrition from other plants."
                    },
                    {
                        "question_id": 20,
                        "question_text": "What type of nutrition do fungi exhibit?",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "Autotrophic", "is_correct": False},
                            {"option_id": "b", "option_text": "Heterotrophic", "is_correct": True},
                            {"option_id": "c", "option_text": "Parasitic", "is_correct": False},
                            {"option_id": "d", "option_text": "Saprophytic", "is_correct": False}
                        ],
                        "explanation": "Fungi are heterotrophic organisms that obtain their nutrition from organic matter."
                    }
                ]
            },
            "respiration": {
                "topic_name": "Respiration in Organisms",
                "description": "Understanding how different organisms respire",
                "questions": [
                    {
                        "question_id": 21,
                        "question_text": "What is the main purpose of respiration?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "To produce oxygen", "is_correct": False},
                            {"option_id": "b", "option_text": "To release energy", "is_correct": True},
                            {"option_id": "c", "option_text": "To remove carbon dioxide", "is_correct": False},
                            {"option_id": "d", "option_text": "To produce water", "is_correct": False}
                        ],
                        "explanation": "The main purpose of respiration is to release energy from glucose for cellular activities."
                    },
                    {
                        "question_id": 22,
                        "question_text": "Which organ is responsible for gas exchange in humans?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "Heart", "is_correct": False},
                            {"option_id": "b", "option_text": "Lungs", "is_correct": True},
                            {"option_id": "c", "option_text": "Liver", "is_correct": False},
                            {"option_id": "d", "option_text": "Kidney", "is_correct": False}
                        ],
                        "explanation": "Lungs are the primary organs responsible for gas exchange in humans."
                    },
                    {
                        "question_id": 23,
                        "question_text": "How do fish respire underwater?",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "Through lungs", "is_correct": False},
                            {"option_id": "b", "option_text": "Through gills", "is_correct": True},
                            {"option_id": "c", "option_text": "Through skin", "is_correct": False},
                            {"option_id": "d", "option_text": "Through spiracles", "is_correct": False}
                        ],
                        "explanation": "Fish respire through gills, which extract oxygen from water."
                    },
                    {
                        "question_id": 24,
                        "question_text": "What happens to the diaphragm during inhalation?",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "It moves up", "is_correct": False},
                            {"option_id": "b", "option_text": "It moves down", "is_correct": True},
                            {"option_id": "c", "option_text": "It remains stationary", "is_correct": False},
                            {"option_id": "d", "option_text": "It contracts and relaxes", "is_correct": False}
                        ],
                        "explanation": "During inhalation, the diaphragm contracts and moves down, increasing the chest cavity volume."
                    },
                    {
                        "question_id": 25,
                        "question_text": "Which gas is released during respiration?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "Oxygen", "is_correct": False},
                            {"option_id": "b", "option_text": "Carbon dioxide", "is_correct": True},
                            {"option_id": "c", "option_text": "Nitrogen", "is_correct": False},
                            {"option_id": "d", "option_text": "Hydrogen", "is_correct": False}
                        ],
                        "explanation": "Carbon dioxide is released as a waste product during cellular respiration."
                    }
                ]
            },
            "transportation": {
                "topic_name": "Transportation in Plants and Animals",
                "description": "Understanding how materials are transported in living organisms",
                "questions": [
                    {
                        "question_id": 26,
                        "question_text": "What is the main function of the heart?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "To produce blood", "is_correct": False},
                            {"option_id": "b", "option_text": "To pump blood", "is_correct": True},
                            {"option_id": "c", "option_text": "To filter blood", "is_correct": False},
                            {"option_id": "d", "option_text": "To store blood", "is_correct": False}
                        ],
                        "explanation": "The heart's main function is to pump blood throughout the body."
                    },
                    {
                        "question_id": 27,
                        "question_text": "Which blood vessels carry blood away from the heart?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "Veins", "is_correct": False},
                            {"option_id": "b", "option_text": "Arteries", "is_correct": True},
                            {"option_id": "c", "option_text": "Capillaries", "is_correct": False},
                            {"option_id": "d", "option_text": "Venules", "is_correct": False}
                        ],
                        "explanation": "Arteries carry oxygenated blood away from the heart to various parts of the body."
                    },
                    {
                        "question_id": 28,
                        "question_text": "What is transported through xylem in plants?",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "Food", "is_correct": False},
                            {"option_id": "b", "option_text": "Water and minerals", "is_correct": True},
                            {"option_id": "c", "option_text": "Oxygen", "is_correct": False},
                            {"option_id": "d", "option_text": "Carbon dioxide", "is_correct": False}
                        ],
                        "explanation": "Xylem transports water and minerals from roots to other parts of the plant."
                    },
                    {
                        "question_id": 29,
                        "question_text": "What is the function of phloem in plants?",
                        "question_type": "multiple_choice",
                        "points": 2,
                        "options": [
                            {"option_id": "a", "option_text": "Transport of water", "is_correct": False},
                            {"option_id": "b", "option_text": "Transport of food", "is_correct": True},
                            {"option_id": "c", "option_text": "Transport of minerals", "is_correct": False},
                            {"option_id": "d", "option_text": "Transport of oxygen", "is_correct": False}
                        ],
                        "explanation": "Phloem transports food (sugars) from leaves to other parts of the plant."
                    },
                    {
                        "question_id": 30,
                        "question_text": "How many chambers does a human heart have?",
                        "question_type": "multiple_choice",
                        "points": 1,
                        "options": [
                            {"option_id": "a", "option_text": "2", "is_correct": False},
                            {"option_id": "b", "option_text": "3", "is_correct": False},
                            {"option_id": "c", "option_text": "4", "is_correct": True},
                            {"option_id": "d", "option_text": "5", "is_correct": False}
                        ],
                        "explanation": "A human heart has 4 chambers: 2 atria and 2 ventricles."
                    }
                ]
            }
        }
    }
}

def get_quiz_data(subject, topic=None):
    """
    Get quiz data for a specific subject and optionally a specific topic
    
    Args:
        subject (str): Subject name ('mathematics' or 'science')
        topic (str, optional): Specific topic name
    
    Returns:
        dict: Quiz data
    """
    if subject not in STATIC_QUIZZES:
        return None
    
    if topic:
        if topic in STATIC_QUIZZES[subject]["topics"]:
            return STATIC_QUIZZES[subject]["topics"][topic]
        else:
            return None
    
    return STATIC_QUIZZES[subject]

def get_all_subjects():
    """
    Get list of all available subjects
    
    Returns:
        list: List of subject names
    """
    return list(STATIC_QUIZZES.keys())

def get_topics_for_subject(subject):
    """
    Get all topics for a specific subject
    
    Args:
        subject (str): Subject name
    
    Returns:
        list: List of topic names
    """
    if subject not in STATIC_QUIZZES:
        return []
    
    return list(STATIC_QUIZZES[subject]["topics"].keys())

def get_questions_for_topic(subject, topic):
    """
    Get all questions for a specific topic
    
    Args:
        subject (str): Subject name
        topic (str): Topic name
    
    Returns:
        list: List of questions
    """
    topic_data = get_quiz_data(subject, topic)
    if topic_data:
        return topic_data.get("questions", [])
    return []

def calculate_quiz_score(answers):
    """
    Calculate quiz score based on answers
    
    Args:
        answers (list): List of answer dictionaries with question_id and selected_option
    
    Returns:
        dict: Score information
    """
    total_score = 0
    total_questions = 0
    correct_answers = 0
    
    # Get all questions from all topics
    all_questions = {}
    for subject in STATIC_QUIZZES.values():
        for topic in subject["topics"].values():
            for question in topic["questions"]:
                all_questions[question["question_id"]] = question
    
    for answer in answers:
        question_id = answer.get("question_id")
        selected_option = answer.get("selected_option")
        
        if question_id in all_questions:
            question = all_questions[question_id]
            total_questions += 1
            
            # Find the correct option
            correct_option = None
            for option in question["options"]:
                if option["is_correct"]:
                    correct_option = option["option_id"]
                    break
            
            if selected_option == correct_option:
                correct_answers += 1
                total_score += question["points"]
    
    percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    return {
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "wrong_answers": total_questions - correct_answers,
        "total_score": total_score,
        "percentage": round(percentage, 2),
        "is_passed": percentage >= 60  # 60% passing criteria
    }
