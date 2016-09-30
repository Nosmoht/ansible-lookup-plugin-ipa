Ansible IPA Lookup plugins
==========

- [Introduction](#introduction)
- [Usage](#usage)
 - [Group](#group)

# Introduction
Ansible lookup plugins to gather information about IPA objects using IPA API.
All plugins return a dictionary with all information as returned by the API.

# Usage

## Group

Gather information about IPA group "ipausers" and show them.

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
      ipa_group: '{{ lookup("ipa_group", "ipausers", ipa_host=ipa_host, ipa_user=ipa_user, ipa_pass=ipa_pass) }}'

  - debug:
      var: ipa_group
```
