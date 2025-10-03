#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_arch_diagrams.py — generates 4 diagrams (PNG 4K + PDF) using local logos from ./assets
"""
import os
from datetime import datetime
try:
    from zoneinfo import ZoneInfo  # Py3.9+
except Exception:
    ZoneInfo = None

def resolve_build_date():
    env = os.getenv("BUILD_DATE")
    if env:
        return env
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("Europe/Belgrade")).strftime("%Y-%m-%d %H:%M %Z")
    return datetime.now().strftime("%Y-%m-%d %H:%M")

BUILD_DATE = resolve_build_date()

from pathlib import Path
import matplotlib.pyplot as plt
from diagram_lib import (FIG_W, FIG_H, DPI, init_axes, draw_card, place_logo_fit, arrow)

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

TITLE = "Macro Insights — Modern Data Platform for Economic Analytics (2010–2025)"
SUBTITLE = "MVP project built with S3, ClickHouse, dbt, GitHub Actions & Grafana"
SIGN = "Eduard Nikolaev — Data Platform Architect"
YEAR = "2025"

LOGO = {
    "s3": ASSETS / "s3.jpeg",
    "clickhouse": ASSETS / "clickhouse.jpeg",
    "dbt": ASSETS / "dbt.jpeg",
    "github": ASSETS / "github.jpeg",
    "grafana": ASSETS / "grafana.jpeg",
    "metabase": ASSETS / "metabase.jpeg",
    "fastapi": ASSETS / "fastapi.jpeg",
    "nextjs": ASSETS / "nextjs.jpeg",
}

def footer_build_date(ax):
    # правый нижний угол
    ax.text(98, 3.5, f"Build: {BUILD_DATE}", fontsize=12, color="#666", ha="right")

def title_block(ax, subtitle=True):
    ax.text(2, 97, TITLE, fontsize=30, fontweight="bold", color="#111")
    if subtitle:
        ax.text(2, 94.5, SUBTITLE, fontsize=18, color="#333")
    ax.text(2, 92.2, SIGN, fontsize=16, color="#444")
    ax.text(98, 92.2, YEAR, fontsize=16, color="#444", ha="right")

def save(fig, name):
    png = OUT / f"{name}.png"
    pdf = OUT / f"{name}.pdf"
    fig.savefig(png, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)

def presentation_full_stack():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = init_axes(fig)
    title_block(ax, subtitle=True)

    COL = {"s3": "#1f77b4", "ch": "#d4aa00", "dbt": "#ff6a3d", "bi": "#ff7700", "api": "#10b981", "gray": "#333333"}

    # Row 1
    draw_card(ax, 3, 77, 44, 12, "Data Sources",
              ["World Bank, IMF, OECD", "CSV / JSON"],
              face="#f6faff", border="#4a7ab7")
    draw_card(ax, 53, 77, 44, 12, "AWS S3 (raw)",
              ["Prefixes: raw/worldbank/gdp/…", "CSV/Parquet • Versioning/Lifecycle"],
              face="#eef6ff", border=COL["s3"])
    place_logo_fit(ax, LOGO["s3"], cx=93.5, cy=84.2, target_h=3.0, max_w=3.0)

    arrow(ax, 47, 83, 53, 83, "Ingest / Upload")

    # Row 2
    draw_card(ax, 3, 58, 44, 14, "ClickHouse Cloud",
              ["Schemas: dbt_demo_dev, dbt_demo_prod",
               "Layers: staging (stg_*), marts",
               "Reads raw via s3()"],
              face="#fffbe6", border=COL["ch"])
    place_logo_fit(ax, LOGO["clickhouse"], cx=42.0, cy=68.0, target_h=3.0, max_w=3.2)

    draw_card(ax, 53, 58, 44, 14, "dbt (local + CI)",
              ["Adapter: dbt-clickhouse", "Targets: dev / prod", "Tests & Docs"],
              face="#fff2ec", border=COL["dbt"])
    place_logo_fit(ax, LOGO["dbt"], cx=93.5, cy=68.0, target_h=3.0, max_w=3.0)

    arrow(ax, 25, 58, 25, 53, "SELECT from s3()")
    arrow(ax, 47, 65, 53, 65, "dbt run")
    arrow(ax, 53, 61, 47, 61, "materialize")

    # Row 3
    draw_card(ax, 3, 39, 44, 14, "BI: Grafana / Metabase",
              ["Dashboards: GDP Growth, CAGR, Recovery",
               "Direct connection to ClickHouse"],
              face="#fff9f2", border=COL["bi"])
    place_logo_fit(ax, LOGO["grafana"], cx=42.0, cy=48.5, target_h=3.0, max_w=3.0)
    place_logo_fit(ax, LOGO["metabase"], cx=37.0, cy=48.5, target_h=3.0, max_w=2.7)

    draw_card(ax, 53, 39, 44, 14, "API + Front",
              ["FastAPI: /api/gdp, /api/cagr",
               "Next.js (Vercel): UI, auth, billing"],
              face="#f2fff8", border=COL["api"])
    place_logo_fit(ax, LOGO["fastapi"], cx=93.5, cy=48.5, target_h=3.0, max_w=3.0)
    place_logo_fit(ax, LOGO["nextjs"], cx=88.8, cy=48.5, target_h=3.0, max_w=2.6)

    arrow(ax, 25, 53, 25, 47, "SQL")
    arrow(ax, 29, 53, 55, 47, "REST/GraphQL")

    # Row 4
    draw_card(ax, 3, 22, 44, 12, "GitHub (Repo)",
              ["dbt SQL & tests", "Issues • PR • Code Review"],
              face="#f6f6f6", border=COL["gray"])
    place_logo_fit(ax, LOGO["github"], cx=42.0, cy=28.0, target_h=3.6, max_w=3.6)

    draw_card(ax, 53, 22, 44, 12, "GitHub Actions (CI/CD)",
              ["PR → dev: dbt build", "main → prod: manual deploy", "Secrets: CH_*, AWS_*"],
              face="#f6f6f6", border=COL["gray"])
    place_logo_fit(ax, LOGO["github"], cx=93.5, cy=28.0, target_h=3.6, max_w=3.6)

    arrow(ax, 25, 22, 25, 18, "push")
    arrow(ax, 25, 18, 56, 18, "trigger")
    arrow(ax, 56, 18, 56, 22, "")

    footer_build_date(ax)
    save(fig, "presentation_full_stack")

def presentation_data_flow():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = init_axes(fig)
    ax.text(2, 97, TITLE, fontsize=30, fontweight="bold", color="#111")
    ax.text(2, 94.5, SUBTITLE, fontsize=18, color="#333")
    ax.text(2, 92.2, SIGN, fontsize=16, color="#444")
    ax.text(98, 92.2, YEAR, fontsize=16, color="#444", ha="right")

    # --- верхний ряд ---
    draw_card(ax, 4, 65, 20, 14, "1) Sources",
              ["World Bank • IMF • OECD", "CSV / JSON"],
              face="#f6faff", border="#4a7ab7")

    draw_card(ax, 28, 65, 20, 14, "2) AWS S3 (raw)",
              ["Parquet / CSV", "Versioned prefixes"],
              face="#eef6ff", border="#1f77b4")
    # было cy=73.0 → опускаем до 71.6; плюс шире (0.9)
    place_logo_fit(ax, LOGO["s3"], cx=46.0, cy=71.6, target_h=3.0, max_w=3.0, width_squeeze=0.9)

    draw_card(ax, 52, 65, 20, 14, "3) ClickHouse (staging)",
              ["stg_* tables", "Reads via s3()"],
              face="#fffbe6", border="#d4aa00")
    # было cy=73.0 → 71.6
    place_logo_fit(ax, LOGO["clickhouse"], cx=70.0, cy=71.6, target_h=3.0, max_w=3.0, width_squeeze=0.9)

    draw_card(ax, 76, 65, 20, 14, "4) dbt (transform)",
              ["marts: GDP growth, CAGR", "tests & docs"],
              face="#fff2ec", border="#ff6a3d")
    # было cy=73.0 → 71.6
    place_logo_fit(ax, LOGO["dbt"], cx=94.0, cy=71.6, target_h=3.0, max_w=3.0, width_squeeze=0.9)

    arrow(ax, 24, 72, 28, 72, "ingest")
    arrow(ax, 48, 72, 52, 72, "s3()")
    arrow(ax, 72, 72, 76, 72, "dbt run")

    # --- нижний ряд ---
    draw_card(ax, 28, 36, 20, 14, "5) ClickHouse (marts)",
              ["gdp_growth_by_country", "cagr_10y, recovery"],
              face="#fffbe6", border="#d4aa00")
    # было cy=44.0 → 42.7
    place_logo_fit(ax, LOGO["clickhouse"], cx=46.0, cy=42.7, target_h=3.0, max_w=3.0, width_squeeze=0.9)

    draw_card(ax, 57, 36, 24, 14, "6) Delivery",
              ["BI: Grafana / Metabase", "API: FastAPI • Front: Next.js"],
              face="#f9fff4", border="#66bb6a")
    # было cy=44.0 → 42.6; все чуть ниже и чуть шире
    place_logo_fit(ax, LOGO["grafana"],  cx=73.0, cy=42.6, target_h=2.8, max_w=2.8, width_squeeze=0.9)
    place_logo_fit(ax, LOGO["metabase"], cx=69.0, cy=42.6, target_h=2.6, max_w=2.6, width_squeeze=0.9)
    place_logo_fit(ax, LOGO["fastapi"],  cx=65.0, cy=42.6, target_h=2.6, max_w=2.6, width_squeeze=0.9)
    place_logo_fit(ax, LOGO["nextjs"],   cx=61.0, cy=42.6, target_h=2.6, max_w=2.6, width_squeeze=0.9)

    arrow(ax, 38, 50, 58, 50, "SELECT / REST")

    ax.text(2, 6, SIGN, fontsize=16, color="#444")
    ax.text(98, 6, YEAR, fontsize=16, color="#444", ha="right")

    footer_build_date(ax)
    save(fig, "presentation_data_flow")

def technical_arch_environments():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = init_axes(fig)
    ax.text(2, 97, "Macro Insights — Architecture & Environments (Technical)",
            fontsize=30, fontweight="bold", color="#111")
    ax.text(2, 94.5, "Monochrome logos, dev/prod targets, schemas",
            fontsize=18, color="#333")
    ax.text(2, 92.2, SIGN, fontsize=16, color="#444")
    ax.text(98, 92.2, YEAR, fontsize=16, color="#444", ha="right")

    gray = "#f2f2f2"
    draw_card(ax, 3, 77, 44, 12, "Compute: ClickHouse Cloud",
              ["Schemas: dbt_demo_dev, dbt_demo_prod", "TLS 8443"],
              face=gray, border="#222")
    place_logo_fit(ax, LOGO["clickhouse"], cx=42.0, cy=84.0, target_h=2.8, max_w=3.0)

    draw_card(ax, 53, 77, 44, 12, "Transform: dbt",
              ["Tags: stg/mart • Tests/Docs"],
              face=gray, border="#222")
    place_logo_fit(ax, LOGO["dbt"], cx=93.5, cy=83.8, target_h=2.8, max_w=3.0)

    draw_card(ax, 3, 58, 44, 14, "Storage: AWS S3 (raw)",
              ["raw/worldbank/gdp/... • IAM access"],
              face=gray, border="#222")
    place_logo_fit(ax, LOGO["s3"], cx=42.0, cy=66.8, target_h=2.8, max_w=3.0)

    draw_card(ax, 53, 58, 44, 14, "Access: BI / API",
              ["Grafana, Metabase, FastAPI, Next.js"],
              face=gray, border="#222")
    for key, cx in [("grafana", 88.0), ("metabase", 92.0), ("fastapi", 96.0), ("nextjs", 84.0)]:
        place_logo_fit(ax, LOGO[key], cx=cx, cy=66.8, target_h=2.4, max_w=2.6)

    draw_card(ax, 3, 39, 44, 14, "Repo", ["GitHub"], face=gray, border="#222")
    place_logo_fit(ax, LOGO["github"], cx=42.0, cy=47.0, target_h=3.0, max_w=3.0)

    draw_card(ax, 53, 39, 44, 14, "CI/CD",
              ["GitHub Actions • Secrets: CH_*, AWS_*"],
              face=gray, border="#222")
    place_logo_fit(ax, LOGO["github"], cx=93.5, cy=47.0, target_h=3.0, max_w=3.0)

    footer_build_date(ax)
    save(fig, "technical_arch_environments")

def technical_cicd_reference():
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax = init_axes(fig)
    ax.text(2, 97, "Macro Insights — CI/CD Variables & Profiles (Technical)",
            fontsize=30, fontweight="bold", color="#111")
    ax.text(2, 94.5, "GitHub Actions • dbt profiles • secrets",
            fontsize=18, color="#333")
    ax.text(2, 92.2, SIGN, fontsize=16, color="#444")
    ax.text(98, 92.2, YEAR, fontsize=16, color="#444", ha="right")

    gray = "#f2f2f2"
    draw_card(ax, 3, 68, 94, 12, "Repository & CI/CD",
              ["GitHub repo: macro-insights • Workflows: dbt.yml",
               "Secrets: CH_HOST_*, CH_USER_*, CH_PASS_*, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY"],
              face=gray, border="#222")
    draw_card(ax, 3, 50, 94, 14, "dbt profiles.yml (targets)",
              ["dev: schema=dbt_demo_dev • prod: schema=dbt_demo_prod",
               "host=$CH_HOST_* • user=$CH_USER_* • password=$CH_PASS_* • secure=true"],
              face=gray, border="#222")
    draw_card(ax, 3, 30, 94, 14, "S3 Prefix Convention",
              ["s3://macro-insights/raw/worldbank/gdp/country=<ISO2>/year=<YYYY>/part-*.{csv|parquet}"],
              face=gray, border="#222")
    draw_card(ax, 3, 12, 94, 14, "Delivery",
              ["BI: Grafana, Metabase • API: FastAPI • Front: Next.js"],
              face=gray, border="#222")

    for key, (cx, cy, th, mw) in {
        "github": (93.0, 73.5, 2.6, 2.6),
        "dbt": (93.0, 55.5, 2.6, 2.6),
        "s3": (93.0, 35.5, 2.6, 2.6),
        "grafana": (70.0, 15.5, 2.2, 2.2),
        "metabase": (74.0, 15.5, 2.0, 2.0),
        "fastapi": (78.0, 15.5, 2.0, 2.0),
        "nextjs": (82.0, 15.5, 2.0, 2.0),
    }.items():
        place_logo_fit(ax, LOGO[key], cx=cx, cy=cy, target_h=th, max_w=mw)

    footer_build_date(ax)
    save(fig, "technical_cicd_reference")

def main():
    presentation_full_stack()
    presentation_data_flow()
    technical_arch_environments()
    technical_cicd_reference()
    print("[✓] Diagrams saved to ./out")

if __name__ == "__main__":
    main()
