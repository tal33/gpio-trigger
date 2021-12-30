# gpio-trigger

* trigger arbitrary action when a gpio button is pressed on a Raspberry Pi
* supported actions are
  * curling a URL
  * executing a command line
* This is a fork of [gpio-trigger from layereight](https://github.com/layereight/gpio-trigger) to tailor it to my needs.
  * switch from gpio-pin to board-pin (BCM) numbering to be consistent with pirc522 and statusled in my MFRC522-triffer fork
  * moved shutdown to BCM pin 5 (GPIO 3) since this pin can be used to wakeup the PI as well
  * added 'Next'-command for volumio to Pin 13 (GPIO 27)

# Usage

```
gpio-trigger.py <*board*_pin_number> <action_type> <action>
```

* example:
```
gpio-trigger.py 13 curl 'http://localhost:3000/api/v1/commands/?cmd=next'
gpio-trigger.py 5 command 'shutdown -h now'
```

# Automated Installation
* automated installation is achieved by using [Ansible](https://docs.ansible.com/ansible/latest/index.html)
* Ansible is an automation tool, if you wanna know more about it have a look at 
  https://docs.ansible.com/ansible/latest/index.html
* replace the contents of the file *inventory* to point to your music box (e.g. my_raspi_host)
* since this contains your password it is recommended that you *copy* inventory to a new file *my-inventory* (which is ignopred from git) so you don't accidentally push your settings
* execute the ansible playbook, it might execute for a while if it needs to update / install stuff
```
$ cd gpio-trigger/ansible
$ ansible-playbook -i my-inventory gpio-trigger.yml 
```
