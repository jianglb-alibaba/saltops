import yaml

from saltjob.salt_https_api import salt_api_token, salt_api_jobs
from saltjob.salt_token_id import token_id
from saltjob.tasks import scanHostJob

ins = salt_api_token({'fun': 'cp.push'},
                     SALT_REST_URL, {'X-Auth-Token': token_id()})
print(ins.CmdRun())
i = ins.sshRun()
print(i)
ins = salt_api_token({'fun': 'key.list_all'},
                     SALT_REST_URL, {'X-Auth-Token': token_id()})
print(ins.wheelRun()['return'][0]['data']['return'])
minions_list_all = salt_api_jobs(
    url=SALT_REST_URL + '/jobs',
    token=token_id()
)
voilet_test = minions_list_all.run()
while True:
    print(voilet_test)
rs = open('/home/kira/dev/github/saltops/doc/script/ls.sls', 'r')

r = yaml.load(rs)
print(r)
