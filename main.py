import praw
from login import reddit
import markdowntable
from pokestarfansloggingsetup import setup_logger


def post_table(twitter):
    ta = markdowntable.Table('Post #')
    ta.all_columns('Title', 'Author' , 'Karma')
    p = [post for post in reddit.subreddit('The_Donald').search('site:twitter.com/%s subreddit:the_donald' %s twitter)]
    if len(p) > 0:
        for i in range(len(p)):
            po = p[i]
            ta.add_row(i, '[{}]({})'.format(po.title, 'https://www.reddit.com' + po.permalink), str(po.author). str(po.score))
        table = ta.table
    else:
        table = '**No Results Found**'
    reddit.subreddit('Russia_Lago').wiki.create('The_Donald/'+twitter,'# Results for {} \n'.format(twitter)+table)
    return 'https://www.reddit.com/r/RussiaLago/wiki/The_Donald/'+twitter
    
def work_with_match(comment):
    u = comment.body.lstrip('!twittercheck').strip()
    link = post_table(u)
    comment.reply('Here is the link to the list: {}'.format(link))
    logging.info('Met request of user {}. Wiki link is at {}'.format(comment.author, link))
    
def main():
    for comment in reddit.subreddit('all').stream.comments():
        try:
            if '!twittercheck' in comment.body:
                work_with_match(comment)
        except Exception:
            logging.error('Error with comment {}!'.format(str(comment)), exc_info = True)
            
if __name__ == '__main__':
    main()
