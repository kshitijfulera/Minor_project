def explain_prediction(features: dict):

    explanations = []

    if features["enemy_density"] > 0.02:
        explanations.append("Too many enemies per area → increases difficulty")

    if features["projectile_rate"] > 0.3:
        explanations.append("High projectile frequency → harder to dodge")

    if features["cluster_score"] > 2:
        explanations.append("Enemies grouped together → sudden difficulty spikes")

    return explanations


def feature_contributions(features: dict):

    contributions = {
        "enemy_density": features["enemy_density"] * 0.3,
        "projectile_rate": features["projectile_rate"] * 0.3,
        "danger_score": features["danger_score"] * 0.2,
        "cluster_score": features["cluster_score"] * 0.2
    }

    return contributions