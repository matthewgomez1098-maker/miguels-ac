# -*- coding: utf-8 -*-
"""
Miguel's A/C — all site content lives here.

Edit this file, then run `python3 build.py` to regenerate every page.
Contact details are in BUSINESS below — change them once, they update sitewide.
"""

# ---------------------------------------------------------------------------
# BUSINESS DETAILS  ***  TODO: replace the placeholders before launch  ***
# ---------------------------------------------------------------------------
BUSINESS = {
    "name": "Miguel's A/C",
    "legal_name": "Miguel's A/C Heating & Air",
    "tagline": "Inland Empire & Los Angeles",
    "owner": "Miguel Guardado",
    "phone": "(909) 228-7653",              # confirmed
    "phone_href": "+19092287653",           # confirmed (E.164)
    "email": "miguelguardadohvac@gmail.com",  # confirmed
    "street": "1234 Foothill Blvd, Suite B",  # TODO: real address
    "city": "Rancho Cucamonga",
    "state": "CA",
    "zip": "91730",                          # TODO: real ZIP
    "license": "CSLB Lic. #0000000",         # TODO: real C-20 license number
    "hours_weekday": "Mon–Sat, 7:00am – 8:00pm",   # TODO: confirm real hours
    "hours_emergency": "Emergency service available after hours",
    "domain": "https://matthewgomez1098-maker.github.io/miguels-ac",  # TODO: real domain once bought
    # TODO: invented. It is on the About page and drives the "15+ years" stat.
    # Do not leave a made-up founding year attached to a real owner's name.
    "founded": "2009",
}
BUSINESS["address_line"] = "{street}, {city}, {state} {zip}".format(**BUSINESS)

# ---------------------------------------------------------------------------
# SERVICES
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "air-conditioning-repair",
        "nav": "Air conditioning repair",
        "name": "Air Conditioning Repair",
        "tag": "Repair",
        "icon": "wrench",
        "short": "Same-day diagnosis and repair for every major brand, with a flat-rate quote before we touch a wrench.",
        "title": "Same-Day AC Repair | Inland Empire & Los Angeles",
        "meta": "Emergency air conditioning repair across the Inland Empire and LA. Same-day service, flat-rate pricing, no overtime charges. Call {phone}.",
        "hero_h1": "AC repair, same day, no overtime charges",
        "hero_p": "When it is 105 degrees outside, a broken air conditioner is not a scheduling problem — it is an emergency. We answer the phone, roll a stocked truck, and get your system running before the house gets any hotter.",
        "body_h2": "We fix what actually breaks",
        "body_p": "Most no-cool calls in the Inland Empire come down to the same short list: a failed capacitor, a burned contactor, a low refrigerant charge from a leak, an iced-over coil, or a condensate switch that tripped. Our trucks carry those parts, which is why the majority of our repairs finish on the first visit instead of turning into a week-long wait for a part order.",
        "bullets": [
            "Free flat-rate quote before any work starts — you approve the number, not a surprise invoice",
            "Capacitors, contactors, relays, motors and thermostats stocked on every truck",
            "Refrigerant leak search with electronic detection, plus proper R-410A and R-454B handling",
            "Blower motor, control board and compressor diagnostics for all major brands",
            "Frozen coil, drain line and condensate switch troubleshooting",
            "Repairs backed by a 1-year parts and labor warranty",
        ],
        "faq": [
            ("How fast can you actually get here?",
             "Most calls placed before 2pm get a same-day appointment window. Full no-cool emergencies get bumped to the front of the schedule — call us and we will tell you a real arrival window, not a vague 'sometime today.'"),
            ("What does a diagnostic cost?",
             "We charge a flat diagnostic fee for the visit, and we tell you the number on the phone before we dispatch. If you approve the repair, that fee comes off the total."),
            ("Do you charge extra for evenings or weekends?",
             "No. We do not add overtime or weekend surcharges. A Saturday night call costs the same as a Tuesday morning."),
            ("Should I repair or replace my system?",
             "Rule of thumb: if the unit is under 10 years old, repair almost always wins. Past 15 years, with a compressor or coil failure and R-22 refrigerant, replacement usually pays for itself in efficiency. We give you both numbers and let you decide."),
        ],
    },
    {
        "slug": "ac-installation-replacement",
        "nav": "AC installation & replacement",
        "name": "AC Installation & Replacement",
        "tag": "Install",
        "icon": "snowflake",
        "short": "Right-sized, permitted, HERS-tested installs with financing — done in a day, not a week.",
        "title": "AC Installation & System Replacement | Miguel's A/C",
        "meta": "New AC and full HVAC system replacement across the Inland Empire. Manual J sizing, permits, HERS testing, 10-year warranties and monthly financing.",
        "hero_h1": "A new system, sized right and installed in a day",
        "hero_p": "A replacement is only as good as the install. We measure the house instead of matching the old label, pull the permit, and get the HERS test done so your warranty and your rebate both hold up.",
        "body_h2": "Why sizing matters more than brand",
        "body_p": "An oversized air conditioner short-cycles: it blasts cold air, hits the thermostat setpoint, and shuts off before it ever pulls humidity out of the house. You end up with a cold, clammy room and a compressor that wears out early. We run a load calculation on your actual square footage, insulation, window orientation and duct layout, then spec the smallest system that will hold your house at temperature on the hottest day of the year.",
        "bullets": [
            "Manual J load calculation on every replacement — no guessing from the old nameplate",
            "City permit pulled and HERS testing scheduled as part of the job",
            "Up to 10-year parts warranty plus our own labor warranty",
            "Full changeouts typically finished in one day",
            "High-efficiency and variable-speed options that qualify for utility rebates",
            "Monthly financing available with approved credit",
        ],
        "faq": [
            ("How long does a full replacement take?",
             "A straightforward changeout — condenser, coil and furnace or air handler — is a one-day job for our crew. If we are also replacing ductwork or moving equipment, plan on two."),
            ("Do I really need a permit?",
             "In California, yes. Equipment changeouts require a permit and a HERS test on the duct system. Contractors who skip it leave you with an unpermitted install that can block a home sale and can void the manufacturer's warranty."),
            ("What size system do I need?",
             "That depends on more than square footage — insulation, window area, ceiling height and duct condition all move the number. We calculate it on site. Be skeptical of anyone who quotes you a tonnage over the phone."),
            ("Can you finance it?",
             "Yes. We offer monthly payment plans with approved credit, and we will show you the monthly number next to the cash price so you can compare honestly."),
        ],
    },
    {
        "slug": "heat-pumps",
        "nav": "Heat pumps",
        "name": "Heat Pumps",
        "tag": "Efficiency",
        "icon": "flame",
        "short": "One system that cools in July and heats in January — and qualifies for the biggest rebates in California.",
        "title": "Heat Pump Installation | Inland Empire & LA | Miguel's A/C",
        "meta": "Heat pump installation and replacement across the Inland Empire and Los Angeles. Rebate-eligible, all-electric heating and cooling from one system.",
        "hero_h1": "Heat pumps: one system, both seasons",
        "hero_p": "A heat pump is an air conditioner that can run backwards. It cools your house all summer and heats it all winter, using a fraction of the energy of a gas furnace or electric strip heat.",
        "body_h2": "The right call for Southern California",
        "body_p": "Our winters are mild, which is exactly the climate a heat pump is built for. There is no deep freeze here to push the system past its efficient range, so you get high-efficiency heating for most of the year without a gas line. Between federal tax credits and California's electrification rebates, a heat pump is frequently the cheapest path to a new system once incentives land.",
        "bullets": [
            "Replaces both your AC and your furnace with one piece of equipment",
            "Eligible for federal tax credits and California electrification rebates",
            "Variable-speed inverter models that run quietly at low capacity most of the day",
            "No gas line, no combustion, no carbon monoxide risk",
            "Works with your existing ductwork in most homes",
            "We handle the rebate paperwork with you",
        ],
        "faq": [
            ("Will a heat pump actually keep my house warm here?",
             "Easily. Inland Empire winter lows rarely fall below the range where modern inverter heat pumps run at full efficiency. For the handful of cold snaps, systems include backup heat that engages automatically."),
            ("Is it more expensive to run than gas?",
             "It depends on your electric rate and how well the house is sealed. For most homes we see, the summer cooling savings from a high-efficiency inverter system offset the winter heating cost difference. We will model it against your actual bills."),
            ("Can I keep my existing ducts?",
             "Usually yes, if they are sealed and correctly sized. We test the duct system before quoting so you are not surprised by an add-on later."),
            ("What rebates are available?",
             "Federal tax credits plus utility and state electrification programs. Programs change, so call us and we will tell you what is currently open in your city."),
        ],
    },
    {
        "slug": "ductless-mini-splits",
        "nav": "Ductless mini-splits",
        "name": "Ductless Mini-Splits",
        "tag": "Ductless",
        "icon": "wind",
        "short": "Cool a garage, an ADU, a converted attic or that one bedroom that never gets cold — no ductwork required.",
        "title": "Ductless Mini-Split Installation | Miguel's A/C",
        "meta": "Ductless mini-split installation for ADUs, garages, additions and hot rooms across the Inland Empire and LA. Zoned, quiet and highly efficient.",
        "hero_h1": "Ductless mini-splits for the rooms your ducts never reached",
        "hero_p": "Additions, garage conversions, ADUs, permitted or not — some spaces were never on the original duct plan. A mini-split gives them their own zone, their own thermostat, and near-silent operation.",
        "body_h2": "Zoning is the point",
        "body_p": "A traditional system treats your whole house as one room. If the west-facing bedroom bakes at 4pm, your only lever is to over-cool everything else. A mini-split puts an independent head in the space that actually needs it — so you cool one room to 70 without dropping the rest of the house to 68 and paying for it.",
        "bullets": [
            "Single-zone and multi-zone systems (one outdoor unit, up to eight indoor heads)",
            "Wall-mount, ceiling cassette and low-wall console indoor units",
            "Heat and cool from the same unit — no separate heater needed in an ADU",
            "Extremely quiet: most indoor heads run under 25 dB on low",
            "Ideal for garage conversions, additions, sunrooms, offices and detached ADUs",
            "Clean line-set routing — we care what the outside of your house looks like",
        ],
        "faq": [
            ("How many heads can one outdoor unit run?",
             "Depending on the system, up to eight. For most homes we spec two to four heads on a single condenser, which keeps the outdoor footprint and the cost down."),
            ("Are they loud?",
             "No — that is one of the main reasons people choose them. The compressor lives outside and the indoor head runs quieter than a ceiling fan on low."),
            ("Do they need ductwork at all?",
             "None. A three-inch hole through the wall carries the refrigerant lines, the drain and the control wire. That is the whole penetration."),
            ("Is a mini-split good for a whole house?",
             "It can be, especially in a home with no existing ducts. We would walk the house and compare a multi-zone ductless design against a ducted system so you can see both costs."),
        ],
    },
    {
        "slug": "duct-repair-replacement",
        "nav": "Duct repair & replacement",
        "name": "Duct Repair & Replacement",
        "tag": "Ductwork",
        "icon": "duct",
        "short": "Leaky attic ducts can waste a third of what you cool. We test, seal and replace them.",
        "title": "Duct Repair, Sealing & Replacement | Miguel's A/C",
        "meta": "Duct testing, sealing and full replacement across the Inland Empire and LA. Stop cooling your attic — fix the leaks that waste 20-30% of your air.",
        "hero_h1": "Stop paying to air condition your attic",
        "hero_p": "In a typical Inland Empire home the ducts run through an attic that hits 140 degrees in August. Every leak in that system dumps cold air where nobody lives, and pulls hot dusty attic air back into your bedrooms.",
        "body_h2": "What a duct test tells you",
        "body_p": "We pressurize the duct system and measure how much air escapes. A tight system leaks under six percent. Plenty of the 1980s and 1990s homes we test out here leak twenty to thirty percent — meaning nearly a third of the air your system cools never makes it to a register. Sealing that is usually the single highest-return HVAC improvement a house can get, and it often costs less than a repair.",
        "bullets": [
            "Duct leakage testing with real numbers, before and after",
            "Mastic sealing at plenums, boots, takeoffs and every connection",
            "Full R-8 flex duct replacement for collapsed or disintegrating runs",
            "Register and return sizing corrections for rooms that never get airflow",
            "Attic duct re-support so runs stop sagging, kinking and choking off",
            "HERS verification when the job requires it",
        ],
        "faq": [
            ("How do I know my ducts are leaking?",
             "Rooms that never get cold, dust that comes back a day after you clean, a system that runs constantly, or a summer bill that jumped without a rate change. A test confirms it in about half an hour."),
            ("Is sealing enough, or do I need replacement?",
             "If the flex duct is intact and just leaking at the connections, sealing is the answer and it is far cheaper. If the inner liner is torn or the insulation has crumbled — common past about 25 years — replacement is the real fix."),
            ("How long does a duct replacement take?",
             "Most single-family homes are one to two days depending on the number of runs and how tight the attic is."),
            ("Will this actually lower my bill?",
             "Sealing a system that tested at 25% leakage is one of the few HVAC improvements where customers reliably notice the difference on the next bill."),
        ],
    },
    {
        "slug": "indoor-air-quality",
        "nav": "Indoor air quality",
        "name": "Indoor Air Quality",
        "tag": "Air quality",
        "icon": "leaf",
        "short": "Filtration, UV and ventilation for wildfire smoke, valley dust and allergy season.",
        "title": "Indoor Air Quality Solutions | Miguel's A/C",
        "meta": "Whole-home air filtration, UV purification and ventilation across the Inland Empire and LA. Built for wildfire smoke, dust and allergy season.",
        "hero_h1": "Cleaner air, for the weeks the sky turns orange",
        "hero_p": "The Inland Empire deals with wildfire smoke, freeway particulates, and some of the worst ozone readings in the country. Your HVAC system already moves all the air in your house — it may as well clean it on the way through.",
        "body_h2": "Start with the filter, then go further",
        "body_p": "The one-inch fiberglass filter at your return does almost nothing for the particles that matter. A properly sized media cabinet holds a four- or five-inch MERV 13 filter that actually captures smoke and fine dust, and because it has far more surface area it does not choke your blower the way a jammed-in high-MERV one-inch filter does. From there we can add UV treatment at the coil and mechanical fresh-air ventilation.",
        "bullets": [
            "MERV 13 and MERV 16 media cabinets sized so airflow does not suffer",
            "Whole-home HEPA bypass filtration for severe allergy and smoke sensitivity",
            "UV-C lamps at the evaporator coil to stop mold and biofilm growth",
            "Steam and bypass humidifiers, and whole-home dehumidification",
            "Fresh-air ventilation to meet current code on tightly sealed homes",
            "Return-air leak sealing — the most common source of attic dust indoors",
        ],
        "faq": [
            ("Will a better filter hurt my system?",
             "Only if it is the wrong kind. Cramming a MERV 13 into a one-inch slot restricts airflow badly. Putting one in a proper four-inch cabinet does not. That is the whole trick."),
            ("Do UV lights actually work?",
             "For what they are designed to do — killing mold and bacteria growing on a wet evaporator coil — yes, and that coil is the most common source of a musty smell when the AC kicks on. They are not a substitute for filtration."),
            ("What helps most during wildfire smoke?",
             "A MERV 13 or better media filter in a properly sized cabinet, sealed returns so you are not drawing smoky attic air, and running the fan continuously so the air keeps cycling through the filter."),
            ("How often should filters be changed?",
             "One-inch: every 1-3 months. Four- or five-inch media: every 6-12 months. Sooner during fire season."),
        ],
    },
    {
        "slug": "maintenance-plans",
        "nav": "Maintenance plans",
        "name": "Maintenance Plans",
        "tag": "Membership",
        "icon": "shield",
        "short": "Two tune-ups a year, priority scheduling, and 15% off any repair you need.",
        "title": "HVAC Maintenance Plans | Miguel's A/C",
        "meta": "Annual HVAC maintenance plans with two tune-ups, priority scheduling, 15% off repairs and no overtime charges. Inland Empire and LA.",
        "hero_h1": "The cheapest repair is the one you never needed",
        "hero_p": "Nearly every emergency no-cool call we run in July traces back to something a spring tune-up would have caught: a weak capacitor, a dirty condenser coil, a clogged drain line. Members get ahead of it.",
        "body_h2": "What a real tune-up includes",
        "body_p": "A tune-up should not be a filter change and a sticker. We wash the condenser coil, check refrigerant charge against superheat and subcooling, test capacitor microfarads against the rating, measure amp draw on the compressor and blower, clear and treat the condensate line, tighten every electrical connection, and check the temperature split across the coil. Then we tell you what we found — including the parts that are still fine.",
        "bullets": [
            "Two visits a year: cooling tune-up in spring, heating check in fall",
            "Priority scheduling — members go to the front of the line in a heat wave",
            "15% off every repair, parts and labor",
            "No diagnostic fee on service calls",
            "No overtime or weekend charges, ever",
            "Filters included and swapped at each visit",
        ],
        "faq": [
            ("Is a maintenance plan worth it?",
             "If your system is over five years old, generally yes — one avoided emergency compressor call usually covers several years of membership. If your system is brand new and under warranty, the case is weaker and we will tell you that."),
            ("When should the tune-up happen?",
             "Cooling in March or April, before the first heat wave books the whole schedule. Heating in October."),
            ("Does the plan transfer if I sell the house?",
             "Yes. Let us know and we will move the remaining term to the new owner — it is a nice thing to hand over at closing."),
            ("Do I have to sign a long contract?",
             "No. Plans are annual and you can cancel at renewal."),
        ],
    },
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------------------
# SERVICE AREAS
# ---------------------------------------------------------------------------
CITIES = [
    # --- Inland Empire -----------------------------------------------------
    {
        "slug": "riverside", "name": "Riverside", "county": "Riverside County",
        "region": "Inland Empire", "dispatch": "same-day",
        "meta_extra": "Wood Streets, Canyon Crest, Orangecrest, La Sierra and Downtown Riverside.",
        "blurb": "Riverside runs hot and dry, and a big share of the housing stock predates modern duct standards. We spend a lot of time out here on 1960s and 1970s homes where the equipment is newer than the ductwork feeding it.",
        "note": "Historic Wood Streets homes often have undersized returns from a retrofit decades ago — the single biggest reason a well-maintained system still can't keep up in August.",
        "areas": ["Wood Streets", "Canyon Crest", "Orangecrest", "La Sierra", "Downtown Riverside", "Arlanza", "Mission Grove", "Hawarden Hills"],
    },
    {
        "slug": "san-bernardino", "name": "San Bernardino", "county": "San Bernardino County",
        "region": "Inland Empire", "dispatch": "same-day",
        "meta_extra": "Arrowhead, Del Rosa, Verdemont, Muscoy and Downtown San Bernardino.",
        "blurb": "San Bernardino regularly posts some of the hottest summer readings in the region. Systems here work harder and longer than the manufacturer's design assumptions, which is exactly why annual service matters more than it does on the coast.",
        "note": "We see a lot of failed run capacitors here in July. It is a $200 part that shuts down a $6,000 system — and a spring tune-up catches it every time.",
        "areas": ["Arrowhead", "Del Rosa", "Verdemont", "Muscoy", "Downtown", "Northpark", "Shandin Hills"],
    },
    {
        "slug": "fontana", "name": "Fontana", "county": "San Bernardino County",
        "region": "Inland Empire", "dispatch": "same-day",
        "meta_extra": "North Fontana, Sierra Lakes, Southridge, Village of Heritage and Downtown Fontana.",
        "blurb": "Fontana's newer North Fontana and Sierra Lakes tracts are full of builder-grade systems now hitting the 12-to-18-year mark all at once. We do a lot of replacements out here, and a lot of honest conversations about repairing one more season instead.",
        "note": "Builder-grade equipment in the North Fontana tracts tends to fail as a cohort. If your neighbors are replacing, get yours tested before it decides for you in August.",
        "areas": ["North Fontana", "Sierra Lakes", "Southridge", "Village of Heritage", "Downtown Fontana", "Coyote Canyon"],
    },
    {
        "slug": "ontario", "name": "Ontario", "county": "San Bernardino County",
        "region": "Inland Empire", "dispatch": "same-day",
        "meta_extra": "Ontario Ranch, Creekside, Downtown Ontario and the Ontario Mills area.",
        "blurb": "Ontario mixes brand-new Ontario Ranch construction with a much older downtown core. We work on both — high-efficiency systems still under warranty, and 1950s bungalows getting their first real duct system.",
        "note": "New Ontario Ranch builds are tight and well sealed, which makes correct sizing and proper fresh-air ventilation more important than it was a generation ago.",
        "areas": ["Ontario Ranch", "Creekside", "Downtown Ontario", "Ontario Mills area", "Westwind", "Rosena"],
    },
    {
        "slug": "rancho-cucamonga", "name": "Rancho Cucamonga", "county": "San Bernardino County",
        "region": "Inland Empire", "dispatch": "same-day",
        "meta_extra": "Alta Loma, Etiwanda, Victoria Gardens, Terra Vista and Haven View.",
        "blurb": "This is home base. Rancho Cucamonga is where our shop is, which means the shortest arrival windows we offer anywhere and the easiest same-day emergency scheduling.",
        "note": "Alta Loma's Santa Ana wind exposure is hard on condenser coils — debris packs the fins and quietly kills efficiency. Coil washing is not optional up on the bench.",
        "areas": ["Alta Loma", "Etiwanda", "Victoria Gardens", "Terra Vista", "Haven View", "Red Hill", "Deer Canyon"],
    },
    {
        "slug": "corona", "name": "Corona", "county": "Riverside County",
        "region": "Inland Empire", "dispatch": "same-day",
        "meta_extra": "South Corona, Eastvale border, Sierra Del Oro, Green River and Downtown Corona.",
        "blurb": "Corona's hillside neighborhoods create real temperature swings between floors. Two-story homes here are our most common zoning and mini-split conversations in the whole service area.",
        "note": "If your upstairs runs eight degrees hotter than your downstairs, that is a zoning and duct-balancing problem — not a reason to buy a bigger unit.",
        "areas": ["South Corona", "Sierra Del Oro", "Green River", "Downtown Corona", "Corona Hills", "Eastvale border"],
    },
    {
        "slug": "moreno-valley", "name": "Moreno Valley", "county": "Riverside County",
        "region": "Inland Empire", "dispatch": "same-day",
        "meta_extra": "Sunnymead, Moreno Valley Ranch, Rancho Belago and Edgemont.",
        "blurb": "Moreno Valley's large 1990s tracts share the same construction and the same failure timeline. We know these floor plans well enough to know where the return is undersized before we walk in.",
        "note": "The 1990s Moreno Valley Ranch plans commonly have a single central return doing the work of two. Adding a return is often cheaper than upsizing equipment.",
        "areas": ["Sunnymead", "Moreno Valley Ranch", "Rancho Belago", "Edgemont", "Towngate"],
    },
    {
        "slug": "redlands", "name": "Redlands", "county": "San Bernardino County",
        "region": "Inland Empire", "dispatch": "same-day",
        "meta_extra": "Smiley Heights, South Redlands, Downtown Redlands and the University District.",
        "blurb": "Redlands has some of the most beautiful older housing stock in the region, and retrofitting modern HVAC into a 1920s home without wrecking the character takes a different approach than a tract install.",
        "note": "For historic Redlands homes, high-velocity systems and multi-zone ductless are usually the right answer — they cool the house without cutting soffits through original plaster.",
        "areas": ["Smiley Heights", "South Redlands", "Downtown Redlands", "University District", "Redlands Heights"],
    },

    # --- San Gabriel Valley ------------------------------------------------
    {
        "slug": "san-gabriel-valley", "name": "San Gabriel Valley", "county": "Los Angeles County",
        "region": "San Gabriel Valley", "dispatch": "same-day", "hub": True,
        "meta_extra": "Claremont, La Verne, San Dimas, Covina, Walnut and the surrounding foothill communities.",
        "blurb": "We cover the San Gabriel Valley end to end, from Claremont and La Verne out through Covina and Walnut. Same crews, same pricing, same same-day emergency service as our Inland Empire routes.",
        "note": "SGV foothill homes get real temperature stratification between floors. Zoned systems and correctly balanced ducts solve it far more cheaply than a bigger condenser.",
        "areas": ["Claremont", "La Verne", "San Dimas", "Covina", "Walnut", "Azusa", "Duarte", "Temple City"],
    },
    {
        "slug": "pomona", "name": "Pomona", "county": "Los Angeles County",
        "region": "San Gabriel Valley", "dispatch": "same-day",
        "meta_extra": "Phillips Ranch, Ganesha Hills, Lincoln Park and Downtown Pomona.",
        "blurb": "Pomona is our gateway into LA County, and we service it on the same schedule as the Inland Empire — same rates, same same-day availability, no travel surcharge.",
        "note": "Lincoln Park's historic homes and Phillips Ranch's 1980s tracts need completely different approaches. We quote them differently, and you should be suspicious of anyone who doesn't.",
        "areas": ["Phillips Ranch", "Ganesha Hills", "Lincoln Park", "Downtown Pomona", "Westmont"],
    },
    {
        "slug": "pasadena", "name": "Pasadena", "county": "Los Angeles County",
        "region": "San Gabriel Valley", "dispatch": "same-day",
        "meta_extra": "Bungalow Heaven, Madison Heights, Linda Vista, Hastings Ranch and Old Pasadena.",
        "blurb": "Pasadena's foothill position means genuinely hot summers paired with some of the oldest housing stock in the county. A lot of these homes were built decades before central air existed, and the retrofits vary wildly in quality.",
        "note": "Pasadena Water & Power runs its own rebate programs separate from Southern California Edison — worth checking before you buy, because the numbers are often better.",
        "areas": ["Bungalow Heaven", "Madison Heights", "Linda Vista", "Hastings Ranch", "Old Pasadena", "San Rafael", "East Pasadena"],
    },
    {
        "slug": "alhambra", "name": "Alhambra", "county": "Los Angeles County",
        "region": "San Gabriel Valley", "dispatch": "same-day",
        "meta_extra": "Downtown Alhambra, Bean Tract, Midwick and the Main Street corridor.",
        "blurb": "Alhambra is dense, largely built out between the 1920s and 1950s, and full of homes still running original wall furnaces with a window unit doing the summer work. Adding real central air or ductless here is our most common job.",
        "note": "Lot lines are tight in Alhambra. Condenser placement and setback clearances matter — a unit crammed against a fence loses efficiency and can fail inspection.",
        "areas": ["Downtown Alhambra", "Bean Tract", "Midwick", "Main Street corridor", "Emery Park", "Granada Park"],
    },
    {
        "slug": "el-monte", "name": "El Monte", "county": "Los Angeles County",
        "region": "San Gabriel Valley", "dispatch": "same-day",
        "meta_extra": "South El Monte, Norwood, Mountain View and the Valley Mall area.",
        "blurb": "El Monte sits in the valley floor where summer heat settles and lingers. The 1950s tract housing here was built for a milder expectation than what the last decade of summers has actually delivered.",
        "note": "A lot of El Monte homes are on original 100-amp panels. If you are adding central air or converting to a heat pump, the electrical service needs checking before anyone quotes equipment.",
        "areas": ["South El Monte", "Norwood", "Mountain View", "Valley Mall area", "Gibson", "Rio Hondo"],
    },
    {
        "slug": "west-covina", "name": "West Covina", "county": "Los Angeles County",
        "region": "San Gabriel Valley", "dispatch": "same-day",
        "meta_extra": "South Hills, Woodside Village, Merced Manor and the Eastland area.",
        "blurb": "West Covina's post-war and 1960s tracts are dense with systems on their second or third replacement cycle. We see the full range here, from well-maintained 20-year-old units to installs that were wrong on day one.",
        "note": "Several West Covina tracts have the air handler in a hallway closet with no return path to speak of. Fixing the return usually buys more comfort than fixing the equipment.",
        "areas": ["South Hills", "Woodside Village", "Merced Manor", "Eastland", "Vincent", "Citrus Grove"],
    },
    {
        "slug": "glendora", "name": "Glendora", "county": "Los Angeles County",
        "region": "San Gabriel Valley", "dispatch": "same-day",
        "meta_extra": "Glendora Village, Morgan Ranch, Gordon Highlands and the foothill neighborhoods.",
        "blurb": "Glendora climbs into the foothills, which means Santa Ana wind exposure and homes on slopes where the upstairs bakes while the downstairs stays comfortable. Zoning conversations happen on most of our visits here.",
        "note": "Foothill Santa Ana exposure packs condenser fins with debris fast. Glendora systems need coil cleaning more often than the flatland tracts do, and skipping it quietly costs you efficiency every season.",
        "areas": ["Glendora Village", "Morgan Ranch", "Gordon Highlands", "Sunflower", "Foothill corridor"],
    },
    {
        "slug": "diamond-bar", "name": "Diamond Bar", "county": "Los Angeles County",
        "region": "San Gabriel Valley", "dispatch": "same-day",
        "meta_extra": "The Country Estates, Diamond Ridge, Summitridge and the Grand Avenue corridor.",
        "blurb": "Diamond Bar is hillside, two-story, and full of homes where one system is asked to hold two very different thermal environments at the same temperature. It rarely works without help.",
        "note": "Two-story Diamond Bar homes are our most frequent zoning retrofit. A damper-and-thermostat zoning system usually costs a fraction of the second system people expect to need.",
        "areas": ["The Country Estates", "Diamond Ridge", "Summitridge", "Grand Avenue corridor", "Walnut border"],
    },

    # --- Central & Southeast LA --------------------------------------------
    {
        "slug": "los-angeles", "name": "Los Angeles", "county": "Los Angeles County",
        "region": "Central & Southeast LA", "dispatch": "scheduled",
        "meta_extra": "Downtown, Silver Lake, Echo Park, Highland Park, Eagle Rock and the surrounding central neighborhoods.",
        "blurb": "Central LA is the widest mix we work in — 1920s hillside bungalows, mid-century duplexes, converted lofts and new multifamily, often on the same block. There is no standard answer here, which is exactly why a load calculation matters more than a catalog.",
        "note": "LADWP runs rebate programs separate from Southern California Edison, and the City of LA has its own permitting process that moves at its own pace. We handle both, and we tell you the real timeline upfront.",
        "areas": ["Downtown", "Silver Lake", "Echo Park", "Highland Park", "Eagle Rock", "Los Feliz", "Mid-City", "Koreatown"],
    },
    {
        "slug": "montebello", "name": "Montebello", "county": "Los Angeles County",
        "region": "Central & Southeast LA", "dispatch": "scheduled",
        "meta_extra": "Montebello Hills, Bella Vista, Whittier Narrows border and the Beverly Boulevard corridor.",
        "blurb": "Montebello's housing is largely post-war, compact, and built when a floor furnace was the whole HVAC plan. Most of our work here is adding real cooling to homes that never had it designed in.",
        "note": "Where there is no existing duct system, a multi-zone ductless install is usually both cheaper and better than cutting ducts into a small post-war floor plan.",
        "areas": ["Montebello Hills", "Bella Vista", "Beverly Boulevard corridor", "Whittier Narrows border", "Garfield"],
    },
    {
        "slug": "whittier", "name": "Whittier", "county": "Los Angeles County",
        "region": "Central & Southeast LA", "dispatch": "scheduled",
        "meta_extra": "Uptown Whittier, Friendly Hills, East Whittier and the College Hills area.",
        "blurb": "Whittier splits cleanly between historic Uptown and the hillside tracts east of it, and the two need different approaches. Uptown's older homes reward careful ductless retrofits; the hillside tracts are conventional replacement work.",
        "note": "Uptown Whittier has genuinely old housing stock where the attic will not take a modern duct run without compromise. We would rather zone it properly than force ducts where they do not fit.",
        "areas": ["Uptown Whittier", "Friendly Hills", "East Whittier", "College Hills", "Whittier Narrows"],
    },
    {
        "slug": "downey", "name": "Downey", "county": "Los Angeles County",
        "region": "Central & Southeast LA", "dispatch": "scheduled",
        "meta_extra": "Downey Landing, Orange Estates, Rancho Estates and the Florence Avenue corridor.",
        "blurb": "Downey is mid-century tract housing at scale — well built, consistent, and now almost universally on its second or third HVAC system. We know these floor plans and what tends to go wrong in them.",
        "note": "Many Downey homes have the original ducts under the slab or in a shallow attic. Both are worth testing before you spend money on equipment that will just push air into a leak.",
        "areas": ["Downey Landing", "Orange Estates", "Rancho Estates", "Florence Avenue corridor", "Northeast Downey"],
    },
    {
        "slug": "norwalk", "name": "Norwalk", "county": "Los Angeles County",
        "region": "Central & Southeast LA", "dispatch": "scheduled",
        "meta_extra": "Norwalk Village, Studebaker, Cerritos border and the Rosecrans corridor.",
        "blurb": "Norwalk's post-war tracts were built fast and built alike, which means the same handful of HVAC problems repeat across whole streets. That is good news — we usually know what we are looking at before we open the panel.",
        "note": "Shallow attics are the norm in Norwalk's tract housing. Duct runs get crushed against the roof deck over time, choking airflow to the far bedrooms.",
        "areas": ["Norwalk Village", "Studebaker", "Rosecrans corridor", "Cerritos border", "Gardenhill"],
    },

    # --- South Bay & Harbor -------------------------------------------------
    {
        "slug": "long-beach", "name": "Long Beach", "county": "Los Angeles County",
        "region": "South Bay & Harbor", "dispatch": "route",
        "meta_extra": "Belmont Shore, Bixby Knolls, California Heights, Naples and Downtown Long Beach.",
        "blurb": "Long Beach is coastal, which changes the job. Milder summers mean smaller equipment, but salt air is genuinely hard on outdoor units, and plenty of the housing stock has no cooling at all.",
        "note": "Salt-air corrosion is the real enemy here. Coastal-rated condensers with treated coils cost more upfront and routinely outlast a standard unit by years within a mile of the water.",
        "areas": ["Belmont Shore", "Bixby Knolls", "California Heights", "Naples", "Downtown Long Beach", "Alamitos Beach", "Los Altos"],
    },
    {
        "slug": "torrance", "name": "Torrance", "county": "Los Angeles County",
        "region": "South Bay & Harbor", "dispatch": "route",
        "meta_extra": "Old Torrance, Hollywood Riviera, Southwood, West Torrance and the Del Amo area.",
        "blurb": "Torrance's coastal moderation makes it one of the best heat pump markets in the county — the winters are mild enough that a heat pump runs in its efficient range essentially year-round, and the summers rarely demand a large system.",
        "note": "Mild coastal weather tempts people into undersizing, then oversizing after one bad heat wave. A proper load calculation settles it — and near the water, specify a coastal-rated condenser.",
        "areas": ["Old Torrance", "Hollywood Riviera", "Southwood", "West Torrance", "Del Amo", "Walteria"],
    },

    # --- Westside -----------------------------------------------------------
    {
        "slug": "santa-monica", "name": "Santa Monica", "county": "Los Angeles County",
        "region": "Westside", "dispatch": "route",
        "meta_extra": "Ocean Park, Sunset Park, Wilshire-Montana, Mid-City and North of Montana.",
        "blurb": "Santa Monica is the mildest climate we serve and the strictest to build in. Most of the older housing has no cooling designed in at all, and the city's permitting and green-building requirements are more demanding than anywhere in the Inland Empire.",
        "note": "Santa Monica's building and energy requirements are stricter than the state baseline. Anyone quoting you a same-week install without mentioning permits has not accounted for the process.",
        "areas": ["Ocean Park", "Sunset Park", "Wilshire-Montana", "Mid-City", "North of Montana", "Pico district"],
    },
    {
        "slug": "culver-city", "name": "Culver City", "county": "Los Angeles County",
        "region": "Westside", "dispatch": "route",
        "meta_extra": "Downtown Culver City, Carlson Park, Blair Hills, Fox Hills and Park East.",
        "blurb": "Culver City sits just far enough inland to actually need cooling, on housing stock that mostly predates it. Ductless retrofits and small right-sized systems are the bulk of what we install here.",
        "note": "Carlson Park and the older Culver City bungalows have almost no attic to work with. Ductless is not a compromise in those homes — it is the correct engineering answer.",
        "areas": ["Downtown Culver City", "Carlson Park", "Blair Hills", "Fox Hills", "Park East", "Studio Village"],
    },

    # --- San Fernando Valley & North ---------------------------------------
    {
        "slug": "burbank", "name": "Burbank", "county": "Los Angeles County",
        "region": "San Fernando Valley & North", "dispatch": "scheduled",
        "meta_extra": "Magnolia Park, Rancho, Burbank Hills, Toluca Lake border and Downtown Burbank.",
        "blurb": "Burbank gets valley heat without valley relief, and much of the housing is 1930s-1950s with retrofit cooling of varying quality. It is a strong replacement market and a strong duct-sealing market.",
        "note": "Burbank Water & Power is a municipal utility with its own rebate programs — separate from Southern California Edison, and often more generous. Ask before you buy.",
        "areas": ["Magnolia Park", "Rancho", "Burbank Hills", "Toluca Lake border", "Downtown Burbank", "Chandler"],
    },
    {
        "slug": "glendale", "name": "Glendale", "county": "Los Angeles County",
        "region": "San Fernando Valley & North", "dispatch": "scheduled",
        "meta_extra": "Adams Hill, Rossmoyne, Verdugo Woodlands, Montrose and Downtown Glendale.",
        "blurb": "Glendale runs from flat downtown blocks up into the Verdugo foothills, and the hillside homes have all the two-story stratification problems that come with elevation. Zoning solves more Glendale complaints than new equipment does.",
        "note": "Glendale Water & Power runs its own rebates independent of Southern California Edison. Between those and federal credits, a heat pump here often pencils out better than people expect.",
        "areas": ["Adams Hill", "Rossmoyne", "Verdugo Woodlands", "Montrose", "Downtown Glendale", "Chevy Chase"],
    },
    {
        "slug": "sherman-oaks", "name": "Sherman Oaks", "county": "Los Angeles County",
        "region": "San Fernando Valley & North", "dispatch": "scheduled",
        "meta_extra": "Sherman Oaks, Studio City, Van Nuys, Encino and the surrounding San Fernando Valley.",
        "blurb": "The San Fernando Valley is the hottest part of LA County, and it shows in the equipment. Systems here run harder and longer than anywhere on the Westside, and they fail on the same August afternoons the Inland Empire does.",
        "note": "Valley heat means attic temperatures well past 140 degrees. Duct leakage that would be a minor issue near the coast is a major one here — testing before replacing is money well spent.",
        "areas": ["Sherman Oaks", "Studio City", "Van Nuys", "Encino", "Valley Village", "North Hollywood"],
    },
    {
        "slug": "santa-clarita", "name": "Santa Clarita", "county": "Los Angeles County",
        "region": "San Fernando Valley & North", "dispatch": "route",
        "meta_extra": "Valencia, Saugus, Newhall, Canyon Country and Stevenson Ranch.",
        "blurb": "Santa Clarita gets summer heat on par with the Inland Empire, on much newer housing. Most of Valencia and Stevenson Ranch is builder-grade equipment now reaching the age where it starts making decisions for you.",
        "note": "Santa Clarita's newer tracts are tightly built, so ventilation and correct sizing matter more than raw tonnage. Oversizing a tight house gives you a cold, clammy room and a short-cycling compressor.",
        "areas": ["Valencia", "Saugus", "Newhall", "Canyon Country", "Stevenson Ranch", "Castaic"],
    },
]

# Dispatch language, so far-flung pages do not promise a window we cannot hold.
DISPATCH = {
    "same-day": "Same-day windows on most calls placed before 2pm.",
    "scheduled": "Same-day when a truck is already out that way, next-day otherwise — we tell you which when you call.",
    "route": "We run scheduled routes out here. Call before noon and we will usually have you booked for the next day.",
}

REGIONS = ["Inland Empire", "San Gabriel Valley", "Central & Southeast LA",
           "South Bay & Harbor", "Westside", "San Fernando Valley & North"]

CITY_NAMES = [c["name"] for c in CITIES]

# ---------------------------------------------------------------------------
# SHARED CONTENT
# ---------------------------------------------------------------------------
STATS = [
    ("29", "Cities across IE & LA County"),
    ("6,400+", "Systems repaired and installed"),
    ("Same day", "On most calls placed before 2pm"),
    ("4.9★", "Average rating across 900+ reviews"),
]

REVIEWS = [
    ("Maria Gonzalez", "Homeowner, Ontario",
     "Called at 9am on a Saturday when it was 108 out and the house was 88 inside. Miguel's had a tech here by 1pm. Bad capacitor, fixed in twenty minutes, and they didn't charge me a weekend rate. I've told half my street about them."),
    ("David Nguyen", "Homeowner, Rancho Cucamonga",
     "Three companies quoted me a full replacement. Miguel's tested the ducts first and found the system was fine — the ducts were leaking almost 30%. Sealed them for a fraction of a new system and my upstairs is finally usable."),
    ("Angela Rivera", "Homeowner, Riverside",
     "They pulled the permit, scheduled the HERS test, and handed me the paperwork without me having to ask. The last contractor I used skipped all of it and I found out during escrow. Night and day."),
    ("Tom Bradley", "Property manager, Fontana",
     "I manage eleven units and Miguel's handles all of them. They give me a real arrival window, they text when they're on the way, and I've never had a callback on the same repair twice."),
    ("Priya Shah", "Homeowner, Corona",
     "Our upstairs was always eight degrees hotter. Instead of selling me a bigger unit they added a return and balanced the ducts. Cost less than I expected and it actually worked."),
    ("Luis Herrera", "Homeowner, San Bernardino",
     "Signed up for the maintenance plan after they caught a failing capacitor in the spring. They were right — that would have died in the middle of July with everyone booked solid."),
]

PLANS = [
    {
        "name": "Service Call",
        "sub": "One-time repair visit",
        "price": "Flat rate",
        "price_note": "Quoted on the phone before we dispatch",
        "features": [
            "Same-day diagnostic visit",
            "Flat-rate repair quote before work starts",
            "No overtime or weekend charges",
            "No surprise fees",
            "1-year parts and labor warranty",
        ],
        "cta": "Book a repair",
        "href": "/contact.html",
        "featured": False,
    },
    {
        "name": "Comfort Plan",
        "sub": "Annual membership",
        "price": "$19",
        "price_note": "per month, cancel at renewal",
        "features": [
            "Two tune-ups a year (cooling + heating)",
            "Priority scheduling in a heat wave",
            "15% off every repair",
            "No diagnostic fee on service calls",
            "Filter replacement included",
        ],
        "cta": "Join the plan",
        "href": "/maintenance-plans.html",
        "featured": True,
    },
    {
        "name": "System Replacement",
        "sub": "New equipment install",
        "price": "Financed",
        "price_note": "Monthly payments with approved credit",
        "features": [
            "Full system replacement, usually in one day",
            "Manual J load calculation, not a nameplate guess",
            "Permits and HERS testing handled",
            "Up to 10-year parts warranty",
            "Rebate paperwork filed with you",
        ],
        "cta": "Get a quote",
        "href": "/financing.html",
        "featured": False,
    },
]

HOME_FAQ = [
    ("Do you charge extra for nights or weekends?",
     "No. We do not add overtime, weekend or holiday surcharges. A Sunday emergency call is billed at the same rate as a Tuesday morning appointment."),
    ("How fast can you get to me?",
     "Most calls placed before 2pm get a same-day window. Full no-cool emergencies get priority. When you call, we give you a real arrival window instead of an all-day range."),
    ("Do you give quotes before starting work?",
     "Always. We diagnose the problem, hand you a flat-rate number, and wait for you to approve it. You will never see a charge on the invoice you didn't agree to first."),
    ("Which brands do you work on?",
     "All the major ones — Carrier, Trane, Lennox, Goodman, Rheem, American Standard, Bryant, York, Daikin, Mitsubishi and the rest. Our trucks carry universal parts for the common failures."),
    ("Are you licensed and insured?",
     "Yes — licensed, bonded and insured in California. Our license number is on every estimate and at the bottom of this page. Ask any contractor for theirs before they start work."),
    ("Do you offer financing?",
     "Yes, on system replacements and larger jobs, with approved credit. We show you the monthly payment next to the cash price so you can compare both honestly."),
]

PROCESS = [
    ("You call", "A person picks up. We ask what the system is doing and give you a real arrival window."),
    ("We diagnose", "A stocked truck arrives, we find the actual fault, and we show you what we found."),
    ("You approve", "Flat-rate quote, in writing, before any work starts. No pressure, no surprise line items."),
    ("We fix it", "Most repairs finish the same visit. Everything is backed by a 1-year parts and labor warranty."),
]
