import sys, yaml, re

with open(sys.argv[1]) as f:
    cfg = yaml.safe_load(f)

issues=[]
for net in cfg.get('networks', []):
    name = net.get('ssid','(unknown)')
    auth = (net.get('auth') or '').upper()
    psk  = net.get('psk','')
    mfp  = (net.get('mfp') or 'optional').lower()  # 802.11w

    if auth in ('OPEN','NONE','WEP'):
        issues.append((name, 'High', f'Authentication is {auth}; use WPA2-PSK or WPA3-SAE'))
    if 'WPA2' in auth and len(psk)<12:
        issues.append((name, 'Medium', 'PSK shorter than 12 chars'))
    if 'WPA3' in auth and len(psk)<12 and 'SAE' in auth:
        issues.append((name, 'Medium', 'WPA3-SAE PSK should be strong'))
    if mfp != 'required':
        issues.append((name, 'Low', '802.11w (MFP) should be required'))

print('SSID,Severity,Message')
for s,se,msg in issues:
    print(f'{s},{se},{msg}')
