"""
Demo AI Provider — Fully deterministic, no API calls required.
Works completely offline. Used for hackathon demos and when no API key is configured.
Returns realistic, contextual responses based on user profile.
"""
import json
from typing import Dict, List, Any
from backend.app.ai.base import BaseAIProvider


class DemoProvider(BaseAIProvider):
    """
    Deterministic AI provider for demo/offline mode.
    All responses are pre-crafted to be realistic and contextual.
    """

    async def extract_profile(self, user_input: str) -> Dict[str, Any]:
        """Extract profile from natural language input using keyword matching."""
        user_lower = user_input.lower()
        
        # Detect target role
        role_keywords = {
            "AI/ML Engineer": ["machine learning engineer", "ml engineer", "ai engineer", "artificial intelligence"],
            "Data Scientist": ["data scientist", "data science"],
            "Data Analyst": ["data analyst", "data analysis"],
            "Software Engineer": ["software engineer", "software developer", "swe"],
            "Frontend Developer": ["frontend", "front-end", "ui developer", "react developer"],
            "Backend Developer": ["backend", "back-end", "server-side"],
            "Full Stack Developer": ["full stack", "fullstack"],
            "Cloud Engineer": ["cloud engineer", "cloud architect"],
            "DevOps Engineer": ["devops", "site reliability", "sre"],
            "Cybersecurity Analyst": ["cybersecurity", "security analyst", "ethical hacker"],
        }
        
        target_role = "Software Engineer"
        for role, keywords in role_keywords.items():
            if any(kw in user_lower for kw in keywords):
                target_role = role
                break
        
        # Detect experience level
        experience = "intermediate"
        if any(w in user_lower for w in ["beginner", "new to", "just started", "no experience", "student", "fresher"]):
            experience = "beginner"
        elif any(w in user_lower for w in ["senior", "expert", "years of experience", "experienced"]):
            experience = "advanced"
        
        # Detect weekly hours
        weekly_hours = 10.0
        if "30 min" in user_lower or "half hour" in user_lower:
            weekly_hours = 3.5
        elif "1 hour" in user_lower or "one hour" in user_lower:
            weekly_hours = 7.0
        elif "2 hour" in user_lower or "two hour" in user_lower:
            weekly_hours = 14.0
        elif "3 hour" in user_lower or "three hour" in user_lower:
            weekly_hours = 21.0
        elif "10 hour" in user_lower:
            weekly_hours = 10.0
        
        # Detect known skills
        skill_keywords = {
            "Python": ["python"],
            "SQL": ["sql"],
            "JavaScript": ["javascript", "js"],
            "Statistics": ["statistics", "stats"],
            "Machine Learning": ["machine learning", "ml"],
            "DSA": ["dsa", "data structures", "algorithms"],
            "React": ["react"],
            "Docker": ["docker"],
        }
        
        detected_skills = {}
        for skill, keywords in skill_keywords.items():
            for kw in keywords:
                if kw in user_lower:
                    # Determine level from context
                    if any(w in user_lower for w in [f"know {kw}", f"good at {kw}", f"know {kw} well"]):
                        detected_skills[skill] = 3
                    elif any(w in user_lower for w in [f"basic {kw}", f"beginner {kw}", f"learning {kw}"]):
                        detected_skills[skill] = 2
                    elif any(w in user_lower for w in [f"expert {kw}", f"advanced {kw}"]):
                        detected_skills[skill] = 4
                    else:
                        detected_skills[skill] = 2
                    break
        
        return {
            "target_role": target_role,
            "experience_level": experience,
            "weekly_hours": weekly_hours,
            "current_skills": detected_skills,
            "career_goal": f"Become a professional {target_role}",
        }

    async def generate_explanation(self, context: Dict[str, Any]) -> str:
        """Generate contextual explanation for a recommendation."""
        resource = context.get("resource", {})
        profile = context.get("profile", {})
        skill_gaps = context.get("skill_gaps", [])
        
        resource_title = resource.get("title", "this resource")
        resource_skills = resource.get("skills", [])
        target_role = profile.get("target_role", "your target role")
        
        # Find the matching gap
        matching_gaps = [g for g in skill_gaps if g.get("skill_name") in resource_skills]
        
        if matching_gaps:
            gap = matching_gaps[0]
            skill_name = gap["skill_name"]
            current = gap["current_level"]
            target = gap["target_level"]
            priority = gap["priority"].upper()
            
            return (
                f"You're targeting **{target_role}** and your current **{skill_name}** level is "
                f"{current}/5, but the role requires {target}/5 — a {priority} priority gap. "
                f"**{resource_title}** directly addresses this gap with structured content "
                f"that will bring you significantly closer to your goal."
            )
        
        if resource_skills:
            skills_str = ", ".join(resource_skills[:2])
            return (
                f"**{resource_title}** covers {skills_str}, which are core competencies for a "
                f"{target_role}. Based on your profile, this resource matches your current "
                f"skill level and preferred learning style."
            )
        
        return (
            f"**{resource_title}** is highly recommended for your journey to become a {target_role}. "
            f"It aligns with your current skill level and fills key gaps in your learning path."
        )

    async def chat(self, messages: List[Dict], context: Dict[str, Any]) -> str:
        """Generate contextual AI mentor responses with multilingual support."""
        if not messages:
            return self._welcome_message(context)

        last_message = messages[-1].get("content", "")
        last_lower = last_message.lower()
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "Software Engineer")
        skill_gaps = context.get("skill_gaps", [])

        # Detect language
        lang = self._detect_language(last_message)

        # Route to appropriate response based on user intent
        # Check both English and Hindi/Hinglish keywords
        if any(w in last_lower for w in ["today", "study today", "do today", "what should i", "aaj", "padhu", "kya padu", "kya seekhu"]):
            response = self._today_recommendation(context)
        elif any(w in last_lower for w in ["struggling", "difficult", "hard", "don't understand", "confused",
                                            "samajh nahi", "samajh nahin", "samajh aa", "nahi aa raha", "mushkil",
                                            "problem", "dikkat"]):
            response = self._struggling_response(last_lower, context)
        elif any(w in last_lower for w in ["skip", "already know", "i know", "pehle se", "aata hai", "pta hai", "pata hai"]):
            response = self._skip_response(last_lower, context)
        elif any(w in last_lower for w in ["why", "why did you", "why this", "recommend", "kyun", "kyu", "matlab"]):
            response = self._explanation_response(context)
        elif any(w in last_lower for w in ["project", "build", "make something", "banau", "koi project", "kya banaun"]):
            response = self._project_recommendation(context)
        elif any(w in last_lower for w in ["roadmap", "path", "plan", "change", "next", "aage", "kya karu", "kya karun"]):
            response = self._roadmap_response(context)
        elif any(w in last_lower for w in ["only have", "30 minutes", "1 hour", "limited time", "sirf", "thoda time", "busy"]):
            response = self._time_limited_response(last_lower, context)
        elif any(w in last_lower for w in ["failed", "fail", "didn't pass", "low score", "fail ho gaya", "nahi hua pass"]):
            response = self._failed_assessment_response(context)
        elif any(w in last_lower for w in ["hello", "hi", "hey", "start", "namaste", "hii", "helo"]):
            response = self._welcome_message(context)
        elif any(concept in last_lower for concept in ["recursion", "loop", "array", "list", "dict", "class",
                                                        "function", "gradient", "neural", "regression", "sql",
                                                        "join", "api", "docker", "git", "algorithm", "complexity",
                                                        "overfitting", "bias", "variance", "clustering"]):
            response = self._concept_explanation(last_lower, context, lang=lang)
        else:
            response = self._general_mentor_response(last_lower, context)

        # Add Hindi/Hinglish prefix if needed
        if lang == "hindi":
            return self._hindi_prefix() + "\n\n" + response
        elif lang == "hinglish":
            return self._hinglish_note() + response

        return response

    def _detect_language(self, text: str) -> str:
        """Detect if text is Hindi, Hinglish, or English using word-boundary matching."""
        import re
        # Hindi Devanagari script detection
        if any('\u0900' <= c <= '\u097f' for c in text):
            return "hindi"

        # Hinglish keywords — use word-boundary matching to avoid false positives
        # e.g. 'ek' must NOT match inside 'like', 'make', 'beginner', 'take'
        hinglish_markers = [
            "mujhe", "kaise", "kya", "hai", "nahi", "nahin", "bhai", "yaar",
            "samajh", "batao", "samjhao", "seekhna", "sikho", "padhu",
            "matlab", "acha", "theek", "haan", "bahut", "thoda", "accha",
            "zyada", "karo", "pehle", "baad", "phir", "aaj", "seekhu",
            "aata", "padh", "karu", "karun", "banaun",
        ]
        text_lower = text.lower()
        matched = sum(
            1 for w in hinglish_markers
            if re.search(r'\b' + re.escape(w) + r'\b', text_lower)
        )
        if matched >= 2:
            return "hinglish"

        return "english"

    def _hindi_prefix(self) -> str:
        return (
            "🤖 *मैं LearnPath AI हूँ — Demo Mode में।*\n"
            "*(Note: Real AI provider के साथ और भी detailed Hindi responses मिलेंगे!)*"
        )

    def _hinglish_note(self) -> str:
        return ""  # No prefix needed for Hinglish, just respond naturally



    async def interpret_feedback(self, feedback: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Interpret user feedback and determine roadmap adaptation."""
        feedback_lower = feedback.lower()
        
        if any(w in feedback_lower for w in ["too easy", "easy", "boring", "already know"]):
            return {
                "action": "increase_difficulty",
                "reason": "User found content too easy",
                "adjustment": "skip_to_next_level",
                "message": "I've updated your roadmap to skip beginner content and focus on intermediate/advanced topics.",
            }
        
        elif any(w in feedback_lower for w in ["too hard", "difficult", "struggling", "confusing"]):
            return {
                "action": "add_prerequisites",
                "reason": "User is struggling with current content",
                "adjustment": "add_prerequisite_resources",
                "message": "I've added foundational resources before the current topic to build a stronger base.",
            }
        
        elif any(w in feedback_lower for w in ["less time", "busy", "only have"]):
            hours = 5.0  # default reduction
            return {
                "action": "reduce_weekly_hours",
                "reason": "User has less time available",
                "adjustment": "compress_timeline",
                "new_weekly_hours": hours,
                "message": f"I've recalculated your roadmap for {hours} hours/week. Your timeline has been extended but the key skills remain covered.",
            }
        
        elif any(w in feedback_lower for w in ["more time", "free", "available"]):
            return {
                "action": "increase_weekly_hours",
                "reason": "User has more time available",
                "adjustment": "expand_content",
                "new_weekly_hours": 20.0,
                "message": "Great! I've added more projects and depth to accelerate your learning.",
            }
        
        elif any(w in feedback_lower for w in ["not relevant", "not useful", "wrong track"]):
            return {
                "action": "refilter_recommendations",
                "reason": "User finds content not relevant",
                "adjustment": "update_goal_mapping",
                "message": "Thanks for the feedback! I've updated your recommendations to better match your goal.",
            }
        
        return {
            "action": "acknowledge",
            "reason": "General feedback received",
            "message": "Thanks for your feedback! I'll keep learning from it to improve your recommendations.",
        }

    # ─── Private Response Generators ──────────────────────────────────────
    def _welcome_message(self, context: Dict) -> str:
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "your target role")
        skill_gaps = context.get("skill_gaps", [])
        
        top_gap = skill_gaps[0]["skill_name"] if skill_gaps else "core skills"
        
        return (
            f"👋 Welcome! I'm your AI learning mentor.\n\n"
            f"I can see you're working toward becoming a **{target_role}**. "
            f"Based on your profile, your top priority right now is building your **{top_gap}** skills.\n\n"
            f"Here's how I can help you:\n"
            f"- 📚 **What should I study today?** — I'll create a focused daily plan\n"
            f"- 🗺️ **Explain my roadmap** — Understand why each step matters\n"
            f"- 💡 **I'm struggling with [topic]** — Get targeted help\n"
            f"- ⏰ **I only have 30 minutes** — Quick session recommendations\n"
            f"- 🔨 **What project should I build?** — Practical application\n\n"
            f"What would you like to work on today?"
        )

    def _today_recommendation(self, context: Dict) -> str:
        profile = context.get("profile", {})
        skill_gaps = context.get("skill_gaps", [])
        weekly_hours = profile.get("weekly_hours", 10)
        daily_hours = weekly_hours / 5
        roadmap = context.get("roadmap") or {}
        milestone = context.get("current_milestone") or {}
        milestone_title = milestone.get("title") if isinstance(milestone, dict) else None
        
        top_gap = skill_gaps[0]["skill_name"] if skill_gaps else "core skills"
        phase = roadmap.get("current_phase") or "your current roadmap phase"
        
        return (
            f"🎯 **Today's Learning Plan** ({daily_hours:.1f} hours)\n\n"
            f"**Priority: {top_gap}** (your highest-impact gap)\n"
            f"**Roadmap phase:** {phase}"
            + (f"\n**Milestone:** {milestone_title}" if milestone_title else "")
            + "\n\nHere's your focused plan for today:\n\n"
            f"1. 📺 **30 min** — Watch the next lesson in your {top_gap} module\n"
            f"2. ✏️ **15 min** — Complete the practice exercises\n"
            f"3. 🔨 **20 min** — Apply to your current project\n\n"
            f"💡 *Pro tip: Even 30 minutes of focused study beats 2 hours of distracted learning.*\n\n"
            f"Ready to start? I can give you the specific resource link."
        )

    def _struggling_response(self, message: str, context: Dict) -> str:
        skill_gaps = context.get("skill_gaps", [])
        topic = "this topic"
        
        # Try to extract the topic from the message
        for gap in skill_gaps:
            if gap["skill_name"].lower() in message:
                topic = gap["skill_name"]
                break
        
        return (
            f"😊 It's completely normal to find {topic} challenging — it's one of the trickier concepts!\n\n"
            f"Here's my recommended approach:\n\n"
            f"**Step 1: Go back to basics**\n"
            f"Sometimes the struggle means we need to strengthen prerequisites. "
            f"Let me check your foundational skills.\n\n"
            f"**Step 2: Try a different explanation**\n"
            f"Every person learns differently. If videos aren't clicking, try:\n"
            f"- Reading the official documentation\n"
            f"- Working through a hands-on tutorial\n"
            f"- Watching a different instructor's explanation\n\n"
            f"**Step 3: Practice with smaller examples**\n"
            f"Break the concept into tiny pieces and master each one before combining them.\n\n"
            f"Would you like me to add some prerequisite resources to your roadmap, or find a simpler explanation of {topic}?"
        )

    def _skip_response(self, message: str, context: Dict) -> str:
        return (
            f"✅ Got it! If you already know this skill, we can skip the beginner content.\n\n"
            f"I'll update your roadmap to:\n"
            f"1. Mark this topic as **verified** ✓\n"
            f"2. Move you to the **next phase** of your roadmap\n"
            f"3. Adjust the timeline accordingly\n\n"
            f"⚠️ **Quick verification**: Would you like to take a 5-minute assessment to confirm your level? "
            f"This ensures we don't skip anything that might cause issues later in your learning journey.\n\n"
            f"- **Yes, let me verify** — Take a quick assessment\n"
            f"- **Skip and continue** — Trust your self-assessment"
        )

    def _explanation_response(self, context: Dict) -> str:
        profile = context.get("profile", {})
        skill_gaps = context.get("skill_gaps", [])
        target_role = profile.get("target_role", "your target role")
        
        if skill_gaps:
            top_gap = skill_gaps[0]
            return (
                f"🔍 **Why this recommendation?**\n\n"
                f"Here's exactly why I recommended this:\n\n"
                f"**Your Goal:** {target_role}\n"
                f"**Critical Gap:** {top_gap['skill_name']} (currently {top_gap['current_level']}/5, need {top_gap['target_level']}/5)\n"
                f"**Gap Priority:** {top_gap['priority'].upper()}\n\n"
                f"This resource was selected because:\n"
                f"✅ It directly addresses your **{top_gap['priority']}** priority gap\n"
                f"✅ The difficulty matches your current skill level\n"
                f"✅ It fits your available study time\n"
                f"✅ Prerequisites are already covered in your roadmap\n\n"
                f"Closing the {top_gap['skill_name']} gap will unlock the next major milestone in your roadmap."
            )
        
        return (
            f"🔍 **Why this recommendation?**\n\n"
            f"This resource was selected based on:\n\n"
            f"1. **Goal alignment** — Directly relevant to becoming a {target_role}\n"
            f"2. **Skill gaps** — Addresses areas where you need the most improvement\n"
            f"3. **Prerequisites** — You've already covered the necessary foundations\n"
            f"4. **Learning style** — Matches your preferred learning format\n"
            f"5. **Time fit** — Duration fits your study schedule\n\n"
            f"Every recommendation I make combines these factors to maximize your learning efficiency."
        )

    def _project_recommendation(self, context: Dict) -> str:
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "Software Engineer")
        
        projects_by_role = {
            "AI/ML Engineer": "🤖 **Customer Churn Prediction** — Build an end-to-end ML pipeline with data preprocessing, model training, and evaluation. Real dataset from Kaggle.",
            "Data Scientist": "📊 **Sales Forecasting Dashboard** — Analyze historical sales data, build predictive models, and create an interactive dashboard.",
            "Frontend Developer": "🎨 **Portfolio Website** — Build a responsive personal portfolio with animations, dark mode, and contact form.",
            "Backend Developer": "⚙️ **REST API with Authentication** — Build a blog API with JWT auth, CRUD operations, and PostgreSQL.",
            "Software Engineer": "🧮 **Algorithm Visualizer** — Interactive web app that visualizes sorting and graph algorithms step by step.",
        }
        
        project = projects_by_role.get(target_role, "🔨 **Full-Stack Application** — Build a complete web application with frontend, backend, and database.")
        
        return (
            f"🚀 **Project Recommendation for {target_role}**\n\n"
            f"{project}\n\n"
            f"**Why this project?**\n"
            f"- Directly relevant to {target_role} job interviews\n"
            f"- Uses the skills you're currently learning\n"
            f"- Portfolio-worthy for job applications\n"
            f"- Appropriate difficulty for your current level\n\n"
            f"**Getting Started:**\n"
            f"1. Start with the dataset/requirements\n"
            f"2. Plan your architecture before coding\n"
            f"3. Build incrementally (don't try to do everything at once)\n"
            f"4. Document everything — this goes on GitHub\n\n"
            f"Want me to break this down into smaller weekly tasks?"
        )

    def _roadmap_response(self, context: Dict) -> str:
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "your goal")
        roadmap = context.get("roadmap") or {}
        title = roadmap.get("title") or f"{target_role} roadmap"
        weeks = roadmap.get("total_weeks") or "several"
        phase = roadmap.get("current_phase") or "the first incomplete phase"
        
        return (
            f"🗺️ **Your Learning Roadmap**\n\n"
            f"You currently have **{title}** ({weeks} weeks). Next focus: **{phase}**.\n\n"
            f"Your personalized path to **{target_role}** is built on 3 principles:\n\n"
            f"**1. Prerequisites First** 🔗\n"
            f"Every topic is ordered so you always have the foundation needed for the next step.\n\n"
            f"**2. Skill Gap Priority** 🎯\n"
            f"We focus first on the skills with the biggest gaps that matter most for {target_role}.\n\n"
            f"**3. Adaptive Timeline** ⏱️\n"
            f"Your roadmap adjusts based on your available time and progress.\n\n"
            f"Want to **adapt your roadmap**? You can:\n"
            f"- Change weekly available hours\n"
            f"- Mark skills as already known\n"
            f"- Adjust your target deadline\n"
            f"- Reprioritize specific skills\n\n"
            f"Just tell me what you'd like to change!"
        )

    def _time_limited_response(self, message: str, context: Dict) -> str:
        # Extract time from message
        time_str = "30 minutes"
        if "1 hour" in message or "one hour" in message:
            time_str = "1 hour"
            tasks = ["Watch one lesson video (30 min)", "Complete 2-3 practice problems (20 min)", "Review notes (10 min)"]
        elif "30 min" in message or "30 minutes" in message:
            time_str = "30 minutes"
            tasks = ["Focus on one concept only", "Watch a short video (15 min)", "Do 1-2 exercises (15 min)"]
        else:
            tasks = ["Quick concept review (15 min)", "1 practice exercise (15 min)"]
        
        tasks_str = "\n".join(f"  {i+1}. {t}" for i, t in enumerate(tasks))
        
        skill_gaps = context.get("skill_gaps") or []
        top_gap = skill_gaps[0]["skill_name"] if skill_gaps else "your next roadmap skill"
        roadmap = context.get("roadmap") or {}
        phase = roadmap.get("current_phase")
        
        return (
            f"⏰ **{time_str} Learning Sprint**\n\n"
            f"Focus this session on **{top_gap}**"
            + (f" in **{phase}**." if phase else ".")
            + "\n\nHere's a focused plan for your available time:\n\n"
            f"{tasks_str}\n\n"
            f"💡 *Short sessions can be just as effective — consistency beats duration.*\n\n"
            f"Even 30 minutes a day adds up to 15 hours a month. That's significant progress!\n\n"
            f"Ready to start? I'll track this session and adjust your roadmap timeline accordingly."
        )

    def _failed_assessment_response(self, context: Dict) -> str:
        skill_gaps = context.get("skill_gaps", [])
        
        return (
            f"💪 **Don't worry — failing an assessment is part of learning!**\n\n"
            f"Here's what I recommend:\n\n"
            f"**Immediate Steps:**\n"
            f"1. Review the questions you got wrong — identify the specific concepts\n"
            f"2. Go back to the lesson materials for those topics\n"
            f"3. Try the practice exercises again\n\n"
            f"**I've Updated Your Roadmap:**\n"
            f"- Added targeted review resources for weak areas\n"
            f"- Scheduled a re-assessment in 1 week\n"
            f"- Adjusted your timeline slightly to ensure solid understanding\n\n"
            f"**Remember:**\n"
            f"Scoring 70% on a first attempt with a solid review plan is better than "
            f"memorizing 100% and forgetting it in a week.\n\n"
            f"Which specific concepts felt most confusing? I can recommend targeted resources."
        )

    def _concept_explanation(self, message: str, context: Dict, lang: str = "english") -> str:
        """Explain programming/ML concepts in a simple, structured way."""
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "Software Engineer")
        is_hinglish = lang in ("hinglish", "hindi")

        concept_map_en = {
            "recursion": (
                "**Recursion** — A function that calls itself! 🧠\n\n"
                "**Simple idea:** Break a big problem into smaller identical subproblems until you hit the simplest case.\n\n"
                "**Real-world analogy:** Imagine looking up a word in a dictionary — the definition uses another word you need to look up too, until you reach a word you already know.\n\n"
                "**Code example:**\n```python\ndef factorial(n):\n    if n == 0:  # base case — STOP!\n        return 1\n"
                "    return n * factorial(n - 1)  # call itself with smaller problem\n\nfactorial(5)  # = 5 × 4 × 3 × 2 × 1 = 120\n```\n\n"
                "**Two rules of recursion:**\n1. Always have a **base case** (otherwise infinite loop!)\n"
                "2. Each call must move **closer to the base case**\n\n"
                "**Quick recap:** Function → calls itself with smaller input → base case → unwinds! 🎉"
            ),
            "overfitting": (
                "**Overfitting** — When your model memorizes instead of learning! 🎯\n\n"
                "**Simple idea:** The model learns the training data too well — including its noise — so it fails on new data.\n\n"
                "**Real-world analogy:** A student who memorizes every past exam question word-for-word. "
                "They score 100% on practice papers but fail the real exam because the questions are slightly different.\n\n"
                "**Symptoms:**\n- Training accuracy: 99% ✅\n- Test accuracy: 60% ❌\n\n"
                "**Fixes:**\n1. Get more training data\n2. Use regularization (L1/L2)\n3. Dropout (for neural nets)\n"
                "4. Reduce model complexity\n5. Cross-validation\n\n"
                "**Bias-Variance tradeoff:** Overfitting = low bias, high variance. You want the sweet spot!"
            ),
            "gradient": (
                "**Gradient Descent** — An optimization algorithm! ⛰️\n\n"
                "**Simple idea:** Minimize a loss function by repeatedly stepping in the direction of steepest descent.\n\n"
                "**Analogy:** You're blindfolded on a hilly landscape trying to reach the lowest point. "
                "At each step, you feel the slope and take a small step downhill. Repeat until flat.\n\n"
                "**Math:**\n```\nw = w - learning_rate × gradient_of_loss\n```\n\n"
                "**Types:**\n- Batch GD: Uses all data (accurate but slow)\n"
                "- SGD: Uses 1 sample (fast but noisy)\n"
                "- Mini-batch GD: Uses small batches (best balance) ✅\n\n"
                "**Learning rate matters:** Too high → overshoots the minimum. Too low → takes forever."
            ),
            "sql": (
                "**SQL Joins** — The most important SQL concept! 🔗\n\n"
                "```\nusers table:      orders table:\nid | name         id | user_id | item\n1  | Alice        1  | 1       | Phone\n2  | Bob          2  | 1       | Laptop\n3  | Charlie      3  | 2       | Book\n```\n\n"
                "**INNER JOIN** — Only matching rows:\n"
                "```sql\nSELECT users.name, orders.item\nFROM users INNER JOIN orders ON users.id = orders.user_id;\n-- Result: Alice→Phone, Alice→Laptop, Bob→Book\n```\n\n"
                "**LEFT JOIN** — All left table rows + matching right:\n"
                "```sql\n-- Charlie appears even with no orders (NULL)\n```\n\n"
                "**Memory trick:** INNER = intersection, LEFT = keep all left, RIGHT = keep all right, FULL = keep everything"
            ),
        }

        concept_map_hinglish = {
            "recursion": (
                "**Recursion** — Simple se samjhte hain! 🧠\n\n"
                "**Simple idea:** Ek function jo khud ko hi call karta hai.\n\n"
                "**Real-world analogy:** Socho tum ek room ke andar ho, aur us room mein ek aur chhota room hai — "
                "jab tak ek empty room na mile. Recursion wahi karta hai!\n\n"
                "**Code example:**\n```python\ndef factorial(n):\n    if n == 0:  # base case — STOP!\n        return 1\n"
                "    return n * factorial(n - 1)  # khud ko call karo\n\nfactorial(5)  # = 120\n```\n\n"
                "**Yaad rakho:** Base case zaroori hai, warna infinite loop ho jaayega! 🔁"
            ),
            "overfitting": (
                "**Overfitting** — Samjho ek student ki tarah! 🎯\n\n"
                "**Problem:** Model ne training data ko zyada yaad kar liya — patterns ki jagah examples.\n\n"
                "**Analogy:** Ek student jo sirf purane papers yaad karta hai. Exam mein new question aaye toh fail! 😅\n\n"
                "**Symptoms:**\n- Training accuracy: 99% ✅\n- Test accuracy: 60% ❌\n\n"
                "**Solutions:**\n1. Zyada data lao\n2. Regularization (L1/L2)\n3. Dropout use karo\n4. Simple model banao\n\n"
                "**Key:** Low bias, high variance = overfitting. Balance chahiye!"
            ),
            "gradient": (
                "**Gradient Descent** — Samjho pahaad se utarne ki tarah! ⛰️\n\n"
                "**Simple idea:** Loss function minimize karna — downhill steps leke.\n\n"
                "**Analogy:** Andhere mein pahaad se utarna hai. Har step pe feel karo — neeche kaunsi direction hai? "
                "Us taraf chalo jab tak valley mein na pahuncho.\n\n"
                "**Math:**\n```\nw = w - learning_rate × gradient\n```\n\n"
                "**Types:**\n- Batch GD: Slow but accurate\n- SGD: Fast but noisy\n- Mini-batch: Best ✅\n\n"
                "**Learning rate:** Zyada bada → overshoot. Zyada chhota → bahut slow."
            ),
            "sql": (
                "**SQL Joins** — Bahut important concept! 🔗\n\n"
                "**INNER JOIN:** Sirf matching rows aate hain\n"
                "**LEFT JOIN:** Left table ke saare rows aate hain, right ke sirf matching\n\n"
                "```sql\nSELECT users.name, orders.item\nFROM users INNER JOIN orders ON users.id = orders.user_id;\n```\n\n"
                "**Trick:** Socho Venn diagram — INNER = intersection, LEFT = left circle poora!"
            ),
        }

        concept_map = concept_map_hinglish if is_hinglish else concept_map_en

        # Find matching concept
        for key, explanation in concept_map.items():
            if key in message:
                return explanation

        # Generic concept help
        return (
            f"Great question! Let me explain this concept step by step. 🧠\n\n"
            f"**My approach for explaining any concept:**\n\n"
            f"1. **Simple summary** — What is it in one sentence?\n"
            f"2. **Real-world analogy** — How does it relate to everyday life?\n"
            f"3. **Example** — Show it in action\n"
            f"4. **Code/formula** — The technical representation\n"
            f"5. **Common pitfalls** — What to watch out for\n\n"
            f"Could you be more specific about which concept you want explained? "
            f"I can give you a detailed breakdown of any topic in your {target_role} roadmap!\n\n"
            f"For example: *\"Explain recursion\"*, *\"What is overfitting?\"*, *\"How does gradient descent work?\"*"
        )



    def _general_mentor_response(self, message: str, context: Dict) -> str:
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "your goal")
        skill_gaps = context.get("skill_gaps", [])
        top_gap = skill_gaps[0]["skill_name"] if skill_gaps else "core skills"

        return (
            f"I'm here to help you on your journey to become a **{target_role}**! 🚀\n\n"
            f"Based on your profile, your current focus should be **{top_gap}**.\n\n"
            f"Here's what I can help you with — just ask naturally:\n\n"
            f"📚 **Concept explanations** — *\"Explain recursion\"* / *\"Recursion samjhao\"*\n"
            f"🎯 **Daily plan** — *\"What should I study today?\"* / *\"Aaj kya padu?\"*\n"
            f"🗺️ **Roadmap help** — *\"What's my next step?\"* / *\"Aage kya karun?\"*\n"
            f"💡 **I'm stuck** — *\"I'm struggling with SQL joins\"* / *\"SQL samajh nahi aa raha\"*\n"
            f"⏰ **Short sessions** — *\"I only have 30 minutes\"* / *\"Sirf thoda time hai\"*\n"
            f"🔨 **Projects** — *\"What project should I build?\"*\n"
            f"📊 **Interview prep** — *\"Help me prepare for ML interviews\"*\n\n"
            f"Ask me anything — in English, Hindi, or Hinglish! 😊"
        )
