"""
Pre-packaged sample resumes and job descriptions for rapid testing and demonstrations.
"""

SAMPLE_DATA = {
    "Full-Stack Software Engineer": {
        "resume": """Alex Rivera
Email: alex.rivera@example.com | GitHub: github.com/alexrivera | LinkedIn: linkedin.com/in/alexrivera
San Francisco, CA

SUMMARY:
Passionate Software Engineer with 2 years of experience building web applications using React, Python, and SQL. Interested in backend microservices, cloud deployments, and scalable APIs.

EXPERIENCE:
Junior Software Engineer | TechNova Solutions | June 2023 - Present
- Built user interfaces using React, Redux, and Tailwind CSS.
- Developed REST APIs in Python using Flask to serve data to frontend dashboards.
- Wrote database queries in PostgreSQL and optimized slow queries.
- Participated in weekly agile scrums and sprint planning meetings.
- Fixed customer-reported bugs in production environments.

Software Intern | CloudForge Systems | Jan 2023 - May 2023
- Assisted senior engineers in migrating legacy PHP scripts to Node.js microservices.
- Created unit tests using Jest and Pytest to achieve 70% code coverage.
- Configured basic Docker containers for local development.

EDUCATION:
B.S. in Computer Science | California State University | Graduated May 2023
GPA: 3.6/4.0

SKILLS:
Languages: Python, JavaScript, TypeScript, SQL, HTML/CSS
Frameworks: React, Node.js, Express, Flask
Databases & Tools: PostgreSQL, MongoDB, Git, Docker, Postman
""",
        "job_description": """Senior Full-Stack Engineer (Python / React / AWS)
Company: Apex Cloud Technologies
Location: Remote (US)

Role Overview:
We are looking for a driven Full-Stack Engineer with strong expertise in Python (FastAPI/Django), React/TypeScript, and modern cloud architectures (AWS). You will architect high-throughput microservices, design event-driven architectures using Kafka, and lead frontend modernization.

Key Responsibilities:
- Design, build, and deploy high-performance REST and GraphQL APIs using Python (FastAPI or Django).
- Develop responsive, stateful web frontends using React 18, TypeScript, and Next.js.
- Implement CI/CD pipelines with GitHub Actions and deploy services to AWS (ECS, Lambda, RDS, S3).
- Implement robust distributed caching strategies with Redis and message brokering with Kafka or RabbitMQ.
- Champion engineering best practices: TDD, strict typing, code reviews, and containerization with Docker & Kubernetes.
- Collaborate with Product Managers and UX designers to deliver enterprise features.

Requirements:
- 3+ years professional software development experience.
- Strong proficiency in modern Python and React with TypeScript.
- Hands-on experience with AWS cloud services (ECS/EKS, Lambda, S3, CloudWatch).
- Solid understanding of distributed systems, relational databases (PostgreSQL), and message queues (Kafka/RabbitMQ).
- Experience with container orchestration (Docker, Kubernetes) and CI/CD automation.
"""
    },
    "Data Scientist / ML Engineer": {
        "resume": """Priya Sharma
Email: priya.sharma@example.com | Portfolio: priyasharma.dev
New York, NY

SUMMARY:
Data Scientist with a background in statistics and predictive modeling. Skilled in Python, Scikit-Learn, pandas, and data visualization. Eager to solve business problems with machine learning and NLP.

EXPERIENCE:
Associate Data Analyst | FinMetrics Analytics | July 2023 - Present
- Analyzed customer churn datasets of 250,000+ accounts using Python and pandas.
- Developed logistic regression and random forest classification models achieving 81% precision.
- Built interactive Tableau and Streamlit dashboards for the executive marketing team.
- Extracted and cleaned unstructured financial records using regular expressions and SQL.

Data Science Intern | MedTech Insights | Feb 2023 - June 2023
- Cleaned and prepared electronic health records (EHR) for clinical study analysis.
- Conducted exploratory data analysis (EDA) and hypothesis testing using scipy and statsmodels.
- Documented findings in Jupyter Notebooks and delivered weekly presentations to stakeholders.

EDUCATION:
B.Tech in Information Technology | National Institute of Technology | 2023
Relevant Coursework: Machine Learning, Probability & Statistics, Data Structures

SKILLS:
Languages: Python, R, SQL
ML & Data: Scikit-learn, Pandas, NumPy, XGBoost, Matplotlib, Seaborn
Tools: Git, Tableau, Jupyter, Docker basics
""",
        "job_description": """Machine Learning Engineer - Generative AI & NLP
Company: Synapse Health AI
Location: Hybrid (New York, NY)

About the Job:
We are seeking an ML Engineer to develop, fine-tune, and deploy state-of-the-art LLMs and deep learning models for biomedical NLP. You will bridge research and production, building end-to-end MLOps pipelines.

Responsibilities:
- Train and fine-tune transformer models (Hugging Face, PyTorch) for clinical information extraction and summarization.
- Implement Retrieval-Augmented Generation (RAG) pipelines using vector databases (Pinecone, ChromaDB) and LangChain/LlamaIndex.
- Build robust model evaluation frameworks tracking hallucinations, perplexity, and domain-specific metrics.
- Deploy scalable model inference endpoints on AWS/GCP with Triton Inference Server or FastAPI.
- Manage experiment tracking and model registries using MLflow or Weights & Biases.

Qualifications:
- Solid background in Machine Learning, Deep Learning, and NLP with PyTorch or TensorFlow.
- Experience with modern Generative AI techniques: LLM fine-tuning (LoRA/QLoRA), RAG architecture, vector search.
- Proficiency in Python, Docker, MLOps tooling (MLflow, Docker, CI/CD).
- Familiarity with cloud platforms (AWS/GCP) and production API development.
"""
    },
    "Product Manager": {
        "resume": """Jordan Lee
Email: jordan.lee@example.com | LinkedIn: linkedin.com/in/jordanlee-pm
Austin, TX

SUMMARY:
Associate Product Manager with 2 years of experience leading cross-functional teams to build SaaS products. Adept at user research, backlog prioritization, and agile delivery.

EXPERIENCE:
Associate Product Manager | SaaSFlow Inc. | Aug 2023 - Present
- Managed product roadmap for onboarding experience, improving new-user 30-day retention by 14%.
- Conducted 40+ user interviews to identify UX bottlenecks and feature requests.
- Wrote detailed PRDs, user stories, and acceptance criteria in Jira.
- Coordinated with UX designers and 6 engineers across bi-weekly sprint cycles.

Product Operations Specialist | SaaSFlow Inc. | Jan 2023 - July 2023
- Analyzed product telemetry data in Mixpanel to diagnose drop-off funnels.
- Streamlined bug reporting workflow between Customer Support and Engineering teams.

EDUCATION:
B.S. in Business Administration (Info Systems Minor) | University of Texas at Austin | 2022

SKILLS:
Product Management: User Research, PRD Authoring, Wireframing, Agile/Scrum, Roadmap Strategy
Analytics & Tools: SQL (Intermediate), Mixpanel, Google Analytics, Jira, Figma, Notion
""",
        "job_description": """Senior Technical Product Manager - AI Platform
Company: Nexus Enterprise Cloud
Location: Austin, TX / Remote

The Role:
Nexus is hiring a Senior Technical PM to lead our AI Core platform. You will define the strategy and execution of our enterprise GenAI developer toolkit, empowering thousands of B2B developers to build autonomous AI workflows.

Responsibilities:
- Own the multi-year vision, strategy, and execution for developer-facing GenAI APIs and platform SDKs.
- Partner deeply with AI research scientists and infrastructure engineers to operationalize foundation models.
- Conduct customer discovery with enterprise CTOs and lead architects to identify mission-critical developer pain points.
- Define quantitative success metrics (API latency, developer adoption, API call volume, gross margin).
- Lead go-to-market strategy, documentation, and developer evangelism initiatives.

Requirements:
- 4+ years of product management experience managing technical or developer-facing products (APIs, developer tools, cloud platforms).
- Strong technical comprehension of LLMs, vector search, API design, and distributed cloud computing.
- Proven track record of taking complex developer platforms from 0 to 1.
- Superior cross-functional leadership, data-driven decision-making, and executive stakeholder communication.
"""
    }
}
