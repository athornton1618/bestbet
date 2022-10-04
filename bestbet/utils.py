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

def TrueProbability(ML_home: float, ML_opposition: float, estimated_bias: float)-> float:
    implied_home = Moneyline2Prob(ML_home)
    implied_opposition = Moneyline2Prob(ML_opposition)
    total_p = implied_home + implied_opposition
    vig_A = (total_p - 1)/2
    p = implied_home - vig_A + estimated_bias # true probability TEAM A wins
    return p

def Vig(ML_home: float, ML_opposition: float)-> float:
    implied_home = Moneyline2Prob(ML_home)
    implied_opposition = Moneyline2Prob(ML_opposition)
    total_p = implied_home + implied_opposition
    vig = (total_p - 1)
    return vig

def KellyRatio(ML_home: float, ML_opposition: float, estimated_bias: float, ) -> float:
    '''
    Compute Kelly Criterion ratio given probability p and odds b
    '''
    p = TrueProbability(ML_home, ML_opposition, estimated_bias)
    b = Moneyline2Odds(ML_home)
    kelly = p - (1-p)/b
    return kelly

def KellyBet(ML_home: float, ML_opposition: float,estimated_bias: float, capital: float) -> float:
    '''
    Determine the Kelly Criterion Bet for TEAM A, given the following inputs:

        ML_home: Moneyline odds for TEAM A

        ML_opposition: Moneyline odds for TEAM B

        capitol: Cash to bet

        estimated_bias: True probability of TEAM A win - implied probability TEAM A win
    '''
    kelly_ratio = KellyRatio(ML_home, ML_opposition, estimated_bias)
    bet = kelly_ratio*capital
    return bet   

def ExpectedGeometricGain(ML_home: float, ML_opposition: float, estimated_bias: float) -> float:
    '''
    Average expected geometric gain for one game, single kelly bet
    '''
    true_p = TrueProbability(ML_home, ML_opposition, estimated_bias)
    b = Moneyline2Odds(ML_home)
    X = KellyRatio(ML_home, ML_opposition, estimated_bias)
    r = (1+b*X)**true_p * (1-X)**(1-true_p)
    return r

def ExpectedEarningsManyGames(r: float, capital: float, num_games: int) -> float:
    '''
    Expected earnings over several games
    '''
    E = capital*(r**num_games -1)
    return E