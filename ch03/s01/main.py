import json
import os


class DatabaseGoogleProject:
    def __init__(self): #  Creates an object for the database Google project
        self.name = 'databases'  # A Sets up the Google project using a Terraform resource with the name “databases”
        self.organization = os.environ.get('USER')  # B Gets the operating system user and sets it to the organization variable
        self.project_id = f'{self.name}-{self.organization}'  # B Makes a unique project ID based on the project name and operating system user so GCP can create the project
        self.resource = self._build() #Creates a DatabaseGoogleProject to generate the JSON configuration for the project

    def _build(self):
        return {
            'resource': [
                {
                    'google_project': [                 #
                        {                               #
                            'databases': [              #
                                {                       #
                                    'name': self.name,  # ^ Sets up the Google project using a Terraform resource with the name “databases”
                                    'project_id': self.project_id   # Makes a unique project ID based on the project name and operating system user so GCP can create the project
                                }
                            ]
                        }
                    ]
                }
            ]
        }


if __name__ == "__main__":
    project = DatabaseGoogleProject()  # C Creates a DatabaseGoogleProject to generate the JSON configuration for the project

    with open('main.tf.json', 'w') as outfile:  # D Writes the Python dictionary to a JSON file to be executed by Terraform later
        json.dump(project.resource, outfile, sort_keys=True, indent=4)  # D 
