"""Static vehicle lists and form helpers. No prices or market values anywhere."""
from datetime import datetime

THIS_YEAR = datetime.now().year
OTHER = "Other (type your own)"

MAKES = {
    "Suzuki": ["Alto", "Cultus", "Wagon R", "Swift", "Mehran", "Bolan", "Every", "Jimny"],
    "Toyota": ["Corolla", "Yaris", "Vitz", "Aqua", "Prius", "Passo", "Hilux", "Fortuner", "Land Cruiser"],
    "Honda": ["City", "Civic", "Vezel", "BR-V", "Fit", "N-WGN"],
    "KIA": ["Sportage", "Picanto", "Stonic"],
    "Hyundai": ["Tucson", "Elantra", "Sonata", "Santro"],
    "Changan": ["Alsvin", "Oshan X7", "Karvaan"],
    "MG": ["HS", "ZS"],
    "Daihatsu": ["Mira", "Cuore", "Move", "Tanto"],
    "Nissan": ["Dayz", "Note", "Sunny"],
    "Mitsubishi": ["Lancer", "Pajero Mini"],
}
CITIES = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Multan",
          "Peshawar", "Quetta", "Hyderabad", "Sialkot", "Gujranwala", "Bahawalpur"]
TRANSMISSIONS = ["Automatic", "Manual", "CVT", "Other"]
FUELS = ["Petrol", "Diesel", "Hybrid", "CNG / LPG", "Electric"]
IMPORTED = ["No", "Yes", "Unknown"]

DEFAULT_FORM = {
    "make_sel": "Toyota", "make_cus": "", "model_sel": "Corolla", "model_cus": "",
    "year": 2018, "mileage": 60000, "transmission": "Automatic", "fuel": "Petrol",
    "city_sel": "Karachi", "city_cus": "", "price": 0, "imported": "No",
}


def normalize_vehicle(form):
    """Turn raw form values into a clean vehicle dict. Returns (vehicle, is_valid, errors)."""
    make = form["make_cus"].strip() if form["make_sel"] == OTHER else form["make_sel"]
    model = form["model_cus"].strip() if form["model_sel"] == OTHER else form["model_sel"]
    city = form["city_cus"].strip() if form["city_sel"] == OTHER else form["city_sel"]
    errors = []
    if not make:
        errors.append("Please enter the car manufacturer.")
    if not model:
        errors.append("Please enter the car model.")
    if not city:
        errors.append("Please enter the city of purchase.")
    if not (1980 <= int(form["year"]) <= THIS_YEAR + 1):
        errors.append(f"Manufacturing year must be between 1980 and {THIS_YEAR + 1}.")
    if int(form["mileage"]) < 0:
        errors.append("Mileage cannot be negative.")
    vehicle = {
        "make": make, "model": model, "year": int(form["year"]),
        "mileage": int(form["mileage"]), "transmission": form["transmission"],
        "fuel": form["fuel"], "city": city, "price": int(form["price"]),
        "imported": form["imported"],
    }
    return vehicle, not errors, errors