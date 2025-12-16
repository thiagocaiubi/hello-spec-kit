<!--
SYNC IMPACT REPORT (Generated: 2025-12-16)
================================================
Version Change: [TEMPLATE] → 1.0.0
Change Type: MINOR (Initial constitution ratification)

Modified Principles:
- Added: I. Clean Code & Simplicity
- Added: II. Minimal Dependencies

Added Sections:
- Technology Stack
- Testing Requirements

Removed Sections:
- None (initial version)

Templates Status:
✅ plan-template.md - Constitution Check section aligns with principles
✅ spec-template.md - Requirements sections support clean code validation
✅ tasks-template.md - Task structure supports unit testing requirements
⚠️ commands/*.md - No command files found to validate

Follow-up TODOs:
- None

Rationale:
Initial constitution establishing foundational principles for clean code,
minimal dependencies, and unit testing discipline for a FastAPI microservice.
================================================
-->

# hello-spec-kit Constitution

## Core Principles

### I. Clean Code & Simplicity

All code MUST adhere to clean code principles with zero tolerance for technical debt:

- **Single Responsibility**: Each module, class, and function has ONE clear purpose
- **Readable & Self-Documenting**: Code must be understandable without extensive comments; use descriptive names
- **DRY (Don't Repeat Yourself)**: No code duplication; extract common logic into reusable functions
- **Small Functions**: Functions should do one thing well; prefer multiple small functions over large ones
- **YAGNI (You Aren't Gonna Need It)**: Implement only what is needed NOW, not what might be needed later
- **Type Safety**: Use type hints throughout; all functions must have typed parameters and return values

**Rationale**: Clean code reduces cognitive load, accelerates onboarding, minimizes bugs, and makes refactoring safe. In a minimal FastAPI service, every line of code should justify its existence. Complexity is a liability that must be actively fought.

### II. Minimal Dependencies

The project MUST maintain the smallest possible dependency footprint:

- **Core Dependencies Only**: FastAPI, Uvicorn, and UV are the ONLY production dependencies
- **No External Services**: No databases, message queues, caches, or external APIs in unit tests
- **No Testing Frameworks Beyond Standard Library**: Use Python's built-in `unittest` or `pytest` if absolutely necessary; no test fixtures requiring external dependencies
- **Dependency Justification**: Any new dependency requires explicit architectural decision record (ADR) documenting why the standard library or existing dependencies are insufficient
- **Version Pinning**: All dependencies must specify exact versions (no `>=` ranges in production)

**Rationale**: Each dependency is a potential security vulnerability, maintenance burden, and source of breaking changes. A minimal dependency tree ensures faster builds, easier audits, predictable behavior, and reduced attack surface. For a simple HTTP service, the standard library + FastAPI provides everything needed.

## Technology Stack

**Language**: Python ≥ 3.10  
**HTTP Framework**: FastAPI 0.115.11 (exact version)  
**ASGI Server**: Uvicorn ≥ 0.34.0  
**Package Manager**: UV ≥ 0.5.1  
**Container Runtime**: Docker with docker-compose  
**Deployment**: Uvicorn running inside Docker container, exposed on port 8000

All code runs in a containerized environment. Local development MUST match production container configuration.

## Testing Requirements

**Unit Tests Only**: This project requires ONLY unit tests with NO external dependencies:

- **No Integration Tests**: No tests that require databases, external services, or network calls
- **No Test Databases**: No PostgreSQL, SQLite, or any persistent storage in tests
- **No Mocking External Services**: If you need to mock it, you shouldn't be testing it in unit tests
- **Pure Logic Testing**: Tests validate business logic, data transformations, and request/response handling using in-memory data structures only
- **Fast Execution**: Entire test suite must complete in under 5 seconds
- **100% Standard Library**: Tests use only Python standard library or FastAPI's built-in test client (`TestClient`)

**Test Structure**:
```
tests/
└── unit/           # Pure unit tests, no external dependencies
    ├── test_models.py
    ├── test_services.py
    └── test_endpoints.py
```

**Rationale**: Unit tests with zero external dependencies ensure tests are fast, reliable, and can run anywhere without setup. Complex integration testing is unnecessary for a minimal HTTP service where business logic is isolated and side-effect-free.

## Governance

This constitution supersedes all other development practices and coding standards.

**Amendment Process**:
1. Proposed changes must be documented with rationale and impact analysis
2. All existing code must be reviewed for compliance impact
3. Migration plan required for breaking changes
4. Templates in `.specify/templates/` must be updated to reflect changes
5. Version must be bumped according to semantic versioning rules

**Compliance**:
- All pull requests MUST verify adherence to these principles
- Code reviews MUST reject violations with reference to specific principle
- Any deviation requires explicit justification in code comments and PR description
- Automated linting and type checking enforces code quality standards

**Versioning Policy**:
- **MAJOR**: Principle removal, redefinition, or backward-incompatible governance change
- **MINOR**: New principle added or existing principle materially expanded
- **PATCH**: Clarifications, typo fixes, non-semantic refinements

**Version**: 1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16
