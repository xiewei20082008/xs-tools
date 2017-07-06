'''
PIN file generator
'''


import argparse
import os
import wget
from gooey import Gooey, GooeyParser

pinTemplate = """\
{{
   "URL": "ssh://git@code.citrite.net/{repo}/{pinRepo}.git",
   "commitish": "{branch}",
   "patchqueue": "{branch}"
}}
"""


def genPin(args):
    for i in args.pinRepo.split(';'):
        content = pinTemplate.format(repo=args.repo, pinRepo=i,
                                     branch=args.branch)
        f = open(os.path.join(args.path, i + '.pin'), 'wb')
        f.write(content)
        f.close()
        print i + ': OK.'


def manualBuild(args):
    print 'rm -r ~/rpmbuild ~/src'
    print 'mkdir -p ~/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}'
    print 'mkdir -p ~/src && cd ~/src'

    print ''
    url = "https://code.citrite.net/projects/XS/repos/xenserver-specs/raw/SPECS/{buildRepo}.spec?at=refs/heads/{branch}".format(
        repo=args.repo, branch=args.branch, buildRepo=args.buildRepo)
    print "curl -o {buildRepo}.spec '".format(buildRepo=args.buildRepo) + url + "'"
    wget.download(url)
    f = open(args.buildRepo + '.spec')
    versionNum = ''
    for line in f:
        if line.startswith('Version'):
            i = line.split(' ')
            versionNum = i[1].strip()
            break
    # print 'versionNum is' + versionNum
    print ''
    f.close()
    os.remove(args.buildRepo + '.spec')
    print "curl -o ~/rpmbuild/SOURCES/{buildRepo}-{versionNum}.tar.gz 'https://code.citrite.net/rest/archive/latest/projects/{repo}/repos/{buildRepo}/archive?at=refs%2Fheads%2F{branch}&format=tar.gz&prefix={buildRepo}-{versionNum}'".format(
        buildRepo=args.buildRepo, repo=args.repo, branch=args.branch, versionNum=versionNum)

    print ''
    print 'spectool -g -R {0}.spec'.format(args.buildRepo)
    print 'rpmbuild -ba {0}.spec'.format(args.buildRepo)

    print 'cd ~/rpmbuild/RPMS/'


@Gooey()
def main():
    parser = GooeyParser()

    parser.add_argument(
        'repo',
        default='~weix',
        action='store')

    parser.add_argument(
        'branch',
        default='private/weix/req-440',
        action='store')

    relatedRepos = 'guest-templates-json;linux-guest-loader;xenserver-pv-tools;xapi'

    parser.add_argument(
        'pinRepo',
        default=relatedRepos,
        action='store')

    parser.add_argument(
        'path',
        default=r'g:/tmp/1',
        action='store')

    parser.add_argument(
        'mode', choices=['Gen pin', 'Manual build'], default='Manual build')
    parser.add_argument('--buildRepo', choices=relatedRepos.split(';'))

    args = parser.parse_args()
    operationMapping = {
        'Gen pin': genPin,
        'Manual build': manualBuild
    }

    operationMapping[args.mode](args)
    print '============================================================='
    print '============================================================='



if __name__ == '__main__':
    main()
