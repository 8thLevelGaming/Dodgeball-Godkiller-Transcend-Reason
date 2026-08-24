"""This module holds miscellaneous utilities and helper functions."""

# Function that draws bars for a status display.
# It takes the current HP/stamina/exp value as well as the maximum values for
# those attributes (100 for exp since you always level up at 100).
# Then the program fills bars based on the current value.

# The way it works is that it uses division to determine what fraction
# of the bar should be filled and this is the scaled through width,
# then rounded to a whole number and we use the max function to
# stop the bar from bugging out if it goes negative.
def make_bar(current, maximum, width=20):
    filled = round((current / maximum) * width)
    filled = max(0, min(filled, width))
    return "[" + ("#" * filled) + ("-" * (width - filled)) + "]"

# This function makes messages print more slowly for readability.
# Text will print 0.5 seconds more slowly.
# The flush value is to correctly make each slowed line move the 
# scroll bar down to the bottom because otherwise it just lingers
# until the program next asks for input, negating any value from
# this function.
# Note that this does not actually seem to work on the
# Khan Academy IDE, but I am leaving the code in just in case
# anyone wishes to run it elsewhere.
# For this reason I also changed it to 0.1 seconds instead.
def slow_print(text, delay=0.1):
    print(text, flush=True)
    time.sleep(delay)