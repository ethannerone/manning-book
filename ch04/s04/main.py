# Note: This example will not apply successfully
# with Terraform because it uses mock users and
# groups. However, it will successfully pass a plan.

import json
import access


class GCPIdentityAdapter:       #Creates an adapter to map generic role types to Google role types
    EMAIL_DOMAIN = 'example.com'        #Sets the email domain as a constant, which you’ll append to each user

    def __init__(self, metadata):
        gcp_roles = {  # A
            'read': 'roles/viewer',  # A
            'write': 'roles/editor',  # A   Creates a dictionary to map generic roles to GCP-specific permissions and roles
            'admin': 'roles/owner'  # A
        }  # A
        self.gcp_users = []
        for permission, users in metadata.items():      #For each permission and user, builds a tuple with the user, GCP identity, and role
            for user in users:
                self.gcp_users.append(
                    (user, self._get_gcp_identity(user),    #Transforms the usernames to GCP-specific member terminology, which uses user type and email address
                        gcp_roles.get(permission)))

    def _get_gcp_identity(self, user):  # B
        if 'team' in user:      #If the username has “team,” the GCP identity needs to be prefixed with “group” and suffixed with the email domain.
            return f'group:{user}@{self.EMAIL_DOMAIN}'
        elif 'automation' in user:
            return f'serviceAccount:{user}@{self.EMAIL_DOMAIN}' #If the username has “automation,” the GCP identity needs to be prefixed with “serviceAccount” and suffixed with the email domain.
        else:
            return f'user:{user}@{self.EMAIL_DOMAIN}'       #For all other users, the GCP identity needs to be prefixed with “user” and suffixed with the email domain.

    def outputs(self):
        return self.gcp_users       #Outputs the list of tuples containing the users, GCP identities, and roles


class GCPProjectUsers:  # C Creates a module for the GCP project users, which uses the factory pattern to attach users to GCP roles for a given project
    def __init__(self, project, users):
        self._project = project
        self._users = users
        self.resources = self._build()      #Uses the module to create the JSON configuration for the project’s users and roles

    def _build(self):
        resources = []
        for (user, member, role) in self._users:        #Creates a dictionary to map generic roles to GCP-specific permissions and roles
            resources.append({
                'google_project_iam_member': [{
                    user: [{
                        'role': role,
                        'member': member,       #Creates a list of Google project IAM members using a Terraform resource. The list retrieves the GCP identity, role, and project to attach a username to read, write, or administrator permissions in GCP.
                        'project': self._project
                    }]
                }]
            })
        return {
            'resource': resources
        }


if __name__ == "__main__":
    users = GCPIdentityAdapter(     #Creates an adapter to map generic role types to Google role types
        access.Infrastructure().resources).outputs()

    with open('main.tf.json', 'w') as outfile:
        json.dump(
            GCPProjectUsers(
                'infrastructure-as-code-book',      #Writes the Python dictionary to a JSON file to be executed by Terraform later
                users).resources, outfile, sort_keys=True, indent=4)
