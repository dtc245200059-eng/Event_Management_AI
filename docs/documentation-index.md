# Master Documentation Index & Governance Catalog

> **Dự Án:** EventAI Pro (Hệ Thống Quản Lý Sự Kiện Tích Hợp AI)  
> **Phiên Bản:** v3.2.0-GA (Final Quality Gate & Release Baseline)  
> **Tổng Số Tài Liệu Kỹ Thuật:** 57 Tệp Markdown trong `docs/`  
> **Trạng thái kiểm duyệt:** Đã nghiệm thu toàn diện Giai đoạn 8 (100% tài liệu, kiểm thử và mã nguồn đạt chuẩn RELEASE_READY)

---

## 1. Mục Đích & Nguyên Tắc Tra Cứu

Bảng chỉ mục tài liệu (Documentation Index) giúp AI Agent và các kỹ sư phát triển nhanh chóng tra cứu:
1. **Mục đích** của từng tài liệu kỹ thuật.
2. **Trạng thái** triển khai (`[IMPLEMENTED]`, `[RESOLVED]`, `[GOVERNANCE]`, `[REPORT]`).
3. **Nguồn chân lý (Source of Truth)** đại diện trong mã nguồn hoặc CSDL.
4. **Kỹ năng AI Agent liên quan** phụ trách việc đọc hiểu, cập nhật và kiểm thử tài liệu đó.

---

## 2. Bảng Danh Mục Toàn Diện 57 Tài Liệu Kỹ Thuật (`docs/`)

| STT | Tài Liệu (Document) | Mục Đích (Purpose) | Trạng Thái (Status) | Nguồn Chân Lý (Source of Truth) | Kỹ Năng Liên Quan (Related Skills) |
|:---:|:---|:---|:---:|:---|:---|
| **1** | [acceptance-criteria.md](acceptance-criteria.md) | Đặc tả tiêu chuẩn nghiệm thu Given-When-Then cho tất cả tính năng | `[IMPLEMENTED]` | `tests/test_*.py` | [requirements-analysis](../.agents/skills/requirements-analysis/SKILL.md), [testing](../.agents/skills/testing/SKILL.md) |
| **2** | [api.md](api.md) | Đặc tả toàn bộ 67 RESTful Endpoints, Schemas, RBAC & HTTP Codes | `[IMPLEMENTED]` | `app/routes/*.py` | [api-development](../.agents/skills/api-development/SKILL.md) |
| **3** | [architecture-decisions.md](architecture-decisions.md) | Hồ sơ 8 quyết định kiến trúc hệ thống cốt lõi (ADR-001..008) | `[IMPLEMENTED]` | `app/__init__.py`, `config.py` | [architecture-design](../.agents/skills/architecture-design/SKILL.md) |
| **4** | [architecture-gap-analysis.md](architecture-gap-analysis.md) | Phân tích khoảng cách giữa kiến trúc tài liệu và mã nguồn thực tế | `[RESOLVED]` | Phase 2 Audit Report | [architecture-design](../.agents/skills/architecture-design/SKILL.md) |
| **5** | [architecture.md](architecture.md) | Kiến trúc tổng thể 3-Tier kết hợp Dual-Engine AI Service Layer | `[IMPLEMENTED]` | `app/` | [architecture-design](../.agents/skills/architecture-design/SKILL.md) |
| **6** | [chatbot-architecture.md](chatbot-architecture.md) | Kiến trúc chuyên sâu phân hệ RAG Chatbot & Dual-Engine (Live/Mock) | `[IMPLEMENTED]` | `app/services/rag_service.py` | [rag-prompt](../.agents/skills/rag-prompt/SKILL.md), [event-retrieval](../.agents/skills/event-retrieval/SKILL.md) |
| **7** | [chatbot-data-flow.md](chatbot-data-flow.md) | Sơ đồ luồng dữ liệu DFD (Mức 0, Mức 1, Mức 2) cho AI Chatbot pipeline | `[IMPLEMENTED]` | `app/routes/ai.py` | [architecture-design](../.agents/skills/architecture-design/SKILL.md) |
| **8** | [code-review.md](code-review.md) | Báo cáo thẩm định chất lượng mã nguồn theo 8 tiêu chuẩn kỹ thuật | `[IMPLEMENTED]` | `app/` (PEP 8, Clean Code) | [code-review](../.agents/skills/code-review/SKILL.md) |
| **9** | [customer-requirement.md](customer-requirement.md) | Nhu cầu khách hàng ban đầu, 4 điểm nghẽn vận hành & KPIs | `[IMPLEMENTED]` | `tailieu/de_tai_09.md` | [requirements-analysis](../.agents/skills/requirements-analysis/SKILL.md) |
| **10** | [database-design.md](database-design.md) | Thiết kế CSDL 11 bảng chuẩn 3NF, ERD, 13 B-Tree indexes, Human Gate 3 | `[IMPLEMENTED]` | `app/models.py`, `database/schema.sql` | [database-design](../.agents/skills/database-design/SKILL.md) |
| **11** | [deployment.md](deployment.md) | Hướng dẫn vận hành & triển khai Local venv, Docker, docker-compose, PaaS | `[IMPLEMENTED]` | `Dockerfile`, `docker-compose.yml`, `Procfile` | [deployment](../.agents/skills/deployment/SKILL.md) |
| **12** | [documentation-change-log.md](documentation-change-log.md) | Nhật ký chi tiết lịch sử 31 mục điều chỉnh tài liệu trong Phase 5 | `[GOVERNANCE]` | Phase 5 Progress | [documentation](../.agents/skills/documentation/SKILL.md) |
| **13** | [documentation-gap-matrix.md](documentation-gap-matrix.md) | Ma trận theo dõi và giải quyết các khoảng trống tài liệu kỹ thuật | `[GOVERNANCE]` | Phase 2 Gap Register | [documentation](../.agents/skills/documentation/SKILL.md) |
| **14** | [documentation-index.md](documentation-index.md) | Bảng chỉ mục tra cứu toàn bộ 41 tài liệu kỹ thuật dự án | `[GOVERNANCE]` | Master Documentation Index | [documentation](../.agents/skills/documentation/SKILL.md) |
| **15** | [documentation-phase5-report.md](documentation-phase5-report.md) | Báo cáo tổng kết 20 mục hoàn thành Phase 5 chuẩn mực kỹ thuật | `[REPORT]` | Phase 5 Execution Report | [documentation](../.agents/skills/documentation/SKILL.md) |
| **16** | [frontend-architecture.md](frontend-architecture.md) | Kiến trúc Presentation Layer, 27 Jinja2 templates, Apple CSS Tokens | `[IMPLEMENTED]` | `app/templates/`, `app/static/css/style.css` | [frontend-development](../.agents/skills/frontend-development/SKILL.md) |
| **17** | [gap-register.md](gap-register.md) | Sổ bộ 12 khoảng cách cốt lõi (100% RESOLVED sau Phase 6) | `[GOVERNANCE]` | Phase 6 Verification | [requirements-analysis](../.agents/skills/requirements-analysis/SKILL.md) |
| **18** | [implementation-fix-log.md](implementation-fix-log.md) | Nhật ký chi tiết 16 mục can thiệp mã nguồn chuẩn hóa trong Phase 6 | `[GOVERNANCE]` | Phase 6 Fix Log | [code-review](../.agents/skills/code-review/SKILL.md), [testing](../.agents/skills/testing/SKILL.md) |
| **19** | [implementation-fix-report.md](implementation-fix-report.md) | Báo cáo nghiệm thu hoàn thành 17 mục Phase 6 chuẩn mực kỹ thuật | `[REPORT]` | Phase 6 Execution Report | [architecture-design](../.agents/skills/architecture-design/SKILL.md) |
| **20** | [known-issues.md](known-issues.md) | Sổ bộ quản trị 4 lỗi mã nguồn (100% RESOLVED trong Phase 6) | `[GOVERNANCE]` | Phase 6 Zero-Warning Verification | [code-review](../.agents/skills/code-review/SKILL.md), [testing](../.agents/skills/testing/SKILL.md) |
| **21** | [multi-agent-architecture.md](multi-agent-architecture.md) | Kiến trúc 7-Agent Ensemble, MessageBus, Critic Guardrail, Retry Loop | `[IMPLEMENTED]` | `app/agents/*.py`, `app/services/database_service.py` | [ai-agent](../.agents/skills/ai-agent/SKILL.md), [ai-evaluation](../.agents/skills/ai-evaluation/SKILL.md) |
| **22** | [multi-agent-benchmark-report.md](multi-agent-benchmark-report.md) | Báo cáo đánh giá thực nghiệm 10 ca kiểm thử Single vs Multi-Agent | `[IMPLEMENTED]` | `tests/test_multi_agent.py::test_benchmark_suite_10_cases` | [ai-evaluation](../.agents/skills/ai-evaluation/SKILL.md) |
| **23** | [problem-audit-before-fix.md](problem-audit-before-fix.md) | Biên bản ghi nhận hiện trạng repository trước khi can thiệp | `[GOVERNANCE]` | Phase 1 Audit | [code-review](../.agents/skills/code-review/SKILL.md) |
| **24** | [question-analysis.md](question-analysis.md) | Phân tích 5 nhóm Intent & Entity Extraction cho RAG Assistant | `[IMPLEMENTED]` | `app/services/rag_service.py`, `app/agents/requirement_agent.py` | [event-retrieval](../.agents/skills/event-retrieval/SKILL.md), [rag-prompt](../.agents/skills/rag-prompt/SKILL.md) |
| **25** | [remediation-plan.md](remediation-plan.md) | Kế hoạch tổng thể 6 Phase khắc phục toàn diện dự án | `[GOVERNANCE]` | SDLC Strategy | [requirements-analysis](../.agents/skills/requirements-analysis/SKILL.md) |
| **26** | [requirements-issues.md](requirements-issues.md) | Báo cáo điểm mơ hồ, giả định kỹ thuật & Biên bản phê duyệt Human Gate 1 | `[RESOLVED]` | Customer Consensus | [requirements-analysis](../.agents/skills/requirements-analysis/SKILL.md) |
| **27** | [requirements.md](requirements.md) | Đặc tả SRS (FR-01..09, FR-AI-01..07, NFR-01..09, Business Rules) | `[IMPLEMENTED]` | `app/` Source Code | [requirements-analysis](../.agents/skills/requirements-analysis/SKILL.md) |
| **28** | [responsive-mobile.md](responsive-mobile.md) | Đặc tả Responsive, Mobile Breakpoints, Drawer, iOS Bottom Nav, Scanner | `[IMPLEMENTED]` | `app/templates/base.html`, `app/static/js/main.js` | [responsive-mobile](../.agents/skills/responsive-mobile/SKILL.md) |
| **29** | [security-review.md](security-review.md) | Đánh giá an ninh mạng OWASP Top 10 Web & OWASP Top 10 LLM | `[IMPLEMENTED]` | Security Controls | [code-review](../.agents/skills/code-review/SKILL.md) |
| **30** | [skill-gap-matrix.md](skill-gap-matrix.md) | Ma trận khoảng cách năng lực kỹ năng Agent từ Phase 2 | `[RESOLVED]` | Phase 2 Skill Audit | [documentation](../.agents/skills/documentation/SKILL.md) |
| **31** | [skill-system-change-log.md](skill-system-change-log.md) | Nhật ký thay đổi và nâng cấp toàn diện hệ thống kỹ năng | `[GOVERNANCE]` | Phase 3 & 4 Records | [documentation](../.agents/skills/documentation/SKILL.md) |
| **32** | [skill-validation-phase3.md](skill-validation-phase3.md) | Biên bản kiểm chứng 12 kỹ năng hiện hữu sau khi sửa chữa ở Phase 3 | `[GOVERNANCE]` | Phase 3 Verification Script | [testing](../.agents/skills/testing/SKILL.md) |
| **33** | [skill-validation-phase4.md](skill-validation-phase4.md) | Biên bản kiểm chứng toàn diện 18/18 kỹ năng sau khi tạo mới ở Phase 4 | `[GOVERNANCE]` | `scratch/validate_skills_phase4.py` | [testing](../.agents/skills/testing/SKILL.md) |
| **34** | [skills-dependency-map.md](skills-dependency-map.md) | Bản đồ cấu trúc và phụ thuộc liên kết giữa 18 kỹ năng Agent | `[GOVERNANCE]` | Skills Topology | [documentation](../.agents/skills/documentation/SKILL.md) |
| **35** | [skills-index.md](skills-index.md) | Bảng chỉ mục tra cứu nhanh toàn bộ 18 kỹ năng Agent | `[GOVERNANCE]` | `.agents/skills/` Catalog | [documentation](../.agents/skills/documentation/SKILL.md) |
| **36** | [test-plan.md](test-plan.md) | Kế hoạch kiểm thử tổng thể, môi trường, 5 test suites & tiêu chí pass/fail | `[IMPLEMENTED]` | `tests/` Test Suites | [testing](../.agents/skills/testing/SKILL.md) |
| **37** | [test-report.md](test-report.md) | Báo cáo chi tiết kết quả thực thi 36/36 ca kiểm thử tự động (100% Pass, 0 Warnings) | `[IMPLEMENTED]` | `tests/` Execution Logs | [testing](../.agents/skills/testing/SKILL.md) |
| **38** | [traceability-gap-matrix.md](traceability-gap-matrix.md) | Ma trận khoảng cách truy vết 9 mắt xích từ Yêu cầu đến Kỹ năng | `[GOVERNANCE]` | SDLC Alignment | [requirements-analysis](../.agents/skills/requirements-analysis/SKILL.md) |
| **39** | [traceability-matrix.md](traceability-matrix.md) | Ma trận truy vết 2 chiều (FR -> Story -> AC -> Code -> Test -> Skill) | `[IMPLEMENTED]` | End-to-End Tracing | [requirements-analysis](../.agents/skills/requirements-analysis/SKILL.md) |
| **40** | [user-guide.md](user-guide.md) | Cẩm nang hướng dẫn sử dụng 12 luồng nghiệp vụ cho 4 vai trò & AI | `[IMPLEMENTED]` | 27 Web Templates | [frontend-development](../.agents/skills/frontend-development/SKILL.md) |
| **41** | [user-stories.md](user-stories.md) | Đặc tả 20 User Stories chuẩn hóa cho 4 vai trò người dùng | `[IMPLEMENTED]` | Requirements Baseline | [requirements-analysis](../.agents/skills/requirements-analysis/SKILL.md) |
| **42** | [test-cases-phase7.md](test-cases-phase7.md) | Danh mục đặc tả toàn diện các test cases kiểm thử Phase 7 | `[IMPLEMENTED]` | `tests/`, `scratch/phase7_eval_harness.py` | [testing](../.agents/skills/testing/SKILL.md) |
| **43** | [test-results-phase7.md](test-results-phase7.md) | Sổ bộ kết quả thực thi 67 ca kiểm thử thực nghiệm Phase 7 (100% Pass) | `[REPORT]` | `scratch/phase7_eval_results.json` | [testing](../.agents/skills/testing/SKILL.md) |
| **44** | [ai-evaluation-phase7.md](ai-evaluation-phase7.md) | Báo cáo đánh giá năng lực AI: 8 kịch bản, 10 ca Benchmark, RAG & Multi-Agent | `[REPORT]` | Benchmark Suite & Gemini Services | [ai-evaluation](../.agents/skills/ai-evaluation/SKILL.md) |
| **45** | [mobile-test-report-phase7.md](mobile-test-report-phase7.md) | Báo cáo kiểm thử giao diện đáp ứng trên 9 viewports (320px..1440px) & Z-index | `[REPORT]` | DOM & CSS Tokens | [responsive-mobile](../.agents/skills/responsive-mobile/SKILL.md) |
| **46** | [security-test-report-phase7.md](security-test-report-phase7.md) | Báo cáo kiểm thử an toàn bảo mật: OWASP Top 10 Web & OWASP Top 10 LLM | `[REPORT]` | Security Controls & Defense | [code-review](../.agents/skills/code-review/SKILL.md) |
| **47** | [performance-test-report-phase7.md](performance-test-report-phase7.md) | Báo cáo đo lường định lượng độ trễ mili-giây, truy vấn N+1 & bộ nhớ | `[REPORT]` | Performance Benchmarks | [testing](../.agents/skills/testing/SKILL.md) |
| **48** | [test-coverage-analysis-phase7.md](test-coverage-analysis-phase7.md) | Phân tích độ bao phủ kiểm thử các đường dẫn nghiệp vụ cốt lõi | `[REPORT]` | Coverage Audit | [testing](../.agents/skills/testing/SKILL.md) |
| **49** | [regression-risk-phase7.md](regression-risk-phase7.md) | Ma trận phân tích rủi ro hồi quy và kết quả kiểm chứng toàn phần | `[REPORT]` | Full Regression Audit | [testing](../.agents/skills/testing/SKILL.md) |
| **50** | [phase7-testing-evaluation-report.md](phase7-testing-evaluation-report.md) | Báo cáo tổng kết nghiệm thu toàn diện 27 mục Giai đoạn 7 (READY Status) | `[REPORT]` | Phase 7 Master Report | [testing](../.agents/skills/testing/SKILL.md), [code-review](../.agents/skills/code-review/SKILL.md) |
| **51** | [reproducibility-check.md](reproducibility-check.md) | Biên bản kiểm chứng tính tái lập hệ thống từ môi trường sạch (10/10 Pass) | `[REPORT]` | Environment Verification | [deployment](../.agents/skills/deployment/SKILL.md) |
| **52** | [release-notes.md](release-notes.md) | Bản ghi chú phát hành v3.2.0 chi tiết tính năng, sửa lỗi và hướng dẫn | `[REPORT]` | Official Release Notes | [documentation](../.agents/skills/documentation/SKILL.md) |
| **53** | [release-blockers.md](release-blockers.md) | Sổ bộ quản trị điểm chặn phát hành (Xác nhận 0 điểm chặn tồn đọng) | `[GOVERNANCE]` | Release Gate Audit | [code-review](../.agents/skills/code-review/SKILL.md) |
| **54** | [release-readiness-checklist.md](release-readiness-checklist.md) | Bảng kiểm tra 76 tiêu chí sẵn sàng phát hành trên 19 phân hệ (100% Pass) | `[GOVERNANCE]` | Release Checklist | [testing](../.agents/skills/testing/SKILL.md) |
| **55** | [final-traceability-report.md](final-traceability-report.md) | Báo cáo truy vết toàn diện cuối cùng xác nhận 20/20 tính năng TRACEABLE | `[REPORT]` | End-to-End Tracing | [requirements-analysis](../.agents/skills/requirements-analysis/SKILL.md) |
| **56** | [project-baseline.md](project-baseline.md) | Đường cơ sở dự án chính thức (v3.2.0-GA Baseline) cho bảo trì tương lai | `[GOVERNANCE]` | Immutable Baseline | [architecture-design](../.agents/skills/architecture-design/SKILL.md) |
| **57** | [phase8-final-validation-report.md](phase8-final-validation-report.md) | Báo cáo thẩm định cuối cùng và quyết định phát hành 25 mục (RELEASE_READY) | `[REPORT]` | Final Quality Gate | [testing](../.agents/skills/testing/SKILL.md), [architecture-design](../.agents/skills/architecture-design/SKILL.md) |

---

## 3. Quy Tắc Duy Trì Tài Liệu Dành Cho AI Agent

1. **Tuyệt đối không sửa mã nguồn nghiệp vụ chỉ để làm khớp tài liệu**: Nếu tài liệu phát hiện mã nguồn sai hoặc thiếu, phải ghi nhận vào `IMPLEMENTATION_GAP` và theo dõi qua `docs/implementation-fix-log.md`.
2. **Không ghi nhận tính năng giả định là đã hoàn thành**: Mọi tính năng phải được dán nhãn trạng thái chính xác: `[IMPLEMENTED]`, `[PARTIALLY_IMPLEMENTED]`, `[PLANNED]`, `[DEPRECATED]`, hoặc `[UNVERIFIED]`.
3. **Kiểm tra liên kết chéo trước khi hoàn tất**: Đảm bảo 100% đường dẫn tệp tương đối tồn tại trên ổ cứng.
