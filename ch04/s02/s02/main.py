import json


class Network:
    def __init__(self, name="hello-network"):   #Creates the Google network using a Terraform resource named “hello-network”
        self.name = name
        self.resource = self._build()       #Uses the module to create the JSON configuration for the network

    def _build(self):
        return {
            'google_compute_network': [
                {
                    f'{self.name}': [
                        {
                            'name': self.name
                        }
                    ]
                }
            ]
        }


class Subnet:                           #Creates the Google subnetwork using a Terraform resource named after the region, us-central1
    def __init__(self, network, region='us-central1'):      #Passes the entire network object to the subnet. The subnet calls the network object for the attributes it needs.
        self.network = network
        self.name = region
        self.subnet_cidr = '10.0.0.0/28'
        self.region = region
        self.resource = self._build()

    def _build(self):
        return {
            'google_compute_subnetwork': [
                {
                    f'{self.name}': [
                        {
                            'name': self.name,
                            'ip_cidr_range': self.subnet_cidr,
                            'region': self.region,      
                            'network': self.network.name        #Interpolates the network name by retrieving it from the object
                        }
                    ]
                }
            ]
        }


class NetworkModule:
    def __init__(self, region='us-central1'):
        self._region = region
        self._network = Network()
        self._subnet = Subnet(self._network)
        self.resource = self._build()

    def _build(self):
        return [
            self._network.resource,
            self._subnet.resource
        ]

    class Output:
        def __init__(self, subnet_name):
            self.subnet_name = subnet_name

    def output(self):
        return self.Output(self._subnet.name)


class ServerModule:
    def __init__(self, name, network,
                 zone='us-central1-a'):
        self._name = name
        self._subnet_name = network.subnet_name
        self._zone = zone
        self.resource = self._build()

    def _build(self):
        return [{
            'google_compute_instance': [{
                self._name: [{
                    'allow_stopping_for_update': True,
                    'boot_disk': [{
                        'initialize_params': [{
                            'image': 'ubuntu-1804-lts'
                        }]
                    }],
                    'machine_type': 'e2-micro',
                    'name': self._name,
                    'zone': self._zone,
                    'network_interface': [{
                        'subnetwork': self._subnet_name
                    }]
                }]
            }]
        }]


if __name__ == "__main__":
    network = NetworkModule()       #Uses the module to create the JSON configuration for the network
    server = ServerModule("hello-world",
                          network.output())
    resources = {
        "resource": network.resource + server.resource
    }

    with open(f'main.tf.json', 'w') as outfile:
        json.dump(resources, outfile, sort_keys=True, indent=4)     #Writes the Python dictionary to a JSON file to be executed by Terraform later
