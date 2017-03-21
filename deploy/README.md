## Deploy

use [Ansible](http://docs.ansible.com/ansible/) to do all


##USAGE

**STEP 1**: install [Ansible](http://docs.ansible.com/ansible/intro_installation.html)
**STEP 2**: modify invertory file(deploy/playbooks/) to make your device reachable.
**STEP 3**: modify secrets.yml(deploy/playbooks/secrets.yml.exmaple), example following:
```
sender_mail: sender_mail
sender_pwd: password
mail_to: receiver_mail_split_by_comma
```
**STEP 4**:
```
cd deploy
ansible-playbook init_run.yml
```

**UPDATE** use this code:
```
cd deploy/
ansible-playbook update_run.yml
```

PS: if you want to stop. your will 'ps -ef |grep python' find the python process id(PID) and 'kill PID'.