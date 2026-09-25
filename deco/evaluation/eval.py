"""Concurrent MQuAKE evaluation."""

from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm


def evaluate_mquake(dataset, pipeline, question_workers):
    total = len(dataset)
    correct = 0
    completed = 0
    failed = 0

    if total == 0:
        return {
            "correct": 0,
            "completed": 0,
            "failed": 0,
            "total": 0,
            "accuracy": 0.0,
        }

    workers = min(question_workers, total)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_index = {
            executor.submit(pipeline.process_question, item): index
            for index, item in enumerate(dataset)
        }

        progress = tqdm(
            as_completed(future_to_index),
            total=total,
            desc="Questions",
        )

        for future in progress:
            index = future_to_index[future]
            completed += 1

            try:
                result = future.result()
            except Exception as error:
                failed += 1
                print(f"\nQuestion {index} crashed: {error!r}")
            else:
                if result["status"] == "success":
                    if result["correct"]:
                        correct += 1
                else:
                    failed += 1

            current_accuracy = correct / completed
            progress.set_postfix(
                correct=correct,
                completed=completed,
                failed=failed,
                acc=f"{current_accuracy:.4f}",
            )

    return {
        "correct": correct,
        "completed": completed,
        "failed": failed,
        "total": total,
        "accuracy": correct / total,
    }
