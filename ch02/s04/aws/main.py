import json

 "provider": [
         {
             "aws": [
                 {
                     "access_key": "AKIARU66GPGZY7NEVVGR",
                     "secret_key": "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",
                     "region": "us-east-1"
                 }
             ]
         }


def hello_server(name, network):
    return {
        'resource': [
            {
                'aws_instance': [
                    {
                        name: [
                            {
                                'ami': '${data.aws_ami.ubuntu.id}',
                                'instance_type': 't2.micro',
                                'subnet_id': network,
                                'tags': {
                                    'Name': name,
                                    'Purpose': 'manning-infrastructure-as-code'
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }


if __name__ == "__main__":
    config = hello_server(name='hello-world', network='${data.aws_subnet.default.id}')

    with open('main.tf.json', 'w') as outfile:
        json.dump(config, outfile, sort_keys=True, indent=4)
