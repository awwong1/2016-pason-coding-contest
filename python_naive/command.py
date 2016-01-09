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

    TANK_ID = 'tank_id'
    DIRECTION = 'direction'
    DISTANCE = 'distance'
    RADS = 'rads'
    CONTROL = 'control'

    @staticmethod
    def get_match_connect_command(team_name, match_token, team_password):
        """
        Match Connect
        returns a json command to connect to an established match.
        :param team_password: String, team password. Created by the registered team.
        :param match_token: String, match_token. Given by the pason match server.
        :param team_name: String, team name. Created by the registered team.
        """
        cmd_dict = dict()
        cmd_dict[Command.COMM_TYPE] = CommType.MATCH_CONNECT
        cmd_dict[Command.TEAM_NAME] = team_name
        cmd_dict[Command.MATCH_TOKEN] = match_token
        cmd_dict[Command.PASSWORD] = team_password
        return json.dumps(cmd_dict)

    @staticmethod
    def get_movement_command(tank_id, direction, distance, client_token):
        """
        Game Move; Movement
        Movement control allows the tank to move forward or backward.
        Issuing a movement command during a movement command already taking place will cancel the original command and
        replace it with the new one.
        :param tank_id: A string formatted as xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. The identifier for the tank.
        :param direction: String FWD or REV
        :param distance: Any decimal value greater than or equal to 0. Tank movement in meters.
        :param client_token: A string formatted as xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        """
        cmd_dict = dict()
        cmd_dict[Command.TANK_ID] = tank_id
        cmd_dict[Command.COMM_TYPE] = CommType.MOVEMENT
        cmd_dict[Command.DIRECTION] = direction
        cmd_dict[Command.DISTANCE] = distance
        cmd_dict[Command.CLIENT_TOKEN] = client_token
        return json.dumps(cmd_dict)

    @staticmethod
    def get_tank_rotation_command(tank_id, direction, rads, client_token):
        """
        Game Move; Tank Rotation
        Tank rotation allows for a change in the direction of travel.
        :param tank_id: A string formatted as xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. The identifier for the tank.
        :param direction: String CW or CCW
        :param rads: Any decimal value in the range [0, 2*Pi].
        :param client_token: A string formatted as xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        """
        cmd_dict = dict()
        cmd_dict[Command.TANK_ID] = tank_id
        cmd_dict[Command.COMM_TYPE] = CommType.TANK_ROTATE
        cmd_dict[Command.DIRECTION] = direction
        cmd_dict[Command.RADS] = rads
        cmd_dict[Command.CLIENT_TOKEN] = client_token
        return json.dumps(cmd_dict)

    @staticmethod
    def get_turret_rotation_command(tank_id, direction, rads, client_token):
        """
        Game Move; Turret Rotation
        Turret rotation allows the player to point their tank's gun.
        :param tank_id: A string formatted as xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. The identifier for the tank.
        :param direction: String CW or CCW
        :param rads: Any decimal value in the range [0, 2*Pi].
        :param client_token: A string formatted as xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        """
        cmd_dict = dict()
        cmd_dict[Command.TANK_ID] = tank_id
        cmd_dict[Command.COMM_TYPE] = CommType.TURRET_ROTATE
        cmd_dict[Command.DIRECTION] = direction
        cmd_dict[Command.RADS] = rads
        cmd_dict[Command.CLIENT_TOKEN] = client_token
        return json.dumps(cmd_dict)

    @staticmethod
    def get_fire_command(tank_id, client_token):
        """
        Game Move; Fire
        Fire allows the player to command their tank to fire.
        :param tank_id: A string formatted as xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. The identifier for the tank.
        :param client_token: A string formatted as xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        """
        cmd_dict = dict()
        cmd_dict[Command.TANK_ID] = tank_id
        cmd_dict[Command.COMM_TYPE] = CommType.FIRE
        cmd_dict[Command.CLIENT_TOKEN] = client_token
        return json.dumps(cmd_dict)

    @staticmethod
    def get_stop_command(tank_id, control, client_token):
        """
        Game Move; Stop
        Allow cancellation of movement, and rotation of the tank, rotation of the turret, or fire commands.
        :param tank_id: A string formatted as xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. The identifier for the tank.
        :param control: String MOVE, ROTATE, ROTATE_TURRET, or FIRE
        :param client_token: A string formatted as xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        """
        cmd_dict = dict()
        cmd_dict[Command.TANK_ID] = tank_id
        cmd_dict[Command.COMM_TYPE] = CommType.STOP
        cmd_dict[Command.CONTROL] = control
        cmd_dict[Command.CLIENT_TOKEN] = client_token
        return json.dumps(cmd_dict)


class CommType(object):
    MATCH_CONNECT = 'MatchConnect'
    MOVEMENT = 'MOVE'
    TANK_ROTATE = 'ROTATE'
    TURRET_ROTATE = 'ROTATE_TURRET'
    FIRE = 'FIRE'
    STOP = 'STOP'

    GAME_START = 'GAME_START'
    GAME_END = 'GAME_END'
    GAME_STATE = 'GAMESTATE'
    MATCH_END = 'MatchEnd'
