from ansible_runner.config.runner import RunnerConfig
from ansible_runner.runner import Runner

def ansible_run(request_type : int, request_contents : dict):
    requests = {1: 'storage', 
                2: 'account', 
                3: 'email'}
    runner_config = RunnerConfig(private_data_dir ="./ansible", inventory="./inventory", playbook=f"/Users/arnavsajith/Documents/Projects/EMPT/it-helpdesk/ansible/{requests[request_type]}.yaml", extravars = request_contents)
    runner_config.prepare()
    rc = Runner(config=runner_config)
    rc.run()

