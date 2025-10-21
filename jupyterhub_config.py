"""
JupyterHub configuration for NOMAD NORTH development environment
"""
from dockerspawner import DockerSpawner

c = get_config()  # noqa: F821

# Basic JupyterHub settings
c.JupyterHub.bind_url = 'http://:9000/nomad-oasis/north'
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8081

# Service for NOMAD to communicate with JupyterHub
c.JupyterHub.services = [
    {
        'name': 'nomad-service',
        'admin': True,
        'api_token': 'secret-token',  # Match this with nomad.yaml
    }
]

# Allow named servers (different tools)
c.JupyterHub.allow_named_servers = True
c.JupyterHub.default_server_name = 'jupyter'

# Use DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner

# Docker spawner configuration
c.DockerSpawner.image = 'jupyter/base-notebook:latest'  # Default image
c.DockerSpawner.network_name = 'nomad_oasis_network'
c.DockerSpawner.remove = True
c.DockerSpawner.prefix = 'nomad_north'

# Timeouts
c.DockerSpawner.http_timeout = 300
c.DockerSpawner.start_timeout = 600

# Pre-spawn hook to configure tools
def pre_spawn(spawner):
    """Configure spawner based on user options"""
    user_options = spawner.user_options
    
    # Mount user home directory
    user_home = user_options.get('user_home')
    if user_home:
        spawner.volumes[user_home['host_path']] = {
            'mode': 'rw',
            'bind': user_home['mount_path'],
        }
    
    # Mount upload directories
    uploads = user_options.get('uploads', [])
    for upload in uploads:
        spawner.volumes[upload['host_path']] = {
            'mode': 'rw',
            'bind': upload['mount_path'],
        }
    
    # Configure tool-specific settings
    tool = user_options.get('tool')
    if tool:
        if tool.get('image'):
            spawner.image = tool['image']
        if tool.get('cmd'):
            spawner.cmd = tool['cmd']
        if tool.get('default_url'):
            spawner.default_url = tool['default_url']
        
        # Environment variables
        environment = user_options.get('environment', {})
        spawner.environment.update(environment)

c.Spawner.pre_spawn_hook = pre_spawn

# Simple authentication for development (NO SECURITY!)
# In production, you'd use OAuthenticator with Keycloak
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'
c.DummyAuthenticator.password = "devpassword"  # Any password works
c.Authenticator.auto_login = True
c.Authenticator.allow_all = True
