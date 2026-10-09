"""
Automated Unit and Smoke Tests for CareerCraft AI
Validates that prompt construction, JSON parsing, and inference engines work properly.
"""

import sys
import unittest
from ai_engine import (
    extract_json_from_response,
    analyze_resume,
    rewrite_bullet,
    generate_interview_questions,
    evaluate_answer
)
from samples import SAMPLE_DATA

class TestCareerCraftAI(unittest.TestCase):

    def test_json_extractor(self):
        sample_raw = """
        Here is the evaluation:
        ```json
        {
            "score": 85,
            "status": "success",
            "items": ["python", "react"]
        }
        ```
        Hope this helps!
        """
        parsed = extract_json_from_response(sample_raw)
        self.assertEqual(parsed["score"], 85)
        self.assertEqual(parsed["status"], "success")
        self.assertEqual(len(parsed["items"]), 2)

    def test_analyze_resume_offline(self):
        sample = SAMPLE_DATA["Full-Stack Software Engineer"]
        result = analyze_resume(
            resume_text=sample["resume"],
            job_desc=sample["job_description"],
            seniority="Mid-Level",
            use_demo_mode=True
        )
        self.assertIn("overall_score", result)
        self.assertIn("score_breakdown", result)
        self.assertIn("missing_keywords", result)
        self.assertIn("strengths", result)
        self.assertIn("critical_gaps", result)
        self.assertTrue(0 <= result["overall_score"] <= 100)
        print("[OK] Resume Analysis test passed: Score =", result["overall_score"])

    def test_rewrite_bullet_offline(self):
        bullet = "Worked on python code and fixed bugs in production."
        result = rewrite_bullet(
            bullet=bullet,
            target_role="Senior Backend Engineer",
            use_demo_mode=True
        )
        self.assertIn("original_bullet", result)
        self.assertIn("revisions", result)
        self.assertGreaterEqual(len(result["revisions"]), 3)
        print("[OK] Bullet Point Polisher test passed with", len(result["revisions"]), "variations.")

    def test_generate_interview_questions_offline(self):
        sample = SAMPLE_DATA["Full-Stack Software Engineer"]
        result = generate_interview_questions(
            resume_text=sample["resume"],
            job_desc=sample["job_description"],
            use_demo_mode=True
        )
        self.assertIn("interview_questions", result)
        self.assertEqual(len(result["interview_questions"]), 5)
        print("[OK] Interview Questions generator test passed with 5 questions.")

    def test_evaluate_answer_offline(self):
        q = "How do you handle a sudden 10x traffic spike?"
        intent = "Evaluate scalability and caching knowledge."
        ans = "I would implement Redis caching and Kafka queue buffering to prevent database overload."
        job = "Full Stack Engineer"
        result = evaluate_answer(q, intent, ans, job, use_demo_mode=True)
        self.assertIn("score", result)
        self.assertIn("rating", result)
        self.assertIn("strengths", result)
        self.assertIn("model_answer", result)
        print("[OK] Answer Evaluation test passed: Score =", result["score"], "Rating =", result["rating"])

if __name__ == "__main__":
    unittest.main()
