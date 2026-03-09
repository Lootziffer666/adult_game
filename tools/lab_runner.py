#!/usr/bin/env python3
import argparse
import csv
import json
import random
from collections import Counter
from copy import deepcopy
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
    "Reaction_Evidence_Helps",
]

BASE_PLACEHOLDERS = {
    "Reaction_Warmer_Guarded": "The reaction is warmer but still guarded.",
    "Reaction_No_Open": "Nothing opens at this time.",
    "Reaction_New_Observation": "A new observation is recorded.",
    "Reaction_Delayed_Shift": "This action changes later availability.",
    "Reaction_Less_Private": "The current context makes the space feel less private.",
    "Reaction_Fragment_Relevant_NotEnough": "The fragment matters here, but not yet enough.",
    "Reaction_Risk_Pushback": "The response hardens after boundary pressure.",
    "Reaction_Context_Aligned": "Timing and context align; response quality improves.",
    "Reaction_Evidence_Helps": "A presented clue makes the response more specific.",
}


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def nowstamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def build_maps(config: Dict) -> Tuple[Dict, Dict]:
    contexts = {c["id"]: c for c in config["contexts"]}
    presets = {p["id"]: p for p in config["state_presets"]}
    return contexts, presets


def render_placeholder(reaction: str, context: Dict, action: str, placeholder_on: bool) -> str:
    if not placeholder_on:
        return reaction

    base = BASE_PLACEHOLDERS[reaction]
    tags = []
    if context["time"] == "Night":
        tags.append("night")
    if context.get("privacy", 0.5) < 0.5:
        tags.append("low-privacy")
    if action == "Action_Return_Later":
        tags.append("return-later")
    if tags:
        return f"{base} [{', '.join(tags)}]"
    return base


def build_eligible_reactions(
    context: Dict,
    action: str,
    known_fragments: List[str],
    state: Dict,
    scenario: Dict,
    object_enabled: bool,
) -> List[str]:
    eligible = ["Reaction_No_Open"]

    if action == "Action_Observe":
        eligible.append("Reaction_New_Observation")

    if action == "Action_Ask":
        if context["time"] in ["Evening", "Night"]:
            eligible.append("Reaction_Warmer_Guarded" if state["trust"] >= 0.35 else "Reaction_Fragment_Relevant_NotEnough")
        if "Fragment_1" in known_fragments:
            eligible.append("Reaction_Context_Aligned")

    if action == "Action_Test_Boundary":
        eligible.append("Reaction_Risk_Pushback")
        if context["privacy"] < 0.55:
            eligible.append("Reaction_Less_Private")

    if action == "Action_Return_Later":
        eligible.append("Reaction_Delayed_Shift")

    if action == "Action_Present_Evidence" and object_enabled:
        if scenario.get("object_evidence") and ("Fragment_1" in known_fragments or scenario.get("memory_flag")):
            eligible.append("Reaction_Evidence_Helps")
        else:
            eligible.append("Reaction_Fragment_Relevant_NotEnough")

    return sorted(set(eligible))


def score_reaction(reaction: str, context: Dict, state: Dict, action: str, params: Dict) -> float:
    base = {
        "Reaction_No_Open": 0.1,
        "Reaction_New_Observation": 0.45,
        "Reaction_Warmer_Guarded": 0.68,
        "Reaction_Delayed_Shift": 0.55,
        "Reaction_Less_Private": 0.5,
        "Reaction_Fragment_Relevant_NotEnough": 0.44,
        "Reaction_Risk_Pushback": 0.6,
        "Reaction_Context_Aligned": 0.72,
        "Reaction_Evidence_Helps": 0.7,
    }[reaction]

    score = base
    if reaction in ["Reaction_Context_Aligned", "Reaction_Warmer_Guarded", "Reaction_Evidence_Helps"]:
        score += params["hint_weight"] * (0.12 if state["curiosity"] > 0.45 else 0.0)
    if reaction == "Reaction_Context_Aligned":
        score += params["context_weight"] * (0.1 if context["time"] in ["Evening", "Night"] else -0.03)
    if reaction == "Reaction_Warmer_Guarded":
        score += params["hidden_state_weight"] * 0.18 * state["trust"]
    if reaction == "Reaction_Risk_Pushback":
        score += params["hidden_state_weight"] * 0.15 * state["tension"]
    if reaction == "Reaction_No_Open":
        score -= params["no_op_penalty"] * 0.15
    if reaction == "Reaction_Delayed_Shift":
        score += params["timing_weight"] * (0.1 if action == "Action_Return_Later" else 0.0)
    if reaction == "Reaction_Evidence_Helps":
        score += params["object_evidence_weight"] * 0.18

    return score


def apply_state_change(state: Dict, reaction: str, action: str) -> Tuple[Dict, List[str]]:
    nxt = deepcopy(state)
    new_info = []

    if action == "Action_Observe":
        nxt["curiosity"] = clamp(nxt["curiosity"] + 0.1)
        new_info.append("Observation candidate recorded.")

    if reaction == "Reaction_Warmer_Guarded":
        nxt["trust"] = clamp(nxt["trust"] + 0.1)
        nxt["tension"] = clamp(nxt["tension"] - 0.04)
        new_info.append("Trust increased slightly.")
    elif reaction == "Reaction_Risk_Pushback":
        nxt["trust"] = clamp(nxt["trust"] - 0.08)
        nxt["tension"] = clamp(nxt["tension"] + 0.1)
        new_info.append("Boundary resistance increased.")
    elif reaction == "Reaction_No_Open":
        nxt["curiosity"] = clamp(nxt["curiosity"] - 0.02)
    elif reaction == "Reaction_New_Observation":
        nxt["curiosity"] = clamp(nxt["curiosity"] + 0.08)
    elif reaction == "Reaction_Context_Aligned":
        nxt["trust"] = clamp(nxt["trust"] + 0.06)
        new_info.append("Context alignment signal recorded.")
    elif reaction == "Reaction_Evidence_Helps":
        nxt["trust"] = clamp(nxt["trust"] + 0.07)
        nxt["curiosity"] = clamp(nxt["curiosity"] + 0.04)
        new_info.append("Evidence-linked response unlocked.")

    return nxt, new_info


def run_candidate(config: Dict, candidate: Dict, scenario_repeats: int, seed: int) -> Tuple[Dict, List[Dict]]:
    rng = random.Random(seed)
    contexts, presets = build_maps(config)
    traces: List[Dict] = []

    scenario_bundle = config["scenario_bundle"]
    delayed_on = config.get("delayed_reactions_enabled", True)
    placeholder_on = config.get("placeholder_text_enabled", True)
    object_on = config.get("object_evidence_enabled", True)

    iter_id = 0
    for rep in range(scenario_repeats):
        order = list(range(len(scenario_bundle)))
        if config.get("variation_mode", "bounded") == "bounded":
            rng.shuffle(order)
        for idx in order:
            iter_id += 1
            scenario = scenario_bundle[idx]
            context = contexts[scenario["context_id"]]
            preset = presets[scenario["state_preset_id"]]
            state = {"trust": preset["trust"], "curiosity": preset["curiosity"], "tension": preset["tension"]}
            known_fragments = list(scenario.get("known_fragments", []))
            delayed_queue = []
            state_signatures = set()

            for step_i, action in enumerate(scenario.get("action_sequence", []), start=1):
                immediate = True
                source = "immediate"

                if delayed_queue and delayed_on:
                    selected = delayed_queue.pop(0)["reaction"]
                    eligible = [selected]
                    immediate = False
                    source = "delayed"
                else:
                    eligible = build_eligible_reactions(context, action, known_fragments, state, scenario, object_on)
                    selected = max(eligible, key=lambda r: score_reaction(r, context, state, action, candidate))

                if delayed_on and selected == "Reaction_Delayed_Shift" and state["curiosity"] >= candidate["delayed_threshold"]:
                    delayed_queue.append({"reaction": "Reaction_Context_Aligned"})

                notes = render_placeholder(selected, context, action, placeholder_on)
                nxt, unlocked = apply_state_change(state, selected, action)

                if selected == "Reaction_New_Observation" and "Fragment_1" not in known_fragments:
                    known_fragments.append("Fragment_1")
                    known_fragments = sorted(set(known_fragments))

                if scenario.get("memory_flag") and selected in ["Reaction_New_Observation", "Reaction_Context_Aligned"]:
                    unlocked.append("Memory flag changed follow-up readiness.")

                signature = (
                    round(nxt["trust"], 2),
                    round(nxt["curiosity"], 2),
                    round(nxt["tension"], 2),
                    action,
                    context["id"],
                )
                repeated_collapse = signature in state_signatures
                state_signatures.add(signature)

                traces.append(
                    {
                        "iteration_id": iter_id,
                        "step_index": step_i,
                        "scenario_id": scenario["id"],
                        "time_context": {"id": context["id"], "space": context["space"], "time": context["time"]},
                        "known_fragments": list(known_fragments),
                        "hidden_state": deepcopy(state),
                        "chosen_action": action,
                        "eligible_reactions": eligible,
                        "selected_reaction": selected,
                        "source": source,
                        "immediate_or_delayed": "immediate" if immediate else "delayed",
                        "newly_unlocked_information": unlocked,
                        "notes": notes,
                        "next_hidden_state": nxt,
                        "repeated_state_collapse": repeated_collapse,
                    }
                )
                state = nxt

    return summarize_run(config, traces, candidate), traces


def summarize_run(config: Dict, traces: List[Dict], candidate: Dict) -> Dict:
    selected = [t["selected_reaction"] for t in traces]
    notes = [t["notes"] for t in traces]
    unique_reactions = sorted(set(selected))
    no_open_freq = selected.count("Reaction_No_Open") / max(1, len(traces))
    delayed_count = sum(1 for t in traces if t["immediate_or_delayed"] == "delayed")
    delayed_freq = delayed_count / max(1, len(traces))
    repeated_collapse_count = sum(1 for t in traces if t.get("repeated_state_collapse"))

    action_ctx = {(t["chosen_action"], t["time_context"]["id"], t["selected_reaction"]) for t in traces}
    action_context_sensitivity = len(action_ctx)

    by_pair = {}
    for t in traces:
        k = f"{t['time_context']['id']}::{t['chosen_action']}"
        by_pair.setdefault(k, set()).add(t["selected_reaction"])
    no_diff_pairs = sorted([k for k, v in by_pair.items() if len(v) == 1])

    hint_useful = sum(1 for t in traces if t["known_fragments"] and t["selected_reaction"] in [
        "Reaction_Context_Aligned", "Reaction_Warmer_Guarded", "Reaction_New_Observation", "Reaction_Evidence_Helps"
    ])
    hint_usefulness = hint_useful / max(1, len(traces))

    reaction_counter = Counter(selected)
    same_reaction_dominance = max(reaction_counter.values()) / max(1, len(traces))
    dead_path_ratio = len(no_diff_pairs) / max(1, len(by_pair))

    reaction_diversity = len(unique_reactions) / len(ALL_REACTIONS)
    note_diversity = len(set(notes)) / max(1, len(traces))
    delayed_balance = 1.0 - abs(delayed_freq - 0.15)
    delayed_balance = clamp(delayed_balance, 0.0, 1.0)
    readability_score = (
        0.45 * reaction_diversity +
        0.3 * note_diversity +
        0.25 * delayed_balance
    )

    metrics = {
        "total_iterations": len(set(t["iteration_id"] for t in traces)),
        "total_steps": len(traces),
        "unique_reactions_triggered": len(unique_reactions),
        "unique_reaction_ids": unique_reactions,
        "reactions_never_triggered": sorted([r for r in ALL_REACTIONS if r not in unique_reactions]),
        "branch_differentiation_count": len(unique_reactions),
        "empty_noop_reaction_frequency": round(no_open_freq, 3),
        "delayed_reaction_frequency": round(delayed_freq, 3),
        "immediate_reaction_count": len(traces) - delayed_count,
        "delayed_reaction_count": delayed_count,
        "hint_usefulness_score": round(hint_usefulness, 3),
        "action_context_sensitivity": action_context_sensitivity,
        "repeated_state_collapse_count": repeated_collapse_count,
        "contexts_actions_with_no_meaningful_difference": no_diff_pairs,
        "same_reaction_dominance": round(same_reaction_dominance, 3),
        "dead_path_ratio": round(dead_path_ratio, 3),
        "readability_score": round(readability_score, 3),
    }

    warnings = []
    if metrics["empty_noop_reaction_frequency"] > 0.45:
        warnings.append("High no-op frequency.")
    if metrics["unique_reactions_triggered"] < 4:
        warnings.append("Low unique reaction coverage.")
    if metrics["same_reaction_dominance"] > 0.4:
        warnings.append("Single reaction dominates too often.")
    metrics["loop_stagnation_warnings"] = warnings

    return {
        "candidate_parameters": candidate,
        "metrics": metrics,
    }


def aggregate_score(summary: Dict, tuning_cfg: Dict) -> float:
    m = summary["metrics"]
    w = tuning_cfg["evaluation_weights"]

    delayed_quality = 1.0 - abs(m["delayed_reaction_frequency"] - 0.15)
    delayed_quality = clamp(delayed_quality, 0.0, 1.0)
    if m["delayed_reaction_frequency"] == 0.0:
        delayed_quality = max(0.0, delayed_quality - 0.35)

    score = 0.0
    score += w["unique_reactions_triggered"] * m["unique_reactions_triggered"]
    score += w["branch_differentiation_count"] * m["branch_differentiation_count"]
    score += w["hint_usefulness_score"] * m["hint_usefulness_score"]
    score += w["action_context_sensitivity"] * (m["action_context_sensitivity"] / 20.0)
    score += w["readability_score"] * m["readability_score"]
    score += w["empty_noop_reaction_frequency"] * m["empty_noop_reaction_frequency"]
    score += w["repeated_state_collapse_count"] * (m["repeated_state_collapse_count"] / 20.0)
    score += w["same_reaction_dominance"] * m["same_reaction_dominance"]
    score += w["dead_path_ratio"] * m["dead_path_ratio"]
    score += w["delayed_usage_quality"] * delayed_quality
    return round(score, 5)


def mutate_candidate(base: Dict, rng: random.Random, strength: float) -> Dict:
    out = deepcopy(base)
    for k, v in out.items():
        delta = rng.uniform(-strength, strength)
        if k in ["delayed_threshold"]:
            out[k] = round(clamp(v + delta, 0.2, 0.9), 4)
        else:
            out[k] = round(clamp(v + delta, 0.2, 2.0), 4)
    return out


def tune(config: Dict, result_dir: Path, seed_override: int = None) -> Dict:
    tuning_cfg = config["tuning"]
    rng = random.Random(seed_override if seed_override is not None else config["seed"])

    baseline = deepcopy(tuning_cfg["base_parameters"])
    repeats = tuning_cfg.get("scenario_repeats", 2)

    baseline_summary, baseline_traces = run_candidate(config, baseline, repeats, seed=rng.randint(1, 10_000_000))
    baseline_score = aggregate_score(baseline_summary, tuning_cfg)

    beam = [{"params": baseline, "summary": baseline_summary, "score": baseline_score, "trace": baseline_traces}]
    history = []

    for gen in range(1, tuning_cfg["generations"] + 1):
        candidates = []
        seeds = [rng.randint(1, 10_000_000) for _ in range(tuning_cfg["population_size"])]

        # Keep current beam members
        for b in beam:
            candidates.append(b)

        while len(candidates) < tuning_cfg["population_size"]:
            parent = rng.choice(beam)
            child_params = mutate_candidate(parent["params"], rng, tuning_cfg["mutation_strength"])
            summary, traces = run_candidate(config, child_params, repeats, seed=seeds[len(candidates) % len(seeds)])
            score = aggregate_score(summary, tuning_cfg)
            candidates.append({"params": child_params, "summary": summary, "score": score, "trace": traces})

        candidates = sorted(candidates, key=lambda c: c["score"], reverse=True)
        beam = candidates[: tuning_cfg["beam_width"]]

        history.append(
            {
                "generation": gen,
                "best_score": beam[0]["score"],
                "median_score": candidates[len(candidates) // 2]["score"],
                "worst_score": candidates[-1]["score"],
                "best_metrics": beam[0]["summary"]["metrics"],
            }
        )

    best = beam[0]
    verdict = "improved" if best["score"] > baseline_score + 0.05 else ("worsened" if best["score"] < baseline_score - 0.05 else "unclear")
    confidence = "high" if abs(best["score"] - baseline_score) > 0.5 else ("medium" if abs(best["score"] - baseline_score) > 0.15 else "low")

    scope_growth = "no, current scope is sufficient for tuning"
    if best["summary"]["metrics"]["unique_reactions_triggered"] < 5:
        scope_growth = "yes, current scope is too small and causes misleading optimization"
    elif len(best["summary"]["metrics"]["contexts_actions_with_no_meaningful_difference"]) > 8:
        scope_growth = "partly, add 2-3 more micro-scenarios"

    report = {
        "tuning_metadata": {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "seed": config["seed"],
            "generations": tuning_cfg["generations"],
            "population_size": tuning_cfg["population_size"],
            "beam_width": tuning_cfg["beam_width"],
            "scenario_repeats": repeats,
        },
        "verdict": {"overall": verdict, "confidence": confidence, "scope_growth": scope_growth},
        "baseline": {"score": baseline_score, **baseline_summary},
        "best_candidate": {"score": best["score"], **best["summary"]},
        "score_delta": round(best["score"] - baseline_score, 5),
        "generation_history": history,
    }

    write_tuning_outputs(result_dir, report, baseline, best)
    return report


def write_latest_outputs(result_dir: Path, payload: Dict, traces: List[Dict], archive: bool):
    result_dir.mkdir(parents=True, exist_ok=True)
    archive_dir = result_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)

    out = deepcopy(payload)
    out["trace"] = traces

    (result_dir / "latest_run.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    with (result_dir / "latest_run.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "iteration_id", "step_index", "scenario_id", "context_id", "space", "time", "action", "selected_reaction",
            "immediate_or_delayed", "known_fragments", "trust", "curiosity", "tension", "notes"
        ])
        for t in traces:
            hs = t["hidden_state"]
            w.writerow([
                t["iteration_id"], t["step_index"], t["scenario_id"], t["time_context"]["id"], t["time_context"]["space"], t["time_context"]["time"],
                t["chosen_action"], t["selected_reaction"], t["immediate_or_delayed"],
                ";".join(t["known_fragments"]), hs["trust"], hs["curiosity"], hs["tension"], t["notes"]
            ])

    m = payload["metrics"]
    md = [
        "# Latest Lab Run Summary",
        "",
        f"- Seed: `{payload.get('seed', 'n/a')}`",
        f"- Scenario repeats: `{payload.get('scenario_repeats', 'n/a')}`",
        f"- Total steps: `{m['total_steps']}`",
        "",
        "## Comparison-friendly summary",
        f"- Unique reactions triggered: `{m['unique_reactions_triggered']}` ({', '.join(m['unique_reaction_ids'])})",
        f"- Reactions never triggered: `{', '.join(m['reactions_never_triggered']) if m['reactions_never_triggered'] else 'none'}`",
        f"- Branch differentiation count: `{m['branch_differentiation_count']}`",
        f"- Empty/no-op frequency: `{m['empty_noop_reaction_frequency']}`",
        f"- Delayed reaction frequency: `{m['delayed_reaction_frequency']}`",
        f"- Hint usefulness score: `{m['hint_usefulness_score']}`",
        f"- Action-context sensitivity: `{m['action_context_sensitivity']}`",
        f"- Readability score: `{m['readability_score']}`",
        f"- Repeated state collapse count: `{m['repeated_state_collapse_count']}`",
        f"- Potential stagnation warnings: `{'; '.join(m['loop_stagnation_warnings']) if m['loop_stagnation_warnings'] else 'none'}`",
        "",
        "## Context/action with no meaningful difference",
    ]
    if m["contexts_actions_with_no_meaningful_difference"]:
        md.extend([f"- `{x}`" for x in m["contexts_actions_with_no_meaningful_difference"]])
    else:
        md.append("- none")
    (result_dir / "latest_run.md").write_text("\n".join(md), encoding="utf-8")

    if archive:
        (archive_dir / f"run_{nowstamp()}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")


def write_tuning_outputs(result_dir: Path, report: Dict, baseline_params: Dict, best: Dict):
    result_dir.mkdir(parents=True, exist_ok=True)

    (result_dir / "latest_tuning_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    best_payload = {
        "score": best["score"],
        "candidate_parameters": best["params"],
        "metrics": best["summary"]["metrics"],
        "trace": best["trace"],
    }
    (result_dir / "best_candidate.json").write_text(json.dumps(best_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    base_m = report["baseline"]["metrics"]
    best_m = report["best_candidate"]["metrics"]
    changed_params = []
    for k in baseline_params:
        if abs(best["params"][k] - baseline_params[k]) > 1e-9:
            changed_params.append((k, baseline_params[k], best["params"][k]))

    improvements = []
    regressions = []
    for k in [
        "unique_reactions_triggered",
        "branch_differentiation_count",
        "hint_usefulness_score",
        "action_context_sensitivity",
        "readability_score",
        "empty_noop_reaction_frequency",
        "repeated_state_collapse_count",
        "same_reaction_dominance",
        "dead_path_ratio",
    ]:
        delta = best_m[k] - base_m[k]
        if k in ["empty_noop_reaction_frequency", "repeated_state_collapse_count", "same_reaction_dominance", "dead_path_ratio"]:
            if delta < 0:
                improvements.append((k, delta))
            elif delta > 0:
                regressions.append((k, delta))
        else:
            if delta > 0:
                improvements.append((k, delta))
            elif delta < 0:
                regressions.append((k, delta))

    md = [
        "# TUNING VERDICT",
        f"Overall: **{report['verdict']['overall']}**",
        f"Confidence: **{report['verdict']['confidence']}**",
        "",
        "## Baseline summary",
        f"- Score: `{report['baseline']['score']}`",
        f"- Unique reactions: `{base_m['unique_reactions_triggered']}`",
        f"- No-op frequency: `{base_m['empty_noop_reaction_frequency']}`",
        f"- Readability score: `{base_m['readability_score']}`",
        "",
        "## Best candidate summary",
        f"- Score: `{report['best_candidate']['score']}`",
        f"- Unique reactions: `{best_m['unique_reactions_triggered']}`",
        f"- No-op frequency: `{best_m['empty_noop_reaction_frequency']}`",
        f"- Readability score: `{best_m['readability_score']}`",
        f"- Score delta vs baseline: `{report['score_delta']}`",
        "",
        "## Main improvements",
    ]
    md.extend([f"- `{k}` changed by `{round(v, 3)}`" for k, v in improvements[:8]] or ["- none clear"])
    md.append("")
    md.append("## Main regressions")
    md.extend([f"- `{k}` changed by `{round(v, 3)}`" for k, v in regressions[:8]] or ["- none clear"])
    md.append("")
    md.append("## Parameters changed most")
    changed_params = sorted(changed_params, key=lambda x: abs(x[2] - x[1]), reverse=True)
    md.extend([f"- `{k}`: `{a}` -> `{b}`" for k, a, b in changed_params[:10]] or ["- none"])
    md.append("")
    repetitive_note = "yes" if best_m["same_reaction_dominance"] > 0.35 else "no"
    md.append(f"- System still too repetitive? **{repetitive_note}**")
    md.append("- Recommended next step: keep tuning if verdict is improved; expand scenarios only when stagnation warnings persist.")
    md.append("")
    md.append("# SHOULD THE LAB SCOPE GROW?")
    md.append(f"- Verdict: **{report['verdict']['scope_growth']}**")

    (result_dir / "latest_tuning_report.md").write_text("\n".join(md), encoding="utf-8")

    bvb = [
        "# Baseline vs Best Candidate",
        "",
        f"- Baseline score: `{report['baseline']['score']}`",
        f"- Best score: `{report['best_candidate']['score']}`",
        f"- Delta: `{report['score_delta']}`",
        "",
        "## Metric deltas",
    ]
    for k in [
        "unique_reactions_triggered",
        "branch_differentiation_count",
        "empty_noop_reaction_frequency",
        "delayed_reaction_frequency",
        "hint_usefulness_score",
        "action_context_sensitivity",
        "repeated_state_collapse_count",
        "same_reaction_dominance",
        "dead_path_ratio",
        "readability_score",
    ]:
        bvb.append(f"- `{k}`: `{base_m[k]}` -> `{best_m[k]}`")
    (result_dir / "baseline_vs_best.md").write_text("\n".join(bvb), encoding="utf-8")


def run_standard(config: Dict, result_dir: Path):
    params = deepcopy(config["tuning"]["base_parameters"])
    summary, traces = run_candidate(config, params, scenario_repeats=1, seed=config["seed"])
    payload = {
        "run_name": config.get("run_name", "baseline_lab"),
        "seed": config["seed"],
        "scenario_repeats": 1,
        "candidate_parameters": params,
        "metrics": summary["metrics"],
    }
    write_latest_outputs(result_dir, payload, traces, archive=config.get("archive_results", True))
    print("Lab run complete.")
    print(f"Seed={config['seed']} total_steps={summary['metrics']['total_steps']} unique_reactions={summary['metrics']['unique_reactions_triggered']}")


def main():
    parser = argparse.ArgumentParser(description="Standalone lab runner with bounded autonomous tuning.")
    parser.add_argument("--config", default="tools/lab_config.json", help="Path to lab config JSON")
    parser.add_argument("--seed", type=int, help="Override seed")
    parser.add_argument("--iterations", type=int, help="Compatibility override (maps to tuning scenario repeats)")
    parser.add_argument("--variation-mode", choices=["deterministic", "bounded"], help="Override variation mode")
    parser.add_argument("--no-archive", action="store_true", help="Disable archive output for standard runs")
    parser.add_argument("--tune", action="store_true", help="Run bounded autonomous tuning loop")
    parser.add_argument("--generations", type=int, help="Override tuning generations")
    parser.add_argument("--population", type=int, help="Override tuning population size")
    parser.add_argument("--mutation", type=float, help="Override mutation strength")
    args = parser.parse_args()

    config = load_json(Path(args.config))
    if args.seed is not None:
        config["seed"] = args.seed
    if args.variation_mode is not None:
        config["variation_mode"] = args.variation_mode
    if args.no_archive:
        config["archive_results"] = False
    if args.iterations is not None:
        config["tuning"]["scenario_repeats"] = max(1, args.iterations)
    if args.generations is not None:
        config["tuning"]["generations"] = max(1, args.generations)
    if args.population is not None:
        config["tuning"]["population_size"] = max(2, args.population)
    if args.mutation is not None:
        config["tuning"]["mutation_strength"] = clamp(args.mutation, 0.01, 0.4)

    result_dir = Path("docs/lab/results")

    if args.tune:
        report = tune(config, result_dir, seed_override=config["seed"])
        print("Tuning run complete.")
        print(f"Verdict={report['verdict']['overall']} confidence={report['verdict']['confidence']} delta={report['score_delta']}")
    else:
        run_standard(config, result_dir)


if __name__ == "__main__":
    main()
