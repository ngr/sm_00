import datetime
from django.utils import timezone

def fit_to_range_float(attr, minv='Zero', maxv='Zero'):
    """ This returns float() of either minv or maxv if
    attr is out of limits. Otherwise float() of given attribute. """

    attr = float(attr)
    if minv != 'Zero':
        minv = float(minv)
        if maxv != 'Zero':
            maxv = float(maxv)
            if maxv < minv:
                print("Limits are inaccurate")
                minv, maxv = maxv, minv
            if attr > maxv:
                return maxv
        else:
            return minv if attr < minv else attr
    return minv if attr < minv else attr


def validate_in_range_float(attr, minv='Zero', maxv='Zero'):
    """  Check if float() attr is in range """
    attr = float(attr)
    if minv != 'Zero':
        minv = float(minv)
        if maxv != 'Zero':
            maxv = float(maxv)
            if maxv < minv:
                minv, maxv = maxv, minv
            if attr > maxv:
                return False
        else:
            return False if attr < minv else True
    return True


def validate_in_range_int(attr, minv='Zero', maxv='Zero'):
    """  Check if int() attr is in range """
    attr = int(float(attr))
    if minv != 'Zero':
        minv = int(float(minv))
        if maxv != 'Zero':
            maxv = int(float(maxv))
            if maxv < minv:
                minv, maxv = maxv, minv
            if attr > maxv:
                return False
        else:
            return False if attr < minv else True
    return True

def fit_to_range_int(attr, minv='Zero', maxv='Zero'):
    """ This returns int() of either minv or maxv if 
    attr is out of limits. Otherwise int() of given attribute. """

    attr = int(float(attr))
    if minv != 'Zero':
        minv = int(float(minv))
        if maxv != 'Zero':
            maxv = int(float(maxv))
            if maxv < minv:
                print("Limits are inaccurate")
                minv, maxv = maxv, minv
            if attr > maxv:
                return maxv
        else:
            return minv if attr < minv else attr
    return minv if attr < minv else attr


""" This is a constant rule cached for exp & skill level functions. """
level_exp_ratio = []
for i in range(1,101):
    if len(level_exp_ratio) > 0:
        level_exp_ratio.append(level_exp_ratio[-1] + i)
    else:
        level_exp_ratio.append(i)

def exp_to_lev(exp, difficulty=1):
    """ Return current level according to given exp in skill """
    exp = int(float(exp))
    i = 0
    while i < len(level_exp_ratio) and exp >= level_exp_ratio[i]:
        i += 1
    return i

def next_game_period(p=3600):
    """ Return the Real time of the beginning of the next
        Game time period. Default is 1 Real hour """ 
    n = timezone.now()
#    print("Now is", n)
    H = p // 3600
    M = p // 60
    S = p % 60
#    print("Period is {0} or {1}:{2}:{3}".format(p, H, M, S))
    discard = datetime.timedelta(
            hours=(n.hour % H if H else 0),
            minutes=(n.minute % M if M else 0),
            seconds=(n.second % S if S else n.second),
            microseconds=n.microsecond)
#    print("Discard", discard)
    r = n - discard + datetime.timedelta(seconds=p)
    return r



def clean_string_title(attr):
    return str(attr).strip().title()

def clean_string_lower(attr):
    return str(attr).strip().lower()

def clean_string_upper(attr):
    return str(attr).strip().upper()





