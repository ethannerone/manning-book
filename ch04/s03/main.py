import json
import re


class StorageBucketFacade:
    def __init__(self, name):       #Using the facade pattern, outputs the bucket name as part of the storage output object. This implements dependency inversion to abstract away unnecessary bucket attributes.
        self.name = name


class StorageBucketModule:          #Creates a low-level module for the GCP storage bucket, which uses the factory pattern to generate a bucket
    def __init__(self, name, location='US'):
        self.name = f'{name}-storage-bucket'        #Creates the Google storage bucket using a Terraform resource based on the name and location
        self.location = location
        self.resources = self._build()

    def _build(self):
        return {
            'resource': [
                {
                    'google_storage_bucket': [{
                        self.name: [{
                            'name': self.name,
                            'location': self.location,
                            'force_destroy': True       #Sets an attribute on the Google storage bucket to destroy it when you delete Terraform resources
                        }]
                    }]
                }
            ]
        }

    def outputs(self):      #Creates an output method for the module that returns a list of attributes for the storage bucket
        return StorageBucketFacade(self.name)


class StorageBucketAccessModule:    #Creates a high-level module to add access control rules to the storage bucket
    def __init__(self, bucket, user, role): #Passes the bucket’s output facade to the high-level module
        if not self._validate_user(user):   #Validates that the users passed to the module match valid user group types for all users or all authenticated users
            print("Please enter valid user or group ID")
            exit()
        if not self._validate_role(role):       #Validates that the roles passed to the module match valid roles in GCP
            print("Please enter valid role")
            exit()
        self.bucket = bucket
        self.user = user
        self.role = role
        self.resources = self._build()

    def _validate_role(self, role):
        valid_roles = ['READER', 'OWNER', 'WRITER']
        if role in valid_roles:
            return True
        return False

    def _validate_user(self, user):
        valid_users_group = ['allUsers', 'allAuthenticatedUsers']
        if user in valid_users_group:
            return True
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, user)):
            return True
        return False

    def _change_case(self):
        return re.sub('[^0-9a-zA-Z]+', '_', self.user)

    def _build(self):
        return {
            'resource': [{
                'google_storage_bucket_access_control': [{
                    self._change_case(): [{
                        'bucket': self.bucket.name,     #Creates Google storage bucket access control rules using a Terraform resource
                        'role': self.role,
                        'entity': self.user
                    }]
                }]
            }]
        }


if __name__ == "__main__":
    bucket = StorageBucketModule('hello-world')
    with open('bucket.tf.json', 'w') as outfile:
        json.dump(bucket.resources, outfile, sort_keys=True, indent=4)

    server = StorageBucketAccessModule(
        bucket.outputs(), 'allAuthenticatedUsers', 'READER')
    with open('bucket_access.tf.json', 'w') as outfile:
        json.dump(server.resources, outfile, sort_keys=True, indent=4)
