Ansible IPA Lookup plugins
==========

- [Usage](#usage)

# Usage
```yaml
---
- hosts: localhost
  connection: local
  vars:
    ipa_host: ipa-server.example.com
    ipa_user: admin
    ipa_pass: T0ps3cr3t
  tasks:
  - name: get IPA group information
    set_fact:
      ipa_group: '{{ lookup("ipa_group", name="ipausers", ipa_host=ipa_host, ipa_user=ipa_user, ipa_pass=ipa_pass) }}'

  - debug:
      var: ipa_group
```
