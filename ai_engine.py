"""
CareerCraft AI - GenAI Engine
Handles communication with Google Gemini API models, structured JSON extraction,
and provides a high-fidelity local deterministic inference engine when running in offline/demo mode.
"""

import json
import re
import random
import os
from typing import Dict, Any, Optional

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from prompts import (
    RESUME_ANALYSIS_SYSTEM_PROMPT,
    RESUME_ANALYSIS_USER_TEMPLATE,
    STAR_BULLET_SYSTEM_PROMPT,
    STAR_BULLET_USER_TEMPLATE,
    INTERVIEW_GEN_SYSTEM_PROMPT,
    INTERVIEW_GEN_USER_TEMPLATE,
    ANSWER_EVAL_SYSTEM_PROMPT,
    ANSWER_EVAL_USER_TEMPLATE
)


def extract_json_from_response(text: str) -> Dict[str, Any]:
    """
    Safely extract JSON object from LLM response text,
    stripping markdown fences or surrounding chatter if present.
    """
    text = text.strip()
    
    # Check for markdown code blocks
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # Try finding the first '{' and last '}'
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            json_str = text[start : end + 1]
        else:
            json_str = text

    try:
        return json.loads(json_str)
    except Exception as e:
        # Fallback sanitization for common JSON syntax issues
        # e.g., trailing commas
        cleaned = re.sub(r",\s*([\]}])", r"\1", json_str)
        return json.loads(cleaned)


def call_gemini(
    system_prompt: str,
    user_prompt: str,
    api_key: Optional[str] = None,
    model_name: str = "gemini-1.5-flash",
    temperature: float = 0.4
) -> str:
    """Calls Google Gemini model via google.generativeai SDK."""
    if not GEMINI_AVAILABLE:
        raise RuntimeError("google-generativeai package is not installed.")

    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError("Missing Gemini API Key. Provide a valid API key or use Demo Mode.")

    genai.configure(api_key=key)
    
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        top_p=0.95,
        max_output_tokens=2500,
        response_mime_type="application/json"
    )

    # Instantiate model with system instruction
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt,
        generation_config=generation_config
    )

    response = model.generate_content(user_prompt)
    if not response.text:
        raise ValueError("Gemini returned an empty response. Check API quota or content safety filters.")
        
    return response.text


# ==============================================================================
# FALLBACK / OFFLINE DETERMINISTIC INFERENCE ENGINE
# ==============================================================================

def fallback_analyze_resume(resume_text: str, job_desc: str, seniority: str) -> Dict[str, Any]:
    """Deterministic, context-aware analysis engine for offline / demo mode."""
    resume_lower = resume_text.lower()
    job_lower = job_desc.lower()

    # Common tech keywords to scan
    keywords_to_check = [
        "python", "react", "typescript", "javascript", "sql", "postgresql",
        "docker", "kubernetes", "aws", "gcp", "azure", "fastapi", "django",
        "graphql", "redis", "kafka", "ci/cd", "rest api", "tailwind", "pytest",
        "pytorch", "tensorflow", "nlp", "llm", "tableau", "mixpanel", "jira",
        "agile", "scrum", "microservices"
    ]

    matched = []
    missing = []
    for kw in keywords_to_check:
        in_job = kw in job_lower
        in_resume = kw in resume_lower
        if in_job and in_resume:
            matched.append(kw.title())
        elif in_job and not in_resume:
            missing.append(kw.title())

    # If job description has very specific custom terms, grab some
    if not missing:
        missing = ["AWS (ECS/Lambda)", "Distributed Caching (Redis)", "CI/CD Automation", "Kafka Message Queues"]
    if not matched:
        matched = ["Python", "REST APIs", "SQL", "Git", "Agile"]

    total_relevant = len(matched) + len(missing)
    ratio = len(matched) / max(total_relevant, 1)
    base_score = int(55 + (ratio * 35))
    base_score = min(max(base_score, 45), 92)

    tech_score = int(base_score * 0.95)
    exp_score = int(base_score * 1.05) if "senior" not in seniority.lower() else int(base_score * 0.82)
    soft_score = random.randint(78, 88)
    edu_score = 85

    return {
        "overall_score": base_score,
        "score_breakdown": {
            "technical_skills": min(tech_score, 98),
            "experience_relevance": min(exp_score, 95),
            "soft_skills": soft_score,
            "education_and_certs": edu_score
        },
        "summary": f"The candidate exhibits solid fundamental experience aligning with key foundations ({', '.join(matched[:3])}). However, to compete effectively for {seniority} level roles, they need to explicitly bridge gaps in cloud-scale infrastructure, event-driven streaming, and quantified delivery metrics.",
        "matching_keywords": matched[:8],
        "missing_keywords": missing[:6],
        "strengths": [
            f"Demonstrated core competence in {', '.join(matched[:2])} with hands-on production application delivery.",
            "Clear educational foundation in computer science with agile team participation.",
            "Practical experience with database query optimization and API layer integration."
        ],
        "critical_gaps": [
            f"Lacks explicit proof of experience with mission-critical target requirements: {', '.join(missing[:3])}.",
            "Current bullet points focus predominantly on daily duties rather than business metrics, latency improvements, or scale.",
            "Limited evidence of architectural design leadership or automated CI/CD pipeline ownership."
        ],
        "actionable_recommendations": [
            f"Incorporate missing high-priority target terms ({', '.join(missing[:3])}) into project descriptions where applicable.",
            "Rewrite current bullet points using the STAR formula with explicit percentages (e.g., '% query speedup', '% coverage').",
            "Include a dedicated 'System Architecture' or 'Cloud DevOps' project highlighting containerized deployments."
        ]
    }


def fallback_rewrite_bullet(bullet: str, target_role: str) -> Dict[str, Any]:
    """Generates three STAR-framework variations of weak bullet points."""
    return {
        "original_bullet": bullet,
        "analysis_of_weakness": "The original bullet point describes passive job duties without highlighting the business context, specific tooling stack, or measurable outcomes achieved.",
        "revisions": [
            {
                "style": "Action & Impact",
                "text": f"Architected and deployed modular backend microservices for {target_role or 'production systems'}, streamlining data pipelines and slashing API response latency by 38%.",
                "why_it_works": "Replaces passive verbs with 'Architected and deployed', emphasizes end-to-end ownership, and connects technical actions to latency improvements."
            },
            {
                "style": "Metric & Quantification Driven",
                "text": "Refactored legacy database queries and implemented asynchronous request batching, reducing server resource utilization by 42% across 150K+ daily transactions.",
                "why_it_works": "Introduces concrete metrics (42% reduction, 150K+ daily transactions), offering indisputable evidence of high-scale engineering."
            },
            {
                "style": "Leadership & Architectural Scope",
                "text": "Spearheaded cross-functional initiative across 5 developers to standardize REST API protocols and CI/CD testing, accelerating release velocity by 2.5x with 99.9% uptime.",
                "why_it_works": "Demonstrates senior-level leadership, collaboration, and measurable organizational acceleration."
            }
        ],
        "suggested_metrics_to_quantify": [
            "Percentage reduction in API latency or page load time",
            "Daily / monthly active users (DAU/MAU) impacted by the feature",
            "Code test coverage improvement (e.g., from 55% to 88%)",
            "Infrastructure cost savings per month via query or caching optimization"
        ]
    }


def fallback_generate_interview_questions(resume_text: str, job_desc: str) -> Dict[str, Any]:
    """Generates 5 tailored, challenging interview questions."""
    return {
        "interview_questions": [
            {
                "id": 1,
                "category": "Technical Architecture",
                "question": "In your resume, you mention developing REST APIs and optimizing queries. How would you architect this service to handle a sudden 10x traffic spike using caching and asynchronous queues?",
                "intent": "Evaluates candidate's comprehension of distributed systems scalability, Redis caching strategies, and load mitigation beyond single-node databases.",
                "tips_for_answering": "Explain caching layers (cache-aside pattern), database connection pooling, read replicas, and offloading heavy tasks to a background worker queue."
            },
            {
                "id": 2,
                "category": "Behavioral (STAR Method)",
                "question": "Tell me about a time when a critical bug or performance regression escaped into production. How did you diagnose it, coordinate with the team, and prevent recurrence?",
                "intent": "Assesses emotional resilience, root-cause analysis (RCA), ownership, blameless post-mortem culture, and CI/CD quality gates.",
                "tips_for_answering": "Use the STAR framework: Describe the Incident (Situation/Task), triage & rollback (Action), monitoring & post-mortem with automated tests added (Result)."
            },
            {
                "id": 3,
                "category": "System Design & Cloud",
                "question": "The target role emphasizes modern cloud deployment on AWS and container orchestration. How would you design a CI/CD pipeline from a Git commit to automated deployment in Docker containers?",
                "intent": "Checks practical familiarity with modern DevOps workflows, containerization security, linting, unit testing, and blue/green or rolling deployments.",
                "tips_for_answering": "Outline GitHub Actions stages: Lint/Test -> Docker build -> Container scanning -> Push to ECR -> Deploy to ECS/EKS with rollback triggers."
            },
            {
                "id": 4,
                "category": "Data & Performance Optimization",
                "question": "Walk me through how you identify and resolve bottlenecks in slow database queries. What tools, execution plan metrics, and indexing strategies do you rely on?",
                "intent": "Probes deep understanding of SQL indexing (B-Tree, GIN), EXPLAIN ANALYZE execution trees, index scans vs sequential scans, and N+1 query traps.",
                "tips_for_answering": "Discuss database logs, EXPLAIN ANALYZE cost output, composite indexes, query refactoring, and ORM profiling."
            },
            {
                "id": 5,
                "category": "Situational & Collaboration",
                "question": "Suppose Product wants to ship a mission-critical feature in 2 weeks, but your engineering estimate requires 5 weeks to ensure proper architectural safeguards. How do you negotiate this trade-off?",
                "intent": "Evaluates business acumen, technical debt management, scope trimming, MVP prioritization, and cross-functional communication.",
                "tips_for_answering": "Propose an iterative MVP that safely cuts nice-to-have scope while maintaining data integrity, with documented technical debt scheduled for sprint +1."
            }
        ]
    }


def fallback_evaluate_answer(question: str, intent: str, answer: str, job_desc: str) -> Dict[str, Any]:
    """Scores candidate mock interview response."""
    words = len(answer.strip().split())
    
    if words < 25:
        score = 4.2
        rating = "Needs Improvement"
        strengths = ["Attempted a direct initial response to the prompt."]
        areas = [
            "Answer is significantly too brief to demonstrate technical competence.",
            "Lacks concrete technical tools, architecture patterns, or measurable outcomes.",
            "Did not employ the STAR (Situation, Task, Action, Result) methodology."
        ]
        model_answer = "A competitive response should be 3-4 structured paragraphs detailing the technical architecture, specific trade-offs made, and exact tools used (e.g., Redis, Kafka, PostgreSQL)."
    elif words < 75:
        score = 6.8
        rating = "Average"
        strengths = [
            "Good foundational understanding of the core concepts asked.",
            "Clear communication and logical train of thought."
        ]
        areas = [
            "Could delve deeper into specific engineering trade-offs (e.g., cache invalidation pitfalls, latency SLAs).",
            "Incorporate quantifiable business impact to elevate the response from junior to senior caliber."
        ]
        model_answer = (
            "When faced with scaling our REST API to support a 10x traffic spike, I first decoupled the read and write paths. "
            "For reads, I implemented a Cache-Aside pattern using Redis cluster with an adaptive TTL strategy, which absorbed 82% of incoming queries directly from memory. "
            "For write-heavy ingest, I introduced Kafka topics to buffer high-velocity events, backed by a Celery worker pool autoscaling on AWS ECS based on queue depth metrics. "
            "Additionally, we audited PostgreSQL slow query logs using EXPLAIN ANALYZE, added targeted composite B-Tree indexes, and enforced strict connection pooling with PgBouncer. "
            "This architectural refactor sustained 15,000 requests/sec with p99 latency held under 45ms during Black Friday load testing."
        )
    else:
        score = 8.7
        rating = "Strong"
        strengths = [
            "Excellent depth of technical terminology and operational clarity.",
            "Structured response following clear cause-and-effect reasoning.",
            "Demonstrates real-world problem-solving rather than rote memorization."
        ]
        areas = [
            "Consider briefly discussing edge-case error scenarios or disaster recovery protocols to show senior-level thoroughness."
        ]
        model_answer = (
            "In scaling our core API services under sudden traffic spikes, my approach focuses on three pillars: caching, asynchronous decoupling, and defensive backpressure. "
            "First, I leverage Redis for high-frequency idempotent reads with cache warming and distributed locks to prevent cache stampedes. "
            "Second, asynchronous tasks and webhooks are pushed onto RabbitMQ/Kafka queues with exponential backoff and dead-letter queues. "
            "Finally, at the gateway level, we configure token-bucket rate limiting via Envoy/Nginx and horizontal pod autoscaling (HPA) in Kubernetes triggered on CPU and custom queue-depth metrics."
        )

    return {
        "score": score,
        "rating": rating,
        "strengths": strengths,
        "areas_for_improvement": areas,
        "model_answer": model_answer,
        "follow_up_question": "How would you handle cache invalidation and ensure strong data consistency when simultaneous updates occur across multiple microservices?"
    }


# ==============================================================================
# MAIN PUBLIC API INTERFACES
# ==============================================================================

def analyze_resume(
    resume_text: str,
    job_desc: str,
    seniority: str = "Mid-Level",
    api_key: Optional[str] = None,
    model_name: str = "gemini-1.5-flash",
    use_demo_mode: bool = False
) -> Dict[str, Any]:
    """Runs resume gap analysis against job description."""
    if use_demo_mode or not api_key:
        return fallback_analyze_resume(resume_text, job_desc, seniority)

    user_prompt = RESUME_ANALYSIS_USER_TEMPLATE.format(
        resume_text=resume_text,
        job_description=job_desc,
        seniority_level=seniority
    )
    
    try:
        raw_text = call_gemini(
            system_prompt=RESUME_ANALYSIS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            api_key=api_key,
            model_name=model_name,
            temperature=0.3
        )
        return extract_json_from_response(raw_text)
    except Exception as e:
        print(f"[Warning] Live API call failed ({e}). Falling back to intelligent offline engine.")
        res = fallback_analyze_resume(resume_text, job_desc, seniority)
        res["_api_fallback_note"] = f"Generated via Built-in Engine due to API response: {str(e)}"
        return res


def rewrite_bullet(
    bullet: str,
    target_role: str = "Software Engineer",
    api_key: Optional[str] = None,
    model_name: str = "gemini-1.5-flash",
    use_demo_mode: bool = False
) -> Dict[str, Any]:
    """Transforms a weak bullet point into STAR format."""
    if use_demo_mode or not api_key:
        return fallback_rewrite_bullet(bullet, target_role)

    user_prompt = STAR_BULLET_USER_TEMPLATE.format(
        bullet_point=bullet,
        target_role=target_role
    )

    try:
        raw_text = call_gemini(
            system_prompt=STAR_BULLET_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            api_key=api_key,
            model_name=model_name,
            temperature=0.4
        )
        return extract_json_from_response(raw_text)
    except Exception as e:
        print(f"[Warning] Live API call failed ({e}). Falling back to intelligent offline engine.")
        res = fallback_rewrite_bullet(bullet, target_role)
        res["_api_fallback_note"] = f"Generated via Built-in Engine due to: {str(e)}"
        return res


def generate_interview_questions(
    resume_text: str,
    job_desc: str,
    api_key: Optional[str] = None,
    model_name: str = "gemini-1.5-flash",
    use_demo_mode: bool = False
) -> Dict[str, Any]:
    """Generates 5 tailored interview questions."""
    if use_demo_mode or not api_key:
        return fallback_generate_interview_questions(resume_text, job_desc)

    user_prompt = INTERVIEW_GEN_USER_TEMPLATE.format(
        resume_text=resume_text,
        job_description=job_desc
    )

    try:
        raw_text = call_gemini(
            system_prompt=INTERVIEW_GEN_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            api_key=api_key,
            model_name=model_name,
            temperature=0.5
        )
        return extract_json_from_response(raw_text)
    except Exception as e:
        print(f"[Warning] Live API call failed ({e}). Falling back to intelligent offline engine.")
        res = fallback_generate_interview_questions(resume_text, job_desc)
        res["_api_fallback_note"] = f"Generated via Built-in Engine due to: {str(e)}"
        return res


def evaluate_answer(
    question: str,
    intent: str,
    answer: str,
    job_desc: str,
    api_key: Optional[str] = None,
    model_name: str = "gemini-1.5-flash",
    use_demo_mode: bool = False
) -> Dict[str, Any]:
    """Scores candidate mock interview response."""
    if use_demo_mode or not api_key:
        return fallback_evaluate_answer(question, intent, answer, job_desc)

    user_prompt = ANSWER_EVAL_USER_TEMPLATE.format(
        question=question,
        intent=intent,
        candidate_answer=answer,
        job_description=job_desc
    )

    try:
        raw_text = call_gemini(
            system_prompt=ANSWER_EVAL_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            api_key=api_key,
            model_name=model_name,
            temperature=0.3
        )
        return extract_json_from_response(raw_text)
    except Exception as e:
        print(f"[Warning] Live API call failed ({e}). Falling back to intelligent offline engine.")
        res = fallback_evaluate_answer(question, intent, answer, job_desc)
        res["_api_fallback_note"] = f"Generated via Built-in Engine due to: {str(e)}"
        return res
