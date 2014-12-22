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
    """ Returns current level according to given exp in skill """
    exp = int(float(exp))
    i = 0
    while i < len(level_exp_ratio) and exp >= level_exp_ratio[i]:
        i += 1
    return i



