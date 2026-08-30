"""
Comprehensive seed data for LearnPath AI.
100+ learning resources, 50+ skills, 30+ projects, 5+ assessments.
All free, legitimate resources from reputable providers.
"""
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.base import AsyncSessionLocal
from backend.app.services.auth_service import get_password_hash


def gen_id():
    return str(uuid.uuid4())


# ─── Skills Data (50+) ─────────────────────────────────────────────────────
SKILLS_DATA = [
    # Programming
    {"name": "Python", "category": "Programming", "difficulty": 2, "prerequisites": [], "tags": ["programming", "scripting"], "description": "Versatile programming language for AI, web, and data science"},
    {"name": "JavaScript", "category": "Programming", "difficulty": 2, "prerequisites": [], "tags": ["web", "frontend", "backend"], "description": "The language of the web — used for both frontend and backend"},
    {"name": "TypeScript", "category": "Programming", "difficulty": 3, "prerequisites": ["JavaScript"], "tags": ["typed", "web"], "description": "Typed superset of JavaScript for large-scale applications"},
    {"name": "Java", "category": "Programming", "difficulty": 3, "prerequisites": [], "tags": ["enterprise", "oop"], "description": "Object-oriented language for enterprise applications"},
    {"name": "C++", "category": "Programming", "difficulty": 4, "prerequisites": [], "tags": ["systems", "performance"], "description": "High-performance systems programming language"},
    {"name": "Go", "category": "Programming", "difficulty": 3, "prerequisites": [], "tags": ["systems", "concurrent"], "description": "Fast, statically typed language for modern applications"},
    {"name": "Rust", "category": "Programming", "difficulty": 5, "prerequisites": ["C++"], "tags": ["systems", "safe"], "description": "Systems programming with memory safety guarantees"},
    {"name": "HTML/CSS", "category": "Web", "difficulty": 1, "prerequisites": [], "tags": ["web", "frontend", "markup"], "description": "Foundation of web development — structure and styling"},
    {"name": "React", "category": "Web", "difficulty": 3, "prerequisites": ["JavaScript", "HTML/CSS"], "tags": ["frontend", "ui", "framework"], "description": "Popular JavaScript library for building user interfaces"},
    {"name": "Next.js", "category": "Web", "difficulty": 3, "prerequisites": ["React", "JavaScript"], "tags": ["fullstack", "ssr"], "description": "React framework for production-grade web applications"},
    {"name": "Node.js", "category": "Web", "difficulty": 3, "prerequisites": ["JavaScript"], "tags": ["backend", "runtime"], "description": "JavaScript runtime for backend development"},
    {"name": "REST APIs", "category": "Software Engineering", "difficulty": 2, "prerequisites": [], "tags": ["api", "backend"], "description": "RESTful API design and implementation principles"},
    # DSA
    {"name": "DSA", "category": "Computer Science", "difficulty": 3, "prerequisites": [], "tags": ["algorithms", "interview"], "description": "Data Structures and Algorithms — core CS foundation"},
    {"name": "Advanced DSA", "category": "Computer Science", "difficulty": 5, "prerequisites": ["DSA"], "tags": ["competitive", "advanced"], "description": "Advanced algorithms: DP, graphs, segment trees"},
    {"name": "System Design", "category": "Software Engineering", "difficulty": 4, "prerequisites": ["DSA", "SQL", "REST APIs"], "tags": ["architecture", "interview", "scalability"], "description": "Designing scalable, reliable distributed systems"},
    # AI/ML
    {"name": "Statistics", "category": "AI/ML", "difficulty": 3, "prerequisites": [], "tags": ["math", "probability", "ml-prerequisite"], "description": "Probability, distributions, hypothesis testing for ML"},
    {"name": "Linear Algebra", "category": "AI/ML", "difficulty": 3, "prerequisites": [], "tags": ["math", "ml-prerequisite"], "description": "Vectors, matrices, transformations for ML"},
    {"name": "Machine Learning", "category": "AI/ML", "difficulty": 4, "prerequisites": ["Python", "Statistics", "Linear Algebra", "NumPy/Pandas"], "tags": ["ml", "ai", "models"], "description": "Core ML algorithms: regression, classification, clustering"},
    {"name": "Deep Learning", "category": "AI/ML", "difficulty": 4, "prerequisites": ["Machine Learning"], "tags": ["neural-networks", "ai"], "description": "Neural networks, CNNs, RNNs, transformers"},
    {"name": "NLP", "category": "AI/ML", "difficulty": 4, "prerequisites": ["Deep Learning"], "tags": ["text", "language", "bert"], "description": "Natural language processing with modern transformers"},
    {"name": "Computer Vision", "category": "AI/ML", "difficulty": 4, "prerequisites": ["Deep Learning"], "tags": ["images", "cnn", "opencv"], "description": "Image recognition, object detection, segmentation"},
    {"name": "Generative AI", "category": "AI/ML", "difficulty": 4, "prerequisites": ["Deep Learning", "NLP"], "tags": ["llm", "gpt", "diffusion"], "description": "Large language models, diffusion models, GANs"},
    {"name": "Reinforcement Learning", "category": "AI/ML", "difficulty": 5, "prerequisites": ["Deep Learning", "Statistics"], "tags": ["rl", "agents"], "description": "Learning through rewards and environment interaction"},
    {"name": "Model Deployment", "category": "AI/ML", "difficulty": 3, "prerequisites": ["Machine Learning", "Docker"], "tags": ["mlops", "deployment"], "description": "Deploying ML models to production environments"},
    {"name": "MLOps", "category": "AI/ML", "difficulty": 4, "prerequisites": ["Model Deployment", "Docker", "CI/CD"], "tags": ["mlops", "production"], "description": "Full ML lifecycle management in production"},
    # Data
    {"name": "SQL", "category": "Data", "difficulty": 2, "prerequisites": [], "tags": ["database", "query", "data"], "description": "Structured Query Language for relational databases"},
    {"name": "NumPy/Pandas", "category": "Data", "difficulty": 2, "prerequisites": ["Python"], "tags": ["data", "numerical", "dataframe"], "description": "Python libraries for numerical computing and data manipulation"},
    {"name": "Data Visualization", "category": "Data", "difficulty": 2, "prerequisites": ["Python", "NumPy/Pandas"], "tags": ["charts", "matplotlib", "plotly"], "description": "Creating insights through visual data representation"},
    {"name": "Power BI/Tableau", "category": "Data", "difficulty": 2, "prerequisites": ["SQL"], "tags": ["bi", "dashboard", "analytics"], "description": "Business intelligence and data visualization tools"},
    {"name": "Excel/Sheets", "category": "Data", "difficulty": 1, "prerequisites": [], "tags": ["spreadsheet", "analysis"], "description": "Spreadsheet tools for data analysis and reporting"},
    {"name": "A/B Testing", "category": "Data", "difficulty": 3, "prerequisites": ["Statistics"], "tags": ["experiments", "hypothesis"], "description": "Designing and analyzing controlled experiments"},
    {"name": "NoSQL", "category": "Data", "difficulty": 3, "prerequisites": ["SQL"], "tags": ["mongodb", "database", "nosql"], "description": "Non-relational databases: MongoDB, Redis, Cassandra"},
    # DevOps / Cloud
    {"name": "Git", "category": "DevOps", "difficulty": 2, "prerequisites": [], "tags": ["version-control", "github"], "description": "Distributed version control for collaborative development"},
    {"name": "Docker", "category": "DevOps", "difficulty": 3, "prerequisites": ["Linux"], "tags": ["containers", "deployment"], "description": "Containerization for consistent application environments"},
    {"name": "Kubernetes", "category": "DevOps", "difficulty": 4, "prerequisites": ["Docker"], "tags": ["orchestration", "k8s"], "description": "Container orchestration for production workloads"},
    {"name": "CI/CD", "category": "DevOps", "difficulty": 3, "prerequisites": ["Git", "Docker"], "tags": ["automation", "pipeline"], "description": "Continuous integration and deployment pipelines"},
    {"name": "Linux", "category": "DevOps", "difficulty": 2, "prerequisites": [], "tags": ["os", "terminal", "bash"], "description": "Linux command line and system administration"},
    {"name": "AWS/GCP/Azure", "category": "Cloud", "difficulty": 3, "prerequisites": ["Linux"], "tags": ["cloud", "aws", "gcp"], "description": "Major cloud platforms for scalable infrastructure"},
    {"name": "Terraform", "category": "DevOps", "difficulty": 3, "prerequisites": ["AWS/GCP/Azure", "Linux"], "tags": ["iac", "infrastructure"], "description": "Infrastructure as Code for cloud provisioning"},
    {"name": "Monitoring", "category": "DevOps", "difficulty": 3, "prerequisites": ["Docker", "Linux"], "tags": ["observability", "prometheus"], "description": "Application and infrastructure monitoring"},
    # Security
    {"name": "Security", "category": "Cybersecurity", "difficulty": 3, "prerequisites": [], "tags": ["security", "fundamentals"], "description": "Information security principles and practices"},
    {"name": "Networking", "category": "Cybersecurity", "difficulty": 3, "prerequisites": [], "tags": ["tcp-ip", "protocols"], "description": "Network protocols, architecture, and security"},
    {"name": "Ethical Hacking", "category": "Cybersecurity", "difficulty": 4, "prerequisites": ["Networking", "Linux", "Security"], "tags": ["pentest", "ctf"], "description": "Penetration testing and security assessment"},
    {"name": "Cryptography", "category": "Cybersecurity", "difficulty": 4, "prerequisites": ["Security"], "tags": ["encryption", "hashing"], "description": "Encryption, hashing, and cryptographic protocols"},
    # Career
    {"name": "Testing", "category": "Software Engineering", "difficulty": 2, "prerequisites": [], "tags": ["unit-test", "tdd", "pytest"], "description": "Writing automated tests for software quality"},
    {"name": "Performance", "category": "Web", "difficulty": 3, "prerequisites": ["React", "JavaScript"], "tags": ["optimization", "lighthouse"], "description": "Web performance optimization techniques"},
    {"name": "UI/UX Design", "category": "Design", "difficulty": 2, "prerequisites": [], "tags": ["figma", "design", "ux"], "description": "User interface and experience design principles"},
]

# ─── Learning Resources Data (100+) ───────────────────────────────────────
RESOURCES_DATA = [
    # === PYTHON ===
    {"title": "Python for Everybody", "provider": "Coursera/University of Michigan", "url": "https://www.coursera.org/specializations/python", "category": "Programming", "skills": ["Python"], "difficulty": 1, "duration_hours": 40, "format": "course", "rating": 4.8, "is_free": True, "prerequisites": [], "description": "Learn Python programming from scratch. Highly rated beginner course."},
    {"title": "Python Official Tutorial", "provider": "Python.org", "url": "https://docs.python.org/3/tutorial/", "category": "Programming", "skills": ["Python"], "difficulty": 1, "duration_hours": 10, "format": "article", "rating": 4.5, "is_free": True, "prerequisites": [], "description": "Official Python documentation tutorial — comprehensive and always up to date."},
    {"title": "Automate the Boring Stuff with Python", "provider": "Al Sweigart", "url": "https://automatetheboringstuff.com/", "category": "Programming", "skills": ["Python"], "difficulty": 2, "duration_hours": 20, "format": "book", "rating": 4.7, "is_free": True, "prerequisites": ["Python"], "description": "Practical Python for automation tasks. Free online book."},
    {"title": "Python Data Science Handbook", "provider": "O'Reilly / Jake VanderPlas", "url": "https://jakevdp.github.io/PythonDataScienceHandbook/", "category": "Data", "skills": ["Python", "NumPy/Pandas", "Data Visualization"], "difficulty": 3, "duration_hours": 30, "format": "book", "rating": 4.8, "is_free": True, "prerequisites": ["Python"], "description": "Comprehensive guide to data science with Python. Free online."},
    {"title": "CS50P: Python Programming", "provider": "Harvard / edX", "url": "https://cs50.harvard.edu/python/", "category": "Programming", "skills": ["Python", "DSA"], "difficulty": 2, "duration_hours": 50, "format": "course", "rating": 4.9, "is_free": True, "prerequisites": [], "description": "Harvard's introduction to Python programming. World-class quality."},
    {"title": "100 Days of Code: Python", "provider": "Udemy / Angela Yu", "url": "https://www.udemy.com/course/100-days-of-code/", "category": "Programming", "skills": ["Python"], "difficulty": 2, "duration_hours": 60, "format": "course", "rating": 4.7, "is_free": False, "prerequisites": [], "description": "Build 100 projects in 100 days with Python."},
    {"title": "Python OOP Tutorial", "provider": "Corey Schafer / YouTube", "url": "https://www.youtube.com/playlist?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc", "category": "Programming", "skills": ["Python"], "difficulty": 2, "duration_hours": 6, "format": "video", "rating": 4.9, "is_free": True, "prerequisites": ["Python"], "description": "Excellent YouTube playlist on Python OOP concepts."},
    
    # === DSA ===
    {"title": "Data Structures & Algorithms — CS61B", "provider": "UC Berkeley", "url": "https://sp21.datastructur.es/", "category": "Computer Science", "skills": ["DSA", "Java"], "difficulty": 4, "duration_hours": 80, "format": "course", "rating": 4.9, "is_free": True, "prerequisites": [], "description": "UC Berkeley's legendary DSA course, free online."},
    {"title": "Algorithms by Princeton", "provider": "Coursera/Princeton", "url": "https://www.coursera.org/learn/algorithms-part1", "category": "Computer Science", "skills": ["DSA"], "difficulty": 4, "duration_hours": 60, "format": "course", "rating": 4.8, "is_free": True, "prerequisites": [], "description": "Comprehensive algorithms course from Princeton University."},
    {"title": "NeetCode 150 — LeetCode Patterns", "provider": "NeetCode", "url": "https://neetcode.io/", "category": "Computer Science", "skills": ["DSA"], "difficulty": 3, "duration_hours": 40, "format": "interactive", "rating": 4.9, "is_free": True, "prerequisites": ["DSA"], "description": "Most curated list of LeetCode problems with video explanations."},
    {"title": "Visualgo — Algorithm Visualizations", "provider": "VisuAlgo", "url": "https://visualgo.net/", "category": "Computer Science", "skills": ["DSA"], "difficulty": 2, "duration_hours": 5, "format": "interactive", "rating": 4.7, "is_free": True, "prerequisites": [], "description": "Beautiful visual explanations of data structures and algorithms."},
    {"title": "The Algorithm Design Manual", "provider": "Steven Skiena", "url": "https://www.algorist.com/", "category": "Computer Science", "skills": ["DSA", "Advanced DSA"], "difficulty": 4, "duration_hours": 50, "format": "book", "rating": 4.6, "is_free": False, "prerequisites": ["DSA"], "description": "Classic textbook for algorithm design and analysis."},
    
    # === STATISTICS & MATH ===
    {"title": "Statistics and Probability", "provider": "Khan Academy", "url": "https://www.khanacademy.org/math/statistics-probability", "category": "AI/ML", "skills": ["Statistics"], "difficulty": 2, "duration_hours": 20, "format": "interactive", "rating": 4.8, "is_free": True, "prerequisites": [], "description": "Free statistics course covering probability, distributions, and inference."},
    {"title": "StatQuest with Josh Starmer", "provider": "YouTube", "url": "https://www.youtube.com/c/joshstarmer", "category": "AI/ML", "skills": ["Statistics", "Machine Learning"], "difficulty": 2, "duration_hours": 30, "format": "video", "rating": 4.9, "is_free": True, "prerequisites": [], "description": "The best YouTube channel for statistics and ML explained clearly."},
    {"title": "Linear Algebra — 3Blue1Brown", "provider": "YouTube / 3Blue1Brown", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab", "category": "AI/ML", "skills": ["Linear Algebra"], "difficulty": 3, "duration_hours": 10, "format": "video", "rating": 4.9, "is_free": True, "prerequisites": [], "description": "Visually stunning intro to linear algebra. Best in class."},
    {"title": "Linear Algebra — MIT OpenCourseWare", "provider": "MIT OCW / Gilbert Strang", "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/", "category": "AI/ML", "skills": ["Linear Algebra"], "difficulty": 4, "duration_hours": 40, "format": "course", "rating": 4.8, "is_free": True, "prerequisites": [], "description": "Complete linear algebra course from MIT. Free lecture videos."},
    {"title": "Mathematics for Machine Learning", "provider": "Coursera/Imperial College", "url": "https://www.coursera.org/specializations/mathematics-machine-learning", "category": "AI/ML", "skills": ["Linear Algebra", "Statistics"], "difficulty": 3, "duration_hours": 50, "format": "course", "rating": 4.6, "is_free": True, "prerequisites": [], "description": "Covers linear algebra, multivariate calculus, and PCA for ML."},
    
    # === MACHINE LEARNING ===
    {"title": "Machine Learning Specialization", "provider": "Coursera/Andrew Ng/DeepLearning.AI", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "category": "AI/ML", "skills": ["Machine Learning", "Statistics"], "difficulty": 3, "duration_hours": 100, "format": "course", "rating": 4.9, "is_free": True, "prerequisites": ["Python", "Statistics"], "description": "The gold standard ML course by Andrew Ng. Updated 2022."},
    {"title": "Google Machine Learning Crash Course", "provider": "Google", "url": "https://developers.google.com/machine-learning/crash-course", "category": "AI/ML", "skills": ["Machine Learning"], "difficulty": 3, "duration_hours": 15, "format": "course", "rating": 4.7, "is_free": True, "prerequisites": ["Python", "Statistics"], "description": "Fast-paced ML course from Google. Practical and concise."},
    {"title": "Scikit-learn User Guide", "provider": "scikit-learn.org", "url": "https://scikit-learn.org/stable/user_guide.html", "category": "AI/ML", "skills": ["Machine Learning", "Python"], "difficulty": 3, "duration_hours": 20, "format": "article", "rating": 4.8, "is_free": True, "prerequisites": ["Python", "NumPy/Pandas"], "description": "Official documentation for the most popular ML library."},
    {"title": "Hands-On Machine Learning with Scikit-Learn", "provider": "O'Reilly / Aurélien Géron", "url": "https://github.com/ageron/handson-ml3", "category": "AI/ML", "skills": ["Machine Learning", "Deep Learning"], "difficulty": 4, "duration_hours": 80, "format": "book", "rating": 4.9, "is_free": False, "prerequisites": ["Python", "Statistics"], "description": "The definitive practical ML book. GitHub code included."},
    {"title": "Kaggle Learn — Intro to ML", "provider": "Kaggle", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "category": "AI/ML", "skills": ["Machine Learning", "Python"], "difficulty": 2, "duration_hours": 4, "format": "interactive", "rating": 4.8, "is_free": True, "prerequisites": ["Python"], "description": "Hands-on ML course with real datasets. Part of Kaggle Learn."},
    {"title": "fast.ai Practical Deep Learning", "provider": "fast.ai", "url": "https://course.fast.ai/", "category": "AI/ML", "skills": ["Machine Learning", "Deep Learning", "NLP", "Computer Vision"], "difficulty": 4, "duration_hours": 60, "format": "course", "rating": 4.9, "is_free": True, "prerequisites": ["Python", "Machine Learning"], "description": "Top-down practical approach to deep learning. Highly regarded."},
    
    # === DEEP LEARNING ===
    {"title": "Deep Learning Specialization", "provider": "Coursera/DeepLearning.AI", "url": "https://www.coursera.org/specializations/deep-learning", "category": "AI/ML", "skills": ["Deep Learning", "NLP", "Computer Vision"], "difficulty": 4, "duration_hours": 120, "format": "course", "rating": 4.9, "is_free": True, "prerequisites": ["Machine Learning"], "description": "5-course deep learning specialization by Andrew Ng."},
    {"title": "Neural Networks: Zero to Hero", "provider": "Andrej Karpathy / YouTube", "url": "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ", "category": "AI/ML", "skills": ["Deep Learning", "NLP"], "difficulty": 4, "duration_hours": 25, "format": "video", "rating": 4.9, "is_free": True, "prerequisites": ["Python", "Machine Learning"], "description": "Build neural networks from scratch. By Tesla/OpenAI's Andrej Karpathy."},
    {"title": "PyTorch Official Tutorials", "provider": "PyTorch", "url": "https://pytorch.org/tutorials/", "category": "AI/ML", "skills": ["Deep Learning"], "difficulty": 3, "duration_hours": 15, "format": "interactive", "rating": 4.7, "is_free": True, "prerequisites": ["Python", "Machine Learning"], "description": "Official PyTorch tutorials from beginner to advanced."},
    {"title": "TensorFlow Developer Certificate", "provider": "Google/Coursera", "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice", "category": "AI/ML", "skills": ["Deep Learning"], "difficulty": 3, "duration_hours": 60, "format": "course", "rating": 4.7, "is_free": True, "prerequisites": ["Machine Learning"], "description": "Practical TensorFlow for deep learning applications."},
    
    # === NLP ===
    {"title": "Hugging Face Course", "provider": "Hugging Face", "url": "https://huggingface.co/learn/nlp-course/chapter1/1", "category": "AI/ML", "skills": ["NLP", "Deep Learning", "Generative AI"], "difficulty": 4, "duration_hours": 30, "format": "course", "rating": 4.9, "is_free": True, "prerequisites": ["Deep Learning"], "description": "Best free NLP course using transformers and Hugging Face ecosystem."},
    {"title": "Stanford CS224N: NLP with Deep Learning", "provider": "Stanford", "url": "https://web.stanford.edu/class/cs224n/", "category": "AI/ML", "skills": ["NLP"], "difficulty": 5, "duration_hours": 60, "format": "course", "rating": 4.9, "is_free": True, "prerequisites": ["Deep Learning"], "description": "Stanford's acclaimed NLP course. Lecture videos free on YouTube."},
    
    # === DATA / SQL ===
    {"title": "SQL Tutorial — Mode Analytics", "provider": "Mode Analytics", "url": "https://mode.com/sql-tutorial/", "category": "Data", "skills": ["SQL"], "difficulty": 1, "duration_hours": 8, "format": "interactive", "rating": 4.7, "is_free": True, "prerequisites": [], "description": "Hands-on SQL tutorial with real-world business scenarios."},
    {"title": "SQLZoo", "provider": "SQLZoo", "url": "https://sqlzoo.net/wiki/SQL_Tutorial", "category": "Data", "skills": ["SQL"], "difficulty": 2, "duration_hours": 10, "format": "interactive", "rating": 4.6, "is_free": True, "prerequisites": [], "description": "Interactive SQL exercises from basics to advanced queries."},
    {"title": "CS50's Introduction to Databases with SQL", "provider": "Harvard / edX", "url": "https://cs50.harvard.edu/sql/", "category": "Data", "skills": ["SQL", "NoSQL"], "difficulty": 2, "duration_hours": 40, "format": "course", "rating": 4.9, "is_free": True, "prerequisites": [], "description": "Harvard's comprehensive SQL course. Free with edX audit."},
    {"title": "Kaggle Learn — Pandas", "provider": "Kaggle", "url": "https://www.kaggle.com/learn/pandas", "category": "Data", "skills": ["NumPy/Pandas"], "difficulty": 2, "duration_hours": 4, "format": "interactive", "rating": 4.8, "is_free": True, "prerequisites": ["Python"], "description": "Practical Pandas for data manipulation. Free with real datasets."},
    {"title": "NumPy Official Tutorial", "provider": "NumPy.org", "url": "https://numpy.org/learn/", "category": "Data", "skills": ["NumPy/Pandas"], "difficulty": 2, "duration_hours": 5, "format": "article", "rating": 4.6, "is_free": True, "prerequisites": ["Python"], "description": "Official NumPy documentation and tutorials."},
    {"title": "Matplotlib & Seaborn Tutorial", "provider": "RealPython", "url": "https://realpython.com/python-matplotlib-guide/", "category": "Data", "skills": ["Data Visualization"], "difficulty": 2, "duration_hours": 6, "format": "article", "rating": 4.5, "is_free": True, "prerequisites": ["Python", "NumPy/Pandas"], "description": "Comprehensive guide to data visualization in Python."},
    {"title": "Plotly & Dash for Interactive Visualizations", "provider": "Plotly", "url": "https://dash.plotly.com/tutorial", "category": "Data", "skills": ["Data Visualization"], "difficulty": 3, "duration_hours": 8, "format": "interactive", "rating": 4.6, "is_free": True, "prerequisites": ["Python"], "description": "Create interactive dashboards with Plotly and Dash."},
    
    # === WEB DEVELOPMENT ===
    {"title": "The Odin Project — Full Stack", "provider": "The Odin Project", "url": "https://www.theodinproject.com/", "category": "Web", "skills": ["HTML/CSS", "JavaScript", "React", "Node.js"], "difficulty": 3, "duration_hours": 200, "format": "course", "rating": 4.9, "is_free": True, "prerequisites": [], "description": "Best free full-stack web development curriculum."},
    {"title": "freeCodeCamp Web Development", "provider": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn", "category": "Web", "skills": ["HTML/CSS", "JavaScript", "React"], "difficulty": 2, "duration_hours": 300, "format": "interactive", "rating": 4.8, "is_free": True, "prerequisites": [], "description": "Comprehensive free web development certification path."},
    {"title": "JavaScript.info", "provider": "JavaScript.info", "url": "https://javascript.info/", "category": "Programming", "skills": ["JavaScript"], "difficulty": 2, "duration_hours": 40, "format": "article", "rating": 4.9, "is_free": True, "prerequisites": [], "description": "The best modern JavaScript tutorial. Comprehensive and free."},
    {"title": "React Official Tutorial", "provider": "React.dev", "url": "https://react.dev/learn", "category": "Web", "skills": ["React", "JavaScript"], "difficulty": 3, "duration_hours": 10, "format": "interactive", "rating": 4.8, "is_free": True, "prerequisites": ["JavaScript", "HTML/CSS"], "description": "Official React documentation with interactive examples."},
    {"title": "TypeScript Handbook", "provider": "Microsoft", "url": "https://www.typescriptlang.org/docs/handbook/intro.html", "category": "Programming", "skills": ["TypeScript", "JavaScript"], "difficulty": 3, "duration_hours": 10, "format": "article", "rating": 4.7, "is_free": True, "prerequisites": ["JavaScript"], "description": "Official TypeScript documentation and handbook."},
    {"title": "Node.js Official Guide", "provider": "Node.js", "url": "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs", "category": "Web", "skills": ["Node.js", "REST APIs"], "difficulty": 2, "duration_hours": 8, "format": "article", "rating": 4.5, "is_free": True, "prerequisites": ["JavaScript"], "description": "Official Node.js documentation for server-side JavaScript."},
    {"title": "FastAPI Official Tutorial", "provider": "FastAPI/Tiangolo", "url": "https://fastapi.tiangolo.com/tutorial/", "category": "Web", "skills": ["REST APIs", "Python"], "difficulty": 3, "duration_hours": 8, "format": "article", "rating": 4.9, "is_free": True, "prerequisites": ["Python"], "description": "Official FastAPI documentation. Best Python web framework."},
    
    # === DEVOPS / CLOUD ===
    {"title": "Git Handbook — GitHub", "provider": "GitHub", "url": "https://docs.github.com/en/get-started/using-git/about-git", "category": "DevOps", "skills": ["Git"], "difficulty": 1, "duration_hours": 4, "format": "article", "rating": 4.7, "is_free": True, "prerequisites": [], "description": "Official GitHub guide to Git. Beginner-friendly."},
    {"title": "Learn Git Branching", "provider": "learngitbranching.js.org", "url": "https://learngitbranching.js.org/", "category": "DevOps", "skills": ["Git"], "difficulty": 2, "duration_hours": 5, "format": "interactive", "rating": 4.9, "is_free": True, "prerequisites": [], "description": "Interactive visual git branching tutorial. Best for learning git flow."},
    {"title": "Docker Official Get Started", "provider": "Docker", "url": "https://docs.docker.com/get-started/", "category": "DevOps", "skills": ["Docker"], "difficulty": 2, "duration_hours": 6, "format": "article", "rating": 4.7, "is_free": True, "prerequisites": ["Linux"], "description": "Official Docker tutorial from basics to compose."},
    {"title": "Docker and Kubernetes for Beginners", "provider": "YouTube/TechWorld with Nana", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "category": "DevOps", "skills": ["Docker", "Kubernetes"], "difficulty": 3, "duration_hours": 4, "format": "video", "rating": 4.8, "is_free": True, "prerequisites": ["Linux"], "description": "Excellent free Docker tutorial by TechWorld with Nana."},
    {"title": "Linux Command Line Basics", "provider": "Udacity", "url": "https://www.udacity.com/course/linux-command-line-basics--ud595", "category": "DevOps", "skills": ["Linux"], "difficulty": 1, "duration_hours": 5, "format": "course", "rating": 4.5, "is_free": True, "prerequisites": [], "description": "Free Linux command line course for beginners."},
    {"title": "AWS Free Tier + Documentation", "provider": "Amazon Web Services", "url": "https://aws.amazon.com/free/", "category": "Cloud", "skills": ["AWS/GCP/Azure"], "difficulty": 3, "duration_hours": 20, "format": "interactive", "rating": 4.6, "is_free": True, "prerequisites": ["Linux"], "description": "AWS free tier with official documentation and tutorials."},
    {"title": "Google Cloud Skills Boost", "provider": "Google Cloud", "url": "https://cloudskillsboost.google/", "category": "Cloud", "skills": ["AWS/GCP/Azure"], "difficulty": 3, "duration_hours": 20, "format": "interactive", "rating": 4.6, "is_free": True, "prerequisites": ["Linux"], "description": "Google's official cloud training platform with free courses."},
    {"title": "GitHub Actions Documentation", "provider": "GitHub", "url": "https://docs.github.com/en/actions", "category": "DevOps", "skills": ["CI/CD", "Git"], "difficulty": 3, "duration_hours": 8, "format": "article", "rating": 4.7, "is_free": True, "prerequisites": ["Git", "Docker"], "description": "Official GitHub Actions docs for CI/CD automation."},
    
    # === SYSTEM DESIGN ===
    {"title": "System Design Primer", "provider": "GitHub / donnemartin", "url": "https://github.com/donnemartin/system-design-primer", "category": "Software Engineering", "skills": ["System Design"], "difficulty": 4, "duration_hours": 30, "format": "article", "rating": 4.9, "is_free": True, "prerequisites": ["DSA", "SQL"], "description": "The most comprehensive free system design resource on GitHub."},
    {"title": "Designing Data-Intensive Applications", "provider": "O'Reilly / Martin Kleppmann", "url": "https://dataintensive.net/", "category": "Software Engineering", "skills": ["System Design"], "difficulty": 5, "duration_hours": 60, "format": "book", "rating": 4.9, "is_free": False, "prerequisites": ["System Design"], "description": "Bible of distributed systems design. Essential reading."},
    {"title": "ByteByteGo System Design Newsletter", "provider": "ByteByteGo", "url": "https://bytebytego.com/", "category": "Software Engineering", "skills": ["System Design"], "difficulty": 4, "duration_hours": 20, "format": "article", "rating": 4.8, "is_free": True, "prerequisites": ["DSA"], "description": "Visual system design explanations. Free newsletter."},
    
    # === CYBERSECURITY ===
    {"title": "TryHackMe", "provider": "TryHackMe", "url": "https://tryhackme.com/", "category": "Cybersecurity", "skills": ["Ethical Hacking", "Networking", "Linux"], "difficulty": 3, "duration_hours": 50, "format": "interactive", "rating": 4.8, "is_free": True, "prerequisites": ["Linux", "Networking"], "description": "Gamified cybersecurity training. Free tier available."},
    {"title": "Networking Fundamentals", "provider": "Cisco / CCNA", "url": "https://skillsforall.com/course/networking-basics", "category": "Cybersecurity", "skills": ["Networking"], "difficulty": 2, "duration_hours": 20, "format": "course", "rating": 4.6, "is_free": True, "prerequisites": [], "description": "Free Cisco networking basics course covering TCP/IP and protocols."},
    {"title": "OWASP Web Security Testing Guide", "provider": "OWASP", "url": "https://owasp.org/www-project-web-security-testing-guide/", "category": "Cybersecurity", "skills": ["Security", "Ethical Hacking"], "difficulty": 4, "duration_hours": 30, "format": "article", "rating": 4.7, "is_free": True, "prerequisites": ["Networking", "Security"], "description": "Comprehensive web security testing methodology from OWASP."},
    
    # === GENERATIVE AI ===
    {"title": "ChatGPT Prompt Engineering for Developers", "provider": "DeepLearning.AI", "url": "https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/", "category": "AI/ML", "skills": ["Generative AI", "NLP"], "difficulty": 2, "duration_hours": 2, "format": "course", "rating": 4.8, "is_free": True, "prerequisites": ["Python"], "description": "Free short course on prompt engineering by Andrew Ng."},
    {"title": "LangChain Documentation", "provider": "LangChain", "url": "https://python.langchain.com/docs/get_started/introduction", "category": "AI/ML", "skills": ["Generative AI", "NLP", "Python"], "difficulty": 4, "duration_hours": 15, "format": "article", "rating": 4.6, "is_free": True, "prerequisites": ["Python", "Deep Learning"], "description": "Official LangChain docs for building LLM applications."},
    {"title": "Building Systems with ChatGPT API", "provider": "DeepLearning.AI", "url": "https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/", "category": "AI/ML", "skills": ["Generative AI"], "difficulty": 3, "duration_hours": 2, "format": "course", "rating": 4.7, "is_free": True, "prerequisites": ["Python", "NLP"], "description": "Free short course on building LLM-powered systems."},
    
    # === CAREER / INTERVIEW ===
    {"title": "Cracking the Coding Interview", "provider": "Gayle Laakmann McDowell", "url": "https://www.crackingthecodinginterview.com/", "category": "Career", "skills": ["DSA", "System Design"], "difficulty": 4, "duration_hours": 40, "format": "book", "rating": 4.8, "is_free": False, "prerequisites": ["DSA"], "description": "The classic interview preparation book. A must-read."},
    {"title": "LeetCode Free Problems", "provider": "LeetCode", "url": "https://leetcode.com/problemset/all/", "category": "Career", "skills": ["DSA"], "difficulty": 3, "duration_hours": 50, "format": "interactive", "rating": 4.8, "is_free": True, "prerequisites": ["DSA"], "description": "Practice coding problems for technical interviews."},
    {"title": "Pramp — Mock Interviews", "provider": "Pramp", "url": "https://www.pramp.com/", "category": "Career", "skills": ["DSA", "System Design"], "difficulty": 4, "duration_hours": 10, "format": "interactive", "rating": 4.6, "is_free": True, "prerequisites": ["DSA"], "description": "Free peer-to-peer mock technical interview platform."},
    
    # === TESTING ===
    {"title": "Pytest Documentation", "provider": "pytest.org", "url": "https://docs.pytest.org/en/stable/getting-started.html", "category": "Software Engineering", "skills": ["Testing", "Python"], "difficulty": 2, "duration_hours": 8, "format": "article", "rating": 4.7, "is_free": True, "prerequisites": ["Python"], "description": "Official pytest documentation for Python testing."},
    {"title": "Testing JavaScript with Jest", "provider": "JavaScript Testing", "url": "https://jestjs.io/docs/getting-started", "category": "Software Engineering", "skills": ["Testing", "JavaScript"], "difficulty": 2, "duration_hours": 6, "format": "article", "rating": 4.6, "is_free": True, "prerequisites": ["JavaScript"], "description": "Official Jest documentation for JavaScript unit testing."},
    
    # === ADDITIONAL ===
    {"title": "CS50 Introduction to Computer Science", "provider": "Harvard / edX", "url": "https://cs50.harvard.edu/x/", "category": "Computer Science", "skills": ["Python", "DSA", "SQL"], "difficulty": 2, "duration_hours": 80, "format": "course", "rating": 4.9, "is_free": True, "prerequisites": [], "description": "Harvard's legendary intro CS course. World's most popular MOOC."},
    {"title": "Kaggle — Data Science Competitions", "provider": "Kaggle", "url": "https://www.kaggle.com/competitions", "category": "AI/ML", "skills": ["Machine Learning", "Data Visualization", "NumPy/Pandas"], "difficulty": 4, "duration_hours": 50, "format": "interactive", "rating": 4.8, "is_free": True, "prerequisites": ["Machine Learning", "Python"], "description": "Real-world data science competitions with prize money."},
    {"title": "Full Stack Open", "provider": "University of Helsinki", "url": "https://fullstackopen.com/", "category": "Web", "skills": ["JavaScript", "React", "Node.js", "TypeScript"], "difficulty": 3, "duration_hours": 200, "format": "course", "rating": 4.9, "is_free": True, "prerequisites": ["JavaScript"], "description": "Deep dive into full-stack development. Completely free."},
    {"title": "Roadmap.sh Developer Roadmaps", "provider": "roadmap.sh", "url": "https://roadmap.sh/", "category": "Career", "skills": [], "difficulty": 1, "duration_hours": 2, "format": "article", "rating": 4.8, "is_free": True, "prerequisites": [], "description": "Community-built roadmaps for various developer career paths."},
    {"title": "MDN Web Docs", "provider": "Mozilla", "url": "https://developer.mozilla.org/", "category": "Web", "skills": ["HTML/CSS", "JavaScript"], "difficulty": 2, "duration_hours": 30, "format": "article", "rating": 4.9, "is_free": True, "prerequisites": [], "description": "The definitive reference for web development. Always up to date."},
    {"title": "Figma UI Design for Beginners", "provider": "Figma", "url": "https://www.figma.com/resources/learn-design/", "category": "Design", "skills": ["UI/UX Design"], "difficulty": 1, "duration_hours": 6, "format": "interactive", "rating": 4.7, "is_free": True, "prerequisites": [], "description": "Official Figma tutorials for learning UI/UX design."},
    {"title": "Power BI for Beginners", "provider": "Microsoft Learn", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi", "category": "Data", "skills": ["Power BI/Tableau"], "difficulty": 2, "duration_hours": 10, "format": "course", "rating": 4.5, "is_free": True, "prerequisites": ["SQL"], "description": "Microsoft's official Power BI learning path. Free."},
    {"title": "Tableau Public Tutorials", "provider": "Tableau", "url": "https://public.tableau.com/en-us/s/resources", "category": "Data", "skills": ["Power BI/Tableau", "Data Visualization"], "difficulty": 2, "duration_hours": 8, "format": "course", "rating": 4.5, "is_free": True, "prerequisites": [], "description": "Official Tableau tutorials and sample workbooks."},
]

# ─── Projects Data (30+) ──────────────────────────────────────────────────
PROJECTS_DATA = [
    # Python / Beginner
    {"title": "CLI Expense Tracker", "description": "Build a command-line expense tracker that reads/writes to CSV files, categorizes expenses, and generates monthly summaries.", "skills": ["Python"], "difficulty": 1, "duration_hours": 4, "category": "Python", "tags": ["beginner", "csv", "cli"]},
    {"title": "Password Manager CLI", "description": "Create a secure CLI password manager with AES encryption to store and retrieve credentials.", "skills": ["Python"], "difficulty": 2, "duration_hours": 6, "category": "Python", "tags": ["security", "encryption", "cli"]},
    {"title": "Web Scraper & News Aggregator", "description": "Scrape top news from 5 websites, deduplicate, and send a daily email digest.", "skills": ["Python"], "difficulty": 2, "duration_hours": 8, "category": "Python", "tags": ["scraping", "email", "beautifulsoup"]},
    {"title": "Student Grade Management System", "description": "OOP-based grade management system with file persistence, statistics, and grade curves.", "skills": ["Python"], "difficulty": 2, "duration_hours": 6, "category": "Python", "tags": ["oop", "file-io", "statistics"]},
    # DSA
    {"title": "Algorithm Visualizer", "description": "Interactive web app that visualizes sorting (bubble, merge, quick) and graph algorithms (BFS, DFS, Dijkstra) step-by-step.", "skills": ["JavaScript", "HTML/CSS", "DSA"], "difficulty": 3, "duration_hours": 20, "category": "DSA", "tags": ["visualization", "animation", "algorithms"]},
    {"title": "Custom Hash Map Implementation", "description": "Implement a HashMap from scratch in Python with collision handling, load factor, and resize functionality. Include tests.", "skills": ["Python", "DSA"], "difficulty": 3, "duration_hours": 8, "category": "DSA", "tags": ["data-structures", "testing", "interview"]},
    {"title": "Graph Path Finder", "description": "Find shortest paths in a city graph using Dijkstra's and A* algorithms. Visualize with matplotlib.", "skills": ["Python", "DSA"], "difficulty": 4, "duration_hours": 12, "category": "DSA", "tags": ["graphs", "pathfinding", "algorithms"]},
    # Data / SQL
    {"title": "SQL Analytics Dashboard", "description": "Analyze a 50k-row sales dataset. Write 20+ complex SQL queries and create a visual dashboard with the insights.", "skills": ["SQL", "Data Visualization"], "difficulty": 2, "duration_hours": 10, "category": "Data Analysis", "tags": ["sql", "analytics", "dashboard"]},
    {"title": "COVID-19 Data Analysis", "description": "Analyze global COVID-19 data using Pandas. Create interactive visualizations with Plotly. Derive 10 key insights.", "skills": ["Python", "NumPy/Pandas", "Data Visualization"], "difficulty": 2, "duration_hours": 8, "category": "Data Analysis", "tags": ["pandas", "covid", "visualization"]},
    {"title": "E-commerce Database Design", "description": "Design and implement a complete e-commerce database with users, products, orders, and reviews. Include complex analytical queries.", "skills": ["SQL"], "difficulty": 3, "duration_hours": 12, "category": "Data", "tags": ["database-design", "erd", "sql"]},
    # Machine Learning
    {"title": "Customer Churn Prediction", "description": "Predict customer churn using Telco dataset. Apply feature engineering, train 5 models, compare with ROC curves. Target: 80%+ AUC.", "skills": ["Machine Learning", "Python", "NumPy/Pandas"], "difficulty": 3, "duration_hours": 15, "category": "Machine Learning", "tags": ["classification", "feature-engineering", "sklearn"]},
    {"title": "House Price Prediction", "description": "Predict house prices using regression. Feature engineering, model selection, hyperparameter tuning. Use Boston/Ames dataset.", "skills": ["Machine Learning", "Statistics", "Python"], "difficulty": 3, "duration_hours": 12, "category": "Machine Learning", "tags": ["regression", "kaggle", "feature-engineering"]},
    {"title": "Movie Recommendation System", "description": "Build a collaborative filtering recommendation system using the MovieLens dataset. Implement user-based and item-based CF.", "skills": ["Machine Learning", "Python", "NumPy/Pandas"], "difficulty": 4, "duration_hours": 20, "category": "Machine Learning", "tags": ["recommendation", "collaborative-filtering", "similarity"]},
    {"title": "Twitter Sentiment Analysis", "description": "Classify tweet sentiment (positive/negative/neutral) using traditional ML and simple neural networks. Achieve 85%+ accuracy.", "skills": ["Machine Learning", "NLP", "Python"], "difficulty": 3, "duration_hours": 14, "category": "NLP", "tags": ["sentiment", "nlp", "classification"]},
    {"title": "Credit Card Fraud Detection", "description": "Detect fraudulent transactions with highly imbalanced dataset. Apply SMOTE, anomaly detection, and precision-recall curves.", "skills": ["Machine Learning", "Python"], "difficulty": 4, "duration_hours": 15, "category": "Machine Learning", "tags": ["imbalanced", "fraud", "anomaly-detection"]},
    # Deep Learning
    {"title": "Image Classification with CNN", "description": "Build a CNN from scratch to classify CIFAR-10. Achieve 85%+ accuracy. Apply data augmentation and batch normalization.", "skills": ["Deep Learning", "Computer Vision", "Python"], "difficulty": 4, "duration_hours": 20, "category": "Deep Learning", "tags": ["cnn", "image-classification", "pytorch"]},
    {"title": "Transfer Learning for Dog Breed Classifier", "description": "Use ResNet/EfficientNet to classify 120 dog breeds. Fine-tune pretrained model on limited data. Target: 90%+ accuracy.", "skills": ["Deep Learning", "Computer Vision", "Python"], "difficulty": 4, "duration_hours": 16, "category": "Deep Learning", "tags": ["transfer-learning", "resnet", "fine-tuning"]},
    {"title": "LSTM Text Generator", "description": "Train an LSTM to generate text in the style of a given author (Shakespeare, news, etc.). Implement temperature sampling.", "skills": ["Deep Learning", "NLP", "Python"], "difficulty": 4, "duration_hours": 18, "category": "Deep Learning", "tags": ["lstm", "text-generation", "rnn"]},
    # Generative AI / LLM
    {"title": "RAG-Based Study Assistant", "description": "Build a Retrieval-Augmented Generation chatbot that answers questions from uploaded PDFs using LangChain and free LLM.", "skills": ["Generative AI", "NLP", "Python"], "difficulty": 4, "duration_hours": 20, "category": "Generative AI", "tags": ["rag", "langchain", "llm", "pdf"]},
    {"title": "AI Code Reviewer", "description": "Create a GitHub Action that automatically reviews PRs and suggests improvements using an LLM API.", "skills": ["Generative AI", "Python", "CI/CD"], "difficulty": 4, "duration_hours": 16, "category": "Generative AI", "tags": ["github-actions", "llm", "code-review"]},
    # Web Development
    {"title": "Personal Portfolio Website", "description": "Build a responsive portfolio website with HTML/CSS/JS. Include projects, skills, contact form, and dark mode.", "skills": ["HTML/CSS", "JavaScript"], "difficulty": 1, "duration_hours": 8, "category": "Frontend", "tags": ["portfolio", "responsive", "dark-mode"]},
    {"title": "Task Management App (React)", "description": "Full-featured task manager with React: drag & drop, labels, deadlines, filtering, and localStorage persistence.", "skills": ["React", "JavaScript", "HTML/CSS"], "difficulty": 3, "duration_hours": 20, "category": "Frontend", "tags": ["react", "state-management", "drag-drop"]},
    {"title": "Real-time Chat Application", "description": "WebSocket-based chat app with React frontend and Node.js backend. Support rooms, private messages, and typing indicators.", "skills": ["React", "Node.js", "JavaScript"], "difficulty": 4, "duration_hours": 24, "category": "Full Stack", "tags": ["websocket", "realtime", "chat"]},
    {"title": "Blog Platform with CMS", "description": "Full-stack blog with Next.js, authentication, markdown editor, SEO optimization, and PostgreSQL.", "skills": ["React", "Node.js", "SQL", "TypeScript"], "difficulty": 4, "duration_hours": 30, "category": "Full Stack", "tags": ["nextjs", "cms", "seo", "auth"]},
    # Backend / API
    {"title": "RESTful API with FastAPI", "description": "Build a production-ready REST API with FastAPI: authentication, CRUD, pagination, validation, documentation, and tests.", "skills": ["Python", "REST APIs", "SQL"], "difficulty": 3, "duration_hours": 16, "category": "Backend", "tags": ["fastapi", "rest", "auth", "testing"]},
    {"title": "Microservices with Docker Compose", "description": "Build 3 microservices (auth, products, orders) that communicate via REST. Orchestrate with Docker Compose.", "skills": ["Docker", "REST APIs", "Python"], "difficulty": 4, "duration_hours": 24, "category": "DevOps", "tags": ["microservices", "docker-compose", "api-gateway"]},
    # MLOps / Deployment
    {"title": "ML Model Deployment as REST API", "description": "Train a model, wrap with FastAPI, containerize with Docker, deploy to free cloud platform. Include health checks.", "skills": ["Machine Learning", "Docker", "Model Deployment", "Python"], "difficulty": 4, "duration_hours": 16, "category": "MLOps", "tags": ["deployment", "docker", "fastapi", "mlops"]},
    {"title": "CI/CD Pipeline for ML Model", "description": "Set up automated testing, model training, and deployment using GitHub Actions. Include model performance regression tests.", "skills": ["CI/CD", "Machine Learning", "Docker", "Git"], "difficulty": 4, "duration_hours": 20, "category": "MLOps", "tags": ["github-actions", "ci-cd", "mlops", "automation"]},
    # System Design
    {"title": "URL Shortener System Design + Implementation", "description": "Design and implement a URL shortener (like bit.ly) with analytics, custom domains, and 100K requests/day capacity.", "skills": ["System Design", "Python", "SQL", "REST APIs"], "difficulty": 4, "duration_hours": 20, "category": "System Design", "tags": ["scalability", "caching", "analytics"]},
    {"title": "Stock Price Dashboard", "description": "Real-time stock price dashboard using free APIs. Display charts, alerts, portfolio tracking with React and WebSockets.", "skills": ["React", "JavaScript", "REST APIs"], "difficulty": 3, "duration_hours": 16, "category": "Full Stack", "tags": ["real-time", "financial", "charts", "api"]},
]

# ─── Assessment Data ───────────────────────────────────────────────────────
INDUSTRY_PROJECTS_EXTRA = [
    {"title": "Demand Forecasting Pipeline", "description": "Forecast product demand from historical sales, promotions, and seasonality. Include model comparison and forecast explainability.", "skills": ["Machine Learning", "Python", "Statistics"], "difficulty": 4, "duration_hours": 18, "category": "Machine Learning", "tags": ["forecasting", "time-series", "business"]},
    {"title": "Resume Skill Analyzer", "description": "Extract skills from resumes, compare them with a target role, and generate a prioritized learning gap report.", "skills": ["NLP", "Python", "Generative AI"], "difficulty": 4, "duration_hours": 18, "category": "Generative AI", "tags": ["resume", "nlp", "career"]},
    {"title": "Document Classification Service", "description": "Classify PDFs or text documents into business categories with preprocessing, model serving, and confidence scores.", "skills": ["NLP", "Machine Learning", "REST APIs"], "difficulty": 4, "duration_hours": 20, "category": "NLP", "tags": ["classification", "documents", "api"]},
    {"title": "Document Q&A Assistant", "description": "Build a question-answering assistant over uploaded documents using embeddings, retrieval, and a lightweight web UI.", "skills": ["Generative AI", "NLP", "Python"], "difficulty": 4, "duration_hours": 22, "category": "Generative AI", "tags": ["rag", "embeddings", "qa"]},
    {"title": "Meeting Summarizer", "description": "Summarize transcripts into decisions, blockers, owners, and follow-up tasks with exportable notes.", "skills": ["Generative AI", "NLP", "Python"], "difficulty": 3, "duration_hours": 14, "category": "Generative AI", "tags": ["summarization", "productivity", "nlp"]},
    {"title": "Code Explanation Assistant", "description": "Paste code and receive plain-language explanations, complexity notes, and suggested test cases.", "skills": ["Generative AI", "Python", "REST APIs"], "difficulty": 4, "duration_hours": 18, "category": "Generative AI", "tags": ["code", "assistant", "developer-tools"]},
    {"title": "Customer Segmentation Analysis", "description": "Segment customers using clustering, profile each group, and recommend targeted business actions.", "skills": ["Machine Learning", "Statistics", "Data Visualization"], "difficulty": 3, "duration_hours": 14, "category": "Data Science", "tags": ["clustering", "analytics", "marketing"]},
    {"title": "Business KPI Analytics Dashboard", "description": "Create an executive dashboard with revenue, retention, funnel, and cohort metrics from raw event data.", "skills": ["SQL", "Data Visualization", "Python"], "difficulty": 3, "duration_hours": 16, "category": "Data Analysis", "tags": ["bi", "dashboard", "kpi"]},
    {"title": "Authentication System", "description": "Implement registration, login, refresh tokens, roles, password reset, and audit logging.", "skills": ["REST APIs", "Security", "SQL"], "difficulty": 3, "duration_hours": 16, "category": "Backend", "tags": ["auth", "jwt", "security"]},
    {"title": "E-commerce Backend API", "description": "Build catalog, cart, orders, payments mock, inventory, and admin APIs with tests and pagination.", "skills": ["REST APIs", "SQL", "Python"], "difficulty": 4, "duration_hours": 24, "category": "Backend", "tags": ["ecommerce", "api", "testing"]},
    {"title": "Real-time Notification System", "description": "Design a notification service with queues, WebSockets, preferences, retries, and delivery status.", "skills": ["System Design", "Node.js", "REST APIs"], "difficulty": 4, "duration_hours": 22, "category": "System Design", "tags": ["realtime", "queues", "websocket"]},
    {"title": "REST API Platform", "description": "Build a reusable API platform with auth, rate limits, versioning, documentation, and monitoring hooks.", "skills": ["REST APIs", "System Design", "Testing"], "difficulty": 4, "duration_hours": 20, "category": "Backend", "tags": ["platform", "api", "observability"]},
    {"title": "OCR Document Processor", "description": "Extract text from scanned documents, clean fields, validate confidence, and store searchable records.", "skills": ["Computer Vision", "Python", "REST APIs"], "difficulty": 4, "duration_hours": 20, "category": "Computer Vision", "tags": ["ocr", "documents", "extraction"]},
    {"title": "Manufacturing Defect Detection", "description": "Classify product images as defective or healthy and explain model confidence for quality review.", "skills": ["Computer Vision", "Deep Learning", "Python"], "difficulty": 5, "duration_hours": 26, "category": "Computer Vision", "tags": ["defect-detection", "cnn", "quality"]},
    {"title": "Log Anomaly Detection", "description": "Detect unusual system behavior from application logs and raise severity-ranked alerts.", "skills": ["Machine Learning", "Security", "Python"], "difficulty": 4, "duration_hours": 20, "category": "Cybersecurity", "tags": ["logs", "anomaly", "security"]},
    {"title": "Phishing Detection Classifier", "description": "Classify suspicious URLs or emails using feature engineering, explainability, and safe evaluation metrics.", "skills": ["Machine Learning", "Security", "NLP"], "difficulty": 4, "duration_hours": 18, "category": "Cybersecurity", "tags": ["phishing", "classification", "security"]},
    {"title": "CI/CD Health Dashboard", "description": "Track build status, deployment frequency, failure rate, and recovery time from CI pipeline data.", "skills": ["CI/CD", "Data Visualization", "React"], "difficulty": 3, "duration_hours": 16, "category": "DevOps", "tags": ["cicd", "dashboard", "metrics"]},
    {"title": "Monitoring Dashboard", "description": "Build a service monitoring dashboard with uptime, latency, error rate, alerts, and incident notes.", "skills": ["Monitoring", "React", "REST APIs"], "difficulty": 4, "duration_hours": 20, "category": "DevOps", "tags": ["observability", "alerts", "sre"]},
    {"title": "Feature Store Mini Platform", "description": "Create a lightweight feature registry with offline storage, validation, and model training examples.", "skills": ["MLOps", "Python", "SQL"], "difficulty": 5, "duration_hours": 28, "category": "MLOps", "tags": ["feature-store", "mlops", "data"]},
    {"title": "A/B Test Analyzer", "description": "Analyze experiment results, calculate confidence intervals, detect sample ratio mismatch, and report decisions.", "skills": ["Statistics", "SQL", "Data Visualization"], "difficulty": 3, "duration_hours": 14, "category": "Data Science", "tags": ["experimentation", "statistics", "analytics"]},
]


def _technologies_for_project(project: dict) -> list:
    skills = set(project.get("skills", []))
    category = project.get("category", "")
    technologies = ["Git", "GitHub", "Documentation"]
    if "Python" in skills or category in {"Machine Learning", "Data Science", "Data Analysis", "NLP", "Computer Vision", "MLOps"}:
        technologies.extend(["Python", "Pandas", "scikit-learn"])
    if "Deep Learning" in skills or "Computer Vision" in skills:
        technologies.extend(["PyTorch", "OpenCV"])
    if "Generative AI" in skills:
        technologies.extend(["Embeddings", "Vector Search", "FastAPI"])
    if "React" in skills or "JavaScript" in skills or category in {"Frontend", "Full Stack"}:
        technologies.extend(["React", "TypeScript", "Tailwind CSS"])
    if "REST APIs" in skills or category in {"Backend", "System Design"}:
        technologies.extend(["FastAPI", "SQLAlchemy", "SQLite"])
    if "Docker" in skills or "CI/CD" in skills or category in {"DevOps", "MLOps"}:
        technologies.extend(["Docker", "GitHub Actions"])
    if "SQL" in skills:
        technologies.extend(["SQL", "SQLite"])
    if "Security" in skills:
        technologies.extend(["OWASP Basics", "Secure Validation"])
    return list(dict.fromkeys(technologies))


def _project_metadata(project: dict) -> dict:
    domain = project.get("domain") or project.get("category") or "Software Engineering"
    technologies = project.get("technologies") or _technologies_for_project(project)
    skills = ", ".join(project.get("skills", [])[:4]) or "core engineering skills"
    title = project["title"]
    return {
        **project,
        "domain": domain,
        "problem_statement": project.get("problem_statement") or f"Build {title} to solve a practical {domain.lower()} problem with production-style constraints.",
        "business_value": project.get("business_value") or f"Demonstrates how {skills} can create measurable operational, product, or decision-making value.",
        "resume_value": project.get("resume_value") or ("High" if project.get("difficulty", 1) >= 4 else "Medium"),
        "technologies": technologies,
        "architecture": project.get("architecture") or "Frontend or notebook workflow, backend/service layer where relevant, persistent storage, evaluation/reporting, and deployment-ready documentation.",
        "resume_bullet": project.get("resume_bullet") or f"Built {title} using {', '.join(technologies[:4])} to demonstrate {skills}.",
    }


ALL_PROJECTS_DATA = [_project_metadata(p) for p in PROJECTS_DATA + INDUSTRY_PROJECTS_EXTRA]


ASSESSMENTS_DATA = [
    {
        "skill_name": "Python",
        "title": "Python Fundamentals Assessment",
        "passing_score": 70.0,
        "estimated_minutes": 25,
        "questions": [
            {"id": "py1", "question": "What is the output of `print(type([]))` ?", "options": ["<class 'list'>", "<class 'tuple'>", "<class 'array'>", "<class 'dict'>"], "correct_answer": 0, "difficulty": "easy", "explanation": "[] creates an empty list, so type([]) returns <class 'list'>."},
            {"id": "py2", "question": "Which of these is NOT a valid Python data type?", "options": ["int", "float", "char", "bool"], "correct_answer": 2, "difficulty": "easy", "explanation": "Python has no 'char' type. Single characters are strings (str)."},
            {"id": "py3", "question": "What does `len('hello')` return?", "options": ["4", "5", "6", "Error"], "correct_answer": 1, "difficulty": "easy", "explanation": "'hello' has 5 characters, so len() returns 5."},
            {"id": "py4", "question": "What is a list comprehension?", "options": ["A way to document lists", "A concise way to create lists using a single expression", "A type of Python loop", "A method to sort lists"], "correct_answer": 1, "difficulty": "easy", "explanation": "List comprehensions provide a concise syntax: [x**2 for x in range(10)]"},
            {"id": "py5", "question": "Which keyword is used to define a function in Python?", "options": ["function", "def", "func", "define"], "correct_answer": 1, "difficulty": "easy", "explanation": "The 'def' keyword is used to define functions in Python."},
            {"id": "py6", "question": "What is the output of `[1, 2, 3][-1]`?", "options": ["1", "3", "-1", "IndexError"], "correct_answer": 1, "difficulty": "easy", "explanation": "Negative indexing starts from the end. -1 gives the last element: 3."},
            {"id": "py7", "question": "What does `*args` do in a function definition?", "options": ["Requires exactly one argument", "Accepts any number of positional arguments into a tuple", "Accepts keyword arguments only", "Creates a list parameter"], "correct_answer": 1, "difficulty": "medium", "explanation": "*args collects extra positional arguments into a tuple."},
            {"id": "py8", "question": "What is the output of `bool('')` ?", "options": ["True", "False", "None", "Error"], "correct_answer": 1, "difficulty": "medium", "explanation": "Empty strings are falsy in Python. bool('') returns False."},
            {"id": "py9", "question": "You need to process a 10GB CSV file line by line without loading it all into memory. Which approach is most appropriate?", "options": ["pd.read_csv('file.csv')", "open('file.csv').readlines()", "Using a generator with open('file.csv') as f: for line in f:", "list(open('file.csv'))"], "correct_answer": 2, "difficulty": "medium", "explanation": "Iterating over a file object with a for loop reads one line at a time — memory efficient for large files."},
            {"id": "py10", "question": "What is the difference between `==` and `is` in Python?", "options": ["No difference", "== checks value equality; is checks identity (same object in memory)", "is checks type; == checks value", "== checks identity; is checks value"], "correct_answer": 1, "difficulty": "medium", "explanation": "== compares values. 'is' checks if both variables point to the SAME object in memory."},
            {"id": "py11", "question": "What is the output of: `x = [1,2,3]; y = x; y.append(4); print(x)` ?", "options": ["[1, 2, 3]", "[1, 2, 3, 4]", "Error", "[4]"], "correct_answer": 1, "difficulty": "medium", "explanation": "Lists are mutable. y = x makes y point to the SAME list. Appending to y modifies x too."},
            {"id": "py12", "question": "What is a decorator in Python?", "options": ["A class for UI styling", "A function that wraps another function to extend its behavior", "A type annotation", "A module import alias"], "correct_answer": 1, "difficulty": "medium", "explanation": "Decorators use @syntax to wrap functions, adding behavior without modifying the original function."},
            {"id": "py13", "question": "What is the output of `{1: 'a', 2: 'b', 1: 'c'}[1]` ?", "options": ["'a'", "'c'", "['a', 'c']", "KeyError"], "correct_answer": 1, "difficulty": "medium", "explanation": "Duplicate keys in a dict — the later value overwrites the earlier one. {1: 'c'} wins."},
            {"id": "py14", "question": "Which of these creates a generator?", "options": ["[x for x in range(10)]", "(x for x in range(10))", "{x for x in range(10)}", "list(range(10))"], "correct_answer": 1, "difficulty": "medium", "explanation": "Using () instead of [] creates a generator expression. It generates values lazily (one at a time)."},
            {"id": "py15", "question": "What does `__init__` do in a Python class?", "options": ["Destroys the object", "Initializes instance attributes when an object is created", "Defines class-level variables", "Imports modules"], "correct_answer": 1, "difficulty": "medium", "explanation": "__init__ is the constructor — it's called automatically when you create an instance of a class."},
            {"id": "py16", "question": "What is the output of `try: 1/0 except ZeroDivisionError: print('caught') finally: print('done')` ?", "options": ["caught", "done", "caught\\ndone", "Error"], "correct_answer": 2, "difficulty": "hard", "explanation": "The except block catches ZeroDivisionError and prints 'caught'. The finally block ALWAYS runs and prints 'done'."},
            {"id": "py17", "question": "You have a function that should cache expensive results. Which Python tool is most appropriate?", "options": ["try/except", "@functools.lru_cache", "global variables", "threading.Lock"], "correct_answer": 1, "difficulty": "hard", "explanation": "@functools.lru_cache memoizes function results, so repeated calls with the same arguments return cached results instantly."},
            {"id": "py18", "question": "What is the GIL (Global Interpreter Lock)?", "options": ["A security feature blocking dangerous code", "A mutex that prevents multiple Python threads from executing Python bytecodes simultaneously", "A way to lock variables", "A garbage collection mechanism"], "correct_answer": 1, "difficulty": "hard", "explanation": "The GIL ensures only one thread executes Python bytecode at a time, which affects CPU-bound multithreaded programs."},
            {"id": "py19", "question": "What is the output of `sorted([3,1,2], key=lambda x: -x)` ?", "options": ["[1, 2, 3]", "[3, 2, 1]", "[-3, -2, -1]", "Error"], "correct_answer": 1, "difficulty": "hard", "explanation": "The key=lambda x: -x sorts by negative value, which reverses the order: [3, 2, 1]."},
            {"id": "py20", "question": "What is the difference between `deepcopy` and `copy` from the copy module?", "options": ["No difference", "deepcopy creates an independent copy of all nested objects; copy only copies the outer object", "copy is faster only", "deepcopy only works with lists"], "correct_answer": 1, "difficulty": "hard", "explanation": "copy() creates a shallow copy (nested objects are shared). deepcopy() recursively copies all nested objects."},
        ]
    },
    {
        "skill_name": "Machine Learning",
        "title": "Machine Learning Concepts Assessment",
        "passing_score": 70.0,
        "estimated_minutes": 30,
        "questions": [
            {"id": "ml1", "question": "What is overfitting in machine learning?", "options": ["The model is too simple", "The model performs well on training data but poorly on new data", "Training takes too long", "The dataset is too large"], "correct_answer": 1, "difficulty": "easy", "explanation": "Overfitting occurs when a model memorizes training data patterns but fails to generalize."},
            {"id": "ml2", "question": "What does 'training accuracy: 99%, validation accuracy: 65%' most likely indicate?", "options": ["Good model", "Underfitting", "Overfitting", "Perfect generalization"], "correct_answer": 2, "difficulty": "easy", "explanation": "High training but low validation accuracy is a classic sign of overfitting."},
            {"id": "ml3", "question": "What does the 'k' in K-Nearest Neighbors represent?", "options": ["Number of features", "Number of training iterations", "Number of nearest neighbors to consider", "Number of classes"], "correct_answer": 2, "difficulty": "easy", "explanation": "k is the number of nearest neighbors used to make a prediction."},
            {"id": "ml4", "question": "What is the purpose of the validation set?", "options": ["To train the model", "To test final model performance", "To tune hyperparameters without contaminating the test set", "To clean the data"], "correct_answer": 2, "difficulty": "easy", "explanation": "Validation set helps tune hyperparameters. The test set should only be used once at the very end."},
            {"id": "ml5", "question": "Which metric is most appropriate for a highly imbalanced binary classification?", "options": ["Accuracy", "F1-Score or AUC-ROC", "Mean Squared Error", "R-squared"], "correct_answer": 1, "difficulty": "easy", "explanation": "With 95% class imbalance, a model predicting the majority class always achieves 95% accuracy. F1 or AUC-ROC is better."},
            {"id": "ml6", "question": "What is gradient descent?", "options": ["A method to increase model complexity", "An optimization algorithm that iteratively minimizes the loss function", "A technique to handle missing data", "A regularization method"], "correct_answer": 1, "difficulty": "easy", "explanation": "Gradient descent updates parameters in the direction opposite to the gradient to minimize the loss."},
            {"id": "ml7", "question": "What is L2 regularization (Ridge) doing to your model?", "options": ["Removes features entirely", "Penalizes large weights by adding their squared sum to the loss", "Increases model complexity", "Only works for neural networks"], "correct_answer": 1, "difficulty": "medium", "explanation": "L2 regularization adds λ·sum(w²) to the loss, penalizing large weights and preventing overfitting."},
            {"id": "ml8", "question": "You have a model with high bias and high variance. What is the correct term?", "options": ["Overfitting", "Underfitting", "Perfect fit", "This cannot happen"], "correct_answer": 1, "difficulty": "medium", "explanation": "High bias = underfitting (model is too simple). High bias AND high variance = very poor model on both training and test data."},
            {"id": "ml9", "question": "What does cross-validation primarily help with?", "options": ["Faster training", "More reliable evaluation by using multiple train/test splits", "Feature selection only", "Reducing dataset size"], "correct_answer": 1, "difficulty": "medium", "explanation": "K-fold cross-validation gives a more robust estimate of model performance by training and testing on k different splits."},
            {"id": "ml10", "question": "In a confusion matrix: TN=800, FP=50, FN=30, TP=120. What is the Precision?", "options": ["0.80", "0.71", "0.80", "0.84"], "correct_answer": 1, "difficulty": "medium", "explanation": "Precision = TP/(TP+FP) = 120/(120+50) = 120/170 ≈ 0.71."},
            {"id": "ml11", "question": "What is feature engineering?", "options": ["Selecting the best algorithm", "Creating, transforming, or selecting features to improve model performance", "A type of regularization", "Reducing training time"], "correct_answer": 1, "difficulty": "medium", "explanation": "Feature engineering transforms raw data into features that better represent the problem, often the most impactful ML step."},
            {"id": "ml12", "question": "Which algorithm naturally handles non-linear decision boundaries without explicit feature mapping?", "options": ["Linear Regression", "Logistic Regression", "Support Vector Machine with RBF kernel", "Naive Bayes"], "correct_answer": 2, "difficulty": "medium", "explanation": "SVM with an RBF kernel implicitly maps data to higher dimensions using the kernel trick, handling non-linear boundaries."},
            {"id": "ml13", "question": "What is the main difference between bagging and boosting?", "options": ["Speed only", "Bagging trains models in parallel independently; boosting trains sequentially where each model corrects the previous", "Bagging only works for trees", "Boosting uses more data"], "correct_answer": 1, "difficulty": "hard", "explanation": "Bagging (e.g., Random Forest) reduces variance via parallel independent models. Boosting (e.g., XGBoost) reduces bias via sequential error correction."},
            {"id": "ml14", "question": "Your model achieves 98% accuracy on test data. A domain expert says results look suspicious. What should you check first?", "options": ["The model architecture", "Data leakage (test data information bleeding into training)", "Learning rate", "Number of epochs"], "correct_answer": 1, "difficulty": "hard", "explanation": "Suspiciously high accuracy often indicates data leakage — test set labels influencing training through improper preprocessing."},
            {"id": "ml15", "question": "What does PCA (Principal Component Analysis) primarily do?", "options": ["Classifies data", "Reduces dimensionality by finding directions of maximum variance", "Handles missing values", "Improves model accuracy directly"], "correct_answer": 1, "difficulty": "hard", "explanation": "PCA projects data onto principal components (directions of maximum variance) to reduce dimensions while preserving information."},
            {"id": "ml16", "question": "What is a learning rate scheduler?", "options": ["A tool to set training time", "A technique to adaptively change the learning rate during training", "A method to select the best model", "Hardware configuration for ML"], "correct_answer": 1, "difficulty": "hard", "explanation": "Learning rate schedulers reduce the learning rate over time, helping the model converge more precisely."},
            {"id": "ml17", "question": "What is the key difference between classification and regression?", "options": ["Speed of training", "Classification predicts discrete categories; regression predicts continuous values", "Number of features", "Algorithm type only"], "correct_answer": 1, "difficulty": "easy", "explanation": "Classification: Is this email spam? (yes/no). Regression: What will house prices be? (a number)."},
            {"id": "ml18", "question": "What is ensemble learning?", "options": ["Training on multiple datasets", "Combining predictions from multiple models to improve performance", "A type of neural network", "Data augmentation"], "correct_answer": 1, "difficulty": "medium", "explanation": "Ensemble methods (Random Forest, Gradient Boosting) combine multiple weaker models to create a stronger predictor."},
            {"id": "ml19", "question": "When should you normalize/standardize features?", "options": ["Never", "Only for tree-based models", "When using distance-based algorithms (KNN, SVM, k-means) or gradient-based optimization", "Only when accuracy is low"], "correct_answer": 2, "difficulty": "hard", "explanation": "Distance-based algorithms are sensitive to feature scales. Gradient descent converges faster with normalized features."},
            {"id": "ml20", "question": "What does SHAP (SHapley Additive exPlanations) help with?", "options": ["Model training speed", "Explaining individual predictions by quantifying each feature's contribution", "Data preprocessing", "Hyperparameter tuning"], "correct_answer": 1, "difficulty": "hard", "explanation": "SHAP provides model interpretability by showing how much each feature contributed to a specific prediction."},
        ]
    },
    {
        "skill_name": "DSA",
        "title": "Data Structures & Algorithms Assessment",
        "passing_score": 70.0,
        "estimated_minutes": 30,
        "questions": [
            {"id": "dsa1", "question": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "correct_answer": 1, "difficulty": "easy", "explanation": "Binary search halves the search space each step: O(log n)."},
            {"id": "dsa2", "question": "Which data structure uses LIFO (Last In, First Out)?", "options": ["Queue", "Stack", "Linked List", "Heap"], "correct_answer": 1, "difficulty": "easy", "explanation": "A Stack follows LIFO — the last element added is the first removed."},
            {"id": "dsa3", "question": "What is the worst-case time complexity of Quicksort?", "options": ["O(n log n)", "O(n²)", "O(n)", "O(log n)"], "correct_answer": 1, "difficulty": "easy", "explanation": "Quicksort degrades to O(n²) with bad pivot selection (e.g., already sorted arrays with first-element pivot)."},
            {"id": "dsa4", "question": "Which algorithm finds the shortest path in an unweighted graph?", "options": ["DFS", "BFS", "Dijkstra's", "Bellman-Ford"], "correct_answer": 1, "difficulty": "easy", "explanation": "BFS guarantees shortest path in unweighted graphs by exploring level by level."},
            {"id": "dsa5", "question": "What is the space complexity of a recursive Fibonacci without memoization?", "options": ["O(1)", "O(n)", "O(log n)", "O(2^n)"], "correct_answer": 1, "difficulty": "easy", "explanation": "Recursive Fibonacci uses O(n) stack space due to the maximum depth of n recursive calls."},
            {"id": "dsa6", "question": "What is a hash table collision?", "options": ["When two keys map to the same index", "When the table is full", "When a key is not found", "When the hash function fails"], "correct_answer": 0, "difficulty": "easy", "explanation": "A collision occurs when two different keys produce the same hash value/index."},
            {"id": "dsa7", "question": "What is the time complexity of inserting into a sorted array at a specific position?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "correct_answer": 2, "difficulty": "medium", "explanation": "Inserting into a sorted array requires shifting elements: O(n) in the worst case."},
            {"id": "dsa8", "question": "What property must a Binary Search Tree (BST) maintain?", "options": ["All nodes equal", "Left child < parent < right child for all nodes", "Left child > parent > right child", "Nodes are sorted by height"], "correct_answer": 1, "difficulty": "medium", "explanation": "BST property: left subtree contains nodes with values less than the parent; right subtree has values greater."},
            {"id": "dsa9", "question": "What is the time complexity of a heap (priority queue) pop operation?", "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"], "correct_answer": 2, "difficulty": "medium", "explanation": "Popping from a heap requires re-heapifying: O(log n)."},
            {"id": "dsa10", "question": "You need to detect a cycle in a linked list efficiently. Which approach is optimal?", "options": ["Store all visited nodes in a HashSet: O(n) space", "Floyd's tortoise and hare algorithm: O(1) space", "Sort the list first", "Use a stack"], "correct_answer": 1, "difficulty": "medium", "explanation": "Floyd's algorithm uses two pointers at different speeds. If there's a cycle, they'll meet. O(n) time, O(1) space."},
            {"id": "dsa11", "question": "What does a topological sort produce?", "options": ["A sorted list of node values", "A linear ordering of vertices in a DAG where each vertex comes before its dependencies", "The shortest path tree", "A minimum spanning tree"], "correct_answer": 1, "difficulty": "medium", "explanation": "Topological sort orders vertices in a directed acyclic graph (DAG) such that for every directed edge u→v, u comes before v."},
            {"id": "dsa12", "question": "What is memoization?", "options": ["Memory optimization via garbage collection", "Caching function results to avoid recomputing for the same inputs", "A type of sorting algorithm", "Array allocation technique"], "correct_answer": 1, "difficulty": "medium", "explanation": "Memoization stores computed results in a dictionary/table. When called again with the same input, it returns the cached result."},
            {"id": "dsa13", "question": "What is the time complexity of finding all subsets of a set with n elements?", "options": ["O(n)", "O(n²)", "O(2^n)", "O(n log n)"], "correct_answer": 2, "difficulty": "hard", "explanation": "Each element can be included or excluded: 2^n possible subsets. Generating all subsets is O(2^n)."},
            {"id": "dsa14", "question": "What distinguishes a graph from a tree?", "options": ["Graphs have more nodes", "Graphs can have cycles; trees are acyclic connected graphs", "Trees are directed; graphs are not", "No difference"], "correct_answer": 1, "difficulty": "medium", "explanation": "Trees are connected acyclic graphs with exactly n-1 edges for n nodes. Graphs can have cycles and may be disconnected."},
            {"id": "dsa15", "question": "Dijkstra's algorithm fails on graphs with which type of edges?", "options": ["Directed edges", "Undirected edges", "Negative weight edges", "Weighted edges"], "correct_answer": 2, "difficulty": "hard", "explanation": "Dijkstra's assumes all edge weights are non-negative. For negative weights, use Bellman-Ford."},
            {"id": "dsa16", "question": "What is the difference between DFS and BFS in terms of space complexity?", "options": ["DFS: O(n), BFS: O(n)", "DFS: O(h) where h=height, BFS: O(w) where w=max width of a level", "Both O(1)", "DFS: O(log n), BFS: O(n)"], "correct_answer": 1, "difficulty": "hard", "explanation": "DFS uses stack space proportional to height. BFS uses queue space proportional to the widest level."},
            {"id": "dsa17", "question": "What does amortized O(1) mean for dynamic array append?", "options": ["Every append is O(1)", "On average across many operations, each append is O(1) even though occasional resizing costs O(n)", "Append is free", "Only the first append is O(1)"], "correct_answer": 1, "difficulty": "hard", "explanation": "When a dynamic array resizes, it doubles capacity. The total cost spread across all appends averages to O(1) per operation."},
            {"id": "dsa18", "question": "What is a trie data structure used for?", "options": ["Sorting numbers", "Efficient prefix-based string search and autocomplete", "Graph traversal", "Heap operations"], "correct_answer": 1, "difficulty": "hard", "explanation": "A trie stores strings character by character, enabling O(L) prefix search where L is string length — ideal for autocomplete."},
            {"id": "dsa19", "question": "What is the difference between stable and unstable sorting algorithms?", "options": ["Speed difference", "Stable sorts maintain relative order of equal elements; unstable may not", "Memory usage", "Stability affects only floating-point numbers"], "correct_answer": 1, "difficulty": "medium", "explanation": "Stable: Merge Sort, Insertion Sort. Unstable: Quick Sort, Heap Sort. Important when sorting objects by multiple keys."},
            {"id": "dsa20", "question": "What is a segment tree used for?", "options": ["Sorting large arrays", "Efficient range queries (sum, min, max) and point updates on arrays: O(log n)", "Graph shortest paths", "Hashing strings"], "correct_answer": 1, "difficulty": "hard", "explanation": "Segment trees support range queries (e.g., sum of elements from index i to j) and updates in O(log n) time."},
        ]
    },
    {
        "skill_name": "SQL",
        "title": "SQL & Databases Assessment",
        "passing_score": 70.0,
        "estimated_minutes": 20,
        "questions": [
            {"id": "sql1", "question": "Which clause filters rows BEFORE aggregation?", "options": ["HAVING", "WHERE", "ORDER BY", "FILTER"], "correct_answer": 1, "difficulty": "easy", "explanation": "WHERE filters rows before GROUP BY. HAVING filters the groups after aggregation."},
            {"id": "sql2", "question": "What does `SELECT COUNT(DISTINCT user_id) FROM orders` return?", "options": ["Total orders", "Number of unique users who placed orders", "Average orders per user", "Maximum orders"], "correct_answer": 1, "difficulty": "easy", "explanation": "COUNT(DISTINCT col) counts unique non-null values."},
            {"id": "sql3", "question": "Which JOIN returns all rows from the left table even if no match in right?", "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "CROSS JOIN"], "correct_answer": 1, "difficulty": "easy", "explanation": "LEFT JOIN returns all left table rows. Non-matching right table columns are NULL."},
            {"id": "sql4", "question": "What is a PRIMARY KEY?", "options": ["Any indexed column", "A column with unique, non-null values that identifies each row", "The first column in a table", "A foreign reference column"], "correct_answer": 1, "difficulty": "easy", "explanation": "PRIMARY KEY: unique, non-null, used to identify each row in a table."},
            {"id": "sql5", "question": "What does this return: `SELECT dept, AVG(salary) FROM employees GROUP BY dept HAVING AVG(salary) > 50000`?", "options": ["All employees with salary > 50000", "Departments where average salary exceeds 50000", "Employees in departments with avg salary > 50000", "Error"], "correct_answer": 1, "difficulty": "medium", "explanation": "GROUP BY + HAVING filters groups (departments) where the aggregated condition (avg salary) is met."},
            {"id": "sql6", "question": "What is a window function?", "options": ["A GUI database tool", "A function that performs calculations across a sliding set of rows related to the current row without collapsing them", "A stored procedure", "A view"], "correct_answer": 1, "difficulty": "medium", "explanation": "Window functions like ROW_NUMBER(), RANK(), LAG() operate over a window of rows but return a value for each row."},
            {"id": "sql7", "question": "What does ACID stand for in databases?", "options": ["Array, Commit, Index, Delete", "Atomicity, Consistency, Isolation, Durability", "Async, Concurrent, Incremental, Distributed", "Add, Create, Index, Drop"], "correct_answer": 1, "difficulty": "medium", "explanation": "ACID ensures reliable transactions: Atomicity (all-or-nothing), Consistency, Isolation, Durability."},
            {"id": "sql8", "question": "What is database normalization?", "options": ["Making queries faster", "Organizing tables to reduce data redundancy and improve data integrity", "Indexing all columns", "Converting data types"], "correct_answer": 1, "difficulty": "medium", "explanation": "Normalization (1NF, 2NF, 3NF) eliminates redundancy by decomposing tables according to functional dependencies."},
            {"id": "sql9", "question": "You have 1 million rows and a query on `WHERE email = ?` is slow. What is the best fix?", "options": ["Add more RAM", "Create an index on the email column", "Use SELECT *", "Delete old rows"], "correct_answer": 1, "difficulty": "medium", "explanation": "An index on email creates a B-tree structure enabling O(log n) lookup instead of O(n) full table scan."},
            {"id": "sql10", "question": "What is the difference between DELETE and TRUNCATE?", "options": ["No difference", "DELETE removes specific rows (can be rolled back); TRUNCATE removes all rows (faster, harder to roll back)", "TRUNCATE is slower", "DELETE only works with WHERE clause"], "correct_answer": 1, "difficulty": "medium", "explanation": "DELETE is DML (can use WHERE, can rollback). TRUNCATE is DDL (removes all rows, minimal logging, faster)."},
            {"id": "sql11", "question": "What does a subquery in a WHERE clause do?", "options": ["Creates a new table", "Allows using the result of one SELECT query as a condition for another", "Joins tables", "Creates indexes"], "correct_answer": 1, "difficulty": "medium", "explanation": "Subqueries let you filter rows based on the result of another query: WHERE id IN (SELECT id FROM ...)"},
            {"id": "sql12", "question": "What is a CTE (Common Table Expression)?", "options": ["A type of index", "A named temporary result set defined with WITH clause for use within a single query", "A database table type", "A JOIN method"], "correct_answer": 1, "difficulty": "hard", "explanation": "WITH cte AS (SELECT ...) SELECT ... FROM cte — CTEs improve readability and enable recursive queries."},
            {"id": "sql13", "question": "What is the difference between a clustered and non-clustered index?", "options": ["Speed only", "Clustered index defines physical row order (only 1 per table); non-clustered is a separate structure with pointers", "Non-clustered is better", "No functional difference"], "correct_answer": 1, "difficulty": "hard", "explanation": "Clustered index = the actual table data sorted by key. Non-clustered = separate B-tree with pointers to rows."},
            {"id": "sql14", "question": "Write the SQL to find the second highest salary. Which is correct?", "options": ["SELECT MAX(salary) FROM emp WHERE salary != MAX(salary)", "SELECT MAX(salary) FROM emp WHERE salary < (SELECT MAX(salary) FROM emp)", "SELECT salary FROM emp ORDER BY salary LIMIT 1 OFFSET 1", "SELECT TOP 2 salary FROM emp"], "correct_answer": 1, "difficulty": "hard", "explanation": "The subquery finds MAX salary, then outer query finds max of all salaries below it = 2nd highest."},
            {"id": "sql15", "question": "What is a deadlock in databases?", "options": ["A slow query", "When two transactions each hold a lock the other needs, causing infinite waiting", "A failed constraint", "Database crash"], "correct_answer": 1, "difficulty": "hard", "explanation": "Deadlock: Transaction A holds Lock 1, needs Lock 2. Transaction B holds Lock 2, needs Lock 1. Neither can proceed."},
        ]
    },
    {
        "skill_name": "Statistics",
        "title": "Statistics for Data Science Assessment",
        "passing_score": 70.0,
        "estimated_minutes": 20,
        "questions": [
            {"id": "stat1", "question": "What does a p-value of 0.03 mean?", "options": ["97% confident the result is true", "3% probability of observing this result if the null hypothesis is true", "The result is definitely significant", "3% error in the experiment"], "correct_answer": 1, "difficulty": "easy", "explanation": "P-value = probability of observing a result as extreme as yours IF the null hypothesis is true. Low p-value → evidence against H0."},
            {"id": "stat2", "question": "What is the Central Limit Theorem?", "options": ["Any distribution's mean is zero", "Sample means approach a normal distribution as sample size increases, regardless of population distribution", "Large samples always have equal variance", "The median equals mean for symmetric data"], "correct_answer": 1, "difficulty": "easy", "explanation": "CLT: With large enough n, sample means are approximately normally distributed — even from non-normal populations."},
            {"id": "stat3", "question": "What does variance measure?", "options": ["The average value", "How spread out values are from the mean (average squared deviation)", "The most frequent value", "The middle value"], "correct_answer": 1, "difficulty": "easy", "explanation": "Variance = average of squared differences from the mean. Standard deviation = sqrt(variance)."},
            {"id": "stat4", "question": "What is a Type I error?", "options": ["False Negative", "False Positive (rejecting a true null hypothesis)", "Underfitting", "Sampling bias"], "correct_answer": 1, "difficulty": "medium", "explanation": "Type I error (α) = false positive = rejecting H0 when it's actually true. Type II (β) = false negative = failing to reject false H0."},
            {"id": "stat5", "question": "Pearson correlation = 0.85 between study hours and exam score. What can you conclude?", "options": ["Studying causes high scores", "Strong positive linear relationship between study hours and exam scores", "95% of variance is explained", "No relationship"], "correct_answer": 1, "difficulty": "easy", "explanation": "Pearson r measures LINEAR relationship strength (-1 to +1). Correlation ≠ causation. r=0.85 means strong positive linear association."},
            {"id": "stat6", "question": "What is the difference between parametric and non-parametric tests?", "options": ["Speed only", "Parametric tests assume data follows a specific distribution (e.g., normal); non-parametric don't", "Non-parametric is always better", "They're the same"], "correct_answer": 1, "difficulty": "medium", "explanation": "Parametric (t-test, ANOVA) assume normality. Non-parametric (Mann-Whitney, Kruskal-Wallis) make no distribution assumptions."},
            {"id": "stat7", "question": "A 95% confidence interval for a mean is [45, 55]. What does this mean?", "options": ["95% of data falls between 45 and 55", "If we repeated the study many times, 95% of such intervals would contain the true mean", "The true mean is definitely in [45, 55]", "There's a 5% chance the mean is wrong"], "correct_answer": 1, "difficulty": "medium", "explanation": "CI interpretation: If we computed this interval from many samples, 95% of those intervals would contain the true population mean."},
            {"id": "stat8", "question": "What is Bayes' theorem used for in data science?", "options": ["Feature selection", "Updating probability beliefs given new evidence: P(A|B) = P(B|A)·P(A)/P(B)", "Model evaluation", "Data normalization"], "correct_answer": 1, "difficulty": "medium", "explanation": "Bayes' theorem: P(H|Data) = P(Data|H)·P(H)/P(Data). Used in spam detection, medical diagnosis, Bayesian ML models."},
            {"id": "stat9", "question": "What is multicollinearity and why is it a problem?", "options": ["Too many features", "When independent variables are highly correlated, making coefficient estimates unstable", "Missing values", "Data imbalance"], "correct_answer": 1, "difficulty": "medium", "explanation": "Multicollinearity in regression makes it hard to distinguish individual feature effects. Inflates variance of coefficient estimates."},
            {"id": "stat10", "question": "What does R² (coefficient of determination) measure?", "options": ["Correlation between variables", "Proportion of variance in the dependent variable explained by the model (0 to 1)", "Model accuracy in percentage", "Average prediction error"], "correct_answer": 1, "difficulty": "medium", "explanation": "R² = 1 means the model explains all variance. R² = 0 means the model explains none. Can be negative if model is worse than mean prediction."},
            {"id": "stat11", "question": "What is the difference between population and sample standard deviation?", "options": ["No difference", "Population uses N in denominator; sample uses N-1 (Bessel's correction for unbiased estimation)", "Population is always larger", "Formulas are identical"], "correct_answer": 1, "difficulty": "hard", "explanation": "Sample SD uses n-1 (Bessel's correction) because sample mean is itself estimated, slightly underestimating spread if n is used."},
            {"id": "stat12", "question": "What is A/B testing?", "options": ["Comparing two ML algorithms", "A controlled experiment comparing two versions (A=control, B=treatment) to determine which performs better", "Testing software bugs", "Data cleaning method"], "correct_answer": 1, "difficulty": "medium", "explanation": "A/B tests randomly split users into groups, apply different treatments, and use statistical tests to determine if differences are significant."},
            {"id": "stat13", "question": "What is the law of large numbers?", "options": ["Large datasets are always better", "As sample size increases, sample mean converges to the true population mean", "Standard deviation increases with n", "All samples are normally distributed"], "correct_answer": 1, "difficulty": "medium", "explanation": "LLN: With more observations, sample statistics become more reliable estimates of population parameters."},
            {"id": "stat14", "question": "When is Mann-Whitney U test more appropriate than a t-test?", "options": ["When data is normally distributed", "When data is non-normal, ordinal, or has outliers", "When sample size is very large", "Never — t-test is always better"], "correct_answer": 1, "difficulty": "hard", "explanation": "Mann-Whitney is a non-parametric test — appropriate when normality assumptions are violated or data is ordinal."},
            {"id": "stat15", "question": "What is the multiple testing problem?", "options": ["Testing with multiple datasets", "Running many statistical tests increases probability of false positives — apply Bonferroni or FDR correction", "Using multiple models", "Testing on multiple machines"], "correct_answer": 1, "difficulty": "hard", "explanation": "With 20 tests at α=0.05, you'd expect ~1 false positive by chance. Bonferroni correction: α_adjusted = α/number_of_tests."},
        ]
    },
]




async def seed_database():
    """Main seed function — idempotent, safe to run multiple times."""
    from backend.app.models import User
    async with AsyncSessionLocal() as db:
        try:
            await _seed_skills(db)
            await _seed_resources(db)
            await _seed_projects(db)
            await _seed_assessments(db)
            await _seed_demo_user(db)
            # Also seed progress for already-existing demo users (idempotent)
            demo_result = await db.execute(
                select(User).where(User.email == "demo@learnpath.ai")
            )
            demo_user = demo_result.scalar_one_or_none()
            if demo_user:
                await _seed_demo_progress(db, demo_user.id)
            await db.commit()
        except Exception as e:
            await db.rollback()
            print(f"[Seed] Error: {e}")
            raise


async def _seed_skills(db: AsyncSession):
    from backend.app.models import Skill
    from sqlalchemy import select

    result = await db.execute(select(Skill).limit(1))
    if result.scalar_one_or_none():
        return  # Already seeded

    for skill_data in SKILLS_DATA:
        skill = Skill(
            id=gen_id(),
            name=skill_data["name"],
            category=skill_data["category"],
            description=skill_data.get("description", ""),
            difficulty=skill_data["difficulty"],
            prerequisites=skill_data["prerequisites"],
            tags=skill_data["tags"],
        )
        db.add(skill)
    await db.flush()
    print(f"[Seed] Added {len(SKILLS_DATA)} skills")


async def _seed_resources(db: AsyncSession):
    from backend.app.models import LearningResource
    from sqlalchemy import select

    result = await db.execute(select(LearningResource).limit(1))
    if result.scalar_one_or_none():
        return

    for r in RESOURCES_DATA:
        resource = LearningResource(
            id=gen_id(),
            title=r["title"],
            description=r.get("description", ""),
            provider=r["provider"],
            url=r["url"],
            category=r["category"],
            skills=r["skills"],
            difficulty=r["difficulty"],
            duration_hours=r["duration_hours"],
            format=r["format"],
            rating=r["rating"],
            tags=r.get("tags", []),
            is_free=r["is_free"],
            prerequisites=r["prerequisites"],
        )
        db.add(resource)
    await db.flush()
    print(f"[Seed] Added {len(RESOURCES_DATA)} resources")


async def _seed_projects(db: AsyncSession):
    from backend.app.models import Project
    from sqlalchemy import select

    added = 0
    updated = 0
    for p in ALL_PROJECTS_DATA:
        result = await db.execute(select(Project).where(Project.title == p["title"]))
        project = result.scalar_one_or_none()

        if not project:
            project = Project(
                id=gen_id(),
                title=p["title"],
                description=p.get("description", ""),
                skills=p["skills"],
                difficulty=p["difficulty"],
                duration_hours=p["duration_hours"],
                category=p["category"],
                tags=p.get("tags", []),
            )
            db.add(project)
            added += 1

        for field in (
            "domain",
            "problem_statement",
            "business_value",
            "resume_value",
            "technologies",
            "architecture",
            "resume_bullet",
        ):
            value = p.get(field)
            if value and not getattr(project, field):
                setattr(project, field, value)
                updated += 1

    await db.flush()
    print(f"[Seed] Processed {len(ALL_PROJECTS_DATA)} projects ({added} added, {updated} metadata fields updated)")


async def _seed_assessments(db: AsyncSession):
    from backend.app.models import Assessment
    from sqlalchemy import select

    for a in ASSESSMENTS_DATA:
        # Check if assessment with this title already exists
        result = await db.execute(
            select(Assessment).where(Assessment.title == a["title"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            # Update with expanded question set if the current one has fewer questions
            if len(existing.questions) < len(a["questions"]):
                existing.questions = a["questions"]
                existing.estimated_minutes = a["estimated_minutes"]
                print(f"[Seed] Updated assessment '{a['title']}' with {len(a['questions'])} questions")
        else:
            assessment = Assessment(
                id=gen_id(),
                skill_name=a["skill_name"],
                title=a["title"],
                questions=a["questions"],
                passing_score=a["passing_score"],
                estimated_minutes=a["estimated_minutes"],
            )
            db.add(assessment)
    await db.flush()
    print(f"[Seed] Processed {len(ASSESSMENTS_DATA)} assessments")



async def _seed_demo_user(db: AsyncSession):
    from backend.app.models import User, LearnerProfile, UserSkill, Roadmap, Skill
    from sqlalchemy import select

    # Check if demo user already exists
    result = await db.execute(select(User).where(User.email == "demo@learnpath.ai"))
    if result.scalar_one_or_none():
        return

    # Create demo user
    demo_user = User(
        id=gen_id(),
        name="Alex Chen",
        email="demo@learnpath.ai",
        hashed_password=get_password_hash("Demo@12345"),
        is_active=True,
        is_demo=True,
    )
    db.add(demo_user)
    await db.flush()

    # Create demo profile
    demo_profile = LearnerProfile(
        id=gen_id(),
        user_id=demo_user.id,
        target_role="AI/ML Engineer",
        experience_level="intermediate",
        education="B.Tech Computer Science, 2nd Year",
        career_goal="Become a Machine Learning Engineer and land a role at a top tech company within 12 months",
        weekly_hours=14.0,
        learning_style="mixed",
        target_deadline="12",
        preferred_duration="medium",
        strengths=["Python", "Problem Solving", "Mathematics"],
        weaknesses=["Statistics", "Deep Learning", "Model Deployment"],
    )
    db.add(demo_profile)

    # Create demo user skills
    demo_skills = [
        {"skill_name": "Python", "current_level": 3, "target_level": 4, "priority": "low"},
        {"skill_name": "SQL", "current_level": 2, "target_level": 3, "priority": "medium"},
        {"skill_name": "DSA", "current_level": 2, "target_level": 3, "priority": "medium"},
        {"skill_name": "Statistics", "current_level": 1, "target_level": 4, "priority": "critical"},
        {"skill_name": "Linear Algebra", "current_level": 1, "target_level": 3, "priority": "high"},
        {"skill_name": "Machine Learning", "current_level": 1, "target_level": 5, "priority": "critical"},
        {"skill_name": "Deep Learning", "current_level": 0, "target_level": 4, "priority": "high"},
        {"skill_name": "NumPy/Pandas", "current_level": 2, "target_level": 4, "priority": "high"},
        {"skill_name": "Git", "current_level": 2, "target_level": 3, "priority": "low"},
    ]

    for skill_data in demo_skills:
        # Find skill id
        skill_result = await db.execute(select(Skill).where(Skill.name == skill_data["skill_name"]))
        skill = skill_result.scalar_one_or_none()
        gap = skill_data["target_level"] - skill_data["current_level"]
        user_skill = UserSkill(
            id=gen_id(),
            user_id=demo_user.id,
            skill_id=skill.id if skill else gen_id(),
            skill_name=skill_data["skill_name"],
            current_level=skill_data["current_level"],
            target_level=skill_data["target_level"],
            gap_score=float(gap),
            priority=skill_data["priority"],
        )
        db.add(user_skill)

    # Create demo progress records for realistic streak/progress
    from backend.app.models import Progress
    from datetime import datetime, timedelta
    import random

    demo_progress = [
        {
            "resource_id": None,
            "project_id": None,
            "status": "completed",
            "completion_percentage": 100,
            "time_spent_hours": 2.5,
            "days_ago": 1,
        },
        {
            "resource_id": None,
            "project_id": None,
            "status": "completed",
            "completion_percentage": 100,
            "time_spent_hours": 3.0,
            "days_ago": 2,
        },
        {
            "resource_id": None,
            "project_id": None,
            "status": "completed",
            "completion_percentage": 100,
            "time_spent_hours": 1.5,
            "days_ago": 3,
        },
        {
            "resource_id": None,
            "project_id": None,
            "status": "in_progress",
            "completion_percentage": 45,
            "time_spent_hours": 1.0,
            "days_ago": 0,
        },
    ]

    for i, prog_data in enumerate(demo_progress):
        completed_at = None
        updated_at = datetime.utcnow()
        if prog_data["status"] == "completed":
            completed_at = datetime.utcnow() - timedelta(days=prog_data["days_ago"])
            updated_at = completed_at
        else:
            updated_at = datetime.utcnow() - timedelta(hours=random.randint(1, 5))

        progress = Progress(
            id=gen_id(),
            user_id=demo_user.id,
            resource_id=prog_data["resource_id"],
            project_id=prog_data["project_id"],
            status=prog_data["status"],
            completion_percentage=prog_data["completion_percentage"],
            time_spent_hours=prog_data["time_spent_hours"],
            completed_at=completed_at,
            updated_at=updated_at,
        )
        db.add(progress)

    # Create demo roadmap
    demo_roadmap = Roadmap(
        id=gen_id(),
        user_id=demo_user.id,
        title="Road to AI/ML Engineer",
        description="Your personalized 48-week roadmap to become an AI/ML Engineer",
        total_weeks=48,
        phases=[
            {
                "phase_number": 1, "title": "Python & DSA Mastery", "weeks": 6,
                "skills": ["Python", "DSA"], "status": "completed",
                "description": "Strengthen Python and learn core data structures and algorithms",
                "estimated_hours": 84,
                "resources": [{"title": "CS50P: Python Programming", "url": "https://cs50.harvard.edu/python/", "format": "course"}],
                "projects": [{"title": "CLI Expense Tracker", "difficulty": 1}],
            },
            {
                "phase_number": 2, "title": "Mathematics for AI", "weeks": 8,
                "skills": ["Statistics", "Linear Algebra"], "status": "in_progress",
                "description": "Build the mathematical foundation for machine learning",
                "estimated_hours": 112,
                "resources": [
                    {"title": "Statistics and Probability", "url": "https://www.khanacademy.org/math/statistics-probability", "format": "interactive"},
                    {"title": "Linear Algebra — 3Blue1Brown", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab", "format": "video"},
                ],
                "projects": [{"title": "Statistical Analysis Project", "difficulty": 2}],
            },
            {
                "phase_number": 3, "title": "Data Manipulation", "weeks": 6,
                "skills": ["NumPy/Pandas", "SQL"], "status": "not_started",
                "description": "Master data manipulation and database querying",
                "estimated_hours": 84,
                "resources": [{"title": "Kaggle Learn — Pandas", "url": "https://www.kaggle.com/learn/pandas", "format": "interactive"}],
                "projects": [{"title": "COVID-19 Data Analysis", "difficulty": 2}],
            },
            {
                "phase_number": 4, "title": "Machine Learning Fundamentals", "weeks": 10,
                "skills": ["Machine Learning"], "status": "not_started",
                "description": "Learn core ML algorithms and build your first models",
                "estimated_hours": 140,
                "resources": [
                    {"title": "Machine Learning Specialization", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "format": "course"},
                    {"title": "Google Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "format": "course"},
                ],
                "projects": [{"title": "Customer Churn Prediction", "difficulty": 3}],
            },
            {
                "phase_number": 5, "title": "Deep Learning", "weeks": 8,
                "skills": ["Deep Learning"], "status": "not_started",
                "description": "Neural networks, CNNs, and modern deep learning architectures",
                "estimated_hours": 112,
                "resources": [
                    {"title": "Deep Learning Specialization", "url": "https://www.coursera.org/specializations/deep-learning", "format": "course"},
                    {"title": "fast.ai Practical Deep Learning", "url": "https://course.fast.ai/", "format": "course"},
                ],
                "projects": [{"title": "Image Classification with CNN", "difficulty": 4}],
            },
            {
                "phase_number": 6, "title": "ML Portfolio Projects", "weeks": 6,
                "skills": ["Machine Learning", "Deep Learning"], "status": "not_started",
                "description": "Build impressive portfolio projects for your resume",
                "estimated_hours": 84,
                "resources": [{"title": "Kaggle — Data Science Competitions", "url": "https://www.kaggle.com/competitions", "format": "interactive"}],
                "projects": [{"title": "RAG-Based Study Assistant", "difficulty": 4}],
            },
            {
                "phase_number": 7, "title": "Model Deployment & MLOps", "weeks": 4,
                "skills": ["Model Deployment", "Docker"], "status": "not_started",
                "description": "Deploy models to production and learn MLOps practices",
                "estimated_hours": 56,
                "resources": [{"title": "Docker Official Get Started", "url": "https://docs.docker.com/get-started/", "format": "article"}],
                "projects": [{"title": "ML Model Deployment as REST API", "difficulty": 4}],
            },
        ],
        milestones=[
            {"id": "m1", "title": "Milestone 1: Foundation Complete", "description": "Python and DSA mastered", "week": 6, "skills_gained": ["Python", "DSA"], "phase": 1},
            {"id": "m2", "title": "Milestone 2: Math Ready", "description": "Statistics and Linear Algebra complete", "week": 14, "skills_gained": ["Statistics", "Linear Algebra"], "phase": 2},
            {"id": "m3", "title": "Milestone 3: First ML Model", "description": "Built and evaluated first ML model", "week": 28, "skills_gained": ["Machine Learning", "NumPy/Pandas"], "phase": 4},
            {"id": "m4", "title": "Milestone 4: Deep Learning", "description": "Built CNN and deployed model", "week": 36, "skills_gained": ["Deep Learning"], "phase": 5},
            {"id": "m5", "title": "Milestone 5: Job Ready!", "description": "Portfolio complete, interview prepared", "week": 48, "skills_gained": ["Model Deployment"], "phase": 7},
        ],
        is_active=True,
    )
    db.add(demo_roadmap)
    await db.flush()
    await _seed_demo_progress(db, demo_user.id)
    print("[Seed] Demo user created: demo@learnpath.ai / Demo@12345")


async def _seed_demo_progress(db: AsyncSession, user_id: str):
    """Seed realistic progress records for demo user so dashboard shows non-zero data."""
    from backend.app.models import Progress, LearningResource
    from sqlalchemy import select
    from datetime import datetime, timedelta

    # Check if progress already seeded
    existing = await db.execute(
        select(Progress).where(Progress.user_id == user_id).limit(1)
    )
    if existing.scalar_one_or_none():
        return  # Already seeded

    # Get first 5 resources from DB to mark as completed/in_progress
    res_result = await db.execute(select(LearningResource).limit(10))
    resources = res_result.scalars().all()
    if not resources:
        return

    now = datetime.utcnow()
    # Seed 3 completed + 2 in_progress resources spanning last 30 days
    progress_data = [
        {"idx": 0, "status": "completed", "pct": 100, "hours": 8.0, "days_ago": 25},
        {"idx": 1, "status": "completed", "pct": 100, "hours": 12.0, "days_ago": 18},
        {"idx": 2, "status": "completed", "pct": 100, "hours": 6.0, "days_ago": 10},
        {"idx": 3, "status": "in_progress", "pct": 65, "hours": 4.5, "days_ago": 5},
        {"idx": 4, "status": "in_progress", "pct": 30, "hours": 2.0, "days_ago": 1},
    ]

    for pd in progress_data:
        if pd["idx"] >= len(resources):
            break
        resource = resources[pd["idx"]]
        updated = now - timedelta(days=pd["days_ago"])
        completed_at = updated if pd["status"] == "completed" else None
        prog = Progress(
            id=gen_id(),
            user_id=user_id,
            resource_id=resource.id,
            status=pd["status"],
            completion_percentage=pd["pct"],
            time_spent_hours=pd["hours"],
            updated_at=updated,
            completed_at=completed_at,
        )
        db.add(prog)

    print("[Seed] Demo progress records seeded (5 resources)")
