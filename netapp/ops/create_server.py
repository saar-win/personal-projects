import click
import time, yaml, os, json
import googleapiclient.discovery

path = os.path.abspath(".")

@click.command()
@click.option("--create_vm", is_flag=True, required=False, help="want to create vm?")
@click.option("--delete_vm", is_flag=True, required=False, help="want to delete vm?")
@click.option("--delete_disk", is_flag=True, required=False, help="want to delete vm?")

def main(**options):
    '''
    Get the action from the user
    '''
    vars = variable()
    if options['create_vm']:
        try:
            create_vm(vars)
        except Exception as e:
            print(e)
    if options['delete_vm']:
        try:
            delete_vm(vars, options)
        except Exception as e:
            print(e)

def list_instances(compute, project, zone):
    '''
    Get a list of instances
    '''
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

def create_instance(compute, project, zone, machine, name, image, disk_size, persistent_vol):
    '''
    Create the create instance itself
    '''
    image_response = compute.images().getFromFamily(
        project=image[0], family=image[1]).execute()
    source_disk_image = image_response['selfLink']
    machine_url = "zones/%s/machineTypes/" + machine
    machine_type = machine_url % zone
    startup_script = open(os.path.join(os.path.dirname(__file__), 'startup-script.sh'), 'r').read()
    config = {
        'name': name,
        'machineType': machine_type,
        'disks': [
            {'boot': True, 'autoDelete': True, "diskSizeGb": disk_size, 'initializeParams': {'sourceImage': source_disk_image}},
            {'boot': False, 'autoDelete': False, "source": f"projects/{project}/zones/{zone}/disks/{persistent_vol}", "deviceName": persistent_vol}
        ],
        'tags': { 'items': [ 'http-server', 'https-server' ]},
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [{'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}]}],

        'serviceAccounts': [{
            'email': 'default',
            'scopes': ['https://www.googleapis.com/auth/devstorage.read_write', 'https://www.googleapis.com/auth/logging.write']}],
        'firewalls': ['http-server', 'https-server'],
        'metadata': {
            'items':
            [
                { 'key': 'startup-script', 'value': startup_script }
            ]
        }
    }

    return compute.instances().insert(project=project, zone=zone, body=config).execute()

def vm_firewall(compute, vars, action):
    '''
    '''
    firewalls = [
    {
        "name": "vm-demo-firewall-allowed",
        "priority": "500",
        "targetTags": [ "http-server", "https-server" ],
        "allowed":
        [
            { "IPProtocol": "tcp", "ports": [ "80" ] },
            { "IPProtocol": "tcp", "ports": [ "443" ] }
        ],
        "sourceRanges": [ vars["allowed_to_connect"] ],
    },
    {
        "name": "vm-demo-firewall-denied",
        "priority": "1000",
        "targetTags": [ "http-server", "https-server" ],
        "denied":
        [
            { "IPProtocol": "tcp", "ports": [ "80" ] },
            { "IPProtocol": "tcp", "ports": [ "443" ] }
        ],
        "sourceRanges": [ vars["denied_to_connect"] ],
    }
    ]
    if action == "create":
        try:
            for firewall in firewalls:
                compute.firewalls().insert(project=vars['project_id'], body=firewall).execute()
        except Exception as e:
            raise Exception(e)
    if action == "delete":
        try:
            for firewall in firewalls:
                compute.firewalls().delete(project=vars['project_id'], firewall=firewall['name']).execute()
        except Exception as e:
            raise Exception(e)

def wait_for_operation(compute, project, zone, operation):
    '''
    wait for the end operation
    '''
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(project=project, zone=zone, operation=operation).execute()
        if result['status'] == 'DONE':
            print("Done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(1)

def persistent_disk(compute, vars, action):
    '''
    Create a persistent volume
    '''
    if action == "delete":
        print("Deleting persistent disk")
        operation = compute.disks().delete(project=vars['project_id'], zone=vars['zone'], disk=vars["persistent_disk"]).execute()
        return operation

    if disk_list(compute, vars):
        return ""
    print("Creating a disk for db")
    disk_body = {
        "name": vars["persistent_disk"],
        "sizeGb": vars["persistent_size"],
        "type": f"projects/{vars['project_id']}/zones/{vars['zone']}/diskTypes/pd-standard",
    }
    if action == "create":
        print("Creating persistent disk")
        return compute.disks().insert(project=vars['project_id'], zone=vars['zone'], body=disk_body).execute()

def disk_list(compute, vars):
    '''
    '''
    response = compute.disks().list(project=vars['project_id'], zone=vars['zone']).execute()
    if "items" in response:
        for disk in response['items']:
            if disk.get("name"):
                return True
            else:
                return None
    else:
        return None

def delete_vm(vars, options):
    '''
    Delete firewall and vm
    '''
    compute = googleapiclient.discovery.build('compute', 'v1')
    print('Deleting instance.')
    vm_firewall(compute, vars, "delete")
    operation = compute.instances().delete(project=vars['project_id'], zone=vars['zone'], instance=vars['instance_name']).execute()
    wait_for_operation(compute, vars['project_id'], vars['zone'], operation['name'])
    if options['delete_disk']:
        operation = persistent_disk(compute, vars, "delete")
    wait_for_operation(compute, vars['project_id'], vars['zone'], operation['name'])

def create_vm(vars):
    '''
    Create the vm with all the parameters
    '''
    compute = googleapiclient.discovery.build('compute', 'v1')
    print('Creating instance.')
    vm_firewall(compute, vars, "create")
    persistent_disk(compute, vars, "create")
    operation = create_instance(compute, vars['project_id'], vars['zone'], vars['machine'], vars['instance_name'], vars['image'], vars['disk_size'], vars["persistent_disk"])
    wait_for_operation(compute, vars["project_id"], vars["zone"], operation['name'])
    instances = list_instances(compute, vars["project_id"], vars["zone"])
    print('Instance in project %s and zone %s:' % (vars["project_id"], vars["zone"]))
    for instance in instances:
        url = f"https://console.cloud.google.com/compute/instancesDetail/zones/{vars['zone']}/instances/{instance['name']}?project={vars['project_id']}"
        for network in instance["networkInterfaces"][0]["accessConfigs"]: server_ip = network["natIP"]
        print(' - ' + url)
        print(' - ' + server_ip)
        print(' ----------- ')

def variable():
    '''
    Get the variables from the user yaml
    '''
    variables = yaml.load(
        open(f'{path}/ops/variables.yaml').read(), Loader=yaml.FullLoader)
    return variables['vm_settings']

if __name__ == '__main__':
    main()
