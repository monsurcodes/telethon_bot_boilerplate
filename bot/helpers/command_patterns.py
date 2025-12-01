from bot.config import COMMAND_PREFIX

def command_pattern(cmd):
    return rf'^{COMMAND_PREFIX}{cmd}(?:@\w+)?$'

def args_command_pattern(cmd):
    return rf'^{COMMAND_PREFIX}{cmd}(?:@\w+)?(?:\s+(.*))?$'
