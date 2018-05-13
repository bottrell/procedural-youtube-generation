The Procedural Youtube Generation bot was created by Jordan Bottrell of the University of Michigan in May 2018

The bot accesses a user-specified subreddit periodically, searching the top posts for video links.

The subreddit that I typically use as an example is /r/globaloffensive, as it's a subreddit almost specifically dedicated
to short clips and highlights from youtube or twitch.

The bot then downloads these top posts, parsing using beautifulSoup for Twitch clips and pyTube for youtube clips.

After downloading the clips, the bot concatenates all of the videos into a "highlight video", forcing the clips to a
1280x720 resolution, then uploads the highlight video to youtube.

To run the bot, you first need to pip install the packages found in requirements.txt, and open a python3 environment.
Then it's as simple as running the generate.py file, which holds the driver for the bot.

I plan to have the bot running perpetually in order to upload clips to my personal youtube channel. Future functionality
will include thumbnail generation, better title generation, description generation, and time limits on videos in order for
a more enjoyable end user experience.

Keep in mind that running the bot will constantly be uploading and dowloading videos of varying sizes, so users with slow
or capped internet should be weary when running the bot. 
