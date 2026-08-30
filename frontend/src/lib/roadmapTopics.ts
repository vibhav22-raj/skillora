/**
 * Curated real-world learning resources for roadmap topics.
 * Contains only verified, high-reputation documentation, tutorials, and YouTube educational links.
 */

export interface TopicResource {
  title: string;
  provider: string;
  url: string;
  type: 'doc' | 'article' | 'video' | 'practice';
  duration?: string;
}

export interface TopicGuide {
  topic: string;
  category: string;
  summary: string;
  why_it_matters: string;
  articles: TopicResource[];
  youtube: TopicResource[];
  practice: TopicResource[];
}

export const TOPIC_GUIDES: Record<string, TopicGuide> = {
  Python: {
    topic: 'Python Programming & OOP',
    category: 'Programming',
    summary: 'Core Python syntax, data structures, list comprehensions, generators, and Object-Oriented Programming (Classes, Inheritance, Polymorphism).',
    why_it_matters: 'Python is the de-facto standard for AI/ML, Data Science, and modern backend APIs. Clean OOP skills are required to write modular production code.',
    articles: [
      { title: 'Official Python Tutorial', provider: 'Python.org', url: 'https://docs.python.org/3/tutorial/', type: 'doc', duration: '5h read' },
      { title: 'Python OOP — Classes and Objects', provider: 'Real Python', url: 'https://realpython.com/python3-object-oriented-programming/', type: 'article', duration: '30m read' },
      { title: 'Python Tutorial & Reference', provider: 'W3Schools', url: 'https://www.w3schools.com/python/', type: 'doc', duration: 'Self-paced' },
      { title: 'Python Programming Guide', provider: 'GeeksforGeeks', url: 'https://www.geeksforgeeks.org/python-programming-language-tutorial/', type: 'article', duration: 'Self-paced' },
    ],
    youtube: [
      { title: 'Python for Beginners — Full Course', provider: 'freeCodeCamp.org', url: 'https://www.youtube.com/watch?v=rfscVS0vtbw', type: 'video', duration: '4h 26m' },
      { title: 'Python OOP Tutorials — Classes, Methods, Inheritance', provider: 'Corey Schafer', url: 'https://www.youtube.com/playlist?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc', type: 'video', duration: '6 videos' },
    ],
    practice: [
      { title: 'Python Practice Problems', provider: 'HackerRank', url: 'https://www.hackerrank.com/domains/python', type: 'practice' },
      { title: 'LeetCode Python Programming Skills', provider: 'LeetCode', url: 'https://leetcode.com/studyplan/programming-skills/', type: 'practice' },
    ],
  },
  DSA: {
    topic: 'Data Structures & Algorithms',
    category: 'Computer Science',
    summary: 'Arrays, Hash Maps, Linked Lists, Stacks, Queues, Binary Trees, Graphs, Sorting, Binary Search, and Dynamic Programming.',
    why_it_matters: 'DSA is essential for solving complex engineering problems with optimal time (Big-O) and space complexity, and is the core of technical interviews.',
    articles: [
      { title: 'Data Structures Tutorial', provider: 'GeeksforGeeks', url: 'https://www.geeksforgeeks.org/data-structures/', type: 'doc', duration: 'Self-paced' },
      { title: 'Visualgo Algorithm Visualizations', provider: 'VisuAlgo', url: 'https://visualgo.net/', type: 'article', duration: 'Interactive' },
      { title: 'NeetCode 150 Roadmap', provider: 'NeetCode', url: 'https://neetcode.io/practice', type: 'article', duration: 'Curated list' },
    ],
    youtube: [
      { title: 'Data Structures & Algorithms Course', provider: 'freeCodeCamp.org', url: 'https://www.youtube.com/watch?v=8hly31xKli0', type: 'video', duration: '5h 15m' },
      { title: 'Algorithms and Data Structures Tutorial', provider: 'Abdul Bari', url: 'https://www.youtube.com/playlist?list=PLDN4rrl48XKpZkf03iYFl-O29szjTrs_O', type: 'video', duration: 'Playlist' },
    ],
    practice: [
      { title: 'LeetCode Top Interview 150', provider: 'LeetCode', url: 'https://leetcode.com/studyplan/top-interview-150/', type: 'practice' },
      { title: 'GeeksforGeeks Problem Solving', provider: 'GeeksforGeeks', url: 'https://practice.geeksforgeeks.org/explore', type: 'practice' },
    ],
  },
  Statistics: {
    topic: 'Statistics & Probability for AI',
    category: 'Mathematics',
    summary: 'Probability distributions, Mean/Median/Mode, Standard Deviation, Hypothesis Testing (p-values), Central Limit Theorem, and Bayes Theorem.',
    why_it_matters: 'Every machine learning algorithm relies on statistical inference, uncertainty quantification, and probability metrics to make decisions.',
    articles: [
      { title: 'Statistics and Probability', provider: 'Khan Academy', url: 'https://www.khanacademy.org/math/statistics-probability', type: 'doc', duration: 'Interactive' },
      { title: 'Seeing Theory — Visual Probability', provider: 'Brown University', url: 'https://seeing-theory.brown.edu/', type: 'article', duration: 'Interactive' },
    ],
    youtube: [
      { title: 'StatQuest with Josh Starmer — Statistics Fundamentals', provider: 'StatQuest', url: 'https://www.youtube.com/playlist?list=PLblh5JKOoLUK0FLuzwntyYI10UQFUhsY9', type: 'video', duration: 'Playlist' },
      { title: 'Statistics for Data Science', provider: 'freeCodeCamp.org', url: 'https://www.youtube.com/watch?v=xxpc-HPKN28', type: 'video', duration: '8h 05m' },
    ],
    practice: [
      { title: 'Khan Academy Statistics Exercises', provider: 'Khan Academy', url: 'https://www.khanacademy.org/math/statistics-probability', type: 'practice' },
    ],
  },
  'Linear Algebra': {
    topic: 'Linear Algebra for Machine Learning',
    category: 'Mathematics',
    summary: 'Vectors, Matrices, Matrix Multiplication, Eigenvalues & Eigenvectors, Dot Products, and Principal Component Analysis (PCA).',
    why_it_matters: 'Neural networks, embeddings, and computer vision models operate on high-dimensional vectors and matrix transformations.',
    articles: [
      { title: 'Linear Algebra — MIT OpenCourseWare', provider: 'MIT OCW', url: 'https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/', type: 'doc', duration: 'Complete Course' },
      { title: 'Immersive Linear Algebra', provider: 'Interactive Book', url: 'http://immersivemath.com/ila/index.html', type: 'article', duration: 'Visual 3D' },
    ],
    youtube: [
      { title: 'Essence of Linear Algebra', provider: '3Blue1Brown', url: 'https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab', type: 'video', duration: '15 videos' },
    ],
    practice: [
      { title: 'Kaggle Linear Algebra Exercises', provider: 'Kaggle Learn', url: 'https://www.kaggle.com/learn', type: 'practice' },
    ],
  },
  'NumPy/Pandas': {
    topic: 'Data Manipulation with NumPy & Pandas',
    category: 'Data Science',
    summary: 'N-dimensional arrays, vectorization, DataFrames, data filtering, missing values, grouping, merging, and reshaping data.',
    why_it_matters: '80% of data science and ML engineering involves cleaning, transforming, and feature-engineering tabular data with Pandas and NumPy.',
    articles: [
      { title: 'NumPy User Guide', provider: 'NumPy.org', url: 'https://numpy.org/doc/stable/user/index.html', type: 'doc', duration: 'Official docs' },
      { title: 'Pandas Getting Started Tutorials', provider: 'Pandas.pydata.org', url: 'https://pandas.pydata.org/docs/getting_started/index.html', type: 'doc', duration: 'Official docs' },
      { title: 'Kaggle Pandas Course', provider: 'Kaggle', url: 'https://www.kaggle.com/learn/pandas', type: 'article', duration: '4h hands-on' },
    ],
    youtube: [
      { title: 'Python Pandas Tutorial', provider: 'Keith Galli', url: 'https://www.youtube.com/watch?v=vmEHCJofslg', type: 'video', duration: '1h 00m' },
      { title: 'NumPy Full Tutorial', provider: 'freeCodeCamp.org', url: 'https://www.youtube.com/watch?v=QUT1VHiLmmI', type: 'video', duration: '1h 00m' },
    ],
    practice: [
      { title: '100 NumPy Exercises with Solutions', provider: 'GitHub / Rougier', url: 'https://github.com/rougier/numpy-100', type: 'practice' },
      { title: 'LeetCode 30 Days of Pandas', provider: 'LeetCode', url: 'https://leetcode.com/studyplan/30-days-of-pandas/', type: 'practice' },
    ],
  },
  SQL: {
    topic: 'SQL & Relational Databases',
    category: 'Data & Backend',
    summary: 'SELECT queries, JOIN types, GROUP BY, Aggregate functions, Subqueries, Window Functions, Indexes, and ACID transactions.',
    why_it_matters: 'SQL is the universal language for data extraction and persistence across relational databases like PostgreSQL, MySQL, and Snowflake.',
    articles: [
      { title: 'SQLBolt — Interactive SQL Lessons', provider: 'SQLBolt', url: 'https://sqlbolt.com/', type: 'article', duration: 'Interactive' },
      { title: 'PostgreSQL Official Documentation', provider: 'PostgreSQL.org', url: 'https://www.postgresql.org/docs/', type: 'doc', duration: 'Official docs' },
      { title: 'W3Schools SQL Tutorial', provider: 'W3Schools', url: 'https://www.w3schools.com/sql/', type: 'doc', duration: 'Self-paced' },
    ],
    youtube: [
      { title: 'SQL Tutorial — Full Database Course for Beginners', provider: 'freeCodeCamp.org', url: 'https://www.youtube.com/watch?v=HXV3zeRR3h4', type: 'video', duration: '4h 20m' },
      { title: 'SQL Joins Explained Visually', provider: 'Luke Barousse', url: 'https://www.youtube.com/watch?v=0h9b0sK3fio', type: 'video', duration: '15m' },
    ],
    practice: [
      { title: 'SQLZoo Interactive Queries', provider: 'SQLZoo', url: 'https://sqlzoo.net/', type: 'practice' },
      { title: 'LeetCode SQL 50 Study Plan', provider: 'LeetCode', url: 'https://leetcode.com/studyplan/top-sql-50/', type: 'practice' },
    ],
  },
  'Machine Learning': {
    topic: 'Machine Learning Algorithms & Pipelines',
    category: 'AI/ML',
    summary: 'Supervised vs Unsupervised learning, Linear/Logistic Regression, Decision Trees, Random Forests, Gradient Boosting (XGBoost), Overfitting, Cross-Validation, and Scikit-Learn.',
    why_it_matters: 'ML is the core foundation for predictive intelligence, recommendation engines, fraud detection, and predictive modeling.',
    articles: [
      { title: 'Scikit-Learn User Guide', provider: 'Scikit-learn.org', url: 'https://scikit-learn.org/stable/user_guide.html', type: 'doc', duration: 'Official docs' },
      { title: 'Google Machine Learning Crash Course', provider: 'Google Developers', url: 'https://developers.google.com/machine-learning/crash-course', type: 'article', duration: '15h interactive' },
      { title: 'Kaggle Intro to Machine Learning', provider: 'Kaggle Learn', url: 'https://www.kaggle.com/learn/intro-to-machine-learning', type: 'article', duration: '3h hands-on' },
    ],
    youtube: [
      { title: 'StatQuest Machine Learning Videos', provider: 'StatQuest with Josh Starmer', url: 'https://www.youtube.com/playlist?list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF', type: 'video', duration: 'Playlist' },
      { title: 'Machine Learning for Everybody', provider: 'freeCodeCamp.org', url: 'https://www.youtube.com/watch?v=i_LwzRVP7bg', type: 'video', duration: '3h 50m' },
    ],
    practice: [
      { title: 'Kaggle Titanic: Machine Learning from Disaster', provider: 'Kaggle', url: 'https://www.kaggle.com/c/titanic', type: 'practice' },
      { title: 'Kaggle House Prices Advanced Regression', provider: 'Kaggle', url: 'https://www.kaggle.com/c/house-prices-advanced-regression-techniques', type: 'practice' },
    ],
  },
  'Deep Learning': {
    topic: 'Deep Learning & Neural Networks',
    category: 'AI/ML',
    summary: 'Feedforward Neural Networks, Backpropagation, Activation Functions, CNNs for computer vision, RNNs/Transformers, PyTorch, and TensorFlow.',
    why_it_matters: 'Deep learning powers state-of-the-art AI, including computer vision, generative AI, speech recognition, and large language models.',
    articles: [
      { title: 'PyTorch Official Tutorials', provider: 'PyTorch.org', url: 'https://pytorch.org/tutorials/', type: 'doc', duration: 'Official docs' },
      { title: 'Deep Learning Book', provider: 'Ian Goodfellow et al.', url: 'https://www.deeplearningbook.org/', type: 'article', duration: 'Comprehensive textbook' },
      { title: 'fast.ai Practical Deep Learning', provider: 'fast.ai', url: 'https://course.fast.ai/', type: 'article', duration: 'Free Course' },
    ],
    youtube: [
      { title: 'Neural Networks / Deep Learning Series', provider: '3Blue1Brown', url: 'https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi', type: 'video', duration: '4 videos' },
      { title: 'PyTorch for Deep Learning Bootcamp', provider: 'freeCodeCamp.org', url: 'https://www.youtube.com/watch?v=V_xro1bcAuA', type: 'video', duration: '25h complete' },
    ],
    practice: [
      { title: 'PyTorch Deep Learning with Examples', provider: 'PyTorch.org', url: 'https://pytorch.org/tutorials/beginner/pytorch_with_examples.html', type: 'practice' },
    ],
  },
  'Generative AI': {
    topic: 'Generative AI & LLMs',
    category: 'AI/ML',
    summary: 'Transformer architecture, Self-Attention, Large Language Models (LLMs), Prompt Engineering, Retrieval-Augmented Generation (RAG), and Fine-tuning.',
    why_it_matters: 'Generative AI and RAG architectures are the fastest-growing sector in modern software engineering and enterprise applications.',
    articles: [
      { title: 'Hugging Face Transformers Documentation', provider: 'HuggingFace.co', url: 'https://huggingface.co/docs/transformers/index', type: 'doc', duration: 'Official docs' },
      { title: 'LangChain Documentation', provider: 'LangChain', url: 'https://python.langchain.com/docs/introduction/', type: 'doc', duration: 'Official docs' },
      { title: 'Anthropic Prompt Engineering Guide', provider: 'Anthropic', url: 'https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview', type: 'article', duration: 'Guide' },
    ],
    youtube: [
      { title: 'Generative AI for Beginners', provider: 'freeCodeCamp.org', url: 'https://www.youtube.com/watch?v=mEsleV16qdo', type: 'video', duration: '2h 10m' },
      { title: "Let's build GPT: from scratch, in code", provider: 'Andrej Karpathy', url: 'https://www.youtube.com/watch?v=kCc8FmEb1nY', type: 'video', duration: '1h 56m' },
    ],
    practice: [
      { title: 'Hugging Face NLP Course', provider: 'Hugging Face', url: 'https://huggingface.co/learn/nlp-course/chapter1/1', type: 'practice' },
    ],
  },
  Docker: {
    topic: 'Docker & Containerization',
    category: 'DevOps',
    summary: 'Images, Containers, Dockerfiles, Docker Compose, Port mapping, Volumes, and multi-stage container builds.',
    why_it_matters: 'Containerization guarantees reproducibility and portability across development, staging, and production environments.',
    articles: [
      { title: 'Docker Official Getting Started Guide', provider: 'Docker.com', url: 'https://docs.docker.com/get-started/', type: 'doc', duration: 'Official docs' },
      { title: 'Docker Tutorial for Beginners', provider: 'GeeksforGeeks', url: 'https://www.geeksforgeeks.org/docker-tutorial/', type: 'article', duration: 'Guide' },
    ],
    youtube: [
      { title: 'Docker Tutorial for Beginners', provider: 'TechWorld with Nana', url: 'https://www.youtube.com/watch?v=3c-iBn73dDE', type: 'video', duration: '3h 00m' },
      { title: 'Docker in 100 Seconds', provider: 'Fireship', url: 'https://www.youtube.com/watch?v=Gjnup-PuquQ', type: 'video', duration: '2m 30s' },
    ],
    practice: [
      { title: 'Play with Docker Interactive Labs', provider: 'Docker', url: 'https://labs.play-with-docker.com/', type: 'practice' },
    ],
  },
  Git: {
    topic: 'Git & GitHub Version Control',
    category: 'DevOps & Collaboration',
    summary: 'Repositories, commits, branches, pull requests, merge conflicts, rebasing, and collaboration workflows.',
    why_it_matters: 'Version control is the essential backbone of every software team and portfolio repository.',
    articles: [
      { title: 'Git Official Documentation & Book', provider: 'Git-scm.com', url: 'https://git-scm.com/book/en/v2', type: 'doc', duration: 'Free Book' },
      { title: 'GitHub Skills Interactive Courses', provider: 'GitHub', url: 'https://skills.github.com/', type: 'article', duration: 'Interactive' },
    ],
    youtube: [
      { title: 'Git and GitHub for Beginners — Crash Course', provider: 'freeCodeCamp.org', url: 'https://www.youtube.com/watch?v=RGOj5yH7evk', type: 'video', duration: '1h 08m' },
    ],
    practice: [
      { title: 'Learn Git Branching (Visual Game)', provider: 'LearnGitBranching', url: 'https://learngitbranching.js.org/', type: 'practice' },
    ],
  },
};

/**
 * Helper to get guide by skill name, falling back to a clean default.
 */
export function getTopicGuide(skillName: string): TopicGuide {
  const match = Object.keys(TOPIC_GUIDES).find(
    (k) => k.toLowerCase() === skillName.toLowerCase() || skillName.toLowerCase().includes(k.toLowerCase())
  );
  if (match) {
    return TOPIC_GUIDES[match];
  }

  // General fallback guide with valid, high-reputation resources
  return {
    topic: skillName,
    category: 'Technical Skill',
    summary: `Comprehensive learning materials and verified video tutorials for mastering ${skillName}.`,
    why_it_matters: `${skillName} is a milestone topic in your learning roadmap that builds directly toward your career goal.`,
    articles: [
      { title: `${skillName} Tutorial & Documentation`, provider: 'GeeksforGeeks', url: `https://www.geeksforgeeks.org/search/?q=${encodeURIComponent(skillName)}`, type: 'doc' },
      { title: `Learn ${skillName}`, provider: 'W3Schools', url: `https://www.w3schools.com/`, type: 'article' },
      { title: 'freeCodeCamp News & Tutorials', provider: 'freeCodeCamp.org', url: `https://www.freecodecamp.org/news/search/?query=${encodeURIComponent(skillName)}`, type: 'article' },
    ],
    youtube: [
      { title: `${skillName} Full Tutorial for Beginners`, provider: 'freeCodeCamp.org / YouTube', url: `https://www.youtube.com/results?search_query=${encodeURIComponent(skillName + ' tutorial freecodecamp')}`, type: 'video' },
    ],
    practice: [
      { title: 'LeetCode Problem Solving', provider: 'LeetCode', url: 'https://leetcode.com/problemset/', type: 'practice' },
    ],
  };
}
