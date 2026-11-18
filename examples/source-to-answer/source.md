# Community Tool Library — fictional Concept of Operations

This is an invented engineering exercise. It does not describe a real organisation, existing policy, approved design, or safety standard. Clause identifiers are the source locators for a new-domain capability test. This brief was written before any architecture was authored for it.

## TL-01 — Purpose and boundary

The tool library lets neighbourhood members reserve, collect and return individually identified gardening tools. The service under study includes reservation coordination, volunteer-steward work, inventory/custody records, member communications and the decision to make a returned tool available again. It exchanges eligibility decisions with an independently managed membership registry and repair outcomes with an external repair provider. Registry internals, repair methods, payment collection, transport to a member's home and procurement of additional tools are outside this study. The brief does not select software, a locker, an organisation structure, or a communications technology.

## TL-02 — Participants and authority

A member requests a tool and accepts the terms of a loan. A volunteer steward handles tools and confirms condition. The duty coordinator owns exceptions and may extend a ready reservation with a recorded reason. The external membership registry alone owns the membership-eligibility decision; neither the tool service nor its volunteers may create a positive registry decision. The external repair provider may report work completed and known remaining defects, but does not decide whether the library offers a tool for loan again.

## TL-03 — Request and candidate selection

A request identifies the member, tool category and desired collection period. The service identifies an available candidate tool by its unique inventory identifier. If no candidate exists, the coordinator offers a wait-list or closes the request at the member's choice. A wait-list offer is not a reservation of a tool and must not reduce available inventory. The rule for choosing between competing requests has not been agreed.

## TL-04 — Independent preparation contributions

For a selected candidate, the service requests an eligibility decision from the registry while a steward inspects the candidate's condition. These two contributions may proceed concurrently; neither requires the other to finish first. The registry returns eligible, ineligible or unavailable, identifying the member and decision. The steward returns fit or unfit, identifying the tool and inspection. The service may prepare a ready reservation only when the selected member is eligible and the selected tool is fit. An unavailable registry result leaves the request pending; an ineligible result leaves it with the coordinator for refusal/clarification. An unfit candidate is quarantined and another candidate may be selected. This brief supplies no decision-freshness limit or maximum wait for the registry.

## TL-05 — Ready notice and hold interval

The service tells the member which tool is ready, the collection location and the hold deadline. The hold interval starts when delivery of the ready notice is confirmed, not when the notice is queued. Unless the member withdraws or a new tool fault is discovered, the ready reservation is held for at least two hours after confirmed notice delivery. If confirmation is absent, the reservation remains pending-notification and the coordinator resolves the contact problem; the service must not expire it using an assumed delivery time. After the hold deadline passes without collection, the coordinator may return a still-fit tool to available status or extend the reservation with a reason. Opening hours, channel acknowledgements and the chosen hold duration beyond the minimum require agreement.

## TL-06 — Collection and custody

At collection, a steward checks the member and the allocated tool against the reservation. The member accepts the loan terms and receipt of that identified tool. The service records the custody transfer from library to member and then records the tool as on loan. A ready notice, eligibility result or physical presentation of a tool by itself does not complete the custody transfer. If identity, tool matching or acceptance is unresolved, the coordinator retains the exception and the normal loan handover does not complete.

## TL-07 — Return and condition recovery

A steward receives the identified tool, confirms receipt and records library custody. A member's report that a tool has been returned is not itself receipt evidence. The returned tool remains unavailable until its condition is assessed. A fit return may become available. An unfit return is quarantined and the coordinator decides whether to request external repair. After a repair report is received, a steward reassesses the tool. Only the steward's fit assessment permits the coordinator to release quarantine. A completed repair report with unresolved defects retains quarantine; a new repair attempt or retirement is a separate coordinator decision. No loan-success or repair-success claim follows solely from a notification.

## TL-08 — Service information and unresolved sizing

Members receive the current outcome of their request, including pending, ready, refused, extended or closed states. Stewards and the coordinator need inventory identity, current custody, condition, reservation linkage and unresolved exceptions. The service must not offer the same identified tool as available while it is reserved, on loan, awaiting returned-tool assessment or quarantined. Demand, tool counts, volunteer capacity, collection opening hours, target turnaround time and notification delivery performance are unknown. The architecture should identify the information needed for those assessments without assigning numbers. Verification activities may be planned from this brief; none have been executed.
