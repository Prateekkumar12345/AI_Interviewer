import streamlit as st
from openai import OpenAI
import json
from datetime import datetime
from typing import List, Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is available
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OPENAI_API_KEY not found in .env file. Please create a .env file with your API key.")
    st.stop()

# ============================
#  RAG Document Store
# ============================

class CompanyKnowledgeBase:
    """Store company-specific interview information"""
    
    def __init__(self):
        self.company_data = {
            "Google": {
                "description": "Google is a technology company focusing on search, cloud computing, and AI.",
                "interview_focus": [
                    "Data structures and algorithms",
                    "System design",
                    "Behavioral questions (Googleyness)",
                    "Coding proficiency in any language",
                    "Problem-solving approach"
                ],
                "common_questions": [
                    "Design a URL shortener",
                    "Implement LRU Cache",
                    "Tell me about a time you disagreed with your manager",
                    "How would you improve Google Maps?",
                    "Explain a complex technical concept to a non-technical person"
                ],
                "culture": "Innovation-driven, data-focused, collaborative environment",
                "tips": "Focus on demonstrating problem-solving process, not just the solution. Google values communication and thought process."
            },
            "Amazon": {
                "description": "Amazon is an e-commerce and cloud computing giant known for AWS and retail operations.",
                "interview_focus": [
                    "Leadership principles (14 principles)",
                    "System design and scalability",
                    "Data structures and algorithms",
                    "Behavioral interviews (STAR method)",
                    "Customer obsession mindset"
                ],
                "common_questions": [
                    "Tell me about a time you failed",
                    "Design Amazon's recommendation system",
                    "Implement a binary search tree",
                    "Describe a time you had to make a difficult decision with limited data",
                    "How would you improve the Amazon checkout process?"
                ],
                "culture": "Customer-obsessed, ownership mentality, high performance standards",
                "tips": "Use STAR method for behavioral questions. Demonstrate ownership and customer-first thinking."
            },
            "Microsoft": {
                "description": "Microsoft is a technology corporation developing software, hardware, and cloud services.",
                "interview_focus": [
                    "Technical depth in your domain",
                    "Collaboration and teamwork",
                    "System design",
                    "Problem-solving skills",
                    "Growth mindset"
                ],
                "common_questions": [
                    "Design a parking lot system",
                    "Implement string manipulation algorithms",
                    "How do you handle conflicting priorities?",
                    "Explain your most challenging project",
                    "How would you test Microsoft Teams?"
                ],
                "culture": "Growth mindset, inclusive, collaborative, innovation-focused",
                "tips": "Emphasize learning, collaboration, and continuous improvement. Show technical depth."
            },
            "Meta": {
                "description": "Meta (formerly Facebook) builds social technology and metaverse platforms.",
                "interview_focus": [
                    "Coding and algorithms",
                    "System design at scale",
                    "Product sense",
                    "Behavioral (impact and collaboration)",
                    "Mobile/web development"
                ],
                "common_questions": [
                    "Design Facebook's newsfeed",
                    "Implement a graph algorithm",
                    "Tell me about a time you influenced without authority",
                    "How would you improve Instagram Stories?",
                    "Design a rate limiter"
                ],
                "culture": "Move fast, be bold, focus on impact, build social value",
                "tips": "Demonstrate impact-driven thinking. Show you can work at scale and move quickly."
            },
            "Apple": {
                "description": "Apple designs consumer electronics, software, and services with a focus on user experience.",
                "interview_focus": [
                    "Technical excellence",
                    "Attention to detail",
                    "Product design thinking",
                    "Innovation and creativity",
                    "Collaboration across teams"
                ],
                "common_questions": [
                    "Design an elevator system",
                    "How would you test AirPods?",
                    "Tell me about a time you improved a product",
                    "Implement a memory-efficient data structure",
                    "How do you ensure code quality?"
                ],
                "culture": "Excellence-driven, detail-oriented, innovation-focused, secretive",
                "tips": "Show attention to detail and user-centric thinking. Demonstrate technical excellence."
            }
        }
    
    def get_company_context(self, company: str) -> str:
        """Get company-specific context for RAG"""
        if company not in self.company_data:
            return ""
        
        data = self.company_data[company]
        context = f"""
Company: {company}
Description: {data['description']}

Interview Focus Areas:
{chr(10).join(f"- {area}" for area in data['interview_focus'])}

Company Culture: {data['culture']}

Interview Tips: {data['tips']}

Common Question Types:
{chr(10).join(f"- {q}" for q in data['common_questions'][:3])}
"""
        return context
    
    def get_available_companies(self) -> List[str]:
        """Get list of available companies"""
        return list(self.company_data.keys())


# ============================
#  AI Interviewer with RAG
# ============================

class RAGInterviewer:
    def __init__(self):
        # Get API key from environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
        self.knowledge_base = CompanyKnowledgeBase()
        
    def initialize_interview(self, job_role: str, difficulty: str, company: str = None) -> str:
        """Initialize interview with RAG context"""
        
        # Build context from knowledge base
        company_context = ""
        if company and company != "General Interview":
            company_context = self.knowledge_base.get_company_context(company)
        
        system_prompt = f"""
You are a professional AI interviewer conducting a {difficulty.lower()} level interview for a {job_role} position.
{f'This interview is specifically for {company}.' if company and company != "General Interview" else 'This is a general technical interview.'}

{company_context}

INTERVIEW GUIDELINES:
1. Start with a warm, professional welcome
2. Ask the candidate to introduce themselves and discuss their background
3. After introduction, ask relevant questions based on:
   - The job role ({job_role})
   - The difficulty level ({difficulty})
   {f'- {company} specific focus areas and culture' if company and company != "General Interview" else '- General industry best practices'}
4. Mix technical questions with behavioral questions
5. Ask follow-up questions based on candidate responses
6. Keep questions clear and focused
7. After 8-12 quality questions, wrap up professionally
8. Maintain a conversational, professional tone

Remember: You're assessing both technical skills and cultural fit{f' for {company}' if company and company != "General Interview" else ''}.
"""

        return self._generate_response(
            system_prompt,
            "Start the interview with a professional welcome and ask the candidate to introduce themselves."
        )
    
    def generate_next_question(self, conversation_history: List[Dict], job_role: str, 
                              difficulty: str, company: str = None) -> str:
        """Generate next question using conversation context"""
        
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" 
                                 for msg in conversation_history[-10:]])
        questions_asked = len([msg for msg in conversation_history 
                              if msg["role"] == "interviewer"])
        
        company_context = ""
        if company and company != "General Interview":
            company_context = self.knowledge_base.get_company_context(company)
        
        system_prompt = f"""
You are conducting an interview for {job_role} ({difficulty} level){f' at {company}' if company and company != "General Interview" else ''}.

{company_context}

Conversation so far:
{history_text}

Questions asked: {questions_asked}

Your task:
- Continue the conversation naturally based on the candidate's last response
- Ask thoughtful follow-up questions or move to new relevant topics
- Balance technical and behavioral questions
{f'- Align questions with {company} culture and values' if company and company != "General Interview" else '- Focus on industry-standard competencies'}
- After 8-12 substantial questions, wrap up the interview
- Keep the conversation flowing like a real human interviewer
"""

        return self._generate_response(
            system_prompt,
            "Provide the next natural interview question or closing remarks."
        )
    
    def generate_feedback(self, conversation_history: List[Dict], job_role: str, 
                         company: str = None) -> str:
        """Generate comprehensive feedback"""
        
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" 
                                 for msg in conversation_history])
        
        company_context = ""
        if company and company != "General Interview":
            company_context = f"\nThis was an interview for {company}. Evaluate cultural fit based on {company}'s values and culture."
        
        system_prompt = f"""
You are an experienced hiring manager reviewing an interview for a {job_role} position.
{company_context}

Provide detailed, constructive feedback covering:

1. **Overall Assessment** - Summary of performance
2. **Key Strengths** - What the candidate did well
3. **Technical Skills** - Evaluation of technical knowledge
4. **Communication Skills** - How well they articulated responses
5. **Areas for Improvement** - Specific growth areas
6. **Recommendations** - Actionable next steps
{f'7. **Cultural Fit for {company}** - Alignment with company values' if company and company != "General Interview" else ''}

Be specific, professional, and actionable.

Interview Conversation:
{history_text}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Provide comprehensive feedback."}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating feedback: {str(e)}"
    
    def _generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate AI response using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"


# ============================
#  Streamlit UI
# ============================

def main():
    st.set_page_config(
        page_title="AI Interview Prep",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 AI-Powered Interview Preparation System")
    st.markdown("---")
    
    # Initialize session state
    if "interviewer" not in st.session_state:
        try:
            st.session_state.interviewer = RAGInterviewer()
        except ValueError as e:
            st.error(f"❌ Configuration Error: {e}")
            st.info("Please create a `.env` file in the project root with your OpenAI API key:")
            st.code("OPENAI_API_KEY=your_api_key_here")
            st.stop()
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "interview_active" not in st.session_state:
        st.session_state.interview_active = False
    if "feedback" not in st.session_state:
        st.session_state.feedback = None
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Display API status
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            # Show masked API key for verification
            masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
            st.success(f"✅ API Key Loaded: `{masked_key}`")
        else:
            st.error("❌ API Key Not Found")
        
        st.markdown("---")
        
        # Interview type selection
        interview_type = st.radio(
            "Interview Type",
            ["Company-Specific Interview", "General Interview"]
        )
        
        # Company selection
        company = None
        if interview_type == "Company-Specific Interview":
            kb = CompanyKnowledgeBase()
            company = st.selectbox(
                "Select Company",
                kb.get_available_companies()
            )
            
            # Show company info
            if company:
                with st.expander(f"ℹ️ About {company}"):
                    context = kb.get_company_context(company)
                    st.markdown(context)
        else:
            company = "General Interview"
        
        st.markdown("---")
        
        job_role = st.text_input("Job Role", value="Software Engineer")
        
        difficulty = st.selectbox(
            "Difficulty Level",
            ["Beginner", "Intermediate", "Advanced"]
        )
        
        st.markdown("---")
        
        # Control buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Start Interview", use_container_width=True, 
                        disabled=st.session_state.interview_active):
                st.session_state.interview_active = True
                st.session_state.conversation_history = []
                st.session_state.feedback = None
                
                # Get initial question
                intro = st.session_state.interviewer.initialize_interview(
                    job_role, difficulty, company
                )
                st.session_state.conversation_history.append({
                    "role": "interviewer",
                    "content": intro
                })
                st.rerun()
        
        with col2:
            if st.button("⏹️ End Interview", use_container_width=True,
                        disabled=not st.session_state.interview_active):
                st.session_state.interview_active = False
                
                # Generate feedback if conversation exists
                if len(st.session_state.conversation_history) > 2:
                    with st.spinner("Generating feedback..."):
                        feedback = st.session_state.interviewer.generate_feedback(
                            st.session_state.conversation_history,
                            job_role,
                            company
                        )
                        st.session_state.feedback = feedback
                st.rerun()
        
        # Reset button
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.conversation_history = []
            st.session_state.interview_active = False
            st.session_state.feedback = None
            st.rerun()
    
    # Main content area
    if not st.session_state.interview_active and not st.session_state.conversation_history:
        # Welcome screen
        st.info("👈 Configure your interview settings in the sidebar and click **Start Interview** to begin!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏢 Company-Specific Interviews")
            st.write("""
            Prepare for interviews at top tech companies:
            - Google, Amazon, Microsoft, Meta, Apple
            - Company-specific questions and culture
            - Tailored feedback based on company values
            """)
        
        with col2:
            st.subheader("📝 General Interviews")
            st.write("""
            General technical interview practice:
            - Industry-standard questions
            - Comprehensive skill assessment
            - Applicable to any company
            """)
        
        # Quick start tips
        with st.expander("💡 Quick Start Tips"):
            st.write("""
            1. Select your target company or choose "General Interview"
            2. Enter your desired job role (e.g., "Software Engineer", "Data Scientist")
            3. Choose difficulty level based on your experience
            4. Click "Start Interview" to begin
            5. Respond naturally to the AI interviewer's questions
            6. Click "End Interview" when done to receive feedback
            """)
    
    else:
        # Interview interface
        st.subheader("💬 Interview Conversation")
        
        # Display conversation
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.conversation_history:
                if msg["role"] == "interviewer":
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(msg["content"])
                else:
                    with st.chat_message("user", avatar="👤"):
                        st.write(msg["content"])
        
        # Input area
        if st.session_state.interview_active:
            user_input = st.chat_input("Type your response here...")
            
            if user_input:
                # Add user response
                st.session_state.conversation_history.append({
                    "role": "candidate",
                    "content": user_input
                })
                
                # Generate next question
                with st.spinner("Thinking..."):
                    next_question = st.session_state.interviewer.generate_next_question(
                        st.session_state.conversation_history,
                        job_role,
                        difficulty,
                        company
                    )
                    
                    st.session_state.conversation_history.append({
                        "role": "interviewer",
                        "content": next_question
                    })
                
                st.rerun()
        
        # Display feedback if available
        if st.session_state.feedback:
            st.markdown("---")
            st.subheader("📊 Interview Feedback")
            st.markdown(st.session_state.feedback)
            
            # Download option
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.download_button(
                    label="📥 Download Feedback",
                    data=st.session_state.feedback,
                    file_name=f"interview_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                ):
                    st.success("Feedback downloaded!")
            
            # Tips for improvement
            with st.expander("🔍 Tips for Improvement"):
                st.write("""
                - **Review your answers**: Identify areas where you could have been more specific
                - **Practice STAR method**: For behavioral questions, use Situation, Task, Action, Result
                - **Technical depth**: Make sure to explain your thinking process for technical questions
                - **Ask questions**: Remember that interviews are a two-way conversation
                - **Record yourself**: Consider recording practice sessions to improve communication skills
                """)


if __name__ == "__main__":
    main()