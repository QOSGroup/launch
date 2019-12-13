#!/usr/bin/python2.7
# -- coding: utf-8 --
import os
import string

cwd = os.getcwd()

VALIDATOR_FILE = "validators.txt"
ACCOUNT_FILE = "accounts.txt"
DELEGATOR_FILE = "delegations.txt"

validatorMap = {}
validatorfile = open(cwd + "/" + VALIDATOR_FILE,"r")
for v in validatorfile:
    v = v.strip()
    if len(v)<=0 or v[0] == '#':
        continue
    v = v.replace("\\ ", "_")
    v = ' '.join(v.split())
    vv = v.split(" ")
    if (len(vv)!=4 or string.index(vv[1], "qosacc") != 0 or len(vv[1]) != 45):
        print("validator format err: " + v)
        exit()
    validatorMap[vv[1]] = {}
print("%d validators find" % len(validatorMap.keys()))

delegatorMap = {}
delegatorfile = open(cwd + "/" + DELEGATOR_FILE,"r")
for d in delegatorfile:
    d = d.strip()
    if len(d)<=0 or d[0] == '#':
        continue
    d = ' '.join(d.split())
    dd = d.split(" ")
    if (len(dd)<3 or string.index(dd[0], "qosacc") != 0 or len(dd[0]) != 45 or string.index(dd[1], "qosacc") != 0 or len(dd[1]) != 45 or not dd[2].isdigit()):
        print("account format err: " + d)
        exit()
    if dd[0] not in validatorMap.keys():
        print("validator %s not found in delegation: %s"% (dd[0], d))
        exit()
    if dd[1] not in delegatorMap.keys():
        # [delegation, account_balance]
        delegatorMap[dd[1]] = [0, 0]
    delegatorMap[dd[1]][0] += int(dd[2])
    if dd[1] not in validatorMap[dd[0]].keys():
        validatorMap[dd[0]][dd[1]] = 0
    else:
        print("duplicated validator-delegator pair found, you may need to check: " + d)
    validatorMap[dd[0]][dd[1]] += int(dd[2])

accountfile = open(cwd + "/" + ACCOUNT_FILE,"r")
for d in accountfile:
    d = d.strip()
    if len(d)<=0 or d[0] == '#':
        continue
    d = ' '.join(d.split())
    dd = d.split(" ")
    if (len(dd)!=2 or string.index(dd[0], "qosacc") != 0 or len(dd[0]) != 45 or not dd[1].isdigit()):
        print("account format err: " + dd)
        exit()
    if dd[0] not in delegatorMap.keys():
        delegatorMap[dd[0]] = [0, 0]
    elif delegatorMap[dd[0]][1] > 0:
        print("duplicated account %s found, you may need to check" % dd[0])
        exit()
    delegatorMap[dd[0]][1] = int(dd[1])

account_ori = open(cwd + "/account_before_delegation.txt", 'w')
# team account
delegatorMap["qosacc1raqeulxtdp29r3k9xvklj49stqwyaqlvscyeey"] = [0, 1666666666664]
totalsupply = 49000000000000 - 10000000000000
for acc in delegatorMap.keys():
    account_ori.write("%s %d\n" % (acc, delegatorMap[acc][0] + delegatorMap[acc][1]))
    totalsupply -= (delegatorMap[acc][0] + delegatorMap[acc][1])
# reserve account
account_ori.write("qosacc1lkc3qrktxxmhslpyatcznwuq8yaqrg2agngm5z %d" % totalsupply)
account_ori.close()
