---
title: "Research: {Feature Name}"
phase: "research"
created: "YYYY-MM-DD"
research_score: 0
---

# Research: {Feature Name}

## 1. Intent Capture

### Core Need

**Why this needs building** (not what to build):

{The underlying "why" - describe the problem, not the solution}

### Success Criteria

{Observable, measurable outcomes that prove success}

1. {Success criterion 1 - specific, testable}
2. {Success criterion 2 - specific, testable}

### Failure Modes

{Specific anti-patterns that must be prevented}

1. **{Failure mode 1}**: {Specific scenario that would constitute failure}
2. **{Failure mode 2}**: {Specific scenario that would constitute failure}

### Value Proposition

**Before**: {Current state - what's painful/missing}

**After**: {Future state - what success looks like}

---

## 2. Context Mapping

### Domain Context

**Key entities and relationships**:

| Entity | Description | Relationships |
|--------|-------------|---------------|
| {Entity 1} | {What it is} | {How it relates} |

**Domain invariants** (what must always be true):
- {Invariant 1}

### Dependencies

**Upstream** (what we depend on):
- {Dependency 1} - {How it affects us}

**Downstream** (what depends on us):
- {Dependent 1} - {How we affect it}

### Constraints

**Technical**:
- {Constraint 1}

**Business/Resource**:
- {Constraint 1}

### Current State Validation

| Assumption | Validation Command | Expected | Actual |
|------------|-------------------|----------|--------|
| {Assumption} | `{command}` | {expected} | {actual} |

**Baseline verified**: {Yes/No - date}

---

## 3. Solution Space Exploration

### Approach 1: {Name}

**Description**: {High-level description}

**Pros**:
- {Pro 1}

**Cons**:
- {Con 1}

**Unknowns**:
- {Unknown 1}

### Approach 2: {Name}

**Description**: {High-level description}

**Pros**:
- {Pro 1}

**Cons**:
- {Con 1}

**Unknowns**:
- {Unknown 1}

### Selected Approach

**Choice**: Approach {N} - {Name}

**Rationale**: {Why this approach, referencing intent and context}

**Trade-offs accepted**: {What we're giving up}

---

## 4. Knowledge Gap Analysis

### Known Unknowns

| Unknown | Investigation Plan | Priority |
|---------|-------------------|----------|
| {Unknown 1} | {How to investigate} | {High/Medium/Low} |

### Implicit Assumption Audit

| Assumption | Category | Validation Command | Risk if Wrong |
|------------|----------|-------------------|---------------|
| {Assumption 1} | Baseline | `{command}` | {Impact} |

### Assumptions Validated

- [ ] {Pending assumption}

---

## 5. Research Quality Checklist

### Intent Completeness
- [ ] Core need states "why" not just "what"
- [ ] Success criteria are measurable and observable
- [ ] Failure modes list concrete anti-patterns
- [ ] Value proposition compares before/after states

**Grade**: {A|B|C|D|F} ({score}/4)

### Context Completeness
- [ ] Domain entities and relationships mapped
- [ ] Dependencies documented
- [ ] Constraints explicit
- [ ] Current state validated
- [ ] Baseline documented

**Grade**: {A|B|C|D|F} ({score}/5)

### Solution Space Completeness
- [ ] Multiple approaches considered
- [ ] Trade-offs explicit for each approach
- [ ] Selected approach rationale documented
- [ ] Unknowns identified

**Grade**: {A|B|C|D|F} ({score}/4)

### Knowledge Gaps Completeness
- [ ] Implicit Assumption Audit completed
- [ ] Known unknowns listed
- [ ] Assumptions explicit with validation strategies
- [ ] Risk assessed for each assumption

**Grade**: {A|B|C|D|F} ({score}/4)

---

## Overall Research Quality Score

**Total**: {sum}/17 = **{percentage}%**

**Ready for planning**: {Yes/No}

**If No, what's needed**:
- {Gap to address}
