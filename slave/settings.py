from django.conf import settings

GAME_YEAR = 3600 
GAME_MONTH = GAME_YEAR / 12

SKILL_LEVEL_REQUIREMENT = 50
KILLER_SLAVES_LIMIT = 100
CHANCE_TO_DIE = 1000.0

""" Do not change anything below this line. 
Constants are just for information here. Better use special constants file. """

INT = 0
STR = 1
AGL = 2
CHR = 3

MALE = True
FEMALE = False

GAME_YEAR = 3600
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



