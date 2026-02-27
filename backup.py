# import streamlit as st
# from openai import OpenAI
# import json
# from datetime import datetime
# from typing import List, Dict, Optional
# import os
# from dotenv import load_dotenv
# import plotly.graph_objects as go

# # Load environment variables
# load_dotenv()

# # Check if API key is available
# if not os.getenv("OPENAI_API_KEY"):
#     st.error("⚠️ OPENAI_API_KEY not found in .env file. Please create a .env file with your API key.")
#     st.stop()

# # ============================
# #  RAG Document Store
# # ============================

# class CompanyKnowledgeBase:
#     """Store company-specific interview information"""
    
#     def __init__(self):
#         self.company_data = {
#             "Google": {
#                 "description": "Google is a technology company focusing on search, cloud computing, and AI.",
#                 "interview_focus": [
#                     "Data structures and algorithms",
#                     "System design",
#                     "Behavioral questions (Googleyness)",
#                     "Coding proficiency in any language",
#                     "Problem-solving approach"
#                 ],
#                 "common_questions": [
#                     "Design a URL shortener",
#                     "Implement LRU Cache",
#                     "Tell me about a time you disagreed with your manager",
#                     "How would you improve Google Maps?",
#                     "Explain a complex technical concept to a non-technical person"
#                 ],
#                 "culture": "Innovation-driven, data-focused, collaborative environment",
#                 "tips": "Focus on demonstrating problem-solving process, not just the solution. Google values communication and thought process."
#             },
#             "Amazon": {
#                 "description": "Amazon is an e-commerce and cloud computing giant known for AWS and retail operations.",
#                 "interview_focus": [
#                     "Leadership principles (14 principles)",
#                     "System design and scalability",
#                     "Data structures and algorithms",
#                     "Behavioral interviews (STAR method)",
#                     "Customer obsession mindset"
#                 ],
#                 "common_questions": [
#                     "Tell me about a time you failed",
#                     "Design Amazon's recommendation system",
#                     "Implement a binary search tree",
#                     "Describe a time you had to make a difficult decision with limited data",
#                     "How would you improve the Amazon checkout process?"
#                 ],
#                 "culture": "Customer-obsessed, ownership mentality, high performance standards",
#                 "tips": "Use STAR method for behavioral questions. Demonstrate ownership and customer-first thinking."
#             },
#             "Microsoft": {
#                 "description": "Microsoft is a technology corporation developing software, hardware, and cloud services.",
#                 "interview_focus": [
#                     "Technical depth in your domain",
#                     "Collaboration and teamwork",
#                     "System design",
#                     "Problem-solving skills",
#                     "Growth mindset"
#                 ],
#                 "common_questions": [
#                     "Design a parking lot system",
#                     "Implement string manipulation algorithms",
#                     "How do you handle conflicting priorities?",
#                     "Explain your most challenging project",
#                     "How would you test Microsoft Teams?"
#                 ],
#                 "culture": "Growth mindset, inclusive, collaborative, innovation-focused",
#                 "tips": "Emphasize learning, collaboration, and continuous improvement. Show technical depth."
#             },
#             "Meta": {
#                 "description": "Meta (formerly Facebook) builds social technology and metaverse platforms.",
#                 "interview_focus": [
#                     "Coding and algorithms",
#                     "System design at scale",
#                     "Product sense",
#                     "Behavioral (impact and collaboration)",
#                     "Mobile/web development"
#                 ],
#                 "common_questions": [
#                     "Design Facebook's newsfeed",
#                     "Implement a graph algorithm",
#                     "Tell me about a time you influenced without authority",
#                     "How would you improve Instagram Stories?",
#                     "Design a rate limiter"
#                 ],
#                 "culture": "Move fast, be bold, focus on impact, build social value",
#                 "tips": "Demonstrate impact-driven thinking. Show you can work at scale and move quickly."
#             },
#             "Apple": {
#                 "description": "Apple designs consumer electronics, software, and services with a focus on user experience.",
#                 "interview_focus": [
#                     "Technical excellence",
#                     "Attention to detail",
#                     "Product design thinking",
#                     "Innovation and creativity",
#                     "Collaboration across teams"
#                 ],
#                 "common_questions": [
#                     "Design an elevator system",
#                     "How would you test AirPods?",
#                     "Tell me about a time you improved a product",
#                     "Implement a memory-efficient data structure",
#                     "How do you ensure code quality?"
#                 ],
#                 "culture": "Excellence-driven, detail-oriented, innovation-focused, secretive",
#                 "tips": "Show attention to detail and user-centric thinking. Demonstrate technical excellence."
#             }
#         }
    
#     def get_company_context(self, company: str) -> str:
#         """Get company-specific context for RAG"""
#         if company not in self.company_data:
#             return ""
        
#         data = self.company_data[company]
#         context = f"""
# Company: {company}
# Description: {data['description']}

# Interview Focus Areas:
# {chr(10).join(f"- {area}" for area in data['interview_focus'])}

# Company Culture: {data['culture']}

# Interview Tips: {data['tips']}

# Common Question Types:
# {chr(10).join(f"- {q}" for q in data['common_questions'][:3])}
# """
#         return context
    
#     def get_available_companies(self) -> List[str]:
#         """Get list of available companies"""
#         return list(self.company_data.keys())


# # ============================
# #  Interview History Manager
# # ============================

# class InterviewHistoryManager:
#     """Manage interview history and scoring"""
    
#     def __init__(self, storage_file="interview_history.json"):
#         self.storage_file = storage_file
#         self.history = self._load_history()
    
#     def _load_history(self) -> Dict:
#         """Load interview history from file"""
#         try:
#             if os.path.exists(self.storage_file):
#                 with open(self.storage_file, 'r') as f:
#                     return json.load(f)
#         except Exception as e:
#             print(f"Error loading history: {e}")
#         return {}
    
#     def _save_history(self):
#         """Save interview history to file"""
#         try:
#             with open(self.storage_file, 'w') as f:
#                 json.dump(self.history, f, indent=2)
#         except Exception as e:
#             print(f"Error saving history: {e}")
    
#     def save_interview(self, candidate_id: str, interview_data: Dict):
#         """Save interview data for a candidate"""
#         if candidate_id not in self.history:
#             self.history[candidate_id] = []
        
#         self.history[candidate_id].append(interview_data)
#         self._save_history()
    
#     def get_candidate_history(self, candidate_id: str) -> List[Dict]:
#         """Get all interviews for a candidate"""
#         return self.history.get(candidate_id, [])
    
#     def get_latest_interview(self, candidate_id: str) -> Optional[Dict]:
#         """Get the most recent interview for a candidate"""
#         interviews = self.get_candidate_history(candidate_id)
#         return interviews[-1] if interviews else None
    
#     def compare_interviews(self, candidate_id: str) -> Optional[Dict]:
#         """Compare latest interview with previous one"""
#         interviews = self.get_candidate_history(candidate_id)
#         if len(interviews) < 2:
#             return None
        
#         current = interviews[-1]
#         previous = interviews[-2]
        
#         comparison = {
#             "current_date": current["date"],
#             "previous_date": previous["date"],
#             "improvements": {},
#             "declines": {}
#         }
        
#         for category in current["scores"]:
#             current_score = current["scores"][category]["score"]
#             previous_score = previous["scores"][category]["score"]
#             diff = current_score - previous_score
            
#             if diff > 0:
#                 comparison["improvements"][category] = {
#                     "current": current_score,
#                     "previous": previous_score,
#                     "change": diff
#                 }
#             elif diff < 0:
#                 comparison["declines"][category] = {
#                     "current": current_score,
#                     "previous": previous_score,
#                     "change": diff
#                 }
        
#         return comparison


# # ============================
# #  AI Interviewer with RAG
# # ============================

# class RAGInterviewer:
#     def __init__(self):
#         # Get API key from environment variable
#         api_key = os.getenv("OPENAI_API_KEY")
#         if not api_key:
#             raise ValueError("OPENAI_API_KEY not found in environment variables")
#         self.client = OpenAI(api_key=api_key)
#         self.knowledge_base = CompanyKnowledgeBase()
#         self.history_manager = InterviewHistoryManager()
        
#     def initialize_interview(self, job_role: str, difficulty: str, company: str = None) -> str:
#         """Initialize interview with RAG context"""
        
#         # Build context from knowledge base
#         company_context = ""
#         if company and company != "General Interview":
#             company_context = self.knowledge_base.get_company_context(company)
        
#         system_prompt = f"""You are a professional AI interviewer conducting a {difficulty.lower()} level interview for a {job_role} position.
# {f'This interview is specifically for {company}.' if company and company != "General Interview" else 'This is a general technical interview.'}

# {company_context}

# INTERVIEW GUIDELINES:
# 1. Start with a warm, professional welcome
# 2. Ask the candidate to introduce themselves and discuss their background
# 3. After introduction, ask relevant questions based on:
#    - The job role ({job_role})
#    - The difficulty level ({difficulty})
#    {f'- {company} specific focus areas and culture' if company and company != "General Interview" else '- General industry best practices'}
# 4. Mix technical questions with behavioral questions
# 5. Ask follow-up questions based on candidate responses
# 6. Keep questions clear and focused
# 7. After 8-12 quality questions, wrap up professionally
# 8. Maintain a conversational, professional tone

# CRITICAL RULES:
# - You must ONLY generate the interviewer's questions/statements
# - NEVER generate, predict, or include the candidate's responses
# - NEVER write "candidate:" or include what the candidate might say
# - Stop immediately after your question or statement
# - Wait for the actual candidate to respond

# Remember: You're assessing both technical skills and cultural fit{f' for {company}' if company and company != "General Interview" else ''}.
# """

#         return self._generate_response(
#             system_prompt,
#             "Start the interview with a professional welcome and ask the candidate to introduce themselves. ONLY provide YOUR welcome and question, nothing else."
#         )
    
#     def generate_next_question(self, conversation_history: List[Dict], job_role: str, 
#                               difficulty: str, company: str = None) -> str:
#         """Generate next question using conversation context"""
        
#         # Extract only the last few exchanges to prevent context overflow
#         history_text = "\n".join([f"{msg['role']}: {msg['content']}" 
#                                  for msg in conversation_history[-6:]])
#         questions_asked = len([msg for msg in conversation_history 
#                               if msg["role"] == "interviewer"])
        
#         company_context = ""
#         if company and company != "General Interview":
#             company_context = self.knowledge_base.get_company_context(company)
        
#         system_prompt = f"""You are conducting an interview for {job_role} ({difficulty} level){f' at {company}' if company and company != "General Interview" else ''}.

# {company_context}

# Recent conversation:
# {history_text}

# Questions asked so far: {questions_asked}

# Your task:
# - Based on the candidate's LAST response, generate your NEXT question or comment
# - Ask thoughtful follow-up questions or move to new relevant topics
# - Balance technical and behavioral questions
# {f'- Align questions with {company} culture and values' if company and company != "General Interview" else '- Focus on industry-standard competencies'}
# - After 8-12 substantial questions, wrap up the interview professionally
# - Keep the conversation flowing naturally

# CRITICAL RULES:
# - ONLY generate the interviewer's response (your response)
# - NEVER include "candidate:" or predict what the candidate will say
# - NEVER generate the candidate's answer
# - Stop immediately after your question/statement
# - Your response should be a single question or brief comment followed by a question
# """

#         user_prompt = "Generate ONLY the interviewer's next question or statement. Do not include any candidate responses."
        
#         return self._generate_response(system_prompt, user_prompt)
    
#     def generate_detailed_feedback(self, conversation_history: List[Dict], job_role: str, 
#                                    company: str = None, candidate_id: str = None) -> Dict:
#         """Generate comprehensive feedback with detailed scoring"""
        
#         history_text = "\n".join([f"{msg['role']}: {msg['content']}" 
#                                  for msg in conversation_history])
        
#         company_context = ""
#         if company and company != "General Interview":
#             company_context = f"\nThis was an interview for {company}. Evaluate cultural fit based on {company}'s values and culture."
        
#         system_prompt = f"""You are an experienced hiring manager reviewing an interview for a {job_role} position.
# {company_context}

# Interview Conversation:
# {history_text}

# Provide a detailed evaluation in the following JSON format:

# {{
#   "overall_summary": "Brief 2-3 sentence overview of the candidate's performance",
#   "scores": {{
#     "technical_skills": {{
#       "score": 0-10,
#       "strengths": ["strength1", "strength2"],
#       "weaknesses": ["weakness1", "weakness2"],
#       "details": "Detailed explanation"
#     }},
#     "communication": {{
#       "score": 0-10,
#       "strengths": ["strength1", "strength2"],
#       "weaknesses": ["weakness1", "weakness2"],
#       "details": "Detailed explanation"
#     }},
#     "problem_solving": {{
#       "score": 0-10,
#       "strengths": ["strength1", "strength2"],
#       "weaknesses": ["weakness1", "weakness2"],
#       "details": "Detailed explanation"
#     }},
#     "cultural_fit": {{
#       "score": 0-10,
#       "strengths": ["strength1", "strength2"],
#       "weaknesses": ["weakness1", "weakness2"],
#       "details": "Detailed explanation"
#     }},
#     "experience_depth": {{
#       "score": 0-10,
#       "strengths": ["strength1", "strength2"],
#       "weaknesses": ["weakness1", "weakness2"],
#       "details": "Detailed explanation"
#     }},
#     "behavioral_responses": {{
#       "score": 0-10,
#       "strengths": ["strength1", "strength2"],
#       "weaknesses": ["weakness1", "weakness2"],
#       "details": "Detailed explanation"
#     }}
#   }},
#   "overall_score": 0-10,
#   "recommendation": "hire/maybe/no_hire",
#   "key_highlights": ["highlight1", "highlight2", "highlight3"],
#   "improvement_areas": ["area1", "area2", "area3"],
#   "actionable_recommendations": ["recommendation1", "recommendation2", "recommendation3"]
# }}

# Rate each category from 0-10:
# - 0-3: Poor (needs significant improvement)
# - 4-5: Below average (needs improvement)
# - 6-7: Average (meets basic expectations)
# - 8-9: Good (exceeds expectations)
# - 10: Excellent (exceptional performance)

# Be specific, objective, and constructive in your evaluation."""

#         try:
#             response = self.client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": "Provide the detailed evaluation in valid JSON format."}
#                 ],
#                 temperature=0.5,
#                 max_tokens=1500
#             )
            
#             # Parse the JSON response
#             feedback_text = response.choices[0].message.content.strip()
            
#             # Remove markdown code blocks if present
#             if feedback_text.startswith("```json"):
#                 feedback_text = feedback_text[7:]
#             if feedback_text.startswith("```"):
#                 feedback_text = feedback_text[3:]
#             if feedback_text.endswith("```"):
#                 feedback_text = feedback_text[:-3]
            
#             feedback_data = json.loads(feedback_text.strip())
            
#             # Add metadata
#             feedback_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             feedback_data["job_role"] = job_role
#             feedback_data["company"] = company if company else "General"
            
#             # Save to history if candidate_id provided
#             if candidate_id:
#                 self.history_manager.save_interview(candidate_id, feedback_data)
            
#             return feedback_data
            
#         except json.JSONDecodeError as e:
#             return {
#                 "error": "Failed to parse feedback",
#                 "details": str(e),
#                 "raw_response": feedback_text if 'feedback_text' in locals() else "No response"
#             }
#         except Exception as e:
#             return {
#                 "error": "Failed to generate feedback",
#                 "details": str(e)
#             }
    
#     def _generate_response(self, system_prompt: str, user_prompt: str) -> str:
#         """Generate AI response using OpenAI"""
#         try:
#             response = self.client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 temperature=0.7,
#                 max_tokens=250,
#                 stop=["candidate:", "Candidate:", "CANDIDATE:"]  # Stop generation if it tries to include candidate response
#             )
            
#             generated_text = response.choices[0].message.content.strip()
            
#             # Additional safety check: remove any candidate responses that slipped through
#             if "candidate:" in generated_text.lower():
#                 generated_text = generated_text.split("candidate:")[0].strip()
#                 generated_text = generated_text.split("Candidate:")[0].strip()
            
#             return generated_text
            
#         except Exception as e:
#             return f"Error: {str(e)}"


# # ============================
# #  Visualization Functions
# # ============================

# def create_score_radar_chart(scores: Dict) -> go.Figure:
#     """Create a radar chart for scores"""
#     categories = []
#     values = []
    
#     for category, data in scores.items():
#         categories.append(category.replace('_', ' ').title())
#         values.append(data['score'])
    
#     fig = go.Figure(data=go.Scatterpolar(
#         r=values,
#         theta=categories,
#         fill='toself',
#         line=dict(color='rgb(67, 147, 195)'),
#         fillcolor='rgba(67, 147, 195, 0.5)'
#     ))
    
#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(
#                 visible=True,
#                 range=[0, 10]
#             )
#         ),
#         showlegend=False,
#         title="Performance Radar Chart",
#         height=400
#     )
    
#     return fig


# def create_comparison_chart(comparison: Dict) -> go.Figure:
#     """Create a comparison chart between interviews"""
#     categories = []
#     current_scores = []
#     previous_scores = []
    
#     for category in comparison.get("improvements", {}).keys():
#         data = comparison["improvements"][category]
#         categories.append(category.replace('_', ' ').title())
#         current_scores.append(data["current"])
#         previous_scores.append(data["previous"])
    
#     for category in comparison.get("declines", {}).keys():
#         data = comparison["declines"][category]
#         if category.replace('_', ' ').title() not in categories:
#             categories.append(category.replace('_', ' ').title())
#             current_scores.append(data["current"])
#             previous_scores.append(data["previous"])
    
#     fig = go.Figure(data=[
#         go.Bar(name='Previous', x=categories, y=previous_scores, marker_color='lightblue'),
#         go.Bar(name='Current', x=categories, y=current_scores, marker_color='darkblue')
#     ])
    
#     fig.update_layout(
#         title="Score Comparison with Previous Interview",
#         barmode='group',
#         yaxis=dict(range=[0, 10], title="Score"),
#         xaxis_title="Categories",
#         height=400
#     )
    
#     return fig


# # ============================
# #  Streamlit UI
# # ============================

# def main():
#     st.set_page_config(
#         page_title="AI Interview Prep Pro",
#         page_icon="🎯",
#         layout="wide"
#     )
    
#     st.title("🎯 AI-Powered Interview Preparation System")
#     st.markdown("### With Detailed Scoring & Progress Tracking")
#     st.markdown("---")
    
#     # Initialize session state
#     if "interviewer" not in st.session_state:
#         try:
#             st.session_state.interviewer = RAGInterviewer()
#         except ValueError as e:
#             st.error(f"❌ Configuration Error: {e}")
#             st.info("Please create a `.env` file in the project root with your OpenAI API key:")
#             st.code("OPENAI_API_KEY=your_api_key_here")
#             st.stop()
#     if "conversation_history" not in st.session_state:
#         st.session_state.conversation_history = []
#     if "interview_active" not in st.session_state:
#         st.session_state.interview_active = False
#     if "feedback_data" not in st.session_state:
#         st.session_state.feedback_data = None
#     if "candidate_id" not in st.session_state:
#         st.session_state.candidate_id = ""
    
#     # Sidebar configuration
#     with st.sidebar:
#         st.header("⚙️ Configuration")
        
#         # Display API status
#         api_key = os.getenv("OPENAI_API_KEY")
#         if api_key:
#             masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
#             st.success(f"✅ API Key: `{masked_key}`")
#         else:
#             st.error("❌ API Key Not Found")
        
#         st.markdown("---")
        
#         # Candidate ID for tracking
#         st.session_state.candidate_id = st.text_input(
#             "Candidate ID (for tracking progress)",
#             value=st.session_state.candidate_id,
#             help="Use same ID to track your improvement over multiple interviews"
#         )
        
#         st.markdown("---")
        
#         # Interview type selection
#         interview_type = st.radio(
#             "Interview Type",
#             ["Company-Specific Interview", "General Interview"]
#         )
        
#         # Company selection
#         company = None
#         if interview_type == "Company-Specific Interview":
#             kb = CompanyKnowledgeBase()
#             company = st.selectbox(
#                 "Select Company",
#                 kb.get_available_companies()
#             )
            
#             if company:
#                 with st.expander(f"ℹ️ About {company}"):
#                     context = kb.get_company_context(company)
#                     st.markdown(context)
#         else:
#             company = "General Interview"
        
#         st.markdown("---")
        
#         job_role = st.text_input("Job Role", value="Software Engineer")
        
#         difficulty = st.selectbox(
#             "Difficulty Level",
#             ["Beginner", "Intermediate", "Advanced"]
#         )
        
#         st.markdown("---")
        
#         # Control buttons
#         col1, col2 = st.columns(2)
        
#         with col1:
#             if st.button("▶️ Start", use_container_width=True, 
#                         disabled=st.session_state.interview_active):
#                 st.session_state.interview_active = True
#                 st.session_state.conversation_history = []
#                 st.session_state.feedback_data = None
                
#                 intro = st.session_state.interviewer.initialize_interview(
#                     job_role, difficulty, company
#                 )
#                 st.session_state.conversation_history.append({
#                     "role": "interviewer",
#                     "content": intro
#                 })
#                 st.rerun()
        
#         with col2:
#             if st.button("⏹️ End", use_container_width=True,
#                         disabled=not st.session_state.interview_active):
#                 st.session_state.interview_active = False
                
#                 if len(st.session_state.conversation_history) > 2:
#                     with st.spinner("Generating detailed feedback..."):
#                         feedback = st.session_state.interviewer.generate_detailed_feedback(
#                             st.session_state.conversation_history,
#                             job_role,
#                             company,
#                             st.session_state.candidate_id if st.session_state.candidate_id else None
#                         )
#                         st.session_state.feedback_data = feedback
#                 st.rerun()
        
#         if st.button("🔄 Reset", use_container_width=True):
#             st.session_state.conversation_history = []
#             st.session_state.interview_active = False
#             st.session_state.feedback_data = None
#             st.rerun()
        
#         # Show previous interview stats
#         if st.session_state.candidate_id:
#             st.markdown("---")
#             st.subheader("📊 Your History")
#             history = st.session_state.interviewer.history_manager.get_candidate_history(
#                 st.session_state.candidate_id
#             )
#             if history:
#                 st.metric("Total Interviews", len(history))
#                 latest = history[-1]
#                 st.metric("Last Score", f"{latest.get('overall_score', 'N/A')}/10")
#             else:
#                 st.info("No previous interviews found")
    
#     # Main content area
#     if not st.session_state.interview_active and not st.session_state.conversation_history:
#         # Welcome screen
#         st.info("👈 Configure your interview settings and click **Start** to begin!")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("🏢 Company-Specific Interviews")
#             st.write("""
#             - Google, Amazon, Microsoft, Meta, Apple
#             - Company-specific questions
#             - Tailored cultural fit assessment
#             """)
        
#         with col2:
#             st.subheader("📝 General Interviews")
#             st.write("""
#             - Industry-standard questions
#             - Comprehensive skill assessment
#             - Universal best practices
#             """)
        
#         with st.expander("💡 Features"):
#             st.write("""
#             ✅ **Detailed Scoring**: Get scored on 6 different categories
#             ✅ **Progress Tracking**: Compare your improvement over time
#             ✅ **Actionable Feedback**: Specific recommendations for improvement
#             ✅ **Company-Specific**: Tailored questions for top tech companies
#             ✅ **History Tracking**: Track all your interview attempts
#             """)
    
#     else:
#         # Interview interface
#         st.subheader("💬 Interview Conversation")
        
#         # Display conversation
#         chat_container = st.container()
#         with chat_container:
#             for msg in st.session_state.conversation_history:
#                 if msg["role"] == "interviewer":
#                     with st.chat_message("assistant", avatar="🤖"):
#                         st.write(msg["content"])
#                 else:
#                     with st.chat_message("user", avatar="👤"):
#                         st.write(msg["content"])
        
#         # Input area
#         if st.session_state.interview_active:
#             user_input = st.chat_input("Type your response here...")
            
#             if user_input:
#                 st.session_state.conversation_history.append({
#                     "role": "candidate",
#                     "content": user_input
#                 })
                
#                 with st.spinner("Thinking..."):
#                     next_question = st.session_state.interviewer.generate_next_question(
#                         st.session_state.conversation_history,
#                         job_role,
#                         difficulty,
#                         company
#                     )
                    
#                     st.session_state.conversation_history.append({
#                         "role": "interviewer",
#                         "content": next_question
#                     })
                
#                 st.rerun()
        
#         # Display detailed feedback
#         if st.session_state.feedback_data and not st.session_state.interview_active:
#             st.markdown("---")
#             st.header("📊 Detailed Interview Feedback")
            
#             feedback = st.session_state.feedback_data
            
#             # Check for errors
#             if "error" in feedback:
#                 st.error(f"Error: {feedback['error']}")
#                 st.info(f"Details: {feedback.get('details', 'Unknown error')}")
#                 if "raw_response" in feedback:
#                     with st.expander("Raw Response (for debugging)"):
#                         st.code(feedback["raw_response"])
#             else:
#                 # Overall summary
#                 st.subheader("📋 Overall Summary")
#                 st.write(feedback.get("overall_summary", "No summary available"))
                
#                 # Overall score with progress bar
#                 overall_score = feedback.get("overall_score", 0)
#                 col1, col2, col3 = st.columns([2, 1, 1])
#                 with col1:
#                     st.metric("Overall Score", f"{overall_score}/10")
#                     st.progress(overall_score / 10)
#                 with col2:
#                     recommendation = feedback.get("recommendation", "N/A")
#                     recommendation_emoji = {
#                         "hire": "✅",
#                         "maybe": "⚠️",
#                         "no_hire": "❌"
#                     }
#                     st.metric("Recommendation", 
#                              f"{recommendation_emoji.get(recommendation, '❓')} {recommendation.replace('_', ' ').title()}")
#                 with col3:
#                     st.metric("Date", feedback.get("date", "N/A").split()[0])
                
#                 st.markdown("---")
                
#                 # Detailed scores
#                 col1, col2 = st.columns([1, 1])
                
#                 with col1:
#                     st.subheader("📈 Score Breakdown")
#                     scores = feedback.get("scores", {})
                    
#                     for category, data in scores.items():
#                         with st.expander(f"**{category.replace('_', ' ').title()}** - {data['score']}/10"):
#                             st.progress(data['score'] / 10)
                            
#                             st.write("**Strengths:**")
#                             for strength in data.get('strengths', []):
#                                 st.write(f"✅ {strength}")
                            
#                             st.write("**Weaknesses:**")
#                             for weakness in data.get('weaknesses', []):
#                                 st.write(f"❌ {weakness}")
                            
#                             st.write("**Details:**")
#                             st.write(data.get('details', 'No details available'))
                
#                 with col2:
#                     st.subheader("📊 Visual Performance")
#                     if scores:
#                         fig = create_score_radar_chart(scores)
#                         st.plotly_chart(fig, use_container_width=True)
                
#                 st.markdown("---")
                
#                 # Key highlights and improvements
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     st.subheader("🌟 Key Highlights")
#                     for highlight in feedback.get("key_highlights", []):
#                         st.success(f"✨ {highlight}")
                
#                 with col2:
#                     st.subheader("📈 Areas for Improvement")
#                     for area in feedback.get("improvement_areas", []):
#                         st.warning(f"⚠️ {area}")
                
#                 st.markdown("---")
                
#                 # Actionable recommendations
#                 st.subheader("💡 Actionable Recommendations")
#                 for i, rec in enumerate(feedback.get("actionable_recommendations", []), 1):
#                     st.info(f"**{i}.** {rec}")
                
#                 # Comparison with previous interview
#                 if st.session_state.candidate_id:
#                     comparison = st.session_state.interviewer.history_manager.compare_interviews(
#                         st.session_state.candidate_id
#                     )
                    
#                     if comparison:
#                         st.markdown("---")
#                         st.subheader("📊 Progress Comparison")
                        
#                         col1, col2, col3 = st.columns(3)
#                         with col1:
#                             st.metric("Improved Areas", len(comparison.get("improvements", {})))
#                         with col2:
#                             st.metric("Declined Areas", len(comparison.get("declines", {})))
#                         with col3:
#                             avg_improvement = sum(
#                                 d["change"] for d in comparison.get("improvements", {}).values()
#                             ) / max(len(comparison.get("improvements", {})), 1)
#                             st.metric("Avg Improvement", f"{avg_improvement:+.1f}")
                        
#                         fig_comparison = create_comparison_chart(comparison)
#                         st.plotly_chart(fig_comparison, use_container_width=True)
                        
#                         with st.expander("📝 Detailed Comparison"):
#                             if comparison.get("improvements"):
#                                 st.write("**Improvements:**")
#                                 for category, data in comparison["improvements"].items():
#                                     st.write(f"✅ {category.replace('_', ' ').title()}: "
#                                            f"{data['previous']} → {data['current']} "
#                                            f"(+{data['change']})")
                            
#                             if comparison.get("declines"):
#                                 st.write("**Declines:**")
#                                 for category, data in comparison["declines"].items():
#                                     st.write(f"❌ {category.replace('_', ' ').title()}: "
#                                            f"{data['previous']} → {data['current']} "
#                                            f"({data['change']})")
                
#                 # Download options
#                 st.markdown("---")
#                 col1, col2 = st.columns([1, 3])
                
#                 with col1:
#                     # Download JSON
#                     json_data = json.dumps(feedback, indent=2)
#                     st.download_button(
#                         label="📥 Download JSON",
#                         data=json_data,
#                         file_name=f"interview_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
#                         mime="application/json",
#                         use_container_width=True
#                     )
                
#                 with col2:
#                     # Download formatted report
#                     report = f"""
# INTERVIEW FEEDBACK REPORT
# {'=' * 50}

# Date: {feedback.get('date', 'N/A')}
# Job Role: {feedback.get('job_role', 'N/A')}
# Company: {feedback.get('company', 'N/A')}
# Overall Score: {feedback.get('overall_score', 'N/A')}/10
# Recommendation: {feedback.get('recommendation', 'N/A').replace('_', ' ').title()}

# OVERALL SUMMARY
# {'-' * 50}
# {feedback.get('overall_summary', 'No summary available')}

# SCORE BREAKDOWN
# {'-' * 50}
# """
#                     for category, data in feedback.get('scores', {}).items():
#                         report += f"\n{category.replace('_', ' ').title()}: {data['score']}/10\n"
#                         report += f"Strengths: {', '.join(data.get('strengths', []))}\n"
#                         report += f"Weaknesses: {', '.join(data.get('weaknesses', []))}\n"
#                         report += f"Details: {data.get('details', 'N/A')}\n"
                    
#                     report += f"\nKEY HIGHLIGHTS\n{'-' * 50}\n"
#                     for highlight in feedback.get('key_highlights', []):
#                         report += f"- {highlight}\n"
                    
#                     report += f"\nAREAS FOR IMPROVEMENT\n{'-' * 50}\n"
#                     for area in feedback.get('improvement_areas', []):
#                         report += f"- {area}\n"
                    
#                     report += f"\nACTIONABLE RECOMMENDATIONS\n{'-' * 50}\n"
#                     for i, rec in enumerate(feedback.get('actionable_recommendations', []), 1):
#                         report += f"{i}. {rec}\n"
                    
#                     st.download_button(
#                         label="📄 Download Report",
#                         data=report,
#                         file_name=f"interview_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
#                         mime="text/plain",
#                         use_container_width=True
#                     )


# if __name__ == "__main__":
#     main()