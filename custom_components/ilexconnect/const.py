from datetime import timedelta

DOMAIN = "ilexconnect"
DEFAULT_UPDATE_INTERVAL = timedelta(seconds=60)

# Meta data keys to keep
META_KEYS = ["dtype", "firmware", "status", "getDAT", "getMAC", "getSRN"]

# Main sensors
SENSOR_KEYS = {
    "getFLO": ("Water Flow", "L/min"),
    "getSV1": ("Salt Content", "kg"),
    "getCS1": ("Water Reserve", "%"),
    "getNOR": ("Normal Regenerations", None),
    "getSRE": ("Service Regenerations", None),
    "getINR": ("Incomplete Regenerations", None),
    "getTOR": ("Total Regenerations", None),
    "getTCG_total": ("Today's Water Usage", "L"),
    "getTCG": ("Hourly Usage Today", "L"),
    "getYCG_total": ("Yesterday's Water Usage", "L"),
    "getYCG": ("Hourly Usage Yesterday", "L"),
    "getMCG_total": ("Yearly Water Usage", "m3"),
    "getMCG": ("Monthly Water Usage", "m3"),
    "getRCG_total": ("Lifetime Water Usage", "m3"),
    "getRCG": ("Yearly Water Usage Breakdown", "m3"),
    "getSCG_total": ("Salt Usage Total", "kg"),
    "getSCG": ("Salt Usage Monthly", "kg"),
    "getRDO": ("Salt Dose", "g/L"),
    "getMPR": ("Water Pressure", "bar"),
    "getWCG_total": ("Current Week Usage", "L"),
    "getWCG": ("Current Week Daily Usage", "L"),
    "getLCG_total": ("Previous Week Usage", "L"),
    "getLCG": ("Previous Week Daily Usage", "L"),
    "getPRS": ("Water Pressure", "bar"),
}   