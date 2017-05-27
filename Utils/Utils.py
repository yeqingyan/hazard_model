def date_to_step(timestamp, start_date, intervals):
    if timestamp < start_date:
        return 0
    return (timestamp - start_date) // intervals
