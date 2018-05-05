import praw

reddit = praw.Reddit(client_id='da1iTPWzHVxDRg',
                     client_secret='3l-8FZ4tecVMx9VeFyeLKt4vCuU',
                     password='Cabrera_24',
                     user_agent='testscript by /u/fakebot3',
                     username='Siqq_cs')


subreddit = reddit.subreddit('globaloffensive')
for submission in subreddit.hot(limit=25):
    print(submission.url,end="\n\n\n")