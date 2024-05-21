# Cilium

## Parse hubble flows

- Capture flows with
```
kubectl --context $MYCONTEXT -n kube-system exec -ti $CILIUMPOD -- hubble observe flows --output json --follow > capture.json
```

- Parse flows with
```
python3 parse-hubble-flows.py capture.json > flows.csv
```
