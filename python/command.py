import json


class Command(object):
    """
    creates json commands that can be sent to the server
    """
    CLIENT_TOKEN = 'client_token'
    COMM_TYPE = 'comm_type'
    NUM_PLAYERS = 'num_players'
    TEAM_NAME = 'team_name'
    MATCH_TOKEN = 'match_token'
    PASSWORD = 'password'
    GAME_MOVE = 'GameMove'
    GAME_END = 'GameEnd'
    MATCH_END = 'MatchEnd'

    @staticmethod
    def get_match_connect_command(team_name, match_token, team_password):
        """
        returns a json command to connect to an established match.
        :param team_password: String, team password. Created by the registered team.
        :param match_token: String, match_token. Given by the pason match server.
        :param team_name: String, team name. Created by the registered team.
        """
        game_dict = dict()
        game_dict[Command.COMM_TYPE] = CommType.MATCH_CONNECT
        game_dict[Command.TEAM_NAME] = team_name
        game_dict[Command.MATCH_TOKEN] = match_token
        game_dict[Command.PASSWORD] = team_password
        return json.dumps(game_dict)


class CommType(object):
    MATCH_CONNECT = 'MatchConnect'
