import numpy as np
import random
from bestbet.utils import KellyRatio, Moneyline2Prob, Moneyline2Odds

def MonteCarlo(ML_home: float, ML_opposition: float, estimated_bias: float, capital: float, true_bias: float, num_games: int, N_mc: int) -> np.ndarray:

    implied_home = Moneyline2Prob(ML_home)
    implied_opposition = Moneyline2Prob(ML_opposition)
    total_p = implied_home + implied_opposition
    vig_A = (total_p - 1)/2
    p = implied_home - vig_A + true_bias # true probability TEAM A wins

    X = KellyRatio(ML_home, ML_opposition, estimated_bias)
    b = Moneyline2Odds(ML_home)

    arr = capital*np.ones(N_mc)
    PlayRound = np.vectorize(PlayGame)

    for _ in range(num_games):
        coins = np.random.rand(N_mc) # flip N_mc coins for this round
        arr = PlayRound(cash=arr, coinflip=coins, kelly_ratio=X, p=p, b=b)
    return arr

def PlayGame(cash: float, coinflip: float, kelly_ratio: float, p: float, b: float) -> float:
    if coinflip < p:
        return cash*(1+b*kelly_ratio)
    else:
        return cash*(1-kelly_ratio)