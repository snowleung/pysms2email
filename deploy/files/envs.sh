#sender config
launchctl setenv USER_MAIL "{{ sender_mail }}"&&launchctl setenv USER_PASSWD "{{ sender_pwd }}"&&launchctl setenv MAIL_TO "{{ mail_to }}"
