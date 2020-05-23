import argparse
import configparser

import twitter


class TwitterApp:

    def __init__(self, filename):
        # Parse values from configuration file
        config = configparser.ConfigParser()
        config.read(filename)

        consumer_key = config['DEFAULT']['consumerKey']
        consumer_secret = config['DEFAULT']['consumerSecret']
        access_token = config['DEFAULT']['accessToken']
        access_token_secret = config['DEFAULT']['accessTokenSecret']

        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token,
                               access_token_secret=access_token_secret,
                               tweet_mode='extended')

    # Write the the newest 100 followers of the specified user name in a file named Twitter_Followers.txt
    def write_followers(self, screen_name):
        results = self.api.GetFollowersPaged(screen_name=screen_name,count=100)
        followers = results[2]

        with open("Twitter_Followers.txt", 'w', encoding="utf-8") as file:
            file.write("{} is followed by:\n".format(screen_name))
            for follower in followers:
                file.write("\t{}\n".format(follower.screen_name))

    # Write the last 100 tweets of the specified user to a file named Twitter_Timeline.txt
    def write_timeline(self, screen_name):

        with open("Twitter_Timeline.txt", 'w', encoding="utf-8") as file:
            timeline = self.api.GetUserTimeline(screen_name=screen_name, count=100)

            file.write("Latest tweets from {}:\n\n".format(screen_name))
            for status in timeline:
               file.write("Url:  https://twitter.com/i/web/status/{}\n".format(status.id))
               file.write("Created at: {}\n".format(status.created_at))
               file.write(" {}\n".format(status.full_text))


def main():

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('screen_name', help='Twitter screen_name to print information on')
    parser.add_argument("-c", "--config-file",
                        help="Path to configuration file containing API information.",
                        required=True)
    args = parser.parse_args()

    # Construct class for interacting with Twitter API
    app = TwitterApp(args.config_file)

    # Write latest tweets/followers to output files
    screen_name = args.screen_name
    app.write_timeline(screen_name)
    app.write_followers(screen_name)


if __name__ == '__main__':
    main()
