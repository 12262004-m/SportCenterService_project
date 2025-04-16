import enum
import strawberry


@strawberry.enum
class GenderEnum(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
