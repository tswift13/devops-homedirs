#! /usr/bin/python
import json
import os
import re
import subprocess
from datetime import datetime

import requests
from ansible import utils


class CallbackModule(object):
    def __init__(self):
        self.playbook       = None
        self.inventory      = None
        self.disabled       = False
        self.slack_endpoint = None
        self.env_name       = None
        self.playbook_name  = None
        self.host_list      = None
        self.subset         = None
        self.tags           = None
        self.skip_tags      = None
        self.user           = None
        self.is_test        = None
        self.git_sha        = None
        self.git_decoration = None
        self.run_id         = None
        self.git_repo_name  = None
        self.is_git_repo    = None
        self.run_host       = None
        self.ansible_version = None

    def load_values(self):
        self.is_git_repo    = self.__git_data('rev-parse --git-dir') == '.git'

        self.playbook       = self.play.playbook
        self.inventory      = self.playbook.inventory
        self.hosts          = self.inventory.get_hosts()

        self.vars           = self.playbook.extra_vars
        self.vars.update(self.inventory.get_variables(self.hosts[0].name))

        self.slack_endpoint = self.vars.get('slack_endpoint')
        self.disabled       = self.vars.get('disable_slack')

        self.playbook_name  = os.path.basename(self.playbook.filename)
        self.host_list      = self.inventory.host_list
        self.subset         = ', '.join(self.inventory._subset) if self.inventory._subset else "--"
        self.tags           = ', '.join(self.playbook.only_tags) if self.playbook.only_tags else "--"
        self.skip_tags      = ', '.join(self.playbook.skip_tags) if self.playbook.skip_tags else "--"
        self.user           = self.playbook.remote_user
        self.is_test        = self.playbook.check
        self.run_id         = datetime.now().isoformat()
        self.run_host       = self.__get_run_host()
        self.ansible_version = utils.version_info(True)['string']

        if self.is_git_repo:
            git_sha = self.__git_data('log -n1 --pretty=format:%H')
            git_decoration = self.__git_data('log -n1 --pretty=format:%d')
            git_dirty = self.__git_data('status --porcelain')

            self.git_sha        = git_sha()[0]
            self.git_decoration = git_decoration()[0]
            self.git_dirty      = git_dirty()
            self.git_repo_name  = self.__git_repo_name()

        if self.disabled:
            utils.warning('Not posting to slack with disable_slack=yes')

    def __get_run_host(self):
        hostname_call =  subprocess.Popen('hostname -f',
                                          shell=True,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
        return hostname_call.stdout.readlines()[0]

    def __git_data(self, git_cmd):
        def git_datum():
            git_call = subprocess.Popen("git %s" % git_cmd,
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            output = git_call.stdout.readlines()
            return output
        return git_datum

    def __git_repo_name(self):
        basic_remotes = [ r[:-1] for r in self.__git_data('remote')() ]
        remotes = self.__git_data('remote -v')()
        decoration = self.__git_data('log -n1 --pretty=format:%D')()[0]

        branch_remote = None
        for remote in basic_remotes:
            for ref in decoration.split():
                if re.match("^%s" % remote, ref):
                    branch_remote = remote

        for remote in remotes:
            name = re.match('%s\tgit@github.com\:(.*?/.*?).git' % branch_remote, remote)
            if name:
                return name.groups()[0]

        return None

    def send_msg(self, msg):
        if not self.disabled:
            # JSON headers
            headers = {
                'Content-type': 'application/json',
                'Accept': 'text/plain'
            }

            # Send message to Slack endpoint
            try:
                response = requests.post(self.slack_endpoint,
                                         data=json.dumps(msg),
                                         headers=headers)
            except:
                utils.warning('Could not submit message to slack')

    def playbook_on_play_start(self, pattern):
        # Enable settings
        self.load_values()

        if not self.disabled:
            # Different color on test/check run
            color = "#FFA500" if self.is_test else "#969696"

            text = 'Executing with Ansible version {}'.format(self.ansible_version)

            if self.is_git_repo:
                if self.git_repo_name:
                    sha_msg = "<https://github.com/{0}/commit/{1}|{1:.8}>".format(
                        self.git_repo_name,
                        self.git_sha
                    )
                else:
                    sha_msg = "{:.8} (Does not exist on Github)".format(self.git_sha)

                dirty_msg = "[DIRTY]" if self.git_dirty else ""
                text

                text = text + "\ncommit {} {}\n{}".format(sha_msg,
                                                          dirty_msg,
                                                          self.git_decoration)


            # Build message on playbook start
            msg = {
                "attachments": [
                    {
                        "title": "[START] Playbook Reporting %s" % self.run_id,
                        # "pretext": "Playbook Reporting",
                        "text": text,
                        "fallback": "*Playbook Start*: _%s_\n" % self.playbook_name + \
                                    "*Invoked By*: _%s_\n" % self.user + \
                                    "*Inventory File*: _%s_\n" % self.host_list + \
                                    "*Tags*: _%s_\n" % self.tags + \
                                    "*Skip Tags*: _%s_\n" % self.skip_tags + \
                                    "*Limit*: _%s_\n" % self.subset,
                        "color": "%s" % (color),
                        "fields": [
                            {
                                "title": "Playbook",
                                "value": "%s" % (self.playbook_name),
                                "short": "true"
                            },
                            {
                                "title": "Invoked By",
                                "value": "{}@{}".format(self.user,
                                                        self.run_host),
                                "short": "true"
                            },
                            {
                                "title": "[--inventory-file]",
                                "value": "%s" % (self.host_list),
                                "short": "true"
                            },
                            {
                                "title": "[--limit]",
                                "value": "%s" % (self.subset),
                                "short": "true"
                            },
                            {
                                "title": "[--tags]",
                                "value": "%s" % (self.tags),
                                "short": "true"
                            },
                            {
                                "title": "[--skip-tags]",
                                "value": "%s" % (self.skip_tags),
                                "short": "true"
                            },
                            {
                                "title": "Environment",
                                "value": "%s" % (self.env_name),
                                "short": "true"
                            },
                            {
                                "title": "[--check]",
                                "value": "%s" % (self.is_test),
                                "short": "true"
                            }
                        ]
                    }
                ]
            }
            self.send_msg(msg)


    def playbook_on_stats(self, stats):
        failures            = False
        unreachable         = False
        servers_name        = ""
        servers_ok          = ""
        servers_skipped     = ""
        servers_changed     = ""
        servers_unreachable = ""
        servers_failures    = ""

        # Keep track of server stats
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            s = stats.summarize(h)
            h_short = h.split(".")[0]

            servers_name        += "%s\n" % (h)
            servers_ok          += "%s: %i\n" % (h_short, s['ok'])
            servers_skipped     += "%s: %i\n" % (h_short, s['skipped'])
            servers_changed     += "%s: %i\n" % (h_short, s['changed'])
            servers_unreachable += "%s: %i\n" % (h_short, s['unreachable'])
            servers_failures    += "%s: %i\n" % (h_short, s['failures'])

            # Global error triggers
            if s['unreachable'] > 0:
                unreachable = True
            if s['failures'] > 0:
                failures = True

        # Global error message
        if failures or unreachable:
            color = "danger"
            result = "Playbook complete: Failures detected :("
        else:
            color = "good"
            result = "Playbook complete: Great Success! :)"

        # Build message based off results
        msg = {
            "attachments": [
                {
                    "title": "[END] Playbook Reporting %s" % self.run_id,
                    "text": result,
                    "fallback": result,
                    "color": color,
                    "fields": [
                        {
                            "title": "Servers",
                            "value": "%s" % (servers_name),
                            "short": "false"
                        },
                        {
                            "title": "OK",
                            "value": "%s" % (servers_ok),
                            "short": "false"
                        },
                        {
                            "title": "Skipped",
                            "value": "%s" % (servers_skipped),
                            "short": "false"
                        },
                        {
                            "title": "Changed",
                            "value": "%s" % (servers_changed),
                            "short": "false"
                        },
                        {
                            "title": "Unreachable",
                            "value": "%s" % (servers_unreachable),
                            "short": "false"
                        },
                        {
                            "title": "Failures",
                            "value": "%s" % (servers_failures),
                            "short": "false"
                        }
                    ]
                }
            ]
        }
        self.send_msg(msg)
