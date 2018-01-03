# My Wedding Website

## Setup
1. Create `instance/config.py` and override the default variables in `config.py`
1. Save `service-credentials.json` for the spreadsheet in `instance/`

## Deploy
1. Add `inventories/web` file and add the IP address of the server you want to use.
  1. Look at `inventories/local` for reference
1. Create a variables file `group_vars/web/private.yml`.
  1. Add `domain_name: <mydomain.com>`
1. Run `ansible-playbook deploy/site.yml -i deploy/inventories/web --private-key "~/.ssh/id_rsa_digital_ocean"`
