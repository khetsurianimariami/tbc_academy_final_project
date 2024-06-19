from copy import deepcopy

from utils import Match, Game


def main():
    match = Match()
    match.generate_players()

    for _ in range(4):
        match.print_match_scores(with_bonus=False)

        match.sort_players()
        match.generate_players_cards()

        game = Game(deepcopy(match.players))

        players_bets = game.place_bets()
        game_scores = game.play_game()

        for name, game_score in game_scores.items():
            score, has_bonus = match.calculate_score(players_bets[name], game_score)
            match.scores[name][0].append(score)
            match.scores[name][1] = match.scores[name][1] and has_bonus

        # rearrange players: first will go to last position
        match.arrange_players_for_next_round()

    match.print_match_scores(with_bonus=True)
    match.print_winner()


if __name__ == "__main__":
    main()
