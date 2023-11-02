from ansible_runner.config.runner import RunnerConfig
from ansible_runner.runner import Runner

def ansible_run(request_type : int, request_contents : dict):
    requests = {0: 'invalid_request',
                1: 'storage', 
                2: 'manage_account', 
                3: 'query_account',
                4: 'manage_users'}
    runner_config = RunnerConfig(private_data_dir ="./ansible", inventory="./inventory2.yaml", playbook=f"/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/ansible/{requests[request_type]}.yaml", extravars = request_contents)
    runner_config.prepare()
    rc = Runner(config=runner_config)
    rc.run()

