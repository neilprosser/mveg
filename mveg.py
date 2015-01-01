import commands
import json
import sys
import time

def create_fs_lines(prefix, fs, timestamp):
    for value in fs['data']:
        path = value['path'].lstrip('/').replace('/', '_')
        print "%s.%s.%s %d %d" % (prefix, path, 'total_in_bytes', value['total_in_bytes'], timestamp)
        print "%s.%s.%s %d %d" % (prefix, path, 'free_in_bytes', value['free_in_bytes'], timestamp)
        print "%s.%s.%s %d %d" % (prefix, path, 'available_in_bytes', value['available_in_bytes'], timestamp)

def create_os_lines(prefix, os, timestamp):
    create_dictionary_lines("%s.%s" % (prefix, 'cpu'), os['cpu'], timestamp)
    create_dictionary_lines("%s.%s" % (prefix, 'mem'), os['mem'], timestamp)
    create_dictionary_lines("%s.%s" % (prefix, 'swap'), os['swap'], timestamp)
    print "%s.%s %d %d" % (prefix, 'uptime_in_millis', os['uptime_in_millis'], timestamp)
    load_average = os['load_average']
    print "%s.%s.%s %g %d" % (prefix, 'load_average', '1m', load_average[0], timestamp)
    print "%s.%s.%s %g %d" % (prefix, 'load_average', '5m', load_average[1], timestamp)
    print "%s.%s.%s %g %d" % (prefix, 'load_average', '15m', load_average[2], timestamp)

def sanitize(name):
    return name.replace(' ', '-')

def create_dictionary_lines(prefix, dictionary, timestamp):
    for name, value in dictionary.items():
        if name == 'timestamp':
            continue
        elif isinstance(value, int):
            print "%s.%s %d %d" % (prefix, sanitize(name), value, timestamp)
        elif isinstance(value, float):
            print "%s.%s %g %d" % (prefix, sanitize(name), value, timestamp)
        elif isinstance(value, dict):
            create_dictionary_lines("%s.%s" % (prefix, sanitize(name)), value, timestamp)


environment = sys.argv[1]
hostname = commands.getoutput('hostname').partition('.')[0].lower()
prefix = "%s.elasticsearch.%s" % (environment, hostname)

lines = []

data = sys.stdin.readlines()
for jsonline in data:
    nodes = json.loads(jsonline)['nodes']
    nodeId = nodes.keys()[0]
    node = nodes[nodeId]
    timestamp = node['timestamp'] / 1000

    create_dictionary_lines("%s.%s" % (prefix, 'indices'), node['indices'], timestamp)
    create_dictionary_lines("%s.%s" % (prefix, 'process'), node['process'], timestamp)
    create_dictionary_lines("%s.%s" % (prefix, 'jvm'), node['jvm'], timestamp)
    create_dictionary_lines("%s.%s" % (prefix, 'thread_pool'), node['thread_pool'], timestamp)
    create_dictionary_lines("%s.%s" % (prefix, 'transport'), node['transport'], timestamp)
    create_dictionary_lines("%s.%s" % (prefix, 'http'), node['http'], timestamp)
    create_dictionary_lines("%s.%s" % (prefix, 'network'), node['network'], timestamp)
    create_fs_lines("%s.%s" % (prefix, 'fs'), node['fs'], timestamp)
    create_os_lines("%s.%s" % (prefix, 'os'), node['os'], timestamp)

    print '\n'.join(lines)
