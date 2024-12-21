def simulate_evolution(initial_state, rules, iterations):
    """
    Simulates state evolution based on given rules.

    Args:
        initial_state (dict): Dictionary of initial state values.
        rules (callable): Function that defines evolution rules.
        iterations (int): Number of iterations to simulate.

    Returns:
        dict: Final state after all iterations.
    """
    state = initial_state
    for _ in range(iterations):
        state = rules(state)
    return state


def recursive_simulation(state, rules, memo=None):
    """
    Performs a recursive simulation with memoization.

    Args:
        state (hashable): Current state.
        rules (callable): Function that defines evolution rules.
        memo (dict, optional): Memoization dictionary.

    Returns:
        result: Result of the simulation.
    """
    if memo is None:
        memo = {}
    if state in memo:
        return memo[state]
    result = rules(state)
    memo[state] = result
    return result
