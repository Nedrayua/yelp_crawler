from itertools import cycle

def creator_sleep_generator(sec_segment:int):
    """
    create generator with num of seconds for next request to prevent site blocking
    """
    sleep_segment = [sec_segment for i in range(30)] + [250]
    sleep_segments = [sleep_segment for segment in range(70)]
    sleep_values = [values for segment in sleep_segments for values in segment] + [75600]
    
    return cycle(sleep_values)