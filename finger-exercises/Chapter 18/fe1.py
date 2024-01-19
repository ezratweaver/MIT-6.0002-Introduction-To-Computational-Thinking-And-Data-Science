import random
import numpy as np


def roll_die():
    return random.choice([1, 2, 3, 4, 5, 6])


class big_six_game:

    def __init__(self):
        self.sixbeforeseven_wins = 0
        self.sixbeforeseven_losses = 0
        self.sevenbeforesix_wins = 0
        self.sevenbeforesix_losses = 0

    def play_hand(self):
        while True:
            dice_roll = roll_die() + roll_die()
            if dice_roll == 6:
                self.sixbeforeseven_wins += 1
                self.sevenbeforesix_losses += 1
                break
            if dice_roll == 7:
                self.sevenbeforesix_wins += 1
                self.sixbeforeseven_losses += 1
                break

    def sixbeforeseven_results(self):
        return self.sixbeforeseven_wins, self.sixbeforeseven_losses

    def sevenbeforesix_results(self):
        return self.sevenbeforesix_wins, self.sevenbeforesix_losses


def sim_big_six_game(games_num, hands_per_game):
    games = []
    for game in range(games_num):
        bsg = big_six_game()
        for hand in range(hands_per_game):
            bsg.play_hand()
        games.append(bsg)

    roi_per_game = []
    winnings_per_game = []
    for game in games:
        wins, losses = game.sixbeforeseven_results()
        roi_per_game.append((wins - losses) / float(hands_per_game))
        winnings_per_game.append((wins - losses) * 5 * 2)

    mean_roi = round(sum(roi_per_game) / hands_per_game, 4)
    sigma = round(np.std(roi_per_game), 4)
    cost_per_hour = round(sum(winnings_per_game) / hands_per_game, 2)
    return mean_roi, sigma, cost_per_hour


def print_sim(games_played, hands_per_hour):
    six_bef_seven = sim_big_six_game(games_played, hands_per_hour)
    print(f"Assuming {hands_per_hour} hands are played per hour, over {games_played} games, each game taking an hour")
    print(f"The return on investment (ROI): {round(six_bef_seven[0]*100, 4)}%")
    print(f"The standard deviation: {six_bef_seven[1]*100}%")
    print(f"The hourly cost to play: ${six_bef_seven[2]}")


print_sim(100, 30)
