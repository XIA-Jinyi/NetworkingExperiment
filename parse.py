from urllib.parse import unquote
from datetime import datetime
from email.mime.text import MIMEText
from sys import stderr
import subprocess
from os.path import abspath

def get_dict(data: str) -> dict[str:str]:
    result = {}
    for pair in data.split('&'):
        key, val = pair.split('=')
        result[key] = unquote(val)
    return result

if __name__ == '__main__':
    print('\033[0;36mParser launched!\033[0m')
    try:
        while input() != '':
            pass
        data = input()
    except:
        print('\033[0;33mParse failed: input error!\033[0m', file=stderr)
        exit()
    try:
        data_dict = get_dict(data)
    except:
        print('\033[0;33mParse failed: not the packet!\033[0m', file=stderr)
        exit()
    try:
        lines = ['From: %s\n' % data_dict['sendmailname']]
        if (val := data_dict.get('to')) != '':
            lines += [f'To: {val}\n']
        if (val := data_dict.get('cc')) != None:
            lines += [f'Cc: {val}\n']
        if (val := data_dict.get('bcc')) != None:
            lines += [f'Bcc: {val}\n']
        lines += ['Subject: %s\n' % data_dict['subject']]
        lines += ['Date: %s\n' % datetime.now().strftime('%a, %d %B %Y %H:%M:%S +0800')]
        lines += [str(MIMEText(data_dict['content__html'], 'html'))]
    except:
        print('\033[0;33mParse failed: syntax error!\033[0m', file=stderr)
        exit()
    try:
        file_name = datetime.now().strftime('%Y.%m.%d-%H.%M.%S.eml')
        with open(f'./saved/{file_name}', 'w') as fout:
            fout.writelines(lines)
    except:
        print('\033[1;31mParse failed: can\'t write email to file!\033[0m', file=stderr)
        exit(-16)
    print('\033[1;32mParse succeeded!\033[0m')
    print(f'Email has been saved to \"' + abspath(f'./saved/{file_name}') + "\".")
    process = subprocess.Popen(['.\\build\\Post\\Debug\\Post.exe'], stdin=subprocess.PIPE)
    process.stdin.write((abspath(f'./saved/{file_name}') + '\n').encode())
    process.stdin.close()
