"""
Orchestrator Agent for Event Management AI.
Central workflow director that dispatches tasks, manages structured message exchanges,
executes the Critic retry loop, records execution traces to MessageBus, and delivers final output.
"""
import time
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent
from app.models.agent_message import AgentMessage
from app.services.multi_agent.message_bus import global_message_bus
from app.agents.requirement_agent import RequirementAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.knowledge_agent import KnowledgeAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.critic_agent import CriticAgent
from app.agents.response_agent import ResponseAgent

class OrchestratorAgent(BaseAgent):
    """
    Orchestrator Agent: Coordinates the 7-agent collaboration lifecycle,
    manages state, handles Critic rejection retries, and records full audit traces.
    """
    def __init__(self, max_retries: int = 2):
        super().__init__("orchestrator_agent")
        self.max_retries = max_retries
        
        # Instantiate sub-agents
        self.requirement_agent = RequirementAgent()
        self.retrieval_agent = RetrievalAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.recommendation_agent = RecommendationAgent()
        self.critic_agent = CriticAgent()
        self.response_agent = ResponseAgent()

    def process(self, message: AgentMessage) -> AgentMessage:
        """
        Executes the complete multi-agent workflow:
        User -> Orchestrator -> Requirement -> (Retrieval + Knowledge) -> Recommendation -> Critic (Retry loop) -> Response.
        """
        start_time = time.time()
        task_id = message.task_id
        global_message_bus.record_message(message)

        user_question = ""
        if isinstance(message.payload, dict):
            user_question = message.payload.get("question", "")
        else:
            user_question = str(message.payload)

        # ---------------------------------------------------------------------
        # STEP 1: Requirement Analysis
        # ---------------------------------------------------------------------
        req_input_msg = AgentMessage(
            task_id=task_id,
            from_agent="orchestrator_agent",
            to_agent="requirement_agent",
            message_type="analyze_question",
            payload={"question": user_question}
        )
        global_message_bus.record_message(req_input_msg)
        req_output_msg = self.requirement_agent.process(req_input_msg)
        global_message_bus.record_message(req_output_msg)
        extracted_requirements = req_output_msg.payload

        # ---------------------------------------------------------------------
        # STEP 2A: Relational Database Retrieval (SQL Tool)
        # ---------------------------------------------------------------------
        sql_input_msg = AgentMessage(
            task_id=task_id,
            from_agent="orchestrator_agent",
            to_agent="retrieval_agent",
            message_type="query_sql_events",
            payload=extracted_requirements
        )
        global_message_bus.record_message(sql_input_msg)
        sql_output_msg = self.retrieval_agent.process(sql_input_msg)
        global_message_bus.record_message(sql_output_msg)
        sql_events = sql_output_msg.payload.get("matched_events", [])

        # ---------------------------------------------------------------------
        # STEP 2B: Semantic Vector Search (Knowledge Tool)
        # ---------------------------------------------------------------------
        vec_input_msg = AgentMessage(
            task_id=task_id,
            from_agent="orchestrator_agent",
            to_agent="knowledge_agent",
            message_type="query_vector_knowledge",
            payload=extracted_requirements
        )
        global_message_bus.record_message(vec_input_msg)
        vec_output_msg = self.knowledge_agent.process(vec_input_msg)
        global_message_bus.record_message(vec_output_msg)
        knowledge_context = vec_output_msg.payload.get("context_summary", "")

        # ---------------------------------------------------------------------
        # STEP 3 & 4: Reasoning & Critic Review (with RETRY LOOP)
        # ---------------------------------------------------------------------
        retry_count = 0
        critic_feedback = None
        recommendation_payload = None
        critic_payload = None

        while True:
            # Dispatch to Recommendation Agent
            rec_input_msg = AgentMessage(
                task_id=task_id,
                from_agent="orchestrator_agent",
                to_agent="recommendation_agent",
                message_type="generate_recommendation",
                payload={
                    "requirements": extracted_requirements,
                    "sql_events": sql_events,
                    "knowledge_context": knowledge_context,
                    "critic_feedback": critic_feedback,
                    "retry_count": retry_count
                }
            )
            global_message_bus.record_message(rec_input_msg)
            rec_output_msg = self.recommendation_agent.process(rec_input_msg)
            global_message_bus.record_message(rec_output_msg)
            recommendation_payload = rec_output_msg.payload.get("recommendations", {})

            # Dispatch to Critic Agent
            critic_input_msg = AgentMessage(
                task_id=task_id,
                from_agent="orchestrator_agent",
                to_agent="critic_agent",
                message_type="audit_recommendation",
                payload={
                    "recommendations": recommendation_payload,
                    "raw_sql_events": sql_events,
                    "requirements": extracted_requirements,
                    "knowledge_context": knowledge_context
                }
            )
            global_message_bus.record_message(critic_input_msg)
            critic_output_msg = self.critic_agent.process(critic_input_msg)
            global_message_bus.record_message(critic_output_msg)
            critic_payload = critic_output_msg.payload

            # Check verdict
            if critic_payload.get("status") == "APPROVE":
                # Approved! Proceed to response
                break
            
            if retry_count >= self.max_retries:
                # Reached maximum retries, accept best effort with safety notice
                break

            # Trigger retry
            retry_count += 1
            critic_feedback = critic_payload

        # ---------------------------------------------------------------------
        # STEP 5: Final Presentation (Response Agent)
        # ---------------------------------------------------------------------
        resp_input_msg = AgentMessage(
            task_id=task_id,
            from_agent="orchestrator_agent",
            to_agent="response_agent",
            message_type="format_response",
            payload={
                "approved_recommendation": recommendation_payload,
                "critic_verdict": critic_payload,
                "user_question": user_question
            }
        )
        global_message_bus.record_message(resp_input_msg)
        resp_output_msg = self.response_agent.process(resp_input_msg)
        global_message_bus.record_message(resp_output_msg)

        total_latency = (time.time() - start_time) * 1000

        # Compile final orchestrator payload
        final_payload = {
            "answer": resp_output_msg.payload.get("text", ""),
            "recommendation": recommendation_payload,
            "critic_verdict": critic_payload,
            "retry_count": retry_count,
            "total_latency_ms": round(total_latency, 2),
            "trace": global_message_bus.get_trace(task_id)
        }

        return self.create_response(
            request_message=message,
            to_agent="user",
            message_type="orchestration_completed",
            payload=final_payload,
            latency_ms=total_latency
        )

    def run(self, user_question: str) -> Dict[str, Any]:
        """Convenience method to execute advisory inquiry directly."""
        initial_msg = AgentMessage(
            from_agent="user",
            to_agent="orchestrator_agent",
            message_type="user_inquiry",
            payload={"question": user_question}
        )
        response_msg = self.process(initial_msg)
        return response_msg.payload
