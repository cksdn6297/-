#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import re
import numpy as np
import pandas as pd

# csv 파일들이 있는 폴더 (지금 레포 루트라면 ".")
BASE_DIR = "."

# 파일 패턴 (csv)
pattern = "FWM_power=*mW_*.csv"

# 파일명에서 파워 추출
POWER_RE = re.compile(r"FWM_power=([0-9.]+)mW")

records = []

files = glob.glob(os.path.join(BASE_DIR, pattern))

print("찾은 파일 개수:", len(files))

for path in files:
    name = os.path.basename(path)
    m = POWER_RE.search(name)
    if not m:
        print("파워 파싱 실패:", name)
        continue

    power = float(m.group(1))

    df = pd.read_csv(path)

    # FWM 신호 컬럼 이름이 정확히 "FWM[V]"인지 확인
    # 다르면 print(df.columns)로 보고 이름을 바꿔줘.
    fwm = df["FWM[V]"].values
    file_mean = float(np.mean(fwm))

    records.append([power, file_mean])

df_raw = pd.DataFrame(records, columns=["Power_mW", "FileMean"])

df_group = (
    df_raw
    .groupby("Power_mW")["FileMean"]
    .agg(["mean", "std", "count"])
    .reset_index()
)

df_group.columns = ["Power_mW", "FWM_Mean", "FWM_Std", "N_Runs"]

out_path = os.path.join(BASE_DIR, "BeamPower_vs_FWM_Mean.csv")
df_group.to_csv(out_path, index=False, encoding="utf-8-sig")

print(df_group)
print("저장:", os.path.abspath(out_path))
