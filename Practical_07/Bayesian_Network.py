

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


model = DiscreteBayesianNetwork([
    ("Cold", "Cough"),
    ("Flu", "Fever"),
    ("Flu", "Fatigue"),
    ("Cold", "Fever"),
])

cpd_flu = TabularCPD(variable="Flu", variable_card=2, values=[[0.90], [0.10]])
cpd_cold = TabularCPD(variable="Cold", variable_card=2, values=[[0.80], [0.20]])

cpd_fatigue = TabularCPD(
    variable="Fatigue", variable_card=2,
    values=[[0.90, 0.20],
            [0.10, 0.80]],
    evidence=["Flu"], evidence_card=[2],
)

cpd_cough = TabularCPD(
    variable="Cough", variable_card=2,
    values=[[0.85, 0.30],
            [0.15, 0.70]],
    evidence=["Cold"], evidence_card=[2],
)


cpd_fever = TabularCPD(
    variable="Fever", variable_card=2,
    values=[
        [0.95, 0.20, 0.30, 0.02],  
        [0.05, 0.80, 0.70, 0.98],  
    ],
    evidence=["Flu", "Cold"], evidence_card=[2, 2],
)

model.add_cpds(cpd_flu, cpd_cold, cpd_fatigue, cpd_cough, cpd_fever)
assert model.check_model()

print("=" * 65)
print("BAYESIAN NETWORK FOR DIAGNOSIS (built with pgmpy)")
print("=" * 65)

print("\nNetwork edges:")
for edge in model.edges():
    print(f"  {edge[0]} --> {edge[1]}")

infer = VariableElimination(model)

print("\n" + "-" * 65)
print("QUERY 1: P(Flu | Fever = yes, Cough = yes)")
q1 = infer.query(variables=["Flu"], evidence={"Fever": 1, "Cough": 1}, show_progress=False)
print(q1)

print("-" * 65)
print("QUERY 2: P(Cold | Fever = yes, Fatigue = no)")
q2 = infer.query(variables=["Cold"], evidence={"Fever": 1, "Fatigue": 0}, show_progress=False)
print(q2)

print("-" * 65)
print("QUERY 3: P(Fever) marginal, no evidence")
q3 = infer.query(variables=["Fever"], show_progress=False)
print(q3)

print("-" * 65)
print("QUERY 4: Most probable Flu/Cold given Fever=yes, Fatigue=yes, Cough=no")
map_result = infer.map_query(
    variables=["Flu", "Cold"],
    evidence={"Fever": 1, "Fatigue": 1, "Cough": 0},
    show_progress=False,
)
print(map_result)
print("=" * 65)
