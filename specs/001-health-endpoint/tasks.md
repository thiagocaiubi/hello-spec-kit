---
description: "Task list for health endpoint implementation"
---

# Tasks: Kubernetes Health Probe Endpoint

**Feature**: 001-health-endpoint  
**Input**: Design documents from `/specs/001-health-endpoint/`  
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓

**Tests**: Unit tests are REQUIRED per constitution (Testing Requirements section).

**Organization**: Single user story (US1) - entire feature is one independently testable unit.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `main.py`, `tests/unit/` at repository root
- **Tests**: Per constitution, only unit tests (`tests/unit/`) - no integration or contract tests

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization for testing infrastructure

- [ ] T001 Create tests directory structure: `tests/unit/`
- [ ] T002 Create `tests/__init__.py` (empty file for Python package)
- [ ] T003 Create `tests/unit/__init__.py` (empty file for Python package)

**Checkpoint**: Testing infrastructure ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational work needed - FastAPI and dependencies already configured

**Status**: ✅ Complete (FastAPI 0.115.11 and Uvicorn already in pyproject.toml)

---

## Phase 3: User Story 1 - Kubernetes Health Probe Check (Priority: P1) 🎯 MVP

**Goal**: Implement GET /health endpoint that returns `{"status": "ok"}` with HTTP 200 for Kubernetes probes

**Independent Test**: Send GET request to `/health`, verify 200 status and `{"status": "ok"}` response

### Tests for User Story 1 (REQUIRED per constitution)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation (TDD)**

- [ ] T004 [US1] Create test file `tests/unit/test_health.py` with imports and TestClient setup
- [ ] T005 [US1] Write test `test_health_endpoint_returns_200()` - verify status code 200
- [ ] T006 [US1] Write test `test_health_endpoint_returns_correct_json()` - verify `{"status": "ok"}` payload
- [ ] T007 [US1] Write test `test_health_endpoint_has_json_content_type()` - verify `Content-Type: application/json`
- [ ] T008 [US1] Write test `test_health_endpoint_ignores_query_params()` - verify `/health?foo=bar` still returns 200
- [ ] T009 [US1] Write test `test_health_endpoint_rejects_post_method()` - verify POST returns 405
- [ ] T010 [US1] Run tests and verify they FAIL (endpoint doesn't exist yet)

### Implementation for User Story 1

- [ ] T011 [US1] Add health endpoint route in `main.py`: `@app.get("/health")` decorator
- [ ] T012 [US1] Implement health function with type hints: `def health() -> dict[str, str]:`
- [ ] T013 [US1] Add return statement: `return {"status": "ok"}`
- [ ] T014 [US1] Run tests and verify they PASS (all 5 tests should pass)

### Validation for User Story 1

- [ ] T015 [US1] Manual test: Start server with `uvicorn main:app --reload`
- [ ] T016 [US1] Manual test: `curl http://localhost:8000/health` - verify output
- [ ] T017 [US1] Manual test: `curl -X POST http://localhost:8000/health` - verify 405 response
- [ ] T018 [US1] Performance test: Measure response time with `curl -w "\nTime: %{time_total}s\n"` - verify <100ms
- [ ] T019 [US1] Run full test suite: `python -m pytest tests/unit/` - verify all pass and complete in <5s

**Checkpoint**: User Story 1 complete - health endpoint fully functional and tested

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and final validation

- [ ] T020 Add docstring to health function explaining purpose for Kubernetes probes
- [ ] T021 Verify FastAPI auto-generated docs include /health endpoint at `http://localhost:8000/docs`
- [ ] T022 Run type checker: `mypy main.py` (if mypy available) or verify type hints are correct
- [ ] T023 Run quickstart.md validation procedures
- [ ] T024 Update main.py with any missing type hints or documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Already complete (no work needed)
- **User Story 1 (Phase 3)**: Depends on Setup (Phase 1) completion
- **Polish (Phase 4)**: Depends on User Story 1 (Phase 3) completion

### User Story 1 Task Dependencies

**Sequential order within US1**:
1. **T004-T010**: Write and verify failing tests (TDD red phase)
2. **T011-T013**: Implement endpoint (TDD green phase)
3. **T014**: Verify tests pass
4. **T015-T019**: Manual validation and performance verification

### Parallel Opportunities

- **Phase 1**: All setup tasks (T001-T003) can run in parallel
- **Phase 3 Tests**: Tests T005-T009 can be written in parallel (all are independent test functions)
- **Phase 3 Implementation**: T011-T013 must be sequential (decorator → function → return)
- **Phase 3 Validation**: T015-T018 can run in parallel (different manual test scenarios)

---

## Parallel Example: User Story 1

```bash
# After T004 (test file created), these can be written in parallel:
# Terminal 1: Write T005
# Terminal 2: Write T006  
# Terminal 3: Write T007
# Terminal 4: Write T008
# Terminal 5: Write T009

# Then run T010 to verify all fail

# Implementation (sequential):
# T011 → T012 → T013 → T014

# Validation (parallel):
# Terminal 1: T015-T016 (manual curl tests)
# Terminal 2: T017 (POST method test)
# Terminal 3: T018 (performance test)
# Terminal 4: T019 (pytest execution)
```

---

## Implementation Strategy

### MVP First (This Feature)

This entire feature IS the MVP - it's a single, minimal endpoint. Complete all tasks in order for a working health probe endpoint.

### Incremental Delivery

**Delivery Milestone**: After T019 (all tests pass)
- Endpoint is production-ready
- Can be deployed to Kubernetes
- Probes can be configured immediately

### Suggested MVP Scope

**Include**: Everything (this is already minimal)
- Phase 1: Setup
- Phase 3: User Story 1 (all tasks)
- Phase 4: Polish

**Timeline**: ~20 minutes for experienced developer

---

## Task Summary

**Total Tasks**: 24
- Setup (Phase 1): 3 tasks
- Foundational (Phase 2): 0 tasks (already complete)
- User Story 1 (Phase 3): 16 tasks (6 tests + 3 implementation + 7 validation)
- Polish (Phase 4): 5 tasks

**Estimated Time**:
- Tests: 10 minutes (T004-T010)
- Implementation: 2 minutes (T011-T013)
- Validation: 8 minutes (T014-T019)
- Polish: 5 minutes (T020-T024)
- **Total**: ~25 minutes

**Parallel Opportunities**: 8 tasks can run in parallel (tests writing, validation)

---

## Validation Checklist

✅ All tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description`  
✅ All tasks include file paths where applicable  
✅ Tasks organized by user story (single story US1)  
✅ Tests marked as REQUIRED per constitution  
✅ TDD workflow: tests first (T004-T010), then implementation (T011-T013)  
✅ Dependencies clearly documented  
✅ Parallel opportunities identified  
✅ Independent test criteria: manual curl test at T016  
✅ Constitution compliance: unit tests only, no external dependencies

---

## Notes

- **Simplicity**: This is intentionally the simplest possible feature (3 lines of implementation)
- **Constitution Aligned**: Zero new dependencies, minimal code, unit tests only
- **Production Ready**: After T019, endpoint is ready for Kubernetes deployment
- **Future Growth**: If health checks need to evolve (dependency checks, etc.), that will be a separate feature
