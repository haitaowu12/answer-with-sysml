package ConOpsArchitecture {
    private import ScalarValues::*;
    doc /* Skill-enabled work and skill improvement
    Conceptual lifecycle across package, agent, host and tools. Codex-specific facts are explicitly scoped; maintenance gates are a proposed design.
    Basis: proposed; status: draft.
    Concept architecture for review. Source statements, derived mappings and design proposals retain separate status. */
    package Types {
        item def I_X_0 {
            doc /* Available package identity
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_0
            Basis: derived; status: draft.
            Source: S4
            Available package identity
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_1 {
            doc /* Names and descriptions
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_1
            Basis: derived; status: draft.
            Source: S3
            Names and descriptions
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_2 {
            doc /* Selected package identity
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_2
            Basis: derived; status: draft.
            Source: S5
            Selected package identity
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_3 {
            doc /* Workflow instructions
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_3
            Basis: derived; status: draft.
            Source: S3
            Workflow instructions
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_4 {
            doc /* Relevant domain detail
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_4
            Basis: derived; status: draft.
            Source: S3
            Relevant domain detail
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_5 {
            doc /* Chosen template
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_5
            Basis: derived; status: draft.
            Source: S2
            Source: S10
            Chosen template
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_6 {
            doc /* Proposed operation and inputs
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_6
            Basis: derived; status: draft.
            Source: S9
            Proposed operation and inputs
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_7 {
            doc /* Permitted operation with prerequisites
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_7
            Basis: derived; status: draft.
            Source: S9
            Permitted operation with prerequisites
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_8 {
            doc /* Operation identity
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_8
            Basis: derived; status: draft.
            Source: S7
            Operation identity
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_9 {
            doc /* Artifact or error evidence
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_9
            Basis: derived; status: draft.
            Source: S7
            Source: S9
            Artifact or error evidence
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_10 {
            doc /* Reviewed outcome
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_10
            Basis: derived; status: draft.
            Source: S9
            Reviewed outcome
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_11 {
            doc /* Candidate and baseline revisions
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_11
            Basis: derived; status: draft.
            Source: S8
            Candidate and baseline revisions
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_12 {
            doc /* Observed paired results
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_12
            Basis: derived; status: draft.
            Source: S8
            Observed paired results
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_13 {
            doc /* Failure evidence
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_13
            Basis: derived; status: draft.
            Source: S8
            Failure evidence
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_14 {
            doc /* Revised candidate
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_14
            Basis: derived; status: draft.
            Source: S8
            Source: S11
            Revised candidate
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_15 {
            doc /* Candidate evaluation evidence
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_15
            Basis: derived; status: draft.
            Source: S11
            Candidate evaluation evidence
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_16 {
            doc /* Released package
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_16
            Basis: derived; status: draft.
            Source: S11
            Released package
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_17 {
            doc /* Task and source brief
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_17
            Basis: derived; status: draft.
            Source: S10
            Task and source brief
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_18 {
            doc /* Source-linked model assertions
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_18
            Basis: derived; status: draft.
            Source: S10
            Source-linked model assertions
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_19 {
            doc /* Candidate native model
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_19
            Basis: derived; status: draft.
            Source: S10
            Candidate native model
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_20 {
            doc /* Qualified model and report
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_20
            Basis: derived; status: draft.
            Source: S10
            Qualified model and report
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_21 {
            doc /* HTML views and model bindings
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_21
            Basis: derived; status: draft.
            Source: S10
            HTML views and model bindings
            Potential exchange; applicability: Applicable to the current task or revision */
        }
        item def I_X_PLAIN {
            doc /* No matching available skill
            Alternative outcome retained explicitly.
            Record: X_PLAIN
            Basis: derived; status: draft.
            Source: S5
            Source: S9
            No matching available skill
            Potential exchange; applicability: The named alternative applies */
        }
        item def I_X_BLOCK {
            doc /* Unavailable prerequisite or permission
            Alternative outcome retained explicitly.
            Record: X_BLOCK
            Basis: derived; status: draft.
            Source: S9
            Unavailable prerequisite or permission
            Potential exchange; applicability: The named alternative applies */
        }
        item def I_CX_0 {
            doc /* Intent, input files and explicit selection
            The task owner supplies the requested outcome, source files and any explicitly selected skill to the agent.
            Record: CX_0
            Basis: derived; status: draft.
            Source: S5
            Source: S9
            Intent, input files and explicit selection
            Potential exchange; applicability: When the corresponding task, operation or revision requires this exchange */
        }
        item def I_CX_1 {
            doc /* Accessible trusted package locations
            The host exposes package locations that are available in its environment and allowed by its trust policy; a remote host may not have local user files.
            Record: CX_1
            Basis: derived; status: draft.
            Source: S4
            Accessible trusted package locations
            Potential exchange; applicability: When the corresponding task, operation or revision requires this exchange */
        }
        item def I_CX_2 {
            doc /* Capabilities and permission disposition
            Before an operation is requested, the host provides which tools are available and whether the intended action is allowed. A matching skill does not supply that authority.
            Record: CX_2
            Basis: derived; status: draft.
            Source: S9
            Capabilities and permission disposition
            Potential exchange; applicability: When the corresponding task, operation or revision requires this exchange */
        }
        item def I_CX_3 {
            doc /* Operation request and inputs
            Execution coordination sends the selected tool an operation name and explicit inputs only after the applicable prerequisites and permissions are satisfied.
            Record: CX_3
            Basis: derived; status: draft.
            Source: S7
            Operation request and inputs
            Potential exchange; applicability: When the corresponding task, operation or revision requires this exchange */
        }
        item def I_CX_4 {
            doc /* Output artifact or error
            The tool returns an output artifact or an error. Execution coordination inspects that response before the agent can treat the task as complete.
            Record: CX_4
            Basis: derived; status: draft.
            Source: S7
            Output artifact or error
            Potential exchange; applicability: When the corresponding task, operation or revision requires this exchange */
        }
        item def I_CX_5 {
            doc /* Reviewed result or precise blocker
            The agent returns the checked result to the task owner, or identifies the work that remains unresolved.
            Record: CX_5
            Basis: derived; status: draft.
            Source: S9
            Reviewed result or precise blocker
            Potential exchange; applicability: When the corresponding task, operation or revision requires this exchange */
        }
        item def I_CX_6 {
            doc /* Candidate revision and intended behavior
            The maintainer submits an identified candidate revision with the task scope and behavior it is intended to improve.
            Record: CX_6
            Basis: derived; status: draft.
            Source: S6
            Source: S11
            Candidate revision and intended behavior
            Potential exchange; applicability: When the corresponding task, operation or revision requires this exchange */
        }
        item def I_CX_7 {
            doc /* Candidate and baseline outputs
            Outcome assurance supplies candidate and baseline outputs from comparable tasks for independent review.
            Record: CX_7
            Basis: derived; status: draft.
            Source: S8
            Candidate and baseline outputs
            Potential exchange; applicability: When the corresponding task, operation or revision requires this exchange */
        }
        item def I_CX_8 {
            doc /* Comparative quality judgment
            The evaluator returns observed strengths, failures and regressions, without treating a favorable single example as universal reliability.
            Record: CX_8
            Basis: derived; status: draft.
            Source: S8
            Comparative quality judgment
            Potential exchange; applicability: When the corresponding task, operation or revision requires this exchange */
        }
        part def T_USER {
            doc /* Task owner
            Supplies intent, inputs and decisions.
            Record: USER
            Basis: derived; status: draft.
            Source: S5
            Source: S9 */
            port p_CX_0 : P_CX_0;
            port p_CX_5 : ~P_CX_5;
        }
        part def T_AUTHOR {
            doc /* Skill maintainer
            Curates focused methods and tests candidate revisions.
            Record: AUTHOR
            Basis: derived; status: draft.
            Source: S6
            Source: S8 */
            port p_CX_6 : P_CX_6;
        }
        part def T_HOST {
            doc /* Host runtime
            Discovers accessible packages and mediates access and execution.
            Record: HOST
            Basis: derived; status: draft.
            Source: S4
            Source: S5
            Source: S9 */
            port p_CX_1 : P_CX_1;
            port p_CX_2 : P_CX_2;
        }
        part def T_TOOLS {
            doc /* Execution tools
            Return operation results, artifacts or errors.
            Record: TOOLS
            Basis: derived; status: draft.
            Source: S7
            Source: S9 */
            port p_CX_3 : ~P_CX_3;
            port p_CX_4 : P_CX_4;
        }
        part def T_REVIEWER {
            doc /* Independent evaluator
            Judges actual outcomes against task expectations.
            Record: REVIEWER
            Basis: derived; status: draft.
            Source: S8 */
            port p_CX_7 : ~P_CX_7;
            port p_CX_8 : P_CX_8;
        }
        action def T_OA_TASK {
            doc /* Achieve a requested outcome
            Use suitable guidance on actual user inputs.
            Record: OA_TASK
            Basis: derived; status: draft.
            Source: S5
            Source: S9 */
        }
        action def T_OA_PROVISION {
            doc /* Make guidance usable
            Provide discoverable and trusted packages within the host environment.
            Record: OA_PROVISION
            Basis: derived; status: draft.
            Source: S4
            Source: S5 */
        }
        action def T_OA_OPERATE {
            doc /* Carry out a bounded operation
            Execute a requested permitted operation and return evidence.
            Record: OA_OPERATE
            Basis: derived; status: draft.
            Source: S7
            Source: S9 */
        }
        action def T_OA_MAINTAIN {
            doc /* Improve reusable know-how
            Revise a method in response to new needs and observed failures.
            Record: OA_MAINTAIN
            Basis: derived; status: draft.
            Source: S6
            Source: S8
            Source: S11 */
        }
        action def T_OA_EVAL {
            doc /* Compare actual outcomes
            Judge candidate outputs independently of the authoring context.
            Record: OA_EVAL
            Basis: derived; status: draft.
            Source: S8 */
        }
        action def T_F_ROOT {
            doc /* Turn reusable guidance into useful work
            Connect task fulfillment to evidence-based improvement.
            Record: F_ROOT
            Basis: derived; status: draft.
            Source: S9
            Source: S11 */
        }
        action def T_F_DISCOVER {
            doc /* Discover usable packages
            Locate available packages under host discovery and trust policy.
            Record: F_DISCOVER
            Basis: derived; status: draft.
            Source: S4
            Source: S5 */
            out item out_X_0 : I_X_0;
            in item in_X_16 : I_X_16;
        }
        action def T_F_CATALOG {
            doc /* Expose names and descriptions
            Provide a compact catalogue rather than load all workflows.
            Record: F_CATALOG
            Basis: derived; status: draft.
            Source: S2
            Source: S3
            Source: S5 */
            in item in_X_0 : I_X_0;
            out item out_X_1 : I_X_1;
        }
        action def T_F_SELECT {
            doc /* Choose relevant guidance
            Use explicit selection or permitted description-based matching; a match may be absent.
            Record: F_SELECT
            Basis: derived; status: draft.
            Source: S5
            Source: S6 */
            in item in_X_1 : I_X_1;
            out item out_X_2 : I_X_2;
            out item out_X_PLAIN : I_X_PLAIN;
        }
        action def T_F_LOAD {
            doc /* Read selected workflow
            Bring the selected SKILL.md instructions into context.
            Record: F_LOAD
            Basis: derived; status: draft.
            Source: S3 */
            in item in_X_2 : I_X_2;
            out item out_X_3 : I_X_3;
        }
        action def T_F_PLAN {
            doc /* Interpret method for this task
            Apply instructions to intent, constraints and current evidence.
            Record: F_PLAN
            Basis: derived; status: draft.
            Source: S9 */
            in item in_X_3 : I_X_3;
            in item in_X_4 : I_X_4;
            out item out_X_6 : I_X_6;
            out item out_X_17 : I_X_17;
        }
        action def T_F_REFERENCE {
            doc /* Read relevant reference
            Load only detail needed for the current task.
            Record: F_REFERENCE
            Basis: derived; status: draft.
            Source: S2
            Source: S3 */
            out item out_X_4 : I_X_4;
        }
        action def T_F_ASSET {
            doc /* Use relevant template
            Adapt an output resource to current evidence.
            Record: F_ASSET
            Basis: derived; status: draft.
            Source: S2
            Source: S9 */
            out item out_X_5 : I_X_5;
        }
        action def T_F_GATE {
            doc /* Check execution prerequisites
            Separate permission, available tool and dependency checks from skill selection.
            Record: F_GATE
            Basis: derived; status: draft.
            Source: S7
            Source: S9 */
            in item in_X_6 : I_X_6;
            out item out_X_7 : I_X_7;
            out item out_X_BLOCK : I_X_BLOCK;
        }
        action def T_F_CALL {
            doc /* Request permitted operation
            Use an existing tool or optional script with explicit inputs.
            Record: F_CALL
            Basis: derived; status: draft.
            Source: S7
            Source: S9 */
            in item in_X_7 : I_X_7;
            out item out_X_8 : I_X_8;
        }
        action def T_F_RESULT {
            doc /* Inspect returned result
            Read outputs, errors and artifacts rather than assume success.
            Record: F_RESULT
            Basis: derived; status: draft.
            Source: S7
            Source: S9 */
            in item in_X_8 : I_X_8;
            out item out_X_9 : I_X_9;
        }
        action def T_F_VERIFY {
            doc /* Check the actual outcome
            Check expected meaning and observable output before delivery.
            Record: F_VERIFY
            Basis: derived; status: draft.
            Source: S8
            Source: S10 */
            in item in_X_9 : I_X_9;
            out item out_X_10 : I_X_10;
            in item in_X_21 : I_X_21;
        }
        action def T_F_ANSWER {
            doc /* Deliver the grounded result
            Return the outcome supported by available evidence.
            Record: F_ANSWER
            Basis: derived; status: draft.
            Source: S9
            Source: S10 */
            in item in_X_10 : I_X_10;
        }
        action def T_F_PLAIN {
            doc /* Proceed without this skill
            Continue normally when no suitable available guidance applies.
            Record: F_PLAIN
            Basis: derived; status: draft.
            Source: S5
            Source: S9 */
            in item in_X_PLAIN : I_X_PLAIN;
        }
        action def T_F_BLOCK {
            doc /* Retain unresolved outcome
            Explain a specific blocker or use a permitted alternative without claiming completion.
            Record: F_BLOCK
            Basis: derived; status: draft.
            Source: S9 */
            in item in_X_BLOCK : I_X_BLOCK;
        }
        action def T_F_DRAFT {
            doc /* Draft a focused revision
            Specify purpose, triggers, inputs, method and outputs.
            Record: F_DRAFT
            Basis: derived; status: draft.
            Source: S6
            Source: S11 */
            out item out_X_11 : I_X_11;
        }
        action def T_F_TRIAL {
            doc /* Run comparable tasks
            Use realistic prompts and negative cases for candidate and baseline.
            Record: F_TRIAL
            Basis: derived; status: draft.
            Source: S8 */
            in item in_X_11 : I_X_11;
            out item out_X_12 : I_X_12;
            in item in_X_14 : I_X_14;
        }
        action def T_F_COMPARE {
            doc /* Compare observed outputs
            Combine behavioral assertions with human quality judgment.
            Record: F_COMPARE
            Basis: derived; status: draft.
            Source: S8 */
            in item in_X_12 : I_X_12;
            out item out_X_13 : I_X_13;
            out item out_X_15 : I_X_15;
        }
        action def T_F_REVISE {
            doc /* Repair observed weaknesses
            Change the method based on actual failure evidence.
            Record: F_REVISE
            Basis: derived; status: draft.
            Source: S8
            Source: S11 */
            in item in_X_13 : I_X_13;
            out item out_X_14 : I_X_14;
        }
        action def T_F_RELEASE {
            doc /* Record evaluated baseline
            Promote the reviewed candidate while retaining its evidence and predecessor.
            Record: F_RELEASE
            Basis: derived; status: draft.
            Source: S11 */
            in item in_X_15 : I_X_15;
            out item out_X_16 : I_X_16;
        }
        action def T_F_INTERPRET {
            doc /* Interpret source into model assertions
            Identify source entities, responsibilities, exchanges and lifecycle conditions.
            Record: F_INTERPRET
            Basis: derived; status: draft.
            Source: S10 */
            in item in_X_17 : I_X_17;
            out item out_X_18 : I_X_18;
        }
        action def T_F_MODEL {
            doc /* Author candidate SysML
            Express sourced meaning and distinguish engineering assumptions.
            Record: F_MODEL
            Basis: derived; status: draft.
            Source: S10 */
            in item in_X_18 : I_X_18;
            out item out_X_19 : I_X_19;
        }
        action def T_F_QUALIFY {
            doc /* Check native model relationships
            Run the available native checker against the exact candidate.
            Record: F_QUALIFY
            Basis: derived; status: draft.
            Source: S10 */
            in item in_X_19 : I_X_19;
            out item out_X_20 : I_X_20;
        }
        action def T_F_RENDER {
            doc /* Build model-backed HTML views
            Project the same model into question-led views.
            Record: F_RENDER
            Basis: derived; status: draft.
            Source: S10 */
            in item in_X_5 : I_X_5;
            in item in_X_20 : I_X_20;
            out item out_X_21 : I_X_21;
        }
        part def T_LC_ROOT {
            doc /* Skill-enabled work system
            Teaching boundary connecting reusable guidance, task application and improvement.
            Record: LC_ROOT
            Basis: derived; status: draft.
            Source: S9
            Source: S11 */
        }
        part def T_LC_REASON {
            doc /* Agent interpretation
            Turns intent and guidance into task-specific decisions.
            Record: LC_REASON
            Basis: derived; status: draft.
            Source: S9 */
            port p_X_1 : ~P_X_1;
            port p_X_2 : P_X_2;
            port p_X_3 : ~P_X_3;
            port p_X_4 : ~P_X_4;
            port p_X_5 : P_X_5;
            port p_X_6 : P_X_6;
            port p_X_10 : ~P_X_10;
            port p_X_19 : P_X_19;
            port p_CX_0 : ~P_CX_0;
            port p_CX_5 : P_CX_5;
        }
        part def T_LC_CONTEXT {
            doc /* Working context
            Contains the currently relevant instructions and evidence, not every installed file.
            Record: LC_CONTEXT
            Basis: derived; status: draft.
            Source: S3 */
            port p_X_1 : P_X_1;
            port p_X_2 : ~P_X_2;
            port p_X_3 : P_X_3;
            port p_X_4 : P_X_4;
            port p_X_16 : ~P_X_16;
        }
        part def T_LC_PACKAGE {
            doc /* Skill package
            Reusable authored content; not an autonomous worker.
            Record: LC_PACKAGE
            Basis: derived; status: draft.
            Source: S1
            Source: S2 */
            port p_CX_1 : ~P_CX_1;
        }
        part def T_LC_META {
            doc /* Name and description
            Discovery and matching metadata.
            Record: LC_META
            Basis: derived; status: draft.
            Source: S2
            Source: S3 */
        }
        part def T_LC_METHOD {
            doc /* SKILL.md workflow
            Task method read after selection.
            Record: LC_METHOD
            Basis: derived; status: draft.
            Source: S2
            Source: S3 */
        }
        part def T_LC_REF {
            doc /* References
            Detailed knowledge read on demand.
            Record: LC_REF
            Basis: derived; status: draft.
            Source: S2
            Source: S3 */
        }
        part def T_LC_SCRIPT {
            doc /* Scripts
            Optional repeatable executable helpers.
            Record: LC_SCRIPT
            Basis: derived; status: draft.
            Source: S2
            Source: S7 */
        }
        part def T_LC_ASSET {
            doc /* Assets
            Reusable templates and output material.
            Record: LC_ASSET
            Basis: derived; status: draft.
            Source: S2 */
        }
        part def T_LC_EXEC {
            doc /* Execution coordination
            Requests operations and interprets their outcomes.
            Record: LC_EXEC
            Basis: derived; status: draft.
            Source: S7
            Source: S9 */
            port p_X_5 : ~P_X_5;
            port p_X_6 : ~P_X_6;
            port p_X_9 : P_X_9;
            port p_X_19 : ~P_X_19;
            port p_X_21 : P_X_21;
            port p_CX_2 : ~P_CX_2;
            port p_CX_3 : P_CX_3;
            port p_CX_4 : ~P_CX_4;
        }
        part def T_LC_ASSURE {
            doc /* Outcome assurance
            Checks source meaning and observable output.
            Record: LC_ASSURE
            Basis: derived; status: draft.
            Source: S8
            Source: S10 */
            port p_X_9 : ~P_X_9;
            port p_X_10 : P_X_10;
            port p_X_11 : ~P_X_11;
            port p_X_13 : P_X_13;
            port p_X_14 : ~P_X_14;
            port p_X_15 : P_X_15;
            port p_X_21 : ~P_X_21;
            port p_CX_7 : P_CX_7;
            port p_CX_8 : ~P_CX_8;
        }
        part def T_LC_MAINTAIN {
            doc /* Skill evolution
            Compares candidate revisions and retains the released baseline.
            Record: LC_MAINTAIN
            Basis: derived; status: draft.
            Source: S8
            Source: S11 */
            port p_X_11 : P_X_11;
            port p_X_13 : ~P_X_13;
            port p_X_14 : P_X_14;
            port p_X_15 : ~P_X_15;
            port p_X_16 : P_X_16;
            port p_CX_6 : ~P_CX_6;
        }
        port def P_X_1 {
            out item payload : I_X_1;
        }
        interface def IF_X_1 {
            end sender : P_X_1;
            end receiver : ~P_X_1;
            flow of I_X_1 from sender.payload to receiver.payload;
        }
        port def P_X_2 {
            out item payload : I_X_2;
        }
        interface def IF_X_2 {
            end sender : P_X_2;
            end receiver : ~P_X_2;
            flow of I_X_2 from sender.payload to receiver.payload;
        }
        port def P_X_3 {
            out item payload : I_X_3;
        }
        interface def IF_X_3 {
            end sender : P_X_3;
            end receiver : ~P_X_3;
            flow of I_X_3 from sender.payload to receiver.payload;
        }
        port def P_X_4 {
            out item payload : I_X_4;
        }
        interface def IF_X_4 {
            end sender : P_X_4;
            end receiver : ~P_X_4;
            flow of I_X_4 from sender.payload to receiver.payload;
        }
        port def P_X_5 {
            out item payload : I_X_5;
        }
        interface def IF_X_5 {
            end sender : P_X_5;
            end receiver : ~P_X_5;
            flow of I_X_5 from sender.payload to receiver.payload;
        }
        port def P_X_6 {
            out item payload : I_X_6;
        }
        interface def IF_X_6 {
            end sender : P_X_6;
            end receiver : ~P_X_6;
            flow of I_X_6 from sender.payload to receiver.payload;
        }
        port def P_X_9 {
            out item payload : I_X_9;
        }
        interface def IF_X_9 {
            end sender : P_X_9;
            end receiver : ~P_X_9;
            flow of I_X_9 from sender.payload to receiver.payload;
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
        port def P_X_13 {
            out item payload : I_X_13;
        }
        interface def IF_X_13 {
            end sender : P_X_13;
            end receiver : ~P_X_13;
            flow of I_X_13 from sender.payload to receiver.payload;
        }
        port def P_X_14 {
            out item payload : I_X_14;
        }
        interface def IF_X_14 {
            end sender : P_X_14;
            end receiver : ~P_X_14;
            flow of I_X_14 from sender.payload to receiver.payload;
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
        port def P_X_19 {
            out item payload : I_X_19;
        }
        interface def IF_X_19 {
            end sender : P_X_19;
            end receiver : ~P_X_19;
            flow of I_X_19 from sender.payload to receiver.payload;
        }
        port def P_X_21 {
            out item payload : I_X_21;
        }
        interface def IF_X_21 {
            end sender : P_X_21;
            end receiver : ~P_X_21;
            flow of I_X_21 from sender.payload to receiver.payload;
        }
        port def P_CX_0 {
            out item payload : I_CX_0;
        }
        interface def IF_CX_0 {
            end sender : P_CX_0;
            end receiver : ~P_CX_0;
            flow of I_CX_0 from sender.payload to receiver.payload;
        }
        port def P_CX_1 {
            out item payload : I_CX_1;
        }
        interface def IF_CX_1 {
            end sender : P_CX_1;
            end receiver : ~P_CX_1;
            flow of I_CX_1 from sender.payload to receiver.payload;
        }
        port def P_CX_2 {
            out item payload : I_CX_2;
        }
        interface def IF_CX_2 {
            end sender : P_CX_2;
            end receiver : ~P_CX_2;
            flow of I_CX_2 from sender.payload to receiver.payload;
        }
        port def P_CX_3 {
            out item payload : I_CX_3;
        }
        interface def IF_CX_3 {
            end sender : P_CX_3;
            end receiver : ~P_CX_3;
            flow of I_CX_3 from sender.payload to receiver.payload;
        }
        port def P_CX_4 {
            out item payload : I_CX_4;
        }
        interface def IF_CX_4 {
            end sender : P_CX_4;
            end receiver : ~P_CX_4;
            flow of I_CX_4 from sender.payload to receiver.payload;
        }
        port def P_CX_5 {
            out item payload : I_CX_5;
        }
        interface def IF_CX_5 {
            end sender : P_CX_5;
            end receiver : ~P_CX_5;
            flow of I_CX_5 from sender.payload to receiver.payload;
        }
        port def P_CX_6 {
            out item payload : I_CX_6;
        }
        interface def IF_CX_6 {
            end sender : P_CX_6;
            end receiver : ~P_CX_6;
            flow of I_CX_6 from sender.payload to receiver.payload;
        }
        port def P_CX_7 {
            out item payload : I_CX_7;
        }
        interface def IF_CX_7 {
            end sender : P_CX_7;
            end receiver : ~P_CX_7;
            flow of I_CX_7 from sender.payload to receiver.payload;
        }
        port def P_CX_8 {
            out item payload : I_CX_8;
        }
        interface def IF_CX_8 {
            end sender : P_CX_8;
            end receiver : ~P_CX_8;
            flow of I_CX_8 from sender.payload to receiver.payload;
        }
        item def Event_SM_REVISION_ST1 {
            doc /* Candidate frozen */
        }
        item def Event_SM_REVISION_ST2 {
            doc /* Regression found */
        }
        item def Event_SM_REVISION_ST3 {
            doc /* Review completed */
        }
        item def Event_SM_REVISION_ST4 {
            doc /* Replacement accepted */
        }
        state def T_SM_REVISION {
            doc /* A skill revision is not automatically a release
            Proposed lifecycle of an identified revision; prior released revision remains usable while the candidate is evaluated.
            Record: SM_REVISION
            Basis: proposed; status: proposed.
            Source: S11
            Lifecycle policy: ongoing
            Terminal states: retired
            Lifecycle exit condition: An identified revision can be retired; future revisions have their own evidence.
            Transition effects below are retained obligations, not executed effects. */
            entry;
            then draft;
            state draft {
                doc /* Draft */
            }
            state evaluating {
                doc /* Under evaluation */
            }
            state released {
                doc /* Released baseline */
            }
            state retired {
                doc /* Retired */
            }
            attribute g_ST1 : Boolean {
                doc /* Review predicate, not an evaluated value: Test tasks and baseline identified */
            }
            transition ST1 first draft accept Event_SM_REVISION_ST1 if g_ST1 then evaluating {
                doc /* Effect/obligation: Collect candidate-specific evidence */
            }
            attribute g_ST2 : Boolean {
                doc /* Review predicate, not an evaluated value: Outcome fails intended expectation */
            }
            transition ST2 first evaluating accept Event_SM_REVISION_ST2 if g_ST2 then draft {
                doc /* Effect/obligation: Revise candidate */
            }
            attribute g_ST3 : Boolean {
                doc /* Review predicate, not an evaluated value: Evidence supports release */
            }
            transition ST3 first evaluating accept Event_SM_REVISION_ST3 if g_ST3 then released {
                doc /* Effect/obligation: Record exact released revision */
            }
            attribute g_ST4 : Boolean {
                doc /* Review predicate, not an evaluated value: New revision independently evaluated */
            }
            transition ST4 first released accept Event_SM_REVISION_ST4 if g_ST4 then retired {
                doc /* Effect/obligation: Retain historical evidence */
            }
            transition finish_retired first retired then done;
        }
    }
    package Operational {
        action activities {
            action OA_TASK : Types::T_OA_TASK {
                doc /* Achieve a requested outcome
                Use suitable guidance on actual user inputs.
                Record: OA_TASK
                Basis: derived; status: draft.
                Source: S5
                Source: S9 */
            }
            action OA_PROVISION : Types::T_OA_PROVISION {
                doc /* Make guidance usable
                Provide discoverable and trusted packages within the host environment.
                Record: OA_PROVISION
                Basis: derived; status: draft.
                Source: S4
                Source: S5 */
            }
            action OA_OPERATE : Types::T_OA_OPERATE {
                doc /* Carry out a bounded operation
                Execute a requested permitted operation and return evidence.
                Record: OA_OPERATE
                Basis: derived; status: draft.
                Source: S7
                Source: S9 */
            }
            action OA_MAINTAIN : Types::T_OA_MAINTAIN {
                doc /* Improve reusable know-how
                Revise a method in response to new needs and observed failures.
                Record: OA_MAINTAIN
                Basis: derived; status: draft.
                Source: S6
                Source: S8
                Source: S11 */
            }
            action OA_EVAL : Types::T_OA_EVAL {
                doc /* Compare actual outcomes
                Judge candidate outputs independently of the authoring context.
                Record: OA_EVAL
                Basis: derived; status: draft.
                Source: S8 */
            }
        }
        part context {
            ref part USER : Types::T_USER {
                doc /* Task owner
                Supplies intent, inputs and decisions.
                Record: USER
                Basis: derived; status: draft.
                Source: S5
                Source: S9 */
                perform activities.OA_TASK;
            }
            ref part AUTHOR : Types::T_AUTHOR {
                doc /* Skill maintainer
                Curates focused methods and tests candidate revisions.
                Record: AUTHOR
                Basis: derived; status: draft.
                Source: S6
                Source: S8 */
                perform activities.OA_MAINTAIN;
            }
            ref part HOST : Types::T_HOST {
                doc /* Host runtime
                Discovers accessible packages and mediates access and execution.
                Record: HOST
                Basis: derived; status: draft.
                Source: S4
                Source: S5
                Source: S9 */
                perform activities.OA_PROVISION;
            }
            ref part TOOLS : Types::T_TOOLS {
                doc /* Execution tools
                Return operation results, artifacts or errors.
                Record: TOOLS
                Basis: derived; status: draft.
                Source: S7
                Source: S9 */
                perform activities.OA_OPERATE;
            }
            ref part REVIEWER : Types::T_REVIEWER {
                doc /* Independent evaluator
                Judges actual outcomes against task expectations.
                Record: REVIEWER
                Basis: derived; status: draft.
                Source: S8 */
                perform activities.OA_EVAL;
            }
        }
    }
    package System {
        action functions {
            action F_ROOT : Types::T_F_ROOT {
                doc /* Turn reusable guidance into useful work
                Connect task fulfillment to evidence-based improvement.
                Record: F_ROOT
                Basis: derived; status: draft.
                Source: S9
                Source: S11 */
                action F_DISCOVER : Types::T_F_DISCOVER {
                    doc /* Discover usable packages
                    Locate available packages under host discovery and trust policy.
                    Record: F_DISCOVER
                    Basis: derived; status: draft.
                    Source: S4
                    Source: S5 */
                }
                action F_CATALOG : Types::T_F_CATALOG {
                    doc /* Expose names and descriptions
                    Provide a compact catalogue rather than load all workflows.
                    Record: F_CATALOG
                    Basis: derived; status: draft.
                    Source: S2
                    Source: S3
                    Source: S5 */
                }
                action F_SELECT : Types::T_F_SELECT {
                    doc /* Choose relevant guidance
                    Use explicit selection or permitted description-based matching; a match may be absent.
                    Record: F_SELECT
                    Basis: derived; status: draft.
                    Source: S5
                    Source: S6 */
                }
                action F_LOAD : Types::T_F_LOAD {
                    doc /* Read selected workflow
                    Bring the selected SKILL.md instructions into context.
                    Record: F_LOAD
                    Basis: derived; status: draft.
                    Source: S3 */
                }
                action F_PLAN : Types::T_F_PLAN {
                    doc /* Interpret method for this task
                    Apply instructions to intent, constraints and current evidence.
                    Record: F_PLAN
                    Basis: derived; status: draft.
                    Source: S9 */
                }
                action F_REFERENCE : Types::T_F_REFERENCE {
                    doc /* Read relevant reference
                    Load only detail needed for the current task.
                    Record: F_REFERENCE
                    Basis: derived; status: draft.
                    Source: S2
                    Source: S3 */
                }
                action F_ASSET : Types::T_F_ASSET {
                    doc /* Use relevant template
                    Adapt an output resource to current evidence.
                    Record: F_ASSET
                    Basis: derived; status: draft.
                    Source: S2
                    Source: S9 */
                }
                action F_GATE : Types::T_F_GATE {
                    doc /* Check execution prerequisites
                    Separate permission, available tool and dependency checks from skill selection.
                    Record: F_GATE
                    Basis: derived; status: draft.
                    Source: S7
                    Source: S9 */
                }
                action F_CALL : Types::T_F_CALL {
                    doc /* Request permitted operation
                    Use an existing tool or optional script with explicit inputs.
                    Record: F_CALL
                    Basis: derived; status: draft.
                    Source: S7
                    Source: S9 */
                }
                action F_RESULT : Types::T_F_RESULT {
                    doc /* Inspect returned result
                    Read outputs, errors and artifacts rather than assume success.
                    Record: F_RESULT
                    Basis: derived; status: draft.
                    Source: S7
                    Source: S9 */
                }
                action F_VERIFY : Types::T_F_VERIFY {
                    doc /* Check the actual outcome
                    Check expected meaning and observable output before delivery.
                    Record: F_VERIFY
                    Basis: derived; status: draft.
                    Source: S8
                    Source: S10 */
                }
                action F_ANSWER : Types::T_F_ANSWER {
                    doc /* Deliver the grounded result
                    Return the outcome supported by available evidence.
                    Record: F_ANSWER
                    Basis: derived; status: draft.
                    Source: S9
                    Source: S10 */
                }
                action F_PLAIN : Types::T_F_PLAIN {
                    doc /* Proceed without this skill
                    Continue normally when no suitable available guidance applies.
                    Record: F_PLAIN
                    Basis: derived; status: draft.
                    Source: S5
                    Source: S9 */
                }
                action F_BLOCK : Types::T_F_BLOCK {
                    doc /* Retain unresolved outcome
                    Explain a specific blocker or use a permitted alternative without claiming completion.
                    Record: F_BLOCK
                    Basis: derived; status: draft.
                    Source: S9 */
                }
                action F_DRAFT : Types::T_F_DRAFT {
                    doc /* Draft a focused revision
                    Specify purpose, triggers, inputs, method and outputs.
                    Record: F_DRAFT
                    Basis: derived; status: draft.
                    Source: S6
                    Source: S11 */
                }
                action F_TRIAL : Types::T_F_TRIAL {
                    doc /* Run comparable tasks
                    Use realistic prompts and negative cases for candidate and baseline.
                    Record: F_TRIAL
                    Basis: derived; status: draft.
                    Source: S8 */
                }
                action F_COMPARE : Types::T_F_COMPARE {
                    doc /* Compare observed outputs
                    Combine behavioral assertions with human quality judgment.
                    Record: F_COMPARE
                    Basis: derived; status: draft.
                    Source: S8 */
                }
                action F_REVISE : Types::T_F_REVISE {
                    doc /* Repair observed weaknesses
                    Change the method based on actual failure evidence.
                    Record: F_REVISE
                    Basis: derived; status: draft.
                    Source: S8
                    Source: S11 */
                }
                action F_RELEASE : Types::T_F_RELEASE {
                    doc /* Record evaluated baseline
                    Promote the reviewed candidate while retaining its evidence and predecessor.
                    Record: F_RELEASE
                    Basis: derived; status: draft.
                    Source: S11 */
                }
                action F_INTERPRET : Types::T_F_INTERPRET {
                    doc /* Interpret source into model assertions
                    Identify source entities, responsibilities, exchanges and lifecycle conditions.
                    Record: F_INTERPRET
                    Basis: derived; status: draft.
                    Source: S10 */
                }
                action F_MODEL : Types::T_F_MODEL {
                    doc /* Author candidate SysML
                    Express sourced meaning and distinguish engineering assumptions.
                    Record: F_MODEL
                    Basis: derived; status: draft.
                    Source: S10 */
                }
                action F_QUALIFY : Types::T_F_QUALIFY {
                    doc /* Check native model relationships
                    Run the available native checker against the exact candidate.
                    Record: F_QUALIFY
                    Basis: derived; status: draft.
                    Source: S10 */
                }
                action F_RENDER : Types::T_F_RENDER {
                    doc /* Build model-backed HTML views
                    Project the same model into question-led views.
                    Record: F_RENDER
                    Basis: derived; status: draft.
                    Source: S10 */
                }
            }
        }
        flow X_0 of Types::I_X_0 from functions.F_ROOT.F_DISCOVER.out_X_0 to functions.F_ROOT.F_CATALOG.in_X_0 {
            doc /* Available package identity
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_0
            Basis: derived; status: draft.
            Source: S4
            Applicability: Applicable to the current task or revision */
        }
        flow X_1 of Types::I_X_1 from functions.F_ROOT.F_CATALOG.out_X_1 to functions.F_ROOT.F_SELECT.in_X_1 {
            doc /* Names and descriptions
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_1
            Basis: derived; status: draft.
            Source: S3
            Applicability: Applicable to the current task or revision */
        }
        flow X_2 of Types::I_X_2 from functions.F_ROOT.F_SELECT.out_X_2 to functions.F_ROOT.F_LOAD.in_X_2 {
            doc /* Selected package identity
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_2
            Basis: derived; status: draft.
            Source: S5
            Applicability: Applicable to the current task or revision */
        }
        flow X_3 of Types::I_X_3 from functions.F_ROOT.F_LOAD.out_X_3 to functions.F_ROOT.F_PLAN.in_X_3 {
            doc /* Workflow instructions
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_3
            Basis: derived; status: draft.
            Source: S3
            Applicability: Applicable to the current task or revision */
        }
        flow X_4 of Types::I_X_4 from functions.F_ROOT.F_REFERENCE.out_X_4 to functions.F_ROOT.F_PLAN.in_X_4 {
            doc /* Relevant domain detail
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_4
            Basis: derived; status: draft.
            Source: S3
            Applicability: Applicable to the current task or revision */
        }
        flow X_5 of Types::I_X_5 from functions.F_ROOT.F_ASSET.out_X_5 to functions.F_ROOT.F_RENDER.in_X_5 {
            doc /* Chosen template
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_5
            Basis: derived; status: draft.
            Source: S2
            Source: S10
            Applicability: Applicable to the current task or revision */
        }
        flow X_6 of Types::I_X_6 from functions.F_ROOT.F_PLAN.out_X_6 to functions.F_ROOT.F_GATE.in_X_6 {
            doc /* Proposed operation and inputs
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_6
            Basis: derived; status: draft.
            Source: S9
            Applicability: Applicable to the current task or revision */
        }
        flow X_7 of Types::I_X_7 from functions.F_ROOT.F_GATE.out_X_7 to functions.F_ROOT.F_CALL.in_X_7 {
            doc /* Permitted operation with prerequisites
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_7
            Basis: derived; status: draft.
            Source: S9
            Applicability: Applicable to the current task or revision */
        }
        flow X_8 of Types::I_X_8 from functions.F_ROOT.F_CALL.out_X_8 to functions.F_ROOT.F_RESULT.in_X_8 {
            doc /* Operation identity
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_8
            Basis: derived; status: draft.
            Source: S7
            Applicability: Applicable to the current task or revision */
        }
        flow X_9 of Types::I_X_9 from functions.F_ROOT.F_RESULT.out_X_9 to functions.F_ROOT.F_VERIFY.in_X_9 {
            doc /* Artifact or error evidence
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_9
            Basis: derived; status: draft.
            Source: S7
            Source: S9
            Applicability: Applicable to the current task or revision */
        }
        flow X_10 of Types::I_X_10 from functions.F_ROOT.F_VERIFY.out_X_10 to functions.F_ROOT.F_ANSWER.in_X_10 {
            doc /* Reviewed outcome
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_10
            Basis: derived; status: draft.
            Source: S9
            Applicability: Applicable to the current task or revision */
        }
        flow X_11 of Types::I_X_11 from functions.F_ROOT.F_DRAFT.out_X_11 to functions.F_ROOT.F_TRIAL.in_X_11 {
            doc /* Candidate and baseline revisions
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_11
            Basis: derived; status: draft.
            Source: S8
            Applicability: Applicable to the current task or revision */
        }
        flow X_12 of Types::I_X_12 from functions.F_ROOT.F_TRIAL.out_X_12 to functions.F_ROOT.F_COMPARE.in_X_12 {
            doc /* Observed paired results
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_12
            Basis: derived; status: draft.
            Source: S8
            Applicability: Applicable to the current task or revision */
        }
        flow X_13 of Types::I_X_13 from functions.F_ROOT.F_COMPARE.out_X_13 to functions.F_ROOT.F_REVISE.in_X_13 {
            doc /* Failure evidence
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_13
            Basis: derived; status: draft.
            Source: S8
            Applicability: Applicable to the current task or revision */
        }
        flow X_14 of Types::I_X_14 from functions.F_ROOT.F_REVISE.out_X_14 to functions.F_ROOT.F_TRIAL.in_X_14 {
            doc /* Revised candidate
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_14
            Basis: derived; status: draft.
            Source: S8
            Source: S11
            Applicability: Applicable to the current task or revision */
        }
        flow X_15 of Types::I_X_15 from functions.F_ROOT.F_COMPARE.out_X_15 to functions.F_ROOT.F_RELEASE.in_X_15 {
            doc /* Candidate evaluation evidence
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_15
            Basis: derived; status: draft.
            Source: S11
            Applicability: Applicable to the current task or revision */
        }
        flow X_16 of Types::I_X_16 from functions.F_ROOT.F_RELEASE.out_X_16 to functions.F_ROOT.F_DISCOVER.in_X_16 {
            doc /* Released package
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_16
            Basis: derived; status: draft.
            Source: S11
            Applicability: Applicable to the current task or revision */
        }
        flow X_17 of Types::I_X_17 from functions.F_ROOT.F_PLAN.out_X_17 to functions.F_ROOT.F_INTERPRET.in_X_17 {
            doc /* Task and source brief
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_17
            Basis: derived; status: draft.
            Source: S10
            Applicability: Applicable to the current task or revision */
        }
        flow X_18 of Types::I_X_18 from functions.F_ROOT.F_INTERPRET.out_X_18 to functions.F_ROOT.F_MODEL.in_X_18 {
            doc /* Source-linked model assertions
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_18
            Basis: derived; status: draft.
            Source: S10
            Applicability: Applicable to the current task or revision */
        }
        flow X_19 of Types::I_X_19 from functions.F_ROOT.F_MODEL.out_X_19 to functions.F_ROOT.F_QUALIFY.in_X_19 {
            doc /* Candidate native model
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_19
            Basis: derived; status: draft.
            Source: S10
            Applicability: Applicable to the current task or revision */
        }
        flow X_20 of Types::I_X_20 from functions.F_ROOT.F_QUALIFY.out_X_20 to functions.F_ROOT.F_RENDER.in_X_20 {
            doc /* Qualified model and report
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_20
            Basis: derived; status: draft.
            Source: S10
            Applicability: Applicable to the current task or revision */
        }
        flow X_21 of Types::I_X_21 from functions.F_ROOT.F_RENDER.out_X_21 to functions.F_ROOT.F_VERIFY.in_X_21 {
            doc /* HTML views and model bindings
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_21
            Basis: derived; status: draft.
            Source: S10
            Applicability: Applicable to the current task or revision */
        }
        flow X_PLAIN of Types::I_X_PLAIN from functions.F_ROOT.F_SELECT.out_X_PLAIN to functions.F_ROOT.F_PLAIN.in_X_PLAIN {
            doc /* No matching available skill
            Alternative outcome retained explicitly.
            Record: X_PLAIN
            Basis: derived; status: draft.
            Source: S5
            Source: S9
            Applicability: The named alternative applies */
        }
        flow X_BLOCK of Types::I_X_BLOCK from functions.F_ROOT.F_GATE.out_X_BLOCK to functions.F_ROOT.F_BLOCK.in_X_BLOCK {
            doc /* Unavailable prerequisite or permission
            Alternative outcome retained explicitly.
            Record: X_BLOCK
            Basis: derived; status: draft.
            Source: S9
            Applicability: The named alternative applies */
        }
    }
    package Logical {
        part architecture {
            part LC_ROOT : Types::T_LC_ROOT {
                doc /* Skill-enabled work system
                Teaching boundary connecting reusable guidance, task application and improvement.
                Record: LC_ROOT
                Basis: derived; status: draft.
                Source: S9
                Source: S11 */
                part LC_REASON : Types::T_LC_REASON {
                    doc /* Agent interpretation
                    Turns intent and guidance into task-specific decisions.
                    Record: LC_REASON
                    Basis: derived; status: draft.
                    Source: S9 */
                }
                part LC_CONTEXT : Types::T_LC_CONTEXT {
                    doc /* Working context
                    Contains the currently relevant instructions and evidence, not every installed file.
                    Record: LC_CONTEXT
                    Basis: derived; status: draft.
                    Source: S3 */
                }
                part LC_PACKAGE : Types::T_LC_PACKAGE {
                    doc /* Skill package
                    Reusable authored content; not an autonomous worker.
                    Record: LC_PACKAGE
                    Basis: derived; status: draft.
                    Source: S1
                    Source: S2 */
                    part LC_META : Types::T_LC_META {
                        doc /* Name and description
                        Discovery and matching metadata.
                        Record: LC_META
                        Basis: derived; status: draft.
                        Source: S2
                        Source: S3 */
                    }
                    part LC_METHOD : Types::T_LC_METHOD {
                        doc /* SKILL.md workflow
                        Task method read after selection.
                        Record: LC_METHOD
                        Basis: derived; status: draft.
                        Source: S2
                        Source: S3 */
                    }
                    part LC_REF : Types::T_LC_REF {
                        doc /* References
                        Detailed knowledge read on demand.
                        Record: LC_REF
                        Basis: derived; status: draft.
                        Source: S2
                        Source: S3 */
                    }
                    part LC_SCRIPT : Types::T_LC_SCRIPT {
                        doc /* Scripts
                        Optional repeatable executable helpers.
                        Record: LC_SCRIPT
                        Basis: derived; status: draft.
                        Source: S2
                        Source: S7 */
                    }
                    part LC_ASSET : Types::T_LC_ASSET {
                        doc /* Assets
                        Reusable templates and output material.
                        Record: LC_ASSET
                        Basis: derived; status: draft.
                        Source: S2 */
                    }
                }
                part LC_EXEC : Types::T_LC_EXEC {
                    doc /* Execution coordination
                    Requests operations and interprets their outcomes.
                    Record: LC_EXEC
                    Basis: derived; status: draft.
                    Source: S7
                    Source: S9 */
                }
                part LC_ASSURE : Types::T_LC_ASSURE {
                    doc /* Outcome assurance
                    Checks source meaning and observable output.
                    Record: LC_ASSURE
                    Basis: derived; status: draft.
                    Source: S8
                    Source: S10 */
                }
                part LC_MAINTAIN : Types::T_LC_MAINTAIN {
                    doc /* Skill evolution
                    Compares candidate revisions and retains the released baseline.
                    Record: LC_MAINTAIN
                    Basis: derived; status: draft.
                    Source: S8
                    Source: S11 */
                    exhibit state SM_REVISION : Types::T_SM_REVISION;
                }
            }
        }
        interface IF_X_1 : Types::IF_X_1 connect architecture.LC_ROOT.LC_CONTEXT.p_X_1 to architecture.LC_ROOT.LC_REASON.p_X_1 {
            doc /* Names and descriptions
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_1
            Basis: derived; status: draft.
            Source: S3
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_2 : Types::IF_X_2 connect architecture.LC_ROOT.LC_REASON.p_X_2 to architecture.LC_ROOT.LC_CONTEXT.p_X_2 {
            doc /* Selected package identity
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_2
            Basis: derived; status: draft.
            Source: S5
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_3 : Types::IF_X_3 connect architecture.LC_ROOT.LC_CONTEXT.p_X_3 to architecture.LC_ROOT.LC_REASON.p_X_3 {
            doc /* Workflow instructions
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_3
            Basis: derived; status: draft.
            Source: S3
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_4 : Types::IF_X_4 connect architecture.LC_ROOT.LC_CONTEXT.p_X_4 to architecture.LC_ROOT.LC_REASON.p_X_4 {
            doc /* Relevant domain detail
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_4
            Basis: derived; status: draft.
            Source: S3
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_5 : Types::IF_X_5 connect architecture.LC_ROOT.LC_REASON.p_X_5 to architecture.LC_ROOT.LC_EXEC.p_X_5 {
            doc /* Chosen template
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_5
            Basis: derived; status: draft.
            Source: S2
            Source: S10
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_6 : Types::IF_X_6 connect architecture.LC_ROOT.LC_REASON.p_X_6 to architecture.LC_ROOT.LC_EXEC.p_X_6 {
            doc /* Proposed operation and inputs
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_6
            Basis: derived; status: draft.
            Source: S9
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_9 : Types::IF_X_9 connect architecture.LC_ROOT.LC_EXEC.p_X_9 to architecture.LC_ROOT.LC_ASSURE.p_X_9 {
            doc /* Artifact or error evidence
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_9
            Basis: derived; status: draft.
            Source: S7
            Source: S9
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_10 : Types::IF_X_10 connect architecture.LC_ROOT.LC_ASSURE.p_X_10 to architecture.LC_ROOT.LC_REASON.p_X_10 {
            doc /* Reviewed outcome
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_10
            Basis: derived; status: draft.
            Source: S9
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_11 : Types::IF_X_11 connect architecture.LC_ROOT.LC_MAINTAIN.p_X_11 to architecture.LC_ROOT.LC_ASSURE.p_X_11 {
            doc /* Candidate and baseline revisions
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_11
            Basis: derived; status: draft.
            Source: S8
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_13 : Types::IF_X_13 connect architecture.LC_ROOT.LC_ASSURE.p_X_13 to architecture.LC_ROOT.LC_MAINTAIN.p_X_13 {
            doc /* Failure evidence
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_13
            Basis: derived; status: draft.
            Source: S8
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_14 : Types::IF_X_14 connect architecture.LC_ROOT.LC_MAINTAIN.p_X_14 to architecture.LC_ROOT.LC_ASSURE.p_X_14 {
            doc /* Revised candidate
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_14
            Basis: derived; status: draft.
            Source: S8
            Source: S11
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_15 : Types::IF_X_15 connect architecture.LC_ROOT.LC_ASSURE.p_X_15 to architecture.LC_ROOT.LC_MAINTAIN.p_X_15 {
            doc /* Candidate evaluation evidence
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_15
            Basis: derived; status: draft.
            Source: S11
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_16 : Types::IF_X_16 connect architecture.LC_ROOT.LC_MAINTAIN.p_X_16 to architecture.LC_ROOT.LC_CONTEXT.p_X_16 {
            doc /* Released package
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_16
            Basis: derived; status: draft.
            Source: S11
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_19 : Types::IF_X_19 connect architecture.LC_ROOT.LC_REASON.p_X_19 to architecture.LC_ROOT.LC_EXEC.p_X_19 {
            doc /* Candidate native model
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_19
            Basis: derived; status: draft.
            Source: S10
            Derived logical contract from candidate primary function allocations. */
        }
        interface IF_X_21 : Types::IF_X_21 connect architecture.LC_ROOT.LC_EXEC.p_X_21 to architecture.LC_ROOT.LC_ASSURE.p_X_21 {
            doc /* HTML views and model bindings
            Potential information transfer; temporal conditions are in scenarios.
            Record: X_21
            Basis: derived; status: draft.
            Source: S10
            Derived logical contract from candidate primary function allocations. */
        }
    }
    allocation AL_F_DISCOVER allocate System::functions.F_ROOT.F_DISCOVER to Logical::architecture.LC_ROOT.LC_CONTEXT {
        doc /* Discover usable packages
        Locate available packages under host discovery and trust policy.
        Record: AL_F_DISCOVER
        Basis: derived; status: draft.
        Source: S4
        Source: S5
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_CATALOG allocate System::functions.F_ROOT.F_CATALOG to Logical::architecture.LC_ROOT.LC_CONTEXT {
        doc /* Expose names and descriptions
        Provide a compact catalogue rather than load all workflows.
        Record: AL_F_CATALOG
        Basis: derived; status: draft.
        Source: S2
        Source: S3
        Source: S5
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_SELECT allocate System::functions.F_ROOT.F_SELECT to Logical::architecture.LC_ROOT.LC_REASON {
        doc /* Choose relevant guidance
        Use explicit selection or permitted description-based matching; a match may be absent.
        Record: AL_F_SELECT
        Basis: derived; status: draft.
        Source: S5
        Source: S6
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_LOAD allocate System::functions.F_ROOT.F_LOAD to Logical::architecture.LC_ROOT.LC_CONTEXT {
        doc /* Read selected workflow
        Bring the selected SKILL.md instructions into context.
        Record: AL_F_LOAD
        Basis: derived; status: draft.
        Source: S3
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_PLAN allocate System::functions.F_ROOT.F_PLAN to Logical::architecture.LC_ROOT.LC_REASON {
        doc /* Interpret method for this task
        Apply instructions to intent, constraints and current evidence.
        Record: AL_F_PLAN
        Basis: derived; status: draft.
        Source: S9
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_REFERENCE allocate System::functions.F_ROOT.F_REFERENCE to Logical::architecture.LC_ROOT.LC_CONTEXT {
        doc /* Read relevant reference
        Load only detail needed for the current task.
        Record: AL_F_REFERENCE
        Basis: derived; status: draft.
        Source: S2
        Source: S3
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_ASSET allocate System::functions.F_ROOT.F_ASSET to Logical::architecture.LC_ROOT.LC_REASON {
        doc /* Use relevant template
        Adapt an output resource to current evidence.
        Record: AL_F_ASSET
        Basis: derived; status: draft.
        Source: S2
        Source: S9
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_GATE allocate System::functions.F_ROOT.F_GATE to Logical::architecture.LC_ROOT.LC_EXEC {
        doc /* Check execution prerequisites
        Separate permission, available tool and dependency checks from skill selection.
        Record: AL_F_GATE
        Basis: derived; status: draft.
        Source: S7
        Source: S9
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_CALL allocate System::functions.F_ROOT.F_CALL to Logical::architecture.LC_ROOT.LC_EXEC {
        doc /* Request permitted operation
        Use an existing tool or optional script with explicit inputs.
        Record: AL_F_CALL
        Basis: derived; status: draft.
        Source: S7
        Source: S9
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_RESULT allocate System::functions.F_ROOT.F_RESULT to Logical::architecture.LC_ROOT.LC_EXEC {
        doc /* Inspect returned result
        Read outputs, errors and artifacts rather than assume success.
        Record: AL_F_RESULT
        Basis: derived; status: draft.
        Source: S7
        Source: S9
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_VERIFY allocate System::functions.F_ROOT.F_VERIFY to Logical::architecture.LC_ROOT.LC_ASSURE {
        doc /* Check the actual outcome
        Check expected meaning and observable output before delivery.
        Record: AL_F_VERIFY
        Basis: derived; status: draft.
        Source: S8
        Source: S10
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_ANSWER allocate System::functions.F_ROOT.F_ANSWER to Logical::architecture.LC_ROOT.LC_REASON {
        doc /* Deliver the grounded result
        Return the outcome supported by available evidence.
        Record: AL_F_ANSWER
        Basis: derived; status: draft.
        Source: S9
        Source: S10
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_PLAIN allocate System::functions.F_ROOT.F_PLAIN to Logical::architecture.LC_ROOT.LC_REASON {
        doc /* Proceed without this skill
        Continue normally when no suitable available guidance applies.
        Record: AL_F_PLAIN
        Basis: derived; status: draft.
        Source: S5
        Source: S9
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_BLOCK allocate System::functions.F_ROOT.F_BLOCK to Logical::architecture.LC_ROOT.LC_EXEC {
        doc /* Retain unresolved outcome
        Explain a specific blocker or use a permitted alternative without claiming completion.
        Record: AL_F_BLOCK
        Basis: derived; status: draft.
        Source: S9
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_DRAFT allocate System::functions.F_ROOT.F_DRAFT to Logical::architecture.LC_ROOT.LC_MAINTAIN {
        doc /* Draft a focused revision
        Specify purpose, triggers, inputs, method and outputs.
        Record: AL_F_DRAFT
        Basis: derived; status: draft.
        Source: S6
        Source: S11
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_TRIAL allocate System::functions.F_ROOT.F_TRIAL to Logical::architecture.LC_ROOT.LC_ASSURE {
        doc /* Run comparable tasks
        Use realistic prompts and negative cases for candidate and baseline.
        Record: AL_F_TRIAL
        Basis: derived; status: draft.
        Source: S8
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_COMPARE allocate System::functions.F_ROOT.F_COMPARE to Logical::architecture.LC_ROOT.LC_ASSURE {
        doc /* Compare observed outputs
        Combine behavioral assertions with human quality judgment.
        Record: AL_F_COMPARE
        Basis: derived; status: draft.
        Source: S8
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_REVISE allocate System::functions.F_ROOT.F_REVISE to Logical::architecture.LC_ROOT.LC_MAINTAIN {
        doc /* Repair observed weaknesses
        Change the method based on actual failure evidence.
        Record: AL_F_REVISE
        Basis: derived; status: draft.
        Source: S8
        Source: S11
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_RELEASE allocate System::functions.F_ROOT.F_RELEASE to Logical::architecture.LC_ROOT.LC_MAINTAIN {
        doc /* Record evaluated baseline
        Promote the reviewed candidate while retaining its evidence and predecessor.
        Record: AL_F_RELEASE
        Basis: derived; status: draft.
        Source: S11
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_INTERPRET allocate System::functions.F_ROOT.F_INTERPRET to Logical::architecture.LC_ROOT.LC_REASON {
        doc /* Interpret source into model assertions
        Identify source entities, responsibilities, exchanges and lifecycle conditions.
        Record: AL_F_INTERPRET
        Basis: derived; status: draft.
        Source: S10
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_MODEL allocate System::functions.F_ROOT.F_MODEL to Logical::architecture.LC_ROOT.LC_REASON {
        doc /* Author candidate SysML
        Express sourced meaning and distinguish engineering assumptions.
        Record: AL_F_MODEL
        Basis: derived; status: draft.
        Source: S10
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_QUALIFY allocate System::functions.F_ROOT.F_QUALIFY to Logical::architecture.LC_ROOT.LC_EXEC {
        doc /* Check native model relationships
        Run the available native checker against the exact candidate.
        Record: AL_F_QUALIFY
        Basis: derived; status: draft.
        Source: S10
        A conceptual responsibility, not a claim about a product service. */
    }
    allocation AL_F_RENDER allocate System::functions.F_ROOT.F_RENDER to Logical::architecture.LC_ROOT.LC_EXEC {
        doc /* Build model-backed HTML views
        Project the same model into question-led views.
        Record: AL_F_RENDER
        Basis: derived; status: draft.
        Source: S10
        A conceptual responsibility, not a claim about a product service. */
    }
    dependency trace_F_ROOT_OA_TASK from ConOpsArchitecture::System::functions::F_ROOT to ConOpsArchitecture::Operational::activities::OA_TASK {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_ROOT_OA_MAINTAIN from ConOpsArchitecture::System::functions::F_ROOT to ConOpsArchitecture::Operational::activities::OA_MAINTAIN {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_DISCOVER_OA_PROVISION from ConOpsArchitecture::System::functions::F_ROOT::F_DISCOVER to ConOpsArchitecture::Operational::activities::OA_PROVISION {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_CATALOG_OA_PROVISION from ConOpsArchitecture::System::functions::F_ROOT::F_CATALOG to ConOpsArchitecture::Operational::activities::OA_PROVISION {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_SELECT_OA_TASK from ConOpsArchitecture::System::functions::F_ROOT::F_SELECT to ConOpsArchitecture::Operational::activities::OA_TASK {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_LOAD_OA_TASK from ConOpsArchitecture::System::functions::F_ROOT::F_LOAD to ConOpsArchitecture::Operational::activities::OA_TASK {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_PLAN_OA_TASK from ConOpsArchitecture::System::functions::F_ROOT::F_PLAN to ConOpsArchitecture::Operational::activities::OA_TASK {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_REFERENCE_OA_TASK from ConOpsArchitecture::System::functions::F_ROOT::F_REFERENCE to ConOpsArchitecture::Operational::activities::OA_TASK {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_ASSET_OA_TASK from ConOpsArchitecture::System::functions::F_ROOT::F_ASSET to ConOpsArchitecture::Operational::activities::OA_TASK {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_GATE_OA_OPERATE from ConOpsArchitecture::System::functions::F_ROOT::F_GATE to ConOpsArchitecture::Operational::activities::OA_OPERATE {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_CALL_OA_OPERATE from ConOpsArchitecture::System::functions::F_ROOT::F_CALL to ConOpsArchitecture::Operational::activities::OA_OPERATE {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_RESULT_OA_OPERATE from ConOpsArchitecture::System::functions::F_ROOT::F_RESULT to ConOpsArchitecture::Operational::activities::OA_OPERATE {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_VERIFY_OA_TASK from ConOpsArchitecture::System::functions::F_ROOT::F_VERIFY to ConOpsArchitecture::Operational::activities::OA_TASK {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_ANSWER_OA_TASK from ConOpsArchitecture::System::functions::F_ROOT::F_ANSWER to ConOpsArchitecture::Operational::activities::OA_TASK {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_PLAIN_OA_TASK from ConOpsArchitecture::System::functions::F_ROOT::F_PLAIN to ConOpsArchitecture::Operational::activities::OA_TASK {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_BLOCK_OA_OPERATE from ConOpsArchitecture::System::functions::F_ROOT::F_BLOCK to ConOpsArchitecture::Operational::activities::OA_OPERATE {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_DRAFT_OA_MAINTAIN from ConOpsArchitecture::System::functions::F_ROOT::F_DRAFT to ConOpsArchitecture::Operational::activities::OA_MAINTAIN {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_TRIAL_OA_EVAL from ConOpsArchitecture::System::functions::F_ROOT::F_TRIAL to ConOpsArchitecture::Operational::activities::OA_EVAL {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_COMPARE_OA_EVAL from ConOpsArchitecture::System::functions::F_ROOT::F_COMPARE to ConOpsArchitecture::Operational::activities::OA_EVAL {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_REVISE_OA_MAINTAIN from ConOpsArchitecture::System::functions::F_ROOT::F_REVISE to ConOpsArchitecture::Operational::activities::OA_MAINTAIN {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_RELEASE_OA_MAINTAIN from ConOpsArchitecture::System::functions::F_ROOT::F_RELEASE to ConOpsArchitecture::Operational::activities::OA_MAINTAIN {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_INTERPRET_OA_TASK from ConOpsArchitecture::System::functions::F_ROOT::F_INTERPRET to ConOpsArchitecture::Operational::activities::OA_TASK {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_MODEL_OA_TASK from ConOpsArchitecture::System::functions::F_ROOT::F_MODEL to ConOpsArchitecture::Operational::activities::OA_TASK {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_QUALIFY_OA_OPERATE from ConOpsArchitecture::System::functions::F_ROOT::F_QUALIFY to ConOpsArchitecture::Operational::activities::OA_OPERATE {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    dependency trace_F_RENDER_OA_OPERATE from ConOpsArchitecture::System::functions::F_ROOT::F_RENDER to ConOpsArchitecture::Operational::activities::OA_OPERATE {
        doc /* System contribution traced to an operational activity; this dependency is not a temporal or data-flow edge. */
    }
    package Context {
        interface CX_0 : Types::IF_CX_0 connect Operational::context.USER.p_CX_0 to Logical::architecture.LC_ROOT.LC_REASON.p_CX_0 {
            doc /* Intent, input files and explicit selection
            The task owner supplies the requested outcome, source files and any explicitly selected skill to the agent.
            Record: CX_0
            Basis: derived; status: draft.
            Source: S5
            Source: S9
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_1 : Types::IF_CX_1 connect Operational::context.HOST.p_CX_1 to Logical::architecture.LC_ROOT.LC_PACKAGE.p_CX_1 {
            doc /* Accessible trusted package locations
            The host exposes package locations that are available in its environment and allowed by its trust policy; a remote host may not have local user files.
            Record: CX_1
            Basis: derived; status: draft.
            Source: S4
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_2 : Types::IF_CX_2 connect Operational::context.HOST.p_CX_2 to Logical::architecture.LC_ROOT.LC_EXEC.p_CX_2 {
            doc /* Capabilities and permission disposition
            Before an operation is requested, the host provides which tools are available and whether the intended action is allowed. A matching skill does not supply that authority.
            Record: CX_2
            Basis: derived; status: draft.
            Source: S9
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_3 : Types::IF_CX_3 connect Logical::architecture.LC_ROOT.LC_EXEC.p_CX_3 to Operational::context.TOOLS.p_CX_3 {
            doc /* Operation request and inputs
            Execution coordination sends the selected tool an operation name and explicit inputs only after the applicable prerequisites and permissions are satisfied.
            Record: CX_3
            Basis: derived; status: draft.
            Source: S7
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_4 : Types::IF_CX_4 connect Operational::context.TOOLS.p_CX_4 to Logical::architecture.LC_ROOT.LC_EXEC.p_CX_4 {
            doc /* Output artifact or error
            The tool returns an output artifact or an error. Execution coordination inspects that response before the agent can treat the task as complete.
            Record: CX_4
            Basis: derived; status: draft.
            Source: S7
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_5 : Types::IF_CX_5 connect Logical::architecture.LC_ROOT.LC_REASON.p_CX_5 to Operational::context.USER.p_CX_5 {
            doc /* Reviewed result or precise blocker
            The agent returns the checked result to the task owner, or identifies the work that remains unresolved.
            Record: CX_5
            Basis: derived; status: draft.
            Source: S9
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_6 : Types::IF_CX_6 connect Operational::context.AUTHOR.p_CX_6 to Logical::architecture.LC_ROOT.LC_MAINTAIN.p_CX_6 {
            doc /* Candidate revision and intended behavior
            The maintainer submits an identified candidate revision with the task scope and behavior it is intended to improve.
            Record: CX_6
            Basis: derived; status: draft.
            Source: S6
            Source: S11
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_7 : Types::IF_CX_7 connect Logical::architecture.LC_ROOT.LC_ASSURE.p_CX_7 to Operational::context.REVIEWER.p_CX_7 {
            doc /* Candidate and baseline outputs
            Outcome assurance supplies candidate and baseline outputs from comparable tasks for independent review.
            Record: CX_7
            Basis: derived; status: draft.
            Source: S8
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
        interface CX_8 : Types::IF_CX_8 connect Operational::context.REVIEWER.p_CX_8 to Logical::architecture.LC_ROOT.LC_ASSURE.p_CX_8 {
            doc /* Comparative quality judgment
            The evaluator returns observed strengths, failures and regressions, without treating a favorable single example as universal reliability.
            Record: CX_8
            Basis: derived; status: draft.
            Source: S8
            Typed operational participant/logical responsibility contract. This does not select a physical protocol or implement the external authority. */
        }
    }
    package Scenarios {
        action SC_DISCLOSE {
            doc /* How much does the agent load?
            How much does the agent load?
            Record: SC_DISCLOSE
            Basis: derived; status: draft.
            Source: S2
            Source: S3
            Source: S4
            Source: S5
            Source: S6
            Source: S9
            Entry: T; h; e;  ; n; a; m; e; d;  ; t; e; a; c; h; i; n; g;  ; s; i; t; u; a; t; i; o; n;  ; a; n; d;  ; r; e; q; u; i; r; e; d;  ; s; o; u; r; c; e;  ; i; n; p; u; t; s;  ; a; p; p; l; y; .
            Exit: O; n; e;  ; o; f;  ; t; h; e;  ; e; x; p; l; i; c; i; t; l; y;  ; d; e; c; l; a; r; e; d;  ; o; u; t; c; o; m; e; s;  ; i; s;  ; r; e; a; c; h; e; d; ;;  ; a; n;  ; u; n; r; e; s; o; l; v; e; d;  ; r; e; s; u; l; t;  ; i; s;  ; n; o; t;  ; c; o; m; p; l; e; t; i; o; n; .
            Guards are documented predicates with unspecified values. No execution, guard exclusivity or timing result is claimed. */
            action 'Discover usable packages' : Types::T_F_DISCOVER {
                doc /* Discover usable packages (Record: discover); responsible role: unresolved */
            }
            action 'Expose names and descriptions' : Types::T_F_CATALOG {
                doc /* Expose names and descriptions (Record: catalog); responsible role: unresolved */
            }
            action 'Choose relevant guidance' : Types::T_F_SELECT {
                doc /* Choose relevant guidance (Record: select); responsible role: unresolved */
            }
            action 'Read selected workflow' : Types::T_F_LOAD {
                doc /* Read selected workflow (Record: load); responsible role: unresolved */
            }
            action 'Interpret method for this task' : Types::T_F_PLAN {
                doc /* Interpret method for this task (Record: plan); responsible role: unresolved */
            }
            action 'Read relevant reference' : Types::T_F_REFERENCE {
                doc /* Read relevant reference (Record: reference); responsible role: unresolved */
            }
            action 'Use relevant template' : Types::T_F_ASSET {
                doc /* Use relevant template (Record: asset); responsible role: unresolved */
            }
            action 'Deliver the grounded result' : Types::T_F_ANSWER {
                doc /* Deliver the grounded result (Record: answer); responsible role: unresolved */
            }
            action 'Proceed without this skill' : Types::T_F_PLAIN {
                doc /* Proceed without this skill (Record: plain); responsible role: unresolved */
            }
            first start then 'Discover usable packages';
            attribute 'Usable packages available' : Boolean {
                doc /* Review predicate: Usable packages available */
            }
            succession SC_DISCLOSE_T1 first 'Discover usable packages' if 'Usable packages available' then 'Expose names and descriptions' {
                doc /* Usable packages available; outcome:  */
            }
            attribute 'Task received' : Boolean {
                doc /* Review predicate: Task received */
            }
            succession SC_DISCLOSE_T2 first 'Expose names and descriptions' if 'Task received' then 'Choose relevant guidance' {
                doc /* Task received; outcome:  */
            }
            attribute 'Explicit choice or relevant permitted match' : Boolean {
                doc /* Review predicate: Explicit choice or relevant permitted match */
            }
            succession SC_DISCLOSE_T3 first 'Choose relevant guidance' if 'Explicit choice or relevant permitted match' then 'Read selected workflow' {
                doc /* Explicit choice or relevant permitted match; outcome:  */
            }
            attribute 'No suitable available skill' : Boolean {
                doc /* Review predicate: No suitable available skill */
            }
            succession SC_DISCLOSE_T4 first 'Choose relevant guidance' if 'No suitable available skill' then 'Proceed without this skill' {
                doc /* No suitable available skill; outcome:  */
            }
            attribute 'Chosen instructions read' : Boolean {
                doc /* Review predicate: Chosen instructions read */
            }
            succession SC_DISCLOSE_T5 first 'Read selected workflow' if 'Chosen instructions read' then 'Interpret method for this task' {
                doc /* Chosen instructions read; outcome:  */
            }
            attribute 'Additional knowledge needed' : Boolean {
                doc /* Review predicate: Additional knowledge needed */
            }
            succession SC_DISCLOSE_T6 first 'Interpret method for this task' if 'Additional knowledge needed' then 'Read relevant reference' {
                doc /* Additional knowledge needed; outcome:  */
            }
            attribute 'Needed detail read' : Boolean {
                doc /* Review predicate: Needed detail read */
            }
            succession SC_DISCLOSE_T7 first 'Read relevant reference' if 'Needed detail read' then 'Interpret method for this task' {
                doc /* Needed detail read; outcome:  */
            }
            attribute 'Template needed' : Boolean {
                doc /* Review predicate: Template needed */
            }
            succession SC_DISCLOSE_T8 first 'Interpret method for this task' if 'Template needed' then 'Use relevant template' {
                doc /* Template needed; outcome:  */
            }
            attribute 'Template available' : Boolean {
                doc /* Review predicate: Template available */
            }
            succession SC_DISCLOSE_T9 first 'Use relevant template' if 'Template available' then 'Interpret method for this task' {
                doc /* Template available; outcome:  */
            }
            attribute 'Instruction-only answer supported' : Boolean {
                doc /* Review predicate: Instruction-only answer supported */
            }
            succession SC_DISCLOSE_T10 first 'Interpret method for this task' if 'Instruction-only answer supported' then 'Deliver the grounded result' {
                doc /* Instruction-only answer supported; outcome:  */
            }
            attribute 'Task answered with selected guidance' : Boolean {
                doc /* Completion criterion: Task answered with selected guidance */
            }
            first 'Deliver the grounded result' if 'Task answered with selected guidance' then done;
            attribute 'No skill-based outcome asserted' : Boolean {
                doc /* Completion criterion: No skill-based outcome asserted */
            }
            first 'Proceed without this skill' if 'No skill-based outcome asserted' then done;
            view ActionFlow : StandardViewDefinitions::ActionFlowView {
                doc /* How much does the agent load? */
                expose SC_DISCLOSE::*;
            }
        }
        action SC_EXEC {
            doc /* Why does a selected skill still fail?
            Why does a selected skill still fail?
            Record: SC_EXEC
            Basis: derived; status: draft.
            Source: S7
            Source: S8
            Source: S9
            Entry: T; h; e;  ; n; a; m; e; d;  ; t; e; a; c; h; i; n; g;  ; s; i; t; u; a; t; i; o; n;  ; a; n; d;  ; r; e; q; u; i; r; e; d;  ; s; o; u; r; c; e;  ; i; n; p; u; t; s;  ; a; p; p; l; y; .
            Exit: O; n; e;  ; o; f;  ; t; h; e;  ; e; x; p; l; i; c; i; t; l; y;  ; d; e; c; l; a; r; e; d;  ; o; u; t; c; o; m; e; s;  ; i; s;  ; r; e; a; c; h; e; d; ;;  ; a; n;  ; u; n; r; e; s; o; l; v; e; d;  ; r; e; s; u; l; t;  ; i; s;  ; n; o; t;  ; c; o; m; p; l; e; t; i; o; n; .
            Guards are documented predicates with unspecified values. No execution, guard exclusivity or timing result is claimed. */
            action 'Interpret method for this task' : Types::T_F_PLAN {
                doc /* Interpret method for this task (Record: plan); responsible role: unresolved */
            }
            action 'Check execution prerequisites' : Types::T_F_GATE {
                doc /* Check execution prerequisites (Record: gate); responsible role: unresolved */
            }
            action 'Request permitted operation' : Types::T_F_CALL {
                doc /* Request permitted operation (Record: call); responsible role: unresolved */
            }
            action 'Inspect returned result' : Types::T_F_RESULT {
                doc /* Inspect returned result (Record: result); responsible role: unresolved */
            }
            action 'Check the actual outcome' : Types::T_F_VERIFY {
                doc /* Check the actual outcome (Record: verify); responsible role: unresolved */
            }
            action 'Deliver the grounded result' : Types::T_F_ANSWER {
                doc /* Deliver the grounded result (Record: answer); responsible role: unresolved */
            }
            action 'Retain unresolved outcome' : Types::T_F_BLOCK {
                doc /* Retain unresolved outcome (Record: block); responsible role: unresolved */
            }
            first start then 'Interpret method for this task';
            attribute 'No operation required' : Boolean {
                doc /* Review predicate: No operation required */
            }
            succession SC_EXEC_T1 first 'Interpret method for this task' if 'No operation required' then 'Check the actual outcome' {
                doc /* No operation required; outcome:  */
            }
            attribute 'Operation needed' : Boolean {
                doc /* Review predicate: Operation needed */
            }
            succession SC_EXEC_T2 first 'Interpret method for this task' if 'Operation needed' then 'Check execution prerequisites' {
                doc /* Operation needed; outcome:  */
            }
            attribute 'Permission and prerequisites satisfied' : Boolean {
                doc /* Review predicate: Permission and prerequisites satisfied */
            }
            succession SC_EXEC_T3 first 'Check execution prerequisites' if 'Permission and prerequisites satisfied' then 'Request permitted operation' {
                doc /* Permission and prerequisites satisfied; outcome:  */
            }
            attribute 'Required permission or capability absent' : Boolean {
                doc /* Review predicate: Required permission or capability absent */
            }
            succession SC_EXEC_T4 first 'Check execution prerequisites' if 'Required permission or capability absent' then 'Retain unresolved outcome' {
                doc /* Required permission or capability absent; outcome:  */
            }
            attribute 'Tool returns' : Boolean {
                doc /* Review predicate: Tool returns */
            }
            succession SC_EXEC_T5 first 'Request permitted operation' if 'Tool returns' then 'Inspect returned result' {
                doc /* Tool returns; outcome:  */
            }
            attribute 'Usable output returned' : Boolean {
                doc /* Review predicate: Usable output returned */
            }
            succession SC_EXEC_T6 first 'Inspect returned result' if 'Usable output returned' then 'Check the actual outcome' {
                doc /* Usable output returned; outcome:  */
            }
            attribute 'Error or unusable output' : Boolean {
                doc /* Review predicate: Error or unusable output */
            }
            succession SC_EXEC_T7 first 'Inspect returned result' if 'Error or unusable output' then 'Retain unresolved outcome' {
                doc /* Error or unusable output; outcome:  */
            }
            attribute 'Required checks support outcome' : Boolean {
                doc /* Review predicate: Required checks support outcome */
            }
            succession SC_EXEC_T8 first 'Check the actual outcome' if 'Required checks support outcome' then 'Deliver the grounded result' {
                doc /* Required checks support outcome; outcome:  */
            }
            attribute 'Required outcome not established' : Boolean {
                doc /* Review predicate: Required outcome not established */
            }
            succession SC_EXEC_T9 first 'Check the actual outcome' if 'Required outcome not established' then 'Retain unresolved outcome' {
                doc /* Required outcome not established; outcome:  */
            }
            attribute 'Outcome checked and delivered' : Boolean {
                doc /* Completion criterion: Outcome checked and delivered */
            }
            first 'Deliver the grounded result' if 'Outcome checked and delivered' then done;
            attribute 'Unresolved work retained as unresolved' : Boolean {
                doc /* Completion criterion: Unresolved work retained as unresolved */
            }
            first 'Retain unresolved outcome' if 'Unresolved work retained as unresolved' then done;
            view ActionFlow : StandardViewDefinitions::ActionFlowView {
                doc /* Why does a selected skill still fail? */
                expose SC_EXEC::*;
            }
        }
        action SC_IMPROVE {
            doc /* How does a skill get better?
            How does a skill get better?
            Record: SC_IMPROVE
            Basis: derived; status: draft.
            Source: S6
            Source: S8
            Source: S11
            Entry: T; h; e;  ; n; a; m; e; d;  ; t; e; a; c; h; i; n; g;  ; s; i; t; u; a; t; i; o; n;  ; a; n; d;  ; r; e; q; u; i; r; e; d;  ; s; o; u; r; c; e;  ; i; n; p; u; t; s;  ; a; p; p; l; y; .
            Exit: O; n; e;  ; o; f;  ; t; h; e;  ; e; x; p; l; i; c; i; t; l; y;  ; d; e; c; l; a; r; e; d;  ; o; u; t; c; o; m; e; s;  ; i; s;  ; r; e; a; c; h; e; d; ;;  ; a; n;  ; u; n; r; e; s; o; l; v; e; d;  ; r; e; s; u; l; t;  ; i; s;  ; n; o; t;  ; c; o; m; p; l; e; t; i; o; n; .
            Guards are documented predicates with unspecified values. No execution, guard exclusivity or timing result is claimed. */
            action 'Draft a focused revision' : Types::T_F_DRAFT {
                doc /* Draft a focused revision (Record: draft); responsible role: unresolved */
            }
            action 'Run comparable tasks' : Types::T_F_TRIAL {
                doc /* Run comparable tasks (Record: trial); responsible role: unresolved */
            }
            action 'Compare observed outputs' : Types::T_F_COMPARE {
                doc /* Compare observed outputs (Record: compare); responsible role: unresolved */
            }
            action 'Repair observed weaknesses' : Types::T_F_REVISE {
                doc /* Repair observed weaknesses (Record: revise); responsible role: unresolved */
            }
            action 'Record evaluated baseline' : Types::T_F_RELEASE {
                doc /* Record evaluated baseline (Record: release); responsible role: unresolved */
            }
            first start then 'Draft a focused revision';
            attribute 'Candidate and baseline identified' : Boolean {
                doc /* Review predicate: Candidate and baseline identified */
            }
            succession SC_IMPROVE_T1 first 'Draft a focused revision' if 'Candidate and baseline identified' then 'Run comparable tasks' {
                doc /* Candidate and baseline identified; outcome:  */
            }
            attribute 'Comparable outcomes collected' : Boolean {
                doc /* Review predicate: Comparable outcomes collected */
            }
            succession SC_IMPROVE_T2 first 'Run comparable tasks' if 'Comparable outcomes collected' then 'Compare observed outputs' {
                doc /* Comparable outcomes collected; outcome:  */
            }
            attribute 'Failure or regression observed' : Boolean {
                doc /* Review predicate: Failure or regression observed */
            }
            succession SC_IMPROVE_T3 first 'Compare observed outputs' if 'Failure or regression observed' then 'Repair observed weaknesses' {
                doc /* Failure or regression observed; outcome:  */
            }
            attribute 'Changed candidate requires fresh tests' : Boolean {
                doc /* Review predicate: Changed candidate requires fresh tests */
            }
            succession SC_IMPROVE_T4 first 'Repair observed weaknesses' if 'Changed candidate requires fresh tests' then 'Run comparable tasks' {
                doc /* Changed candidate requires fresh tests; outcome:  */
            }
            attribute 'Evidence supports intended improvement' : Boolean {
                doc /* Review predicate: Evidence supports intended improvement */
            }
            succession SC_IMPROVE_T5 first 'Compare observed outputs' if 'Evidence supports intended improvement' then 'Record evaluated baseline' {
                doc /* Evidence supports intended improvement; outcome:  */
            }
            attribute 'Reviewed candidate recorded; no universal quality claim' : Boolean {
                doc /* Completion criterion: Reviewed candidate recorded; no universal quality claim */
            }
            first 'Record evaluated baseline' if 'Reviewed candidate recorded; no universal quality claim' then done;
            view ActionFlow : StandardViewDefinitions::ActionFlowView {
                doc /* How does a skill get better? */
                expose SC_IMPROVE::*;
            }
        }
        action SC_SYSML {
            doc /* Example: explain how agent skills work
            Example: explain how agent skills work
            Record: SC_SYSML
            Basis: derived; status: draft.
            Source: S10
            Source: S9
            Entry: T; h; e;  ; n; a; m; e; d;  ; t; e; a; c; h; i; n; g;  ; s; i; t; u; a; t; i; o; n;  ; a; n; d;  ; r; e; q; u; i; r; e; d;  ; s; o; u; r; c; e;  ; i; n; p; u; t; s;  ; a; p; p; l; y; .
            Exit: O; n; e;  ; o; f;  ; t; h; e;  ; e; x; p; l; i; c; i; t; l; y;  ; d; e; c; l; a; r; e; d;  ; o; u; t; c; o; m; e; s;  ; i; s;  ; r; e; a; c; h; e; d; ;;  ; a; n;  ; u; n; r; e; s; o; l; v; e; d;  ; r; e; s; u; l; t;  ; i; s;  ; n; o; t;  ; c; o; m; p; l; e; t; i; o; n; .
            Guards are documented predicates with unspecified values. No execution, guard exclusivity or timing result is claimed. */
            action 'Read selected workflow' : Types::T_F_LOAD {
                doc /* Read selected workflow (Record: load); responsible role: unresolved */
            }
            action 'Interpret source into model assertions' : Types::T_F_INTERPRET {
                doc /* Interpret source into model assertions (Record: interpret); responsible role: unresolved */
            }
            action 'Author candidate SysML' : Types::T_F_MODEL {
                doc /* Author candidate SysML (Record: model); responsible role: unresolved */
            }
            action 'Check execution prerequisites' : Types::T_F_GATE {
                doc /* Check execution prerequisites (Record: gate); responsible role: unresolved */
            }
            action 'Check native model relationships' : Types::T_F_QUALIFY {
                doc /* Check native model relationships (Record: qualify); responsible role: unresolved */
            }
            action 'Build model-backed HTML views' : Types::T_F_RENDER {
                doc /* Build model-backed HTML views (Record: render); responsible role: unresolved */
            }
            action 'Check the actual outcome' : Types::T_F_VERIFY {
                doc /* Check the actual outcome (Record: verify); responsible role: unresolved */
            }
            action 'Deliver the grounded result' : Types::T_F_ANSWER {
                doc /* Deliver the grounded result (Record: answer); responsible role: unresolved */
            }
            action 'Retain unresolved outcome' : Types::T_F_BLOCK {
                doc /* Retain unresolved outcome (Record: block); responsible role: unresolved */
            }
            first start then 'Read selected workflow';
            attribute 'Answer with SysML selected' : Boolean {
                doc /* Review predicate: Answer with SysML selected */
            }
            succession SC_SYSML_T1 first 'Read selected workflow' if 'Answer with SysML selected' then 'Interpret source into model assertions' {
                doc /* Answer with SysML selected; outcome:  */
            }
            attribute 'Sources and assumptions separated' : Boolean {
                doc /* Review predicate: Sources and assumptions separated */
            }
            succession SC_SYSML_T2 first 'Interpret source into model assertions' if 'Sources and assumptions separated' then 'Author candidate SysML' {
                doc /* Sources and assumptions separated; outcome:  */
            }
            attribute 'Candidate ready to check' : Boolean {
                doc /* Review predicate: Candidate ready to check */
            }
            succession SC_SYSML_T3 first 'Author candidate SysML' if 'Candidate ready to check' then 'Check execution prerequisites' {
                doc /* Candidate ready to check; outcome:  */
            }
            attribute 'Checker available and permitted' : Boolean {
                doc /* Review predicate: Checker available and permitted */
            }
            succession SC_SYSML_T4 first 'Check execution prerequisites' if 'Checker available and permitted' then 'Check native model relationships' {
                doc /* Checker available and permitted; outcome:  */
            }
            attribute 'Native checking unavailable' : Boolean {
                doc /* Review predicate: Native checking unavailable */
            }
            succession SC_SYSML_T5 first 'Check execution prerequisites' if 'Native checking unavailable' then 'Retain unresolved outcome' {
                doc /* Native checking unavailable; outcome:  */
            }
            attribute 'Native errors require repair' : Boolean {
                doc /* Review predicate: Native errors require repair */
            }
            succession SC_SYSML_T6 first 'Check native model relationships' if 'Native errors require repair' then 'Author candidate SysML' {
                doc /* Native errors require repair; outcome:  */
            }
            attribute 'Exact candidate qualified' : Boolean {
                doc /* Review predicate: Exact candidate qualified */
            }
            succession SC_SYSML_T7 first 'Check native model relationships' if 'Exact candidate qualified' then 'Build model-backed HTML views' {
                doc /* Exact candidate qualified; outcome:  */
            }
            attribute 'Model-backed views produced' : Boolean {
                doc /* Review predicate: Model-backed views produced */
            }
            succession SC_SYSML_T8 first 'Build model-backed HTML views' if 'Model-backed views produced' then 'Check the actual outcome' {
                doc /* Model-backed views produced; outcome:  */
            }
            attribute 'Source-meaning defect found' : Boolean {
                doc /* Review predicate: Source-meaning defect found */
            }
            succession SC_SYSML_T9 first 'Check the actual outcome' if 'Source-meaning defect found' then 'Author candidate SysML' {
                doc /* Source-meaning defect found; outcome:  */
            }
            attribute 'Layout or interaction defect found' : Boolean {
                doc /* Review predicate: Layout or interaction defect found */
            }
            succession SC_SYSML_T10 first 'Check the actual outcome' if 'Layout or interaction defect found' then 'Build model-backed HTML views' {
                doc /* Layout or interaction defect found; outcome:  */
            }
            attribute 'Source and delivered views checked' : Boolean {
                doc /* Review predicate: Source and delivered views checked */
            }
            succession SC_SYSML_T11 first 'Check the actual outcome' if 'Source and delivered views checked' then 'Deliver the grounded result' {
                doc /* Source and delivered views checked; outcome:  */
            }
            attribute 'Source, native model and views delivered' : Boolean {
                doc /* Completion criterion: Source, native model and views delivered */
            }
            first 'Deliver the grounded result' if 'Source, native model and views delivered' then done;
            attribute 'No false native qualification claim' : Boolean {
                doc /* Completion criterion: No false native qualification claim */
            }
            first 'Retain unresolved outcome' if 'No false native qualification claim' then done;
            view ActionFlow : StandardViewDefinitions::ActionFlowView {
                doc /* Example: explain how agent skills work */
                expose SC_SYSML::*;
            }
        }
    }
    package Requirements {
        requirement <R_DISCLOSE> 'Expose metadata before loading relevant detail.' {
            doc /* Expose metadata before loading relevant detail. */
            comment ReviewBasis /* Basis: derived; status: draft.
            Source: S3
            Rationale: Preserve the distinction needed for this teaching system. */
            subject subjectOfRequirement : ConOpsArchitecture::Types::T_F_CATALOG = System::functions.F_ROOT.F_CATALOG;
            require constraint criterion {
                doc /* Expose metadata before loading relevant detail. */
            }
        }
        requirement <R_HOST> 'Do not turn one host selection policy into a format-wide fact.' {
            doc /* Do not turn one host selection policy into a format-wide fact. */
            comment ReviewBasis /* Basis: derived; status: draft.
            Source: S4
            Source: S5
            Source: S12
            Rationale: Preserve the distinction needed for this teaching system. */
            subject subjectOfRequirement : ConOpsArchitecture::Types::T_F_SELECT = System::functions.F_ROOT.F_SELECT;
            require constraint criterion {
                doc /* Do not turn one host selection policy into a format-wide fact. */
            }
        }
        requirement <R_OPTIONAL> 'Permit useful instruction-only work without requiring scripts.' {
            doc /* Permit useful instruction-only work without requiring scripts. */
            comment ReviewBasis /* Basis: derived; status: draft.
            Source: S6
            Rationale: Preserve the distinction needed for this teaching system. */
            subject subjectOfRequirement : ConOpsArchitecture::Types::T_F_PLAN = System::functions.F_ROOT.F_PLAN;
            require constraint criterion {
                doc /* Permit useful instruction-only work without requiring scripts. */
            }
        }
        requirement <R_AUTH> 'A skill selection must not be treated as permission for an operation.' {
            doc /* A skill selection must not be treated as permission for an operation. */
            comment ReviewBasis /* Basis: derived; status: draft.
            Source: S9
            Rationale: Preserve the distinction needed for this teaching system. */
            subject subjectOfRequirement : ConOpsArchitecture::Types::T_F_GATE = System::functions.F_ROOT.F_GATE;
            require constraint criterion {
                doc /* A skill selection must not be treated as permission for an operation. */
            }
        }
        requirement <R_RESULT> 'Distinguish tool invocation, returned output and verified outcome.' {
            doc /* Distinguish tool invocation, returned output and verified outcome. */
            comment ReviewBasis /* Basis: derived; status: draft.
            Source: S7
            Source: S9
            Rationale: Preserve the distinction needed for this teaching system. */
            subject subjectOfRequirement : ConOpsArchitecture::Types::T_F_VERIFY = System::functions.F_ROOT.F_VERIFY;
            require constraint criterion {
                doc /* Distinguish tool invocation, returned output and verified outcome. */
            }
        }
        requirement <R_EVAL> 'Evaluate the changed candidate against the baseline before recording improvement.' {
            doc /* Evaluate the changed candidate against the baseline before recording improvement. */
            comment ReviewBasis /* Basis: derived; status: draft.
            Source: S8
            Source: S11
            Rationale: Preserve the distinction needed for this teaching system. */
            subject subjectOfRequirement : ConOpsArchitecture::Types::T_F_RELEASE = System::functions.F_ROOT.F_RELEASE;
            require constraint criterion {
                doc /* Evaluate the changed candidate against the baseline before recording improvement. */
            }
        }
        requirement <R_SOURCE> 'Preserve source evidence and identify model assumptions.' {
            doc /* Preserve source evidence and identify model assumptions. */
            comment ReviewBasis /* Basis: derived; status: draft.
            Source: S10
            Rationale: Preserve the distinction needed for this teaching system. */
            subject subjectOfRequirement : ConOpsArchitecture::Types::T_F_MODEL = System::functions.F_ROOT.F_MODEL;
            require constraint criterion {
                doc /* Preserve source evidence and identify model assumptions. */
            }
        }
        requirement <R_FRESH> 'Native qualification applies to the checked candidate bytes only.' {
            doc /* Native qualification applies to the checked candidate bytes only. */
            comment ReviewBasis /* Basis: derived; status: draft.
            Source: S10
            Rationale: Preserve the distinction needed for this teaching system. */
            subject subjectOfRequirement : ConOpsArchitecture::Types::T_F_QUALIFY = System::functions.F_ROOT.F_QUALIFY;
            require constraint criterion {
                doc /* Native qualification applies to the checked candidate bytes only. */
            }
        }
    }
    package Verification {
        verification def V_R_DISCLOSE {
            doc /* Check R_DISCLOSE
            Review source and a counterexample for this obligation.
            Record: V_R_DISCLOSE
            Basis: proposed; status: planned.
            Source: S3
            Method: Source review and behavioral example
            Setup: Inspect the corresponding native subject and the positive and negative scenario branches.
            Expected result: Expose metadata before loading relevant detail.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ConOpsArchitecture::Types::T_F_CATALOG;
            objective {
                verify Requirements::'Expose metadata before loading relevant detail.';
            }
        }
        verification def V_R_HOST {
            doc /* Check R_HOST
            Review source and a counterexample for this obligation.
            Record: V_R_HOST
            Basis: proposed; status: planned.
            Source: S4
            Source: S5
            Source: S12
            Method: Source review and behavioral example
            Setup: Inspect the corresponding native subject and the positive and negative scenario branches.
            Expected result: Do not turn one host selection policy into a format-wide fact.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ConOpsArchitecture::Types::T_F_SELECT;
            objective {
                verify Requirements::'Do not turn one host selection policy into a format-wide fact.';
            }
        }
        verification def V_R_OPTIONAL {
            doc /* Check R_OPTIONAL
            Review source and a counterexample for this obligation.
            Record: V_R_OPTIONAL
            Basis: proposed; status: planned.
            Source: S6
            Method: Source review and behavioral example
            Setup: Inspect the corresponding native subject and the positive and negative scenario branches.
            Expected result: Permit useful instruction-only work without requiring scripts.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ConOpsArchitecture::Types::T_F_PLAN;
            objective {
                verify Requirements::'Permit useful instruction-only work without requiring scripts.';
            }
        }
        verification def V_R_AUTH {
            doc /* Check R_AUTH
            Review source and a counterexample for this obligation.
            Record: V_R_AUTH
            Basis: proposed; status: planned.
            Source: S9
            Method: Source review and behavioral example
            Setup: Inspect the corresponding native subject and the positive and negative scenario branches.
            Expected result: A skill selection must not be treated as permission for an operation.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ConOpsArchitecture::Types::T_F_GATE;
            objective {
                verify Requirements::'A skill selection must not be treated as permission for an operation.';
            }
        }
        verification def V_R_RESULT {
            doc /* Check R_RESULT
            Review source and a counterexample for this obligation.
            Record: V_R_RESULT
            Basis: proposed; status: planned.
            Source: S7
            Source: S9
            Method: Source review and behavioral example
            Setup: Inspect the corresponding native subject and the positive and negative scenario branches.
            Expected result: Distinguish tool invocation, returned output and verified outcome.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ConOpsArchitecture::Types::T_F_VERIFY;
            objective {
                verify Requirements::'Distinguish tool invocation, returned output and verified outcome.';
            }
        }
        verification def V_R_EVAL {
            doc /* Check R_EVAL
            Review source and a counterexample for this obligation.
            Record: V_R_EVAL
            Basis: proposed; status: planned.
            Source: S8
            Source: S11
            Method: Source review and behavioral example
            Setup: Inspect the corresponding native subject and the positive and negative scenario branches.
            Expected result: Evaluate the changed candidate against the baseline before recording improvement.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ConOpsArchitecture::Types::T_F_RELEASE;
            objective {
                verify Requirements::'Evaluate the changed candidate against the baseline before recording improvement.';
            }
        }
        verification def V_R_SOURCE {
            doc /* Check R_SOURCE
            Review source and a counterexample for this obligation.
            Record: V_R_SOURCE
            Basis: proposed; status: planned.
            Source: S10
            Method: Source review and behavioral example
            Setup: Inspect the corresponding native subject and the positive and negative scenario branches.
            Expected result: Preserve source evidence and identify model assumptions.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ConOpsArchitecture::Types::T_F_MODEL;
            objective {
                verify Requirements::'Preserve source evidence and identify model assumptions.';
            }
        }
        verification def V_R_FRESH {
            doc /* Check R_FRESH
            Review source and a counterexample for this obligation.
            Record: V_R_FRESH
            Basis: proposed; status: planned.
            Source: S10
            Method: Source review and behavioral example
            Setup: Inspect the corresponding native subject and the positive and negative scenario branches.
            Expected result: Native qualification applies to the checked candidate bytes only.
            No executed result or acceptance recorded. */
            subject subjectUnderReview : ConOpsArchitecture::Types::T_F_QUALIFY;
            objective {
                verify Requirements::'Native qualification applies to the checked candidate bytes only.';
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
        view Lifecycle_SM_REVISION : StandardViewDefinitions::StateTransitionView {
            doc /* A skill revision is not automatically a release */
            expose Types::T_SM_REVISION::*;
        }
    }
    package ReviewDecisions {
        package D_HOST {
            doc /* Host integration remains specific
            Check the receiving host for package locations, duplicate-name handling, trust filtering and implicit invocation settings before assuming a shared folder behaves identically there.
            Record: D_HOST
            Basis: derived; status: draft.
            Source: S4
            Source: S5
            Source: S12
            Which host and current configuration?
            Alternatives: ["Use current host documentation", "Keep unsupported behavior unspecified"] */
        }
    }
}
