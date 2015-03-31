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
CHANCE_TO_DIE = 1000.0

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

MALE = True
FEMALE = False

BABY_AGE = 5
CHILD_AGE = 15
REPRODUCTIVE_AGE = 25

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

TASK_TYPES = (
        ('farming', 'Farming'),
        ('crafting', 'Crafting'),
        ('building', 'Building'),
)

FIXED_TIME_TASK_TYPES = ('farmingtaskdirectory')
FIXED_WORK_TASK_TYPES = ('craftingtaskdirectory', 'buildingtaskdirectory')

TASK_DIRECTORIES = (
        ('farmingtaskdirectory', 'Farming Task'),
        ('craftingtaskdirectory', 'Crafting Task'),
        ('buildingtaskdirectory', 'Building Task'),
)

LOCATION_TYPES = (
        ('farmingfield', 'Farming Field'),
        ('housingdistrict', 'Housing District'),
        ('workshop', 'Workshop'),
)

ITEM_TYPES = (
        ('fooddirectory', 'Food'),
        ('materialdirectory', 'Material'),
)






