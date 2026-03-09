#!/usr/bin/env python3
import argparse
import csv
import json
import random
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


ALL_REACTIONS = [
    "Reaction_Warmer_Guarded",
    "Reaction_No_Open",
    "Reaction_New_Observation",
    "Reaction_Delayed_Shift",
    "Reaction_Less_Private",
    "Reaction_Fragment_Relevant_NotEnough",
    "Reaction_Risk_Pushback",
    "Reaction_Context_Aligned",
]

PLACEHOLDER_TEXT = {
    "Reaction_Warmer_Guarded": "The reaction is warmer but still guarded.",
    "Reaction_No_Open": "Nothing opens at this time.",
    "Reaction_New_Observation": "A new observation is recorded.",
    "Reaction_Delayed_Shift": "This action changes later availability.",
    "Reaction_Less_Private": "The current context makes the space feel less private.",
    "Reaction_Fragment_Relevant_NotEnough": "The fragment matters here, but not yet enough.",
    "Reaction_Risk_Pushback": "The response hardens after boundary pressure.",
    "Reaction_Context_Aligned": "Timing and context align; response quality improves.",
}


@dataclass
class StepResult:
    trace_entry: Dict
    delayed_queue_out: List[Dict]


def load_config(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def clamp(v: float) -> float:
    return max(0.0, min(1.0, v))


def random_fragments(rng: random.Random, fragments: List[str]) -> List[str]:
    count = rng.randint(0, min(2, len(fragments)))
    return sorted(rng.sample(fragments, count)) if count else []


def choose_action(rng: random.Random, actions: List[str], mode: str) -> str:
    if mode == "deterministic":
        return actions[0]
    return rng.choice(actions)


def build_eligible_reactions(context: Dict, action: str, known_fragments: List[str], state: Dict) -> List[str]:
    eligible = ["Reaction_No_Open"]

    if action == "Action_Observe":
        eligible.append("Reaction_New_Observation")

    if action == "Action_Ask" and context["time"] in ["Evening", "Night"]:
        eligible.append("Reaction_Warmer_Guarded" if state["trust"] >= 0.35 else "Reaction_Fragment_Relevant_NotEnough")

    if action == "Action_Test_Boundary":
        eligible.append("Reaction_Risk_Pushback")
        if context["privacy"] < 0.5:
            eligible.append("Reaction_Less_Private")

    if action == "Action_Return_Later":
        eligible.append("Reaction_Delayed_Shift")

    if known_fragments and "Fragment_1" in known_fragments and action == "Action_Ask":
        eligible.append("Reaction_Context_Aligned")

    return sorted(set(eligible))


def score_reaction(reaction: str, context: Dict, state: Dict, action: str) -> float:
    base = {
        "Reaction_No_Open": 0.1,
        "Reaction_New_Observation": 0.45,
        "Reaction_Warmer_Guarded": 0.7,
        "Reaction_Delayed_Shift": 0.6,
        "Reaction_Less_Private": 0.55,
        "Reaction_Fragment_Relevant_NotEnough": 0.5,
        "Reaction_Risk_Pushback": 0.65,
        "Reaction_Context_Aligned": 0.75,
    }[reaction]

    if reaction == "Reaction_Warmer_Guarded":
        base += 0.2 * state["trust"]
    if reaction == "Reaction_Context_Aligned" and context["time"] in ["Evening", "Night"]:
        base += 0.1
    if reaction == "Reaction_Risk_Pushback":
        base += 0.2 * state["tension"]
    if reaction == "Reaction_No_Open" and action == "Action_Ask":
        base += 0.05
    return base


def apply_state_change(state: Dict, reaction: str, action: str) -> Tuple[Dict, List[str]]:
    new_state = deepcopy(state)
    new_info = []

    if action == "Action_Observe":
        new_state["curiosity"] = clamp(new_state["curiosity"] + 0.1)
        new_info.append("Fragment candidate surfaced.")

    if reaction == "Reaction_Warmer_Guarded":
        new_state["trust"] = clamp(new_state["trust"] + 0.1)
        new_state["tension"] = clamp(new_state["tension"] - 0.05)
        new_info.append("Trust increased slightly.")
    elif reaction == "Reaction_Risk_Pushback":
        new_state["trust"] = clamp(new_state["trust"] - 0.08)
        new_state["tension"] = clamp(new_state["tension"] + 0.1)
        new_info.append("Boundary resistance increased.")
    elif reaction == "Reaction_No_Open":
        new_state["curiosity"] = clamp(new_state["curiosity"] - 0.02)
    elif reaction == "Reaction_New_Observation":
        new_state["curiosity"] = clamp(new_state["curiosity"] + 0.08)
    elif reaction == "Reaction_Context_Aligned":
        new_state["trust"] = clamp(new_state["trust"] + 0.06)
        new_info.append("Context alignment signal recorded.")

    return new_state, new_info


def process_step(
    iteration_id: int,
    step_index: int,
    context: Dict,
    known_fragments: List[str],
    state: Dict,
    action: str,
    delayed_queue: List[Dict],
    delayed_enabled: bool,
    placeholder_text_enabled: bool,
) -> StepResult:
    delayed_queue_out = deepcopy(delayed_queue)
    immediate = True
    source = "immediate"

    if delayed_queue_out and delayed_enabled:
        due = delayed_queue_out.pop(0)
        selected = due["reaction"]
        eligible = [selected]
        source = "delayed"
        immediate = False
    else:
        eligible = build_eligible_reactions(context, action, known_fragments, state)
        selected = max(eligible, key=lambda r: score_reaction(r, context, state, action))

    if delayed_enabled and selected == "Reaction_Delayed_Shift":
        delayed_queue_out.append({"reaction": "Reaction_Context_Aligned", "delay_steps": 1})

    next_state, new_info = apply_state_change(state, selected, action)

    notes = PLACEHOLDER_TEXT[selected] if placeholder_text_enabled else selected
    trace_entry = {
        "iteration_id": iteration_id,
        "step_index": step_index,
        "time_context": {"space": context["space"], "time": context["time"], "id": context["id"]},
        "known_fragments": known_fragments,
        "hidden_state": state,
        "chosen_action": action,
        "eligible_reactions": eligible,
        "selected_reaction": selected,
        "source": source,
        "immediate_or_delayed": "immediate" if immediate else "delayed",
        "newly_unlocked_information": new_info,
        "notes": notes,
        "next_hidden_state": next_state,
    }
    return StepResult(trace_entry=trace_entry, delayed_queue_out=delayed_queue_out)


def build_metrics(config: Dict, traces: List[Dict], run_meta: Dict) -> Dict:
    selected = [t["selected_reaction"] for t in traces]
    unique = sorted(set(selected))
    never = sorted([r for r in ALL_REACTIONS if r not in unique])
    no_open_count = selected.count("Reaction_No_Open")
    delayed_count = sum(1 for t in traces if t["immediate_or_delayed"] == "delayed")

    action_context_pairs = {(t["chosen_action"], t["time_context"]["id"], t["selected_reaction"]) for t in traces}
    action_context_sensitivity = len(action_context_pairs)

    fragment_helpful = 0
    for t in traces:
        frag = set(t["known_fragments"])
        if frag and t["selected_reaction"] in ["Reaction_Context_Aligned", "Reaction_Warmer_Guarded", "Reaction_New_Observation"]:
            fragment_helpful += 1
    hint_usefulness_score = round(fragment_helpful / max(1, len(traces)), 3)

    seen_states = {}
    repeated_state_collapse = 0
    for t in traces:
        key = (
            round(t["next_hidden_state"]["trust"], 2),
            round(t["next_hidden_state"]["curiosity"], 2),
            round(t["next_hidden_state"]["tension"], 2),
            t["time_context"]["id"],
        )
        seen_states[key] = seen_states.get(key, 0) + 1
    repeated_state_collapse = sum(1 for c in seen_states.values() if c >= 3)

    loop_stagnation_warnings = []
    if no_open_count / max(1, len(traces)) > 0.45:
        loop_stagnation_warnings.append("High no-open frequency suggests weak reaction differentiation.")
    if len(unique) < 4:
        loop_stagnation_warnings.append("Low unique reaction count.")
    if repeated_state_collapse > 8:
        loop_stagnation_warnings.append("State collapse repeated frequently.")

    by_context_action = {}
    for t in traces:
        k = f"{t['time_context']['id']}::{t['chosen_action']}"
        by_context_action.setdefault(k, set()).add(t["selected_reaction"])
    no_diff_pairs = sorted([k for k, v in by_context_action.items() if len(v) == 1])

    immediate_count = len(traces) - delayed_count
    branch_diff_count = len(unique)

    return {
        "run_metadata": run_meta,
        "metrics": {
            "total_iterations": run_meta["iterations"],
            "total_steps": len(traces),
            "unique_reactions_triggered": len(unique),
            "unique_reaction_ids": unique,
            "reactions_never_triggered": never,
            "branch_differentiation_count": branch_diff_count,
            "empty_noop_reaction_frequency": round(no_open_count / max(1, len(traces)), 3),
            "delayed_reaction_frequency": round(delayed_count / max(1, len(traces)), 3),
            "immediate_reaction_count": immediate_count,
            "delayed_reaction_count": delayed_count,
            "hint_usefulness_score": hint_usefulness_score,
            "action_context_sensitivity": action_context_sensitivity,
            "repeated_state_collapse_count": repeated_state_collapse,
            "loop_stagnation_warnings": loop_stagnation_warnings,
            "contexts_actions_with_no_meaningful_difference": no_diff_pairs,
        },
    }


def write_outputs(result_dir: Path, payload: Dict, traces: List[Dict], archive: bool):
    result_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = result_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    latest_json = result_dir / "latest_run.json"
    latest_csv = result_dir / "latest_run.csv"
    latest_md = result_dir / "latest_run.md"

    out = deepcopy(payload)
    out["trace"] = traces
    latest_json.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    with latest_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "iteration_id", "step_index", "context_id", "space", "time", "action", "selected_reaction",
            "immediate_or_delayed", "known_fragments", "trust", "curiosity", "tension", "notes"
        ])
        for t in traces:
            hs = t["hidden_state"]
            w.writerow([
                t["iteration_id"], t["step_index"], t["time_context"]["id"], t["time_context"]["space"], t["time_context"]["time"],
                t["chosen_action"], t["selected_reaction"], t["immediate_or_delayed"],
                ";".join(t["known_fragments"]), hs["trust"], hs["curiosity"], hs["tension"], t["notes"]
            ])

    m = payload["metrics"]
    md = [
        "# Latest Lab Run Summary",
        "",
        f"- Run name: `{payload['run_metadata']['run_name']}`",
        f"- Seed: `{payload['run_metadata']['seed']}`",
        f"- Iterations: `{payload['run_metadata']['iterations']}`",
        f"- Max steps/iteration: `{payload['run_metadata']['max_steps_per_iteration']}`",
        "",
        "## Comparison-friendly summary",
        f"- Unique reactions triggered: `{m['unique_reactions_triggered']}` ({', '.join(m['unique_reaction_ids'])})",
        f"- Reactions never triggered: `{', '.join(m['reactions_never_triggered']) if m['reactions_never_triggered'] else 'none'}`",
        f"- Branch differentiation count: `{m['branch_differentiation_count']}`",
        f"- Empty/no-op frequency: `{m['empty_noop_reaction_frequency']}`",
        f"- Delayed reaction frequency: `{m['delayed_reaction_frequency']}`",
        f"- Hint usefulness score: `{m['hint_usefulness_score']}`",
        f"- Action-context sensitivity: `{m['action_context_sensitivity']}`",
        f"- Repeated state collapse count: `{m['repeated_state_collapse_count']}`",
        f"- Potential stagnation warnings: `{'; '.join(m['loop_stagnation_warnings']) if m['loop_stagnation_warnings'] else 'none'}`",
        "",
        "## Context/action with no meaningful difference",
    ]
    if m["contexts_actions_with_no_meaningful_difference"]:
        md.extend([f"- `{x}`" for x in m["contexts_actions_with_no_meaningful_difference"][:20]])
    else:
        md.append("- none")
    latest_md.write_text("\n".join(md), encoding="utf-8")

    if archive:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        (archive_dir / f"run_{ts}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")


def run_sim(config: Dict) -> Tuple[Dict, List[Dict]]:
    rng = random.Random(config["seed"])
    traces = []

    contexts = config["contexts"]
    presets = config["state_presets"]
    actions = config["actions"]
    fragments = config["fragments"]

    for iteration in range(1, config["iterations"] + 1):
        context = contexts[(iteration - 1) % len(contexts)] if config["variation_mode"] == "deterministic" else rng.choice(contexts)
        preset = presets[(iteration - 1) % len(presets)] if config["variation_mode"] == "deterministic" else rng.choice(presets)
        state = {"trust": preset["trust"], "curiosity": preset["curiosity"], "tension": preset["tension"]}
        known_fragments = random_fragments(rng, fragments)
        delayed_queue = []

        for step in range(1, config["max_steps_per_iteration"] + 1):
            action = choose_action(rng, actions, config["variation_mode"])
            res = process_step(
                iteration_id=iteration,
                step_index=step,
                context=context,
                known_fragments=known_fragments,
                state=state,
                action=action,
                delayed_queue=delayed_queue,
                delayed_enabled=config["delayed_reactions_enabled"],
                placeholder_text_enabled=config["placeholder_text_enabled"],
            )
            traces.append(res.trace_entry)
            state = res.trace_entry["next_hidden_state"]
            delayed_queue = res.delayed_queue_out

            if res.trace_entry["selected_reaction"] == "Reaction_New_Observation" and "Fragment_1" not in known_fragments:
                known_fragments = sorted(set(known_fragments + ["Fragment_1"]))

    run_meta = {
        "run_name": config.get("run_name", "lab_run"),
        "seed": config["seed"],
        "iterations": config["iterations"],
        "max_steps_per_iteration": config["max_steps_per_iteration"],
        "variation_mode": config["variation_mode"],
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    payload = build_metrics(config, traces, run_meta)
    return payload, traces


def main():
    parser = argparse.ArgumentParser(description="Run autonomous lab simulations and emit comparison-ready logs.")
    parser.add_argument("--config", default="tools/lab_config.json", help="Path to lab config JSON")
    parser.add_argument("--seed", type=int, help="Override seed")
    parser.add_argument("--iterations", type=int, help="Override iterations")
    parser.add_argument("--variation-mode", choices=["deterministic", "bounded"], help="Override variation mode")
    parser.add_argument("--no-archive", action="store_true", help="Disable archive output for this run")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    if args.seed is not None:
        config["seed"] = args.seed
    if args.iterations is not None:
        config["iterations"] = args.iterations
    if args.variation_mode is not None:
        config["variation_mode"] = args.variation_mode
    if args.no_archive:
        config["archive_results"] = False

    payload, traces = run_sim(config)
    write_outputs(Path("docs/lab/results"), payload, traces, archive=config.get("archive_results", True))
    print("Lab run complete.")
    print(f"Seed={payload['run_metadata']['seed']} iterations={payload['run_metadata']['iterations']} total_steps={payload['metrics']['total_steps']}")


if __name__ == "__main__":
    main()
