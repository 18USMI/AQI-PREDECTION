"""
India Cities Database
All major cities, towns, and monitoring locations across India
with coordinates for real-time AQI fetching.
"""

# Format: "City Name": (latitude, longitude, state, tier)
# Tier: 1=Metro, 2=Major city, 3=State capital, 4=District town

INDIA_CITIES = {
    # ── Tier 1 Metros ─────────────────────────────────────────────────────────
    "Delhi":          (28.6139,  77.2090, "Delhi",             1),
    "Mumbai":         (19.0760,  72.8777, "Maharashtra",       1),
    "Kolkata":        (22.5726,  88.3639, "West Bengal",       1),
    "Chennai":        (13.0827,  80.2707, "Tamil Nadu",        1),
    "Bangalore":      (12.9716,  77.5946, "Karnataka",         1),
    "Hyderabad":      (17.3850,  78.4867, "Telangana",         1),
    "Ahmedabad":      (23.0225,  72.5714, "Gujarat",           1),
    "Pune":           (18.5204,  73.8567, "Maharashtra",       1),

    # ── State Capitals ────────────────────────────────────────────────────────
    "Jaipur":         (26.9124,  75.7873, "Rajasthan",         2),
    "Lucknow":        (26.8467,  80.9462, "Uttar Pradesh",     2),
    "Bhopal":         (23.2599,  77.4126, "Madhya Pradesh",    2),
    "Chandigarh":     (30.7333,  76.7794, "Punjab/Haryana",    2),
    "Patna":          (25.5941,  85.1376, "Bihar",             2),
    "Bhubaneswar":    (20.2961,  85.8245, "Odisha",            2),
    "Thiruvananthapuram": (8.5241, 76.9366, "Kerala",          2),
    "Guwahati":       (26.1445,  91.7362, "Assam",             2),
    "Ranchi":         (23.3441,  85.3096, "Jharkhand",         2),
    "Raipur":         (21.2514,  81.6296, "Chhattisgarh",      2),
    "Dehradun":       (30.3165,  78.0322, "Uttarakhand",       2),
    "Shimla":         (31.1048,  77.1734, "Himachal Pradesh",  2),
    "Srinagar":       (34.0837,  74.7973, "J&K",               2),
    "Jammu":          (32.7266,  74.8570, "J&K",               2),
    "Leh":            (34.1526,  77.5770, "Ladakh",            2),
    "Panaji":         (15.4989,  73.8278, "Goa",               2),
    "Aizawl":         (23.7271,  92.7176, "Mizoram",           2),
    "Imphal":         (24.8170,  93.9368, "Manipur",           2),
    "Shillong":       (25.5788,  91.8933, "Meghalaya",         2),
    "Kohima":         (25.6751,  94.1086, "Nagaland",          2),
    "Itanagar":       (27.0844,  93.6053, "Arunachal Pradesh", 2),
    "Gangtok":        (27.3314,  88.6138, "Sikkim",            2),
    "Agartala":       (23.8315,  91.2868, "Tripura",           2),
    "Dispur":         (26.1433,  91.7898, "Assam",             2),
    "Silvassa":       (20.2741,  73.0169, "Dadra & NH",        3),
    "Daman":          (20.3974,  72.8328, "Daman & Diu",       3),
    "Kavaratti":      (10.5593,  72.6358, "Lakshadweep",       3),
    "Port Blair":     (11.6234,  92.7265, "Andaman & Nicobar", 3),

    # ── UP & NCR ──────────────────────────────────────────────────────────────
    "Noida":          (28.5355,  77.3910, "Uttar Pradesh",     2),
    "Ghaziabad":      (28.6692,  77.4538, "Uttar Pradesh",     2),
    "Faridabad":      (28.4089,  77.3178, "Haryana",           2),
    "Gurugram":       (28.4595,  77.0266, "Haryana",           2),
    "Agra":           (27.1767,  78.0081, "Uttar Pradesh",     2),
    "Varanasi":       (25.3176,  82.9739, "Uttar Pradesh",     2),
    "Kanpur":         (26.4499,  80.3319, "Uttar Pradesh",     2),
    "Allahabad":      (25.4358,  81.8463, "Uttar Pradesh",     2),
    "Meerut":         (28.9845,  77.7064, "Uttar Pradesh",     3),
    "Aligarh":        (27.8974,  78.0880, "Uttar Pradesh",     3),
    "Bareilly":       (28.3670,  79.4304, "Uttar Pradesh",     3),
    "Moradabad":      (28.8386,  78.7733, "Uttar Pradesh",     3),
    "Gorakhpur":      (26.7606,  83.3732, "Uttar Pradesh",     3),
    "Mathura":        (27.4924,  77.6737, "Uttar Pradesh",     3),
    "Firozabad":      (27.1591,  78.3957, "Uttar Pradesh",     3),

    # ── Rajasthan ─────────────────────────────────────────────────────────────
    "Jodhpur":        (26.2389,  73.0243, "Rajasthan",         2),
    "Udaipur":        (24.5854,  73.7125, "Rajasthan",         2),
    "Kota":           (25.2138,  75.8648, "Rajasthan",         2),
    "Ajmer":          (26.4499,  74.6399, "Rajasthan",         3),
    "Bikaner":        (28.0229,  73.3119, "Rajasthan",         3),

    # ── Maharashtra ───────────────────────────────────────────────────────────
    "Nagpur":         (21.1458,  79.0882, "Maharashtra",       2),
    "Nashik":         (19.9975,  73.7898, "Maharashtra",       2),
    "Aurangabad":     (19.8762,  75.3433, "Maharashtra",       2),
    "Solapur":        (17.6599,  75.9064, "Maharashtra",       3),
    "Kolhapur":       (16.7050,  74.2433, "Maharashtra",       3),
    "Nanded":         (19.1383,  77.3210, "Maharashtra",       3),
    "Amravati":       (20.9374,  77.7796, "Maharashtra",       3),
    "Thane":          (19.2183,  72.9781, "Maharashtra",       2),
    "Navi Mumbai":    (19.0330,  73.0297, "Maharashtra",       2),

    # ── Gujarat ───────────────────────────────────────────────────────────────
    "Surat":          (21.1702,  72.8311, "Gujarat",           2),
    "Vadodara":       (22.3072,  73.1812, "Gujarat",           2),
    "Rajkot":         (22.3039,  70.8022, "Gujarat",           2),
    "Bhavnagar":      (21.7645,  72.1519, "Gujarat",           3),
    "Jamnagar":       (22.4707,  70.0577, "Gujarat",           3),
    "Gandhinagar":    (23.2156,  72.6369, "Gujarat",           2),

    # ── Madhya Pradesh ────────────────────────────────────────────────────────
    "Indore":         (22.7196,  75.8577, "Madhya Pradesh",    2),
    "Jabalpur":       (23.1815,  79.9864, "Madhya Pradesh",    2),
    "Gwalior":        (26.2183,  78.1828, "Madhya Pradesh",    2),
    "Ujjain":         (23.1793,  75.7849, "Madhya Pradesh",    3),

    # ── Karnataka ─────────────────────────────────────────────────────────────
    "Mysore":         (12.2958,  76.6394, "Karnataka",         2),
    "Hubli":          (15.3647,  75.1240, "Karnataka",         2),
    "Mangalore":      (12.9141,  74.8560, "Karnataka",         2),
    "Belgaum":        (15.8497,  74.4977, "Karnataka",         3),
    "Gulbarga":       (17.3297,  76.8343, "Karnataka",         3),
    "Davangere":      (14.4644,  75.9218, "Karnataka",         3),

    # ── Tamil Nadu ────────────────────────────────────────────────────────────
    "Coimbatore":     (11.0168,  76.9558, "Tamil Nadu",        2),
    "Madurai":        (9.9252,   78.1198, "Tamil Nadu",        2),
    "Tiruchirappalli": (10.7905, 78.7047, "Tamil Nadu",        2),
    "Salem":          (11.6643,  78.1460, "Tamil Nadu",        3),
    "Tirunelveli":    (8.7139,   77.7567, "Tamil Nadu",        3),
    "Vellore":        (12.9165,  79.1325, "Tamil Nadu",        3),
    "Erode":          (11.3410,  77.7172, "Tamil Nadu",        3),

    # ── Kerala ────────────────────────────────────────────────────────────────
    "Kochi":          (9.9312,   76.2673, "Kerala",            2),
    "Kozhikode":      (11.2588,  75.7804, "Kerala",            2),
    "Thrissur":       (10.5276,  76.2144, "Kerala",            3),
    "Kollam":         (8.8932,   76.6141, "Kerala",            3),
    "Kannur":         (11.8745,  75.3704, "Kerala",            3),

    # ── Andhra Pradesh & Telangana ────────────────────────────────────────────
    "Visakhapatnam":  (17.6868,  83.2185, "Andhra Pradesh",    2),
    "Vijayawada":     (16.5062,  80.6480, "Andhra Pradesh",    2),
    "Guntur":         (16.3008,  80.4428, "Andhra Pradesh",    2),
    "Tirupati":       (13.6288,  79.4192, "Andhra Pradesh",    2),
    "Nellore":        (14.4426,  79.9865, "Andhra Pradesh",    3),
    "Warangal":       (17.9784,  79.5941, "Telangana",         2),
    "Nizamabad":      (18.6725,  78.0941, "Telangana",         3),

    # ── West Bengal ───────────────────────────────────────────────────────────
    "Durgapur":       (23.5204,  87.3119, "West Bengal",       2),
    "Asansol":        (23.6839,  86.9524, "West Bengal",       2),
    "Siliguri":       (26.7271,  88.3953, "West Bengal",       2),
    "Haldia":         (22.0667,  88.0694, "West Bengal",       3),

    # ── Bihar & Jharkhand ─────────────────────────────────────────────────────
    "Gaya":           (24.7914,  85.0002, "Bihar",             3),
    "Bhagalpur":      (25.2425,  86.9842, "Bihar",             3),
    "Muzaffarpur":    (26.1197,  85.3910, "Bihar",             3),
    "Jamshedpur":     (22.8046,  86.2029, "Jharkhand",         2),
    "Dhanbad":        (23.7957,  86.4304, "Jharkhand",         2),
    "Bokaro":         (23.6693,  86.1511, "Jharkhand",         3),

    # ── Punjab & Haryana ──────────────────────────────────────────────────────
    "Ludhiana":       (30.9010,  75.8573, "Punjab",            2),
    "Amritsar":       (31.6340,  74.8723, "Punjab",            2),
    "Jalandhar":      (31.3260,  75.5762, "Punjab",            2),
    "Patiala":        (30.3398,  76.3869, "Punjab",            3),
    "Bathinda":       (30.2110,  74.9455, "Punjab",            3),
    "Ambala":         (30.3752,  76.7821, "Haryana",           3),
    "Rohtak":         (28.8955,  76.6066, "Haryana",           3),
    "Hisar":          (29.1492,  75.7217, "Haryana",           3),
    "Panipat":        (29.3909,  76.9635, "Haryana",           3),
    "Sonipat":        (28.9931,  77.0151, "Haryana",           3),

    # ── Odisha ────────────────────────────────────────────────────────────────
    "Cuttack":        (20.4625,  85.8830, "Odisha",            2),
    "Rourkela":       (22.2492,  84.8828, "Odisha",            2),
    "Berhampur":      (19.3150,  84.7941, "Odisha",            3),
    "Sambalpur":      (21.4669,  83.9756, "Odisha",            3),

    # ── Assam & NE ────────────────────────────────────────────────────────────
    "Dibrugarh":      (27.4728,  94.9120, "Assam",             3),
    "Silchar":        (24.8333,  92.7789, "Assam",             3),

    # ── Uttarakhand ───────────────────────────────────────────────────────────
    "Haridwar":       (29.9457,  78.1642, "Uttarakhand",       3),
    "Rishikesh":      (30.0869,  78.2676, "Uttarakhand",       3),
    "Roorkee":        (29.8543,  77.8880, "Uttarakhand",       3),

    # ── Chhattisgarh ─────────────────────────────────────────────────────────
    "Bhilai":         (21.1938,  81.3509, "Chhattisgarh",      2),
    "Bilaspur":       (22.0797,  82.1409, "Chhattisgarh",      3),
    "Korba":          (22.3595,  82.7501, "Chhattisgarh",      3),

    # ── Goa ──────────────────────────────────────────────────────────────────
    "Margao":         (15.2993,  73.9862, "Goa",               3),
    "Vasco da Gama":  (15.3982,  73.8113, "Goa",               3),
}


# State groupings for the filter dropdown
STATE_GROUPS = {}
for city, (lat, lon, state, tier) in INDIA_CITIES.items():
    STATE_GROUPS.setdefault(state, []).append(city)

# All states sorted
ALL_STATES = sorted(STATE_GROUPS.keys())


def get_cities_by_state(state: str) -> list:
    return sorted(STATE_GROUPS.get(state, []))


def get_tier1_cities() -> list:
    return [c for c, v in INDIA_CITIES.items() if v[3] == 1]


def get_all_cities() -> list:
    return sorted(INDIA_CITIES.keys())


def get_coords(city: str):
    """Return (lat, lon) or None."""
    entry = INDIA_CITIES.get(city)
    return (entry[0], entry[1]) if entry else None


if __name__ == "__main__":
    print(f"Total cities: {len(INDIA_CITIES)}")
    print(f"Total states/UTs: {len(ALL_STATES)}")
    print(f"Tier-1 metros: {get_tier1_cities()}")
