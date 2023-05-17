import json


def hello_server(name, network): # Passes the name and network as parameters to the configuration
    return {
        'resource': [
            {
                'google_compute_instance': [ # Uses Terraform’s google_compute_instance resource to configure a server
                    {
                        name: [
                            {
                                'allow_stopping_for_update': True,
                                'zone': 'us-central1-a',
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
                                'name': name,
                                'network_interface': [
                                    {
                                        'network': network # Sets the network by using the “network” variable
                                    }
                                ],
                                'labels': {
                                    'name': name,
                                    'purpose': 'manning-infrastructure-as-code'
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }


if __name__ == "__main__":
    config = hello_server(name='hello-world', network='default') #Sets the network dependency as the default network when you run the script

    with open('main.tf.json', 'w') as outfile:
        json.dump(config, outfile, sort_keys=True, indent=4) #Creates a JSON file with the server object and runs it with Terraform
