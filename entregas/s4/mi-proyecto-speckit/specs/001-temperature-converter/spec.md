# Feature Specification: Temperature Unit Converter

**Feature Branch**: `001-temperature-converter`

**Created**: 2026-09-03

**Status**: Draft

**Input**: User description: "Convertidor de unidades de temperatura entre Celsius, Fahrenheit y Kelvin. Debe convertir correctamente entre las tres escalas, redondear a 2 decimales, y rechazar temperaturas en Kelvin menores a 0."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Convert between Celsius and Fahrenheit (Priority: P1)

As a user needing everyday temperature conversions (such as weather, cooking, or scientific comparisons), I want to convert temperature values between Celsius and Fahrenheit accurately and receive the result rounded to two decimal places.

**Why this priority**: Celsius and Fahrenheit are the most widely used temperature scales globally for daily life and commercial applications. Delivering this slice establishes the core conversion workflow and rounding mechanism as an MVP.

**Independent Test**: Can be fully tested by providing standard benchmark temperatures (such as 0 °C to 32 °F, 100 °C to 212 °F, -40 °C to -40 °F) and verifying that results are accurate to 2 decimal places.

**Acceptance Scenarios**:

1. **Given** a temperature in Celsius (e.g., 25 °C), **When** converting to Fahrenheit, **Then** the system returns 77.00 °F.
2. **Given** a temperature in Fahrenheit (e.g., 98.6 °F), **When** converting to Celsius, **Then** the system returns 37.00 °C.
3. **Given** a temperature that results in a recurring decimal (e.g., 100 °F to Celsius), **When** converting, **Then** the result is rounded to 2 decimal places (37.78 °C).
4. **Given** a negative temperature above absolute zero (e.g., -40 °C), **When** converting to Fahrenheit, **Then** the result is -40.00 °F.

---

### User Story 2 - Convert to and from Kelvin (Priority: P2)

As a student, researcher, or engineer working in scientific contexts, I want to convert temperature values to and from Kelvin (from/to Celsius and Fahrenheit) with precision rounded to two decimal places.

**Why this priority**: Kelvin is the SI base unit for thermodynamic temperature. Supporting Kelvin alongside Celsius and Fahrenheit completes the three-scale interoperability requested by the user.

**Independent Test**: Can be tested independently by converting reference points between Kelvin and Celsius/Fahrenheit (e.g., 273.15 K to 0.00 °C, 373.15 K to 212.00 °F, 300 K to 26.85 °C).

**Acceptance Scenarios**:

1. **Given** a temperature in Celsius (e.g., 0 °C), **When** converting to Kelvin, **Then** the system returns 273.15 K.
2. **Given** a temperature in Kelvin (e.g., 300 K), **When** converting to Celsius, **Then** the system returns 26.85 °C.
3. **Given** a temperature in Fahrenheit (e.g., 32 °F), **When** converting to Kelvin, **Then** the system returns 273.15 K.
4. **Given** a temperature in Kelvin (e.g., 373.15 K), **When** converting to Fahrenheit, **Then** the system returns 212.00 °F.
5. **Given** a temperature converted to the same unit (identity conversion, e.g., 300 K to Kelvin), **When** converting, **Then** the system returns 300.00 K.

---

### User Story 3 - Physical Boundary Validation (Priority: P3)

As a user or client application, I want the system to reject impossible physical temperatures (specifically Kelvin values below absolute zero) and provide an explanatory error message so that invalid calculations are prevented.

**Why this priority**: Absolute zero (0 K) is the lowest possible physical temperature. Preventing negative Kelvin values guarantees physical validity and system robustness.

**Independent Test**: Can be tested independently by supplying negative Kelvin values (e.g., -1 K, -273.15 K) and values at absolute zero (0 K) to verify proper rejection or acceptance.

**Acceptance Scenarios**:

1. **Given** a temperature in Kelvin strictly below zero (e.g., -5 K), **When** a conversion is requested, **Then** the system rejects the operation and outputs an error explaining that temperatures in Kelvin cannot be negative.
2. **Given** an exact temperature of 0 K (absolute zero), **When** converting to Celsius or Fahrenheit, **Then** the system succeeds and returns -273.15 °C or -459.67 °F.
3. **Given** a temperature in Celsius or Fahrenheit below absolute zero (e.g., -300 °C or -500 °F), **When** a conversion is requested, **Then** the system rejects the input as physically invalid (below absolute zero).

---

### Edge Cases

- **Exact Absolute Zero**: Input of 0 K must be accepted and correctly converted to -273.15 °C and -459.67 °F.
- **Just Below Absolute Zero**: Input of -0.01 K must be rejected as strictly below 0 K.
- **Round-trip Precision**: Converting 100 °C to Fahrenheit (212.00 °F) and back to Celsius must yield 100.00 °C.
- **Repeating Decimals**: Calculations resulting in recurring fractions (e.g., 1 °F to Celsius: (1 - 32) * 5/9 = -17.2222...) must round properly to -17.22 °C.
- **Coincidence Point**: -40 °C must convert to exactly -40.00 °F, and -40 °F must convert to -40.00 °C.
- **Identity Conversion**: Converting from unit X to unit X (e.g., 21.5 °C to Celsius) must return the original value formatted to 2 decimal places (21.50 °C).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support bidirectional conversions between all three temperature scales: Celsius (°C), Fahrenheit (°F), and Kelvin (K).
- **FR-002**: System MUST validate input temperatures and reject any Kelvin value strictly less than 0 (K < 0).
- **FR-003**: System MUST reject temperatures in other scales that fall below absolute zero (Celsius < -273.15 °C, Fahrenheit < -459.67 °F).
- **FR-004**: System MUST round all conversion results to exactly two (2) decimal places using standard mathematical rounding (round half-up).
- **FR-005**: System MUST return clear and descriptive error messages when an invalid temperature value or unsupported unit scale is submitted.
- **FR-006**: System MUST accept both integer and floating-point decimal numbers as input temperatures.
- **FR-007**: System MUST support case-insensitive unit identifiers for Celsius ('C', 'celsius'), Fahrenheit ('F', 'fahrenheit'), and Kelvin ('K', 'kelvin').
- **FR-008**: System MUST support identity conversions where the source and target units are the same, returning the input rounded to two decimal places.

### Key Entities *(include if feature involves data)*

- **Temperature Scale**: Represents one of the three supported thermodynamic scales: Celsius, Fahrenheit, or Kelvin.
- **Temperature Measurement**: Consists of a numeric value and an associated Temperature Scale.
- **Conversion Request**: A request containing the source Temperature Measurement and the target Temperature Scale.
- **Conversion Result**: The outcome containing either the resulting numeric value rounded to 2 decimal places with the target unit, or an error description explaining why the conversion could not be performed.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of valid conversion requests between Celsius, Fahrenheit, and Kelvin produce mathematically exact results rounded to two decimal places according to physical standard formulas.
- **SC-002**: 100% of conversion requests with Kelvin < 0 or temperatures below absolute zero are rejected with an informative error message before calculating.
- **SC-003**: Benchmark reference points (Absolute Zero, Water Freezing Point: 0 °C / 32 °F / 273.15 K, Water Boiling Point: 100 °C / 212 °F / 373.15 K, and -40 °C / -40 °F) yield zero discrepancy within 2 decimal places.
- **SC-004**: Conversion operations execute instantaneously (under 10 milliseconds per conversion) with zero noticeable lag for users.

## Assumptions

- Standard mathematical rounding (round half-up to 2 decimal places) applies to all final conversion outputs.
- Absolute zero is defined using standard scientific constants: 0 K = -273.15 °C = -459.67 °F.
- Scale identifiers may be provided as single-letter abbreviations ('C', 'F', 'K') or full English names ('celsius', 'fahrenheit', 'kelvin') in case-insensitive fashion.
- The feature is interface-agnostic at this specification stage; it specifies the conversion rules and domain behavior without restricting delivery to CLI, web service, or library.
