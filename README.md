# Othello AI Agents

This othello ai agent is developed in CSC384 Artificail Intelligence at the University of Toronto.
Users may play against two ai agents that utilizes Min-Max and Alpha-Beta prunning respectively to explore the game search tree and select the best move.
The two agents also deploy depth limit, state caching and node ordering heuristics to accelerate the searching process and reduce memory usage.
I am also working on another agent that implements the monte carlo tree search algorithm and compare their runtime.

# Acknowledgement
This assignments is based on one used in Columbia University's Artifical Intelligence Course (COMS W4701).
Special thanks to Daniel Bauer, who originally developed the start code.

# Getting started
The othello gui can be run by typing $python3 otherllo_gui.py -d board_size -a agent.py, where the parameter board_size is an integer representing the dimension of the baord and agent.py is the ai agent that you wish to play against. You can choose to play against the agent that utilizes the Min-Max strategy by running $python3 otherllo_gui.py -d board_size -a agent.py -m whereas running $python3 otherllo_gui.py -d board_size -a agent.py will have you play against the same agent using the Alpha-Beta prunning strategy. Note that without any acceleration techniques, these algorithms are quite slow so limit the board size to 4 as the agents are programmed to lose if they take more than 10 seconds to compute their move.

# Depth Limit
We can speed up the agents using a depth limit on their search. For example, running $python3 otherllo_gui.py -d board_size -a agent.py -m -l 5 will run the Min-Max agent with a depth limit of 5 imposed on its search. Feel free to explore the effects of running the agents with different depth limit.

# Caching States
We can further speed up the algorithms by caching the states we have seen before. To do this, run $python3 otherllo_gui.py -d board_size -a agent.py -m -c and the algorithm will cache the states we have seen and avoid repeated calculations.

# Node Ordering Heuristic
This speed up only works for the Alpha-Beta prunning agent and will first explore the options that lead to a better result. Calling $python3 otherllo_gui.py -d board_size -a agent.py -o will run the Alpha-Beta prunning agent that orders its options according to this rule: the moves that results in the highest number of the AI agent's disks minus the number of opponent's disks will be explopred first. 

# A sophiscated AI agent
Combining all the accelerating techniques we have mentioned before gives us a pretty challenging agent to play against. Try playing on a 8x8 board with an agent that utilizes state caching, alpha-beta pruning and node ordering and depth limit by typing $python3 otherllo_gui.py -d 8 -a agent.py -l 5 -c -o.
