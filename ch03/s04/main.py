import json


class StandardTags():
    def __init__(self):
        self.resource = {
            'customer': 'my-company',      # Creates a module using the prototype pattern that returns a copy of standard tags, such as customer, cost center, and business unit
            'automated': True,
            'cost_center': 123456,
            'business_unit': 'ecommerce'
        }


class ServerFactory:        #Creates a module using the factory pattern to create a Google computer instance (server) based on name, network, and tags
    def __init__(self, name, network, zone='us-central1-a', tags={}):
        self.name = name
        self.network = network      #Passes tags as a variable to the server module
        self.zone = zone
        self.tags = tags
        self.resource = self._build(). #Uses the module to create the JSON configuration for a server on the “default” network

    def _build(self):
        return {
            'resource': [
                {
                    'google_compute_instance': [        #Creates the Google compute instance (server) using a Terraform resource
                        {
                            self.name: [
                                {
                                    'allow_stopping_for_update': True,
                                    'boot_disk': [
                                        {
                                            'initialize_params': [
                                                {
                                                    'image': 'ubuntu-1804-lts'
                                                }
                                            ]
                                        }
                                    ],
                                    'machine_type': 'e2-micro',
                                    'name': self.name,
                                    'network_interface': [
                                        {
                                            'network': self.network
                                        }
                                    ],
                                    'zone': self.zone,
                                    'labels': self.tags #Adds the tags stored in the variable to the Google compute instance resource
                                }
                            ]
                        }
                    ]
                }
            ]
        }


if __name__ == "__main__":
    config = ServerFactory(     #Uses the module to create the JSON configuration for a server on the “default” network
        name='database-server', network='default',
        tags=StandardTags().resource)   #Uses the standard tags module to add tags to the server

    with open('main.tf.json', 'w') as outfile:  #Writes the Python dictionary to a JSON file to be executed by Terraform later 
        json.dump(config.resource, outfile,
                  sort_keys=True, indent=4)
