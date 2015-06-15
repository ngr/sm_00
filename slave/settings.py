from django.conf import settings

# TIME
GAME_YEAR = 86400
GAME_MONTH = GAME_YEAR / 12
GAME_DAY   = GAME_MONTH / 30

# ITEMS
MIN_FOOD_SHELF_LIFE = GAME_MONTH

#SKILL_LEVEL_REQUIREMENT = 50
MIN_EXP_FOR_CHILD_SKILLS = 1275 # Equiv level 50
KILLER_SLAVES_LIMIT = 100
#CHANCE_TO_DIE = 1000.0
# start_age, end_age, male, female
DEATH_RISKS = [
        (0, 1, 177, 227),
        (1, 4, 4386, 5376),
        (5, 14, 8333, 10417),
        (15, 24, 1908, 4132),
        (25, 34, 1215, 2488),
        (35, 44, 663, 1106),
        (45, 54, 279, 421),
        (55, 64, 112, 178),
        (65, 74, 42, 65),
        (75, 84, 15, 21),
        (85, 1000, 6, 7) ]


PRIMARY_SKILL_WORK_VALUE = 0.5
SECONDARY_SKILLS_WORK_VALUE = 0.5
YIELD_RANDOMIZER = 25

BASE_EXP_PER_DAY = 3
SECONDARY_SKILLS_EXP_PER_DAY = 1

MIN_LOCATION_SIZE = 1

# Housing
MIN_BED_AREA    = 3
MAX_BED_AREA    = 10
""" Do not change anything below this line. 
Constants are just for information here. Better use special constants file. """

INT = 0
STR = 1
AGL = 2
CHR = 3

MALE = 'm'
FEMALE = 'f'

BABY_AGE  = 5
CHILD_AGE = 15
ADULT_AGE = 25

REPRODUCTIVE_AGE = 17
END_OF_REPRODUCTIVE_AGE = 30
CHANCE_OF_REPRODUCTION = 0.85
CHANCE_OF_REPRODUCTION_DELTA = 0.15

BLUE = 0
CYAN = 1
AQUA = 2

SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        )

RACE_CHOICES = (
        (BLUE, 'Blue'),
        (CYAN, 'Cyan'),
        (AQUA, 'Aqua'),
        )

ATTRIBUTE_CHOICES = (
        (INT, 'Intelligence'),
        (STR, 'Strength'),
        (AGL, 'Agility'),
        (CHR, 'Charisma'),
)

TASK_DIRECTORIES = (
        ('farmingtaskdirectory', 'Farming'),
        ('craftingtaskdirectory', 'Crafting'),
        ('harvestingtaskdirectory', 'Harvesting'),
        ('buildingtaskdirectory', 'Building'),
)

#TASK_TYPES = (
#        ('farming', 'Farming'),
#        ('crafting', 'Crafting'),
#        ('harvesting', 'Harvesting'),
#        ('building', 'Building'),
#)

#FIXED_TIME_TASK_TYPES = ('farmingtaskdirectory')
#FIXED_WORK_TASK_TYPES = ('craftingtaskdirectory', 'buildingtaskdirectory')

#LOCATION_TYPES = (
#        ('farmingfield', 'Farming Field'),
#        ('housingdistrict', 'Housing District'),
#        ('workshop', 'Workshop'),
#)

#ITEM_TYPES = (
#        ('fooddirectory', 'Food'),
#        ('materialdirectory', 'Material'),
#)






