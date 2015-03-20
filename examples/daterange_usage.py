
import datetime
from openrange.dt import DateRange

start_date = datetime.date.today()
end_date = start_date + datetime.timedelta(days=365)
two_weeks = datetime.timedelta(days=14)

# yield datetime.date objects for every 2 weeks, starting today, for a year
for dt_date in DateRange(start_date, end_date, two_weeks):
    # ... profit

