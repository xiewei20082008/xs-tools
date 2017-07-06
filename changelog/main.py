from gooey import Gooey, GooeyParser
import subprocess32 as subprocess
from subprocess32 import PIPE, Popen
import os
import datetime
import json

env = os.environ.copy()


def waitSubprocess(p):
    try:
        out, err = p.communicate(timeout=10)
        return out
    except TimeoutExpired:
        print 'subprocess time out.'
        p.kill()
        raise SubErr


def exe(cmd, cwd):
    p = subprocess.Popen(cmd, stderr=PIPE, stdout=PIPE,
                         cwd=cwd, env=env, shell=True)
    try:
        out = waitSubprocess(p)
        return out
    except "suberr":
        raise


@Gooey()
def main():
    data = None
    with open('config.json') as dataFile:
        data = json.load(dataFile)

    parser = GooeyParser()

    parser.add_argument(
        'repo',
        default=data['defaultRepo'],
        action='store'
    )

    parser.add_argument(
        'tagRange',
        default=data['defaultTagRange'],
        action='store'
    )

    args = parser.parse_args()

    currentTime = datetime.date.today()
    time = currentTime.strftime('%a %b %d %Y')
    name = data['signature']
    aimTag = args.tagRange.split('..')[1]
    tag = '- {tag}-1'.format(tag=aimTag)
    header = ' '.join(['*', time, name, tag])
    print header

    exe('git checkout master',
        '{codePath}/{repo}'.format(codePath=data['codePath'], repo=args.repo))
    t = exe('git log --no-merges --oneline {tagRange}'.format(tagRange=args.tagRange),
            '{codePath}/{repo}'.format(codePath=data['codePath'], repo=args.repo))
    for i in t.split('\n'):
        if i:
            print '- ' + ' '.join(i.split(' ')[1:])

    print ''
    print 'Update {repo} to {tag}'.format(repo=args.repo, tag=aimTag)
    print '============================================================='
    print '============================================================='


if __name__ == '__main__':
    main()
