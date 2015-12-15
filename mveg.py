import commands
import httplib
import json
import sys

if len(sys.argv) != 6:
    sys.stderr.write('Not enough (or too many) arguments\n')
    sys.exit(1)

hostname = sys.argv[1].partition('.')[0].lower()
environment = sys.argv[2].lower()
application = sys.argv[3].lower()
prefix = '{0}.{1}.{2}'.format(environment, application, hostname)

host = sys.argv[4]
port = sys.argv[5]

connection = httplib.HTTPConnection(host, port)

def tidy_up():
    connection.close()

def request_and_response_or_bail(method, url, message):
    try:
        connection.request(method, url)
        return connection.getresponse().read()
    except:
        tidy_up()
        sys.stderr.write('{0}\n'.format(message))
        sys.exit(1)

def create_fs_lines(prefix, fs, timestamp):
    create_dictionary_lines("%s.%s" % (prefix, 'total'), fs['total'], timestamp)
    for value in fs['data']:
        path = value['path'].lstrip('/').replace('/', '_')
        create_dictionary_lines("%s.%s" % (prefix, path), value, timestamp)

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

data = request_and_response_or_bail('GET', '/_nodes/_local/stats/?all=true', 'Error while retrieving stats.')
stats = json.loads(data)
nodes = stats['nodes']
nodeId = nodes.keys()[0]
node = nodes[nodeId]
timestamp = node['timestamp'] / 1000

create_dictionary_lines("%s.%s" % (prefix, 'indices'), node['indices'], timestamp)
create_dictionary_lines("%s.%s" % (prefix, 'os'), node['os'], timestamp)
create_dictionary_lines("%s.%s" % (prefix, 'process'), node['process'], timestamp)
create_dictionary_lines("%s.%s" % (prefix, 'jvm'), node['jvm'], timestamp)
create_dictionary_lines("%s.%s" % (prefix, 'thread_pool'), node['thread_pool'], timestamp)
create_fs_lines("%s.%s" % (prefix, 'fs'), node['fs'], timestamp)
create_dictionary_lines("%s.%s" % (prefix, 'transport'), node['transport'], timestamp)
create_dictionary_lines("%s.%s" % (prefix, 'http'), node['http'], timestamp)
create_dictionary_lines("%s.%s" % (prefix, 'breakers'), node['breakers'], timestamp)
create_dictionary_lines("%s.%s" % (prefix, 'script'), node['script'], timestamp)

tidy_up()