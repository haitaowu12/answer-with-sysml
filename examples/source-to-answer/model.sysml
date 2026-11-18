package ToolLibraryArchitecture {
    private import ScalarValues::*;
    doc /* Community tool lending service
    A sociotechnical service for reservation coordination, steward work, records, member communication and return-to-availability decisions. Membership eligibility remains the external registry decision; repair methods and provider decisions remain external. Logical components below are candidate responsibilities, not selected software or organisations.
    Basis: proposed; status: draft.
    Concept architecture for review. Source statements, derived mappings and design proposals retain separate status. */
    package Types {
        item def I_X_01 {
            doc /* Member, category and collection window
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_01
            Basis: derived; status: proposed.
            Source: TL-03
            Member, category and collection window
            Potential exchange; applicability: Request received */
        }
        item def I_X_02 {
            doc /* Unfilled request
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_02
            Basis: derived; status: proposed.
            Source: TL-03
            Unfilled request
            Potential exchange; applicability: No available candidate */
        }
        item def I_X_03 {
            doc /* Selected tool and member identifiers
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_03
            Basis: derived; status: proposed.
            Source: TL-04
            Selected tool and member identifiers
            Potential exchange; applicability: Candidate is available */
        }
        item def I_X_04 {
            doc /* Identified membership decision request
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_04
            Basis: derived; status: proposed.
            Source: TL-04
            Identified membership decision request
            Potential exchange; applicability: Preparation case selected */
        }
        item def I_X_05 {
            doc /* Identified candidate inspection request
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_05
            Basis: derived; status: proposed.
            Source: TL-04
            Identified candidate inspection request
            Potential exchange; applicability: Preparation case selected */
        }
        item def I_X_06 {
            doc /* Member-linked eligible/ineligible/unavailable decision
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_06
            Basis: derived; status: proposed.
            Source: TL-04
            Member-linked eligible/ineligible/unavailable decision
            Potential exchange; applicability: Registry contribution received */
        }
        item def I_X_07 {
            doc /* Tool-linked fit/unfit inspection
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_07
            Basis: derived; status: proposed.
            Source: TL-04
            Tool-linked fit/unfit inspection
            Potential exchange; applicability: Steward contribution received */
        }
        item def I_X_08 {
            doc /* Matched eligible member and fit tool evidence
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_08
            Basis: derived; status: proposed.
            Source: TL-04
            Matched eligible member and fit tool evidence
            Potential exchange; applicability: Both admission contributions permit readiness */
        }
        item def I_X_09 {
            doc /* Unavailable or ineligible membership case
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_09
            Basis: derived; status: proposed.
            Source: TL-04
            Unavailable or ineligible membership case
            Potential exchange; applicability: Admission unresolved or denied */
        }
        item def I_X_10 {
            doc /* Unfit candidate identity and inspection
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_10
            Basis: derived; status: proposed.
            Source: TL-04
            Unfit candidate identity and inspection
            Potential exchange; applicability: Candidate unfit */
        }
        item def I_X_11 {
            doc /* Member-selected wait-list or closure
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_11
            Basis: derived; status: proposed.
            Source: TL-03
            Member-selected wait-list or closure
            Potential exchange; applicability: No reservation created */
        }
        item def I_X_12 {
            doc /* Ready tool, location and deadline information
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_12
            Basis: derived; status: proposed.
            Source: TL-05
            Ready tool, location and deadline information
            Potential exchange; applicability: Ready reservation prepared */
        }
        item def I_X_13 {
            doc /* Identified tool reservation linkage
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_13
            Basis: derived; status: proposed.
            Source: TL-08
            Identified tool reservation linkage
            Potential exchange; applicability: Ready reservation committed */
        }
        item def I_X_14 {
            doc /* Notice delivery outcome
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_14
            Basis: derived; status: proposed.
            Source: TL-05
            Notice delivery outcome
            Potential exchange; applicability: Delivery evidence supplied or missing */
        }
        item def I_X_15 {
            doc /* Confirmed delivery time and reservation identity
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_15
            Basis: derived; status: proposed.
            Source: TL-05
            Confirmed delivery time and reservation identity
            Potential exchange; applicability: Actual delivery confirmed */
        }
        item def I_X_16 {
            doc /* Missing delivery confirmation
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_16
            Basis: derived; status: proposed.
            Source: TL-05
            Missing delivery confirmation
            Potential exchange; applicability: No confirmation evidence */
        }
        item def I_X_17 {
            doc /* Effective hold deadline or extension information
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_17
            Basis: derived; status: proposed.
            Source: TL-05
            Effective hold deadline or extension information
            Potential exchange; applicability: Deadline communication needs reconciliation */
        }
        item def I_X_18 {
            doc /* Current ready reservation
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_18
            Basis: derived; status: proposed.
            Source: TL-06
            Current ready reservation
            Potential exchange; applicability: Member presents for collection */
        }
        item def I_X_19 {
            doc /* Deadline and collection/withdrawal state
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_19
            Basis: derived; status: proposed.
            Source: TL-05
            Deadline and collection/withdrawal state
            Potential exchange; applicability: Deadline passed or withdrawal received */
        }
        item def I_X_20 {
            doc /* Still-fit release or reasoned extension disposition
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_20
            Basis: derived; status: proposed.
            Source: TL-05
            Still-fit release or reasoned extension disposition
            Potential exchange; applicability: Coordinator decides */
        }
        item def I_X_21 {
            doc /* Extended or closed request outcome
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_21
            Basis: derived; status: proposed.
            Source: TL-08
            Extended or closed request outcome
            Potential exchange; applicability: Disposition recorded */
        }
        item def I_X_22 {
            doc /* Matched member and identified tool
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_22
            Basis: derived; status: proposed.
            Source: TL-06
            Matched member and identified tool
            Potential exchange; applicability: Identity and reservation match */
        }
        item def I_X_23 {
            doc /* Unresolved identity or tool mismatch
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_23
            Basis: derived; status: proposed.
            Source: TL-06
            Unresolved identity or tool mismatch
            Potential exchange; applicability: Matching incomplete */
        }
        item def I_X_24 {
            doc /* Accepted terms and identified-tool receipt
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_24
            Basis: derived; status: proposed.
            Source: TL-06
            Accepted terms and identified-tool receipt
            Potential exchange; applicability: Both acceptance obligations recorded */
        }
        item def I_X_25 {
            doc /* Unresolved acceptance
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_25
            Basis: derived; status: proposed.
            Source: TL-06
            Unresolved acceptance
            Potential exchange; applicability: Acceptance incomplete */
        }
        item def I_X_26 {
            doc /* Recorded library-to-member custody transfer
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_26
            Basis: derived; status: proposed.
            Source: TL-06
            Recorded library-to-member custody transfer
            Potential exchange; applicability: Custody record exists */
        }
        item def I_X_27 {
            doc /* On-loan state and custody link
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_27
            Basis: derived; status: proposed.
            Source: TL-06
            On-loan state and custody link
            Potential exchange; applicability: After transfer record */
        }
        item def I_X_28 {
            doc /* Confirmed physical receipt and library custody
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_28
            Basis: derived; status: proposed.
            Source: TL-07
            Confirmed physical receipt and library custody
            Potential exchange; applicability: Identified tool received */
        }
        item def I_X_29 {
            doc /* Awaiting-assessment state and custody
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_29
            Basis: derived; status: proposed.
            Source: TL-07
            Awaiting-assessment state and custody
            Potential exchange; applicability: Receipt confirmed */
        }
        item def I_X_30 {
            doc /* Fit return inspection
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_30
            Basis: derived; status: proposed.
            Source: TL-07
            Fit return inspection
            Potential exchange; applicability: Tool assessed fit */
        }
        item def I_X_31 {
            doc /* Unfit return inspection
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_31
            Basis: derived; status: proposed.
            Source: TL-07
            Unfit return inspection
            Potential exchange; applicability: Tool assessed unfit */
        }
        item def I_X_32 {
            doc /* Quarantined tool and defect context
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_32
            Basis: derived; status: proposed.
            Source: TL-07
            Quarantined tool and defect context
            Potential exchange; applicability: Coordinator considers repair */
        }
        item def I_X_33 {
            doc /* Quarantine state
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_33
            Basis: derived; status: proposed.
            Source: TL-08
            Quarantine state
            Potential exchange; applicability: Unfit condition retained */
        }
        item def I_X_34 {
            doc /* Repair case and identified tool
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_34
            Basis: derived; status: proposed.
            Source: TL-07
            Repair case and identified tool
            Potential exchange; applicability: External repair requested */
        }
        item def I_X_35 {
            doc /* Completed work and remaining defects
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_35
            Basis: derived; status: proposed.
            Source: TL-07
            Completed work and remaining defects
            Potential exchange; applicability: Provider report received */
        }
        item def I_X_36 {
            doc /* Steward fit reassessment
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_36
            Basis: derived; status: proposed.
            Source: TL-07
            Steward fit reassessment
            Potential exchange; applicability: Tool reassessed fit */
        }
        item def I_X_37 {
            doc /* Remaining defects/unfit reassessment
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_37
            Basis: derived; status: proposed.
            Source: TL-07
            Remaining defects/unfit reassessment
            Potential exchange; applicability: Quarantine retained */
        }
        item def I_X_38 {
            doc /* New repair decision
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_38
            Basis: derived; status: proposed.
            Source: TL-07
            New repair decision
            Potential exchange; applicability: Coordinator requests another attempt */
        }
        item def I_X_39 {
            doc /* Retirement or retained-quarantine disposition
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_39
            Basis: derived; status: proposed.
            Source: TL-07
            Retirement or retained-quarantine disposition
            Potential exchange; applicability: Coordinator decides */
        }
        item def I_X_40 {
            doc /* Authorised available status
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_40
            Basis: derived; status: proposed.
            Source: TL-07
            Authorised available status
            Potential exchange; applicability: Required condition/release evidence present */
        }
        item def I_X_41 {
            doc /* Available inventory identities
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_41
            Basis: derived; status: proposed.
            Source: TL-08
            Available inventory identities
            Potential exchange; applicability: Tool not reserved/on-loan/awaiting assessment/quarantined */
        }
        item def I_X_42 {
            doc /* Current inventory, reservation and exception state
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_42
            Basis: derived; status: proposed.
            Source: TL-08
            Current inventory, reservation and exception state
            Potential exchange; applicability: Current outcome needed */
        }
        item def I_X_43 {
            doc /* Accountable pending/refused/closed outcome
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_43
            Basis: derived; status: proposed.
            Source: TL-08
            Accountable pending/refused/closed outcome
            Potential exchange; applicability: Exception disposition known */
        }
        item def I_X_44 {
            doc /* Unresolved exception and retained state
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_44
            Basis: derived; status: proposed.
            Source: TL-08
            Unresolved exception and retained state
            Potential exchange; applicability: Exception persists */
        }
        item def I_CX_01 {
            doc /* Request, period, category, wait-list/closure choice and withdrawal
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_01
            Basis: derived; status: proposed.
            Source: TL-03
            Request, period, category, wait-list/closure choice and withdrawal
            Potential exchange; applicability:  */
        }
        item def I_CX_02 {
            doc /* Identified membership eligibility query
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_02
            Basis: derived; status: proposed.
            Source: TL-04
            Identified membership eligibility query
            Potential exchange; applicability:  */
        }
        item def I_CX_03 {
            doc /* Member-linked eligibility decision and decision identity
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_03
            Basis: derived; status: proposed.
            Source: TL-04
            Member-linked eligibility decision and decision identity
            Potential exchange; applicability:  */
        }
        item def I_CX_04 {
            doc /* Ready tool, location, deadline and current request outcome
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_04
            Basis: derived; status: proposed.
            Source: TL-05
            Ready tool, location, deadline and current request outcome
            Potential exchange; applicability:  */
        }
        item def I_CX_05 {
            doc /* Loan terms and identified-tool receipt acceptance
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_05
            Basis: derived; status: proposed.
            Source: TL-06
            Loan terms and identified-tool receipt acceptance
            Potential exchange; applicability:  */
        }
        item def I_CX_06 {
            doc /* Tool-linked condition findings and inspections
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_06
            Basis: derived; status: proposed.
            Source: TL-04
            Tool-linked condition findings and inspections
            Potential exchange; applicability:  */
        }
        item def I_CX_07 {
            doc /* Matching and physical returned-tool receipt evidence
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_07
            Basis: derived; status: proposed.
            Source: TL-07
            Matching and physical returned-tool receipt evidence
            Potential exchange; applicability:  */
        }
        item def I_CX_08 {
            doc /* Identified-tool repair request and defects
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_08
            Basis: derived; status: proposed.
            Source: TL-07
            Identified-tool repair request and defects
            Potential exchange; applicability:  */
        }
        item def I_CX_09 {
            doc /* Work completed and known remaining defects
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_09
            Basis: derived; status: proposed.
            Source: TL-07
            Work completed and known remaining defects
            Potential exchange; applicability:  */
        }
        item def I_CX_10 {
            doc /* Exception, extension and reservation disposition
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_10
            Basis: derived; status: proposed.
            Source: TL-05
            Exception, extension and reservation disposition
            Potential exchange; applicability:  */
        }
        item def I_CX_11 {
            doc /* Repair, quarantine release or retirement decision
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_11
            Basis: derived; status: proposed.
            Source: TL-07
            Repair, quarantine release or retirement decision
            Potential exchange; applicability:  */
        }
        item def I_CX_12 {
            doc /* Tool identity, custody, condition and reservation linkage
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_12
            Basis: derived; status: proposed.
            Source: TL-08
            Tool identity, custody, condition and reservation linkage
            Potential exchange; applicability:  */
        }
        part def T_A_MEMBER {
            doc /* Member
            Requests and collects a tool; accepts loan terms and receipt.
            Record: A_MEMBER
            Basis: source-explicit; status: draft.
            Source: TL-02
            Source: TL-06 */
            port p_CX_01 : P_CX_01;
            port p_CX_04 : ~P_CX_04;
            port p_CX_05 : P_CX_05;
        }
        part def T_A_STEWARD {
            doc /* Volunteer steward
            Handles tools, confirms receipt and assesses condition.
            Record: A_STEWARD
            Basis: source-explicit; status: draft.
            Source: TL-02
            Source: TL-07 */
            port p_CX_06 : P_CX_06;
            port p_CX_07 : P_CX_07;
            port p_CX_12 : ~P_CX_12;
        }
        part def T_A_COORD {
            doc /* Duty coordinator
            Owns exceptions, extensions, repair requests and quarantine release decisions.
            Record: A_COORD
            Basis: source-explicit; status: draft.
            Source: TL-02
            Source: TL-05
            Source: TL-07 */
            port p_CX_10 : P_CX_10;
            port p_CX_11 : P_CX_11;
        }
        part def T_A_REGISTRY {
            doc /* External membership registry
            Sole authority for the membership eligibility decision.
            Record: A_REGISTRY
            Basis: source-explicit; status: draft.
            Source: TL-01
            Source: TL-02
            Source: TL-04 */
            port p_CX_02 : ~P_CX_02;
            port p_CX_03 : P_CX_03;
        }
        part def T_A_REPAIR {
            doc /* External repair provider
            Reports completed work and remaining defects; cannot release tools for lending.
            Record: A_REPAIR
            Basis: source-explicit; status: draft.
            Source: TL-02
            Source: TL-07 */
            port p_CX_08 : ~P_CX_08;
            port p_CX_09 : P_CX_09;
        }
        action def T_OA_REQUEST {
            doc /* Request and accept a tool loan
            Express the need, select wait-list/closure and accept a specific loan.
            Record: OA_REQUEST
            Basis: derived; status: proposed.
            Source: TL-03
            Source: TL-06 */
        }
        action def T_OA_COORD {
            doc /* Coordinate reservations and exceptions
            Select a candidate, keep unresolved cases accountable and govern reservation disposition.
            Record: OA_COORD
            Basis: derived; status: proposed.
            Source: TL-03
            Source: TL-05 */
        }
        action def T_OA_ELIG {
            doc /* Decide membership eligibility
            Return identified eligible, ineligible or unavailable decision.
            Record: OA_ELIG
            Basis: derived; status: proposed.
            Source: TL-02
            Source: TL-04 */
        }
        action def T_OA_CONDITION {
            doc /* Assess identified-tool condition
            Inspect candidate, return or repaired tool and retain fit/unfit evidence.
            Record: OA_CONDITION
            Basis: derived; status: proposed.
            Source: TL-04
            Source: TL-07 */
        }
        action def T_OA_CUSTODY {
            doc /* Confirm tool handover and return
            Confirm matched collection, terms/receipt and physical returned-tool receipt.
            Record: OA_CUSTODY
            Basis: derived; status: proposed.
            Source: TL-06
            Source: TL-07 */
        }
        action def T_OA_REPAIR {
            doc /* Report repair outcome
            Supply completed work and known remaining defects for reassessment.
            Record: OA_REPAIR
            Basis: derived; status: proposed.
            Source: TL-02
            Source: TL-07 */
        }
        action def T_OA_INFO {
            doc /* Maintain accountable service information
            Make current request, inventory, custody and exception information available.
            Record: OA_INFO
            Basis: derived; status: proposed.
            Source: TL-08 */
        }
        action def T_F_ROOT {
            doc /* Deliver a tool lending service
            Group functions by outcome, inputs and handover responsibility.
            Record: F_ROOT
            Basis: derived; status: proposed.
            Source: TL-01 */
        }
        action def T_F_ACQUIRE {
            doc /* Prepare an eligible and fit reservation
            Group functions by outcome, inputs and handover responsibility.
            Record: F_ACQUIRE
            Basis: derived; status: proposed.
            Source: TL-01 */
        }
        action def T_F_LOAN {
            doc /* Notify and transfer the reserved tool
            Group functions by outcome, inputs and handover responsibility.
            Record: F_LOAN
            Basis: derived; status: proposed.
            Source: TL-01 */
        }
        action def T_F_RETURN {
            doc /* Recover the returned tool
            Group functions by outcome, inputs and handover responsibility.
            Record: F_RETURN
            Basis: derived; status: proposed.
            Source: TL-01 */
        }
        action def T_F_SUPPORT {
            doc /* Keep service decisions and state accountable
            Group functions by outcome, inputs and handover responsibility.
            Record: F_SUPPORT
            Basis: derived; status: proposed.
            Source: TL-01 */
        }
        action def T_F_REQUEST {
            doc /* Capture the request
            Retain member, category and desired collection period.
            Record: F_REQUEST
            Basis: derived; status: proposed.
            Source: TL-03 */
            out item out_X_01 : I_X_01;
        }
        action def T_F_SELECT {
            doc /* Select an available identified candidate
            Use the current inventory state; do not reserve inventory for a wait-list.
            Record: F_SELECT
            Basis: derived; status: proposed.
            Source: TL-03
            Source: TL-08 */
            in item in_X_01 : I_X_01;
            out item out_X_02 : I_X_02;
            out item out_X_03 : I_X_03;
            in item in_X_41 : I_X_41;
        }
        action def T_F_NO_CAND {
            doc /* Dispose of an unfilled request
            Offer wait-list or closure at the member choice without a tool reservation.
            Record: F_NO_CAND
            Basis: derived; status: proposed.
            Source: TL-03 */
            in item in_X_02 : I_X_02;
            out item out_X_11 : I_X_11;
        }
        action def T_F_PREP {
            doc /* Establish the preparation case
            Retain the selected member/tool identifiers before the two independent preparation contributions.
            Record: F_PREP
            Basis: derived; status: proposed.
            Source: TL-04 */
            in item in_X_03 : I_X_03;
            out item out_X_04 : I_X_04;
            out item out_X_05 : I_X_05;
        }
        action def T_F_ELIG {
            doc /* Obtain the registry decision
            Request and retain the external decision and identifiers; do not manufacture a positive decision.
            Record: F_ELIG
            Basis: derived; status: proposed.
            Source: TL-02
            Source: TL-04 */
            in item in_X_04 : I_X_04;
            out item out_X_06 : I_X_06;
        }
        action def T_F_INSPECT {
            doc /* Inspect the candidate tool
            Retain the steward fit/unfit finding for the selected identified tool.
            Record: F_INSPECT
            Basis: derived; status: proposed.
            Source: TL-04 */
            in item in_X_05 : I_X_05;
            out item out_X_07 : I_X_07;
        }
        action def T_F_ASSESS {
            doc /* Assess preparation contributions
            Match member/tool evidence and distinguish eligible-and-fit, unavailable, ineligible and unfit cases.
            Record: F_ASSESS
            Basis: derived; status: proposed.
            Source: TL-04 */
            in item in_X_06 : I_X_06;
            in item in_X_07 : I_X_07;
            out item out_X_08 : I_X_08;
            out item out_X_09 : I_X_09;
            out item out_X_10 : I_X_10;
        }
        action def T_F_RESERVE {
            doc /* Prepare the ready reservation
            Commit the eligible member/fit identified tool reservation; exclude that tool from available offers.
            Record: F_RESERVE
            Basis: derived; status: proposed.
            Source: TL-04
            Source: TL-08 */
            in item in_X_08 : I_X_08;
            out item out_X_12 : I_X_12;
            out item out_X_13 : I_X_13;
        }
        action def T_F_NOTICE {
            doc /* Deliver the ready notice
            Provide tool, location and hold deadline; retain delivery outcome separately from queueing. Deadline/acknowledgement coordination needs agreement.
            Record: F_NOTICE
            Basis: derived; status: proposed.
            Source: TL-05 */
            in item in_X_12 : I_X_12;
            out item out_X_14 : I_X_14;
            in item in_X_17 : I_X_17;
        }
        action def T_F_CONFIRM {
            doc /* Record confirmed notice delivery
            Retain actual confirmed delivery time; missing confirmation remains pending-notification.
            Record: F_CONFIRM
            Basis: derived; status: proposed.
            Source: TL-05 */
            in item in_X_14 : I_X_14;
            out item out_X_15 : I_X_15;
            out item out_X_16 : I_X_16;
        }
        action def T_F_HOLD {
            doc /* Govern the confirmed hold interval
            Bind the minimum hold to confirmed delivery time; withdrawal/new fault exceptions remain separate.
            Record: F_HOLD
            Basis: derived; status: proposed.
            Source: TL-05 */
            in item in_X_15 : I_X_15;
            out item out_X_17 : I_X_17;
            out item out_X_18 : I_X_18;
            out item out_X_19 : I_X_19;
            attribute minimumConfirmedDeliveryHold : ISQBase::DurationValue;
        }
        action def T_F_EXPIRY {
            doc /* Resolve expiry, withdrawal or extension
            Coordinator returns a still-fit tool after expiry or records the extension reason; withdrawal is a separate release cause.
            Record: F_EXPIRY
            Basis: derived; status: proposed.
            Source: TL-05 */
            in item in_X_19 : I_X_19;
            out item out_X_20 : I_X_20;
            out item out_X_21 : I_X_21;
        }
        action def T_F_MATCH {
            doc /* Match the collection case
            Steward checks member and allocated tool against the reservation.
            Record: F_MATCH
            Basis: derived; status: proposed.
            Source: TL-06 */
            in item in_X_18 : I_X_18;
            out item out_X_22 : I_X_22;
            out item out_X_23 : I_X_23;
        }
        action def T_F_ACCEPT {
            doc /* Capture terms and identified-tool receipt acceptance
            Record member acceptance; presentation or readiness alone is insufficient.
            Record: F_ACCEPT
            Basis: derived; status: proposed.
            Source: TL-06 */
            in item in_X_22 : I_X_22;
            out item out_X_24 : I_X_24;
            out item out_X_25 : I_X_25;
        }
        action def T_F_TRANSFER {
            doc /* Record custody transfer to member
            Commit library-to-member custody only after matching and acceptance evidence.
            Record: F_TRANSFER
            Basis: derived; status: proposed.
            Source: TL-06 */
            in item in_X_24 : I_X_24;
            out item out_X_26 : I_X_26;
        }
        action def T_F_ONLOAN {
            doc /* Record the tool on loan
            Update on-loan state after the custody transfer record.
            Record: F_ONLOAN
            Basis: derived; status: proposed.
            Source: TL-06
            Source: TL-08 */
            in item in_X_26 : I_X_26;
            out item out_X_27 : I_X_27;
        }
        action def T_F_RECEIVE {
            doc /* Confirm returned-tool receipt
            Steward receives the identified tool and records library custody; a member report alone is insufficient.
            Record: F_RECEIVE
            Basis: derived; status: proposed.
            Source: TL-07 */
            out item out_X_28 : I_X_28;
            out item out_X_29 : I_X_29;
        }
        action def T_F_RETURN_ASSESS {
            doc /* Assess returned-tool condition
            Keep received tool unavailable pending fit/unfit assessment.
            Record: F_RETURN_ASSESS
            Basis: derived; status: proposed.
            Source: TL-07 */
            in item in_X_28 : I_X_28;
            out item out_X_30 : I_X_30;
            out item out_X_31 : I_X_31;
        }
        action def T_F_QUARANTINE {
            doc /* Quarantine an unfit tool
            Retain identity, condition and unavailability.
            Record: F_QUARANTINE
            Basis: derived; status: proposed.
            Source: TL-04
            Source: TL-07 */
            in item in_X_10 : I_X_10;
            in item in_X_31 : I_X_31;
            out item out_X_32 : I_X_32;
            out item out_X_33 : I_X_33;
        }
        action def T_F_REPAIR_REQUEST {
            doc /* Coordinate the repair request
            Coordinator decides whether to request external repair and retains tool/defect context.
            Record: F_REPAIR_REQUEST
            Basis: derived; status: proposed.
            Source: TL-07 */
            in item in_X_32 : I_X_32;
            out item out_X_34 : I_X_34;
            in item in_X_38 : I_X_38;
        }
        action def T_F_REPAIR_REPORT {
            doc /* Receive the repair report
            Retain completed work and remaining defects; the report grants no lending release.
            Record: F_REPAIR_REPORT
            Basis: derived; status: proposed.
            Source: TL-02
            Source: TL-07 */
            in item in_X_34 : I_X_34;
            out item out_X_35 : I_X_35;
        }
        action def T_F_REASSESS {
            doc /* Reassess after repair
            Steward reassesses the identified tool before any quarantine release.
            Record: F_REASSESS
            Basis: derived; status: proposed.
            Source: TL-07 */
            in item in_X_35 : I_X_35;
            out item out_X_36 : I_X_36;
            out item out_X_37 : I_X_37;
        }
        action def T_F_RELEASE {
            doc /* Release a fit tool for availability
            Apply the accountable availability decision; quarantine release requires the steward fit finding and coordinator decision.
            Record: F_RELEASE
            Basis: derived; status: proposed.
            Source: TL-07 */
            in item in_X_30 : I_X_30;
            in item in_X_36 : I_X_36;
            out item out_X_40 : I_X_40;
        }
        action def T_F_DISPOSITION {
            doc /* Decide rework or retirement
            Coordinator retains quarantine for remaining defects and chooses a separate repair attempt or retirement.
            Record: F_DISPOSITION
            Basis: derived; status: proposed.
            Source: TL-07 */
            in item in_X_37 : I_X_37;
            out item out_X_38 : I_X_38;
            out item out_X_39 : I_X_39;
        }
        action def T_F_EXCEPTION {
            doc /* Coordinate an unresolved case
            Keep pending, refusal, contact, handover and condition exceptions with an accountable coordinator.
            Record: F_EXCEPTION
            Basis: derived; status: proposed.
            Source: TL-04
            Source: TL-05
            Source: TL-06
            Source: TL-07 */
            in item in_X_09 : I_X_09;
            in item in_X_16 : I_X_16;
            in item in_X_23 : I_X_23;
            in item in_X_25 : I_X_25;
            out item out_X_43 : I_X_43;
            out item out_X_44 : I_X_44;
        }
        action def T_F_LEDGER {
            doc /* Maintain custody, condition and availability state
            Maintain tool identity, custody, condition, reservation linkage and unresolved exceptions; prevent available offers in excluded states.
            Record: F_LEDGER
            Basis: derived; status: proposed.
            Source: TL-08 */
            in item in_X_13 : I_X_13;
            in item in_X_20 : I_X_20;
            in item in_X_27 : I_X_27;
            in item in_X_29 : I_X_29;
            in item in_X_33 : I_X_33;
            in item in_X_39 : I_X_39;
            in item in_X_40 : I_X_40;
            out item out_X_41 : I_X_41;
            out item out_X_42 : I_X_42;
            in item in_X_44 : I_X_44;
        }
        action def T_F_STATUS {
            doc /* Communicate the current request outcome
            Provide pending, ready, refused, extended or closed outcomes without implying loan or repair success.
            Record: F_STATUS
            Basis: derived; status: proposed.
            Source: TL-07
            Source: TL-08 */
            in item in_X_11 : I_X_11;
            in item in_X_21 : I_X_21;
            in item in_X_42 : I_X_42;
            in item in_X_43 : I_X_43;
        }
        part def T_LC_ROOT {
            doc /* Tool lending service
            Candidate responsibility decomposition.
            Record: LC_ROOT
            Basis: proposed; status: proposed.
            Source: TL-01
            Source: TL-08 */
        }
        part def T_LC_COORD {
            doc /* Reservation coordination
            Own request, candidate and eligibility coordination without taking registry decision authority.
            Record: LC_COORD
            Basis: proposed; status: proposed.
            Source: TL-01
            Source: TL-08 */
            port p_X_05 : P_X_05;
            port p_X_07 : ~P_X_07;
            port p_X_10 : P_X_10;
            port p_X_11 : P_X_11;
            port p_X_12 : P_X_12;
            port p_X_13 : P_X_13;
            port p_X_16 : ~P_X_16;
            port p_X_19 : ~P_X_19;
            port p_X_20 : P_X_20;
            port p_X_21 : P_X_21;
            port p_X_23 : ~P_X_23;
            port p_X_25 : ~P_X_25;
            port p_X_41 : ~P_X_41;
            port p_X_43 : P_X_43;
            port p_X_44 : P_X_44;
            port p_CX_01 : ~P_CX_01;
            port p_CX_02 : P_CX_02;
            port p_CX_03 : ~P_CX_03;
            port p_CX_10 : ~P_CX_10;
        }
        part def T_LC_HANDLING {
            doc /* Condition assessment
            Own steward inspection evidence and matching of its identified tool.
            Record: LC_HANDLING
            Basis: proposed; status: proposed.
            Source: TL-01
            Source: TL-08 */
            port p_X_05 : ~P_X_05;
            port p_X_07 : P_X_07;
            port p_X_28 : ~P_X_28;
            port p_X_30 : P_X_30;
            port p_X_31 : P_X_31;
            port p_X_35 : ~P_X_35;
            port p_X_36 : P_X_36;
            port p_X_37 : P_X_37;
            port p_CX_06 : ~P_CX_06;
        }
        part def T_LC_COMMS {
            doc /* Member communication
            Own notice content, confirmation evidence and current-outcome communication.
            Record: LC_COMMS
            Basis: proposed; status: proposed.
            Source: TL-01
            Source: TL-08 */
            port p_X_11 : ~P_X_11;
            port p_X_12 : ~P_X_12;
            port p_X_15 : P_X_15;
            port p_X_16 : P_X_16;
            port p_X_17 : ~P_X_17;
            port p_X_21 : ~P_X_21;
            port p_X_42 : ~P_X_42;
            port p_X_43 : ~P_X_43;
            port p_CX_04 : P_CX_04;
        }
        part def T_LC_CUSTODY {
            doc /* Custody handover
            Own matching, terms/receipt acceptance and ordered custody transfer.
            Record: LC_CUSTODY
            Basis: proposed; status: proposed.
            Source: TL-01
            Source: TL-08 */
            port p_X_18 : ~P_X_18;
            port p_X_23 : P_X_23;
            port p_X_25 : P_X_25;
            port p_X_26 : P_X_26;
            port p_X_28 : P_X_28;
            port p_X_29 : P_X_29;
            port p_CX_05 : ~P_CX_05;
            port p_CX_07 : ~P_CX_07;
        }
        part def T_LC_RECOVERY {
            doc /* Condition recovery
            Own quarantine, external repair coordination and authorised release or retirement.
            Record: LC_RECOVERY
            Basis: proposed; status: proposed.
            Source: TL-01
            Source: TL-08 */
            port p_X_10 : ~P_X_10;
            port p_X_30 : ~P_X_30;
            port p_X_31 : ~P_X_31;
            port p_X_33 : P_X_33;
            port p_X_35 : P_X_35;
            port p_X_36 : ~P_X_36;
            port p_X_37 : ~P_X_37;
            port p_X_39 : P_X_39;
            port p_X_40 : P_X_40;
            port p_CX_08 : P_CX_08;
            port p_CX_09 : ~P_CX_09;
            port p_CX_11 : ~P_CX_11;
        }
        part def T_LC_RECORDS {
            doc /* Service state and inventory
            Own identified-tool state, custody linkage, hold timing and availability invariant.
            Record: LC_RECORDS
            Basis: proposed; status: proposed.
            Source: TL-01
            Source: TL-08 */
            port p_X_13 : ~P_X_13;
            port p_X_15 : ~P_X_15;
            port p_X_17 : P_X_17;
            port p_X_18 : P_X_18;
            port p_X_19 : P_X_19;
            port p_X_20 : ~P_X_20;
            port p_X_26 : ~P_X_26;
            port p_X_29 : ~P_X_29;
            port p_X_33 : ~P_X_33;
            port p_X_39 : ~P_X_39;
            port p_X_40 : ~P_X_40;
            port p_X_41 : P_X_41;
            port p_X_42 : P_X_42;
            port p_X_44 : ~P_X_44;
            port p_CX_12 : P_CX_12;
        }
        port def P_X_05 {
            out item payload : I_X_05;
        }
        interface def IF_X_05 {
            end sender : P_X_05;
            end receiver : ~P_X_05;
            flow of I_X_05 from sender.payload to receiver.payload;
        }
        port def P_X_07 {
            out item payload : I_X_07;
        }
        interface def IF_X_07 {
            end sender : P_X_07;
            end receiver : ~P_X_07;
            flow of I_X_07 from sender.payload to receiver.payload;
        }
        port def P_X_10 {
            out item payload : I_X_10;
        }
        interface def IF_X_10 {
            end sender : P_X_10;
            end receiver : ~P_X_10;
            flow of I_X_10 from sender.payload to receiver.payload;
        }
        port def P_X_11 {
            out item payload : I_X_11;
        }
        interface def IF_X_11 {
            end sender : P_X_11;
            end receiver : ~P_X_11;
            flow of I_X_11 from sender.payload to receiver.payload;
        }
        port def P_X_12 {
            out item payload : I_X_12;
        }
        interface def IF_X_12 {
            end sender : P_X_12;
            end receiver : ~P_X_12;
            flow of I_X_12 from sender.payload to receiver.payload;
        }
        port def P_X_13 {
            out item payload : I_X_13;
        }
        interface def IF_X_13 {
            end sender : P_X_13;
            end receiver : ~P_X_13;
            flow of I_X_13 from sender.payload to receiver.payload;
        }
        port def P_X_15 {
            out item payload : I_X_15;
        }
        interface def IF_X_15 {
            end sender : P_X_15;
            end receiver : ~P_X_15;
            flow of I_X_15 from sender.payload to receiver.payload;
        }
        port def P_X_16 {
            out item payload : I_X_16;
        }
        interface def IF_X_16 {
            end sender : P_X_16;
            end receiver : ~P_X_16;
            flow of I_X_16 from sender.payload to receiver.payload;
        }
        port def P_X_17 {
            out item payload : I_X_17;
        }
        interface def IF_X_17 {
            end sender : P_X_17;
            end receiver : ~P_X_17;
            flow of I_X_17 from sender.payload to receiver.payload;
        }
        port def P_X_18 {
            out item payload : I_X_18;
        }
        interface def IF_X_18 {
            end sender : P_X_18;
            end receiver : ~P_X_18;
            flow of I_X_18 from sender.payload to receiver.payload;
        }
        port def P_X_19 {
            out item payload : I_X_19;
        }
        interface def IF_X_19 {
            end sender : P_X_19;
            end receiver : ~P_X_19;
            flow of I_X_19 from sender.payload to receiver.payload;
        }
        port def P_X_20 {
            out item payload : I_X_20;
        }
        interface def IF_X_20 {
            end sender : P_X_20;
            end receiver : ~P_X_20;
            flow of I_X_20 from sender.payload to receiver.payload;
        }
        port def P_X_21 {
            out item payload : I_X_21;
        }
        interface def IF_X_21 {
            end sender : P_X_21;
            end receiver : ~P_X_21;
            flow of I_X_21 from sender.payload to receiver.payload;
        }
        port def P_X_23 {
            out item payload : I_X_23;
        }
        interface def IF_X_23 {
            end sender : P_X_23;
            end receiver : ~P_X_23;
            flow of I_X_23 from sender.payload to receiver.payload;
        }
        port def P_X_25 {
            out item payload : I_X_25;
        }
        interface def IF_X_25 {
            end sender : P_X_25;
            end receiver : ~P_X_25;
            flow of I_X_25 from sender.payload to receiver.payload;
        }
        port def P_X_26 {
            out item payload : I_X_26;
        }
        interface def IF_X_26 {
            end sender : P_X_26;
            end receiver : ~P_X_26;
            flow of I_X_26 from sender.payload to receiver.payload;
        }
        port def P_X_28 {
            out item payload : I_X_28;
        }
        interface def IF_X_28 {
            end sender : P_X_28;
            end receiver : ~P_X_28;
            flow of I_X_28 from sender.payload to receiver.payload;
        }
        port def P_X_29 {
            out item payload : I_X_29;
        }
        interface def IF_X_29 {
            end sender : P_X_29;
            end receiver : ~P_X_29;
            flow of I_X_29 from sender.payload to receiver.payload;
        }
        port def P_X_30 {
            out item payload : I_X_30;
        }
        interface def IF_X_30 {
            end sender : P_X_30;
            end receiver : ~P_X_30;
            flow of I_X_30 from sender.payload to receiver.payload;
        }
        port def P_X_31 {
            out item payload : I_X_31;
        }
        interface def IF_X_31 {
            end sender : P_X_31;
            end receiver : ~P_X_31;
            flow of I_X_31 from sender.payload to receiver.payload;
        }
        port def P_X_33 {
            out item payload : I_X_33;
        }
        interface def IF_X_33 {
            end sender : P_X_33;
            end receiver : ~P_X_33;
            flow of I_X_33 from sender.payload to receiver.payload;
        }
        port def P_X_35 {
            out item payload : I_X_35;
        }
        interface def IF_X_35 {
            end sender : P_X_35;
            end receiver : ~P_X_35;
            flow of I_X_35 from sender.payload to receiver.payload;
        }
        port def P_X_36 {
            out item payload : I_X_36;
        }
        interface def IF_X_36 {
            end sender : P_X_36;
            end receiver : ~P_X_36;
            flow of I_X_36 from sender.payload to receiver.payload;
        }
        port def P_X_37 {
            out item payload : I_X_37;
        }
        interface def IF_X_37 {
            end sender : P_X_37;
            end receiver : ~P_X_37;
            flow of I_X_37 from sender.payload to receiver.payload;
        }
        port def P_X_39 {
            out item payload : I_X_39;
        }
        interface def IF_X_39 {
            end sender : P_X_39;
            end receiver : ~P_X_39;
            flow of I_X_39 from sender.payload to receiver.payload;
        }
        port def P_X_40 {
            out item payload : I_X_40;
        }
        interface def IF_X_40 {
            end sender : P_X_40;
            end receiver : ~P_X_40;
            flow of I_X_40 from sender.payload to receiver.payload;
        }
        port def P_X_41 {
            out item payload : I_X_41;
        }
        interface def IF_X_41 {
            end sender : P_X_41;
            end receiver : ~P_X_41;
            flow of I_X_41 from sender.payload to receiver.payload;
        }
        port def P_X_42 {
            out item payload : I_X_42;
        }
        interface def IF_X_42 {
            end sender : P_X_42;
            end receiver : ~P_X_42;
            flow of I_X_42 from sender.payload to receiver.payload;
        }
        port def P_X_43 {
            out item payload : I_X_43;
        }
        interface def IF_X_43 {
            end sender : P_X_43;
            end receiver : ~P_X_43;
            flow of I_X_43 from sender.payload to receiver.payload;
        }
        port def P_X_44 {
            out item payload : I_X_44;
        }
        interface def IF_X_44 {
            end sender : P_X_44;
            end receiver : ~P_X_44;
            flow of I_X_44 from sender.payload to receiver.payload;
        }
        port def P_CX_01 {
            out item payload : I_CX_01;
        }
        interface def IF_CX_01 {
            end sender : P_CX_01;
            end receiver : ~P_CX_01;
            flow of I_CX_01 from sender.payload to receiver.payload;
        }
        port def P_CX_02 {
            out item payload : I_CX_02;
        }
        interface def IF_CX_02 {
            end sender : P_CX_02;
            end receiver : ~P_CX_02;
            flow of I_CX_02 from sender.payload to receiver.payload;
        }
        port def P_CX_03 {
            out item payload : I_CX_03;
        }
        interface def IF_CX_03 {
            end sender : P_CX_03;
            end receiver : ~P_CX_03;
            flow of I_CX_03 from sender.payload to receiver.payload;
        }
        port def P_CX_04 {
            out item payload : I_CX_04;
        }
        interface def IF_CX_04 {
            end sender : P_CX_04;
            end receiver : ~P_CX_04;
            flow of I_CX_04 from sender.payload to receiver.payload;
        }
        port def P_CX_05 {
            out item payload : I_CX_05;
        }
        interface def IF_CX_05 {
            end sender : P_CX_05;
            end receiver : ~P_CX_05;
            flow of I_CX_05 from sender.payload to receiver.payload;
        }
        port def P_CX_06 {
            out item payload : I_CX_06;
        }
        interface def IF_CX_06 {
            end sender : P_CX_06;
            end receiver : ~P_CX_06;
            flow of I_CX_06 from sender.payload to receiver.payload;
        }
        port def P_CX_07 {
            out item payload : I_CX_07;
        }
        interface def IF_CX_07 {
            end sender : P_CX_07;
            end receiver : ~P_CX_07;
            flow of I_CX_07 from sender.payload to receiver.payload;
        }
        port def P_CX_08 {
            out item payload : I_CX_08;
        }
        interface def IF_CX_08 {
            end sender : P_CX_08;
            end receiver : ~P_CX_08;
            flow of I_CX_08 from sender.payload to receiver.payload;
        }
        port def P_CX_09 {
            out item payload : I_CX_09;
        }
        interface def IF_CX_09 {
            end sender : P_CX_09;
            end receiver : ~P_CX_09;
            flow of I_CX_09 from sender.payload to receiver.payload;
        }
        port def P_CX_10 {
            out item payload : I_CX_10;
        }
        interface def IF_CX_10 {
            end sender : P_CX_10;
            end receiver : ~P_CX_10;
            flow of I_CX_10 from sender.payload to receiver.payload;
        }
        port def P_CX_11 {
            out item payload : I_CX_11;
        }
        interface def IF_CX_11 {
            end sender : P_CX_11;
            end receiver : ~P_CX_11;
            flow of I_CX_11 from sender.payload to receiver.payload;
        }
        port def P_CX_12 {
            out item payload : I_CX_12;
        }
        interface def IF_CX_12 {
            end sender : P_CX_12;
            end receiver : ~P_CX_12;
            flow of I_CX_12 from sender.payload to receiver.payload;
        }
        item def Event_SM_TOOL_ST_01 {
            doc /* Ready reservation committed */
        }
        item def Event_SM_TOOL_ST_02 {
            doc /* Notice delivery confirmed */
        }
        item def Event_SM_TOOL_ST_03 {
            doc /* Member withdraws */
        }
        item def Event_SM_TOOL_ST_04 {
            doc /* New fault found */
        }
        item def Event_SM_TOOL_ST_05 {
            doc /* Custody transfer recorded */
        }
        item def Event_SM_TOOL_ST_06 {
            doc /* Expiry or withdrawal disposition recorded */
        }
        item def Event_SM_TOOL_ST_07 {
            doc /* New tool fault found */
        }
        item def Event_SM_TOOL_ST_08 {
            doc /* Steward confirms returned-tool receipt */
        }
        item def Event_SM_TOOL_ST_09 {
            doc /* Fit return assessment recorded */
        }
        item def Event_SM_TOOL_ST_10 {
            doc /* Unfit return assessment recorded */
        }
        item def Event_SM_TOOL_ST_11 {
            doc /* Coordinator releases quarantine */
        }
        item def Event_SM_TOOL_ST_12 {
            doc /* Coordinator retires tool */
        }
        state def T_SM_TOOL {
            doc /* Identified-tool availability lifecycle
            Representative identified-tool record lifecycle; no fleet size or execution is inferred.
            Record: SM_TOOL
            Basis: derived; status: proposed.
            Source: TL-04
            Source: TL-05
            Source: TL-06
            Source: TL-07
            Source: TL-08
            Lifecycle policy: ongoing
            Terminal states: retired
            Lifecycle exit condition: The identified record remains governed until retirement and retention disposition.
            Transition effects below are retained obligations, not executed effects. */
            entry;
            then available;
            state available {
                doc /* Available */
            }
            state pending_notice {
                doc /* Reserved, pending notification */
            }
            state ready {
                doc /* Ready under confirmed hold */
            }
            state on_loan {
                doc /* On loan */
            }
            state awaiting_assessment {
                doc /* Library custody, awaiting assessment */
            }
            state quarantined {
                doc /* Quarantined */
            }
            state retired {
                doc /* Retired */
            }
            attribute g_ST_01 : Boolean {
                doc /* Review predicate, not an evaluated value: Matching eligible member and fit tool evidence present */
            }
            transition ST_01 first available accept Event_SM_TOOL_ST_01 if g_ST_01 then pending_notice {
                doc /* Effect/obligation: Exclude from available offers */
            }
            attribute g_ST_02 : Boolean {
                doc /* Review predicate, not an evaluated value: Effective deadline is at least two hours from actual confirmed delivery */
            }
            transition ST_02 first pending_notice accept Event_SM_TOOL_ST_02 if g_ST_02 then ready {
                doc /* Effect/obligation: Retain confirmed hold basis */
            }
            attribute g_ST_03 : Boolean {
                doc /* Review predicate, not an evaluated value: Coordinator records withdrawal and tool remains fit */
            }
            transition ST_03 first pending_notice accept Event_SM_TOOL_ST_03 if g_ST_03 then available {
                doc /* Effect/obligation: Close reservation */
            }
            attribute g_ST_04 : Boolean {
                doc /* Review predicate, not an evaluated value: Condition concern applies to identified tool */
            }
            transition ST_04 first pending_notice accept Event_SM_TOOL_ST_04 if g_ST_04 then quarantined {
                doc /* Effect/obligation: Retain unavailable condition */
            }
            attribute g_ST_05 : Boolean {
                doc /* Review predicate, not an evaluated value: Member/tool match and terms/identified-tool receipt accepted */
            }
            transition ST_05 first ready accept Event_SM_TOOL_ST_05 if g_ST_05 then on_loan {
                doc /* Effect/obligation: Record on-loan after custody transfer */
            }
            attribute g_ST_06 : Boolean {
                doc /* Review predicate, not an evaluated value: Coordinator permits release, tool still fit and no extension */
            }
            transition ST_06 first ready accept Event_SM_TOOL_ST_06 if g_ST_06 then available {
                doc /* Effect/obligation: Clear reservation and offer availability */
            }
            attribute g_ST_07 : Boolean {
                doc /* Review predicate, not an evaluated value: Fault overrides continued readiness */
            }
            transition ST_07 first ready accept Event_SM_TOOL_ST_07 if g_ST_07 then quarantined {
                doc /* Effect/obligation: Retain quarantine */
            }
            attribute g_ST_08 : Boolean {
                doc /* Review predicate, not an evaluated value: Identified physical receipt and library custody recorded */
            }
            transition ST_08 first on_loan accept Event_SM_TOOL_ST_08 if g_ST_08 then awaiting_assessment {
                doc /* Effect/obligation: Keep unavailable for assessment */
            }
            attribute g_ST_09 : Boolean {
                doc /* Review predicate, not an evaluated value: Identified tool assessed fit */
            }
            transition ST_09 first awaiting_assessment accept Event_SM_TOOL_ST_09 if g_ST_09 then available {
                doc /* Effect/obligation: Permit available status */
            }
            attribute g_ST_10 : Boolean {
                doc /* Review predicate, not an evaluated value: Identified tool assessed unfit */
            }
            transition ST_10 first awaiting_assessment accept Event_SM_TOOL_ST_10 if g_ST_10 then quarantined {
                doc /* Effect/obligation: Retain quarantine */
            }
            attribute g_ST_11 : Boolean {
                doc /* Review predicate, not an evaluated value: Steward fit reassessment exists; repair report alone is insufficient */
            }
            transition ST_11 first quarantined accept Event_SM_TOOL_ST_11 if g_ST_11 then available {
                doc /* Effect/obligation: Permit availability */
            }
            attribute g_ST_12 : Boolean {
                doc /* Review predicate, not an evaluated value: Retirement separately decided and recorded */
            }
            transition ST_12 first quarantined accept Event_SM_TOOL_ST_12 if g_ST_12 then retired {
                doc /* Effect/obligation: Keep out of available inventory */
            }
            transition finish_retired first retired then done;
        }
    }
    package Operational {
        action activities {
            action OA_REQUEST : Types::T_OA_REQUEST {
                doc /* Request and accept a tool loan
                Express the need, select wait-list/closure and accept a specific loan.
                Record: OA_REQUEST
                Basis: derived; status: proposed.
                Source: TL-03
                Source: TL-06 */
            }
            action OA_COORD : Types::T_OA_COORD {
                doc /* Coordinate reservations and exceptions
                Select a candidate, keep unresolved cases accountable and govern reservation disposition.
                Record: OA_COORD
                Basis: derived; status: proposed.
                Source: TL-03
                Source: TL-05 */
            }
            action OA_ELIG : Types::T_OA_ELIG {
                doc /* Decide membership eligibility
                Return identified eligible, ineligible or unavailable decision.
                Record: OA_ELIG
                Basis: derived; status: proposed.
                Source: TL-02
                Source: TL-04 */
            }
            action OA_CONDITION : Types::T_OA_CONDITION {
                doc /* Assess identified-tool condition
                Inspect candidate, return or repaired tool and retain fit/unfit evidence.
                Record: OA_CONDITION
                Basis: derived; status: proposed.
                Source: TL-04
                Source: TL-07 */
            }
            action OA_CUSTODY : Types::T_OA_CUSTODY {
                doc /* Confirm tool handover and return
                Confirm matched collection, terms/receipt and physical returned-tool receipt.
                Record: OA_CUSTODY
                Basis: derived; status: proposed.
                Source: TL-06
                Source: TL-07 */
            }
            action OA_REPAIR : Types::T_OA_REPAIR {
                doc /* Report repair outcome
                Supply completed work and known remaining defects for reassessment.
                Record: OA_REPAIR
                Basis: derived; status: proposed.
                Source: TL-02
                Source: TL-07 */
            }
            action OA_INFO : Types::T_OA_INFO {
                doc /* Maintain accountable service information
                Make current request, inventory, custody and exception information available.
                Record: OA_INFO
                Basis: derived; status: proposed.
                Source: TL-08 */
            }
        }
        part context {
            ref part A_MEMBER : Types::T_A_MEMBER {
                doc /* Member
                Requests and collects a tool; accepts loan terms and receipt.
                Record: A_MEMBER
                Basis: source-explicit; status: draft.
                Source: TL-02
                Source: TL-06 */
                perform activities.OA_REQUEST;
            }
            ref part A_STEWARD : Types::T_A_STEWARD {
                doc /* Volunteer steward
                Handles tools, confirms receipt and assesses condition.
                Record: A_STEWARD
                Basis: source-explicit; status: draft.
                Source: TL-02
                Source: TL-07 */
                perform activities.OA_CONDITION;
                perform activities.OA_CUSTODY;
            }
            ref part A_COORD : Types::T_A_COORD {
                doc /* Duty coordinator
                Owns exceptions, extensions, repair requests and quarantine release decisions.
                Record: A_COORD
                Basis: source-explicit; status: draft.
                Source: TL-02
                Source: TL-05
                Source: TL-07 */
                perform activities.OA_COORD;
                perform activities.OA_INFO;
            }
            ref part A_REGISTRY : Types::T_A_REGISTRY {
                doc /* External membership registry
                Sole authority for the membership eligibility decision.
                Record: A_REGISTRY
                Basis: source-explicit; status: draft.
                Source: TL-01
                Source: TL-02
                Source: TL-04 */
                perform activities.OA_ELIG;
            }
            ref part A_REPAIR : Types::T_A_REPAIR {
                doc /* External repair provider
                Reports completed work and remaining defects; cannot release tools for lending.
                Record: A_REPAIR
                Basis: source-explicit; status: draft.
                Source: TL-02
                Source: TL-07 */
                perform activities.OA_REPAIR;
            }
        }
    }
    package System {
        action functions {
            action F_ROOT : Types::T_F_ROOT {
                doc /* Deliver a tool lending service
                Group functions by outcome, inputs and handover responsibility.
                Record: F_ROOT
                Basis: derived; status: proposed.
                Source: TL-01 */
                action F_ACQUIRE : Types::T_F_ACQUIRE {
                    doc /* Prepare an eligible and fit reservation
                    Group functions by outcome, inputs and handover responsibility.
                    Record: F_ACQUIRE
                    Basis: derived; status: proposed.
                    Source: TL-01 */
                    action F_REQUEST : Types::T_F_REQUEST {
                        doc /* Capture the request
                        Retain member, category and desired collection period.
                        Record: F_REQUEST
                        Basis: derived; status: proposed.
                        Source: TL-03 */
                    }
                    action F_SELECT : Types::T_F_SELECT {
                        doc /* Select an available identified candidate
                        Use the current inventory state; do not reserve inventory for a wait-list.
                        Record: F_SELECT
                        Basis: derived; status: proposed.
                        Source: TL-03
                        Source: TL-08 */
                    }
                    action F_NO_CAND : Types::T_F_NO_CAND {
                        doc /* Dispose of an unfilled request
                        Offer wait-list or closure at the member choice without a tool reservation.
                        Record: F_NO_CAND
                        Basis: derived; status: proposed.
                        Source: TL-03 */
                    }
                    action F_PREP : Types::T_F_PREP {
                        doc /* Establish the preparation case
                        Retain the selected member/tool identifiers before the two independent preparation contributions.
                        Record: F_PREP
                        Basis: derived; status: proposed.
                        Source: TL-04 */
                    }
                    action F_ELIG : Types::T_F_ELIG {
                        doc /* Obtain the registry decision
                        Request and retain the external decision and identifiers; do not manufacture a positive decision.
                        Record: F_ELIG
                        Basis: derived; status: proposed.
                        Source: TL-02
                        Source: TL-04 */
                    }
                    action F_INSPECT : Types::T_F_INSPECT {
                        doc /* Inspect the candidate tool
                        Retain the steward fit/unfit finding for the selected identified tool.
                        Record: F_INSPECT
                        Basis: derived; status: proposed.
                        Source: TL-04 */
                    }
                    action F_ASSESS : Types::T_F_ASSESS {
                        doc /* Assess preparation contributions
                        Match member/tool evidence and distinguish eligible-and-fit, unavailable, ineligible and unfit cases.
                        Record: F_ASSESS
                        Basis: derived; status: proposed.
                        Source: TL-04 */
                    }
                    action F_RESERVE : Types::T_F_RESERVE {
                        doc /* Prepare the ready reservation
                        Commit the eligible member/fit identified tool reservation; exclude that tool from available offers.
                        Record: F_RESERVE
                        Basis: derived; status: proposed.
                        Source: TL-04
                        Source: TL-08 */
                    }
                }
                action F_LOAN : Types::T_F_LOAN {
                    doc /* Notify and transfer the reserved tool
                    Group functions by outcome, inputs and handover responsibility.
                    Record: F_LOAN
                    Basis: derived; status: proposed.
                    Source: TL-01 */
                    action F_NOTICE : Types::T_F_NOTICE {
                        doc /* Deliver the ready notice
                        Provide tool, location and hold deadline; retain delivery outcome separately from queueing. Deadline/acknowledgement coordination needs agreement.
                        Record: F_NOTICE
                        Basis: derived; status: proposed.
                        Source: TL-05 */
                    }
                    action F_CONFIRM : Types::T_F_CONFIRM {
                        doc /* Record confirmed notice delivery
                        Retain actual confirmed delivery time; missing confirmation remains pending-notification.
                        Record: F_CONFIRM
                        Basis: derived; status: proposed.
                        Source: TL-05 */
                    }
                    action F_HOLD : Types::T_F_HOLD {
                        doc /* Govern the confirmed hold interval
                        Bind the minimum hold to confirmed delivery time; withdrawal/new fault exceptions remain separate.
                        Record: F_HOLD
                        Basis: derived; status: proposed.
                        Source: TL-05 */
                    }
                    action F_EXPIRY : Types::T_F_EXPIRY {
                        doc /* Resolve expiry, withdrawal or extension
                        Coordinator returns a still-fit tool after expiry or records the extension reason; withdrawal is a separate release cause.
                        Record: F_EXPIRY
                        Basis: derived; status: proposed.
                        Source: TL-05 */
                    }
                    action F_MATCH : Types::T_F_MATCH {
                        doc /* Match the collection case
                        Steward checks member and allocated tool against the reservation.
                        Record: F_MATCH
                        Basis: derived; status: proposed.
                        Source: TL-06 */
                    }
                    action F_ACCEPT : Types::T_F_ACCEPT {
                        doc /* Capture terms and identified-tool receipt acceptance
                        Record member acceptance; presentation or readiness alone is insufficient.
                        Record: F_ACCEPT
                        Basis: derived; status: proposed.
                        Source: TL-06 */
                    }
                    action F_TRANSFER : Types::T_F_TRANSFER {
                        doc /* Record custody transfer to member
                        Commit library-to-member custody only after matching and acceptance evidence.
                        Record: F_TRANSFER
                        Basis: derived; status: proposed.
                        Source: TL-06 */
                    }
                    action F_ONLOAN : Types::T_F_ONLOAN {
                        doc /* Record the tool on loan
                        Update on-loan state after the custody transfer record.
                        Record: F_ONLOAN
                        Basis: derived; status: proposed.
                        Source: TL-06
                        Source: TL-08 */
                    }
                }
                action F_RETURN : Types::T_F_RETURN {
                    doc /* Recover the returned tool
                    Group functions by outcome, inputs and handover responsibility.
                    Record: F_RETURN
                    Basis: derived; status: proposed.
                    Source: TL-01 */
                    action F_RECEIVE : Types::T_F_RECEIVE {
                        doc /* Confirm returned-tool receipt
                        Steward receives the identified tool and records library custody; a member report alone is insufficient.
                        Record: F_RECEIVE
                        Basis: derived; status: proposed.
                        Source: TL-07 */
                    }
                    action F_RETURN_ASSESS : Types::T_F_RETURN_ASSESS {
                        doc /* Assess returned-tool condition
                        Keep received tool unavailable pending fit/unfit assessment.
                        Record: F_RETURN_ASSESS
                        Basis: derived; status: proposed.
                        Source: TL-07 */
                    }
                    action F_QUARANTINE : Types::T_F_QUARANTINE {
                        doc /* Quarantine an unfit tool
                        Retain identity, condition and unavailability.
                        Record: F_QUARANTINE
                        Basis: derived; status: proposed.
                        Source: TL-04
                        Source: TL-07 */
                    }
                    action F_REPAIR_REQUEST : Types::T_F_REPAIR_REQUEST {
                        doc /* Coordinate the repair request
                        Coordinator decides whether to request external repair and retains tool/defect context.
                        Record: F_REPAIR_REQUEST
                        Basis: derived; status: proposed.
                        Source: TL-07 */
                    }
                    action F_REPAIR_REPORT : Types::T_F_REPAIR_REPORT {
                        doc /* Receive the repair report
                        Retain completed work and remaining defects; the report grants no lending release.
                        Record: F_REPAIR_REPORT
                        Basis: derived; status: proposed.
                        Source: TL-02
                        Source: TL-07 */
                    }
                    action F_REASSESS : Types::T_F_REASSESS {
                        doc /* Reassess after repair
                        Steward reassesses the identified tool before any quarantine release.
                        Record: F_REASSESS
                        Basis: derived; status: proposed.
                        Source: TL-07 */
                    }
                    action F_RELEASE : Types::T_F_RELEASE {
                        doc /* Release a fit tool for availability
                        Apply the accountable availability decision; quarantine release requires the steward fit finding and coordinator decision.
                        Record: F_RELEASE
                        Basis: derived; status: proposed.
                        Source: TL-07 */
                    }
                    action F_DISPOSITION : Types::T_F_DISPOSITION {
                        doc /* Decide rework or retirement
                        Coordinator retains quarantine for remaining defects and chooses a separate repair attempt or retirement.
                        Record: F_DISPOSITION
                        Basis: derived; status: proposed.
                        Source: TL-07 */
                    }
                }
                action F_SUPPORT : Types::T_F_SUPPORT {
                    doc /* Keep service decisions and state accountable
                    Group functions by outcome, inputs and handover responsibility.
                    Record: F_SUPPORT
                    Basis: derived; status: proposed.
                    Source: TL-01 */
                    action F_EXCEPTION : Types::T_F_EXCEPTION {
                        doc /* Coordinate an unresolved case
                        Keep pending, refusal, contact, handover and condition exceptions with an accountable coordinator.
                        Record: F_EXCEPTION
                        Basis: derived; status: proposed.
                        Source: TL-04
                        Source: TL-05
                        Source: TL-06
                        Source: TL-07 */
                    }
                    action F_LEDGER : Types::T_F_LEDGER {
                        doc /* Maintain custody, condition and availability state
                        Maintain tool identity, custody, condition, reservation linkage and unresolved exceptions; prevent available offers in excluded states.
                        Record: F_LEDGER
                        Basis: derived; status: proposed.
                        Source: TL-08 */
                    }
                    action F_STATUS : Types::T_F_STATUS {
                        doc /* Communicate the current request outcome
                        Provide pending, ready, refused, extended or closed outcomes without implying loan or repair success.
                        Record: F_STATUS
                        Basis: derived; status: proposed.
                        Source: TL-07
                        Source: TL-08 */
                    }
                }
            }
        }
        flow X_01 of Types::I_X_01 from functions.F_ROOT.F_ACQUIRE.F_REQUEST.out_X_01 to functions.F_ROOT.F_ACQUIRE.F_SELECT.in_X_01 {
            doc /* Member, category and collection window
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_01
            Basis: derived; status: proposed.
            Source: TL-03
            Applicability: Request received */
        }
        flow X_02 of Types::I_X_02 from functions.F_ROOT.F_ACQUIRE.F_SELECT.out_X_02 to functions.F_ROOT.F_ACQUIRE.F_NO_CAND.in_X_02 {
            doc /* Unfilled request
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_02
            Basis: derived; status: proposed.
            Source: TL-03
            Applicability: No available candidate */
        }
        flow X_03 of Types::I_X_03 from functions.F_ROOT.F_ACQUIRE.F_SELECT.out_X_03 to functions.F_ROOT.F_ACQUIRE.F_PREP.in_X_03 {
            doc /* Selected tool and member identifiers
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_03
            Basis: derived; status: proposed.
            Source: TL-04
            Applicability: Candidate is available */
        }
        flow X_04 of Types::I_X_04 from functions.F_ROOT.F_ACQUIRE.F_PREP.out_X_04 to functions.F_ROOT.F_ACQUIRE.F_ELIG.in_X_04 {
            doc /* Identified membership decision request
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_04
            Basis: derived; status: proposed.
            Source: TL-04
            Applicability: Preparation case selected */
        }
        flow X_05 of Types::I_X_05 from functions.F_ROOT.F_ACQUIRE.F_PREP.out_X_05 to functions.F_ROOT.F_ACQUIRE.F_INSPECT.in_X_05 {
            doc /* Identified candidate inspection request
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_05
            Basis: derived; status: proposed.
            Source: TL-04
            Applicability: Preparation case selected */
        }
        flow X_06 of Types::I_X_06 from functions.F_ROOT.F_ACQUIRE.F_ELIG.out_X_06 to functions.F_ROOT.F_ACQUIRE.F_ASSESS.in_X_06 {
            doc /* Member-linked eligible/ineligible/unavailable decision
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_06
            Basis: derived; status: proposed.
            Source: TL-04
            Applicability: Registry contribution received */
        }
        flow X_07 of Types::I_X_07 from functions.F_ROOT.F_ACQUIRE.F_INSPECT.out_X_07 to functions.F_ROOT.F_ACQUIRE.F_ASSESS.in_X_07 {
            doc /* Tool-linked fit/unfit inspection
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_07
            Basis: derived; status: proposed.
            Source: TL-04
            Applicability: Steward contribution received */
        }
        flow X_08 of Types::I_X_08 from functions.F_ROOT.F_ACQUIRE.F_ASSESS.out_X_08 to functions.F_ROOT.F_ACQUIRE.F_RESERVE.in_X_08 {
            doc /* Matched eligible member and fit tool evidence
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_08
            Basis: derived; status: proposed.
            Source: TL-04
            Applicability: Both admission contributions permit readiness */
        }
        flow X_09 of Types::I_X_09 from functions.F_ROOT.F_ACQUIRE.F_ASSESS.out_X_09 to functions.F_ROOT.F_SUPPORT.F_EXCEPTION.in_X_09 {
            doc /* Unavailable or ineligible membership case
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_09
            Basis: derived; status: proposed.
            Source: TL-04
            Applicability: Admission unresolved or denied */
        }
        flow X_10 of Types::I_X_10 from functions.F_ROOT.F_ACQUIRE.F_ASSESS.out_X_10 to functions.F_ROOT.F_RETURN.F_QUARANTINE.in_X_10 {
            doc /* Unfit candidate identity and inspection
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_10
            Basis: derived; status: proposed.
            Source: TL-04
            Applicability: Candidate unfit */
        }
        flow X_11 of Types::I_X_11 from functions.F_ROOT.F_ACQUIRE.F_NO_CAND.out_X_11 to functions.F_ROOT.F_SUPPORT.F_STATUS.in_X_11 {
            doc /* Member-selected wait-list or closure
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_11
            Basis: derived; status: proposed.
            Source: TL-03
            Applicability: No reservation created */
        }
        flow X_12 of Types::I_X_12 from functions.F_ROOT.F_ACQUIRE.F_RESERVE.out_X_12 to functions.F_ROOT.F_LOAN.F_NOTICE.in_X_12 {
            doc /* Ready tool, location and deadline information
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_12
            Basis: derived; status: proposed.
            Source: TL-05
            Applicability: Ready reservation prepared */
        }
        flow X_13 of Types::I_X_13 from functions.F_ROOT.F_ACQUIRE.F_RESERVE.out_X_13 to functions.F_ROOT.F_SUPPORT.F_LEDGER.in_X_13 {
            doc /* Identified tool reservation linkage
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_13
            Basis: derived; status: proposed.
            Source: TL-08
            Applicability: Ready reservation committed */
        }
        flow X_14 of Types::I_X_14 from functions.F_ROOT.F_LOAN.F_NOTICE.out_X_14 to functions.F_ROOT.F_LOAN.F_CONFIRM.in_X_14 {
            doc /* Notice delivery outcome
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_14
            Basis: derived; status: proposed.
            Source: TL-05
            Applicability: Delivery evidence supplied or missing */
        }
        flow X_15 of Types::I_X_15 from functions.F_ROOT.F_LOAN.F_CONFIRM.out_X_15 to functions.F_ROOT.F_LOAN.F_HOLD.in_X_15 {
            doc /* Confirmed delivery time and reservation identity
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_15
            Basis: derived; status: proposed.
            Source: TL-05
            Applicability: Actual delivery confirmed */
        }
        flow X_16 of Types::I_X_16 from functions.F_ROOT.F_LOAN.F_CONFIRM.out_X_16 to functions.F_ROOT.F_SUPPORT.F_EXCEPTION.in_X_16 {
            doc /* Missing delivery confirmation
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_16
            Basis: derived; status: proposed.
            Source: TL-05
            Applicability: No confirmation evidence */
        }
        flow X_17 of Types::I_X_17 from functions.F_ROOT.F_LOAN.F_HOLD.out_X_17 to functions.F_ROOT.F_LOAN.F_NOTICE.in_X_17 {
            doc /* Effective hold deadline or extension information
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_17
            Basis: derived; status: proposed.
            Source: TL-05
            Applicability: Deadline communication needs reconciliation */
        }
        flow X_18 of Types::I_X_18 from functions.F_ROOT.F_LOAN.F_HOLD.out_X_18 to functions.F_ROOT.F_LOAN.F_MATCH.in_X_18 {
            doc /* Current ready reservation
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_18
            Basis: derived; status: proposed.
            Source: TL-06
            Applicability: Member presents for collection */
        }
        flow X_19 of Types::I_X_19 from functions.F_ROOT.F_LOAN.F_HOLD.out_X_19 to functions.F_ROOT.F_LOAN.F_EXPIRY.in_X_19 {
            doc /* Deadline and collection/withdrawal state
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_19
            Basis: derived; status: proposed.
            Source: TL-05
            Applicability: Deadline passed or withdrawal received */
        }
        flow X_20 of Types::I_X_20 from functions.F_ROOT.F_LOAN.F_EXPIRY.out_X_20 to functions.F_ROOT.F_SUPPORT.F_LEDGER.in_X_20 {
            doc /* Still-fit release or reasoned extension disposition
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_20
            Basis: derived; status: proposed.
            Source: TL-05
            Applicability: Coordinator decides */
        }
        flow X_21 of Types::I_X_21 from functions.F_ROOT.F_LOAN.F_EXPIRY.out_X_21 to functions.F_ROOT.F_SUPPORT.F_STATUS.in_X_21 {
            doc /* Extended or closed request outcome
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_21
            Basis: derived; status: proposed.
            Source: TL-08
            Applicability: Disposition recorded */
        }
        flow X_22 of Types::I_X_22 from functions.F_ROOT.F_LOAN.F_MATCH.out_X_22 to functions.F_ROOT.F_LOAN.F_ACCEPT.in_X_22 {
            doc /* Matched member and identified tool
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_22
            Basis: derived; status: proposed.
            Source: TL-06
            Applicability: Identity and reservation match */
        }
        flow X_23 of Types::I_X_23 from functions.F_ROOT.F_LOAN.F_MATCH.out_X_23 to functions.F_ROOT.F_SUPPORT.F_EXCEPTION.in_X_23 {
            doc /* Unresolved identity or tool mismatch
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_23
            Basis: derived; status: proposed.
            Source: TL-06
            Applicability: Matching incomplete */
        }
        flow X_24 of Types::I_X_24 from functions.F_ROOT.F_LOAN.F_ACCEPT.out_X_24 to functions.F_ROOT.F_LOAN.F_TRANSFER.in_X_24 {
            doc /* Accepted terms and identified-tool receipt
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_24
            Basis: derived; status: proposed.
            Source: TL-06
            Applicability: Both acceptance obligations recorded */
        }
        flow X_25 of Types::I_X_25 from functions.F_ROOT.F_LOAN.F_ACCEPT.out_X_25 to functions.F_ROOT.F_SUPPORT.F_EXCEPTION.in_X_25 {
            doc /* Unresolved acceptance
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_25
            Basis: derived; status: proposed.
            Source: TL-06
            Applicability: Acceptance incomplete */
        }
        flow X_26 of Types::I_X_26 from functions.F_ROOT.F_LOAN.F_TRANSFER.out_X_26 to functions.F_ROOT.F_LOAN.F_ONLOAN.in_X_26 {
            doc /* Recorded library-to-member custody transfer
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_26
            Basis: derived; status: proposed.
            Source: TL-06
            Applicability: Custody record exists */
        }
        flow X_27 of Types::I_X_27 from functions.F_ROOT.F_LOAN.F_ONLOAN.out_X_27 to functions.F_ROOT.F_SUPPORT.F_LEDGER.in_X_27 {
            doc /* On-loan state and custody link
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_27
            Basis: derived; status: proposed.
            Source: TL-06
            Applicability: After transfer record */
        }
        flow X_28 of Types::I_X_28 from functions.F_ROOT.F_RETURN.F_RECEIVE.out_X_28 to functions.F_ROOT.F_RETURN.F_RETURN_ASSESS.in_X_28 {
            doc /* Confirmed physical receipt and library custody
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_28
            Basis: derived; status: proposed.
            Source: TL-07
            Applicability: Identified tool received */
        }
        flow X_29 of Types::I_X_29 from functions.F_ROOT.F_RETURN.F_RECEIVE.out_X_29 to functions.F_ROOT.F_SUPPORT.F_LEDGER.in_X_29 {
            doc /* Awaiting-assessment state and custody
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_29
            Basis: derived; status: proposed.
            Source: TL-07
            Applicability: Receipt confirmed */
        }
        flow X_30 of Types::I_X_30 from functions.F_ROOT.F_RETURN.F_RETURN_ASSESS.out_X_30 to functions.F_ROOT.F_RETURN.F_RELEASE.in_X_30 {
            doc /* Fit return inspection
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_30
            Basis: derived; status: proposed.
            Source: TL-07
            Applicability: Tool assessed fit */
        }
        flow X_31 of Types::I_X_31 from functions.F_ROOT.F_RETURN.F_RETURN_ASSESS.out_X_31 to functions.F_ROOT.F_RETURN.F_QUARANTINE.in_X_31 {
            doc /* Unfit return inspection
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_31
            Basis: derived; status: proposed.
            Source: TL-07
            Applicability: Tool assessed unfit */
        }
        flow X_32 of Types::I_X_32 from functions.F_ROOT.F_RETURN.F_QUARANTINE.out_X_32 to functions.F_ROOT.F_RETURN.F_REPAIR_REQUEST.in_X_32 {
            doc /* Quarantined tool and defect context
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_32
            Basis: derived; status: proposed.
            Source: TL-07
            Applicability: Coordinator considers repair */
        }
        flow X_33 of Types::I_X_33 from functions.F_ROOT.F_RETURN.F_QUARANTINE.out_X_33 to functions.F_ROOT.F_SUPPORT.F_LEDGER.in_X_33 {
            doc /* Quarantine state
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_33
            Basis: derived; status: proposed.
            Source: TL-08
            Applicability: Unfit condition retained */
        }
        flow X_34 of Types::I_X_34 from functions.F_ROOT.F_RETURN.F_REPAIR_REQUEST.out_X_34 to functions.F_ROOT.F_RETURN.F_REPAIR_REPORT.in_X_34 {
            doc /* Repair case and identified tool
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_34
            Basis: derived; status: proposed.
            Source: TL-07
            Applicability: External repair requested */
        }
        flow X_35 of Types::I_X_35 from functions.F_ROOT.F_RETURN.F_REPAIR_REPORT.out_X_35 to functions.F_ROOT.F_RETURN.F_REASSESS.in_X_35 {
            doc /* Completed work and remaining defects
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_35
            Basis: derived; status: proposed.
            Source: TL-07
            Applicability: Provider report received */
        }
        flow X_36 of Types::I_X_36 from functions.F_ROOT.F_RETURN.F_REASSESS.out_X_36 to functions.F_ROOT.F_RETURN.F_RELEASE.in_X_36 {
            doc /* Steward fit reassessment
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_36
            Basis: derived; status: proposed.
            Source: TL-07
            Applicability: Tool reassessed fit */
        }
        flow X_37 of Types::I_X_37 from functions.F_ROOT.F_RETURN.F_REASSESS.out_X_37 to functions.F_ROOT.F_RETURN.F_DISPOSITION.in_X_37 {
            doc /* Remaining defects/unfit reassessment
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_37
            Basis: derived; status: proposed.
            Source: TL-07
            Applicability: Quarantine retained */
        }
        flow X_38 of Types::I_X_38 from functions.F_ROOT.F_RETURN.F_DISPOSITION.out_X_38 to functions.F_ROOT.F_RETURN.F_REPAIR_REQUEST.in_X_38 {
            doc /* New repair decision
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_38
            Basis: derived; status: proposed.
            Source: TL-07
            Applicability: Coordinator requests another attempt */
        }
        flow X_39 of Types::I_X_39 from functions.F_ROOT.F_RETURN.F_DISPOSITION.out_X_39 to functions.F_ROOT.F_SUPPORT.F_LEDGER.in_X_39 {
            doc /* Retirement or retained-quarantine disposition
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_39
            Basis: derived; status: proposed.
            Source: TL-07
            Applicability: Coordinator decides */
        }
        flow X_40 of Types::I_X_40 from functions.F_ROOT.F_RETURN.F_RELEASE.out_X_40 to functions.F_ROOT.F_SUPPORT.F_LEDGER.in_X_40 {
            doc /* Authorised available status
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_40
            Basis: derived; status: proposed.
            Source: TL-07
            Applicability: Required condition/release evidence present */
        }
        flow X_41 of Types::I_X_41 from functions.F_ROOT.F_SUPPORT.F_LEDGER.out_X_41 to functions.F_ROOT.F_ACQUIRE.F_SELECT.in_X_41 {
            doc /* Available inventory identities
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_41
            Basis: derived; status: proposed.
            Source: TL-08
            Applicability: Tool not reserved/on-loan/awaiting assessment/quarantined */
        }
        flow X_42 of Types::I_X_42 from functions.F_ROOT.F_SUPPORT.F_LEDGER.out_X_42 to functions.F_ROOT.F_SUPPORT.F_STATUS.in_X_42 {
            doc /* Current inventory, reservation and exception state
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_42
            Basis: derived; status: proposed.
            Source: TL-08
            Applicability: Current outcome needed */
        }
        flow X_43 of Types::I_X_43 from functions.F_ROOT.F_SUPPORT.F_EXCEPTION.out_X_43 to functions.F_ROOT.F_SUPPORT.F_STATUS.in_X_43 {
            doc /* Accountable pending/refused/closed outcome
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_43
            Basis: derived; status: proposed.
            Source: TL-08
            Applicability: Exception disposition known */
        }
        flow X_44 of Types::I_X_44 from functions.F_ROOT.F_SUPPORT.F_EXCEPTION.out_X_44 to functions.F_ROOT.F_SUPPORT.F_LEDGER.in_X_44 {
            doc /* Unresolved exception and retained state
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_44
            Basis: derived; status: proposed.
            Source: TL-08
            Applicability: Exception persists */
        }
    }
    package Logical {
        part architecture {
            part LC_ROOT : Types::T_LC_ROOT {
                doc /* Tool lending service
                Candidate responsibility decomposition.
                Record: LC_ROOT
                Basis: proposed; status: proposed.
                Source: TL-01
                Source: TL-08 */
                part LC_COORD : Types::T_LC_COORD {
                    doc /* Reservation coordination
                    Own request, candidate and eligibility coordination without taking registry decision authority.
                    Record: LC_COORD
                    Basis: proposed; status: proposed.
                    Source: TL-01
                    Source: TL-08 */
                }
                part LC_HANDLING : Types::T_LC_HANDLING {
                    doc /* Condition assessment
                    Own steward inspection evidence and matching of its identified tool.
                    Record: LC_HANDLING
                    Basis: proposed; status: proposed.
                    Source: TL-01
                    Source: TL-08 */
                }
                part LC_COMMS : Types::T_LC_COMMS {
                    doc /* Member communication
                    Own notice content, confirmation evidence and current-outcome communication.
                    Record: LC_COMMS
                    Basis: proposed; status: proposed.
                    Source: TL-01
                    Source: TL-08 */
                }
                part LC_CUSTODY : Types::T_LC_CUSTODY {
                    doc /* Custody handover
                    Own matching, terms/receipt acceptance and ordered custody transfer.
                    Record: LC_CUSTODY
                    Basis: proposed; status: proposed.
                    Source: TL-01
                    Source: TL-08 */
                }
                part LC_RECOVERY : Types::T_LC_RECOVERY {
                    doc /* Condition recovery
                    Own quarantine, external repair coordination and authorised release or retirement.
                    Record: LC_RECOVERY
                    Basis: proposed; status: proposed.
                    Source: TL-01
                    Source: TL-08 */
                }
                part LC_RECORDS : Types::T_LC_RECORDS {
                    doc /* Service state and inventory
                    Own identified-tool state, custody linkage, hold timing and availability invariant.
                    Record: LC_RECORDS
                    Basis: proposed; status: proposed.
                    Source: TL-01
                    Source: TL-08 */
                    exhibit state SM_TOOL : Types::T_SM_TOOL;
                }
            }
        }
        interface IF_X_05 : Types::IF_X_05 connect architecture.LC_ROOT.LC_COORD.p_X_05 to architecture.LC_ROOT.LC_HANDLING.p_X_05 {
            doc /* Identified candidate inspection request
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_05
            Basis: derived; status: proposed.
            Source: TL-04
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_07 : Types::IF_X_07 connect architecture.LC_ROOT.LC_HANDLING.p_X_07 to architecture.LC_ROOT.LC_COORD.p_X_07 {
            doc /* Tool-linked fit/unfit inspection
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_07
            Basis: derived; status: proposed.
            Source: TL-04
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_10 : Types::IF_X_10 connect architecture.LC_ROOT.LC_COORD.p_X_10 to architecture.LC_ROOT.LC_RECOVERY.p_X_10 {
            doc /* Unfit candidate identity and inspection
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_10
            Basis: derived; status: proposed.
            Source: TL-04
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_11 : Types::IF_X_11 connect architecture.LC_ROOT.LC_COORD.p_X_11 to architecture.LC_ROOT.LC_COMMS.p_X_11 {
            doc /* Member-selected wait-list or closure
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_11
            Basis: derived; status: proposed.
            Source: TL-03
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_12 : Types::IF_X_12 connect architecture.LC_ROOT.LC_COORD.p_X_12 to architecture.LC_ROOT.LC_COMMS.p_X_12 {
            doc /* Ready tool, location and deadline information
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_12
            Basis: derived; status: proposed.
            Source: TL-05
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_13 : Types::IF_X_13 connect architecture.LC_ROOT.LC_COORD.p_X_13 to architecture.LC_ROOT.LC_RECORDS.p_X_13 {
            doc /* Identified tool reservation linkage
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_13
            Basis: derived; status: proposed.
            Source: TL-08
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_15 : Types::IF_X_15 connect architecture.LC_ROOT.LC_COMMS.p_X_15 to architecture.LC_ROOT.LC_RECORDS.p_X_15 {
            doc /* Confirmed delivery time and reservation identity
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_15
            Basis: derived; status: proposed.
            Source: TL-05
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_16 : Types::IF_X_16 connect architecture.LC_ROOT.LC_COMMS.p_X_16 to architecture.LC_ROOT.LC_COORD.p_X_16 {
            doc /* Missing delivery confirmation
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_16
            Basis: derived; status: proposed.
            Source: TL-05
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_17 : Types::IF_X_17 connect architecture.LC_ROOT.LC_RECORDS.p_X_17 to architecture.LC_ROOT.LC_COMMS.p_X_17 {
            doc /* Effective hold deadline or extension information
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_17
            Basis: derived; status: proposed.
            Source: TL-05
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_18 : Types::IF_X_18 connect architecture.LC_ROOT.LC_RECORDS.p_X_18 to architecture.LC_ROOT.LC_CUSTODY.p_X_18 {
            doc /* Current ready reservation
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_18
            Basis: derived; status: proposed.
            Source: TL-06
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_19 : Types::IF_X_19 connect architecture.LC_ROOT.LC_RECORDS.p_X_19 to architecture.LC_ROOT.LC_COORD.p_X_19 {
            doc /* Deadline and collection/withdrawal state
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_19
            Basis: derived; status: proposed.
            Source: TL-05
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_20 : Types::IF_X_20 connect architecture.LC_ROOT.LC_COORD.p_X_20 to architecture.LC_ROOT.LC_RECORDS.p_X_20 {
            doc /* Still-fit release or reasoned extension disposition
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_20
            Basis: derived; status: proposed.
            Source: TL-05
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_21 : Types::IF_X_21 connect architecture.LC_ROOT.LC_COORD.p_X_21 to architecture.LC_ROOT.LC_COMMS.p_X_21 {
            doc /* Extended or closed request outcome
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_21
            Basis: derived; status: proposed.
            Source: TL-08
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_23 : Types::IF_X_23 connect architecture.LC_ROOT.LC_CUSTODY.p_X_23 to architecture.LC_ROOT.LC_COORD.p_X_23 {
            doc /* Unresolved identity or tool mismatch
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_23
            Basis: derived; status: proposed.
            Source: TL-06
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_25 : Types::IF_X_25 connect architecture.LC_ROOT.LC_CUSTODY.p_X_25 to architecture.LC_ROOT.LC_COORD.p_X_25 {
            doc /* Unresolved acceptance
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_25
            Basis: derived; status: proposed.
            Source: TL-06
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_26 : Types::IF_X_26 connect architecture.LC_ROOT.LC_CUSTODY.p_X_26 to architecture.LC_ROOT.LC_RECORDS.p_X_26 {
            doc /* Recorded library-to-member custody transfer
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_26
            Basis: derived; status: proposed.
            Source: TL-06
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_28 : Types::IF_X_28 connect architecture.LC_ROOT.LC_CUSTODY.p_X_28 to architecture.LC_ROOT.LC_HANDLING.p_X_28 {
            doc /* Confirmed physical receipt and library custody
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_28
            Basis: derived; status: proposed.
            Source: TL-07
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_29 : Types::IF_X_29 connect architecture.LC_ROOT.LC_CUSTODY.p_X_29 to architecture.LC_ROOT.LC_RECORDS.p_X_29 {
            doc /* Awaiting-assessment state and custody
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_29
            Basis: derived; status: proposed.
            Source: TL-07
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_30 : Types::IF_X_30 connect architecture.LC_ROOT.LC_HANDLING.p_X_30 to architecture.LC_ROOT.LC_RECOVERY.p_X_30 {
            doc /* Fit return inspection
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_30
            Basis: derived; status: proposed.
            Source: TL-07
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_31 : Types::IF_X_31 connect architecture.LC_ROOT.LC_HANDLING.p_X_31 to architecture.LC_ROOT.LC_RECOVERY.p_X_31 {
            doc /* Unfit return inspection
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_31
            Basis: derived; status: proposed.
            Source: TL-07
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_33 : Types::IF_X_33 connect architecture.LC_ROOT.LC_RECOVERY.p_X_33 to architecture.LC_ROOT.LC_RECORDS.p_X_33 {
            doc /* Quarantine state
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_33
            Basis: derived; status: proposed.
            Source: TL-08
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_35 : Types::IF_X_35 connect architecture.LC_ROOT.LC_RECOVERY.p_X_35 to architecture.LC_ROOT.LC_HANDLING.p_X_35 {
            doc /* Completed work and remaining defects
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_35
            Basis: derived; status: proposed.
            Source: TL-07
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_36 : Types::IF_X_36 connect architecture.LC_ROOT.LC_HANDLING.p_X_36 to architecture.LC_ROOT.LC_RECOVERY.p_X_36 {
            doc /* Steward fit reassessment
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_36
            Basis: derived; status: proposed.
            Source: TL-07
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_37 : Types::IF_X_37 connect architecture.LC_ROOT.LC_HANDLING.p_X_37 to architecture.LC_ROOT.LC_RECOVERY.p_X_37 {
            doc /* Remaining defects/unfit reassessment
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_37
            Basis: derived; status: proposed.
            Source: TL-07
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_39 : Types::IF_X_39 connect architecture.LC_ROOT.LC_RECOVERY.p_X_39 to architecture.LC_ROOT.LC_RECORDS.p_X_39 {
            doc /* Retirement or retained-quarantine disposition
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_39
            Basis: derived; status: proposed.
            Source: TL-07
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_40 : Types::IF_X_40 connect architecture.LC_ROOT.LC_RECOVERY.p_X_40 to architecture.LC_ROOT.LC_RECORDS.p_X_40 {
            doc /* Authorised available status
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_40
            Basis: derived; status: proposed.
            Source: TL-07
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_41 : Types::IF_X_41 connect architecture.LC_ROOT.LC_RECORDS.p_X_41 to architecture.LC_ROOT.LC_COORD.p_X_41 {
            doc /* Available inventory identities
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_41
            Basis: derived; status: proposed.
            Source: TL-08
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_42 : Types::IF_X_42 connect architecture.LC_ROOT.LC_RECORDS.p_X_42 to architecture.LC_ROOT.LC_COMMS.p_X_42 {
            doc /* Current inventory, reservation and exception state
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_42
            Basis: derived; status: proposed.
            Source: TL-08
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_43 : Types::IF_X_43 connect architecture.LC_ROOT.LC_COORD.p_X_43 to architecture.LC_ROOT.LC_COMMS.p_X_43 {
            doc /* Accountable pending/refused/closed outcome
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_43
            Basis: derived; status: proposed.
            Source: TL-08
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_44 : Types::IF_X_44 connect architecture.LC_ROOT.LC_COORD.p_X_44 to architecture.LC_ROOT.LC_RECORDS.p_X_44 {
            doc /* Unresolved exception and retained state
            Potential transfer with the stated applicability; temporal behavior is modeled separately.
            Record: X_44
            Basis: derived; status: proposed.
            Source: TL-08
            Derived logical contract from candidate primary function allocations. */
        }
    }
    allocation AL_F_REQUEST allocate System::functions.F_ROOT.F_ACQUIRE.F_REQUEST to Logical::architecture.LC_ROOT.LC_COORD {
        doc /* Capture the request responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_REQUEST
        Basis: proposed; status: proposed.
        Source: TL-03
        Keep the capture the request evidence and decision with the reservation coordination responsibility. */
    }
    allocation AL_F_SELECT allocate System::functions.F_ROOT.F_ACQUIRE.F_SELECT to Logical::architecture.LC_ROOT.LC_COORD {
        doc /* Select an available identified candidate responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_SELECT
        Basis: proposed; status: proposed.
        Source: TL-03
        Source: TL-08
        Keep the select an available identified candidate evidence and decision with the reservation coordination responsibility. */
    }
    allocation AL_F_NO_CAND allocate System::functions.F_ROOT.F_ACQUIRE.F_NO_CAND to Logical::architecture.LC_ROOT.LC_COORD {
        doc /* Dispose of an unfilled request responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_NO_CAND
        Basis: proposed; status: proposed.
        Source: TL-03
        Keep the dispose of an unfilled request evidence and decision with the reservation coordination responsibility. */
    }
    allocation AL_F_PREP allocate System::functions.F_ROOT.F_ACQUIRE.F_PREP to Logical::architecture.LC_ROOT.LC_COORD {
        doc /* Establish the preparation case responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_PREP
        Basis: proposed; status: proposed.
        Source: TL-04
        Keep the establish the preparation case evidence and decision with the reservation coordination responsibility. */
    }
    allocation AL_F_ELIG allocate System::functions.F_ROOT.F_ACQUIRE.F_ELIG to Logical::architecture.LC_ROOT.LC_COORD {
        doc /* Obtain the registry decision responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_ELIG
        Basis: proposed; status: proposed.
        Source: TL-02
        Source: TL-04
        Keep the obtain the registry decision evidence and decision with the reservation coordination responsibility. */
    }
    allocation AL_F_INSPECT allocate System::functions.F_ROOT.F_ACQUIRE.F_INSPECT to Logical::architecture.LC_ROOT.LC_HANDLING {
        doc /* Inspect the candidate tool responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_INSPECT
        Basis: proposed; status: proposed.
        Source: TL-04
        Keep the inspect the candidate tool evidence and decision with the condition assessment responsibility. */
    }
    allocation AL_F_ASSESS allocate System::functions.F_ROOT.F_ACQUIRE.F_ASSESS to Logical::architecture.LC_ROOT.LC_COORD {
        doc /* Assess preparation contributions responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_ASSESS
        Basis: proposed; status: proposed.
        Source: TL-04
        Keep the assess preparation contributions evidence and decision with the reservation coordination responsibility. */
    }
    allocation AL_F_RESERVE allocate System::functions.F_ROOT.F_ACQUIRE.F_RESERVE to Logical::architecture.LC_ROOT.LC_COORD {
        doc /* Prepare the ready reservation responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_RESERVE
        Basis: proposed; status: proposed.
        Source: TL-04
        Source: TL-08
        Keep the prepare the ready reservation evidence and decision with the reservation coordination responsibility. */
    }
    allocation AL_F_NOTICE allocate System::functions.F_ROOT.F_LOAN.F_NOTICE to Logical::architecture.LC_ROOT.LC_COMMS {
        doc /* Deliver the ready notice responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_NOTICE
        Basis: proposed; status: proposed.
        Source: TL-05
        Keep the deliver the ready notice evidence and decision with the member communication responsibility. */
    }
    allocation AL_F_CONFIRM allocate System::functions.F_ROOT.F_LOAN.F_CONFIRM to Logical::architecture.LC_ROOT.LC_COMMS {
        doc /* Record confirmed notice delivery responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_CONFIRM
        Basis: proposed; status: proposed.
        Source: TL-05
        Keep the record confirmed notice delivery evidence and decision with the member communication responsibility. */
    }
    allocation AL_F_HOLD allocate System::functions.F_ROOT.F_LOAN.F_HOLD to Logical::architecture.LC_ROOT.LC_RECORDS {
        doc /* Govern the confirmed hold interval responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_HOLD
        Basis: proposed; status: proposed.
        Source: TL-05
        Keep the govern the confirmed hold interval evidence and decision with the service state and inventory responsibility. */
    }
    allocation AL_F_EXPIRY allocate System::functions.F_ROOT.F_LOAN.F_EXPIRY to Logical::architecture.LC_ROOT.LC_COORD {
        doc /* Resolve expiry, withdrawal or extension responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_EXPIRY
        Basis: proposed; status: proposed.
        Source: TL-05
        Keep the resolve expiry, withdrawal or extension evidence and decision with the reservation coordination responsibility. */
    }
    allocation AL_F_MATCH allocate System::functions.F_ROOT.F_LOAN.F_MATCH to Logical::architecture.LC_ROOT.LC_CUSTODY {
        doc /* Match the collection case responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_MATCH
        Basis: proposed; status: proposed.
        Source: TL-06
        Keep the match the collection case evidence and decision with the custody handover responsibility. */
    }
    allocation AL_F_ACCEPT allocate System::functions.F_ROOT.F_LOAN.F_ACCEPT to Logical::architecture.LC_ROOT.LC_CUSTODY {
        doc /* Capture terms and identified-tool receipt acceptance responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_ACCEPT
        Basis: proposed; status: proposed.
        Source: TL-06
        Keep the capture terms and identified-tool receipt acceptance evidence and decision with the custody handover responsibility. */
    }
    allocation AL_F_TRANSFER allocate System::functions.F_ROOT.F_LOAN.F_TRANSFER to Logical::architecture.LC_ROOT.LC_CUSTODY {
        doc /* Record custody transfer to member responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_TRANSFER
        Basis: proposed; status: proposed.
        Source: TL-06
        Keep the record custody transfer to member evidence and decision with the custody handover responsibility. */
    }
    allocation AL_F_ONLOAN allocate System::functions.F_ROOT.F_LOAN.F_ONLOAN to Logical::architecture.LC_ROOT.LC_RECORDS {
        doc /* Record the tool on loan responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_ONLOAN
        Basis: proposed; status: proposed.
        Source: TL-06
        Source: TL-08
        Keep the record the tool on loan evidence and decision with the service state and inventory responsibility. */
    }
    allocation AL_F_RECEIVE allocate System::functions.F_ROOT.F_RETURN.F_RECEIVE to Logical::architecture.LC_ROOT.LC_CUSTODY {
        doc /* Confirm returned-tool receipt responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_RECEIVE
        Basis: proposed; status: proposed.
        Source: TL-07
        Keep the confirm returned-tool receipt evidence and decision with the custody handover responsibility. */
    }
    allocation AL_F_RETURN_ASSESS allocate System::functions.F_ROOT.F_RETURN.F_RETURN_ASSESS to Logical::architecture.LC_ROOT.LC_HANDLING {
        doc /* Assess returned-tool condition responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_RETURN_ASSESS
        Basis: proposed; status: proposed.
        Source: TL-07
        Keep the assess returned-tool condition evidence and decision with the condition assessment responsibility. */
    }
    allocation AL_F_QUARANTINE allocate System::functions.F_ROOT.F_RETURN.F_QUARANTINE to Logical::architecture.LC_ROOT.LC_RECOVERY {
        doc /* Quarantine an unfit tool responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_QUARANTINE
        Basis: proposed; status: proposed.
        Source: TL-04
        Source: TL-07
        Keep the quarantine an unfit tool evidence and decision with the condition recovery responsibility. */
    }
    allocation AL_F_REPAIR_REQUEST allocate System::functions.F_ROOT.F_RETURN.F_REPAIR_REQUEST to Logical::architecture.LC_ROOT.LC_RECOVERY {
        doc /* Coordinate the repair request responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_REPAIR_REQUEST
        Basis: proposed; status: proposed.
        Source: TL-07
        Keep the coordinate the repair request evidence and decision with the condition recovery responsibility. */
    }
    allocation AL_F_REPAIR_REPORT allocate System::functions.F_ROOT.F_RETURN.F_REPAIR_REPORT to Logical::architecture.LC_ROOT.LC_RECOVERY {
        doc /* Receive the repair report responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_REPAIR_REPORT
        Basis: proposed; status: proposed.
        Source: TL-02
        Source: TL-07
        Keep the receive the repair report evidence and decision with the condition recovery responsibility. */
    }
    allocation AL_F_REASSESS allocate System::functions.F_ROOT.F_RETURN.F_REASSESS to Logical::architecture.LC_ROOT.LC_HANDLING {
        doc /* Reassess after repair responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_REASSESS
        Basis: proposed; status: proposed.
        Source: TL-07
        Keep the reassess after repair evidence and decision with the condition assessment responsibility. */
    }
    allocation AL_F_RELEASE allocate System::functions.F_ROOT.F_RETURN.F_RELEASE to Logical::architecture.LC_ROOT.LC_RECOVERY {
        doc /* Release a fit tool for availability responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_RELEASE
        Basis: proposed; status: proposed.
        Source: TL-07
        Keep the release a fit tool for availability evidence and decision with the condition recovery responsibility. */
    }
    allocation AL_F_DISPOSITION allocate System::functions.F_ROOT.F_RETURN.F_DISPOSITION to Logical::architecture.LC_ROOT.LC_RECOVERY {
        doc /* Decide rework or retirement responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_DISPOSITION
        Basis: proposed; status: proposed.
        Source: TL-07
        Keep the decide rework or retirement evidence and decision with the condition recovery responsibility. */
    }
    allocation AL_F_EXCEPTION allocate System::functions.F_ROOT.F_SUPPORT.F_EXCEPTION to Logical::architecture.LC_ROOT.LC_COORD {
        doc /* Coordinate an unresolved case responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_EXCEPTION
        Basis: proposed; status: proposed.
        Source: TL-04
        Source: TL-05
        Source: TL-06
        Source: TL-07
        Keep the coordinate an unresolved case evidence and decision with the reservation coordination responsibility. */
    }
    allocation AL_F_LEDGER allocate System::functions.F_ROOT.F_SUPPORT.F_LEDGER to Logical::architecture.LC_ROOT.LC_RECORDS {
        doc /* Maintain custody, condition and availability state responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_LEDGER
        Basis: proposed; status: proposed.
        Source: TL-08
        Keep the maintain custody, condition and availability state evidence and decision with the service state and inventory responsibility. */
    }
    allocation AL_F_STATUS allocate System::functions.F_ROOT.F_SUPPORT.F_STATUS to Logical::architecture.LC_ROOT.LC_COMMS {
        doc /* Communicate the current request outcome responsibility
        Candidate allocation; no implementation or organisation is selected.
        Record: AL_F_STATUS
        Basis: proposed; status: proposed.
        Source: TL-07
        Source: TL-08
        Keep the communicate the current request outcome evidence and decision with the member communication responsibility. */
    }
    dependency trace_F_ROOT_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_ACQUIRE_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT::F_ACQUIRE to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_LOAN_OA_CUSTODY from ToolLibraryArchitecture::System::functions::F_ROOT::F_LOAN to ToolLibraryArchitecture::Operational::activities::OA_CUSTODY {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_RETURN_OA_CONDITION from ToolLibraryArchitecture::System::functions::F_ROOT::F_RETURN to ToolLibraryArchitecture::Operational::activities::OA_CONDITION {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_SUPPORT_OA_INFO from ToolLibraryArchitecture::System::functions::F_ROOT::F_SUPPORT to ToolLibraryArchitecture::Operational::activities::OA_INFO {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_REQUEST_OA_REQUEST from ToolLibraryArchitecture::System::functions::F_ROOT::F_ACQUIRE::F_REQUEST to ToolLibraryArchitecture::Operational::activities::OA_REQUEST {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_SELECT_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT::F_ACQUIRE::F_SELECT to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_NO_CAND_OA_REQUEST from ToolLibraryArchitecture::System::functions::F_ROOT::F_ACQUIRE::F_NO_CAND to ToolLibraryArchitecture::Operational::activities::OA_REQUEST {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_PREP_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT::F_ACQUIRE::F_PREP to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_ELIG_OA_ELIG from ToolLibraryArchitecture::System::functions::F_ROOT::F_ACQUIRE::F_ELIG to ToolLibraryArchitecture::Operational::activities::OA_ELIG {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_INSPECT_OA_CONDITION from ToolLibraryArchitecture::System::functions::F_ROOT::F_ACQUIRE::F_INSPECT to ToolLibraryArchitecture::Operational::activities::OA_CONDITION {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_ASSESS_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT::F_ACQUIRE::F_ASSESS to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_RESERVE_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT::F_ACQUIRE::F_RESERVE to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_NOTICE_OA_INFO from ToolLibraryArchitecture::System::functions::F_ROOT::F_LOAN::F_NOTICE to ToolLibraryArchitecture::Operational::activities::OA_INFO {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_CONFIRM_OA_INFO from ToolLibraryArchitecture::System::functions::F_ROOT::F_LOAN::F_CONFIRM to ToolLibraryArchitecture::Operational::activities::OA_INFO {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_HOLD_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT::F_LOAN::F_HOLD to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_EXPIRY_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT::F_LOAN::F_EXPIRY to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_MATCH_OA_CUSTODY from ToolLibraryArchitecture::System::functions::F_ROOT::F_LOAN::F_MATCH to ToolLibraryArchitecture::Operational::activities::OA_CUSTODY {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_ACCEPT_OA_REQUEST from ToolLibraryArchitecture::System::functions::F_ROOT::F_LOAN::F_ACCEPT to ToolLibraryArchitecture::Operational::activities::OA_REQUEST {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_TRANSFER_OA_CUSTODY from ToolLibraryArchitecture::System::functions::F_ROOT::F_LOAN::F_TRANSFER to ToolLibraryArchitecture::Operational::activities::OA_CUSTODY {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_ONLOAN_OA_INFO from ToolLibraryArchitecture::System::functions::F_ROOT::F_LOAN::F_ONLOAN to ToolLibraryArchitecture::Operational::activities::OA_INFO {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_RECEIVE_OA_CUSTODY from ToolLibraryArchitecture::System::functions::F_ROOT::F_RETURN::F_RECEIVE to ToolLibraryArchitecture::Operational::activities::OA_CUSTODY {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_RETURN_ASSESS_OA_CONDITION from ToolLibraryArchitecture::System::functions::F_ROOT::F_RETURN::F_RETURN_ASSESS to ToolLibraryArchitecture::Operational::activities::OA_CONDITION {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_QUARANTINE_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT::F_RETURN::F_QUARANTINE to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_REPAIR_REQUEST_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT::F_RETURN::F_REPAIR_REQUEST to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_REPAIR_REPORT_OA_REPAIR from ToolLibraryArchitecture::System::functions::F_ROOT::F_RETURN::F_REPAIR_REPORT to ToolLibraryArchitecture::Operational::activities::OA_REPAIR {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_REASSESS_OA_CONDITION from ToolLibraryArchitecture::System::functions::F_ROOT::F_RETURN::F_REASSESS to ToolLibraryArchitecture::Operational::activities::OA_CONDITION {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_RELEASE_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT::F_RETURN::F_RELEASE to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_DISPOSITION_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT::F_RETURN::F_DISPOSITION to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_EXCEPTION_OA_COORD from ToolLibraryArchitecture::System::functions::F_ROOT::F_SUPPORT::F_EXCEPTION to ToolLibraryArchitecture::Operational::activities::OA_COORD {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_LEDGER_OA_INFO from ToolLibraryArchitecture::System::functions::F_ROOT::F_SUPPORT::F_LEDGER to ToolLibraryArchitecture::Operational::activities::OA_INFO {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_STATUS_OA_INFO from ToolLibraryArchitecture::System::functions::F_ROOT::F_SUPPORT::F_STATUS to ToolLibraryArchitecture::Operational::activities::OA_INFO {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    package Context {
        interface CX_01 : Types::IF_CX_01 connect Operational::context.A_MEMBER.p_CX_01 to Logical::architecture.LC_ROOT.LC_COORD.p_CX_01 {
            doc /* Request, period, category, wait-list/closure choice and withdrawal
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_01
            Basis: derived; status: proposed.
            Source: TL-03
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_02 : Types::IF_CX_02 connect Logical::architecture.LC_ROOT.LC_COORD.p_CX_02 to Operational::context.A_REGISTRY.p_CX_02 {
            doc /* Identified membership eligibility query
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_02
            Basis: derived; status: proposed.
            Source: TL-04
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_03 : Types::IF_CX_03 connect Operational::context.A_REGISTRY.p_CX_03 to Logical::architecture.LC_ROOT.LC_COORD.p_CX_03 {
            doc /* Member-linked eligibility decision and decision identity
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_03
            Basis: derived; status: proposed.
            Source: TL-04
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_04 : Types::IF_CX_04 connect Logical::architecture.LC_ROOT.LC_COMMS.p_CX_04 to Operational::context.A_MEMBER.p_CX_04 {
            doc /* Ready tool, location, deadline and current request outcome
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_04
            Basis: derived; status: proposed.
            Source: TL-05
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_05 : Types::IF_CX_05 connect Operational::context.A_MEMBER.p_CX_05 to Logical::architecture.LC_ROOT.LC_CUSTODY.p_CX_05 {
            doc /* Loan terms and identified-tool receipt acceptance
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_05
            Basis: derived; status: proposed.
            Source: TL-06
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_06 : Types::IF_CX_06 connect Operational::context.A_STEWARD.p_CX_06 to Logical::architecture.LC_ROOT.LC_HANDLING.p_CX_06 {
            doc /* Tool-linked condition findings and inspections
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_06
            Basis: derived; status: proposed.
            Source: TL-04
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_07 : Types::IF_CX_07 connect Operational::context.A_STEWARD.p_CX_07 to Logical::architecture.LC_ROOT.LC_CUSTODY.p_CX_07 {
            doc /* Matching and physical returned-tool receipt evidence
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_07
            Basis: derived; status: proposed.
            Source: TL-07
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_08 : Types::IF_CX_08 connect Logical::architecture.LC_ROOT.LC_RECOVERY.p_CX_08 to Operational::context.A_REPAIR.p_CX_08 {
            doc /* Identified-tool repair request and defects
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_08
            Basis: derived; status: proposed.
            Source: TL-07
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_09 : Types::IF_CX_09 connect Operational::context.A_REPAIR.p_CX_09 to Logical::architecture.LC_ROOT.LC_RECOVERY.p_CX_09 {
            doc /* Work completed and known remaining defects
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_09
            Basis: derived; status: proposed.
            Source: TL-07
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_10 : Types::IF_CX_10 connect Operational::context.A_COORD.p_CX_10 to Logical::architecture.LC_ROOT.LC_COORD.p_CX_10 {
            doc /* Exception, extension and reservation disposition
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_10
            Basis: derived; status: proposed.
            Source: TL-05
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_11 : Types::IF_CX_11 connect Operational::context.A_COORD.p_CX_11 to Logical::architecture.LC_ROOT.LC_RECOVERY.p_CX_11 {
            doc /* Repair, quarantine release or retirement decision
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_11
            Basis: derived; status: proposed.
            Source: TL-07
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_12 : Types::IF_CX_12 connect Logical::architecture.LC_ROOT.LC_RECORDS.p_CX_12 to Operational::context.A_STEWARD.p_CX_12 {
            doc /* Tool identity, custody, condition and reservation linkage
            Boundary contract retaining the participant authority; no protocol selected.
            Record: CX_12
            Basis: derived; status: proposed.
            Source: TL-08
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
    }
    package Scenarios {
        action SC_PREP {
            doc /* Prepare a reservation and confirmed notice
            A bounded declared operational thread. Guards are review predicates, not executed decisions.
            Record: SC_PREP
            Basis: derived; status: proposed.
            Source: TL-03
            Source: TL-04
            Source: TL-05
            Entry: Member submits a tool category and collection period.
            Exit: Wait-list/closure, accountable unresolved case, or ready reservation with confirmed hold basis.
            Guards are documented predicates with unspecified values. No execution, guard exclusivity or timing result is claimed. */
            action 'Capture the request' : Types::T_F_REQUEST {
                doc /* Capture the request (Record: request); responsible role: unresolved */
            }
            action 'Select an available identified candidate' : Types::T_F_SELECT {
                doc /* Select an available identified candidate (Record: select); responsible role: unresolved */
            }
            action 'Dispose of an unfilled request' : Types::T_F_NO_CAND {
                doc /* Dispose of an unfilled request (Record: no_candidate); responsible role: unresolved */
            }
            action 'Establish the preparation case' : Types::T_F_PREP {
                doc /* Establish the preparation case (Record: prepare); responsible role: unresolved */
            }
            action 'Obtain the registry decision' : Types::T_F_ELIG {
                doc /* Obtain the registry decision (Record: registry); responsible role: unresolved */
            }
            action 'Inspect the candidate tool' : Types::T_F_INSPECT {
                doc /* Inspect the candidate tool (Record: inspect); responsible role: unresolved */
            }
            action 'Assess preparation contributions' : Types::T_F_ASSESS {
                doc /* Assess preparation contributions (Record: assess); responsible role: unresolved */
            }
            action 'Prepare the ready reservation' : Types::T_F_RESERVE {
                doc /* Prepare the ready reservation (Record: reserve); responsible role: unresolved */
            }
            action 'Quarantine an unfit tool' : Types::T_F_QUARANTINE {
                doc /* Quarantine an unfit tool (Record: quarantine); responsible role: unresolved */
            }
            action 'Coordinate an unresolved case' : Types::T_F_EXCEPTION {
                doc /* Coordinate an unresolved case (Record: pending); responsible role: unresolved */
            }
            action 'Coordinate an unresolved case (refused)' : Types::T_F_EXCEPTION {
                doc /* Coordinate an unresolved case (Record: refused); responsible role: unresolved */
            }
            action 'Deliver the ready notice' : Types::T_F_NOTICE {
                doc /* Deliver the ready notice (Record: notice); responsible role: unresolved */
            }
            action 'Record confirmed notice delivery' : Types::T_F_CONFIRM {
                doc /* Record confirmed notice delivery (Record: confirm); responsible role: unresolved */
            }
            action 'Coordinate an unresolved case (contact)' : Types::T_F_EXCEPTION {
                doc /* Coordinate an unresolved case (Record: contact); responsible role: unresolved */
            }
            action 'Govern the confirmed hold interval' : Types::T_F_HOLD {
                doc /* Govern the confirmed hold interval (Record: hold); responsible role: unresolved */
            }
            action 'Communicate the current request outcome' : Types::T_F_STATUS {
                doc /* Communicate the current request outcome (Record: status); responsible role: unresolved */
            }
            first start then 'Capture the request';
            fork control_PREP_BOTH_fork;
            join control_PREP_BOTH_join;
            succession control_PREP_BOTH_enter first 'Establish the preparation case' then control_PREP_BOTH_fork;
            succession control_PREP_BOTH_leave first control_PREP_BOTH_join then 'Assess preparation contributions';
            attribute 'Complete request identifiers available' : Boolean {
                doc /* Review predicate: Complete request identifiers available */
            }
            succession SC_PREP_T01 first 'Capture the request' if 'Complete request identifiers available' then 'Select an available identified candidate' {
                doc /* Complete request identifiers available; outcome:  */
            }
            attribute 'No candidate tool available' : Boolean {
                doc /* Review predicate: No candidate tool available */
            }
            succession SC_PREP_T02 first 'Select an available identified candidate' if 'No candidate tool available' then 'Dispose of an unfilled request' {
                doc /* No candidate tool available; outcome:  */
            }
            attribute 'Member chooses wait-list or closure; no inventory reserved' : Boolean {
                doc /* Review predicate: Member chooses wait-list or closure; no inventory reserved */
            }
            succession SC_PREP_T03 first 'Dispose of an unfilled request' if 'Member chooses wait-list or closure; no inventory reserved' then 'Communicate the current request outcome' {
                doc /* Member chooses wait-list or closure; no inventory reserved; outcome:  */
            }
            attribute 'An available identified candidate is selected' : Boolean {
                doc /* Review predicate: An available identified candidate is selected */
            }
            succession SC_PREP_T04 first 'Select an available identified candidate' if 'An available identified candidate is selected' then 'Establish the preparation case' {
                doc /* An available identified candidate is selected; outcome:  */
            }
            attribute 'The selected case requires the registry contribution' : Boolean {
                doc /* Review predicate: The selected case requires the registry contribution */
            }
            succession SC_PREP_T05 first control_PREP_BOTH_fork if 'The selected case requires the registry contribution' then 'Obtain the registry decision' {
                doc /* The selected case requires the registry contribution; outcome:  */
            }
            attribute 'The selected case requires the condition contribution' : Boolean {
                doc /* Review predicate: The selected case requires the condition contribution */
            }
            succession SC_PREP_T06 first control_PREP_BOTH_fork if 'The selected case requires the condition contribution' then 'Inspect the candidate tool' {
                doc /* The selected case requires the condition contribution; outcome:  */
            }
            attribute 'Identified registry decision received, including unavailable' : Boolean {
                doc /* Review predicate: Identified registry decision received, including unavailable */
            }
            succession SC_PREP_T07 first 'Obtain the registry decision' if 'Identified registry decision received, including unavailable' then control_PREP_BOTH_join {
                doc /* Identified registry decision received, including unavailable; outcome:  */
            }
            attribute 'Identified fit or unfit inspection recorded' : Boolean {
                doc /* Review predicate: Identified fit or unfit inspection recorded */
            }
            succession SC_PREP_T08 first 'Inspect the candidate tool' if 'Identified fit or unfit inspection recorded' then control_PREP_BOTH_join {
                doc /* Identified fit or unfit inspection recorded; outcome:  */
            }
            attribute 'Selected member eligible and selected tool fit' : Boolean {
                doc /* Review predicate: Selected member eligible and selected tool fit */
            }
            succession SC_PREP_T09 first 'Assess preparation contributions' if 'Selected member eligible and selected tool fit' then 'Prepare the ready reservation' {
                doc /* Selected member eligible and selected tool fit; outcome:  */
            }
            attribute 'Candidate unfit regardless of eligibility disposition' : Boolean {
                doc /* Review predicate: Candidate unfit regardless of eligibility disposition */
            }
            succession SC_PREP_T10 first 'Assess preparation contributions' if 'Candidate unfit regardless of eligibility disposition' then 'Quarantine an unfit tool' {
                doc /* Candidate unfit regardless of eligibility disposition; outcome:  */
            }
            attribute 'Coordinator selects another candidate if one is available' : Boolean {
                doc /* Review predicate: Coordinator selects another candidate if one is available */
            }
            succession SC_PREP_T11 first 'Quarantine an unfit tool' if 'Coordinator selects another candidate if one is available' then 'Select an available identified candidate' {
                doc /* Coordinator selects another candidate if one is available; outcome:  */
            }
            attribute 'Candidate fit and registry unavailable' : Boolean {
                doc /* Review predicate: Candidate fit and registry unavailable */
            }
            succession SC_PREP_T12 first 'Assess preparation contributions' if 'Candidate fit and registry unavailable' then 'Coordinate an unresolved case' {
                doc /* Candidate fit and registry unavailable; outcome:  */
            }
            attribute 'Candidate fit and member ineligible' : Boolean {
                doc /* Review predicate: Candidate fit and member ineligible */
            }
            succession SC_PREP_T13 first 'Assess preparation contributions' if 'Candidate fit and member ineligible' then 'Coordinate an unresolved case (refused)' {
                doc /* Candidate fit and member ineligible; outcome:  */
            }
            attribute 'Request retained pending with coordinator' : Boolean {
                doc /* Review predicate: Request retained pending with coordinator */
            }
            succession SC_PREP_T14 first 'Coordinate an unresolved case' if 'Request retained pending with coordinator' then 'Communicate the current request outcome' {
                doc /* Request retained pending with coordinator; outcome:  */
            }
            attribute 'Refusal/clarification retained with coordinator' : Boolean {
                doc /* Review predicate: Refusal/clarification retained with coordinator */
            }
            succession SC_PREP_T15 first 'Coordinate an unresolved case (refused)' if 'Refusal/clarification retained with coordinator' then 'Communicate the current request outcome' {
                doc /* Refusal/clarification retained with coordinator; outcome:  */
            }
            attribute 'Ready reservation recorded' : Boolean {
                doc /* Review predicate: Ready reservation recorded */
            }
            succession SC_PREP_T16 first 'Prepare the ready reservation' if 'Ready reservation recorded' then 'Deliver the ready notice' {
                doc /* Ready reservation recorded; outcome:  */
            }
            attribute 'Delivery confirmation evidence received' : Boolean {
                doc /* Review predicate: Delivery confirmation evidence received */
            }
            succession SC_PREP_T17 first 'Deliver the ready notice' if 'Delivery confirmation evidence received' then 'Record confirmed notice delivery' {
                doc /* Delivery confirmation evidence received; outcome:  */
            }
            attribute 'Delivery confirmation absent' : Boolean {
                doc /* Review predicate: Delivery confirmation absent */
            }
            succession SC_PREP_T18 first 'Deliver the ready notice' if 'Delivery confirmation absent' then 'Coordinate an unresolved case (contact)' {
                doc /* Delivery confirmation absent; outcome:  */
            }
            attribute 'Coordinator resolves contact and authorises another attempt' : Boolean {
                doc /* Review predicate: Coordinator resolves contact and authorises another attempt */
            }
            succession SC_PREP_T19 first 'Coordinate an unresolved case (contact)' if 'Coordinator resolves contact and authorises another attempt' then 'Deliver the ready notice' {
                doc /* Coordinator resolves contact and authorises another attempt; outcome:  */
            }
            attribute 'Confirmed delivery time matched to the reservation' : Boolean {
                doc /* Review predicate: Confirmed delivery time matched to the reservation */
            }
            succession SC_PREP_T20 first 'Record confirmed notice delivery' if 'Confirmed delivery time matched to the reservation' then 'Govern the confirmed hold interval' {
                doc /* Confirmed delivery time matched to the reservation; outcome:  */
            }
            attribute 'Effective deadline meets minimum confirmed-delivery hold' : Boolean {
                doc /* Review predicate: Effective deadline meets minimum confirmed-delivery hold */
            }
            succession SC_PREP_T21 first 'Govern the confirmed hold interval' if 'Effective deadline meets minimum confirmed-delivery hold' then 'Communicate the current request outcome' {
                doc /* Effective deadline meets minimum confirmed-delivery hold; outcome:  */
            }
            first 'Communicate the current request outcome' then done;
            view ActionFlow : StandardViewDefinitions::ActionFlowView {
                doc /* Prepare a reservation and confirmed notice */
                expose SC_PREP::*;
            }
        }
        action SC_COLLECT {
            doc /* Resolve collection, expiry and failed handover
            A bounded declared operational thread. Guards are review predicates, not executed decisions.
            Record: SC_COLLECT
            Basis: derived; status: proposed.
            Source: TL-05
            Source: TL-06
            Entry: An identified ready reservation has a confirmed-delivery hold basis.
            Exit: Recorded loan, expiry/extension, withdrawal or retained exception; no notification-only custody transfer.
            Guards are documented predicates with unspecified values. No execution, guard exclusivity or timing result is claimed. */
            action 'Govern the confirmed hold interval' : Types::T_F_HOLD {
                doc /* Govern the confirmed hold interval (Record: hold); responsible role: unresolved */
            }
            action 'Match the collection case' : Types::T_F_MATCH {
                doc /* Match the collection case (Record: match); responsible role: unresolved */
            }
            action 'Capture terms and identified-tool receipt acceptance' : Types::T_F_ACCEPT {
                doc /* Capture terms and identified-tool receipt acceptance (Record: accept); responsible role: unresolved */
            }
            action 'Record custody transfer to member' : Types::T_F_TRANSFER {
                doc /* Record custody transfer to member (Record: transfer); responsible role: unresolved */
            }
            action 'Record the tool on loan' : Types::T_F_ONLOAN {
                doc /* Record the tool on loan (Record: on_loan); responsible role: unresolved */
            }
            action 'Resolve expiry, withdrawal or extension' : Types::T_F_EXPIRY {
                doc /* Resolve expiry, withdrawal or extension (Record: expiry); responsible role: unresolved */
            }
            action 'Quarantine an unfit tool' : Types::T_F_QUARANTINE {
                doc /* Quarantine an unfit tool (Record: quarantine); responsible role: unresolved */
            }
            action 'Coordinate an unresolved case' : Types::T_F_EXCEPTION {
                doc /* Coordinate an unresolved case (Record: exception); responsible role: unresolved */
            }
            action 'Communicate the current request outcome' : Types::T_F_STATUS {
                doc /* Communicate the current request outcome (Record: status); responsible role: unresolved */
            }
            first start then 'Govern the confirmed hold interval';
            attribute 'Member presents during an applicable ready reservation' : Boolean {
                doc /* Review predicate: Member presents during an applicable ready reservation */
            }
            succession SC_COLLECT_T01 first 'Govern the confirmed hold interval' if 'Member presents during an applicable ready reservation' then 'Match the collection case' {
                doc /* Member presents during an applicable ready reservation; outcome:  */
            }
            attribute 'Deadline passed without collection, or member withdraws' : Boolean {
                doc /* Review predicate: Deadline passed without collection, or member withdraws */
            }
            succession SC_COLLECT_T02 first 'Govern the confirmed hold interval' if 'Deadline passed without collection, or member withdraws' then 'Resolve expiry, withdrawal or extension' {
                doc /* Deadline passed without collection, or member withdraws; outcome:  */
            }
            attribute 'New tool fault discovered' : Boolean {
                doc /* Review predicate: New tool fault discovered */
            }
            succession SC_COLLECT_T03 first 'Govern the confirmed hold interval' if 'New tool fault discovered' then 'Quarantine an unfit tool' {
                doc /* New tool fault discovered; outcome:  */
            }
            attribute 'Member and tool match reservation' : Boolean {
                doc /* Review predicate: Member and tool match reservation */
            }
            succession SC_COLLECT_T04 first 'Match the collection case' if 'Member and tool match reservation' then 'Capture terms and identified-tool receipt acceptance' {
                doc /* Member and tool match reservation; outcome:  */
            }
            attribute 'Identity or tool matching unresolved' : Boolean {
                doc /* Review predicate: Identity or tool matching unresolved */
            }
            succession SC_COLLECT_T05 first 'Match the collection case' if 'Identity or tool matching unresolved' then 'Coordinate an unresolved case' {
                doc /* Identity or tool matching unresolved; outcome:  */
            }
            attribute 'Loan terms and receipt of identified tool accepted' : Boolean {
                doc /* Review predicate: Loan terms and receipt of identified tool accepted */
            }
            succession SC_COLLECT_T06 first 'Capture terms and identified-tool receipt acceptance' if 'Loan terms and receipt of identified tool accepted' then 'Record custody transfer to member' {
                doc /* Loan terms and receipt of identified tool accepted; outcome:  */
            }
            attribute 'Terms or receipt acceptance unresolved' : Boolean {
                doc /* Review predicate: Terms or receipt acceptance unresolved */
            }
            succession SC_COLLECT_T07 first 'Capture terms and identified-tool receipt acceptance' if 'Terms or receipt acceptance unresolved' then 'Coordinate an unresolved case' {
                doc /* Terms or receipt acceptance unresolved; outcome:  */
            }
            attribute 'Custody transfer recorded from library to member' : Boolean {
                doc /* Review predicate: Custody transfer recorded from library to member */
            }
            succession SC_COLLECT_T08 first 'Record custody transfer to member' if 'Custody transfer recorded from library to member' then 'Record the tool on loan' {
                doc /* Custody transfer recorded from library to member; outcome:  */
            }
            attribute 'On-loan state recorded after custody transfer' : Boolean {
                doc /* Review predicate: On-loan state recorded after custody transfer */
            }
            succession SC_COLLECT_T09 first 'Record the tool on loan' if 'On-loan state recorded after custody transfer' then 'Communicate the current request outcome' {
                doc /* On-loan state recorded after custody transfer; outcome:  */
            }
            attribute 'Coordinator records still-fit release or reasoned extension' : Boolean {
                doc /* Review predicate: Coordinator records still-fit release or reasoned extension */
            }
            succession SC_COLLECT_T10 first 'Resolve expiry, withdrawal or extension' if 'Coordinator records still-fit release or reasoned extension' then 'Communicate the current request outcome' {
                doc /* Coordinator records still-fit release or reasoned extension; outcome:  */
            }
            attribute 'Fault and retained custody require coordinator disposition' : Boolean {
                doc /* Review predicate: Fault and retained custody require coordinator disposition */
            }
            succession SC_COLLECT_T11 first 'Quarantine an unfit tool' if 'Fault and retained custody require coordinator disposition' then 'Coordinate an unresolved case' {
                doc /* Fault and retained custody require coordinator disposition; outcome:  */
            }
            attribute 'Normal handover remains incomplete; current exception communicated' : Boolean {
                doc /* Review predicate: Normal handover remains incomplete; current exception communicated */
            }
            succession SC_COLLECT_T12 first 'Coordinate an unresolved case' if 'Normal handover remains incomplete; current exception communicated' then 'Communicate the current request outcome' {
                doc /* Normal handover remains incomplete; current exception communicated; outcome:  */
            }
            first 'Communicate the current request outcome' then done;
            view ActionFlow : StandardViewDefinitions::ActionFlowView {
                doc /* Resolve collection, expiry and failed handover */
                expose SC_COLLECT::*;
            }
        }
        action SC_RECOVER {
            doc /* Return, repair and release condition recovery
            A bounded declared operational thread. Guards are review predicates, not executed decisions.
            Record: SC_RECOVER
            Basis: derived; status: proposed.
            Source: TL-07
            Source: TL-08
            Entry: A returned identified tool is physically presented to a steward.
            Exit: Assessed available, retired, or retained unavailable/quarantine state with current outcome.
            Guards are documented predicates with unspecified values. No execution, guard exclusivity or timing result is claimed. */
            action 'Confirm returned-tool receipt' : Types::T_F_RECEIVE {
                doc /* Confirm returned-tool receipt (Record: receive); responsible role: unresolved */
            }
            action 'Assess returned-tool condition' : Types::T_F_RETURN_ASSESS {
                doc /* Assess returned-tool condition (Record: assess); responsible role: unresolved */
            }
            action 'Quarantine an unfit tool' : Types::T_F_QUARANTINE {
                doc /* Quarantine an unfit tool (Record: quarantine); responsible role: unresolved */
            }
            action 'Coordinate the repair request' : Types::T_F_REPAIR_REQUEST {
                doc /* Coordinate the repair request (Record: repair); responsible role: unresolved */
            }
            action 'Receive the repair report' : Types::T_F_REPAIR_REPORT {
                doc /* Receive the repair report (Record: report); responsible role: unresolved */
            }
            action 'Reassess after repair' : Types::T_F_REASSESS {
                doc /* Reassess after repair (Record: reassess); responsible role: unresolved */
            }
            action 'Release a fit tool for availability' : Types::T_F_RELEASE {
                doc /* Release a fit tool for availability (Record: release); responsible role: unresolved */
            }
            action 'Decide rework or retirement' : Types::T_F_DISPOSITION {
                doc /* Decide rework or retirement (Record: disposition); responsible role: unresolved */
            }
            action 'Maintain custody, condition and availability state' : Types::T_F_LEDGER {
                doc /* Maintain custody, condition and availability state (Record: ledger); responsible role: unresolved */
            }
            action 'Coordinate an unresolved case' : Types::T_F_EXCEPTION {
                doc /* Coordinate an unresolved case (Record: exception); responsible role: unresolved */
            }
            action 'Communicate the current request outcome' : Types::T_F_STATUS {
                doc /* Communicate the current request outcome (Record: status); responsible role: unresolved */
            }
            first start then 'Confirm returned-tool receipt';
            attribute 'Steward confirms identified physical receipt and library custody' : Boolean {
                doc /* Review predicate: Steward confirms identified physical receipt and library custody */
            }
            succession SC_RECOVER_T01 first 'Confirm returned-tool receipt' if 'Steward confirms identified physical receipt and library custody' then 'Assess returned-tool condition' {
                doc /* Steward confirms identified physical receipt and library custody; outcome:  */
            }
            attribute 'Returned tool assessed fit' : Boolean {
                doc /* Review predicate: Returned tool assessed fit */
            }
            succession SC_RECOVER_T02 first 'Assess returned-tool condition' if 'Returned tool assessed fit' then 'Release a fit tool for availability' {
                doc /* Returned tool assessed fit; outcome:  */
            }
            attribute 'Returned tool assessed unfit' : Boolean {
                doc /* Review predicate: Returned tool assessed unfit */
            }
            succession SC_RECOVER_T03 first 'Assess returned-tool condition' if 'Returned tool assessed unfit' then 'Quarantine an unfit tool' {
                doc /* Returned tool assessed unfit; outcome:  */
            }
            attribute 'Coordinator considers the repair disposition' : Boolean {
                doc /* Review predicate: Coordinator considers the repair disposition */
            }
            succession SC_RECOVER_T04 first 'Quarantine an unfit tool' if 'Coordinator considers the repair disposition' then 'Coordinate the repair request' {
                doc /* Coordinator considers the repair disposition; outcome:  */
            }
            attribute 'External repair request authorised; await provider report' : Boolean {
                doc /* Review predicate: External repair request authorised; await provider report */
            }
            succession SC_RECOVER_T05 first 'Coordinate the repair request' if 'External repair request authorised; await provider report' then 'Receive the repair report' {
                doc /* External repair request authorised; await provider report; outcome:  */
            }
            attribute 'Repair decision remains pending' : Boolean {
                doc /* Review predicate: Repair decision remains pending */
            }
            succession SC_RECOVER_T06 first 'Coordinate the repair request' if 'Repair decision remains pending' then 'Coordinate an unresolved case' {
                doc /* Repair decision remains pending; outcome:  */
            }
            attribute 'Repair report received regardless of completion wording' : Boolean {
                doc /* Review predicate: Repair report received regardless of completion wording */
            }
            succession SC_RECOVER_T07 first 'Receive the repair report' if 'Repair report received regardless of completion wording' then 'Reassess after repair' {
                doc /* Repair report received regardless of completion wording; outcome:  */
            }
            attribute 'Steward records fit reassessment and coordinator permits quarantine release' : Boolean {
                doc /* Review predicate: Steward records fit reassessment and coordinator permits quarantine release */
            }
            succession SC_RECOVER_T08 first 'Reassess after repair' if 'Steward records fit reassessment and coordinator permits quarantine release' then 'Release a fit tool for availability' {
                doc /* Steward records fit reassessment and coordinator permits quarantine release; outcome:  */
            }
            attribute 'Defects remain or tool is unfit; retain quarantine' : Boolean {
                doc /* Review predicate: Defects remain or tool is unfit; retain quarantine */
            }
            succession SC_RECOVER_T09 first 'Reassess after repair' if 'Defects remain or tool is unfit; retain quarantine' then 'Decide rework or retirement' {
                doc /* Defects remain or tool is unfit; retain quarantine; outcome:  */
            }
            attribute 'Coordinator requests a separate new repair attempt' : Boolean {
                doc /* Review predicate: Coordinator requests a separate new repair attempt */
            }
            succession SC_RECOVER_T10 first 'Decide rework or retirement' if 'Coordinator requests a separate new repair attempt' then 'Coordinate the repair request' {
                doc /* Coordinator requests a separate new repair attempt; outcome:  */
            }
            attribute 'Coordinator retires tool with recorded disposition' : Boolean {
                doc /* Review predicate: Coordinator retires tool with recorded disposition */
            }
            succession SC_RECOVER_T11 first 'Decide rework or retirement' if 'Coordinator retires tool with recorded disposition' then 'Maintain custody, condition and availability state' {
                doc /* Coordinator retires tool with recorded disposition; outcome:  */
            }
            attribute 'Required fit/release evidence supports available status' : Boolean {
                doc /* Review predicate: Required fit/release evidence supports available status */
            }
            succession SC_RECOVER_T12 first 'Release a fit tool for availability' if 'Required fit/release evidence supports available status' then 'Maintain custody, condition and availability state' {
                doc /* Required fit/release evidence supports available status; outcome:  */
            }
            attribute 'Current custody, condition and disposition recorded' : Boolean {
                doc /* Review predicate: Current custody, condition and disposition recorded */
            }
            succession SC_RECOVER_T13 first 'Maintain custody, condition and availability state' if 'Current custody, condition and disposition recorded' then 'Communicate the current request outcome' {
                doc /* Current custody, condition and disposition recorded; outcome:  */
            }
            attribute 'Quarantine and accountable pending decision remain visible' : Boolean {
                doc /* Review predicate: Quarantine and accountable pending decision remain visible */
            }
            succession SC_RECOVER_T14 first 'Coordinate an unresolved case' if 'Quarantine and accountable pending decision remain visible' then 'Communicate the current request outcome' {
                doc /* Quarantine and accountable pending decision remain visible; outcome:  */
            }
            first 'Communicate the current request outcome' then done;
            view ActionFlow : StandardViewDefinitions::ActionFlowView {
                doc /* Return, repair and release condition recovery */
                expose SC_RECOVER::*;
            }
        }
    }
    package Requirements {
        requirement <R_AUTH> 'Retain registry decision authority' {
            doc /* Applicability: Whenever membership eligibility is required Retain registry member/decision identity and eligible, ineligible or unavailable outcome; neither service nor volunteer creates a positive decision. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-02
            Source: TL-04
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_ELIG = System::functions.F_ROOT.F_ACQUIRE.F_ELIG;
            require constraint criterion {
                doc /* Retain registry member/decision identity and eligible, ineligible or unavailable outcome; neither service nor volunteer creates a positive decision. */
            }
        }
        requirement <R_WAIT> 'Keep wait-list separate from reservation' {
            doc /* Applicability: When no candidate tool exists Offer wait-list or closure at member choice without a reservation or decrease of available inventory. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-03
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_NO_CAND = System::functions.F_ROOT.F_ACQUIRE.F_NO_CAND;
            require constraint criterion {
                doc /* Offer wait-list or closure at member choice without a reservation or decrease of available inventory. */
            }
        }
        requirement <R_GATE> 'Require both matching preparation contributions' {
            doc /* Applicability: Before preparing a ready reservation The selected member is eligible and selected tool fit, with matching decision/inspection identities; unavailable remains pending, ineligible remains accountable, unfit is quarantined. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-04
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_ASSESS = System::functions.F_ROOT.F_ACQUIRE.F_ASSESS;
            require constraint criterion {
                doc /* The selected member is eligible and selected tool fit, with matching decision/inspection identities; unavailable remains pending, ineligible remains accountable, unfit is quarantined. */
            }
        }
        requirement <R_NOTICE> 'Provide the ready notice content' {
            doc /* Applicability: When communicating ready status Identify the ready tool, collection location and hold deadline; retain queueing and confirmed delivery as different events. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-05
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_NOTICE = System::functions.F_ROOT.F_LOAN.F_NOTICE;
            require constraint criterion {
                doc /* Identify the ready tool, collection location and hold deadline; retain queueing and confirmed delivery as different events. */
            }
        }
        requirement <R_HOLD> 'Maintain at least two confirmed-delivery hours' {
            doc /* Applicability: After confirmed delivery unless member withdraws or a new tool fault is discovered Hold the ready reservation for at least two hours measured from confirmed notice delivery, not queued-notice time. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-05
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_HOLD = System::functions.F_ROOT.F_LOAN.F_HOLD;
            require constraint criterion {
                subjectOfRequirement.minimumConfirmedDeliveryHold >= 2 [SI::h]
            }
        }
        requirement <R_NO_ACK> 'Retain pending notification without confirmation' {
            doc /* Applicability: When delivery confirmation is absent Keep pending-notification and coordinator contact resolution; do not expire using an assumed delivery time. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-05
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_CONFIRM = System::functions.F_ROOT.F_LOAN.F_CONFIRM;
            require constraint criterion {
                doc /* Keep pending-notification and coordinator contact resolution; do not expire using an assumed delivery time. */
            }
        }
        requirement <R_EXTEND> 'Record the coordinator expiry/extension decision' {
            doc /* Applicability: After deadline passes without collection Only return a still-fit tool to available or extend with a recorded coordinator reason; retain withdrawal and fault as distinct causes. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-05
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_EXPIRY = System::functions.F_ROOT.F_LOAN.F_EXPIRY;
            require constraint criterion {
                doc /* Only return a still-fit tool to available or extend with a recorded coordinator reason; retain withdrawal and fault as distinct causes. */
            }
        }
        requirement <R_CUSTODY> 'Complete matched and accepted custody handover' {
            doc /* Applicability: Before recording the tool on loan Require member/tool matching, accepted loan terms and receipt of the identified tool; record library-to-member custody then on-loan state. Ready notice, eligibility or presentation alone cannot complete transfer. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-06
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_TRANSFER = System::functions.F_ROOT.F_LOAN.F_TRANSFER;
            require constraint criterion {
                doc /* Require member/tool matching, accepted loan terms and receipt of the identified tool; record library-to-member custody then on-loan state. Ready notice, eligibility or presentation alone cannot complete transfer. */
            }
        }
        requirement <R_RECEIPT> 'Require actual returned-tool receipt' {
            doc /* Applicability: When accepting return of a tool Record steward-confirmed identified receipt and library custody; member return report alone is insufficient. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-07
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_RECEIVE = System::functions.F_ROOT.F_RETURN.F_RECEIVE;
            require constraint criterion {
                doc /* Record steward-confirmed identified receipt and library custody; member return report alone is insufficient. */
            }
        }
        requirement <R_REPAIR> 'Reassess repair without implied release' {
            doc /* Applicability: When a repair report arrives Steward reassesses condition; completion wording or unresolved defects cannot establish fit or lending availability. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-02
            Source: TL-07
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_REASSESS = System::functions.F_ROOT.F_RETURN.F_REASSESS;
            require constraint criterion {
                doc /* Steward reassesses condition; completion wording or unresolved defects cannot establish fit or lending availability. */
            }
        }
        requirement <R_RELEASE> 'Preserve quarantine release authority' {
            doc /* Applicability: Before releasing quarantine Require steward fit assessment and coordinator release decision; remaining defects retain quarantine and require a separate rework/retirement decision. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-07
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_RELEASE = System::functions.F_ROOT.F_RETURN.F_RELEASE;
            require constraint criterion {
                doc /* Require steward fit assessment and coordinator release decision; remaining defects retain quarantine and require a separate rework/retirement decision. */
            }
        }
        requirement <R_INVENTORY> 'Prevent contradictory available offers' {
            doc /* Applicability: Whenever inventory candidates are offered An identified tool is not offered as available while reserved, on loan, awaiting returned-tool assessment or quarantined. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-08
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_LEDGER = System::functions.F_ROOT.F_SUPPORT.F_LEDGER;
            require constraint criterion {
                doc /* An identified tool is not offered as available while reserved, on loan, awaiting returned-tool assessment or quarantined. */
            }
        }
        requirement <R_RECORDS> 'Retain decision-relevant service information' {
            doc /* Applicability: While coordinating a tool/request case Retain tool identity, custody, condition, reservation linkage and unresolved exceptions for steward/coordinator work. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-08
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_LEDGER = System::functions.F_ROOT.F_SUPPORT.F_LEDGER;
            require constraint criterion {
                doc /* Retain tool identity, custody, condition, reservation linkage and unresolved exceptions for steward/coordinator work. */
            }
        }
        requirement <R_OUTCOME> 'Communicate current request disposition' {
            doc /* Applicability: When request status changes Communicate current pending, ready, refused, extended or closed outcome without inferring loan/repair success from notification. */
            comment ReviewBasis /* Basis: source-explicit; status: draft.
            Source: TL-08
            Source: TL-07
            Rationale: Preserve the source condition, authority and observable outcome. */
            subject subjectOfRequirement : ToolLibraryArchitecture::Types::T_F_STATUS = System::functions.F_ROOT.F_SUPPORT.F_STATUS;
            require constraint criterion {
                doc /* Communicate current pending, ready, refused, extended or closed outcome without inferring loan/repair success from notification. */
            }
        }
    }
    package Verification {
        verification def V_R_AUTH {
            doc /* Review retain registry decision authority
            Planned evidence activity; no executed result.
            Record: V_R_AUTH
            Basis: proposed; status: planned.
            Source: TL-02
            Source: TL-04
            Method: Inspection and scenario walkthrough
            Setup: Inspect decision provenance and unavailable/ineligible cases.
            Expected result: Retain registry member/decision identity and eligible, ineligible or unavailable outcome; neither service nor volunteer creates a positive decision.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_ELIG;
            objective {
                verify Requirements::'Retain registry decision authority';
            }
        }
        verification def V_R_WAIT {
            doc /* Review keep wait-list separate from reservation
            Planned evidence activity; no executed result.
            Record: V_R_WAIT
            Basis: proposed; status: planned.
            Source: TL-03
            Method: Inspection and scenario walkthrough
            Setup: Compare inventory before/after wait-list and closure choices.
            Expected result: Offer wait-list or closure at member choice without a reservation or decrease of available inventory.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_NO_CAND;
            objective {
                verify Requirements::'Keep wait-list separate from reservation';
            }
        }
        verification def V_R_GATE {
            doc /* Review require both matching preparation contributions
            Planned evidence activity; no executed result.
            Record: V_R_GATE
            Basis: proposed; status: planned.
            Source: TL-04
            Method: Inspection and scenario walkthrough
            Setup: Walk eligible/fit, unavailable/fit, ineligible/fit and eligible/unfit cases, including mismatched identifiers.
            Expected result: The selected member is eligible and selected tool fit, with matching decision/inspection identities; unavailable remains pending, ineligible remains accountable, unfit is quarantined.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_ASSESS;
            objective {
                verify Requirements::'Require both matching preparation contributions';
            }
        }
        verification def V_R_NOTICE {
            doc /* Review provide the ready notice content
            Planned evidence activity; no executed result.
            Record: V_R_NOTICE
            Basis: proposed; status: planned.
            Source: TL-05
            Method: Inspection and scenario walkthrough
            Setup: Inspect notice content and independent delivery confirmation evidence.
            Expected result: Identify the ready tool, collection location and hold deadline; retain queueing and confirmed delivery as different events.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_NOTICE;
            objective {
                verify Requirements::'Provide the ready notice content';
            }
        }
        verification def V_R_HOLD {
            doc /* Review maintain at least two confirmed-delivery hours
            Planned evidence activity; no executed result.
            Record: V_R_HOLD
            Basis: proposed; status: planned.
            Source: TL-05
            Method: Inspection and scenario walkthrough
            Setup: Use an identified ready reservation and a controlled time basis. Record queued-notice time separately from actual confirmed-delivery time t0. Observe just before t0 + 2 h and at t0 + 2 h; separately observe just before, at and after the agreed hold deadline, which may exceed the minimum. Repeat with no delivery confirmation, member withdrawal, a newly discovered fault, and coordinator extension with a recorded reason. Keep opening hours and the chosen duration as agreed test inputs, not invented source values.
            Expected result: Without withdrawal or a new fault, the reservation remains held before t0 + 2 h and through the applicable agreed hold deadline. At/after the agreed deadline without collection, only the coordinator records a still-fit release or reasoned extension. Withdrawal and new fault follow their explicit dispositions. Without confirmed delivery, pending-notification remains, no t0 is invented and no ordinary expiry is inferred. Queueing time never substitutes for confirmed delivery. These are planned observations, not measured results.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_HOLD;
            objective {
                verify Requirements::'Maintain at least two confirmed-delivery hours';
            }
        }
        verification def V_R_NO_ACK {
            doc /* Review retain pending notification without confirmation
            Planned evidence activity; no executed result.
            Record: V_R_NO_ACK
            Basis: proposed; status: planned.
            Source: TL-05
            Method: Inspection and scenario walkthrough
            Setup: Suppress confirmation and inspect state and absence of assumed-time expiry.
            Expected result: Keep pending-notification and coordinator contact resolution; do not expire using an assumed delivery time.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_CONFIRM;
            objective {
                verify Requirements::'Retain pending notification without confirmation';
            }
        }
        verification def V_R_EXTEND {
            doc /* Review record the coordinator expiry/extension decision
            Planned evidence activity; no executed result.
            Record: V_R_EXTEND
            Basis: proposed; status: planned.
            Source: TL-05
            Method: Inspection and scenario walkthrough
            Setup: Walk expiry, reasoned extension and new-fault cases.
            Expected result: Only return a still-fit tool to available or extend with a recorded coordinator reason; retain withdrawal and fault as distinct causes.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_EXPIRY;
            objective {
                verify Requirements::'Record the coordinator expiry/extension decision';
            }
        }
        verification def V_R_CUSTODY {
            doc /* Review complete matched and accepted custody handover
            Planned evidence activity; no executed result.
            Record: V_R_CUSTODY
            Basis: proposed; status: planned.
            Source: TL-06
            Method: Inspection and scenario walkthrough
            Setup: Try mismatch, missing terms, missing receipt and notice-only cases; compare custody/state event order.
            Expected result: Require member/tool matching, accepted loan terms and receipt of the identified tool; record library-to-member custody then on-loan state. Ready notice, eligibility or presentation alone cannot complete transfer.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_TRANSFER;
            objective {
                verify Requirements::'Complete matched and accepted custody handover';
            }
        }
        verification def V_R_RECEIPT {
            doc /* Review require actual returned-tool receipt
            Planned evidence activity; no executed result.
            Record: V_R_RECEIPT
            Basis: proposed; status: planned.
            Source: TL-07
            Method: Inspection and scenario walkthrough
            Setup: Compare a member-only report with witnessed steward receipt.
            Expected result: Record steward-confirmed identified receipt and library custody; member return report alone is insufficient.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_RECEIVE;
            objective {
                verify Requirements::'Require actual returned-tool receipt';
            }
        }
        verification def V_R_REPAIR {
            doc /* Review reassess repair without implied release
            Planned evidence activity; no executed result.
            Record: V_R_REPAIR
            Basis: proposed; status: planned.
            Source: TL-02
            Source: TL-07
            Method: Inspection and scenario walkthrough
            Setup: Use completed-with-defects report followed by fit and unfit reassessment cases.
            Expected result: Steward reassesses condition; completion wording or unresolved defects cannot establish fit or lending availability.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_REASSESS;
            objective {
                verify Requirements::'Reassess repair without implied release';
            }
        }
        verification def V_R_RELEASE {
            doc /* Review preserve quarantine release authority
            Planned evidence activity; no executed result.
            Record: V_R_RELEASE
            Basis: proposed; status: planned.
            Source: TL-07
            Method: Inspection and scenario walkthrough
            Setup: Inspect release authority and block provider-only completion.
            Expected result: Require steward fit assessment and coordinator release decision; remaining defects retain quarantine and require a separate rework/retirement decision.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_RELEASE;
            objective {
                verify Requirements::'Preserve quarantine release authority';
            }
        }
        verification def V_R_INVENTORY {
            doc /* Review prevent contradictory available offers
            Planned evidence activity; no executed result.
            Record: V_R_INVENTORY
            Basis: proposed; status: planned.
            Source: TL-08
            Method: Inspection and scenario walkthrough
            Setup: Query available offers in each excluded state and after a valid release.
            Expected result: An identified tool is not offered as available while reserved, on loan, awaiting returned-tool assessment or quarantined.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_LEDGER;
            objective {
                verify Requirements::'Prevent contradictory available offers';
            }
        }
        verification def V_R_RECORDS {
            doc /* Review retain decision-relevant service information
            Planned evidence activity; no executed result.
            Record: V_R_RECORDS
            Basis: proposed; status: planned.
            Source: TL-08
            Method: Inspection and scenario walkthrough
            Setup: Inspect a full lifecycle record and deliberately omit each required relation.
            Expected result: Retain tool identity, custody, condition, reservation linkage and unresolved exceptions for steward/coordinator work.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_LEDGER;
            objective {
                verify Requirements::'Retain decision-relevant service information';
            }
        }
        verification def V_R_OUTCOME {
            doc /* Review communicate current request disposition
            Planned evidence activity; no executed result.
            Record: V_R_OUTCOME
            Basis: proposed; status: planned.
            Source: TL-08
            Source: TL-07
            Method: Inspection and scenario walkthrough
            Setup: Compare communicated outcome with current custody, condition and exception state.
            Expected result: Communicate current pending, ready, refused, extended or closed outcome without inferring loan/repair success from notification.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ToolLibraryArchitecture::Types::T_F_STATUS;
            objective {
                verify Requirements::'Communicate current request disposition';
            }
        }
    }
    package ReviewViews {
        view OperationalContext : StandardViewDefinitions::GeneralView {
            doc /* Who participates and what operational activities are in scope? */
            expose Operational::context::*;
            expose Operational::activities::*;
        }
        view SystemFunctions : StandardViewDefinitions::GeneralView {
            doc /* How is the system function decomposed? */
            expose System::functions::*;
        }
        view LogicalInterfaces : StandardViewDefinitions::InterconnectionView {
            doc /* Which proposed responsibilities exchange information or material? */
            expose Logical::architecture::*;
            expose Logical::*;
        }
        view RequirementsAndVerification : StandardViewDefinitions::GeneralView {
            doc /* What must hold and what verification is planned? */
            expose Requirements::*;
            expose Verification::*;
        }
        view Lifecycle_SM_TOOL : StandardViewDefinitions::StateTransitionView {
            doc /* Identified-tool availability lifecycle */
            expose Types::T_SM_TOOL::*;
        }
    }
    package ReviewDecisions {
        package D_PRIORITY {
            doc /* How are competing requests ordered?
            Unresolved design question; options are proposals, not approved policy.
            Record: D_PRIORITY
            Basis: proposed; status: proposed.
            Source: TL-03
            How are competing requests ordered?
            Alternatives: ["FIFO", "Prioritised allocation with an agreed basis"] */
        }
        package D_REGISTRY {
            doc /* What are decision freshness and registry wait limits?
            Unresolved design question; options are proposals, not approved policy.
            Record: D_REGISTRY
            Basis: proposed; status: proposed.
            Source: TL-04
            What are decision freshness and registry wait limits?
            Alternatives: ["Agree validity and timeout policy", "Retain explicit pending cases until a decision"] */
        }
        package D_NOTICE {
            doc /* How are notice deadline and actual delivery confirmation coordinated?
            Unresolved design question; options are proposals, not approved policy.
            Record: D_NOTICE
            Basis: proposed; status: proposed.
            Source: TL-05
            How are notice deadline and actual delivery confirmation coordinated?
            Alternatives: ["Agreed acknowledgement plus reconciled deadline", "Another agreed confirmation/deadline protocol"] */
        }
        package D_HOURS {
            doc /* Which opening hours and hold duration beyond the minimum apply?
            Unresolved design question; options are proposals, not approved policy.
            Record: D_HOURS
            Basis: proposed; status: proposed.
            Source: TL-05
            Which opening hours and hold duration beyond the minimum apply?
            Alternatives: ["Agree collection windows and duration", "Keep minimum bound and schedule unresolved"] */
        }
        package D_SIZING {
            doc /* What demand, inventory and volunteer basis supports sizing?
            Unresolved design question; options are proposals, not approved policy.
            Record: D_SIZING
            Basis: proposed; status: proposed.
            Source: TL-08
            What demand, inventory and volunteer basis supports sizing?
            Alternatives: ["Gather demand/capacity observations", "Retain unquantified concept until evidence exists"] */
        }
        package D_COMBINED {
            doc /* How are simultaneous reservation exceptions ordered?
            Unresolved design question; options are proposals, not approved policy.
            Record: D_COMBINED
            Basis: proposed; status: proposed.
            Source: TL-04
            Source: TL-05
            How are simultaneous reservation exceptions ordered?
            Alternatives: ["Prioritise condition quarantine while preserving eligibility state", "Agree another explicit rule preserving both obligations"] */
        }
    }
}
