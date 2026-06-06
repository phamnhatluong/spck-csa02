"""
generate_all_samples.py
Tạo 6 bộ dữ liệu mẫu cho các ngành khác nhau:
  1. technology   — Công nghệ thông tin
  2. healthcare   — Y tế & Dược phẩm
  3. finance      — Tài chính & Ngân hàng
  4. logistics    — Logistics & Vận tải
  5. retail       — Bán lẻ & Thương mại điện tử
  6. education    — Giáo dục & Đào tạo
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

OUT = "sample_data"
os.makedirs(OUT, exist_ok=True)

# ─── Shared config ─────────────────────────────────────────────────────────────
REGIONS_VN = ["Hà Nội", "TP.HCM", "Đà Nẵng", "Cần Thơ", "Hải Phòng", "Bình Dương", "Đồng Nai"]
REGIONS_GLOBAL = ["Hanoi", "Ho Chi Minh City", "Da Nang", "Singapore", "Bangkok", "Manila", "Jakarta"]
EXP    = ["Fresher", "Junior", "Senior"]
COMP   = ["Low", "Medium", "High"]
RISK   = ["Low", "Medium", "High"]
DEMAND = ["Growing", "Stable", "Declining"]

rng = np.random.default_rng(42)
random.seed(42)

def days_offset(start, n): return start + timedelta(days=int(n))

def make_base(n, start_date, regions):
    dates = [start_date + timedelta(days=random.randint(0, 900)) for _ in range(n)]
    return sorted(dates), regions

def salary_for(exp, base, noise=3000):
    mult = {"Fresher": 1.0, "Junior": 1.9, "Senior": 3.6}[exp]
    return max(base * 0.4, base * mult + rng.normal(0, noise))

# ══════════════════════════════════════════════════════════════════════════════
# 1. TECHNOLOGY
# ══════════════════════════════════════════════════════════════════════════════
def gen_technology(n=700):
    start = datetime(2022, 1, 1)
    titles = [
        "Software Engineer", "Data Scientist", "ML Engineer", "DevOps Engineer",
        "Backend Developer", "Frontend Developer", "Cloud Architect", "QA Engineer",
        "Product Manager", "Data Analyst", "Security Engineer", "Full Stack Developer",
    ]
    skills_pool = [
        "Python", "JavaScript", "TypeScript", "React", "Node.js", "Docker",
        "Kubernetes", "AWS", "Azure", "SQL", "TensorFlow", "Go", "Rust",
        "Machine Learning", "CI/CD", "GraphQL", "Redis", "MongoDB", "Spark",
    ]
    rows = []
    for i in range(n):
        dt  = start + timedelta(days=random.randint(0, 900))
        exp = random.choice(EXP)
        base_sal = 12000
        sal = salary_for(exp, base_sal, 4000) * (1 + 0.00025 * (dt - start).days)
        rows.append({
            "date":               dt.strftime("%Y-%m-%d"),
            "industry":           "Technology",
            "job_title":          random.choice(titles),
            "region":             random.choice(REGIONS_GLOBAL),
            "job_openings":       max(5, int(rng.poisson(120) + (dt-start).days * 0.08)),
            "avg_salary":         round(sal, 2),
            "salary_growth_rate": round(rng.uniform(5, 20), 2),
            "experience_level":   exp,
            "remote_ratio":       random.randint(40, 100),
            "required_skills":    ", ".join(random.sample(skills_pool, random.randint(3, 7))),
            "competition_level":  random.choices(COMP, weights=[1, 3, 5])[0],
            "automation_risk":    random.choices(RISK, weights=[3, 4, 2])[0],
            "growth_score":       round(rng.uniform(55, 98), 1),
            "demand_forecast":    random.choices(DEMAND, weights=[6, 3, 1])[0],
        })
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    path = f"{OUT}/technology_sector.csv"
    df.to_csv(path, index=False)
    print(f"✅ {path}  ({len(df)} rows)")
    return df

# ══════════════════════════════════════════════════════════════════════════════
# 2. HEALTHCARE
# ══════════════════════════════════════════════════════════════════════════════
def gen_healthcare(n=600):
    start = datetime(2021, 6, 1)
    titles = [
        "General Practitioner", "Nurse Practitioner", "Pharmacist", "Radiologist",
        "Medical Data Analyst", "Healthcare IT Specialist", "Biomedical Engineer",
        "Hospital Administrator", "Surgeon", "Physical Therapist", "Clinical Researcher",
        "Telemedicine Physician",
    ]
    skills_pool = [
        "Patient Care", "EMR Systems", "Clinical Research", "Pharmacology",
        "Medical Coding", "HL7/FHIR", "Data Analysis", "Radiology", "Surgery",
        "HIPAA Compliance", "Python", "SQL", "AI Diagnostics", "Telemedicine",
    ]
    rows = []
    for i in range(n):
        dt  = start + timedelta(days=random.randint(0, 1000))
        exp = random.choice(EXP)
        sal = salary_for(exp, 10000, 3500) * (1 + 0.00015 * (dt - start).days)
        rows.append({
            "date":               dt.strftime("%Y-%m-%d"),
            "industry":           "Healthcare",
            "job_title":          random.choice(titles),
            "region":             random.choice(REGIONS_VN),
            "job_openings":       max(5, int(rng.poisson(80) + (dt-start).days * 0.04)),
            "avg_salary":         round(sal, 2),
            "salary_growth_rate": round(rng.uniform(3, 12), 2),
            "experience_level":   exp,
            "remote_ratio":       random.randint(0, 40),
            "required_skills":    ", ".join(random.sample(skills_pool, random.randint(2, 5))),
            "competition_level":  random.choices(COMP, weights=[2, 4, 3])[0],
            "automation_risk":    random.choices(RISK, weights=[5, 3, 1])[0],
            "growth_score":       round(rng.uniform(45, 85), 1),
            "demand_forecast":    random.choices(DEMAND, weights=[5, 4, 1])[0],
        })
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    path = f"{OUT}/healthcare_sector.csv"
    df.to_csv(path, index=False)
    print(f"✅ {path}  ({len(df)} rows)")
    return df

# ══════════════════════════════════════════════════════════════════════════════
# 3. FINANCE
# ══════════════════════════════════════════════════════════════════════════════
def gen_finance(n=650):
    start = datetime(2021, 1, 1)
    titles = [
        "Financial Analyst", "Investment Banker", "Risk Manager", "Quantitative Analyst",
        "Compliance Officer", "FinTech Developer", "Credit Analyst", "Actuary",
        "Portfolio Manager", "Blockchain Developer", "RegTech Specialist",
        "Chief Financial Officer",
    ]
    skills_pool = [
        "Excel", "SQL", "Python", "Bloomberg Terminal", "Risk Modeling", "CFA",
        "Blockchain", "Solidity", "Financial Modelling", "Tableau", "Power BI",
        "Basel III", "AML", "FX Trading", "Options Pricing", "Machine Learning",
    ]
    rows = []
    for i in range(n):
        dt  = start + timedelta(days=random.randint(0, 1000))
        exp = random.choice(EXP)
        sal = salary_for(exp, 14000, 5000) * (1 + 0.00018 * (dt - start).days)
        rows.append({
            "date":               dt.strftime("%Y-%m-%d"),
            "industry":           "Finance",
            "job_title":          random.choice(titles),
            "region":             random.choice(REGIONS_GLOBAL),
            "job_openings":       max(5, int(rng.poisson(70) + (dt-start).days * 0.03)),
            "avg_salary":         round(sal, 2),
            "salary_growth_rate": round(rng.uniform(4, 16), 2),
            "experience_level":   exp,
            "remote_ratio":       random.randint(15, 65),
            "required_skills":    ", ".join(random.sample(skills_pool, random.randint(3, 6))),
            "competition_level":  random.choices(COMP, weights=[1, 3, 5])[0],
            "automation_risk":    random.choices(RISK, weights=[2, 5, 4])[0],
            "growth_score":       round(rng.uniform(40, 80), 1),
            "demand_forecast":    random.choices(DEMAND, weights=[4, 5, 2])[0],
        })
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    path = f"{OUT}/finance_sector.csv"
    df.to_csv(path, index=False)
    print(f"✅ {path}  ({len(df)} rows)")
    return df

# ══════════════════════════════════════════════════════════════════════════════
# 4. LOGISTICS
# ══════════════════════════════════════════════════════════════════════════════
def gen_logistics(n=500):
    start = datetime(2022, 3, 1)
    titles = [
        "Supply Chain Analyst", "Warehouse Manager", "Fleet Operations Manager",
        "Logistics Coordinator", "Freight Broker", "Last-Mile Delivery Specialist",
        "Cold Chain Manager", "Procurement Specialist", "Customs Officer",
        "Transportation Engineer", "3PL Account Manager",
    ]
    skills_pool = [
        "SAP WMS", "Route Optimization", "ERP Systems", "Excel", "Power BI",
        "Supply Chain Management", "Last-Mile Logistics", "Cold Chain", "Customs",
        "Freight Forwarding", "IoT Tracking", "SQL", "Python", "Negotiation",
    ]
    rows = []
    for i in range(n):
        dt  = start + timedelta(days=random.randint(0, 800))
        exp = random.choice(EXP)
        sal = salary_for(exp, 7000, 2000) * (1 + 0.0001 * (dt - start).days)
        rows.append({
            "date":               dt.strftime("%Y-%m-%d"),
            "industry":           "Logistics",
            "job_title":          random.choice(titles),
            "region":             random.choice(REGIONS_VN),
            "job_openings":       max(5, int(rng.poisson(90) + (dt-start).days * 0.06)),
            "avg_salary":         round(sal, 2),
            "salary_growth_rate": round(rng.uniform(2, 10), 2),
            "experience_level":   exp,
            "remote_ratio":       random.randint(0, 30),
            "required_skills":    ", ".join(random.sample(skills_pool, random.randint(2, 5))),
            "competition_level":  random.choices(COMP, weights=[3, 4, 2])[0],
            "automation_risk":    random.choices(RISK, weights=[2, 4, 5])[0],
            "growth_score":       round(rng.uniform(35, 70), 1),
            "demand_forecast":    random.choices(DEMAND, weights=[4, 4, 2])[0],
        })
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    path = f"{OUT}/logistics_sector.csv"
    df.to_csv(path, index=False)
    print(f"✅ {path}  ({len(df)} rows)")
    return df

# ══════════════════════════════════════════════════════════════════════════════
# 5. RETAIL & E-COMMERCE
# ══════════════════════════════════════════════════════════════════════════════
def gen_retail(n=580):
    start = datetime(2022, 1, 1)
    titles = [
        "E-Commerce Manager", "Category Manager", "Merchandising Analyst",
        "Digital Marketing Specialist", "CRM Specialist", "UX Designer",
        "Data Analyst - Retail", "Store Operations Manager", "Growth Hacker",
        "Performance Marketing Manager", "Customer Success Manager",
    ]
    skills_pool = [
        "Shopify", "Google Analytics", "Facebook Ads", "SEO", "SEM", "CRM",
        "Python", "SQL", "Tableau", "Excel", "A/B Testing", "Email Marketing",
        "Supply Chain", "Inventory Management", "Customer Journey",
    ]
    rows = []
    for i in range(n):
        dt  = start + timedelta(days=random.randint(0, 900))
        exp = random.choice(EXP)
        sal = salary_for(exp, 8000, 2500) * (1 + 0.00012 * (dt - start).days)
        rows.append({
            "date":               dt.strftime("%Y-%m-%d"),
            "industry":           "Retail & E-Commerce",
            "job_title":          random.choice(titles),
            "region":             random.choice(REGIONS_VN),
            "job_openings":       max(5, int(rng.poisson(100) + (dt-start).days * 0.07)),
            "avg_salary":         round(sal, 2),
            "salary_growth_rate": round(rng.uniform(3, 13), 2),
            "experience_level":   exp,
            "remote_ratio":       random.randint(20, 70),
            "required_skills":    ", ".join(random.sample(skills_pool, random.randint(2, 6))),
            "competition_level":  random.choices(COMP, weights=[2, 4, 4])[0],
            "automation_risk":    random.choices(RISK, weights=[2, 4, 4])[0],
            "growth_score":       round(rng.uniform(40, 80), 1),
            "demand_forecast":    random.choices(DEMAND, weights=[5, 3, 2])[0],
        })
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    path = f"{OUT}/retail_ecommerce_sector.csv"
    df.to_csv(path, index=False)
    print(f"✅ {path}  ({len(df)} rows)")
    return df

# ══════════════════════════════════════════════════════════════════════════════
# 6. EDUCATION & EDTECH
# ══════════════════════════════════════════════════════════════════════════════
def gen_education(n=450):
    start = datetime(2021, 9, 1)
    titles = [
        "EdTech Developer", "Curriculum Designer", "Online Course Instructor",
        "Learning Experience Designer", "Education Data Analyst", "School Principal",
        "Corporate Trainer", "STEM Teacher", "E-Learning Developer",
        "Academic Researcher", "Student Success Manager",
    ]
    skills_pool = [
        "Instructional Design", "LMS Administration", "Articulate 360", "Python",
        "Data Analysis", "SCORM", "Video Production", "STEM Teaching", "Research",
        "Curriculum Development", "Learning Analytics", "Gamification", "AI Tools",
    ]
    rows = []
    for i in range(n):
        dt  = start + timedelta(days=random.randint(0, 1000))
        exp = random.choice(EXP)
        sal = salary_for(exp, 6000, 1800) * (1 + 0.00008 * (dt - start).days)
        rows.append({
            "date":               dt.strftime("%Y-%m-%d"),
            "industry":           "Education",
            "job_title":          random.choice(titles),
            "region":             random.choice(REGIONS_VN),
            "job_openings":       max(5, int(rng.poisson(60) + (dt-start).days * 0.03)),
            "avg_salary":         round(sal, 2),
            "salary_growth_rate": round(rng.uniform(2, 9), 2),
            "experience_level":   exp,
            "remote_ratio":       random.randint(30, 90),
            "required_skills":    ", ".join(random.sample(skills_pool, random.randint(2, 5))),
            "competition_level":  random.choices(COMP, weights=[4, 4, 2])[0],
            "automation_risk":    random.choices(RISK, weights=[3, 4, 3])[0],
            "growth_score":       round(rng.uniform(30, 75), 1),
            "demand_forecast":    random.choices(DEMAND, weights=[4, 4, 2])[0],
        })
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    path = f"{OUT}/education_sector.csv"
    df.to_csv(path, index=False)
    print(f"✅ {path}  ({len(df)} rows)")
    return df

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("🔨 Generating industry sample datasets...\n")
    dfs = {
        "technology":  gen_technology(),
        "healthcare":  gen_healthcare(),
        "finance":     gen_finance(),
        "logistics":   gen_logistics(),
        "retail":      gen_retail(),
        "education":   gen_education(),
    }

    # Also generate a combined multi-industry file
    combined = pd.concat(list(dfs.values()), ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)
    combined_path = f"{OUT}/combined_all_sectors.csv"
    combined.to_csv(combined_path, index=False)
    print(f"\n✅ {combined_path}  ({len(combined)} rows — tất cả ngành)")

    print("\n📊 Tóm tắt:")
    print(f"{'Ngành':<30} {'Rows':>6}  {'Avg Salary':>12}  {'Avg Growth':>12}")
    print("─" * 65)
    for name, df in dfs.items():
        print(f"{name:<30} {len(df):>6}  ${df['avg_salary'].mean():>10,.0f}  {df['growth_score'].mean():>10.1f}/100")
    print(f"\n✅ Tổng cộng: {sum(len(d) for d in dfs.values())} rows + {len(combined)} combined")
    print(f"📁 Tất cả file đã lưu vào thư mục: ./{OUT}/")
