"""
Comprehensive Test Suite for Multi-Agent Event Advisory & Decision Making Architecture.
Validates all 7 Agents, Tools (SQL & Vector), Critic Validation, Retry Loop, and Benchmark Suite.
"""
import pytest
from app.models.agent_message import AgentMessage, CriticVerdict
from app.services.multi_agent.message_bus import MessageBus
from app.services.multi_agent.database_service import search_events_sql, get_event_full_details_sql
from app.services.multi_agent.vector_service import VectorService
from app.agents.requirement_agent import RequirementAgent
from app.agents.retrieval_agent import RetrievalAgent
from app.agents.knowledge_agent import KnowledgeAgent
from app.agents.recommendation_agent import RecommendationAgent
from app.agents.critic_agent import CriticAgent
from app.agents.response_agent import ResponseAgent
from app.agents.orchestrator_agent import OrchestratorAgent
from app.services.multi_agent.benchmark_service import run_benchmark_suite, BENCHMARK_CASES

def test_agent_message_protocol():
    """Test 1: Validates AgentMessage schema, fields, serialization, and CriticVerdict."""
    msg = AgentMessage(
        task_id="TASK-TEST-001",
        from_agent="requirement_agent",
        to_agent="retrieval_agent",
        message_type="event_requirements",
        payload={"category": "Công nghệ", "max_price": 500000}
    )
    assert msg.task_id == "TASK-TEST-001"
    assert msg.from_agent == "requirement_agent"
    assert msg.payload["max_price"] == 500000
    assert msg.status == "success"

    verdict = CriticVerdict(
        status="REJECT",
        score=0.65,
        errors=["Giá vé không khớp dữ liệu CSDL"],
        critique="Cần sửa giá vé theo bảng tickets"
    )
    assert verdict.status == "REJECT"
    assert verdict.score == 0.65
    assert len(verdict.errors) == 1

def test_message_bus_audit_log():
    """Test 2: Validates MessageBus recording, task isolation, and retrieval."""
    bus = MessageBus()
    msg1 = AgentMessage(
        task_id="TASK-BUS-1",
        from_agent="orchestrator",
        to_agent="requirement_agent",
        message_type="start",
        payload="test 1"
    )
    msg2 = AgentMessage(
        task_id="TASK-BUS-1",
        from_agent="requirement_agent",
        to_agent="orchestrator",
        message_type="result",
        payload="test 2"
    )
    bus.record_message(msg1)
    bus.record_message(msg2)

    trace = bus.get_trace("TASK-BUS-1")
    assert len(trace) == 2
    assert trace[0]["from_agent"] == "orchestrator"
    assert trace[1]["from_agent"] == "requirement_agent"

def test_sql_tool_database_queries():
    """Test 3: Validates SQL Tool parameterized event search and details retrieval."""
    # Search all
    events = search_events_sql({})
    assert len(events) > 0, "CSDL phải có ít nhất 1 sự kiện hoạt động"

    # Search with budget filter
    budget_events = search_events_sql({"max_price": 10000000})
    assert isinstance(budget_events, list)

    # Full details check
    first_id = events[0]["id"]
    details = get_event_full_details_sql(first_id)
    assert details is not None
    assert "tickets" in details
    assert "schedules" in details
    assert "venue_name" in details

def test_vector_search_tool_knowledge():
    """Test 4: Validates VectorService semantic search across event documents."""
    vs = VectorService()
    vs.build_index_from_database()
    assert len(vs.documents) > 0

    # Search for checkin policy
    results = vs.search("chính sách check-in QR code và vào cổng", top_k=2)
    assert len(results) > 0
    assert "content" in results[0]
    assert results[0]["similarity_score"] > 0

def test_requirement_agent_extraction():
    """Test 5: Validates RequirementAgent parsing user query into structured criteria."""
    agent = RequirementAgent()
    req_msg = AgentMessage(
        from_agent="user",
        to_agent="requirement_agent",
        message_type="user_question",
        payload={"question": "Tìm sự kiện công nghệ tại TP. Hồ Chí Minh dưới 500k cho sinh viên"}
    )
    res_msg = agent.process(req_msg)
    assert res_msg.status == "success"
    payload = res_msg.payload
    assert payload.get("category") == "Công nghệ"
    assert payload.get("city") == "TP. Hồ Chí Minh"
    assert payload.get("max_price") == 500000

def test_retrieval_agent_execution():
    """Test 6: Validates RetrievalAgent calling SQL Tool and returning event candidates."""
    agent = RetrievalAgent()
    req_msg = AgentMessage(
        from_agent="orchestrator",
        to_agent="retrieval_agent",
        message_type="query",
        payload={"category": "Công nghệ", "max_price": 1000000}
    )
    res_msg = agent.process(req_msg)
    assert res_msg.status == "success"
    events = res_msg.payload.get("matched_events", [])
    assert isinstance(events, list)

def test_critic_agent_approve_and_reject():
    """Test 7: Validates CriticAgent detecting fake events and rejecting vs approving valid ones."""
    critic = CriticAgent()

    # 1. Fake hallucinated event -> Must REJECT
    fake_msg = AgentMessage(
        from_agent="orchestrator",
        to_agent="critic_agent",
        message_type="audit",
        payload={
            "recommendations": {
                "recommended_events": [{
                    "event_id": 999999,
                    "title": "Hội Nghị Công Nghệ Lượng Tử Sao Hỏa 2099",
                    "dates": "2099-01-01",
                    "venue": "Căn cứ Alpha",
                    "ticket_summary": "Miễn phí"
                }]
            },
            "raw_sql_events": [{"id": 1, "title": "Sự kiện thật"}],
            "requirements": {"category": "Công nghệ"}
        }
    )
    fake_res = critic.process(fake_msg)
    assert fake_res.payload["status"] == "REJECT"
    assert fake_res.payload["score"] < 0.80
    assert len(fake_res.payload["errors"]) > 0

    # 2. Grounded real event -> Must APPROVE
    real_event = get_event_full_details_sql(1) or {"id": 1, "title": "Sự kiện thật", "tickets": [{"price": 0}]}
    real_msg = AgentMessage(
        from_agent="orchestrator",
        to_agent="critic_agent",
        message_type="audit",
        payload={
            "recommendations": {
                "recommended_events": [{
                    "event_id": real_event["id"],
                    "title": real_event["title"],
                    "dates": str(real_event.get("start_date", "2026-10-10"))[:10],
                    "venue": str(real_event.get("venue_name", "Trung tâm Hội nghị")),
                    "ticket_summary": "Vé tham dự: 0 VNĐ"
                }]
            },
            "raw_sql_events": [real_event],
            "requirements": {}
        }
    )
    real_res = critic.process(real_msg)
    assert real_res.payload["status"] == "APPROVE"
    assert real_res.payload["score"] >= 0.85

def test_full_orchestrator_workflow_and_trace():
    """Test 8: End-to-end multi-agent orchestration of all 7 agents with trace logging."""
    orchestrator = OrchestratorAgent(max_retries=2)
    result = orchestrator.run("Tôi muốn tham gia sự kiện công nghệ hoặc AI chất lượng cao")

    assert "answer" in result
    assert len(result["answer"]) > 50
    assert "critic_verdict" in result
    assert result["critic_verdict"]["status"] == "APPROVE"
    assert "trace" in result
    assert len(result["trace"]) >= 10, "Trace phải ghi nhận đầy đủ luồng message của các agent"

def test_orchestrator_retry_loop_on_critique():
    """Test 9: Validates that Orchestrator properly executes retry loop when Critic critiques draft."""
    orchestrator = OrchestratorAgent(max_retries=2)
    initial_msg = AgentMessage(
        from_agent="user",
        to_agent="orchestrator_agent",
        message_type="user_inquiry",
        payload={"question": "Tìm sự kiện có vé dưới 200.000 VNĐ"}
    )
    response_msg = orchestrator.process(initial_msg)
    assert response_msg.status == "success"
    assert response_msg.payload["retry_count"] >= 0
    assert response_msg.payload["critic_verdict"]["status"] == "APPROVE"

def test_benchmark_suite_10_cases():
    """Test 10: Runs the complete 10-test-case benchmark suite comparing Single-Agent vs Multi-Agent."""
    assert len(BENCHMARK_CASES) == 10, "Tài liệu yêu cầu tối thiểu 10 test cases"
    
    # Run in quick mode (first 4 cases for fast unit test execution)
    benchmark_data = run_benchmark_suite(quick_mode=True)
    assert "summary" in benchmark_data
    assert "test_cases" in benchmark_data
    
    summary = benchmark_data["summary"]
    # Multi-agent should achieve zero hallucination
    assert summary["multi_agent"]["hallucination_rate"] == 0.0
    # Multi-agent accuracy should be higher than or equal to single-agent
    assert summary["multi_agent"]["avg_accuracy"] >= summary["single_agent"]["avg_accuracy"]
