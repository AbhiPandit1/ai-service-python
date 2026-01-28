import time

ROLE_QUESTIONS = {
    "mern": [
        "Explain Node.js event loop",
        "How does React virtual DOM work?",
        "Difference between MongoDB and SQL",
        "Explain JWT authentication",
        "What is useEffect in React?"
    ]
}

class QuestionEngine:

    def __init__(self, role):
        self.role = role
        self.questions = ROLE_QUESTIONS.get(role, [])
        self.index = 0

    def next_question(self):

        if self.index >= len(self.questions):
            return None

        q = self.questions[self.index]

        self.index += 1

        return {
            "questionId": self.index,
            "question": q,
            "timestamp": time.time()
        }
