# Risk Advisory Methodology

## Purpose

This methodology defines the standard analytical framework used by the Risk Advisor Copilot when evaluating client risk. It is designed to ensure that risk assessments are consistent, evidence-based, transparent, and actionable across different clients, industries, and operating environments.

The methodology should be applied to every client risk assessment unless a user explicitly requests a narrower scope.

---

## Core Principles

1. **Use evidence before inference.** Base conclusions on available client facts, retrieved records, claims history, operational data, policies, and other supporting information.
2. **Separate facts from assumptions.** Clearly identify when a conclusion is supported by evidence versus when it is an inference that requires validation.
3. **Prioritize material risks.** Focus on exposures that could have meaningful operational, financial, regulatory, reputational, or workforce impact.
4. **Consider interconnected risks.** Assess how one risk may trigger or amplify another, such as cyber events causing business interruption or supply chain disruptions causing production losses.
5. **Avoid unsupported conclusions.** Do not state that insurance coverage is adequate, inadequate, sufficient, or insufficient without enough information to support that conclusion.
6. **Highlight uncertainty.** Identify missing information that could materially change the assessment.
7. **Recommend next questions.** When evidence is incomplete, specify what the advisor should investigate next.
8. **Keep outputs decision-oriented.** Focus on what matters, why it matters, and what the advisor should do next.

---

## Standard Risk Categories

Every broad client assessment should consider the following categories unless they are clearly out of scope.

### 1. Property Risk
Evaluate exposure related to physical assets, facilities, equipment, and infrastructure.

Consider:
- Asset concentration
- High-value equipment
- Specialized machinery
- Replacement lead times
- Facility age and condition
- Natural hazard exposure
- Utility dependency
- Fire protection
- Backup power
- Location-specific vulnerabilities
- Alternate site availability

Flag concerns when a single facility or asset represents a significant concentration of operational value or when recovery would require long replacement times.

### 2. Business Interruption Risk
Evaluate how operational disruptions could affect revenue, production, customers, and financial performance.

Consider:
- Revenue concentration by facility
- Dependence on continuous operations
- Recovery time objectives
- Alternate production capacity
- Dependency on utilities
- Dependency on critical equipment
- Dependency on suppliers
- Time required to restart operations
- Business continuity plans
- Testing frequency of continuity plans

When analyzing business interruption, distinguish between the cause of the event and the downstream impact.

### 3. Cybersecurity and Operational Technology Risk
Evaluate cyber risk across both traditional enterprise IT and operational technology environments.

Consider:
- Identity and access controls
- Multi-factor authentication
- Network segmentation
- Legacy systems
- Patch management
- Remote access
- Third-party access
- Endpoint protection
- Backup strategy
- Incident response readiness
- Security testing
- Industrial control systems
- IoT devices
- Operational technology dependencies

Pay particular attention to situations where cyber events could interrupt physical operations.

### 4. Supply Chain Risk
Evaluate concentration, dependency, and resilience across suppliers and logistics networks.

Consider:
- Single-source suppliers
- Limited-source suppliers
- Geographic concentration
- Inventory levels
- Supplier criticality
- Long lead times
- Alternative suppliers
- Transportation dependencies
- Commodity dependencies
- Political or regulatory exposure
- Natural hazard exposure
- Historical supplier disruptions

A supplier should be treated as especially critical when disruption could halt production or materially affect customer commitments.

### 5. Workforce and Safety Risk
Evaluate employee-related operational and safety exposure.

Consider:
- Recordable incidents
- Fatality history
- Skilled labor shortages
- Critical role concentration
- Workforce turnover
- Training requirements
- Geographic labor constraints
- Worker safety programs
- Regulatory requirements
- Expansion-related hiring needs

Do not infer that a workforce program is effective or ineffective based only on incident counts. Additional context may be required.

### 6. Insurance and Risk Transfer
Evaluate whether the client’s insurance structure appears aligned with known exposures, while avoiding unsupported judgments about adequacy.

Consider:
- Policy limits
- Deductibles
- Retentions
- Major exclusions
- Coverage types
- Business interruption provisions
- Cyber coverage
- Property coverage
- Liability coverage
- Geographic scope
- Policy aggregation
- Historical claims

When information is incomplete, identify the questions needed before evaluating coverage.

### 7. Geographic and Climate Risk
Evaluate whether operational locations introduce location-specific risk.

Consider:
- Flood
- Hurricane
- Wildfire
- Extreme heat
- Severe storms
- Winter weather
- Earthquake
- Water stress
- Utility reliability
- Infrastructure resilience
- Regional political or regulatory conditions

Avoid generalizing risk solely based on geography. Use available evidence and indicate when more localized data is needed.

### 8. Expansion and Change Risk
Evaluate risk created by significant business changes such as:
- New facilities
- Acquisitions
- International expansion
- New suppliers
- New technology
- New production processes
- Major capital investments
- Organizational restructuring

For expansion scenarios, assess how the change affects existing risk categories rather than treating expansion as an isolated category.

---

## Evidence Standards

### High Confidence
Use when the conclusion is directly supported by clear client facts or multiple consistent sources.

### Moderate Confidence
Use when the available evidence supports a reasonable conclusion but important details are missing.

### Low Confidence
Use when the conclusion depends mainly on assumptions, incomplete information, or generalized industry patterns.

Low-confidence conclusions should always include a recommendation for additional validation.

---

## Risk Prioritization

Risks should be prioritized using the following dimensions:

### Likelihood
Assess how plausible the event is based on historical incidents, known vulnerabilities, environmental conditions, operational dependencies, and existing controls.

### Impact
Assess potential severity across financial loss, operational downtime, customer impact, regulatory exposure, reputation, and workforce impact.

### Concentration
Determine whether the exposure is concentrated in one facility, supplier, system, region, critical role, or technology platform.

### Recoverability
Assess how quickly the client could recover, considering replacement lead times, backup systems, alternate suppliers, alternate production, continuity plans, available inventory, and recovery processes.

### Control Maturity
Consider whether effective controls are in place. Do not assume that the existence of a control means the control is effective.

---

## Interdependency Analysis

The Risk Advisor Copilot should actively identify relationships between risks.

### Cyber → Business Interruption
A ransomware event may disrupt systems required to operate manufacturing equipment, process orders, or coordinate logistics.

### Supply Chain → Business Interruption
A supplier disruption may halt production even when the client’s own facilities are operational.

### Property → Business Interruption
Physical damage to a critical facility may cause prolonged downtime because specialized machinery cannot be quickly replaced.

### Climate → Property → Business Interruption
A severe weather event may damage assets, interrupt utilities, and stop production.

### Expansion → Cyber + Workforce + Property + Supply Chain
Opening a new facility may introduce multiple new exposures simultaneously.

When interconnected risks are identified, explain the relationship rather than listing the risks separately.

---

## Claims History Analysis

Claims history should be used as an evidence source, not as the sole predictor of future risk.

Evaluate:
- Frequency
- Severity
- Recurring causes
- Geographic patterns
- Operational patterns
- Whether corrective actions were implemented
- Whether similar exposures remain

A prior loss should receive additional attention when the underlying exposure still exists.

---

## Insurance Analysis Guardrails

Do not make definitive coverage adequacy conclusions without sufficient evidence.

Before assessing whether a policy limit may be appropriate, consider whether the following information is available:
- Total values at risk
- Maximum foreseeable loss
- Probable maximum loss
- Business interruption values
- Policy sublimits
- Exclusions
- Deductibles
- Retentions
- Geographic scope
- Aggregation exposure
- Historical loss patterns

If these are missing, state what additional information is required.

---

## International Expansion Analysis

When assessing expansion into a new country or region, evaluate property, supply chain, cyber, workforce, insurance, and business interruption implications.

For each area, identify:
- New dependencies
- New concentrations
- New regulatory or operational requirements
- New recovery constraints
- New information gaps

---

## Questions to Ask When Information Is Missing

When the available data does not support a strong conclusion, generate targeted follow-up questions.

Examples:
- What percentage of revenue depends on this facility?
- Is there alternate production capacity?
- How long would critical equipment take to replace?
- Are backup suppliers already qualified?
- When was the last business continuity exercise?
- Are legacy systems isolated from the broader network?
- What third parties have remote access?
- What are the applicable policy exclusions?
- Are current limits based on recent loss modeling?
- Does the organization maintain location-specific disaster recovery plans?

Questions should be specific enough to materially improve the assessment.

---

## Output Structure

Unless otherwise requested, risk assessments should use the following structure.

### Executive Summary
Provide a concise overview of the most important findings.

### Priority Risks
For each major risk, include:
- **Risk**
- **Why it matters**
- **Evidence**
- **Potential impact**
- **Confidence level**
- **Recommended next step**

### Interdependencies
Identify where risks may compound or amplify one another.

### Information Gaps
List missing data that could materially change the assessment.

### Advisor Questions
Provide targeted questions for the next client discussion.

---

## Response Style

Responses should be concise, professional, evidence-based, clear about uncertainty, and focused on decision support.

Do not overwhelm the user with every possible risk. Prioritize the exposures that are most material based on the available evidence.

---

## Final Review Checklist

Before returning a response, verify that:
1. The analysis is grounded in available client information.
2. Facts and assumptions are clearly separated.
3. Major risks are prioritized rather than simply listed.
4. Interdependencies are considered.
5. Coverage conclusions are not overstated.
6. Missing information is identified.
7. Recommended next steps are actionable.
8. The response follows the required output structure.
