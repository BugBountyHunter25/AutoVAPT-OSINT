from scripts.run_osint import run_osint_stage

if __name__ == '__main__':
    domain = input("Enter domain: ")
    password = input("Enter password to check (optional): ") or None
    result = run_osint_stage(domain, password)
    print(result)
