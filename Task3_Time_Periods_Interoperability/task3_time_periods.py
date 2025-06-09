from datetime import datetime, timedelta
import pytz

# Define CET timezone
cet = pytz.timezone('Europe/Paris')  # CET/CEST auto-handled

# Current time in CET
now = datetime.now(cet)

# Next day midnight in CET
next_day = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

# Generate hourly intervals (24 hours)
time_periods = []
for i in range(24):
    start = next_day + timedelta(hours=i)
    end = start + timedelta(hours=1)
    time_periods.append((start.isoformat(), end.isoformat()))

# Print the intervals
for start, end in time_periods:
    print(f"[{start}, {end})")
