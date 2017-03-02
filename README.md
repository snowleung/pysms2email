# sms2email
Forwarding you iPhone SMS to your email list.
Work at python2.5(iOS6 cydia/Pyobjc), iphone4(iOS6) with cydia, using *hotmail* to send the message.

##HOW TO USE:

1. Upload all the file to your iphone
2. Fill the file environment_variable
3. Type this "source ./environment_variable && nohup python sms2email.py&" without quote(sms2email.py will run in background, only use 'ps -ef |grep python' can get it.)
4. Success if your mail recive subject with "SMS Monitor"


PS: if you want to stop. your will 'ps -ef |grep python' find the python process id(PID) and 'kill PID'.