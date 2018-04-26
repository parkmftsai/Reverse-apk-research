# import frida
# import sys
#
# session = frida.attach("hello")
# script = session.create_script(
# """
# Interceptor.attach(ptr("%s"), {
#     onEnter: function(args) {
#         args[0] = ptr(12345);
#     }
# });
# """
#
# % int(sys.argv[1], 16))
# print("%x" % int(sys.argv[1], 16))
#
# script.load()
# sys.stdin.read()

import codecs
import frida
import base64

def on_message(message, data):
    if message['type'] == 'send':
        print(message['payload'])
    elif message['type'] == 'error':
        print(message['stack'])

session = frida.attach("hello")
with codecs.open('./agent.js', 'r', 'utf-8') as f:
    source = f.read()
print(base64.b64encode("i am yhing"))
script = session.create_script(source)
script.on('message', on_message)
script.load()
print(script.exports.add(2, 3))
#print(script.exports.sub(5, 3))
session.detach()