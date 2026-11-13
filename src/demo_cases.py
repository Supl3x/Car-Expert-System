"""Five preloaded scenarios for the viva demo and the tests."""
from questions import QUESTIONS, POSITIVE_KEYS
from inference_engine import VERDICT_GOOD, VERDICT_INSPECT, VERDICT_NEGOTIATE, VERDICT_AVOID


def clean_answers():
    """Every concern = No, every positive check = Yes."""
    return {q["key"]: ("Yes" if q["key"] in POSITIVE_KEYS else "No") for q in QUESTIONS}


def _with(**changes):
    a = clean_answers()
    a.update(changes)
    return a


DEMO_CASES = {
    "1. Clean Toyota Corolla": {
        "form": {"make_sel": "Toyota", "model_sel": "Corolla", "year": 2019, "mileage": 55000,
                 "transmission": "Automatic", "fuel": "Petrol", "city_sel": "Karachi", "imported": "No"},
        "answers": clean_answers(), "expected": VERDICT_GOOD},
    "2. Suzuki Wagon R with minor issues": {
        "form": {"make_sel": "Suzuki", "model_sel": "Wagon R", "year": 2017, "mileage": 90000,
                 "transmission": "Manual", "fuel": "Petrol", "city_sel": "Lahore", "imported": "No"},
        "answers": _with(oil_leak="Yes", sidewall_damage="Yes", ac_not_cooling="Yes"),
        "expected": VERDICT_INSPECT},
    "3. Honda Civic with several concerns": {
        "form": {"make_sel": "Honda", "model_sel": "Civic", "year": 2015, "mileage": 130000,
                 "transmission": "Automatic", "fuel": "Petrol", "city_sel": "Islamabad", "imported": "No"},
        "answers": _with(pulls_braking="Yes", trans_slipping="Yes", service_history_complete="No",
                         major_service_overdue="Yes", headlight_fault="Yes"),
        "expected": VERDICT_NEGOTIATE},
    "4. Imported Vitz with red flags": {
        "form": {"make_sel": "Toyota", "model_sel": "Vitz", "year": 2014, "mileage": 40000,
                 "transmission": "Automatic", "fuel": "Petrol", "city_sel": "Karachi", "imported": "Yes"},
        "answers": _with(engine_no_match="No", flood_indicators="Yes", damp_carpets="Yes",
                         docs_original="No", seller_refuses_inspection="Yes", customs_papers="No"),
        "expected": VERDICT_AVOID},
    "5. Almost nothing checked": {
        "form": {"make_sel": "Toyota", "model_sel": "Corolla", "year": 2018, "mileage": 60000,
                 "transmission": "Automatic", "fuel": "Petrol", "city_sel": "Karachi", "imported": "No"},
        "answers": {}, "expected": VERDICT_INSPECT},
}