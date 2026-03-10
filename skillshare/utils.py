import random


def get_random_slug() -> str:
    """
    Génère un slug aléatoire basé sur une liste de mots en anglais
    au format "adjectif-nom-nombre" (ex: "happy-dog-420").
    """
    adjectives = [
        "happy",
        "bright",
        "quick",
        "clever",
        "brave",
        "calm",
        "funny",
        "smart",
        "fast",
        "wise",
        "strong",
        "gentle",
        "bold",
        "sweet",
        "fancy",
        "sly",
        "sneaky",
        "kind",
        "smooth",
        "proud",
        "sharp",
        "witty",
        "fierce",
        "sly",
        "wild",
        "swift",
        "cunning",
    ]
    nouns = [
        "lion",
        "tiger",
        "eagle",
        "fox",
        "bear",
        "wolf",
        "wildcat",
        "lynx",
        "jaguar",
        "panther",
        "cheetah",
        "hawk",
        "sharkowl",
        "cheetah",
        "leopard",
        "lynx",
        "cougar",
        "raccoon",
        "raptor",
        "vulture",
    ]
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    random_number = random.randint(100, 999)
    return f"{adjective}{noun}{random_number}"
