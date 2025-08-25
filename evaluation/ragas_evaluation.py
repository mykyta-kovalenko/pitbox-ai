"""RAGAS evaluation for NASCAR RAG system."""

import asyncio
import os
from typing import Dict, List

import numpy as np
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_correctness,
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)

from app.tools.rag_knowledge import get_knowledge_rag

# Constants
METRIC_NAMES = [
    "faithfulness",
    "answer_relevancy", 
    "context_precision",
    "context_recall",
    "answer_correctness",
]
DEFAULT_NUM_RUNS = 5
STABILITY_THRESHOLD = 0.1


class RAGASEvaluator:
    """Evaluates RAG system using RAGAS metrics."""

    def __init__(self):
        self.rag = get_knowledge_rag()
        self.metrics = [
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
            answer_correctness,
        ]

    def create_test_dataset(self) -> Dataset:
        """Create test dataset for evaluation."""
        test_data = [
            {
                "question": "Who are the current drivers for Trackhouse Racing?",
                "ground_truth": (
                    "The current drivers for Trackhouse Racing are Ross Chastain "
                    "driving the No. 1 Chevrolet, Daniel Suárez driving the No. 99 "
                    "Chevrolet, and Shane van Gisbergen driving the No. 88 Chevrolet."
                ),
            },
            {
                "question": "What is the yellow flag in NASCAR?",
                "ground_truth": (
                    "The yellow flag brings the race to a slowed pace and indicates a "
                    "caution period on-track due to a crash or debris that would impede "
                    "the race from continuing under full-speed conditions. When the flag "
                    "waves, the pace car enters the track and controls the field behind it."
                ),
            },
            {
                "question": "How long is Daytona International Speedway?",
                "ground_truth": (
                    "Daytona International Speedway is 2.5 miles long with 31-degree "
                    "high banks and is a tri-oval track."
                ),
            },
            {
                "question": "What is pit road in NASCAR?",
                "ground_truth": (
                    "Pit road is where teams service the race cars. This is where teams "
                    "make adjustments on the car, fuel stops, tire changes and fix damage "
                    "to the race cars. Pit road has specific speed limits that must be observed."
                ),
            },
            {
                "question": "Who owns Trackhouse Racing?",
                "ground_truth": (
                    "Trackhouse Racing is owned by Justin Marks and rapper Pitbull "
                    "(Armando Christian Pérez)."
                ),
            },
            {
                "question": "What are superspeedways in NASCAR?",
                "ground_truth": (
                    "Superspeedways are tracks that are 2.5 miles and bigger and feature "
                    "more drafting and pack racing. On the current schedule those are "
                    "Daytona International Speedway and Talladega Superspeedway."
                ),
            },
            {
                "question": "How many stages are in NASCAR Cup Series races?",
                "ground_truth": (
                    "Each race is typically comprised of three stages (Stage 1, Stage 2 "
                    "and the Final Stage; the Coca-Cola 600 has four stages). Stage winners "
                    "earn playoff points and regular season points."
                ),
            },
            {
                "question": "What is Bristol Motor Speedway known for?",
                "ground_truth": (
                    "Bristol Motor Speedway is a concrete half-mile track nicknamed "
                    "'The World's Fastest Half-Mile,' 'Thunder Valley' and 'The Last "
                    "Great Colosseum.' It features 24 degrees of banking through the turns."
                ),
            },
        ]

        # Generate answers and contexts using the RAG system
        questions = [item["question"] for item in test_data]
        ground_truths = [item["ground_truth"] for item in test_data]

        answers = []
        contexts = []

        for question in questions:
            # Get retriever results for context
            retrieved_docs = self.rag.retriever.invoke(question)
            context_list = [doc.page_content for doc in retrieved_docs]
            contexts.append(context_list)

            # Get RAG answer
            answer = self.rag.invoke(question)
            answers.append(answer)

        return Dataset.from_dict(
            {
                "question": questions,
                "answer": answers,
                "contexts": contexts,
                "ground_truth": ground_truths,
            }
        )

    def run_evaluation(self) -> Dict:
        """Run RAGAS evaluation."""
        dataset = self.create_test_dataset()
        result = evaluate(dataset, metrics=self.metrics)
        return result

    def run_reliability_test(self, num_runs: int = DEFAULT_NUM_RUNS) -> Dict:
        """Run multiple evaluations to test metric reliability."""
        print(f"Running reliability test with {num_runs} runs...")

        all_results = []

        for _ in range(num_runs):
            result = self.run_evaluation()

            df = result.to_pandas()
            run_scores = {}
            for metric_name in METRIC_NAMES:
                if metric_name in df.columns:
                    run_scores[metric_name] = df[metric_name].mean()
            all_results.append(run_scores)

        return self.analyze_reliability(all_results)

    def analyze_reliability(self, all_results: List[Dict]) -> Dict:
        """Analyze reliability across multiple runs."""
        metrics_data = {}

        for metric_name in METRIC_NAMES:
            scores = [
                run.get(metric_name, 0)
                for run in all_results
                if run.get(metric_name) is not None
            ]
            if scores:
                metrics_data[metric_name] = {
                    "scores": scores,
                    "mean": np.mean(scores),
                    "std": np.std(scores),
                    "min": np.min(scores),
                    "max": np.max(scores),
                    "cv": np.std(scores) / np.mean(scores)
                    if np.mean(scores) > 0
                    else 0,
                }

        return {"reliability_analysis": metrics_data, "all_runs": all_results}

    def print_results(self, results):
        """Print evaluation results in a formatted way."""
        print("\n" + "=" * 50)
        print("RAGAS EVALUATION RESULTS")
        print("=" * 50)

        df = results.to_pandas()
        for metric_name in METRIC_NAMES:
            if metric_name in df.columns:
                score = df[metric_name].mean()
                print(f"{metric_name:.<30} {score:.3f}")

        print("=" * 50)

    def print_reliability_results(self, reliability_data: Dict):
        """Print reliability test results"""
        print("\n" + "=" * 60)
        print("RAGAS RELIABILITY TEST RESULTS")
        print("=" * 60)

        analysis = reliability_data["reliability_analysis"]

        for metric_name, data in analysis.items():
            print(f"\n{metric_name.upper()}:")
            print(f"  Mean:     {data['mean']:.3f}")
            print(f"  Std Dev:  {data['std']:.3f}")
            print(f"  Min:      {data['min']:.3f}")
            print(f"  Max:      {data['max']:.3f}")
            print(
                f"  CV:       {data['cv']:.3f} ({'STABLE' if data['cv'] < 0.1 else 'VOLATILE'})"
            )
            print(f"  Scores:   {[f'{s:.3f}' for s in data['scores']]}")

        print("\n" + "=" * 60)
        print("RELIABILITY SUMMARY:")
        print("=" * 60)

        stable_metrics = []
        volatile_metrics = []

        for metric_name, data in analysis.items():
            if data["cv"] < STABILITY_THRESHOLD:
                stable_metrics.append(f"{metric_name} (CV: {data['cv']:.3f})")
            else:
                volatile_metrics.append(f"{metric_name} (CV: {data['cv']:.3f})")

        if stable_metrics:
            print(f"✅ STABLE METRICS ({len(stable_metrics)}):")
            for metric in stable_metrics:
                print(f"   • {metric}")

        if volatile_metrics:
            print(f"⚠️  VOLATILE METRICS ({len(volatile_metrics)}):")
            for metric in volatile_metrics:
                print(f"   • {metric}")
        else:
            print("🎯 ALL METRICS ARE STABLE!")

        print("=" * 60)

    def save_results(self, results, filename: str = "ragas_results.json"):
        """Save results to file."""
        import json

        results_path = os.path.join("evaluation", filename)
        os.makedirs("evaluation", exist_ok=True)

        df = results.to_pandas() if hasattr(results, "to_pandas") else None
        if df is not None:
            serializable_results = {
                col: float(df[col].mean())
                for col in df.columns
                if col in METRIC_NAMES
            }
        else:
            serializable_results = results

        with open(results_path, "w") as f:
            json.dump(serializable_results, f, indent=2)


async def main():
    """Main evaluation function."""
    evaluator = RAGASEvaluator()
    
    reliability_results = evaluator.run_reliability_test()
    evaluator.print_reliability_results(reliability_results)
    evaluator.save_results(reliability_results, "ragas_reliability_results.json")


if __name__ == "__main__":
    asyncio.run(main())
