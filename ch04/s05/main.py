import json
from server import ServerFactoryModule
from firewall import FirewallFactoryModule  #Imports the factory modules for the network, server, and firewall
from network import NetworkFactoryModule


class Mediator:                             #Creates a mediator to decide how and in which order to automate changes to resources
    def __init__(self, resource, **attributes):
        self.resources = self._create(resource, **attributes)

    def _create(self, resource, **attributes):          #When you call the mediator to create a resource like a network, server, or firewall, you allow the mediator to decide all the resources to configure.
        if isinstance(resource, FirewallFactoryModule):     #If you want to create a firewall rule as a resource, the mediator will recursively call itself to create the server first.
            server = ServerFactoryModule(resource._name)
            resources = self._create(server)
            firewall = FirewallFactoryModule(
                resource._name, depends_on=resources[1].outputs())      #After the mediator creates the server configuration, it builds the firewall rule configuration.
            resources.append(firewall)
        elif isinstance(resource, ServerFactoryModule):     #If you want to create a server as a resource, the mediator will recursively call itself to create the network first.
            network = NetworkFactoryModule(resource._name)
            resources = self._create(network)
            server = ServerFactoryModule(
                resource._name, depends_on=network.outputs())       #After the mediator creates the network configuration, it builds the server configuration.
            resources.append(server)
        else:
            resources = [resource]      #If you pass any other resource to the mediator, such as the network, it will build its default configuration.
        return resources

    def build(self):
        metadata = []
        for resource in self.resources:
            metadata += resource.build()        #Uses the module to create a list of resources from the mediator and render the JSON configuration
        return {'resource': metadata}


if __name__ == "__main__":
    name = 'hello-world'
    resource = FirewallFactoryModule(name)
    # Uncomment to create network only
    # resource = NetworkFactoryModule(name, ip_range='10.0.0.0/16')     #Passes the mediator a firewall resource. The mediator will create the network, server, and then the firewall configuration.
    # Uncomment to create server and network only
    # resource = ServerFactoryModule(name)
    mediator = Mediator(resource)

    with open('main.tf.json', 'w') as outfile:      #Writes the Python dictionary to a JSON file to be executed by Terraform later
        json.dump(mediator.build(), outfile, sort_keys=True, indent=4)
