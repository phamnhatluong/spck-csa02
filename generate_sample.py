"""Tạo dữ liệu mẫu để test IndustryLens Streamlit"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

N = 600
start = datetime(2022, 1, 1)

industries    = ["Technology","Healthcare","Finance","Education","Manufacturing","Retail","Logistics"]
regions       = ["Hà Nội","TP.HCM","Đà Nẵng","Cần Thơ","Hải Phòng","Bình Dương","Đồng Nai"]
job_titles    = ["Software Engineer","Data Analyst","Product Manager","DevOps Engineer",
                 "UX Designer","Data Scientist","Backend Developer","Frontend Developer",
                 "ML Engineer","Business Analyst","QA Engineer","Cloud Architect"]
exp_levels    = ["Fresher","Junior","Senior"]
comp_levels   = ["Low","Medium","High"]
auto_risks    = ["Low","Medium","High"]
demand_labels = ["Growing","Stable","Declining"]
skill_pool    = ["Python","JavaScript","SQL","Machine Learning","React","Docker",
                 "AWS","TypeScript","Java","Communication","Go","Kubernetes",
                 "TensorFlow","Figma","Agile","Power BI","Excel","Spark"]

rows = []
for _ in range(N):
    exp  = random.choice(exp_levels)
    base = {"Fresher":7000,"Junior":14000,"Senior":28000}[exp]
    sal  = max(4000, base + np.random.normal(0,3500))
    # trend: slight growth over time
    date = start + timedelta(days=random.randint(0,900))
    sal  *= (1 + 0.0002 * (date - start).days)
    rows.append({
        "date":               date.strftime("%Y-%m-%d"),
        "industry":           random.choice(industries),
        "job_title":          random.choice(job_titles),
        "region":             random.choice(regions),
        "job_openings":       max(5, int(np.random.poisson(80) + (date-start).days*0.05)),
        "avg_salary":         round(sal, 2),
        "salary_growth_rate": round(np.random.uniform(2, 18), 2),
        "experience_level":   exp,
        "remote_ratio":       random.randint(0, 100),
        "required_skills":    ", ".join(random.sample(skill_pool, random.randint(2,6))),
        "competition_level":  random.choice(comp_levels),
        "automation_risk":    random.choice(auto_risks),
        "growth_score":       round(np.random.uniform(20,95), 1),
        "demand_forecast":    random.choice(demand_labels),
    })

df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
df.to_csv("sample_data.csv", index=False)
print(f"✅ Đã tạo {N} bản ghi → sample_data.csv")
print(df.head(3).to_string())
