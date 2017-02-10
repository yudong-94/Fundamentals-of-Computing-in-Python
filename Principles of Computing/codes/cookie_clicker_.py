"""
Cookie Clicker Simulator
"""

# http://www.codeskulptor.org/#user41_8zAo6X9SmkRmKzZ.py

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(30)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._time = 0.0
        self._total_cookie = 0.0
        self._current_cookie = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        history_information = ''
        #for time_point in self._history:
        #    history_information += 'time    ' + str(time_point[0]) + '\n'
        #    history_information += 'bought  ' + str(time_point[1]) +'\n'
        #    history_information += 'costs   ' + str(time_point[2]) +'\n'
        #    history_information += 'total cookies ' + str(time_point[3]) +'\n\n'
        history_information += 'final time '+ str(self._time) + '\n'
        history_information += 'final cookie ' + str(self._current_cookie) + '\n'
        history_information += 'total cookie '+ str(self._total_cookie) + '\n'
        history_information += 'current cps ' + str(self._cps) + '\n'
        #history_information += str(self._history[-1])
        return history_information

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookie

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._current_cookie >= cookies:
            return 0.0
        else:
            time_left = (cookies - self._current_cookie) / self._cps
            if time_left - int(time_left) > 0:
                return int(time_left) + 1.0
            else:
                return time_left

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            pass
        else:
            self._time += time
            self._total_cookie += time * self._cps
            self._current_cookie += time * self._cps


    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookie < cost:
            pass
        else:
            self._current_cookie -= cost
            self._cps += additional_cps
            self._history.append((self._time, item_name, cost, self._total_cookie))

#state_test = ClickerState()
#print state_test
#state_test.wait(15.0)
#state_test.buy_item('Cursor', 15, 0.1)
#state_test.wait(15.0)
#state_test.buy_item('Cursor', 15, 0.1)
#print state_test
#print 'current cookies '+ str(state_test.get_cookies())
#print 'current cps ' + str(state_test.get_cps())
#print 'current time ' + str(state_test.get_time())
#print 'history ' + str(state_test.get_history())
#print state_test.time_until(50)

def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    copy_build_info = build_info.clone()
    clicker_state = ClickerState()
    time_left = duration
    while clicker_state.get_time() <= duration:
        current_cookies = clicker_state.get_cookies()
        current_cps = clicker_state.get_cps()
        history = clicker_state.get_history()
        #print 'time left', time_left
        item = strategy(current_cookies, current_cps, history, time_left, copy_build_info)
        #print item
        if item == None:
            break
        else:
            item_cost = copy_build_info.get_cost(item)
            time_to_buy = clicker_state.time_until(item_cost)
            if duration < clicker_state.get_time() + time_to_buy:
                break
            else:
                clicker_state.wait(time_to_buy)
                #print 'time to buy', time_to_buy
                #print 'current time', clicker_state.get_time()
                item_cps = copy_build_info.get_cps(item)
                clicker_state.buy_item(item, item_cost, item_cps)
                copy_build_info.update_item(item)
                time_left = duration - clicker_state.get_time()
        #print 'time left', time_left
        #print 'current cookie', clicker_state.get_cookies()
        #print 'current cps', clicker_state.get_cps()
    clicker_state.wait(time_left)

    return clicker_state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    item_list = build_info.build_items()
    afford_items = []
    for item in item_list:
        if cookies + cps * time_left >= build_info.get_cost(item):
            afford_items.append(item)
    if len(afford_items) == 0:
        return None
    else:
        cheapest_item = afford_items[0]
        cheapest_cost = build_info.get_cost(afford_items[0])
        for item in afford_items:
            if build_info.get_cost(item) < cheapest_cost:
                cheapest_cost = build_info.get_cost(item)
                cheapest_item = item
        return cheapest_item


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    item_list = build_info.build_items()
    afford_items = []
    for item in item_list:
        if cookies + cps * time_left >= build_info.get_cost(item):
            afford_items.append(item)
    if len(afford_items) == 0:
        return None
    else:
        expensive_item = afford_items[0]
        expensive_cost = build_info.get_cost(afford_items[0])
        for item in afford_items:
            if build_info.get_cost(item) > expensive_cost:
                expensive_cost = build_info.get_cost(item)
                expensive_item = item
        return expensive_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    Always choose the most cost-efficient one:
    cost-efficient = cost / future_cps
    """
    item_list = build_info.build_items()
    afford_items = []
    for item in item_list:
        if cookies + cps * time_left >= build_info.get_cost(item):
            afford_items.append(item)
    if len(afford_items) == 0:
        return None
    else:
        effcient_item = afford_items[0]
        best_efficiency = efficiency(afford_items[0], build_info)
        for item in afford_items:
            if efficiency(item, build_info) < best_efficiency:
                best_efficiency = efficiency(item, build_info)
                effcient_item = item
        return effcient_item

def efficiency(item, build_info):
    '''
    function to calculate efficiency of each item.
    '''
    cost = build_info.get_cost(item)
    add_cps = build_info.get_cps(item)
    return cost / add_cps

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

#run()
