from maze_server.maze_handler.MazeHandler import MazeHandler

maze_handler = MazeHandler()
while True:
    option = input("option: ").lower()
    if option == "n" or option == 's' or option == 'e' or option == 'w':
        maze_handler.move_player(option.upper(), 'test')
    elif option == 'make':
        maze_handler.create_maze()
    elif option == 'create':
        maze_handler.create_team('test')
