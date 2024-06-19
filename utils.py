import random

from colored import Fore, Style

ranks = ['6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
colors = ['Hearts', 'Diamonds', 'Clubs', 'Spades']


class Player:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards


class Match:
    def __init__(self):
        self.players = []
        self.scores = {}  # [list of scores, is on bonus]
        self.trump_card = None

    def sort_players(self):
        last_player = random.choice(self.players)
        self.players.remove(last_player)
        self.players.append(last_player)

    def generate_players(self):
        for _ in range(4):
            player_name = input("Please enter player name: ")
            player = Player(player_name, [])
            self.players.append(player)
            self.scores[player.name] = [[], True]

        return self.players

    def arrange_players_for_next_round(self):
        first_player = self.players.pop(0)
        self.players.append(first_player)

    def generate_players_cards(self) -> list:
        deck = generate_deck()

        for player in self.players:
            # clear cards before adding new
            player.cards = []
            for _ in range(9):
                player.cards.append(deck.pop())

        return self.players

    @staticmethod
    def calculate_score(bet_score, game_score):
        scores_per_bet = {0: 50, 1: 100, 2: 150, 3: 200, 4: 250, 5: 300, 6: 350, 7: 400, 8: 450, 9: 900}

        if bet_score > 0 and game_score == 0:
            return -500, False

        if bet_score != game_score:
            return game_score * 10, False

        return scores_per_bet[game_score], True

    def calculate_match_scores(self, with_bonus):
        scores = dict()
        for name, data in self.scores.items():
            scores[name] = sum(data[0])
            if with_bonus and data[1]:
                scores[name] += max(data[0])

        return scores

    def print_match_scores(self, with_bonus):
        scores = self.calculate_match_scores(with_bonus)
        print()
        print(f'{Fore.yellow}Current Match Scores: {scores}{Style.reset}')

    def print_winner(self):
        winner_name = max(self.scores, key=lambda x: self.scores[x])
        print()
        print(f'Winner winner chicken dinner: {Fore.green}{winner_name}{Style.reset}')


class Game:
    def __init__(self, players):
        self.players = players
        self.trump_card = self.choose_trump_card()
        self.players_bets = {}

    def choose_trump_card(self):
        player = self.players[0]
        print()
        print("- " * 100)

        print(f'{Fore.red}{player.name}, these are your cards {player.cards[:3]}{Style.reset}')

        while True:
            trump_card = input(
                f"{Fore.red}{player.name} which one should be trump card? Please enter: "
                f"(Hearts, Clubs, Diamonds, Spades or -) :{Style.reset}")
            print(" " * 100)
            print("- " * 100)
            if trump_card in ("Hearts", "Clubs", "Diamonds", "Spades", "-"):
                return trump_card

    def place_bets(self):
        print(f"{Fore.red}Place your bet: {Style.reset}")

        for player in self.players[0:3]:
            print(player.name, player.cards)

            while True:
                try:
                    player_bet = int(input(f"{player.name} please tell us your bet([0-9]): "))
                except ValueError:
                    continue

                if player_bet in range(0, 10):
                    self.players_bets[player.name] = player_bet
                    break

        print(self.players[3].name, self.players[3].cards)

        while True:
            try:
                player_bet = int(input(f"{self.players[3].name} please tell us your bet([0-9]): "))
            except ValueError:
                continue
            print(" " * 100)
            print("- " * 100)

            if player_bet in range(0, 10) and sum(self.players_bets.values()) + player_bet != 9:
                self.players_bets[self.players[3].name] = player_bet
                break
        return self.players_bets

    @staticmethod
    def choose_first_move(player):
        print(f"{Fore.red}Play game: {Style.reset}")
        print(player.name, player.cards)

        while True:
            try:
                card_index = int(input(f"{player.name} please choose your card to play(cards index) :"))
            except ValueError:
                continue
            if card_index < len(player.cards):
                return player.cards.pop(card_index)

    def choose_next_move(self, player, first_move_card):
        print(" " * 100)
        print("- " * 100)
        print(player.name, player.cards)

        while True:
            try:
                card_index = int(input(f"{player.name} please choose your card to play(cards index) :"))
            except ValueError:
                continue

            if card_index >= len(player.cards):
                continue

            print(" " * 100)
            print("- " * 100)
            if player.cards[card_index][1] == first_move_card[1] \
                    or player.cards[card_index][1] == self.trump_card \
                    or player.cards[card_index][0] == 'Joker':

                return player.cards.pop(card_index)

            elif first_move_card[1] in [card[1] for card in player.cards]:
                print("Incorrect cards, please enter correct card!")
                continue

            elif self.trump_card in [card[1] for card in player.cards]:
                print("Incorrect cards, please enter correct card!")
                continue

            elif 'Joker' in [card[0] for card in player.cards]:
                print("Incorrect cards, please enter correct card!")
                continue

            else:
                return player.cards.pop(card_index)

    def choose_higher_between_two_card(self, first_card, second_card):
        if first_card[1] == second_card[1]:
            if ranks.index(first_card[0]) > ranks.index(second_card[0]):
                return first_card
            else:
                return second_card
        elif second_card[1] == self.trump_card or second_card[0] == 'Joker':
            return second_card

        return first_card

    def find_winner_card(self, first_card, second_card, third_card, fourth_card):
        winner_card = first_card
        winner_card = self.choose_higher_between_two_card(winner_card, second_card)
        winner_card = self.choose_higher_between_two_card(winner_card, third_card)
        winner_card = self.choose_higher_between_two_card(winner_card, fourth_card)

        return winner_card

    def play_game(self):
        scores = {player.name: 0 for player in self.players}

        for _ in range(9):
            first_card = self.choose_first_move(self.players[0])
            second_card = self.choose_next_move(self.players[1], first_card)
            third_card = self.choose_next_move(self.players[2], first_card)
            fourth_card = self.choose_next_move(self.players[3], first_card)
            winner_card = self.find_winner_card(first_card, second_card, third_card, fourth_card)

            if winner_card == first_card:
                winner = self.players[0]
            elif winner_card == second_card:
                winner = self.players[1]
            elif winner_card == third_card:
                winner = self.players[2]
            else:
                winner = self.players[3]

            scores[winner.name] += 1

            # rearrange order so winner will start next round
            self.players = self.players[self.players.index(winner):] + self.players[: self.players.index(winner)]

        return scores


def generate_deck():
    deck = [('Joker', 'Red'), ('Joker', 'Black')]
    for rank in ranks:
        for color in colors:
            deck.append((rank, color))

    deck.remove(('6', 'Spades'))
    deck.remove(('6', 'Clubs'))

    random.shuffle(deck)

    return deck
