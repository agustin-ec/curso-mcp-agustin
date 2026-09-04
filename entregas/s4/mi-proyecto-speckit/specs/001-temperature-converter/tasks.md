# Tasks: Temperature Unit Converter

**Feature**: `001-temperature-converter`
**Spec**: [spec.md](file:///home/agustin/entorno-desarrollo/certificacion-ia-gen/modulo2-backend/curso-mcp-agustin/entregas/s4/mi-proyecto-speckit/specs/001-temperature-converter/spec.md)
**Plan**: [plan.md](file:///home/agustin/entorno-desarrollo/certificacion-ia-gen/modulo2-backend/curso-mcp-agustin/entregas/s4/mi-proyecto-speckit/specs/001-temperature-converter/plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, directory structure, and environment readiness.

- [X] T001 Create project directory structure with package initializers in src/__init__.py and tests/__init__.py
- [X] T002 [P] Create project documentation and CLI usage instructions in README.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain types, enum definitions, and CLI skeleton that all user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T003 [P] Implement TemperatureScale enum, aliases parsing, and custom exceptions in src/converter.py
- [X] T004 [P] Implement base CLI argument parser skeleton with flags in src/cli.py

**Checkpoint**: Foundation ready — user story implementation can begin.

---

## Phase 3: User Story 1 - Convert between Celsius and Fahrenheit (Priority: P1) 🎯 MVP

**Goal**: Convert temperature values bidirectionally between Celsius (°C) and Fahrenheit (°F) with results rounded to 2 decimal places.

**Independent Test**: Convert landmark reference temperatures (0 °C -> 32.00 °F, 100 °C -> 212.00 °F, -40 °C -> -40.00 °F, 98.6 °F -> 37.00 °C, 100 °F -> 37.78 °C) via both library function and CLI.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T005 [P] [US1] Write unit tests for Celsius and Fahrenheit conversions and rounding in tests/test_converter.py
- [X] T006 [P] [US1] Write CLI integration tests for Celsius and Fahrenheit conversions in tests/test_cli.py

### Implementation for User Story 1

- [X] T007 [US1] Implement Celsius <-> Fahrenheit conversion formulas and 2-decimal rounding in src/converter.py
- [X] T008 [US1] Implement CLI command execution for Celsius and Fahrenheit conversions in src/cli.py

**Checkpoint**: User Story 1 is fully functional, independently testable, and delivers the MVP increment.

---

## Phase 4: User Story 2 - Convert to and from Kelvin (Priority: P2)

**Goal**: Support Kelvin conversions (Celsius to Kelvin, Kelvin to Celsius, Fahrenheit to Kelvin, Kelvin to Fahrenheit) and identity conversions, rounded to 2 decimal places.

**Independent Test**: Convert reference points (0 °C -> 273.15 K, 300 K -> 26.85 °C, 32 °F -> 273.15 K, 373.15 K -> 212.00 °F, 300 K -> 300.00 K).

### Tests for User Story 2 ⚠️

- [X] T009 [P] [US2] Write unit tests for Kelvin bidirectional and identity conversions in tests/test_converter.py
- [X] T010 [P] [US2] Write CLI integration tests for Kelvin conversions and aliases in tests/test_cli.py

### Implementation for User Story 2

- [X] T011 [US2] Implement Kelvin conversion formulas and identity scale logic in src/converter.py
- [X] T012 [US2] Integrate Kelvin conversion support and unit aliases into CLI in src/cli.py

**Checkpoint**: User Story 1 AND User Story 2 both work independently and integrate seamlessly.

---

## Phase 5: User Story 3 - Physical Boundary Validation (Priority: P3)

**Goal**: Enforce physical boundary conditions, strictly rejecting temperatures in Kelvin < 0 K (and equivalent sub-absolute zero inputs) with descriptive errors, appropriate exit codes, and JSON error reporting.

**Independent Test**: Request conversion with Kelvin < 0 (e.g. -5 K) or C < -273.15 °C; verify that `AbsoluteZeroError` is raised by the library, CLI returns exit code 1 with stderr message, and 0 K succeeds.

### Tests for User Story 3 ⚠️

- [X] T013 [P] [US3] Write boundary validation unit tests for Kelvin < 0, 0 K, and sub-absolute zero values in tests/test_converter.py
- [X] T014 [P] [US3] Write CLI error handling tests for invalid inputs, exit code 1, and JSON errors in tests/test_cli.py

### Implementation for User Story 3

- [X] T015 [US3] Implement absolute zero validation logic and error raising in src/converter.py
- [X] T016 [US3] Implement CLI error handling, exit codes, and JSON error reporting in src/cli.py

**Checkpoint**: All three user stories are complete, robust against invalid inputs, and physically bounded.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, packaging exports, and end-to-end verification.

- [X] T017 [P] Add type annotations and public module exports in src/__init__.py
- [X] T018 [P] Create validation verification script in scripts/verify.sh
- [X] T019 Execute full test suite and quickstart validation guide in specs/001-temperature-converter/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — executes immediately.
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories.
- **User Story 1 (Phase 3)**: Depends on Phase 2 completion — delivers MVP.
- **User Story 2 (Phase 4)**: Depends on Phase 2 completion (builds incrementally on US1).
- **User Story 3 (Phase 5)**: Depends on Phase 2 completion (integrates boundary checks into US1/US2 conversions).
- **Polish (Phase 6)**: Depends on all user stories (Phases 3, 4, 5) being completed.

### User Story Dependencies

- **US1 (P1)**: Independent of US2 and US3.
- **US2 (P2)**: Independent of US3; shares base converter types with US1.
- **US3 (P3)**: Validates boundary inputs for all supported scales (C, F, K).

---

## Parallel Opportunities

- **Phase 1**: T001 and T002 can run in parallel.
- **Phase 2**: T003 (`src/converter.py`) and T004 (`src/cli.py`) can run in parallel.
- **Phase 3 (US1)**: T005 (`test_converter.py`) and T006 (`test_cli.py`) can run in parallel.
- **Phase 4 (US2)**: T009 (`test_converter.py`) and T010 (`test_cli.py`) can run in parallel.
- **Phase 5 (US3)**: T013 (`test_converter.py`) and T014 (`test_cli.py`) can run in parallel.
- **Phase 6 (Polish)**: T017 and T018 can run in parallel.

---

## Parallel Example: User Story 1

```bash
# Launch test creation in parallel:
Task: "Write unit tests for Celsius and Fahrenheit conversions and rounding in tests/test_converter.py"
Task: "Write CLI integration tests for Celsius and Fahrenheit conversions in tests/test_cli.py"

# After tests are in place and failing, implement core and CLI:
Task: "Implement Celsius <-> Fahrenheit conversion formulas and 2-decimal rounding in src/converter.py"
Task: "Implement CLI command execution for Celsius and Fahrenheit conversions in src/cli.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (`src/`, `tests/`, `README.md`)
2. Complete Phase 2: Foundational (Enums, Exceptions, CLI Skeleton)
3. Complete Phase 3: User Story 1 (Celsius <-> Fahrenheit with 2 decimal places)
4. **STOP and VALIDATE**: Run `python3 -m unittest tests/test_converter.py` to confirm MVP.

### Incremental Delivery

1. Foundation ready (Phases 1-2)
2. Deliver US1 (C <-> F) -> Functional MVP.
3. Deliver US2 (Kelvin bidirectional + identity) -> Full 3-scale support.
4. Deliver US3 (Physical limit validation) -> Robustness & absolute zero enforcement.
5. Polish (Phase 6) -> Documentation and quickstart smoke tests.
