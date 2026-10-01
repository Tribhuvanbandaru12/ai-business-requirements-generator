# -*- coding: utf-8 -*-
"""Mock data generator for Demo Mode.

Provides canned deliverables for the refund process and customer onboarding samples,
as well as a dynamic mock generator for custom user inputs.
"""

from __future__ import annotations
import re
from utils import make_title

# =====================================================================
# 1. REFUND PROCESS AUTOMATION MOCK DATA
# =====================================================================

REFUND_BRD = """# Business Requirements Document

## 1. Executive Summary
The customer service team is receiving an elevated volume of customer complaints regarding delayed refund processing. Currently, refunds are manually tracked using spreadsheet software, offering zero status visibility to stakeholders, managers, or end customers. The desired future state is an automated refund tracker dashboard to streamline calculations, improve transparency, and lower processing delays.

## 2. Business Problem Summary
- Current State: Refunds are manually tracked in Microsoft Excel. Customer service agents must log into several separate systems to verify details before confirming a refund status.
- Pain Points: Processing times are slow and error-prone due to manual entry. Customers frequently call or email to check status because there is no self-service visibility.
- Business Impact: Decreased customer satisfaction, high overhead costs due to repetitive support queries, and potential financial audit risks from manual errors.
- Desired Future State: A central refund dashboard showing pending refunds, delayed refunds, refund amounts, and responsible team ownership to reduce manual follow-ups.

## 3. Stakeholders and Personas
- Customer Service Agent (Persona: Sarah) [Stated]: Needs to quickly see real-time refund status to answer customer inquiries without switching between tools.
- Customer Service Manager (Persona: David) [Stated]: Needs high-level dashboard visibility to monitor SLA compliance, bottlenecks, and team workloads.
- Finance Reviewer (Persona: Elena) [Inferred]: Needs to review and approve refund amounts securely.
- End Customer (Persona: Alex) [Stated]: Desires automatic status updates or email alerts regarding refund progress.

## 4. Business Requirements (BR)
- BR-001 [Stated]: The system shall provide a centralized, real-time dashboard for managing and tracking the refund process.
- BR-002 [Stated]: The system shall reduce manual follow-up inquiries by providing proactive customer status notifications.
- BR-003 [Inferred]: The system shall provide audit trails for all refund status transitions and approvals.

## 5. Functional Requirements (FR)
- FR-001 [Stated]: The dashboard shall display pending refunds, delayed refunds, refund amounts, and the assigned team.
  - Supports: BR-001
- FR-002 [Inferred]: The system shall automatically send email notifications to customers when their refund status changes.
  - Supports: BR-002
- FR-003 [Inferred]: The system shall log the username, timestamp, and action for every refund status transition.
  - Supports: BR-003

## 6. Non-Functional Requirements (NFR)
- NFR-001 (Security) [Inferred]: Only authorized Finance and Manager roles shall approve refunds over threshold limit.
  - Supports: BR-003
- NFR-002 (Availability) [Inferred]: The dashboard must be available 99.9% of standard business hours (Threshold TBD in discovery).
  - Supports: BR-001
- NFR-003 (Performance) [Inferred]: Search results for refund status must load in under 2 seconds (Threshold TBD in discovery).
  - Supports: BR-001

## 7. User Stories (US)
- US-001 [Stated]: As a Customer Service Agent, I want to search for a refund by customer name or email, so that I can provide an immediate status update.
  - Supports: FR-001
- US-002 [Stated]: As a Customer Service Manager, I want to see pending and delayed refunds grouped by the responsible team, so that I can reallocate resources to remove bottlenecks.
  - Supports: FR-001
- US-003 [Inferred]: As a Customer, I want to receive an email update when my refund is approved, so that I don't have to call customer service.
  - Supports: FR-002

## 8. Acceptance Criteria (AC)
- AC-001a (Happy Path for US-001):
  - Given the Customer Service Agent is logged into the portal
  - When they enter a valid customer name or email in the search bar and click search
  - Then the system displays matching refund records with status, amount, and history within 2 seconds.
- AC-001b (Negative / Boundary Case for US-001):
  - Given the Customer Service Agent enters an unregistered email or non-existent reference ID
  - When they click search
  - Then the system displays "No refund records found for this query" without system errors.
- AC-002a (Happy Path for US-002):
  - Given the Manager is viewing the Dashboard page
  - When there are delayed refunds beyond the configured SLA threshold
  - Then those items are highlighted in red and sorted by delay duration.
- AC-002b (Edge Case for US-002):
  - Given there are zero delayed refunds across all teams
  - When the Manager views the delayed filter
  - Then the dashboard displays a confirmation message "All refunds are currently within SLA".
- AC-003a (Happy Path for US-003):
  - Given a customer refund status changes to "Approved"
  - When the transaction is completed
  - And the customer has a valid email on file
  - Then an automated email notification containing the refund reference ID is sent within 5 minutes.
- AC-003b (Negative Case for US-003):
  - Given a customer has an invalid or missing email address
  - When the refund status changes to "Approved"
  - Then the system logs a delivery exception flag on the dashboard for manual agent review.

## 9. UAT Test Cases
| Test Case ID | Related AC ID | Related FR ID | Scenario Type (Happy/Edge) | Preconditions | Test Steps | Expected Result |
|---|---|---|---|---|---|---|
| TC-001a | AC-001a | FR-001 | Happy | User has agent access | 1. Enter valid customer email.<br>2. Click Search. | Displays matching refund details and status. |
| TC-001b | AC-001b | FR-001 | Negative | User has agent access | 1. Enter invalid email string.<br>2. Click Search. | System displays friendly 'No records found' message. |
| TC-002a | AC-002a | FR-001 | Happy | Delayed records exist | 1. Open manager dashboard.<br>2. Check delayed queue. | Delayed refunds appear in red grouped by team. |
| TC-002b | AC-002b | FR-001 | Edge | No delayed records | 1. Clear delay queue.<br>2. Refresh dashboard. | Displays 'All refunds within SLA' banner. |
| TC-003a | AC-003a | FR-002 | Happy | Valid email present | 1. Set refund to Approved.<br>2. Check recipient inbox. | Notification email delivered with reference ID. |
| TC-003b | AC-003b | FR-002 | Negative | Missing customer email | 1. Set refund to Approved.<br>2. Inspect agent dashboard. | Delivery exception flag raised for agent follow-up. |

## 10. Requirements Traceability Matrix (RTM)
| BR ID | Business Objective | FR / NFR ID | Requirement Summary | US ID | AC ID | UAT TC ID | Status |
|---|---|---|---|---|---|---|---|
| BR-001 | Centralized dashboard for refunds | FR-001 | Display pending, delayed, and team assignments | US-001 | AC-001a | TC-001a | Draft |
| BR-001 | Centralized dashboard for refunds | FR-001 | Display pending, delayed, and team assignments | US-001 | AC-001b | TC-001b | Draft |
| BR-001 | Centralized dashboard for refunds | FR-001 | Group delayed items by responsible team | US-002 | AC-002a | TC-002a | Draft |
| BR-001 | Centralized dashboard for refunds | FR-001 | Group delayed items by responsible team | US-002 | AC-002b | TC-002b | Draft |
| BR-002 | Proactive customer notifications | FR-002 | Automated status change notification dispatch | US-003 | AC-003a | TC-003a | Draft |
| BR-002 | Proactive customer notifications | FR-002 | Automated status change notification dispatch | US-003 | AC-003b | TC-003b | Draft |
| BR-003 | Audit trails for refund transitions | FR-003 | Log username, timestamp, and transition actions | US-001 | AC-001a | TC-001a | Draft |

## 11. Risks & Assumptions
- Risks [Stated / Inferred]: Connecting the new refund tracker to legacy billing systems might cause API sync delays (Mitigation: Implement webhook queue retry mechanism).
- Assumptions [Inferred]: Legacy databases have APIs that allow extracting refund information in near real-time.

## 12. Clarification Questions & Scope Conflicts
1. What legacy systems are currently used for verifying refund eligibility?
2. What is the exact business threshold (in days or hours) for a refund to be classified as "delayed"?
3. Are multi-currency refunds supported or is it single currency only?

## 13. Suggested Next Steps
1. Conduct a process mapping workshop with customer service managers.
2. Draft a data integration diagram showing billing API fields.
3. Establish a user testing schedule with the finance approval team.
"""

REFUND_RTM = """| Business Requirement ID | Business Objective | Functional Requirement ID | Functional Requirement Summary | User Story ID | UAT Test Case ID | Coverage Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BR-001** | Real-time dashboard for refund management | FR-001 | Dashboard displays pending, delayed, and team details | US-002 | TC-001 | Covered |
| **BR-002** | Reduce customer inquiries by 40% | FR-002 | Send automatic status email notifications | US-003 | TC-002 | Covered |
| **BR-003** | Provide audit trail for all refund approvals | FR-003 | Log username, timestamp, and refund actions | US-001 | TC-003 | Covered |
"""

REFUND_JIRA = """| Issue Type | Summary | Description | Acceptance Criteria | Priority | Labels |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Story** | Refund status search bar for agent portal | As a Customer Service Agent, I want to search for a refund by name/email to give quick status updates. | AC-001: Enter email/name, click search, show status details. | High | `refund`, `search`, `customer` |
| **Story** | Dashboard pending/delayed list by team | As a Manager, I want to see pending and delayed refunds grouped by team to optimize workloads. | AC-002: Delayed (>5 days) highlighted in red, sorted by delay time. | Medium | `dashboard`, `reporting` |
| **Story** | Automatic customer approval email | As a Customer, I want an automatic email notification when approved so I don't have to call. | AC-003: On status "Approved", send mail with refund reference ID. | High | `notifications`, `email` |
"""

REFUND_QUALITY = """# BA Quality Review

## Overall Score
8.5/10

## Strengths
- Clear ID assignment (BR-001, FR-001, etc.) providing a solid reference standard.
- Specific Gherkin acceptance criteria (Given-When-Then) which make the user stories testable.
- Clear pain point analysis linking the manual Excel tracking directly to business impacts.

## Gaps or Weaknesses
- Does not specify the exact fields to display on the dashboard interface.
- Has not defined what "delayed" means in absolute units of time (e.g. business days or hours).

## Recommended Improvements
- Define the delay threshold explicitly (e.g. "delayed = pending > 3 business days").
- Add a wireframe layout or data model outlining standard refund status fields (Status, Amount, Date Submitted).

## Interview Talking Point
This review shows how an analyst acts as a quality gatekeeper. Rather than accepting requirements at face value, the analyst reviews them for completeness, testability, and edge cases before handing them off to development.
"""

REFUND_EXECUTIVE = """# Executive Summary

## Business Issue
Delayed refund processing due to manual tracking in Excel. Agents spend valuable time checking multiple systems, and customers have no transparency, leading to high support query volumes and lower customer satisfaction.

## Proposed Solution
Deploy an automated Central Refund Dashboard that pulls status records from legacy systems, provides visibility across teams, and triggers automated email updates to customers.

## Expected Business Value
- **40%+ reduction** in customer queries about refund status.
- Faster processing times and fewer manual entry errors.
- Improved management visibility into team queues and SLA bottlenecks.

## Key Risks
- Legacy database APIs may not be ready or reliable for real-time status synchronization.
- Customer support team resistance if not properly trained on the new tool.

## Decisions Needed
- Approve the 5-day SLA definition for marking refunds as "delayed."
- Confirm which support email account will be used to dispatch automated notifications.

## Recommended Next Step
Arrange a 30-minute integration review workshop with the billing systems technical owner to confirm API access.
"""


# =====================================================================
# 2. CUSTOMER ONBOARDING TRACKER MOCK DATA
# =====================================================================

ONBOARDING_BRD = """# Business Requirements Document

## 1. Executive Summary
Customer onboarding processes take too long after a sales deal closes. Account executives currently email customer details to Operations manually. Operations then manually populates the CRM, and finance performs contract validation separately. Implementation managers are often left with incomplete data. The goal is to design a central Onboarding Tracker system to reduce delays, automate entries, and ensure data completeness.

## 2. Business Problem Summary
- Current State: Manual email transitions of customer contracts. No shared system or state visibility exists across sales, operations, finance, and implementation managers.
- Pain Points: Account executives forget to send documents. Operations makes manual copy-paste errors. Finance reviews contracts asynchronously. Implementation managers lack customer context.
- Business Impact: Delayed customer go-live dates, lost contract value, and developer hours wasted waiting for specifications.
- Desired Future State: A shared Onboarding Tracker showing client name, owner, stage, blockers, expected go-live date, and overdue tasks.

## 3. Stakeholders and Personas
- Account Executive (AE) (Persona: Karen) [Stated]: Wants to close deals and automatically trigger onboarding without manual email handoffs.
- Operations Analyst (Persona: Marcus) [Stated]: Wants to see new accounts instantly and validate intake details without copy-pasting.
- Finance Specialist (Persona: Jane) [Stated]: Wants to audit contracts and check payment terms before delivery begins.
- Implementation Manager (Persona: Sam) [Stated]: Needs access to customer settings and verified files to begin system configuration.

## 4. Business Requirements (BR)
- BR-001 [Stated]: The system shall provide an automated mechanism to transition closed sales opportunities from the CRM into the onboarding pipeline.
- BR-002 [Stated]: The system shall support a unified, real-time onboarding dashboard accessible across all internal departments.
- BR-003 [Inferred]: The system shall mandate contract data completeness before an account can advance to the implementation stage.

## 5. Functional Requirements (FR)
- FR-001 [Stated]: The tracker shall automatically generate a new onboarding card when a CRM opportunity is marked "Closed-Won."
  - Supports: BR-001
- FR-002 [Stated]: The tracker UI shall display client name, owner, stage, blocker notes, expected go-live date, and overdue tasks.
  - Supports: BR-002
- FR-003 [Inferred]: The tracker shall block status changes to "Active Implementation" if the contract document link is blank.
  - Supports: BR-003

## 6. Non-Functional Requirements (NFR)
- NFR-001 (Auditing) [Inferred]: Onboarding stage changes must record user actions and timestamps for audit controls.
  - Supports: BR-003
- NFR-002 (Reporting) [Inferred]: Pipeline duration reports must be generated for management (Threshold TBD in discovery).
  - Supports: BR-002
- NFR-003 (Security) [Inferred]: Implementation managers must not have access to financial contract terms.
  - Supports: BR-002

## 7. User Stories (US)
- US-001 [Stated]: As an Operations Analyst, I want CRM closed-won deal details to populate the onboarding tracker automatically, so I don't have to copy-paste.
  - Supports: FR-001
- US-002 [Stated]: As an Implementation Manager, I want to see blocker flags and overdue tasks on my dashboard, so I can intervene early.
  - Supports: FR-002
- US-003 [Inferred]: As a Finance Specialist, I want to approve payment verification status directly in the tracker, so that delivery knows the contract is valid.
  - Supports: FR-003

## 8. Acceptance Criteria (AC)
- AC-001a (Happy Path for US-001):
  - Given a Sales opportunity is marked "Closed-Won" in the CRM
  - When the CRM webhook payload is received
  - Then a new record is created in the onboarding tracker with customer name, owner, and stage set to "Intake Draft".
- AC-001b (Negative Case for US-001):
  - Given the CRM opportunity payload is missing the primary client contact name
  - When the webhook is triggered
  - Then the tracker logs a sync warning and creates a draft card flagged as "Missing Mandatory Info".
- AC-002a (Happy Path for US-002):
  - Given an onboarding project has a task past its scheduled due date
  - When the manager loads the tracker dashboard
  - Then the record displays an "Overdue" status indicator highlighted in red.
- AC-002b (Edge Case for US-002):
  - Given an onboarding task is marked completed on the exact due date
  - When the dashboard refreshes
  - Then the status reflects "Completed On-Time" without overdue warnings.
- AC-003a (Happy Path for US-003):
  - Given the Finance specialist is reviewing a draft onboarding card
  - When they attach the contract document link and select "Contract Validated"
  - Then the system allows the stage to advance to "Active Implementation".
- AC-003b (Negative / Boundary Case for US-003):
  - Given the contract link field is blank
  - When any user attempts to transition the stage to "Active Implementation"
  - Then the system blocks the transition and displays "Validation Error: Contract document link is required".

## 9. UAT Test Cases
| Test Case ID | Related AC ID | Related FR ID | Scenario Type (Happy/Edge) | Preconditions | Test Steps | Expected Result |
|---|---|---|---|---|---|---|
| TC-001a | AC-001a | FR-001 | Happy | CRM deal active | 1. Change deal to 'Closed-Won'.<br>2. Open tracker dashboard. | Onboarding card appears automatically with correct client details. |
| TC-001b | AC-001b | FR-001 | Negative | CRM deal missing contact | 1. Trigger webhook with missing contact.<br>2. Check tracker. | Card created with 'Missing Mandatory Info' flag. |
| TC-002a | AC-002a | FR-002 | Happy | Project overdue | 1. Set task milestone to yesterday.<br>2. View tracker dashboard. | Red overdue badge is displayed. |
| TC-002b | AC-002b | FR-002 | Edge | Task completed on due date | 1. Mark task complete on due date.<br>2. View tracker dashboard. | Badge shows 'Completed On-Time'. |
| TC-003a | AC-003a | FR-003 | Happy | Valid contract link | 1. Attach contract link.<br>2. Click Advance Stage. | Stage advances to 'Active Implementation'. |
| TC-003b | AC-003b | FR-003 | Negative | Empty contract link | 1. Leave contract link blank.<br>2. Click Advance Stage. | Action blocked with mandatory link error dialog. |

## 10. Requirements Traceability Matrix (RTM)
| BR ID | Business Objective | FR / NFR ID | Requirement Summary | US ID | AC ID | UAT TC ID | Status |
|---|---|---|---|---|---|---|---|
| BR-001 | Automated CRM opportunity handoffs | FR-001 | Auto-generate onboarding card on opportunity close | US-001 | AC-001a | TC-001a | Draft |
| BR-001 | Automated CRM opportunity handoffs | FR-001 | Auto-generate onboarding card on opportunity close | US-001 | AC-001b | TC-001b | Draft |
| BR-002 | Shared onboarding tracker dashboard | FR-002 | Display client name, stage, blockers, and dates | US-002 | AC-002a | TC-002a | Draft |
| BR-002 | Shared onboarding tracker dashboard | FR-002 | Display client name, stage, blockers, and dates | US-002 | AC-002b | TC-002b | Draft |
| BR-003 | Mandate data completeness | FR-003 | Block transition if contract link is blank | US-003 | AC-003a | TC-003a | Draft |
| BR-003 | Mandate data completeness | FR-003 | Block transition if contract link is blank | US-003 | AC-003b | TC-003b | Draft |

## 11. Risks & Assumptions
- Risks [Stated / Inferred]: If CRM webhook fails, deals will not sync into onboarding (Mitigation: Add scheduled reconciliation polling).
- Assumptions [Inferred]: CRM supports outbound webhooks on opportunity status changes.

## 12. Clarification Questions & Scope Conflicts
1. Which specific CRM opportunity fields must be mapped to the onboarding card?
2. What is the defined SLA for the finance contract validation step?
3. Who is authorized to override a blocked stage transition?

## 13. Suggested Next Steps
1. Map the step-by-step handoff process from sales close to implementation kick-off.
2. Confirm CRM webhook options and permission configurations with the CRM administrator.
3. Review onboarding card field layouts with account executives.
"""

ONBOARDING_RTM = """| Business Requirement ID | Business Objective | Functional Requirement ID | Functional Requirement Summary | User Story ID | UAT Test Case ID | Coverage Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BR-001** | Automate opportunity handoffs from CRM | FR-001 | Auto-generate onboarding card on opportunity close | US-001 | TC-001 | Covered |
| **BR-002** | Provide shared onboarding tracker dashboard | FR-002 | Display client name, stage, blockers, and dates | US-002 | TC-003 | Covered |
| **BR-003** | Ensure data completeness before implementation | FR-003 | Block transition if contract link is blank | US-003 | TC-002 | Covered |
"""

ONBOARDING_JIRA = """| Issue Type | Summary | Description | Acceptance Criteria | Priority | Labels |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Story** | CRM Webhook for onboarding card creation | As an Operations Analyst, I want CRM closed-won deal details to populate the tracker automatically. | AC-001: Webhook triggers card creation, populating name, AE, and status. | High | `integration`, `crm`, `onboarding` |
| **Story** | Onboarding card dashboard UI details | As a Manager, I want to see blocker flags and overdue tasks on my dashboard view. | AC-002: Overdue indicator matches overdue date; blocker comments show. | Medium | `ui`, `dashboard` |
| **Story** | Transition validation for contract link | As a Finance Specialist, I want to ensure contract details are attached before implementation starts. | AC-003: Require contract link field to transition to 'Implementation' stage. | High | `validation`, `finance` |
"""

ONBOARDING_QUALITY = """# BA Quality Review

## Overall Score
9.0/10

## Strengths
- High-level business objective links cleanly down to functional validation steps.
- The Gherkin syntax is cleanly constructed for testing purposes.
- Recognizes the CRM handoff boundary as the main failure point.

## Gaps or Weaknesses
- Financial fields to be hidden from implementation managers have not been listed.
- Webhook failure recovery procedures have not been detailed.

## Recommended Improvements
- Define a secondary checklist for manual entry in case the CRM webhook fails.
- Detail role-based permissions (finance vs implementation manager) for sensitive fields.

## Interview Talking Point
This showcases how an analyst improves quality by identifying cross-department boundary failures. By building strict transition rules (like blocking without contract files), the analyst protects delivery timelines.
"""

ONBOARDING_EXECUTIVE = """# Executive Summary

## Business Issue
Delayed client onboarding times and manual handoff processes. Account details are emailed manually, causing copy-paste errors, contract review gaps, and implementation delays.

## Proposed Solution
Implement a shared Onboarding Tracker system integrated with the CRM to automatically log new accounts, enforce contract link presence, and highlight project blockers.

## Expected Business Value
- **Reduced turnaround times** for onboarding handoffs.
- Elimination of manual record creation errors.
- Real-time project stage and blocker visibility for management.

## Key Risks
- CRM webhook integrations may fail during peak sales cycles.
- Lack of alignment between sales processes and operations data fields.

## Decisions Needed
- Confirm the mandatory checklist fields required before implementation kickoff.
- Approve role restrictions preventing delivery teams from seeing financial terms.

## Recommended Next Step
Set up a CRM webhook discovery call with the system admin to confirm integration permissions.
"""


# =====================================================================
# 3. GENERIC DYNAMIC MOCK DATA GENERATOR
# =====================================================================

def generate_generic_mock_data(notes: str, domain: str, depth: str) -> dict[str, str]:
    """Generates realistic structured requirements using terms found in the user's input."""
    # Find some keywords
    words = re.findall(r'[a-zA-Z]{4,}', notes)
    keywords = []
    seen = set()
    for w in words:
        wl = w.lower()
        if wl not in seen and wl not in {"about", "there", "their", "would", "could", "should", "wants", "needs", "using", "wants", "tracker", "dashboard", "system", "process"}:
            seen.add(wl)
            keywords.append(w)
            if len(keywords) >= 5:
                break
                
    if not keywords:
        keywords = ["Process", "Operation", "System", "Interface", "Database"]
    
    title_text = make_title(notes, max_length=45)
    main_kw = keywords[0].capitalize()
    sec_kw = keywords[1].lower() if len(keywords) > 1 else "data"
    third_kw = keywords[2].lower() if len(keywords) > 2 else "status"
    fourth_kw = keywords[3].lower() if len(keywords) > 3 else "users"

    brd = f"""# Business Requirements Document

## 1. Executive Summary
The business is experiencing efficiency bottlenecks in the {domain} process, as described in the stakeholder notes. The primary challenges revolve around manual coordination, missing tracking points, and lack of system visibility. This project aims to deliver a modern software solution to streamline these operations, automate workflow status updates, and support standard business growth.

## 2. Business Problem Summary
- Current State: The current process is highly manual, relying on disjointed communications (such as emails or paper checklists) to handle "{sec_kw}" and verify "{third_kw}" actions.
- Pain Points: Stakeholders note that data is scattered across multiple locations, updates are delayed, and manual updates are error-prone.
- Business Impact: Delayed processing cycles, poor alignment across groups, and limited analytical reporting visibility.
- Desired Future State: A digital tool that integrates "{sec_kw}" workflows, displays real-time "{third_kw}" states, and minimizes manual intervention.

## 3. Stakeholders and Personas
- Workflow Executor (Persona: Jamie) [Stated]: Needs to input "{sec_kw}" details and track {third_kw} without dealing with manual emails.
- Process Manager (Persona: Robin) [Stated]: Needs a dashboard to oversee workflow metrics, identify delays, and audit completed steps.
- Integration Lead (Persona: Alex) [Inferred]: Needs clean interfaces to push system updates to downstream applications.

## 4. Business Requirements (BR)
- BR-001 [Stated]: The system shall centralize "{sec_kw}" management in a unified application.
- BR-002 [Stated]: The system shall provide real-time dashboard tracking of "{third_kw}" states.
- BR-003 [Inferred]: The system shall enforce data validation checks prior to finalize actions.

## 5. Functional Requirements (FR)
- FR-001 [Stated]: The system shall allow authorized operators to create, update, and search for {sec_kw} records.
  - Supports: BR-001
- FR-002 [Stated]: The system shall update the dashboard statuses automatically whenever a step completes.
  - Supports: BR-002
- FR-003 [Inferred]: The system shall validate that mandatory "{fourth_kw}" values are complete before record submission.
  - Supports: BR-003

## 6. Non-Functional Requirements (NFR)
- NFR-001 (Usability) [Inferred]: System search results must return in under 3 seconds under normal load (Threshold TBD in discovery).
  - Supports: BR-001
- NFR-002 (Security) [Inferred]: All data exchanges containing "{sec_kw}" attributes must use encrypted communication protocols.
  - Supports: BR-003
- NFR-003 (Auditability) [Inferred]: System must log history logs of all modifications, including operator name and timestamp.
  - Supports: BR-003

## 7. User Stories (US)
- US-001 [Stated]: As a Workflow Executor, I want to create a new {sec_kw} item online, so that I do not have to rely on email updates.
  - Supports: FR-001
- US-002 [Stated]: As a Process Manager, I want to view a real-time {third_kw} overview dashboard, so that I can discover operational delays.
  - Supports: FR-002
- US-003 [Inferred]: As a system integrator, I want to sync new {fourth_kw} updates automatically, so that databases remain aligned.
  - Supports: FR-003

## 8. Acceptance Criteria (AC)
- AC-001a (Happy Path for US-001):
  - Given the Workflow Executor is logged in
  - When they fill out the {sec_kw} details form and submit
  - Then the system saves the record and sets its initial status to 'Pending Review'.
- AC-001b (Negative Case for US-001):
  - Given mandatory fields in the {sec_kw} form are left blank
  - When the user clicks submit
  - Then the system prevents saving and highlights the missing fields in red.
- AC-002a (Happy Path for US-002):
  - Given the Process Manager is viewing the main tracker page
  - When {third_kw} updates occur
  - Then the dashboard metrics refresh to reflect the changes within 5 seconds.
- AC-002b (Edge Case for US-002):
  - Given there are no active {third_kw} records
  - When the Process Manager views the queue
  - Then the dashboard displays a status message 'No pending records'.
- AC-003a (Happy Path for US-003):
  - Given external {fourth_kw} updates are received
  - When the integration API executes
  - Then matching records are updated and logged in the system audit trail.
- AC-003b (Negative Case for US-003):
  - Given the external sync service is unreachable
  - When sync is attempted
  - Then the system logs a sync failure alert and queues the update for automatic retry.

## 9. UAT Test Cases
| Test Case ID | Related AC ID | Related FR ID | Scenario Type (Happy/Edge) | Preconditions | Test Steps | Expected Result |
|---|---|---|---|---|---|---|
| TC-001a | AC-001a | FR-001 | Happy | User is logged in | 1. Enter {sec_kw} fields.<br>2. Click save. | Record saved with 'Pending Review' status. |
| TC-001b | AC-001b | FR-001 | Negative | Form fields empty | 1. Leave form blank.<br>2. Click save. | Validation error highlights missing fields. |
| TC-002a | AC-002a | FR-002 | Happy | Metrics updated | 1. Update {third_kw} state.<br>2. View dashboard. | Dashboard counters refresh automatically. |
| TC-002b | AC-002b | FR-002 | Edge | Queue is empty | 1. Clear queue.<br>2. View dashboard. | Displays 'No pending records' message. |
| TC-003a | AC-003a | FR-003 | Happy | Valid {fourth_kw} data | 1. Submit complete form.<br>2. Verify database. | Record saved and logged in audit history. |
| TC-003b | AC-003b | FR-003 | Negative | Invalid {fourth_kw} data | 1. Enter invalid format.<br>2. Submit form. | System blocks submission and flags format error. |

## 10. Requirements Traceability Matrix (RTM)
| BR ID | Business Objective | FR / NFR ID | Requirement Summary | US ID | AC ID | UAT TC ID | Status |
|---|---|---|---|---|---|---|---|
| BR-001 | Centralize {sec_kw} management | FR-001 | Allow operators to create, update, search {sec_kw} | US-001 | AC-001a | TC-001a | Draft |
| BR-001 | Centralize {sec_kw} management | FR-001 | Allow operators to create, update, search {sec_kw} | US-001 | AC-001b | TC-001b | Draft |
| BR-002 | Provide real-time {third_kw} tracking | FR-002 | Automatically update dashboard status metrics | US-002 | AC-002a | TC-002a | Draft |
| BR-002 | Provide real-time {third_kw} tracking | FR-002 | Automatically update dashboard status metrics | US-002 | AC-002b | TC-002b | Draft |
| BR-003 | Enforce process validation checks | FR-003 | Validate mandatory {fourth_kw} fields | US-003 | AC-003a | TC-003a | Draft |
| BR-003 | Enforce process validation checks | FR-003 | Validate mandatory {fourth_kw} fields | US-003 | AC-003b | TC-003b | Draft |

## 11. Risks & Assumptions
- Risks [Stated / Inferred]: Inputting incorrect "{sec_kw}" information could distort downstream workflows (Mitigation: Enforce pre-submission validation rules).
- Assumptions [Inferred]: Standard corporate network connectivity will be available to all operators.

## 12. Clarification Questions & Scope Conflicts
1. What are the precise data validation rules for "{sec_kw}" fields?
2. What are the current delay criteria for status alerts?
3. Who should be notified when a process is blocked?

## 13. Suggested Next Steps
1. Conduct a requirements review session with primary workflow actors.
2. Outline current data mapping rules for integration endpoints.
3. Schedule a test review session with the verification lead.
"""

    rtm = f"""| Business Requirement ID | Business Objective | Functional Requirement ID | Functional Requirement Summary | User Story ID | UAT Test Case ID | Coverage Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BR-001** | Centralize {sec_kw} management | FR-001 | Allow operators to create, update, search {sec_kw} | US-001 | TC-001 | Covered |
| **BR-002** | Provide real-time {third_kw} tracking | FR-002 | Automatically update dashboard status metrics | US-002 | TC-002 | Covered |
| **BR-003** | Enforce process validation checks | FR-003 | Validate mandatory {fourth_kw} fields | US-003 | TC-003 | Covered |
"""

    jira = f"""| Issue Type | Summary | Description | Acceptance Criteria | Priority | Labels |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Story** | Form UI for {sec_kw} records creation | As a Workflow Executor, I want to create {sec_kw} items online to avoid emails. | AC-001: Form accepts details, saves to DB, sets status to 'Pending'. | High | `{sec_kw}`, `ui`, `workflow` |
| **Story** | Dashboard status tracking views | As a Process Manager, I want to see real-time {third_kw} dashboard items. | AC-002: Refreshes to show updated metrics when data changes. | Medium | `dashboard`, `reporting`, `{third_kw}` |
| **Story** | Data validation blocker triggers | As an integrator, I want validation rules to block incomplete forms. | AC-003: Require {fourth_kw} entries before final submission. | Medium | `validation`, `{fourth_kw}` |
"""

    quality = f"""# BA Quality Review

## Overall Score
7.8/10

## Strengths
- Good mapping of process constraints from the raw notes into logical business points.
- Acceptance criteria follow clear outcomes for testing teams.
- Identifies critical process risks regarding input data quality.

## Gaps or Weaknesses
- Needs specific rules for what constitutes complete {sec_kw} details.
- Does not specify concrete performance load metrics beyond basic page response times.

## Recommended Improvements
- Define a detailed data dictionary for the {sec_kw} entities.
- Add user authentication details to NFR guidelines.

## Interview Talking Point
Reviewing custom notes dynamically highlights the analyst's role in refining raw ideas. Translating informal complaints into strict, testable acceptance rules prevents downstream rework.
"""

    exec_summary = f"""# Executive Summary

## Business Issue
Inefficiencies and tracking gaps in the {domain} process, currently marked by manual handoffs, scattered notes, and slow updates.

## Proposed Solution
Deploy a unified process manager interface to track "{sec_kw}" statuses, automate dashboard metric reporting, and enforce input validations.

## Expected Business Value
- Unified system dashboard for operational visibility.
- Improved audit logs and tracking for quality control.
- Streamlined coordination for stakeholders handling "{third_kw}."

## Key Risks
- Legacy database integrations might not fully support real-time data syncs.
- Resistance from user groups during the initial software rollout.

## Decisions Needed
- Identify which fields are mandatory for the first iteration.
- Agree on final approval authority rules.

## Recommended Next Step
Conduct a 30-minute kickoff review with stakeholders to confirm validation checkpoints.
"""

    return {
        "brd": brd,
        "rtm": rtm,
        "jira": jira,
        "quality": quality,
        "executive": exec_summary
    }


# =====================================================================
# PUBLIC INTERFACE
# =====================================================================

def get_mock_deliverables(notes: str, domain: str = "General Business Process", depth: str = "Detailed") -> dict[str, str]:
    """Helper method to return all mock deliverables based on note keywords."""
    notes_lower = notes.lower()
    
    # Check if the notes match the Customer Onboarding sample
    if "onboarding" in notes_lower or "deal is closed" in notes_lower or "account executives" in notes_lower:
        return {
            "brd": ONBOARDING_BRD,
            "rtm": ONBOARDING_RTM,
            "jira": ONBOARDING_JIRA,
            "quality": ONBOARDING_QUALITY,
            "executive": ONBOARDING_EXECUTIVE
        }
        
    # Check if the notes match the Refund Process sample
    if "refund" in notes_lower or "excel" in notes_lower or "customer service team" in notes_lower:
        return {
            "brd": REFUND_BRD,
            "rtm": REFUND_RTM,
            "jira": REFUND_JIRA,
            "quality": REFUND_QUALITY,
            "executive": REFUND_EXECUTIVE
        }
        
    # Fallback to dynamic custom mock data
    return generate_generic_mock_data(notes, domain, depth)
