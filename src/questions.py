"""Questionnaire definitions. Every question is answered Yes / No / Unknown."""

OPTIONS = ["Unknown", "Yes", "No"]

CATEGORIES = ["Engine", "Transmission", "Exterior", "Suspension & Brakes", "Tires",
              "Electrical", "Interior", "Maintenance", "Documents & Ownership",
              "Seller & Test Drive"]

QUESTIONS = []


def _add(cat, rows):
    for row in rows:
        key, label, help_text, applies = (list(row) + [None] * 4)[:4]
        QUESTIONS.append({"key": key, "category": cat, "label": label,
                          "help": help_text or "", "applies": applies})


_add("Engine", [
    ("blue_smoke", "Does the exhaust show blue-grey smoke?", "Look after a cold start and when accelerating."),
    ("white_smoke_coolant_loss", "Thick white smoke AND the coolant level keeps dropping?", "A sweet smell is also a hint."),
    ("overheating", "Has the engine overheated, or does the temperature gauge climb?", "Ask the owner and watch the gauge on the drive."),
    ("oil_leak", "Is oil visibly leaking on or under the engine?", "Check the ground where the car was parked."),
    ("engine_knocking", "Is there a knocking or tapping noise from the engine?", "Listen with the bonnet open at idle."),
    ("rough_idle", "Is the idle shaky or uneven?", "The car vibrates or the RPM hunts while stopped."),
    ("hard_cold_start", "Is it hard to start when cold?", "Long cranking, stalling right after start."),
    ("coolant_in_oil", "Milky residue under the oil cap, or oil floating in the coolant?", "Look under the oil filler cap."),
    ("low_oil_level", "Is the dipstick oil level below the minimum mark?", "Check with the engine off and on level ground."),
    ("high_oil_consumption", "Does the owner report unusually frequent oil top-ups?", "Ask how often oil is added between changes."),
    ("warning_lights_persist", "Do warning lights stay on after the engine starts?", "Check engine, oil pressure or battery lights."),
    ("engine_smooth", "Does the engine start easily and run smoothly?", "Positive check: quiet, steady idle."),
])
_add("Transmission", [
    ("delayed_engagement", "Is there a delay when engaging Drive, Reverse or a gear?", "A pause or a jolt before the car moves."),
    ("trans_slipping", "Automatic: do the revs rise without matching acceleration?", "Feels like the gearbox is slipping.", "automatic"),
    ("trans_noises", "Whining, grinding or clunking from the gearbox?", "Listen while shifting and accelerating."),
    ("hard_shifting", "Are gear changes rough or difficult?", "Jerky shifts or a stiff gear lever."),
    ("clutch_slipping", "Manual: does the clutch slip (revs up, speed does not)?", "Try accelerating in a high gear.", "manual"),
    ("accel_vibration", "Is there vibration while accelerating?", "Felt through the floor or seat."),
    ("trans_fluid_leak", "Is transmission fluid leaking?", "Reddish or brown fluid under the car."),
    ("shifts_smooth", "Are gear changes smooth and quiet?", "Positive check."),
])
_add("Exterior", [
    ("uneven_paint", "Is the paint texture uneven (orange peel, overspray)?", "View the panels at an angle in daylight."),
    ("panel_shade_mismatch", "Are some panels a slightly different shade?", "Compare doors, bumpers and fenders."),
    ("visible_rust", "Is there visible rust on the body, sills or floor?", "Check door bottoms, wheel arches and under the car."),
    ("structural_repair_signs", "Are there signs of structural repair?", "Weld marks, bent pillars, repaired chassis rails."),
    ("uneven_panel_gaps", "Are the panel gaps uneven?", "Compare gaps around the bonnet, doors and boot."),
    ("flood_indicators", "Are there flood signs (water lines, silt, rust in odd places)?", "Check under the carpets, seat rails and the boot floor."),
    ("cracked_windscreen", "Is the windscreen cracked or heavily chipped?", ""),
    ("body_original", "Does the body look original with consistent paint and gaps?", "Positive check."),
])
_add("Suspension & Brakes", [
    ("pulls_braking", "Does the car pull to one side when braking?", "Brake firmly on a safe, straight road."),
    ("susp_noise", "Clunks or squeaks over bumps?", "Drive over speed breakers slowly."),
    ("steering_vibration", "Does the steering wheel shake or vibrate?", "Note the speed at which it happens."),
    ("brake_warning", "Is a brake or ABS warning light on?", ""),
    ("soft_brake_pedal", "Does the brake pedal feel soft, spongy or sink?", "A safety-critical check."),
    ("uneven_braking", "Do the brakes grab unevenly or the pedal pulsate?", ""),
    ("susp_fluid_leak", "Fluid leaking from the shock absorbers or brake lines?", "Look inside the wheels and under the car."),
    ("tracks_straight", "Does the car track straight with firm brakes?", "Positive check."),
])
_add("Tires", [
    ("uneven_tire_wear", "Is tire wear uneven across a tire or between tires?", "Inner or outer edges worn more."),
    ("sidewall_damage", "Are there bulges, cuts or cracks on the sidewalls?", ""),
    ("mismatched_tires", "Are the tire sizes or brands mismatched?", ""),
    ("low_tread", "Is the tread low (near the wear indicators)?", ""),
    ("tires_good", "Are all four tires evenly worn with good tread?", "Positive check."),
])
_add("Electrical", [
    ("battery_warning", "Is the battery or charging warning light on?", ""),
    ("headlight_fault", "Do any headlights or tail lights fail?", ""),
    ("indicator_fault", "Do the indicators or hazard lights malfunction?", ""),
    ("window_fault", "Do any power windows or locks malfunction?", ""),
    ("repeated_electrical_failures", "Does the owner mention repeated electrical failures?", "Ask about repeated fuse or wiring repairs."),
    ("electricals_ok", "Do all electrical items work properly?", "Positive check."),
])
_add("Interior", [
    ("interior_wear_heavy", "Is wear on the seat, steering wheel or pedals heavy for the claimed mileage?", "Compare wear with the odometer."),
    ("damp_carpets", "Are the carpets damp or is there a musty smell?", "Press the carpet and smell the cabin."),
    ("airbag_light", "Is the airbag (SRS) warning light on?", ""),
    ("ac_not_cooling", "Is the air conditioning not cooling properly?", ""),
])
_add("Maintenance", [
    ("service_history_complete", "Is a service history available?", "Service book or workshop records."),
    ("service_receipts", "Are receipts available for major repairs?", ""),
    ("major_service_overdue", "Is a major service overdue (timing belt or chain, fluids)?", ""),
    ("accident_reported", "Has the seller said the car had an accident?", "Record what the seller states."),
    ("odometer_inconsistent", "Does the odometer conflict with records or wear?", "Compare with service stickers and records."),
])
_add("Documents & Ownership", [
    ("docs_original", "Is the original registration book or smart card available to see?", "Ask to see the original, not a copy."),
    ("engine_no_match", "Does the engine number match the documents?", "Compare the engine block stamp with the papers."),
    ("chassis_no_match", "Does the chassis number match the documents?", "Compare the chassis plate or stamp with the papers."),
    ("token_tax_paid", "Is token tax paid with no outstanding dues?", "Verify with the registration authority."),
    ("owner_is_seller", "Is the seller the registered owner (name matches)?", ""),
    ("transfer_papers_ready", "Are the ownership transfer documents available and ready?", ""),
    ("ownership_history_clear", "Is the ownership history clear and explainable?", ""),
    ("customs_papers", "Imported car: are the customs clearance papers available?", "", "imported"),
    ("auction_sheet_ok", "Imported car: is the auction sheet available and consistent with the car?", "", "imported"),
])
_add("Seller & Test Drive", [
    ("seller_refuses_inspection", "Does the seller refuse an independent inspection?", ""),
    ("seller_refuses_test_drive", "Does the seller refuse a reasonable test drive?", ""),
    ("seller_cant_explain", "Is the seller unable to explain the ownership history?", ""),
    ("engine_pre_warmed", "Was the engine already warm although you asked for a cold start?", ""),
    ("seller_pressure", "Is the seller pressuring you to decide immediately?", ""),
    ("warning_lights_drive", "Did multiple warning lights appear during the test drive?", ""),
    ("drive_vibration", "Was there significant abnormal vibration while driving?", ""),
    ("seller_open", "Did the seller allow inspection and the test drive openly?", "Positive check."),
])

# Answering "Yes" to these is a good sign (all other questions: "Yes" = a concern).
POSITIVE_KEYS = {"engine_smooth", "shifts_smooth", "body_original", "tracks_straight",
                 "tires_good", "electricals_ok", "service_history_complete", "service_receipts",
                 "docs_original", "engine_no_match", "chassis_no_match", "token_tax_paid",
                 "owner_is_seller", "transfer_papers_ready", "ownership_history_clear",
                 "customs_papers", "auction_sheet_ok", "seller_open"}

# Safety / legal checks. If 3 or more are Unknown, the verdict cannot be "Good Candidate".
CRITICAL_KEYS = ["docs_original", "engine_no_match", "chassis_no_match", "owner_is_seller",
                 "transfer_papers_ready", "soft_brake_pedal", "flood_indicators", "coolant_in_oil"]


def applicable(q, vehicle):
    """Some questions only apply to certain vehicles (manual / automatic / imported)."""
    a = q["applies"]
    if a == "manual":
        return vehicle.get("transmission") == "Manual"
    if a == "automatic":
        return vehicle.get("transmission") != "Manual"
    if a == "imported":
        return vehicle.get("imported") == "Yes"
    return True