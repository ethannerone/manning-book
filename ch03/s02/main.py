import json


class Network: #Creates a module for the network, which uses the composition pattern to bundle the network and subnet together
    def __init__(self, region='us-central1'): #Sets the region to the default region, us-central1
        self._network_name = 'my-network' #sets up the Google network using a Terraform resource with the name “my-network”. GCP does not require a network CIDR block to be defined.
        self._subnet_name = f'{self._network_name}-subnet' #Sets up the Google subnetwork using a Terraform resource with the name “my-network-subnet
        self._subnet_cidr = '10.0.0.0/28' #Sets the subnet’s CIDR block as 10.0.0.0/28
        self._region = region #Sets the region to the default region, us-central1
        self.resource = self._build() #Uses the module to create the JSON configuration for the network and subnetwork

    def _build(self):
        return {
            'resource': [
                {
                    'google_compute_network': [
                        {
                            f'{self._network_name}': [
                                {
                                    'name': self._network_name #Sets up the Google network using a Terraform resource with the name “my-network”. GCP does not require a network CIDR block to be defined.
                                }
                            ]
                        }
                    ]
                },
                {
                    'google_compute_subnetwork': [ #Creates the Google subnetwork on the network by using a Terraform variable. Terraform dynamically references the network ID and inserts it to the subnetwork’s configuration for you.
                        {
                            f'{self._subnet_name}': [
                                {                           #Sets up the Google subnetwork using a Terraform resource with the name “my-network-subnet”
                                    'name': self._subnet_name,
                                    'ip_cidr_range': self._subnet_cidr,   #Sets the subnet’s CIDR block as 10.0.0.0/28
                                    'region': self._region,
                                    'network': f'${{google_compute_network.{self._network_name}.name}}'
                                }
                            ]
                        }
                    ]
                }
            ]
        }


if __name__ == "__main__":
    network = Network(). #Uses the module to create the JSON configuration for the network and subnetwork

    with open(f'main.tf.json', 'w') as outfile:
        json.dump(network.resource, outfile, sort_keys=True, indent=4) #Writes the Python dictionary to a JSON file to be executed by Terraform later
