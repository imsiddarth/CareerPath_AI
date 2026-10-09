"""
CareerCraft AI - Main Streamlit Application
Generative AI Platform for Resume Optimization, ATS Gap Analysis, and Mock Interview Coaching.
"""

import streamlit as st
import json
from typing import Dict, Any

from samples import SAMPLE_DATA
from ai_engine import (
    analyze_resume,
    rewrite_bullet,
    generate_interview_questions,
    evaluate_answer
)

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CareerCraft AI | GenAI Career Preparation Suite",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern card designs, badges, and clean spacing
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(120deg, #2563eb, #7c3aed, #db2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8fafc;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        text-align: center;
    }
    .score-badge-high {
        font-size: 2rem;
        font-weight: 800;
        color: #16a34a;
    }
    .score-badge-med {
        font-size: 2rem;
        font-weight: 800;
        color: #d97706;
    }
    .score-badge-low {
        font-size: 2rem;
        font-weight: 800;
        color: #dc2626;
    }
    .badge-pill-green {
        display: inline-block;
        background: #dcfce7;
        color: #15803d;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 3px;
        border: 1px solid #bbf7d0;
    }
    .badge-pill-red {
        display: inline-block;
        background: #fee2e2;
        color: #b91c1c;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 3px;
        border: 1px solid #fecaca;
    }
    .info-box {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 1rem;
        font-size: 0.95rem;
    }
    .recommendation-box {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "resume_text" not in st.session_state:
    st.session_state.resume_text = SAMPLE_DATA["Full-Stack Software Engineer"]["resume"]
if "job_description" not in st.session_state:
    st.session_state.job_description = SAMPLE_DATA["Full-Stack Software Engineer"]["job_description"]
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = None
if "evaluation_results" not in st.session_state:
    st.session_state.evaluation_results = {}
if "bullet_results" not in st.session_state:
    st.session_state.bullet_results = None


# -----------------------------------------------------------------------------
# SIDEBAR: CONFIGURATION & SAMPLE DATA
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/brain.png", width=64)
    st.title("CareerCraft AI")
    st.caption("GenAI Career Intelligence & Interview Simulator")
    st.divider()

    st.subheader("⚙️ GenAI Engine Settings")
    engine_mode = st.radio(
        "Inference Engine:",
        ["⚡ Demo / Intelligent Local Engine", "🔑 Live Google Gemini API"],
        help="Demo mode uses context-aware simulated intelligence without needing an API key. Live mode connects to Google Gemini models."
    )

    api_key = None
    model_name = "gemini-1.5-flash"
    use_demo = True

    if engine_mode == "🔑 Live Google Gemini API":
        use_demo = False
        api_key = st.text_input("Enter Gemini API Key:", type="password", placeholder="AIzaSy...")
        model_name = st.selectbox(
            "Select Model:",
            ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"],
            index=0
        )
        st.markdown("[Get a free Gemini API Key](https://aistudio.google.com/app/apikey)", unsafe_allow_html=True)
    else:
        st.success("✅ Demo Engine Active (Zero Configuration Required)")

    st.divider()
    st.subheader("📁 Quick Presets")
    selected_preset = st.selectbox(
        "Load Sample Profile:",
        list(SAMPLE_DATA.keys()),
        index=0
    )
    if st.button("📥 Apply Sample Profile", use_container_width=True):
        st.session_state.resume_text = SAMPLE_DATA[selected_preset]["resume"]
        st.session_state.job_description = SAMPLE_DATA[selected_preset]["job_description"]
        st.session_state.analysis_results = None
        st.session_state.interview_questions = None
        st.session_state.evaluation_results = {}
        st.success(f"Loaded '{selected_preset}' profile!")
        st.rerun()

    st.divider()
    st.caption("Developed for Learning Block 1: Generative AI Project Submission")


# -----------------------------------------------------------------------------
# APP HEADER
# -----------------------------------------------------------------------------
st.markdown('<div class="main-header">🎯 CareerCraft AI: GenAI Career Preparation Suite</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated ATS Resume Optimization, Semantic Gap Analysis, and Real-time AI Mock Interview Coaching.</div>', unsafe_allow_html=True)

# Main Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Tab 1: ATS Resume & Gap Analyzer",
    "✍️ Tab 2: STAR Bullet Point Polisher",
    "🎙️ Tab 3: Interactive Mock Interviewer",
    "📊 Tab 4: Career Audit Summary & Export"
])


# =============================================================================
# TAB 1: ATS RESUME & GAP ANALYZER
# =============================================================================
with tab1:
    st.header("📄 Resume & Job Description Gap Analysis")
    st.write("Cross-reference your candidate profile with the target job opening using Generative AI semantic analysis.")

    col_in1, col_in2 = st.columns(2)
    with col_in1:
        st.subheader("1. Candidate Resume")
        uploaded_file = st.file_uploader("Upload Resume (.txt, .md)", type=["txt", "md"])
        if uploaded_file is not None:
            st.session_state.resume_text = uploaded_file.read().decode("utf-8")

        resume_input = st.text_area(
            "Resume Plaintext:",
            value=st.session_state.resume_text,
            height=280,
            key="resume_textarea"
        )
        st.session_state.resume_text = resume_input

    with col_in2:
        st.subheader("2. Target Job Description")
        job_input = st.text_area(
            "Job Posting Details:",
            value=st.session_state.job_description,
            height=320,
            key="job_textarea"
        )
        st.session_state.job_description = job_input

    col_opt1, col_opt2 = st.columns([1, 2])
    with col_opt1:
        seniority = st.selectbox(
            "Target Seniority Level:",
            ["Entry-Level / Intern", "Mid-Level Engineer", "Senior / Lead Engineer", "Staff / Principal"],
            index=1
        )
    with col_opt2:
        st.write("")
        st.write("")
        analyze_btn = st.button("🚀 Run GenAI ATS Gap Analysis", type="primary", use_container_width=True)

    if analyze_btn:
        with st.spinner("🤖 Generative AI is conducting semantic analysis & ATS keyword parsing..."):
            results = analyze_resume(
                resume_text=st.session_state.resume_text,
                job_desc=st.session_state.job_description,
                seniority=seniority,
                api_key=api_key,
                model_name=model_name,
                use_demo_mode=use_demo
            )
            st.session_state.analysis_results = results

    # Display Analysis Results
    if st.session_state.analysis_results:
        res = st.session_state.analysis_results
        st.divider()
        st.subheader("📊 GenAI Evaluation Breakdown")

        score = res.get("overall_score", 70)
        badge_class = "score-badge-high" if score >= 80 else ("score-badge-med" if score >= 60 else "score-badge-low")

        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        with col_m1:
            st.markdown(f"""
            <div class="metric-card">
                <div>Overall ATS Match</div>
                <div class="{badge_class}">{score}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="metric-card">
                <div>Technical Skills</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #2563eb;">
                    {res.get('score_breakdown', {}).get('technical_skills', 75)}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="metric-card">
                <div>Experience Relevance</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #7c3aed;">
                    {res.get('score_breakdown', {}).get('experience_relevance', 70)}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_m4:
            st.markdown(f"""
            <div class="metric-card">
                <div>Soft Skills & Culture</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #0891b2;">
                    {res.get('score_breakdown', {}).get('soft_skills', 80)}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_m5:
            st.markdown(f"""
            <div class="metric-card">
                <div>Education & Certs</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #059669;">
                    {res.get('score_breakdown', {}).get('education_and_certs', 85)}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="info-box" style="margin-top: 1.2rem;">
            <b>Executive Summary:</b> {res.get('summary', 'Analysis completed successfully.')}
        </div>
        """, unsafe_allow_html=True)

        col_k1, col_k2 = st.columns(2)
        with col_k1:
            st.markdown("#### ✅ Matching Target Keywords")
            matched_html = "".join([f'<span class="badge-pill-green">{kw}</span>' for kw in res.get("matching_keywords", [])])
            st.markdown(matched_html or "<em>No direct matches found.</em>", unsafe_allow_html=True)

        with col_k2:
            st.markdown("#### ⚠️ High-Priority Missing Keywords (ATS Gaps)")
            missing_html = "".join([f'<span class="badge-pill-red">{kw}</span>' for kw in res.get("missing_keywords", [])])
            st.markdown(missing_html or "<em>No major gaps detected!</em>", unsafe_allow_html=True)

        st.markdown("---")
        col_sg1, col_sg2 = st.columns(2)
        with col_sg1:
            st.markdown("#### 🌟 Candidate Strengths")
            for item in res.get("strengths", []):
                st.markdown(f"- **{item}**")

        with col_sg2:
            st.markdown("#### 🔍 Critical Gaps & Vulnerabilities")
            for item in res.get("critical_gaps", []):
                st.markdown(f"- ⚠️ {item}")

        st.markdown("#### 🎯 GenAI Actionable Recommendations to Boost Score")
        for rec in res.get("actionable_recommendations", []):
            st.markdown(f"""
            <div class="recommendation-box">
                💡 {rec}
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# TAB 2: STAR BULLET POINT POLISHER
# =============================================================================
with tab2:
    st.header("✍️ GenAI STAR Bullet Point Polisher")
    st.write("Convert generic, passive duty descriptions into high-impact, quantified achievement statements using the STAR (Situation, Task, Action, Result) methodology.")

    sample_bullets = [
        "Worked on python code and fixed bugs in production.",
        "Helped team with marketing campaigns and managed social media posts.",
        "Responsible for writing SQL queries and creating monthly reports."
    ]

    st.markdown("**Try a sample weak bullet:**")
    b_cols = st.columns(3)
    preset_bullet = ""
    for i, b in enumerate(sample_bullets):
        if b_cols[i].button(f"Use Example {i+1}", key=f"ex_btn_{i}", use_container_width=True):
            preset_bullet = b

    input_bullet = st.text_area(
        "Enter your current resume bullet point:",
        value=preset_bullet or "Developed REST APIs in Python using Flask to serve data to frontend dashboards.",
        height=90,
        key="bullet_input_area"
    )

    target_role_context = st.text_input(
        "Target Role / Domain Context:",
        value="Senior Full-Stack Engineer (Python / Cloud)",
        key="target_role_input"
    )

    if st.button("✨ Transform with GenAI", type="primary"):
        with st.spinner("Refactoring using STAR framework and action verbs..."):
            b_results = rewrite_bullet(
                bullet=input_bullet,
                target_role=target_role_context,
                api_key=api_key,
                model_name=model_name,
                use_demo_mode=use_demo
            )
            st.session_state.bullet_results = b_results

    if st.session_state.bullet_results:
        b_res = st.session_state.bullet_results
        st.divider()
        st.markdown(f"**Weakness Identified:** {b_res.get('analysis_of_weakness', '')}")

        st.subheader("🚀 High-Impact STAR Variations")
        revisions = b_res.get("revisions", [])
        
        for rev in revisions:
            style_name = rev.get("style", "Alternative")
            text = rev.get("text", "")
            why = rev.get("why_it_works", "")
            
            with st.container():
                st.markdown(f"""
                <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:16px; margin-bottom:14px; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
                    <div style="font-weight:700; color:#1e293b; font-size:1.05rem; margin-bottom:6px;">
                        📌 Style: <span style="color:#2563eb;">{style_name}</span>
                    </div>
                    <div style="background:#f1f5f9; padding:10px 14px; border-radius:6px; font-family:monospace; font-size:0.95rem; color:#0f172a; margin-bottom:8px;">
                        • {text}
                    </div>
                    <div style="font-size:0.85rem; color:#64748b;">
                        <em>Why this converts:</em> {why}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if b_res.get("suggested_metrics_to_quantify"):
            st.markdown("#### 📈 Recommended Metrics to Quantify in this Bullet:")
            for m in b_res.get("suggested_metrics_to_quantify", []):
                st.markdown(f"- 💡 {m}")


# =============================================================================
# TAB 3: INTERACTIVE AI MOCK INTERVIEWER
# =============================================================================
with tab3:
    st.header("🎙️ Role-Specific AI Mock Interviewer")
    st.write("Prepare for demanding interviews with custom questions generated specifically from your resume and target job requirements.")

    col_q1, col_q2 = st.columns([1, 2])
    with col_q1:
        gen_q_btn = st.button("⚡ Generate 5 Tailored Questions", type="primary", use_container_width=True)

    if gen_q_btn:
        with st.spinner("Formulating role-specific behavioral, technical, and architectural questions..."):
            q_data = generate_interview_questions(
                resume_text=st.session_state.resume_text,
                job_desc=st.session_state.job_description,
                api_key=api_key,
                model_name=model_name,
                use_demo_mode=use_demo
            )
            st.session_state.interview_questions = q_data.get("interview_questions", [])

    if st.session_state.interview_questions:
        q_list = st.session_state.interview_questions
        q_options = [f"Q{q['id']}: [{q.get('category', 'Technical')}] {q['question'][:75]}..." for q in q_list]
        
        selected_idx = st.selectbox(
            "Select an Interview Question to Answer:",
            range(len(q_list)),
            format_func=lambda i: q_options[i]
        )
        
        active_q = q_list[selected_idx]

        st.markdown(f"""
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:10px; padding:18px; margin: 15px 0;">
            <div style="font-size:0.85rem; font-weight:700; color:#6366f1; text-transform:uppercase;">
                Category: {active_q.get('category', 'Technical')}
            </div>
            <div style="font-size:1.2rem; font-weight:700; color:#0f172a; margin: 8px 0;">
                "{active_q.get('question')}"
            </div>
            <div style="font-size:0.9rem; color:#475569; margin-bottom:6px;">
                <b>Interviewer's Evaluation Intent:</b> {active_q.get('intent', '')}
            </div>
            <div style="font-size:0.85rem; color:#059669;">
                <b>💡 Tips for Answering:</b> {active_q.get('tips_for_answering', '')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        user_answer = st.text_area(
            "Your Answer (Type or paste your response):",
            height=160,
            placeholder="Structure your answer using the STAR methodology (Situation, Task, Action, Result) or discuss architecture trade-offs...",
            key=f"ans_input_{selected_idx}"
        )

        col_eval1, col_eval2 = st.columns([1, 2])
        with col_eval1:
            eval_btn = st.button("📝 Submit Answer for GenAI Evaluation", type="primary")

        if eval_btn:
            if not user_answer.strip():
                st.warning("Please type an answer before requesting evaluation.")
            else:
                with st.spinner("🤖 GenAI Senior Hiring Coach is assessing technical depth and structure..."):
                    eval_result = evaluate_answer(
                        question=active_q.get("question"),
                        intent=active_q.get("intent"),
                        answer=user_answer,
                        job_desc=st.session_state.job_description,
                        api_key=api_key,
                        model_name=model_name,
                        use_demo_mode=use_demo
                    )
                    st.session_state.evaluation_results[selected_idx] = eval_result

        # Display answer assessment
        if selected_idx in st.session_state.evaluation_results:
            e_res = st.session_state.evaluation_results[selected_idx]
            st.divider()
            st.subheader("🎯 Coach Evaluation & Feedback")

            e_score = e_res.get("score", 7.0)
            e_rating = e_res.get("rating", "Strong")

            col_es1, col_es2 = st.columns([1, 3])
            with col_es1:
                st.metric(label="Overall Score", value=f"{e_score} / 10", delta=e_rating)
            with col_es2:
                st.markdown(f"**Rating Assessment:** Candidate demonstrated **{e_rating}** communication.")

            col_fb1, col_fb2 = st.columns(2)
            with col_fb1:
                st.markdown("#### 🌟 What Went Well (Strengths)")
                for s in e_res.get("strengths", []):
                    st.markdown(f"- ✅ {s}")
            with col_fb2:
                st.markdown("#### ⚠️ Constructive Feedback")
                for w in e_res.get("areas_for_improvement", []):
                    st.markdown(f"- 🔧 {w}")

            st.markdown("#### 🏆 Exemplary Model Answer (How to Answer Like a Pro):")
            st.info(e_res.get("model_answer", "Model answer not available."))

            if e_res.get("follow_up_question"):
                st.markdown(f"**🔥 Expected Follow-up Question from Interviewer:** *\"{e_res.get('follow_up_question')}\"*")
    else:
        st.info("Click 'Generate 5 Tailored Questions' above to begin your customized mock interview session.")


# =============================================================================
# TAB 4: CAREER AUDIT SUMMARY & EXPORT
# =============================================================================
with tab4:
    st.header("📊 Career Readiness Audit Report")
    st.write("Export your comprehensive GenAI Career Analysis, ATS gap scorecard, and interview preparation kit.")

    if st.session_state.analysis_results is None:
        st.warning("⚠️ Please run the ATS Gap Analysis in Tab 1 first to compile your comprehensive audit report.")
    else:
        res = st.session_state.analysis_results
        
        report_markdown = f"""# CareerCraft AI - Candidate Readiness Audit Report
Generated for: Candidate Profile
Target Seniority: {seniority}

## 1. Executive Summary
{res.get('summary', 'N/A')}

## 2. ATS Match Metrics
- **Overall ATS Score:** {res.get('overall_score', 0)}%
- **Technical Skills Alignment:** {res.get('score_breakdown', {}).get('technical_skills', 0)}%
- **Experience Relevance:** {res.get('score_breakdown', {}).get('experience_relevance', 0)}%
- **Soft Skills / Culture Fit:** {res.get('score_breakdown', {}).get('soft_skills', 0)}%
- **Education & Credentials:** {res.get('score_breakdown', {}).get('education_and_certs', 0)}%

## 3. Keyword Match Analysis
- **Matching Keywords:** {', '.join(res.get('matching_keywords', []))}
- **Missing High-Priority Keywords (Action Required):** {', '.join(res.get('missing_keywords', []))}

## 4. Strengths
"""
        for s in res.get("strengths", []):
            report_markdown += f"- {s}\n"

        report_markdown += "\n## 5. Critical Gaps to Address\n"
        for g in res.get("critical_gaps", []):
            report_markdown += f"- {g}\n"

        report_markdown += "\n## 6. Actionable Improvement Steps\n"
        for rec in res.get("actionable_recommendations", []):
            report_markdown += f"- {rec}\n"

        st.markdown(report_markdown)

        st.download_button(
            label="📥 Download Audit Report (.md)",
            data=report_markdown,
            file_name="CareerCraft_AI_Audit_Report.md",
            mime="text/markdown",
            use_container_width=True
        )
