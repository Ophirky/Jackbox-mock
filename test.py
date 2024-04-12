import random

class Player:
    """Player class - contains the username and score of the player."""
    def __init__(self, username, is_admin=False):
        self.username = username
        self.score = 0
        self.is_admin = is_admin

    def __str__(self):
        return f"{self.username}, {self.score}"

def assign_sentences(sentences, players):
    """
    Randomly assigns sentences to players, ensuring each sentence has at most two players.
    :param sentences: Tuple of sentences (strings)
    :param players: List of Player objects
    :return: Dictionary with the sentence as the key and a tuple of usernames as the value
    """
    # Shuffle the list of players for randomness
    random.shuffle(players)

    # Prepare the result dictionary
    sentence_assignments = {sentence: [] for sentence in sentences}

    # List of usernames already assigned to a sentence
    assigned_usernames = set()

    # Create a list of indices for the sentences to shuffle
    sentence_indices = list(range(len(sentences)))
    random.shuffle(sentence_indices)

    # Assign players to sentences using shuffled indices
    player_iterator = iter(players)
    for index in sentence_indices:
        try:
            # Assign up to two players per sentence
            counter = 0
            while counter < 2:
                player = next(player_iterator)
                if player.username not in assigned_usernames:
                    sentence_assignments[sentences[index]].append(player)
                    assigned_usernames.add(player.username)
                    counter += 1
        except StopIteration:
            # No more players available
            break

    # Filter out any empty sentence assignments and convert lists to tuples
    final_assignments = {k: tuple(v) for k, v in sentence_assignments.items() if v}
    return final_assignments

# Example usage:
sentences = (
    "I couldn't believe my eyes when I saw %s.",
    "The last thing I want to see is %s.",
    "My secret talent is %s.",
    "The title of my autobiography would be 'The Life and Times of %s.'",
    "If I could have any superpower, it would be %s.",
    "The most surprising thing I learned yesterday was %s.",
    "My favorite hobby is %s.",
    "If I could live anywhere in the world, it would be %s.",
    "The one thing I can't live without is %s.",
    "My biggest fear is %s.",
    "The most unusual thing in my house is %s.",
    "If I were an animal, I would be a %s.",
    "My favorite movie of all time is %s.",
    "The best piece of advice I've ever received is %s.",
    "If I could meet anyone, living or dead, it would be %s.",
    "The most interesting fact I know is %s.",
    "If I could go back in time, I would visit %s.",
    "My dream job is %s.",
    "The funniest joke I know is %s.",
    "The most beautiful place I've ever been is %s.",
    "A new TV show called \"MommyFight\" is about %s"
)

players = [Player('Alice', True), Player('Bob'), Player('Charlie'), Player('Dana'), Player("John"), Player('Alice'),
           Player('Veronica'), Player('Betty'), Player('George')]

assignments = assign_sentences(sentences, players)
for sentence, assigned_players in assignments.items():
    print(f"{sentence}: {assigned_players}")
