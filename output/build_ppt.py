#!/usr/bin/env python3
"""Build premium PDCA presentation for elderly health management project."""

import os
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ASSETS = Path(__file__).parent / "assets"
OUT = Path(__file__).parent / "PDCA提高老年人健康管理率.pptx"

# Brand palette
NAVY = RGBColor(0x0D, 0x2B, 0x45)
TEAL = RGBColor(0x1A, 0x7A, 0x8C)
GOLD = RGBColor(0xC9, 0xA2, 0x27)
LIGHT = RGBColor(0xF0, 0xF4, 0xF8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK = RGBColor(0x2C, 0x3E, 0x50)
SOFT_TEAL = RGBColor(0xE8, 0xF4, 0xF6)


def make_trend_chart():
    months = ["3月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    rates = [7.38, 13.5, 18.28, 25.08, 28.30, 33.65, 47.3, 58.8, 65.50]
    target = 64

    plt.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "Noto Sans CJK SC", "SimHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(12, 6), facecolor="#F5F8FA")
    ax.set_facecolor("#F5F8FA")

    ax.fill_between(range(len(months)), rates, alpha=0.15, color="#1A7A8C")
    ax.plot(months, rates, "o-", color="#0D2B45", linewidth=3, markersize=10,
            markerfacecolor="#C9A227", markeredgecolor="#0D2B45", markeredgewidth=2, zorder=5)
    ax.axhline(y=target, color="#C9A227", linestyle="--", linewidth=2.5, label=f"目标线 {target}%", zorder=3)

    for i, (m, r) in enumerate(zip(months, rates)):
        offset = 12 if i % 2 == 0 else -18
        ax.annotate(f"{r}%", (m, r), textcoords="offset points", xytext=(0, offset),
                    ha="center", fontsize=11, fontweight="bold", color="#0D2B45")

    ax.set_ylabel("老年人健康管理率 (%)", fontsize=13, color="#0D2B45", fontweight="bold")
    ax.set_xlabel("时间", fontsize=12, color="#0D2B45")
    ax.set_title("改进后老年人健康管理率趋势图", fontsize=16, color="#0D2B45", fontweight="bold", pad=16)
    ax.set_ylim(0, 80)
    ax.grid(True, alpha=0.3, linestyle="-")
    ax.legend(loc="lower right", fontsize=11, framealpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    path = ASSETS / "trend-chart.png"
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="#F5F8FA")
    plt.close()
    return path


def set_slide_bg(slide, color=LIGHT):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_top_bar(slide, title, subtitle=None):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.15))
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()

    accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.15), Inches(13.333), Inches(0.06))
    accent.fill.solid()
    accent.fill.fore_color.rgb = GOLD
    accent.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.55), Inches(0.22), Inches(10), Inches(0.7))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = WHITE

    if subtitle:
        sb = slide.shapes.add_textbox(Inches(0.55), Inches(0.72), Inches(10), Inches(0.4))
        sp = sb.text_frame.paragraphs[0]
        sp.text = subtitle
        sp.font.size = Pt(14)
        sp.font.color.rgb = GOLD


def add_card(slide, left, top, width, height, title, lines, accent=TEAL):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = RGBColor(0xDD, 0xE4, 0xEA)
    card.line.width = Pt(1)

    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.08), height)
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = accent
    stripe.line.fill.background()

    tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.12), width - Inches(0.35), height - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY
    for line in lines:
        p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(12)
        p.font.color.rgb = DARK
        p.space_before = Pt(6)


def add_bullet_box(slide, left, top, width, height, items, title=None):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = RGBColor(0xDD, 0xE4, 0xEA)

    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    if title:
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = TEAL
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 and not title else tf.add_paragraph()
        if i == 0 and not title:
            pass
        p.text = f"● {item}"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK
        p.space_before = Pt(8)
        p.level = 0


def add_notes(slide, text):
    notes = slide.notes_slide
    notes.notes_text_frame.text = text


def slide_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(str(ASSETS / "cover-bg.png"), 0, 0, width=prs.slide_width, height=prs.slide_height)

    dark = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(2.2), prs.slide_width, Inches(5.0))
    dark.fill.solid()
    dark.fill.fore_color.rgb = NAVY
    dark.line.fill.background()

    gold_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(3.5), Inches(1.5), Inches(0.06))
    gold_line.fill.solid()
    gold_line.fill.fore_color.rgb = GOLD
    gold_line.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(11), Inches(1.2))
    p = tb.text_frame.paragraphs[0]
    p.text = "广西骨伤医院 · 2025年提升医疗质量与服务能力"
    p.font.size = Pt(18)
    p.font.color.rgb = GOLD

    tb2 = slide.shapes.add_textbox(Inches(1.2), Inches(3.7), Inches(11), Inches(1.5))
    p2 = tb2.text_frame.paragraphs[0]
    p2.text = "PDCA提高老年人健康管理率"
    p2.font.size = Pt(44)
    p2.font.bold = True
    p2.font.color.rgb = WHITE

    tb3 = slide.shapes.add_textbox(Inches(1.2), Inches(5.3), Inches(11), Inches(1.5))
    tf = tb3.text_frame
    for i, line in enumerate([
        "汇报单位：长虹社区卫生服务中心",
        "项目负责人：姜雪冰  副主任医师",
        "汇报日期：2025年3月",
    ]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(16)
        p.font.color.rgb = RGBColor(0xCC, 0xDD, 0xEE)
        p.space_before = Pt(6)

    add_notes(slide, "各位评委、各位同仁，大家好！我是长虹社区卫生服务中心姜雪冰，今天汇报的项目是《PDCA提高老年人健康管理率》。")


def slide_agenda(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_top_bar(slide, "汇报提纲", "CONTENTS")

    items = [
        ("01", "项目背景", "政策依据 · 问题现状"),
        ("02", "指标与目标", "监测指标 · 改进目标"),
        ("03", "原因分析", "鱼骨图 · 柏拉图验证"),
        ("04", "PDCA循环", "计划 · 执行 · 检查 · 处理"),
        ("05", "成效总结", "数据成果 · 持续改进"),
    ]
    for i, (num, title, sub) in enumerate(items):
        col = i % 3
        row = i // 3
        left = Inches(0.6 + col * 4.1)
        top = Inches(1.6 + row * 2.6)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.8), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE if i % 2 == 0 else SOFT_TEAL
        card.line.color.rgb = TEAL

        nb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(1), Inches(0.6))
        np = nb.text_frame.paragraphs[0]
        np.text = num
        np.font.size = Pt(28)
        np.font.bold = True
        np.font.color.rgb = GOLD

        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.85), Inches(3.3), Inches(1.2))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEAL

    add_notes(slide, "本次汇报分为五个部分：项目背景、指标目标、原因分析、PDCA循环改进过程、以及成效总结。")


def slide_team(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_top_bar(slide, "项目团队", "PROJECT TEAM")

    members = [
        ("姜雪冰", "48岁", "副主任医师", "项目负责人"),
        ("黄文乐", "33岁", "主管护师", "公卫培训"),
        ("李俊洁", "39岁", "副主任护师", "健康管理"),
        ("莫威浪", "35岁", "主治医师", "全科诊疗"),
        ("甘艳凤", "38岁", "主管护师", "家医签约"),
        ("唐诗", "27岁", "护师", "健康宣教"),
        ("罗文清", "27岁", "护士", "上门服务"),
    ]

    # header row
    headers = ["姓名", "年龄", "职称", "分工"]
    for j, h in enumerate(headers):
        cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6 + j * 3.05), Inches(1.45), Inches(2.95), Inches(0.45))
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.line.fill.background()
        tb = slide.shapes.add_textbox(Inches(0.7 + j * 3.05), Inches(1.52), Inches(2.8), Inches(0.35))
        p = tb.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    for i, row in enumerate(members):
        bg = WHITE if i % 2 == 0 else SOFT_TEAL
        for j, val in enumerate(row):
            cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6 + j * 3.05), Inches(1.9 + i * 0.52), Inches(2.95), Inches(0.48))
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.line.color.rgb = RGBColor(0xDD, 0xE4, 0xEA)
            tb = slide.shapes.add_textbox(Inches(0.7 + j * 3.05), Inches(1.97 + i * 0.52), Inches(2.8), Inches(0.35))
            p = tb.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(12)
            p.font.color.rgb = DARK if j == 0 else RGBColor(0x55, 0x66, 0x77)
            p.font.bold = (j == 0)
            p.alignment = PP_ALIGN.CENTER

    info = slide.shapes.add_textbox(Inches(0.6), Inches(5.6), Inches(12), Inches(0.8))
    p = info.text_frame.paragraphs[0]
    p.text = "项目启动日期：2025年3月  |  多学科协作 · 医护公卫联动 · 全科思维贯穿全程"
    p.font.size = Pt(13)
    p.font.color.rgb = TEAL
    p.font.bold = True

    add_notes(slide, "项目团队由7名成员组成，涵盖副主任医师、主治医师、护师等多岗位，实现医护公卫协同。")


def slide_background(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_top_bar(slide, "选题背景", "BACKGROUND")

    add_card(slide, Inches(0.5), Inches(1.4), Inches(6.1), Inches(2.5), "政策依据",
             ['《"健康中国2030"规划纲要》', "《国家基本公共卫生服务规范》",
              "2024年青秀区基层卫生医疗机构公卫服务任务要求"],
             TEAL)
    add_card(slide, Inches(6.8), Inches(1.4), Inches(6.1), Inches(2.5), "辖区基本情况",
             ["管辖人口：31,012人次", "年度任务指标：约2,128人（65岁及以上）",
              "考核要求：老年人城乡社区规范健康管理服务率≥64%"],
             GOLD)

    add_card(slide, Inches(0.5), Inches(4.1), Inches(12.4), Inches(2.3), "选题理由",
             ["经对长虹社区老年人健康管理情况分析，若不完成相关指标，公卫年度考核将不通过，",
              "直接影响年度服务人口划分及服务内容落实。",
              "本项目以PDCA循环为工具，系统提升老年人健康管理率，保障公卫服务质量。"],
             NAVY)

    add_notes(slide, "选题依据国家健康中国与基本公共卫生服务规范，结合辖区实际人口任务和考核压力。")


def slide_problem(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_top_bar(slide, "问题陈述", "PROBLEM STATEMENT")

    stats = [
        ("2024年", "1,246", "2,128", "58.6%", "未达标"),
        ("2025年1-3月", "318", "2,128", "7.38%", "严重偏低"),
    ]
    labels = ["时间段", "完成体检人数", "任务目标", "健康管理率", "状态"]
    for j, lb in enumerate(labels):
        c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5 + j * 2.5), Inches(1.5), Inches(2.4), Inches(0.5))
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY
        c.line.fill.background()
        tb = slide.shapes.add_textbox(Inches(0.55 + j * 2.5), Inches(1.57), Inches(2.3), Inches(0.4))
        p = tb.text_frame.paragraphs[0]
        p.text = lb
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    for i, row in enumerate(stats):
        for j, val in enumerate(row):
            bg = SOFT_TEAL if i == 0 else RGBColor(0xFD, 0xE8, 0xE8)
            c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5 + j * 2.5), Inches(2.05 + i * 0.55), Inches(2.4), Inches(0.5))
            c.fill.solid()
            c.fill.fore_color.rgb = bg
            c.line.color.rgb = RGBColor(0xDD, 0xE4, 0xEA)
            tb = slide.shapes.add_textbox(Inches(0.55 + j * 2.5), Inches(2.12 + i * 0.55), Inches(2.3), Inches(0.4))
            p = tb.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(13)
            p.font.bold = (j == 3)
            p.font.color.rgb = RGBColor(0xC0, 0x39, 0x2B) if j == 4 else DARK
            p.alignment = PP_ALIGN.CENTER

    add_bullet_box(slide, Inches(0.5), Inches(3.4), Inches(12.4), Inches(2.8), [
        "2024年7月划分人口后至年底，65岁及以上老年人体检仅完成1,246人次，距2,128人目标差距明显",
        "2025年一季度健康管理率仅7.38%，远低于64%的考核要求",
        "若不干预，将影响公卫年度考核通过及服务人口划分",
        "亟需运用质量管理工具，查找真因、制定对策、系统改进",
    ], "核心问题")

    add_notes(slide, "用数据说话：2024年未达标，2025年初仅7.38%，问题紧迫。")


def slide_indicator(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_top_bar(slide, "监测指标与改进目标", "INDICATORS & GOALS")

    # formula box
    formula = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.4), Inches(12.4), Inches(1.1))
    formula.fill.solid()
    formula.fill.fore_color.rgb = NAVY
    formula.line.fill.background()
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(1.55), Inches(12), Inches(0.8))
    p = tb.text_frame.paragraphs[0]
    p.text = "老年人健康管理率 ＝  年内接受健康管理人数  ÷  年内辖区65岁及以上常住居民数  ×  100%"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    add_card(slide, Inches(0.5), Inches(2.7), Inches(6.1), Inches(2.2), "指标定义",
             ["接受健康管理须同时满足：", "① 建立健康档案", "② 接受健康体检",
              "③ 获得健康指导", "④ 健康体检表填写完整"],
             TEAL)
    add_card(slide, Inches(6.8), Inches(2.7), Inches(6.1), Inches(2.2), "改进目标",
             ["南宁市考核目标：≥64%", "项目预期目标：年终完成2,128人次",
              "项目启动时现状：7.38%（2025年1-3月）",
              "改进后达成：65%（12月达65.50%）"],
             GOLD)

    add_card(slide, Inches(0.5), Inches(5.1), Inches(12.4), Inches(1.5), "预期延伸效益",
             ["通过定期体检、健康评估和个性化指导，早期发现高血压、糖尿病、心血管疾病等慢性病，",
              "及时干预治疗，降低致残率和病死率，延长老年人健康寿命。"],
             NAVY)

    add_notes(slide, "明确指标公式、定义、目标值和预期社会效益。")


def slide_fishbone(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_top_bar(slide, "原因分析 — 鱼骨图", "CAUSE ANALYSIS · ISHIKAWA")

    slide.shapes.add_picture(str(ASSETS / "fishbone-diagram.png"), Inches(0.3), Inches(1.35), width=Inches(12.7))

    add_notes(slide, "运用鱼骨图从人、机、料、法、环等维度分析，归纳三大主因：健康宣教不足、全科思维不足、家医服务包未完成。")


def slide_pareto(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_top_bar(slide, "真因验证 — 柏拉图", "ROOT CAUSE · PARETO")

    slide.shapes.add_picture(str(ASSETS / "pareto-chart.png"), Inches(0.5), Inches(1.35), width=Inches(7.5))

    add_bullet_box(slide, Inches(8.2), Inches(1.5), Inches(4.7), Inches(4.5), [
        "健康宣教不足（45%）— 首要真因",
        "全科思维模式不足（35%）",
        "家庭医师服务包未完成（20%）",
        "前三项累计占比80%，符合帕累托法则",
        "对策应优先针对前三项真因制定",
    ], "真因排序结论")

    add_notes(slide, "柏拉图验证：前三项原因累计占80%，为对策拟定的重点方向。")


def slide_plan(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_top_bar(slide, "对策拟定（Plan）", "PDCA · PLAN")

    rows = [
        ["健康宣教不足", "加强健康宣教", "每月外出2次义诊及人员培训", "2025.3.26-6.20", "辖区及中心"],
        ["全科思维模式不足", "外派人员学习及培训", "每季度一次", "2025.6.21-7.12", "中心"],
        ["家医服务包未完成", "逐步落实服务包应用", "长期推进", "2025.8.13-10.5", "中心"],
    ]
    headers = ["真因", "对策", "实施方式", "时间", "地点"]
    widths = [2.2, 2.2, 2.8, 2.0, 1.8]
    left_start = 0.45
    for j, (h, w) in enumerate(zip(headers, widths)):
        l = Inches(left_start + sum(widths[:j]))
        c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, Inches(1.45), Inches(w), Inches(0.48))
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY
        c.line.fill.background()
        tb = slide.shapes.add_textbox(l + Inches(0.05), Inches(1.52), Inches(w - 0.1), Inches(0.35))
        p = tb.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    for i, row in enumerate(rows):
        bg = WHITE if i % 2 == 0 else SOFT_TEAL
        for j, (val, w) in enumerate(zip(row, widths)):
            l = Inches(left_start + sum(widths[:j]))
            c = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, Inches(1.93 + i * 0.72), Inches(w), Inches(0.65))
            c.fill.solid()
            c.fill.fore_color.rgb = bg
            c.line.color.rgb = RGBColor(0xDD, 0xE4, 0xEA)
            tb = slide.shapes.add_textbox(l + Inches(0.08), Inches(2.0 + i * 0.72), Inches(w - 0.15), Inches(0.55))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = DARK

    slide.shapes.add_picture(str(ASSETS / "pdca-cycle.png"), Inches(4.5), Inches(4.2), width=Inches(4.3))

    add_notes(slide, "针对三大真因，逐一拟定对策、明确时间地点和责任人。")


def slide_do(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_top_bar(slide, "对策实施（Do）", "PDCA · DO")

    actions = [
        ("01", "公卫规范培训", "加强公卫小组成员基本规范业务培训，统一服务标准与操作流程。"),
        ("02", "全科思维培训", "加强医师全科思维业务培训，开展全员医疗与卫生联动家庭医师签约模式培训。"),
        ("03", "义诊上门服务", "增加外出义诊及家医上门服务频次，将服务延伸至社区居民身边。"),
    ]
    for i, (num, title, desc) in enumerate(actions):
        top = Inches(1.5 + i * 1.75)
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.6), top, Inches(0.7), Inches(0.7))
        circle.fill.solid()
        circle.fill.fore_color.rgb = GOLD
        circle.line.fill.background()
        nb = slide.shapes.add_textbox(Inches(0.72), top + Inches(0.12), Inches(0.5), Inches(0.5))
        np = nb.text_frame.paragraphs[0]
        np.text = num
        np.font.size = Pt(16)
        np.font.bold = True
        np.font.color.rgb = WHITE

        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), top, Inches(11.3), Inches(1.5))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = TEAL
        tb = slide.shapes.add_textbox(Inches(1.7), top + Inches(0.15), Inches(10.9), Inches(1.2))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = DARK
        p2.space_before = Pt(8)

    add_notes(slide, "三项核心实施举措：培训、全科思维、义诊上门。")


def slide_study(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_top_bar(slide, "效果评价（Study）", "PDCA · STUDY")

    slide.shapes.add_picture(str(ASSETS / "trend-chart.png"), Inches(0.3), Inches(1.35), width=Inches(8.5))

    # KPI cards
    kpis = [("7.38%", "改进前\n(2025.3月)"), ("65%", "改进后\n(年终)"), ("+57.6%", "提升幅度"), ("64%", "考核目标")]
    for i, (val, label) in enumerate(kpis):
        left = Inches(8.9 + (i % 2) * 2.1)
        top = Inches(1.5 + (i // 2) * 2.0)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(1.95), Inches(1.7))
        card.fill.solid()
        card.fill.fore_color.rgb = NAVY if i == 1 else WHITE
        card.line.color.rgb = GOLD if i == 1 else TEAL

        vb = slide.shapes.add_textbox(left + Inches(0.1), top + Inches(0.25), Inches(1.75), Inches(0.7))
        vp = vb.text_frame.paragraphs[0]
        vp.text = val
        vp.font.size = Pt(22)
        vp.font.bold = True
        vp.font.color.rgb = GOLD if i == 1 else NAVY
        vp.alignment = PP_ALIGN.CENTER

        lb = slide.shapes.add_textbox(left + Inches(0.1), top + Inches(1.0), Inches(1.75), Inches(0.6))
        lp = lb.text_frame.paragraphs[0]
        lp.text = label
        lp.font.size = Pt(10)
        lp.font.color.rgb = WHITE if i == 1 else DARK
        lp.alignment = PP_ALIGN.CENTER

    add_bullet_box(slide, Inches(8.9), Inches(5.6), Inches(4.1), Inches(1.2), [
        "学习内容：质控工具运用、《国家基本公共卫生服务规范》",
    ])

    add_notes(slide, "数据证明改进有效：从7.38%提升至65%，超额完成64%目标。5-12月持续上升。")


def slide_action(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_top_bar(slide, "标准化巩固（Action）", "PDCA · ACTION")

    add_card(slide, Inches(0.5), Inches(1.4), Inches(6.1), Inches(2.0), "改进成效",
             ["本轮持续改进后，长虹社区老年人健康管理率较前明显提高",
              "12月健康管理率达65.50%，超额完成考核目标"],
             TEAL)

    add_card(slide, Inches(6.8), Inches(1.4), Inches(6.1), Inches(2.0), "仍存问题",
             ["宣教形式单一、专业术语多、未考虑老年人视听能力下降",
              "医护缺乏系统全科培训，病例讨论未形成制度",
              "任务分工不明、签约服务停留纸面、医生动力不足"],
             RGBColor(0xC0, 0x39, 0x2B))

    measures = [
        ("宣教创新", "药品说明书、膳食指南转化为实物模型（盐勺、油壶、食物模具）及大字图画版手册"),
        ("思维固化", "设计《全科接诊思维导图》台卡，放置诊室，兼顾生物-心理-社会模式"),
        ("激励机制", '确立"按劳分配"原则，明确完成完整服务包的绩效奖励标准'),
    ]
    for i, (title, desc) in enumerate(measures):
        left = Inches(0.5 + i * 4.15)
        add_card(slide, left, Inches(3.6), Inches(3.95), Inches(2.8), title, [desc], GOLD)

    add_notes(slide, "Action阶段：总结成效、分析问题、制定标准化巩固措施。")


def slide_summary(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide)
    add_top_bar(slide, "项目成效与推广价值", "ACHIEVEMENTS")

    items = [
        ("质量提升", "老年人健康管理率从7.38%提升至65%，超额完成64%考核目标"),
        ("方法科学", "熟练运用PDCA、鱼骨图、柏拉图等质量管理工具"),
        ("服务延伸", "义诊上门、家医签约、个性化健康指导全面落地"),
        ("持续改进", "建立宣教创新、全科思维、绩效激励长效机制"),
        ("社会效益", "早期发现慢性病，降低致残病死率，延长健康寿命"),
        ("可推广性", "模式可借鉴至其他社区卫生服务中心公卫项目"),
    ]
    for i, (title, desc) in enumerate(items):
        col = i % 3
        row = i // 3
        left = Inches(0.5 + col * 4.15)
        top = Inches(1.5 + row * 2.3)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.95), Inches(2.0))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = TEAL

        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.2), top + Inches(0.2), Inches(0.35), Inches(0.35))
        dot.fill.solid()
        dot.fill.fore_color.rgb = GOLD
        dot.line.fill.background()

        tb = slide.shapes.add_textbox(left + Inches(0.65), top + Inches(0.15), Inches(3.1), Inches(1.7))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = DARK
        p2.space_before = Pt(6)

    add_notes(slide, "从质量、方法、服务、机制、社会效益、推广性六个维度总结项目价值。")


def slide_thanks(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(str(ASSETS / "section-bg.png"), 0, 0, width=prs.slide_width, height=prs.slide_height)

    overlay = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    overlay.fill.solid()
    overlay.fill.fore_color.rgb = NAVY
    overlay.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(2), Inches(2.5), Inches(9.3), Inches(1.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "感谢聆听"
    p.font.size = Pt(52)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    tb2 = slide.shapes.add_textbox(Inches(2), Inches(4.0), Inches(9.3), Inches(1.5))
    tf = tb2.text_frame
    for i, line in enumerate([
        "长虹社区卫生服务中心",
        "汇报人：姜雪冰",
        "敬请各位评委批评指正！",
    ]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(18)
        p.font.color.rgb = GOLD
        p.alignment = PP_ALIGN.CENTER
        p.space_before = Pt(10)

    add_notes(slide, "感谢各位评委聆听，请批评指正！")


def main():
    make_trend_chart()

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    slide_cover(prs)
    slide_agenda(prs)
    slide_team(prs)
    slide_background(prs)
    slide_problem(prs)
    slide_indicator(prs)
    slide_fishbone(prs)
    slide_pareto(prs)
    slide_plan(prs)
    slide_do(prs)
    slide_study(prs)
    slide_action(prs)
    slide_summary(prs)
    slide_thanks(prs)

    prs.save(str(OUT))
    print(f"Saved: {OUT} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
