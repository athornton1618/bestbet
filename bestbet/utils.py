import numpy as np

def Moneyline2Prob(ML: float) -> float:
    '''
    Convert moneyline odd to implied probability
    '''
    if ML > 0:
        p = 100/(100+ML)
    else:
        p = -ML/(100-ML)
    return p

def Moneyline2Odds(ML: float) -> float:
    '''
    Convert moneyline odd to mathematical odd
    '''
    if ML > 0:
        b = ML/100 
    else:
        b = -100/ML
    return b

def TrueProbability(MLteamA: float, MLteamB: float, teamAunder: float)-> float:
    implied_A = Moneyline2Prob(MLteamA)
    implied_B = Moneyline2Prob(MLteamB)
    total_p = implied_A + implied_B
    vig_A = (total_p - 1)/2
    p = implied_A - vig_A + teamAunder # true probability TEAM A wins
    return p

def Vig(MLteamA: float, MLteamB: float)-> float:
    implied_A = Moneyline2Prob(MLteamA)
    implied_B = Moneyline2Prob(MLteamB)
    total_p = implied_A + implied_B
    vig = (total_p - 1)
    return vig

def KellyRatio(p: float, b: float) -> float:
    '''
    Compute Kelly Criterion ratio given probability p and odds b
    '''
    kelly = p - (1-p)/b
    return kelly

def KellyBet(MLteamA: float, MLteamB: float, teamAunder: float, capital: float) -> float:
    '''
    Determine the Kelly Criterion Bet for TEAM A, given the following inputs:

        MLteamA: Moneyline odds for TEAM A

        MLteamB: Moneyline odds for TEAM B

        capitol: Cash to bet

        teamAunder: True probability of TEAM A win - implied probability TEAM A win
    '''

    true_p = TrueProbability(MLteamA, MLteamB, teamAunder)
    b = Moneyline2Odds(MLteamA)
    kelly_ratio = KellyRatio(true_p, b)
    bet = kelly_ratio*capital
    return bet   

def ExpectedGeometricGain(MLteamA: float, MLteamB: float, teamAunder: float) -> float:
    '''
    Average expected geometric gain for one game, single kelly bet
    '''
    true_p = TrueProbability(MLteamA, MLteamB, teamAunder)
    b = Moneyline2Odds(MLteamA)
    X = KellyRatio(true_p, b)
    r = (1+b*X)**true_p * (1-X)**(1-true_p)
    return r

def ExpectedEarningsManyGames(r: float, capital: float, num_games: int) -> float:
    '''
    Expected earnings over several games
    '''
    E = capital*(r**num_games -1)
    return E