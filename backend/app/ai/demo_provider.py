"""
Demo AI Provider — Fully deterministic, no API calls required.
Works completely offline. Used for hackathon demos and when no API key is configured.
Returns realistic, contextual responses based on user profile.
"""
import json
from typing import Dict, List, Any
from app.ai.base import BaseAIProvider


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
        """Generate contextual, conversational AI mentor responses with multi-turn memory and multilingual support."""
        if not messages:
            return self._welcome_message(context)

        last_message = messages[-1].get("content", "")
        last_lower = last_message.lower()
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "Software Engineer")
        skill_gaps = context.get("skill_gaps", [])

        # Detect language
        lang = self._detect_language(last_message)

        # Look back at conversation history to understand context for follow-up questions
        previous_text = " ".join([m.get("content", "").lower() for m in messages[:-1][-3:]])
        combined_context_text = f"{previous_text} {last_lower}"

        # 1. Check for follow-up queries like "ek example de", "aur samjhao", "code dikhao"
        is_follow_up = any(f in last_lower for f in [
            "example", "udaharan", "code", "aur", "dikhao", "de", "do", "explain more",
            "show me", "isko python", "samjhao aur", "example batao"
        ]) and len(last_lower.split()) <= 6

        # 2. Check for Exam / Test / Interview prep
        if any(w in last_lower for w in ["exam", "kal exam", "parso exam", "interview", "test hai", "kya padhu exam", "exam preparation"]):
            response = self._exam_prep_response(last_lower, context, lang=lang)
        # 3. Follow-up example resolution
        elif is_follow_up and previous_text:
            response = self._follow_up_response(previous_text, last_lower, context, lang=lang)
        # 4. Routine intents
        elif any(w in last_lower for w in ["today", "study today", "do today", "what should i", "aaj", "padhu", "kya padu", "kya seekhu"]):
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
        elif any(w in last_lower for w in ["hello", "hi", "hey", "start", "namaste", "hii", "helo", "kese ho", "kaise ho"]):
            response = self._welcome_message(context)
        elif any(concept in combined_context_text for concept in [
            "recursion", "loop", "array", "list", "dict", "class", "oop", "inheritance", "polymorphism",
            "encapsulation", "abstraction", "function", "gradient", "neural", "regression", "sql",
            "join", "api", "docker", "git", "algorithm", "complexity", "overfitting", "bias", "variance",
            "clustering", "dp", "dynamic programming", "tree", "binary search"
        ]):
            response = self._concept_explanation(combined_context_text, context, lang=lang)
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

    def _exam_prep_response(self, message: str, context: Dict, lang: str = "english") -> str:
        """Personalized study plan for exams and tests."""
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "Software Engineer")
        skill_gaps = context.get("skill_gaps", [])
        top_gaps = [g["skill_name"] for g in skill_gaps[:3]] if skill_gaps else ["Core Fundamentals", "Problem Solving"]
        roadmap = context.get("roadmap") or {}
        current_phase = roadmap.get("current_phase") or "Current Phase"

        if lang in ("hinglish", "hindi"):
            return (
                f"🚨 **Tension mat le bhai! 😄 Smart revision plan banate hain.**\n\n"
                f"Target Role: **{target_role}** | Current Focus: **{current_phase}**\n\n"
                f"Kal/Upcoming exam ke liye yeh 3-Step Strategy follow karo:\n\n"
                f"⏱️ **Block 1 (First 2 Hours) — High-Yield Core Concepts:**\n"
                f"• **{top_gaps[0] if len(top_gaps) > 0 else 'Core Concept'}**: Formulas, definitions, aur key syntax revise karo.\n"
                f"• **{top_gaps[1] if len(top_gaps) > 1 else 'Problem Solving'}**: Most repeated questions aur standard patterns dekho.\n\n"
                f"💻 **Block 2 (1.5 Hours) — Hands-On / Code Practice:**\n"
                f"• 3-4 standard code questions khud likh ke dry-run karo.\n"
                f"• Edge cases (e.g. empty input, base cases) check karo.\n\n"
                f"🧠 **Block 3 (Final 30 Mins) — Rapid Cheat Sheet Review:**\n"
                f"• Summary notes aur quick formulas dekho.\n"
                f"• Der raat tak mat jaagna — 7 hours sleep zaroori hai memory consolidation ke liye! 💤\n\n"
                f"Kisi specific topic ka quick recap ya code example chahiye toh batao, abhi samjhaata hoon!"
            )

        return (
            f"🎯 **Targeted Exam / Interview Prep Strategy**\n\n"
            f"Target: **{target_role}** | Key Focus: **{current_phase}**\n\n"
            f"Here is your high-efficiency revision breakdown:\n\n"
            f"**Phase 1: High-Weightage Core Revision (45%)**\n"
            f"- Prioritize your critical gaps: **{', '.join(top_gaps)}**.\n"
            f"- Review fundamental definitions, invariants, and syntax.\n\n"
            f"**Phase 2: Pattern Practice & Dry Runs (40%)**\n"
            f"- Solve 2-3 canonical scenario questions without looking at solutions.\n"
            f"- Practice calculating Big-O time and space complexity.\n\n"
            f"**Phase 3: Formula & Cheat Sheet Recap (15%)**\n"
            f"- Quick scan of key APIs, parameters, and edge cases.\n"
            f"- Rest well before the exam to keep your problem-solving sharp!\n\n"
            f"Which topic would you like a fast 2-minute summary on right now?"
        )

    def _follow_up_response(self, previous_text: str, current_message: str, context: Dict, lang: str = "english") -> str:
        """Handle conversational follow-ups like 'ek example de', 'code dikhao', 'aur samjhao'."""
        is_hinglish = lang in ("hinglish", "hindi")

        # Detect what concept they were discussing
        if any(w in previous_text for w in ["inheritance", "inherit"]):
            if is_hinglish:
                return (
                    "**Inheritance ka Simple Code Example:** 👨‍👦\n\n"
                    "```python\n# Parent Class (Super Class)\nclass Car:\n    def __init__(self, brand):\n        self.brand = brand\n    \n    def drive(self):\n        return f'{self.brand} car chal rahi hai! 🚗'\n\n"
                    "# Child Class (Sub Class) — Inherits from Car\nclass ElectricCar(Car):\n    def __init__(self, brand, battery_kwh):\n        super().__init__(brand)  # Parent constructor call\n        self.battery_kwh = battery_kwh\n    \n    def charge(self):\n        return f'{self.brand} charging... 🔋'\n\n"
                    "# Usage\ntesla = ElectricCar('Tesla', 75)\nprint(tesla.drive())   # Output: Tesla car chal rahi hai! (Parent ka method)\nprint(tesla.charge())  # Output: Tesla charging... (Child ka apna method)\n```\n\n"
                    "**Samajh aaya?** `ElectricCar` ne `Car` ki saari properties inherit kar li bina dubara code likhe! 🎉"
                )
            return (
                "**Inheritance Code Example:** 👨‍👦\n\n"
                "```python\nclass Vehicle:\n    def __init__(self, name):\n        self.name = name\n    def move(self):\n        return f'{self.name} is moving.'\n\n"
                "class ElectricCar(Vehicle):\n    def __init__(self, name, battery_capacity):\n        super().__init__(name)\n        self.battery_capacity = battery_capacity\n\n"
                "tesla = ElectricCar('Tesla Model 3', '75kWh')\nprint(tesla.move())  # Inherited from Vehicle\n```\n\n"
                "`ElectricCar` reuses `Vehicle` functionality without code duplication."
            )

        if any(w in previous_text for w in ["recursion", "factorial"]):
            if is_hinglish:
                return (
                    "**Recursion ka Step-by-Step Execution:** 🔁\n\n"
                    "Dekh bhai `factorial(4)` kaise execute hota hai:\n\n"
                    "```python\ndef fact(n):\n    if n <= 1: return 1   # Base Case (Ruk jao)\n    return n * fact(n - 1) # Recursive Call\n```\n\n"
                    "**Call Stack:**\n"
                    "1. `fact(4)` = 4 * `fact(3)`\n"
                    "2. `fact(3)` = 3 * `fact(2)`\n"
                    "3. `fact(2)` = 2 * `fact(1)`\n"
                    "4. `fact(1)` returns 1 (Base case reached!)\n"
                    "→ Wapas unwinding: 2*1=2 → 3*2=6 → 4*6=24!\n\n"
                    "Result = **24** ✅"
                )
            return (
                "**Step-by-Step Recursion Trace:** 🔁\n\n"
                "```python\ndef countdown(n):\n    if n == 0:        # Base case\n        print('Blast off! 🚀')\n        return\n    print(n)\n    countdown(n - 1)  # Recursive step\n\ncountdown(3) # Prints: 3, 2, 1, Blast off!\n```"
            )

        if any(w in previous_text for w in ["oop", "class", "object"]):
            if is_hinglish:
                return (
                    "**OOP (Class & Object) ka Real-Life Example:** 🏗️\n\n"
                    "• **Class = BluePrint (Naksha):** Socho 'House Blueprint'\n"
                    "• **Object = Actual Ghar:** Blueprint se bana hua actual physical ghar!\n\n"
                    "```python\nclass Student:\n    def __init__(self, name, roll_no):\n        self.name = name\n        self.roll_no = roll_no\n    \n    def study(self):\n        return f'{self.name} is studying for AI/ML!'\n\n# Objects (Instances)\nrahul = Student('Rahul', 101)\npriya = Student('Priya', 102)\n\nprint(rahul.study())\n```"
                )
            return (
                "**Class vs Object Example:** 🏗️\n\n"
                "```python\nclass BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self.balance = balance\n    def deposit(self, amount):\n        self.balance += amount\n        return f'Deposited ${amount}. Balance: ${self.balance}'\n\nacc = BankAccount('Alex', 100)\nprint(acc.deposit(50)) # Balance: $150\n```"
            )

        # Fallback to general concept explanation
        return self._concept_explanation(previous_text, context, lang=lang)

    def _concept_explanation(self, message: str, context: Dict, lang: str = "english") -> str:
        """Explain programming/ML concepts in a simple, structured way."""
        profile = context.get("profile", {})
        target_role = profile.get("target_role", "Software Engineer")
        is_hinglish = lang in ("hinglish", "hindi")

        concept_map_en = {
            "recursion": (
                "**Recursion** — A function that calls itself! 🧠\n\n"
                "**Simple idea:** Break a big problem into smaller identical subproblems until you hit the simplest base case.\n\n"
                "**Real-world analogy:** Looking up a word in a dictionary — if the definition uses another word you don't know, you recursively look that word up until you reach known words.\n\n"
                "**Code example:**\n```python\ndef factorial(n):\n    if n == 0:  # base case — STOP!\n        return 1\n    return n * factorial(n - 1)  # call itself\n\nfactorial(5)  # 5 × 4 × 3 × 2 × 1 = 120\n```\n\n"
                "**Two Golden Rules:**\n1. Always have a **base case** (prevents Stack Overflow!)\n2. Each call must move **closer to the base case**."
            ),
            "inheritance": (
                "**Inheritance in OOP** — Code reuse and hierarchy! 🧬\n\n"
                "**Simple idea:** A child class automatically inherits attributes and methods from a parent class.\n\n"
                "**Real-world analogy:** You inherit traits (like eye color) from your parents, but you also have your own unique skills.\n\n"
                "**Code example:**\n```python\nclass Animal:\n    def speak(self):\n        return 'Some sound'\n\nclass Dog(Animal):\n    def speak(self):  # Method overriding\n        return 'Woof! 🐶'\n\nd = Dog()\nprint(d.speak()) # Output: Woof!\n```\n\n"
                "**Why use it:** Eliminates boilerplate, models real-world taxonomies, and enables polymorphism."
            ),
            "oop": (
                "**Object-Oriented Programming (OOP)** — Modeling code around real-world entities! 📦\n\n"
                "**4 Core Pillars of OOP:**\n"
                "1. **Encapsulation:** Bundling data (attributes) and methods together inside a class.\n"
                "2. **Abstraction:** Hiding complex internal implementation and exposing only clean interfaces.\n"
                "3. **Inheritance:** Deriving new classes from existing ones (`ChildClass(ParentClass)`).\n"
                "4. **Polymorphism:** Same method name behaving differently across different classes.\n\n"
                "**Why it matters:** Essential for building production-grade ML pipelines and modular software."
            ),
            "polymorphism": (
                "**Polymorphism** — Many forms, one interface! 🎭\n\n"
                "**Simple idea:** The ability of different objects to respond to the same function/method call in their own specific way.\n\n"
                "**Example:** In Python, `len([1,2,3])` and `len('hello')` both work on different data structures using the same interface."
            ),
            "overfitting": (
                "**Overfitting** — When your model memorizes instead of learning! 🎯\n\n"
                "**Simple idea:** The model learns the training data and its random noise too well, failing on unseen test data.\n\n"
                "**Real-world analogy:** A student who memorizes past exam answers word-for-word, but fails when numbers are changed.\n\n"
                "**Symptoms:** Training accuracy: 99% ✅ | Test accuracy: 60% ❌\n\n"
                "**How to fix:**\n1. Regularization (L1/L2)\n2. Add more training data\n3. Dropout layers (Neural Nets)\n4. Reduce model complexity\n5. K-Fold Cross-Validation."
            ),
            "gradient": (
                "**Gradient Descent** — The engine of Machine Learning optimization! ⛰️\n\n"
                "**Simple idea:** An iterative algorithm that minimizes a loss function by taking steps in the direction of steepest downhill slope.\n\n"
                "**Formula:** `w = w - learning_rate * d(Loss)/dw`\n\n"
                "**Key types:**\n- **Batch GD:** Full dataset (slow, accurate)\n- **SGD:** 1 sample per step (fast, noisy)\n- **Mini-batch GD:** 32–256 batch size (industry standard ✅)."
            ),
            "sql": (
                "**SQL Joins** — Merging tables relational data! 🔗\n\n"
                "• **INNER JOIN:** Returns records with matching values in both tables.\n"
                "• **LEFT JOIN:** Returns all records from left table + matched records from right.\n"
                "• **RIGHT JOIN:** Returns all records from right table + matched records from left.\n"
                "• **FULL JOIN:** Returns all records when there is a match in either table.\n\n"
                "```sql\nSELECT users.name, orders.amount\nFROM users\nINNER JOIN orders ON users.id = orders.user_id;\n```"
            ),
        }

        concept_map_hinglish = {
            "recursion": (
                "**Recursion** — Ekdum simple se samjhte hain! 🧠\n\n"
                "**Concept:** Ek function jo khud ko hi call karta hai jab tak chhota case na mil jaye.\n\n"
                "**Real-life Analogy:** Socho tum line mein khade ho aur aage waale se puchte ho 'mai kitne number pe hoon?'. Wo aage waale se puchta hai, aur line ke first bande pe pahunch ke baat clear hoti hai!\n\n"
                "```python\ndef fact(n):\n    if n <= 1: return 1       # Base Case (Rukne ka rule)\n    return n * fact(n - 1)     # Recursive Step\n\nprint(fact(4)) # 4 * 3 * 2 * 1 = 24\n```\n\n"
                "💡 **Yaad rakhna:** Base case nahi diya toh `RecursionError: maximum recursion depth exceeded` (Stack overflow) ho jaayega!"
            ),
            "inheritance": (
                "**Inheritance (OOP)** — Bilkul simple hai bhai! 🧬\n\n"
                "**Concept:** Jab ek Child Class apne Parent Class ki saari properties aur methods use kar sakti hai.\n\n"
                "**Real-life Analogy:** Jaise tumhe apne parents se height ya eye color milta hai, waise hi child class ko parent class ka code milta hai bina dobara likhe!\n\n"
                "```python\nclass Vehicle:\n    def start(self):\n        return 'Engine started! 🚗'\n\nclass Bike(Vehicle):  # Bike inherits from Vehicle\n    def wheelie(self):\n        return 'Doing a wheelie! 🏍️'\n\nb = Bike()\nprint(b.start())   # Parent method automatically available!\nprint(b.wheelie()) # Child ka apna feature\n```\n\n"
                "Code reusability badhti hai aur time bachta hai!"
            ),
            "oop": (
                "**OOP (Object Oriented Programming)** — Code ko Real World jaise organize karna! 📦\n\n"
                "Dekh bhai, OOP ke 4 Main Pillars hote hain:\n\n"
                "1. **Classes & Objects:** Class = Blueprint (e.g. Car design), Object = Real Car (e.g. tumhari Swift).\n"
                "2. **Encapsulation:** Data aur functions ko ek capsule (class) ke andar band rakhna.\n"
                "3. **Inheritance:** Parent class se code reuse karna (`Child(Parent)`).\n"
                "4. **Polymorphism:** Ek hi naam ka method alag alag objects me alag behave kare.\n\n"
                "Kisi ek pillar ka deeper example chahiye toh batao!"
            ),
            "polymorphism": (
                "**Polymorphism** — 'Poly' = Many, 'Morph' = Forms! 🎭\n\n"
                "**Concept:** Ek hi method naam alag alag classes ke liye alag tareeke se kaam kare.\n\n"
                "**Example:**\n"
                "• `Dog.speak()` → 'Woof!'\n"
                "• `Cat.speak()` → 'Meow!'\n"
                "Dono ka method name `speak()` hai lekin output alag hai. Yahi polymorphism hai!"
            ),
            "overfitting": (
                "**Overfitting** — Samjho ek student ki tarah! 🎯\n\n"
                "**Problem:** Model ne training data ko patterns samajhne ki jagah 'ratta' (memorize) maar liya.\n\n"
                "**Analogy:** Ek student jo past question paper ke exact answers yaad karta hai. Exam me naya question aaya toh blank ho gaya! 😅\n\n"
                "**Symptoms:** Training Accuracy: 99% ✅, Testing Accuracy: 60% ❌\n\n"
                "**Solutions:**\n1. Regularization (L1/L2) use karo\n2. Zyada training data lao\n3. Dropout layers lagao (Neural networks me)\n4. Simple model use karo."
            ),
            "gradient": (
                "**Gradient Descent** — Samjho pahaad se neeche utarna! ⛰️\n\n"
                "**Concept:** Loss function (error) ko minimize karne ke liye weights ko step-by-step update karna.\n\n"
                "**Analogy:** Andhere mein pahaad se utarna hai. Har step pe pair se feel karo ki neeche ki dhalan kahan hai, aur us taraf chhota step lo.\n\n"
                "**Formula:** `weight = weight - (learning_rate * gradient)`\n\n"
                "Learning rate zyada bada mat rakhna warna valley paar ho jaayegi (overshoot)!"
            ),
            "sql": (
                "**SQL Joins** — Tables ko aapas mein jodne ka formula! 🔗\n\n"
                "• **INNER JOIN:** Sirf wahi rows jo dono table me common match hoti hain.\n"
                "• **LEFT JOIN:** Left table ke saare records + Right table ke matching records.\n"
                "• **RIGHT JOIN:** Right table ke saare records + Left ke matching.\n"
                "• **FULL JOIN:** Dono tables ka poora union.\n\n"
                "Venn diagram jaisa socho — INNER = Center Intersection circle! 🎯"
            ),
        }

        concept_map = concept_map_hinglish if is_hinglish else concept_map_en

        for key, explanation in concept_map.items():
            if key in message:
                return explanation

        # Fallback friendly explanation
        if is_hinglish:
            return (
                f"Bhai yeh topic **{target_role}** ke liye kaafi important hai! 🚀\n\n"
                f"Mai isko 3 simple steps me explain karta hoon:\n"
                f"1. **Core Concept:** Iska main purpose kya hai?\n"
                f"2. **Real Example:** Real life mein kaise use hota hai?\n"
                f"3. **Code Demo:** Python snippet.\n\n"
                f"Aap specific question pucho (jaise *'OOP samjhao'*, *'Inheritance ka example de'*, *'Overfitting kya hai'*), mai turant step-by-step bata dunga!"
            )

        return (
            f"Great question! Let me break this down step-by-step for your **{target_role}** roadmap. 🧠\n\n"
            f"1. **Summary:** What it is in simple terms\n"
            f"2. **Real-world analogy:** How it relates to everyday life\n"
            f"3. **Code implementation:** Practical snippet\n\n"
            f"Feel free to ask specific questions like *'Explain OOP'*, *'Give an inheritance example'*, or *'What is overfitting?'*!"
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
            f"📚 **Concept explanations** — *\"Explain recursion\"* / *\"bhai inheritance samjhao\"*\n"
            f"💡 **Code & Examples** — *\"ek example de\"* / *\"show me a code snippet\"*\n"
            f"🎯 **Daily & Exam plans** — *\"What should I study today?\"* / *\"kal exam hai kya padhu\"*\n"
            f"🗺️ **Roadmap help** — *\"What's my next step?\"* / *\"Aage kya karun?\"*\n"
            f"🔨 **Projects & Prep** — *\"What project should I build for my resume?\"*\n\n"
            f"Ask me anything — in English, Hindi, or Hinglish! 😊"
        )

