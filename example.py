from mail_tm import MailTM

def main():
    # Initializing the client
    client = MailTM()

    # Getting the list of available domains
    domains = client.fetch_domains()
    if domains == None or len(domains) == 0: return
    print(f'List of available domains:\n{domains}\n')

    # Generating and registering a new random email address
    ap = client.register_random()
    if ap == None: return
    print(f'Registered (address, password) pair:\n{ap[0]}, {ap[1]}\n')

    # Getting the associated token
    token = client.bearer_token(ap[0], ap[1])
    print(f'Token:\n{token}\n')

    # Getting the list of received email:
    emails = client.fetch_emails(token)
    if emails == None: return
    print(f'There are currently {len(emails)} emails in the inbox:\n{emails}')

if __name__ == '__main__': main()