from knowledge_base import TOURS, KNOWLEDGE_BASE


def calculate_results(selected_answers):
    scores = {tour: 0 for tour in TOURS}

    for answer_id in selected_answers:
        weights = KNOWLEDGE_BASE[answer_id]

        for tour, weight in weights.items():
            scores[tour] += weight

    max_possible_score = len(selected_answers) * 5

    ranking = []

    for tour, score in scores.items():
        percentage = round(
            score / max_possible_score * 100
        )

        ranking.append({
            "tour": tour,
            "score": score,
            "percentage": percentage
        })

    ranking.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return ranking


def get_explanation(
    selected_answers,
    selected_labels,
    selected_categories,
    tour
):
    explanation = []

    for answer_id, answer_text, category in zip(
        selected_answers,
        selected_labels,
        selected_categories
    ):
        weight = KNOWLEDGE_BASE[answer_id][tour]

        explanation.append({
            "category": category,
            "criterion": answer_text,
            "weight": weight
        })

    return explanation