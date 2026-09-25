import argparse

from deco import config
from deco.evaluation.eval import evaluate_mquake
from deco.pipeline import DeCOPipeline
from deco.utils.data import load_json
from deco.utils.retrieval import ContrieverRetriever


def parse_args():
    parser = argparse.ArgumentParser(description="DeCO evaluation on MQuAKE")
    parser.add_argument(
        "--backend",
        choices=("vllm", "dmx", "openrouter"),
        default="vllm",
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="Path to MQuAKE-CF-3k-v2.json.",
    )
    parser.add_argument(
        "--full-dataset",
        required=True,
        help="Path to MQuAKE-CF.json used for demonstrations.",
    )
    parser.add_argument(
        "--contriever-model",
        required=True,
        help="Local Contriever path or compatible Hugging Face model ID.",
    )
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--max-iterations", type=int, default=7)
    parser.add_argument(
        "--question-workers",
        type=int,
        default=config.QUESTION_WORKERS,
    )
    return parser.parse_args()


def main():
    args = parse_args()
    dataset = load_json(args.dataset)
    full_dataset = load_json(args.full_dataset)

    print("Loading Contriever and building embeddings...")
    retriever = ContrieverRetriever(
        model_path=args.contriever_model,
        device=args.device,
    )
    pipeline = DeCOPipeline(
        backend=args.backend,
        retriever=retriever,
        dataset=dataset,
        full_dataset=full_dataset,
        max_iterations=args.max_iterations,
    )

    print("=" * 70)
    print("DeCO MQuAKE Evaluation")
    print(f"Backend          : {args.backend}")
    print(f"Question workers : {args.question_workers}")
    print(f"Conflict workers : {config.CONFLICT_WORKERS}")
    print(f"Dataset size     : {len(dataset)}")
    print("=" * 70)

    result = evaluate_mquake(
        dataset,
        pipeline,
        question_workers=args.question_workers,
    )

    print("\n" + "=" * 70)
    print(
        f"Multi-hop acc = {result['accuracy']:.4f} "
        f"({result['correct']} / {result['total']})"
    )
    print(f"Completed = {result['completed']}")
    print(f"Failed    = {result['failed']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
