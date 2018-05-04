import frida

import sys
print("aaa!!!")
session = frida.attach("hello1")

script = session.create_script(
"""

var st = Memory.allocUtf8String("TESTMEPLZ!");
var f = new NativeFunction(ptr(0x400566), 'int', ['int','pointer']);

for(var i =0;i<100;i++)
f(5,st);


"""
)

# script = session.create_script(
# """
#
# Interceptor.attach(ptr(0x4005b6), {
#     onEnter: function(args) {
#          var n =100
#         args(ptr(n))
#    }
# });
# """
# )
#% int(sys.argv[1], 16))
#print("%x" % int(sys.argv[1], 16))

while(1):
    script.load()

    sys.stdin.read()

# import codecs
# import frida
# import base64
#
# def on_message(message, data):
#     if message['type'] == 'send':
#         print(message['payload'])
#     elif message['type'] == 'error':
#         print(message['stack'])
#
# #session = frida.attach("hello")
# session=frida.get_usb_device().attach("com.android.calendar")
# with codecs.open('./android.js', 'r', 'utf-8') as f:
#     source = f.read()
#
#
# script = session.create_script(source)
# script.on('message', on_message)
# script.load()
# print(script.exports.add())
# #print(script.exports.sub(5, 3))
# session.detach()