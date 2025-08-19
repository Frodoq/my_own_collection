#!/usr/bin/python

# Copyright: (c) 2023, Your Name <your@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Create a text file.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This module creates a text file with specified content at a given path.

options:
    path:
        description: The absolute path where the file should be created.
        required: true
        type: str
    content:
        description: The content to write into the file.
        required: true
        type: str
author:
    - Your Name (@Frodoq)
'''

EXAMPLES = r'''
- name: Create a simple text file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/testfile.txt
    content: Hello, World!
'''

RETURN = r'''
path:
    description: The path of the created file.
    type: str
    returned: always
    sample: '/tmp/testfile.txt'
content:
    description: The content that was written to the file.
    type: str
    returned: always
    sample: 'Hello, World!'
'''

from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path='',
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Extract parameters
    path = module.params['path']
    content = module.params['content']

    result['path'] = path
    result['content'] = content

    # Check if the file already exists with the same content
    if os.path.exists(path):
        with open(path, 'r') as existing_file:
            existing_content = existing_file.read()
        if existing_content == content:
            # File exists and content is the same -> no change
            module.exit_json(**result)
        else:
            # File exists but content is different -> mark changed
            result['changed'] = True
    else:
        # File doesn't exist -> mark changed
        result['changed'] = True

    # If in check mode, exit without making changes
    if module.check_mode:
        module.exit_json(**result)

    # Actually create/write the file
    try:
        with open(path, 'w') as file:
            file.write(content)
    except Exception as e:
        module.fail_json(msg=f"Failed to create file: {str(e)}", **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
