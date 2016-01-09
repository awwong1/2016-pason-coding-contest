import optparse
import gameinfo
import command
import communication
import json

from algorithm import Algorithm


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
            algo = Algorithm(self.game_info.team_name, self.game_info.client_token)
            raw_state_message = self.comm.receive(self.comm.Origin.PublishSocket)
            try:
                json_state_message = json.loads(raw_state_message)
                if json_state_message[self.cmd.COMM_TYPE] == command.CommType.GAME_STATE:
                    algo.parse_game_state(json_state_message)
                    actions = algo.generate_actions()
                    for action in actions:
                        self.comm.send(action)
                        """
                        # This never seemed to work, but actions performed fine
                        raw_command_message = self.comm.receive(self.comm.Origin.CommandSocket)
                        try:
                            json_command_message = json.loads(raw_command_message)
                            if json_command_message['resp'] == 'ok':
                                continue
                            else:
                                print "Command did not execute properly!"
                                print raw_command_message
                        except Exception:
                            print "Command did not return valid JSON message!"
                            print raw_command_message
                        """
                    continue
                elif json_state_message[self.cmd.COMM_TYPE] == command.CommType.GAME_START:
                    print "Game Name: %s" % json_state_message['game_name']
                    print "Timestamp: %s" % json_state_message['timestamp']
                    print "Game Number: %s out of %s" % (json_state_message['game_num'], json_state_message ['game_count'])
                    continue
                elif json_state_message[self.cmd.COMM_TYPE] == command.CommType.GAME_END:
                    print "Game Ended! Moving onto the next game..."
                    continue
                elif json_state_message[self.cmd.COMM_TYPE] == command.CommType.MATCH_END:
                    print "Match Ended!"
                    break
                else:
                    print "Something went wrong. No valid comm_type in server response but response is valid json!"
                    print json_state_message
                    continue
            except ValueError:
                # Not valid json, this must the match token string
                self.game_info.match_token = raw_state_message
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
