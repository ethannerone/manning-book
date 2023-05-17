import json
import ipaddress


def _generate_subnet_name(address):
    address_identifier = format(ipaddress.ip_network(
        address).network_address).replace('.', '-')         #For a given subnet, generates the subnet name by dash-delimiting the IP address range and appending it to the “network”
    return f'network-{address_identifier}'


class SubnetFactory:        #Creates a module for the subnet, which uses the factory pattern to generate any number of subnets
    def __init__(self, address, region):
        self.name = _generate_subnet_name(address)
        self.address = address      #Passes the subnet’s address to the factory
        self.region = region        #Passes the subnet’s region to the factory
        self.network = 'default'    #Creates the subnets on the “default” network in this example
        self.resource = self._build()   #Uses the module to create the JSON configuration for the network and subnetwork

    def _build(self):
        return {
            'resource': [
                {
                    'google_compute_subnetwork': [
                        {
                            f'{self.name}': [
                                {
                                    'name': self.name,
                                    'ip_cidr_range': self.address,      #Creates the Google subnetwork using a Terraform resource based on the name, address, region, and network
                                    'region': self.region,
                                    'network': self.network
                                }
                            ]
                        }
                    ]
                }
            ]
        }


if __name__ == "__main__":
    subnets_and_regions = {
        '10.0.0.0/24': 'us-central1',
        '10.0.1.0/24': 'us-west1',      #For each subnet defined with its IP address range and region, creates a subnet using the factory module
        '10.0.2.0/24': 'us-east1',
    }

    for address, region in subnets_and_regions.items():

        subnetwork = SubnetFactory(address, region)

        with open(f'{_generate_subnet_name(address)}.tf.json', 'w') as outfile:
            json.dump(subnetwork.resource, outfile, sort_keys=True, indent=4)       #Writes the Python dictionary to a JSON file to be executed by Terraform later
