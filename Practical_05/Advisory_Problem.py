
rules = [
    {
        "symptoms": {"fever", "cough", "sore_throat"},
        "diagnosis": "Common Cold / Flu",
        "advice": "Rest, fluids, and over-the-counter fever/cough medicine. See a doctor if symptoms persist beyond 5-7 days."
    },
    {
        "symptoms": {"fever", "cough", "shortness_of_breath", "fatigue"},
        "diagnosis": "Possible Respiratory Infection",
        "advice": "Seek medical attention promptly; monitor oxygen levels if possible."
    },
    {
        "symptoms": {"headache", "nausea", "sensitivity_to_light"},
        "diagnosis": "Possible Migraine",
        "advice": "Rest in a dark quiet room; consult a doctor if this is a new or severe pattern."
    },
    {
        "symptoms": {"itchy_skin", "rash", "swelling"},
        "diagnosis": "Possible Allergic Reaction",
        "advice": "Avoid the suspected allergen; take an antihistamine; seek emergency care if breathing is affected."
    },
    {
        "symptoms": {"fever", "joint_pain", "rash"},
        "diagnosis": "Possible Viral Infection (e.g., Dengue-like)",
        "advice": "Seek medical testing promptly; avoid aspirin/NSAIDs until confirmed."
    },
    {
        "symptoms": {"thirst", "frequent_urination", "fatigue"},
        "diagnosis": "Possible Diabetes Indicator",
        "advice": "Recommend a blood glucose test and consultation with a physician."
    },
]

DEFAULT_ADVICE = (
    "Symptoms do not match a known rule confidently. Recommend consulting a physician for proper evaluation."
)

class DiagnosisExpertSystem:
    """Simple forward-chaining rule-based inference engine."""

    def __init__(self, knowledge_base):
        self.rules = knowledge_base

    def infer(self, patient_symptoms):
        patient_symptoms = set(patient_symptoms)
        matches = []
        for rule in self.rules:

            if rule["symptoms"].issubset(patient_symptoms):
                matched_fraction = len(rule["symptoms"]) / len(rule["symptoms"])
                matches.append((rule, matched_fraction))
        return matches

if __name__ == "__main__":
    engine = DiagnosisExpertSystem(rules)

    test_cases = [
        {"fever", "cough", "sore_throat"},
        {"headache", "nausea", "sensitivity_to_light", "fatigue"},
        {"itchy_skin", "rash", "swelling"},
        {"fever", "cough", "shortness_of_breath", "fatigue"},
        {"thirst", "frequent_urination", "fatigue"},
        {"dizziness"},  
    ]

    print("=" * 65)
    print("RULE-BASED EXPERT SYSTEM - MEDICAL DIAGNOSIS ADVISOR")
    print("=" * 65)

    for idx, symptoms in enumerate(test_cases, start=1):
        print(f"\nCase {idx}")
        print(f"Reported Symptoms: {sorted(symptoms)}")
        results = engine.infer(symptoms)
        if results:
            for rule, _ in results:
                print(f" -> Diagnosis: {rule['diagnosis']}")
                print(f"    Advice   : {rule['advice']}")
        else:
            print(" -> Diagnosis: Unknown")
            print(f"    Advice   : {DEFAULT_ADVICE}")

    print("-" * 65)
    print("Total Rules in Knowledge Base:", len(rules))
    print("=" * 65)
