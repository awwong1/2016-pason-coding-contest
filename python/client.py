import optparse
import gameinfo
import command
import communication
import json


class Client(object):
    """
    The main client class. Responsible for running the game.
    """

    def __init__(self):
        """
        Constructor
        """

        parser = optparse.OptionParser()
        parser.add_option('-t', help='specifies the team name', dest='team_name')
        parser.add_option('-p', help='specifies the teams password', dest='team_password')
        parser.add_option('-m', help='specifies the match token', dest='match_token')
        parser.add_option('-n', help='specifies the host name', dest='host_name')

        global opts
        (opts, args) = parser.parse_args()

        if opts.team_name is None or 0 == len(opts.team_name):
            print "team name is mandatory"
            parser.print_help()
            exit(1)

        if opts.match_token is None or 0 == len(opts.match_token):
            print "match token is mandatory"
            parser.print_help()
            exit(1)

        if opts.team_password is None or 0 == len(opts.team_password):
            print "team password is mandatory"
            parser.print_help()
            exit(1)

        if opts.host_name is None or 0 == len(opts.host_name):
            print "host name is mandatory"
            parser.print_help()
            exit(1)

        self.game_info = gameinfo.GameInfo(opts.team_name, opts.match_token, opts.team_password)
        self.cmd = command.Command()
        self.comm = communication.Communication(opts.host_name)

    def run(self):
        """
        Runs the game
        """
        print "Starting Battle Tanks Client..."

        connect_command = self.cmd.get_match_connect_command(self.game_info.team_name, self.game_info.match_token,
                                                             self.game_info.team_password)

        print 'Connecting to server...'
        self.comm.set_subscription(opts.match_token)
        self.game_info.client_token = self.comm.send(connect_command, self.cmd.CLIENT_TOKEN)

        print 'Received client token... %s' % self.game_info.client_token
        print 'Starting game...'

        while True:
            raw_state_message = self.comm.receive(self.comm.Origin.PublishSocket)
            try:
                json_state_message = json.loads(raw_state_message)
                if json_state_message[self.cmd.COMM_TYPE] == 'GAME_START':
                    print "Game Name: %s" % json_state_message['game_name']
                    print "Timestamp: %s" % json_state_message['timestamp']
                    print "Game Number: %s out of %s" % (json_state_message['game_num'], json_state_message ['game_count'])
                    continue
                if json_state_message[self.cmd.COMM_TYPE] == 'GAME_END':
                    print "Game Ended! Moving onto the next game..."
                    continue
                if json_state_message[self.cmd.COMM_TYPE] == 'MatchEnd':
                    print "Match Ended!"
                    break
                if json_state_message[self.cmd.COMM_TYPE] == 'GAMESTATE':
                    """
                    comm_type String The message type to indicate that this is a game state message.
                    timeRemaining Number The amount of time, in seconds, remaining in the game.
                    timestamp Number The current time, in milliseconds, that this state was generated.
                    map Object Describes the various attributes about the game map. More information is provided below.
                    players Array of Objects
                    Describes various attributes about the players in the game. More information is provided below.
                    """
                    # TODO: Fancy pro battle tank algorithm goes here
                    print json_state_message
            except ValueError:
                # Not valid json, this must the match token string
                self.game_info.match_token = raw_state_message
                print "Match Token: %s" % raw_state_message
                continue

        print 'Exiting...'
        exit()

    def exit(self):
        """
        cleanup and exit
        """
        self.comm.close()


if __name__ == "__main__":
    client = Client()
    try:
        client.run()
    except (SystemExit, KeyboardInterrupt):
        client.exit()
