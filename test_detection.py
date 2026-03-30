from detection.detector import detect_log_type

log = "SRC=192.168.1.1 DST=10.0.0.5 PROTO=6 SPT=443 DPT=51515 LABEL=BENIGN"

print(detect_log_type(log))