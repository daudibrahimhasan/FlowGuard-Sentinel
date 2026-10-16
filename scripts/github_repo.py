"""Inspect or update this repository's GitHub metadata using Git Credential Manager."""
import argparse
import json
import subprocess
import urllib.error
import urllib.request

REPOSITORY = 'daudibrahimhasan/FlowGuard-Sentinel'
DESCRIPTION = ('Human-supervised SME finance copilot with 14-day cash-flow forecasting, '
               'exact-action approvals, deterministic policy checks, sandbox execution, '
               'outcome verification and tamper-evident audit logs.')
TOPICS = ['fintech', 'sme-finance', 'cash-flow-forecasting', 'ai-safety',
          'human-in-the-loop', 'llm-agents', 'openrouter', 'fastapi', 'nextjs',
          'typescript', 'python', 'sqlite']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='Update description and topics')
    args = parser.parse_args()
    result = subprocess.run(['git', 'credential', 'fill'],
                            input='protocol=https\nhost=github.com\n\n',
                            text=True, capture_output=True, check=True)
    credential = dict(line.split('=', 1) for line in result.stdout.splitlines() if '=' in line)
    token = credential.get('password')
    if not token:
        raise SystemExit('No GitHub credential was returned. Credentials were not printed.')

    def api(path, method='GET', body=None):
        request = urllib.request.Request('https://api.github.com' + path, method=method,
            headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json',
                     'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'FlowGuard-repository-setup',
                     'Content-Type': 'application/json'},
            data=json.dumps(body).encode() if body is not None else None)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            raise SystemExit(f'GitHub returned HTTP {error.code} for {method} {path}; no credentials printed.') from None

    account = api('/user')['login']
    if account.lower() != REPOSITORY.split('/')[0].lower():
        raise SystemExit(f'Authenticated GitHub account {account} does not match the requested owner.')
    if args.apply:
        api('/repos/' + REPOSITORY, 'PATCH', {'description': DESCRIPTION})
        api('/repos/' + REPOSITORY + '/topics', 'PUT', {'names': TOPICS})
    repository = api('/repos/' + REPOSITORY)
    print(json.dumps({key: repository.get(key) for key in
                      ('full_name', 'html_url', 'description', 'topics', 'default_branch',
                       'private', 'size', 'permissions')}, indent=2))


if __name__ == '__main__':
    main()
