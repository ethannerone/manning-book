import json


class NetworkModuleOutput:      #Creates an object that captures the schema of the network module’s output. This makes it easier for the server to retrieve the subnet name.
    def __init__(self):
        with open('network/terraform.tfstate', 'r') as network_state:
            network_attributes = json.load(network_state)
        self.name = network_attributes['outputs']['name']['value']      #The object for the network output parses the value of the subnet name from the JSON object.


class ServerFactoryModule:      #Creates a module for the server, which uses the factory pattern
    def __init__(self, name, zone='us-central1-a'):     #Creates the Google compute instance using a Terraform resource with a name and zone
        self._name = name
        self._network = NetworkModuleOutput()   #The server module calls the network output object, which contains the subnet name parsed from the network module’s JSON file.
        self._zone = zone
        self.resources = self._build()
                                                  #Uses the module to create the JSON configuration for the server using the subnetwork name
    def _build(self):
        return {
            'resource': [{
                'google_compute_instance': [{
                    self._name: [{
                        'allow_stopping_for_update': True,
                        'boot_disk': [{
                            'initialize_params': [{
                                'image': 'ubuntu-1804-lts'      #Creates the Google compute instance using a Terraform resource with a name and zone
                            }]
                        }],
                        'machine_type': 'e2-micro',
                        'name': self._name,
                        'zone': self._zone,
                        'network_interface': [{ #The server module references the network output’s name and passes it to the “subnetwork” field.
                            'subnetwork': self._network.name
                        }]
                    }]
                }]
            }]
        }


if __name__ == "__main__":
    server = ServerFactoryModule(name='hello-world')
    with open('main.tf.json', 'w') as outfile:
        json.dump(server.resources, outfile, sort_keys=True, indent=4) #Writes the Python dictionary to a JSON file to be executed by Terraform later
