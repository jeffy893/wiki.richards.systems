#!/usr/bin/env python3
"""
Build script: Converts Confluence HTML export (RS/) into a beautiful wiki site.
Outputs to the root of wiki.richards.systems/ for GitHub Pages deployment.
"""

import os
import re
import html
from pathlib import Path
from urllib.parse import unquote

BASE_DIR = Path(__file__).parent
RS_DIR = BASE_DIR / 'RS'
PAGES_DIR = BASE_DIR / 'pages'
ASSETS_DIR = BASE_DIR / 'assets'

PAGES_DIR.mkdir(exist_ok=True)

# ============================================
# Navigation Tree Structure (from RS/index.html)
# ============================================

NAV_TREE = [
    {
        "title": "Richards Systems",
        "file": "Richards-Systems_16679146.html",
        "is_home": True,
        "children": [
            {"title": "2014 Cosmos Introduction", "file": "2014-Cosmos-Introduction_91488258.html"},
            {"title": "2014 Philosophy: Freedom to Model", "file": "96337921.html"},
            {"title": "2015 Philosophy of AI", "file": "2015-Philosophy-of-AI_247627792.html"},
            {
                "title": "2015-2025 Cortext.io",
                "file": "2015-2025-Cortext.io_193134629.html",
                "children": [
                    {"title": "Sponsor Jefferson to Keep Coding", "file": "Sponsor-Jefferson-to-Keep-Coding_17170460.html"},
                    {"title": "Intro: Project Overview", "file": "17399817.html"},
                    {"title": "Intro: BostonCC Video", "file": "17399899.html"},
                    {"title": "2016-11-28 Semantic Algebra", "file": "2016-11-28-Semantic-Algebra_17661953.html"},
                    {"title": "Inspired by the GDELT Project", "file": "Inspired-by-the-GDELT-Project_17072130.html"},
                    {"title": "2017-04-27 ISO 31000 News Service", "file": "2017-04-27-ISO-31000-News-Service_17661955.html"},
                    {"title": "2018-06-20 Cortext Nascent Aim", "file": "2018-06-20-Cortext-Nascent-Aim_17367066.html"},
                    {"title": "2018-10-08 Cortext Data Model", "file": "2018-10-08-Cortext-Data-Model_17203235.html"},
                    {"title": "2022-11-01 AWS Batch-Fargate Setup", "file": "2022-11-01-AWS-Batch-Fargate-Setup_17236017.html"},
                    {"title": "Microservices", "file": "Microservices_17498129.html"},
                    {"title": "Cortext.io Event Report", "file": "Cortext.io-Event-Report_17498151.html"},
                    {"title": "Cortext.io Elastic Stack", "file": "Cortext.io-Elastic-Stack_17367070.html"},
                    {"title": "Cortext.io Extension", "file": "Cortext.io-Extension_17235994.html"},
                    {"title": "2024-02-27 Serverless Arch ProcureCrawl", "file": "2024-02-27-Serverless-Arch-ProcureCrawl_17399881.html"},
                    {"title": "2024-08-13 Consolidation", "file": "2024-08-13-Consolidation_17301534.html"},
                    {"title": "2024-09-04 Cortext.io Conclusion", "file": "2024-09-04-Cortext.io-Conclusion_33128449.html"},
                    {"title": "2024-10-01 Reverse Conway on Richards Systems", "file": "2024-10-01-Reverse-Conway-on-Richards-Systems_39616513.html"},
                ]
            },
            {
                "title": "2019-2025 Responsibility Futures",
                "file": "2019-2025-Responsibility-Futures_192643159.html",
                "children": [
                    {
                        "title": "2019-2021 Responsibility Index",
                        "file": "2019-2021-Responsibility-Index_205717544.html",
                        "children": [
                            {"title": "2019-04-13 Constitution of MANGO", "file": "2019-04-13_Constitution_of_MANGO_94404609.html"},
                            {"title": "2019 Responsibility Futures", "file": "2019-Responsibility-Futures_247758851.html"},
                            {"title": "2019-05-29 Invasive Species", "file": "2019-05-29_Invasive-Species_90505220.html"},
                            {"title": "2021-03-12 Intention Div Negligence", "file": "2021-03-12_Intention_Div_Negligence_96206849.html"},
                            {"title": "2019-11-21 Phone Deprivation", "file": "2019-11-21_Phone_Deprivation_109084731.html"},
                        ]
                    },
                    {
                        "title": "2024-2025 Responsibility Futures",
                        "file": "2024-2025-Responsibility-Futures_205717545.html",
                        "children": [
                            {"title": "2024-04-27 Clusteral Solidarity", "file": "2024-04-27_Clusteral_Solidarity_109248513.html"},
                            {"title": "9 Constraints of AI", "file": "9-Constraints-of-AI_91389954.html"},
                            {"title": "Predicate Calculus for Responsibility Index", "file": "Predicate-Calculus-for-Responsibility-Index_94044161.html"},
                            {"title": "2025-04-25 The Sugar Oracle", "file": "2025-04-25_The-Sugar-Oracle_109281281.html"},
                            {"title": "2025-04-26 Prolog Companions", "file": "2025-04-26_Prolog-Companions_109215762.html"},
                            {"title": "riskrunners/sugarscapes", "file": "110231553.html"},
                            {"title": "The Sugar Oracle Applications", "file": "The-Sugar-Oracle-Applications_112066561.html"},
                            {
                                "title": "Further Research: Social Agent-Based Models",
                                "file": "112033797.html",
                                "children": [
                                    {"title": "Social Agent-Based Models", "file": "Social-Agent-Based-Models_112001043.html"},
                                ]
                            },
                            {"title": "riskrunners/dark-campus", "file": "112295937.html"},
                            {"title": "riskrunners/schrodingers-fish", "file": "204308500.html"},
                            {"title": "Conclusion to Responsibility Index", "file": "Conclusion-to-Responsibility-Index_112001099.html"},
                            {"title": "2025-10-12 Common Grievances", "file": "2025-10-12-Common-Grievances_160595969.html"},
                            {"title": "Resp. Futures Integration with Cortext.io", "file": "Resp.-Futures-Integration-with-Cortext.io_190676994.html"},
                            {"title": "Tribute to The Local Hub", "file": "Tribute-to-The-Local-Hub_204636161.html"},
                        ]
                    },
                ]
            },
            {
                "title": "Allegories",
                "file": "Allegories_17760257.html",
                "children": [
                    {"title": "Crypto Mine", "file": "Crypto-Mine_17760311.html"},
                    {"title": "The Estranged Mouse", "file": "The-Estranged-Mouse_17760296.html"},
                    {"title": "Pimper", "file": "Pimper_17760326.html"},
                    {"title": "The Traveling Analyst", "file": "The-Traveling-Analyst_17760356.html"},
                    {"title": "The Boxers Strategy", "file": "The-Boxers-Strategy_17760371.html"},
                    {"title": "Honey, Flo gave me call", "file": "Honey%2C-Flo-gave-me-call_17760386.html"},
                    {"title": "The Big Sorority Shirt", "file": "The-Big-Sorority-Shirt_17760401.html"},
                    {"title": "Quotas took our jobs!", "file": "Quotas-took-our-jobs%21_17760423.html"},
                    {"title": "Who Moved My Cheese?", "file": "17760438.html"},
                    {"title": "The Brazen Cups", "file": "The-Brazen-Cups_17760453.html"},
                    {"title": "Re-Porter Potty", "file": "Re-Porter-Potty_17760468.html"},
                    {"title": "The Great Polished Catamaran", "file": "The-Great-Polished-Catamaran_17760341.html"},
                    {"title": "Digital Icarus", "file": "Digital-Icarus_33030147.html"},
                    {"title": "15 Minutes of Fame", "file": "15-Minutes-of-Fame_67076097.html"},
                    {"title": "Lavender-Cucumber-Blueberry Water", "file": "Lavender-Cucumber-Blueberry-Water_69926913.html"},
                    {"title": "The Grand Arbiter", "file": "The-Grand-Arbiter_78675969.html"},
                    {"title": "To Match Your Pretty Eyes", "file": "To-Match-Your-Pretty-Eyes_81428481.html"},
                    {"title": "AR Tactile Education Opportunities", "file": "AR-Tactile-Education-Opportunities_83787781.html"},
                    {"title": "Hermes", "file": "Hermes_84967427.html"},
                    {"title": "The Pacific Go", "file": "The-Pacific-Go_90800131.html"},
                    {"title": "Caveman Fashion", "file": "Caveman-Fashion_152895556.html"},
                    {"title": "Street Math", "file": "Street-Math_273383426.html"},
                ]
            },
            {
                "title": "iMASS and Family Resource Mgmt",
                "file": "iMASS-and-Family-Resource-Mgmt_125206530.html",
                "children": [
                    {
                        "title": "Account Ninja",
                        "file": "Account-Ninja_125206539.html",
                        "children": [
                            {"title": "jeffy893/account.ninja", "file": "208470021.html"},
                            {"title": "Account Ninja - Financial Dashboard", "file": "Account-Ninja---Financial-Dashboard_208437253.html"},
                        ]
                    },
                    {
                        "title": "Ambient-Gantt",
                        "file": "Ambient-Gantt_152797206.html",
                        "children": [
                            {"title": "2025-09-21 Dunbar Calculus of Value", "file": "2025-09-21-Dunbar-Calculus-of-Value_152895504.html"},
                            {"title": "2025-09-27 Decentral Time Value of Events", "file": "2025-09-27-Decentral-Time-Value-of-Events_152797190.html"},
                            {"title": "Ambient Gantt - the antidote", "file": "Ambient-Gantt---the-antidote_152797228.html"},
                            {"title": "Ambient Gantt Slides", "file": "Ambient-Gantt-Slides_152895520.html"},
                            {"title": "The Language of Happiness", "file": "The-Language-of-Happiness_152797235.html"},
                            {"title": "2019-10-30 FlyByWire Optimization", "file": "2019-10-30-FlyByWire-Optimization_144310273.html"},
                        ]
                    },
                    {"title": "2024-05-08 Family FHIR", "file": "2024-05-08-Family-FHIR_175734785.html"},
                    {"title": "2025-09-28 Tiny Homes Digital Twin", "file": "2025-09-28-Tiny-Homes-Digital-Twin_153092164.html"},
                    {"title": "2025-10-12 Family Charter", "file": "2025-10-12-Family-Charter_160497665.html"},
                    {"title": "2026-04-30 Language of Happiness", "file": "2026-04-30-Language-of-Happiness_291864577.html"},
                ]
            },
            {
                "title": "This Ship is Built - Final Reflection",
                "file": "This-Ship-is-Built---Final-Reflection_112001110.html",
                "children": [
                    {"title": "New Horizon", "file": "New-Horizon_112787458.html"},
                ]
            },
            {
                "title": "Central Links",
                "file": "Central-Links_192643158.html",
                "children": [
                    {"title": "LinguaLint: The Re-Search Engine", "file": "17563669.html"},
                    {"title": "Richards Plus: Consulting", "file": "17399884.html"},
                    {"title": "Richards Systems", "file": "Richards-Systems_17891329.html"},
                    {"title": "About Jefferson", "file": "About-Jefferson_17563671.html"},
                    {"title": "Integral Manuf. and Shared Services", "file": "Integral-Manuf.-and-Shared-Services_17498166.html"},
                    {"title": "Codebase", "file": "Codebase_193298433.html"},
                    {"title": "2022-2023 Philosophy Club", "file": "2022-2023-Philosophy-Club_17662020.html"},
                ]
            },
            {
                "title": "AI Resilience Architecture",
                "file": "AI-Resilience-Architecture_203751428.html",
                "children": [
                    {"title": "jeffy893/agentic-procurement", "file": "205029377.html"},
                    {"title": "jeffy893/gurila.tools - Potential Projects", "file": "204308481.html"},
                    {"title": "jeffy893/riskrunners - Potential Projects", "file": "203915300.html"},
                ]
            },
            {
                "title": "Survitality Series",
                "file": "Survitality-Series_273645597.html",
                "children": [
                    {
                        "title": "Put Options on Loyalty",
                        "file": "Put-Options-on-Loyalty_273580035.html",
                        "children": [
                            {"title": "Street Math (with a Super Computer?)", "file": "273711105.html"},
                            {"title": "Chapter 10 (of Put Options on Loyalty)", "file": "273416209.html"},
                            {"title": "Ontology of Survitality", "file": "Ontology-of-Survitality_329383944.html"},
                        ]
                    },
                ]
            },
        ]
    }
]

# ============================================
# External link mapping for LINK_ONLY pages
# ============================================

EXTERNAL_LINKS = {
    "110231553.html": "https://github.com/jeffy893/riskrunners/tree/dev/2.0/sugarscapes",
    "112295937.html": "https://github.com/jeffy893/riskrunners/tree/dev/2.0/legacy/dark-campus",
    "17399884.html": "https://www.richards.plus/",
    "17563669.html": "https://www.lingualint.com/",
    "2022-2023-Philosophy-Club_17662020.html": "https://www.epicideas.club/",
    "203915300.html": "https://github.com/jeffy893/riskrunners",
    "204308481.html": "https://github.com/jeffy893/gurila.tools",
    "204308500.html": "https://github.com/jeffy893/riskrunners/tree/dev/2.0/platforms/02_schrodingers-fish",
    "205029377.html": "https://github.com/jeffy893/agentic-procurement",
    "208470021.html": "https://github.com/jeffy893/account.ninja",
    "About-Jefferson_17563671.html": "https://www.jefferson.cloud/",
    "Account-Ninja---Financial-Dashboard_208437253.html": "https://account.ninja/",
    "Codebase_193298433.html": "https://github.com/jeffy893",
    "Inspired-by-the-GDELT-Project_17072130.html": "https://www.gdeltproject.org/",
    "Integral-Manuf.-and-Shared-Services_17498166.html": "https://www.integralmass.com/",
    "Resp.-Futures-Integration-with-Cortext.io_190676994.html": "https://github.com/jeffy893/riskrunners/tree/dev/2.0/responsibility-futures",
    "Richards-Systems_17891329.html": "https://www.richards.systems/",
    "Sponsor-Jefferson-to-Keep-Coding_17170460.html": "https://github.com/sponsors/jeffy893",
    "Tribute-to-The-Local-Hub_204636161.html": "https://github.com/jeffy893/riskrunners/tree/dev/2.0/platforms/02_schrodingers-fish/economic-overture",
}

# Google Drive links mapping
GDRIVE_LINKS = {
    "17399817.html": "https://docs.google.com/presentation/d/1iF034r66DqmLbjaLk6GjKlraQK_TBmU5_qHB9TzgyOg/edit?usp=sharing",
    "17399899.html": "https://drive.google.com/file/d/1DNyBEWJV30TY06fF_Os71mA3mys8LKAl/view?usp=sharing",
    "2016-11-28-Semantic-Algebra_17661953.html": "https://drive.google.com/file/d/19mTkX7dPVlAoY7zWT6jYoKPBOQwThO5e/view?usp=sharing",
    "2017-04-27-ISO-31000-News-Service_17661955.html": "https://drive.google.com/file/d/1NwZr6wiNvsbLNfmS2uzgbGatrj-FEy4X/view?usp=sharing",
    "2018-06-20-Cortext-Nascent-Aim_17367066.html": "https://drive.google.com/file/d/1N0aNkgt0O8JP2CB31_q-zcTjqlbYikBA/view?usp=sharing",
    "2018-10-08-Cortext-Data-Model_17203235.html": "https://drive.google.com/file/d/1oReSeNzUJSY9_Nchgov31JZbXPYRHPQw/view?usp=sharing",
    "2019-04-13_Constitution_of_MANGO_94404609.html": "https://drive.google.com/file/d/1D-k0A5SKWPvVWQBOMCGAAyfHYbAw2zRL/view?usp=drivesdk",
    "2019-05-29_Invasive-Species_90505220.html": "https://drive.google.com/file/d/1prvOrJPCp8j5F7xyoBeSnpqqhTIqnz-g/view?usp=sharing",
    "2019-10-30-FlyByWire-Optimization_144310273.html": "https://drive.google.com/file/d/1uKGg4K9C6-ifASTgi4bRyvbtLrqX5jXY/view?usp=sharing",
    "2019-11-21_Phone_Deprivation_109084731.html": "https://drive.google.com/file/d/1Bex6QPXIJA8D-EdDXcoUQCIstoA4wa5J/view?usp=sharing",
    "2021-03-12_Intention_Div_Negligence_96206849.html": "https://drive.google.com/file/d/1qjUBgX_isiVw_vC1pNxuBLc2sEBbok68/view?usp=drivesdk",
    "2022-11-01-AWS-Batch-Fargate-Setup_17236017.html": "https://drive.google.com/file/d/1bueBz1oQ4VuOLIH3fyt8qu9ZoQWoirTw/view?usp=sharing",
    "2024-02-27-Serverless-Arch-ProcureCrawl_17399881.html": "https://drive.google.com/file/d/18QxMPgKUVtTBfn0xDYd_QDrRLV-S2zf5/view?usp=sharing",
    "2024-04-27_Clusteral_Solidarity_109248513.html": "https://drive.google.com/file/d/1q2mK_ByRP7YbcQweH1wBrHfFFiDAPcPA/view?usp=drive_link",
    "2024-05-08-Family-FHIR_175734785.html": "https://drive.google.com/file/d/1FGYsRFzFsoXPzgjZKpnsV8BqVK7U1xiX/view?usp=sharing",
    "2025-04-25_The-Sugar-Oracle_109281281.html": "https://drive.google.com/file/d/1mGq3KV1pN1Pje0K6x5JCJhE_rV7Bu_Io/view?usp=drive_link",
    "2025-04-26_Prolog-Companions_109215762.html": "https://drive.google.com/file/d/1JAgpDY5b25kKsKpS98xvkwtJ4y_Kexe0/view?usp=drive_link",
    "2025-09-21-Dunbar-Calculus-of-Value_152895504.html": "https://drive.google.com/file/d/1ghNZUIuqR2_dg_U5V32IF-9w91SoW4XH/view?usp=sharing",
    "2025-09-27-Decentral-Time-Value-of-Events_152797190.html": "https://drive.google.com/file/d/1s-INmPZocEUm91ix8EFE16kQusbNCQm7/view?usp=sharing",
    "2025-09-28-Tiny-Homes-Digital-Twin_153092164.html": "https://drive.google.com/file/d/1wNAc3GcN6U--HRr3GasAj4OMoupcQWC1/view?usp=sharing",
    "2025-10-12-Common-Grievances_160595969.html": "https://drive.google.com/file/d/1b9FNXonVrPjTEBKP9aQHUowqm47VJbTN/view?usp=sharing",
    "2025-10-12-Family-Charter_160497665.html": "https://drive.google.com/file/d/1x8fIid56oBoxp15qOz-P64MEdGKscwcK/view?usp=sharing",
    "2026-04-30-Language-of-Happiness_291864577.html": "https://drive.google.com/file/d/1epCJ2zTn5QdN0J9w9I5c2TAxhxMAYR1G/view?usp=sharing",
    "96337921.html": "https://drive.google.com/file/d/0B2QZwX8LNehRZkRRY0kzM1BqaGM/view?usp=drivesdk&resourcekey=0-GWLFN4LcxCMOFN8XomWJDA",
    "Ambient-Gantt---the-antidote_152797228.html": "https://drive.google.com/file/d/1rHQkng9Ke3vttyeiw1kcMvc7eNXN5DXv/view?usp=sharing",
    "Ambient-Gantt-Slides_152895520.html": "https://drive.google.com/file/d/11EnnMQF4dMANL2CCxjkgtnCeKlIvSyJt/view?usp=sharing",
    "The-Language-of-Happiness_152797235.html": "https://drive.google.com/file/d/1AUAzhivtUgH_2XN9-CUA5--rdrqFX7JL/view?usp=sharing",
}

AMAZON_LINKS = {
    "2015-Philosophy-of-AI_247627792.html": "https://www.amazon.com/dp/B0GLFMX155",
    "2019-Responsibility-Futures_247758851.html": "https://www.amazon.com/dp/B0GL5XM82R",
}

# Pages with manually-created custom content (skip during build if already exists)
CUSTOM_PAGES = {
    "Cortext.io-Event-Report_17498151.html",
}

# Popular pages (25+ views from Confluence analytics)
# These get a visual "popular" indicator in the sidebar
POPULAR_PAGES = {
    "Richards-Systems_16679146.html",          # 1976
    "AI-Resilience-Architecture_203751428.html",  # 69
    "Allegories_17760257.html",                # 63
    "Lavender-Cucumber-Blueberry-Water_69926913.html",  # 54
    "iMASS-and-Family-Resource-Mgmt_125206530.html",    # 54
    "9-Constraints-of-AI_91389954.html",       # 44
    "2014-Cosmos-Introduction_91488258.html",  # 43
    "This-Ship-is-Built---Final-Reflection_112001110.html",  # 39
    "The-Boxers-Strategy_17760371.html",       # 37
    "2024-10-01-Reverse-Conway-on-Richards-Systems_39616513.html",  # 37
    "Quotas-took-our-jobs%21_17760423.html",   # 33
    "The-Great-Polished-Catamaran_17760341.html",  # 28
    "The-Grand-Arbiter_78675969.html",         # 27
    "Ambient-Gantt_152797206.html",            # 27
    "Account-Ninja_125206539.html",            # 26
    "Cortext.io-Event-Report_17498151.html",   # 25
    "Digital-Icarus_33030147.html",            # 25
}

# ============================================
# Page title lookup
# ============================================

def build_title_map(tree, result=None):
    """Build a flat map of filename -> title from nav tree."""
    if result is None:
        result = {}
    for node in tree:
        result[node["file"]] = node["title"]
        if "children" in node:
            build_title_map(node["children"], result)
    return result

TITLE_MAP = build_title_map(NAV_TREE)


def get_page_slug(filename):
    """Convert RS filename to a clean page slug for the new site."""
    slug = filename.replace('.html', '').replace('%2C', ',').replace('%21', '!')
    return slug


def get_page_url(filename, from_root=False):
    """Get URL for a page in the new site."""
    if filename == "Richards-Systems_16679146.html":
        return "/" if from_root else "index.html"
    return f"pages/{get_page_slug(filename)}.html"

# ============================================
# Sidebar HTML generation
# ============================================

def render_nav_tree(tree, current_file=None, depth=0):
    """Render the sidebar navigation tree as HTML."""
    html_parts = []
    cls = 'nav-tree' if depth == 0 else 'nav-tree'
    expanded = ' expanded' if depth == 0 else ''
    html_parts.append(f'<ul class="{cls}{expanded}">')
    
    for node in tree:
        filename = node["file"]
        title = node["title"]
        has_children = "children" in node and len(node.get("children", [])) > 0
        is_active = (filename == current_file)
        is_external = filename in EXTERNAL_LINKS
        is_home = node.get("is_home", False)
        
        # Check if current file is in this subtree
        in_subtree = is_in_subtree(node, current_file) if has_children else False
        
        html_parts.append('<li class="nav-item">')
        
        # Determine link
        if is_external:
            url = EXTERNAL_LINKS[filename]
            active_cls = ' active' if is_active else ''
            html_parts.append(f'<a class="nav-link{active_cls}" href="{url}" target="_blank" rel="noopener">')
            html_parts.append(f'<span>{html_escape(title)}</span>')
            html_parts.append('<svg class="external-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/></svg>')
            html_parts.append('</a>')
        elif is_home:
            active_cls = ' active' if is_active else ''
            html_parts.append(f'<a class="nav-link{active_cls}" href="index.html">')
            html_parts.append(f'<span>{html_escape(title)}</span></a>')
        else:
            active_cls = ' active' if is_active else ''
            page_url = f"pages/{get_page_slug(filename)}.html"
            popular_cls = ' popular' if filename in POPULAR_PAGES else ''
            
            if has_children:
                toggle_cls = ' expanded' if in_subtree else ''
                html_parts.append(f'<a class="nav-link{active_cls}{popular_cls}" href="{page_url}">')
                html_parts.append(f'<button class="nav-toggle{toggle_cls}" aria-label="Expand"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg></button>')
                html_parts.append(f'<span>{html_escape(title)}</span></a>')
            else:
                html_parts.append(f'<a class="nav-link{active_cls}{popular_cls}" href="{page_url}">')
                html_parts.append(f'<span>{html_escape(title)}</span></a>')
        
        if has_children:
            html_parts.append(render_nav_tree(node["children"], current_file, depth + 1))
        
        html_parts.append('</li>')
    
    html_parts.append('</ul>')
    return '\n'.join(html_parts)


def is_in_subtree(node, target_file):
    """Check if target_file is anywhere in this node's subtree."""
    if node["file"] == target_file:
        return True
    for child in node.get("children", []):
        if is_in_subtree(child, target_file):
            return True
    return False


def html_escape(text):
    """Escape HTML entities."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

# ============================================
# HTML Template
# ============================================

def page_template(title, content, sidebar_html, breadcrumbs_html, meta="", is_home=False):
    """Generate full HTML page with template."""
    css_path = "../assets/css/styles.css" if not is_home else "assets/css/styles.css"
    js_path = "../assets/js/main.js" if not is_home else "assets/js/main.js"
    
    # Fix sidebar links for home page (they already have pages/ prefix)
    # For subpages, links need to be relative properly
    if is_home:
        sidebar_nav = sidebar_html
    else:
        sidebar_nav = sidebar_html.replace('href="index.html"', 'href="../index.html"')
        sidebar_nav = sidebar_nav.replace('href="pages/', 'href="')
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_escape(title)} - Richards Systems Wiki</title>
    <meta name="description" content="Richards Systems Knowledge Base — 10+ years of homegrown AI, responsibility futures, and systems architecture.">
    
    <!-- Open Graph / Twitter -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://wiki.richards.systems/">
    <meta property="og:title" content="{html_escape(title)} - Richards Systems Wiki">
    <meta property="og:description" content="Richards Systems Knowledge Base — 10+ years of homegrown AI, responsibility futures, and systems architecture.">
    <meta property="og:image" content="https://wiki.richards.systems/assets/images/logo.jpeg">
    <meta property="og:image:width" content="1536">
    <meta property="og:image:height" content="1536">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:image" content="https://wiki.richards.systems/assets/images/logo.jpeg">
    
    <!-- Favicons -->
    <link rel="icon" type="image/png" sizes="32x32" href="{('assets/images/favicon-32.png' if is_home else '../assets/images/favicon-32.png')}">
    <link rel="icon" type="image/png" sizes="16x16" href="{('assets/images/favicon-16.png' if is_home else '../assets/images/favicon-16.png')}">
    <link rel="apple-touch-icon" href="{('assets/images/apple-touch-icon.png' if is_home else '../assets/images/apple-touch-icon.png')}">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{css_path}">
</head>
<body>
<div class="site-wrapper">
    <!-- Header -->
    <header class="site-header">
        <div class="header-inner">
            <div class="header-left">
                <button class="sidebar-toggle" aria-label="Toggle navigation">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M3 12h18M3 6h18M3 18h18"/>
                    </svg>
                </button>
                <a href="{'index.html' if is_home else '../index.html'}" class="site-logo">
                    <img src="{('assets/images/logo.jpeg' if is_home else '../assets/images/logo.jpeg')}" alt="Richards Systems" class="logo-image">
                    <div>
                        <div class="site-title">Richards Systems</div>
                        <div class="site-subtitle">Knowledge Base</div>
                    </div>
                </a>
            </div>
            <div class="header-right">
                <nav class="header-nav">
                    <a href="https://jefferson.cloud" target="_blank" class="header-nav-link socialize">Socialize</a>
                    <a href="https://richards.systems" target="_blank" class="header-nav-link decode">Decode</a>
                    <a href="https://richards.plus" target="_blank" class="header-nav-link consult">Consult</a>
                </nav>
            </div>
        </div>
    </header>

    <div class="site-body">
        <!-- Sidebar -->
        <aside class="site-sidebar">
            <div class="sidebar-search">
                <div class="search-input-wrapper">
                    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
                    <input type="text" class="search-input" placeholder="Search pages..." aria-label="Search pages">
                    <div class="search-results"></div>
                </div>
            </div>
            <div class="sidebar-content">
                {sidebar_nav}
            </div>
        </aside>
        <div class="sidebar-overlay"></div>

        <!-- Main Content -->
        <main class="site-main">
            <div class="content-wrapper">
                {breadcrumbs_html}
                {content}
            </div>

            <!-- Footer -->
            <footer class="site-footer">
                <div class="footer-content">
                    <div class="footer-section">
                        <h4>Richards Systems</h4>
                        <p>Navigating 10+ years of homegrown AI, responsibility futures, and systems architecture.</p>
                    </div>
                    <div class="footer-section">
                        <h4>Jefferson.Cloud</h4>
                        <div class="footer-links">
                            <a href="https://jefferson.cloud" target="_blank">Socialize</a>
                            <a href="https://richards.systems" target="_blank">Decode</a>
                            <a href="https://richards.plus" target="_blank">Consult</a>
                        </div>
                    </div>
                    <div class="footer-section">
                        <h4>Connect</h4>
                        <div class="footer-links">
                            <a href="mailto:jefferson@richards.plus">jefferson@richards.plus</a>
                            <a href="https://calendar.app.google/P5EQ2C3zceR9r1NM8" target="_blank">Book 30min with Jefferson</a>
                        </div>
                    </div>
                </div>
                <div class="footer-bottom">
                    <div class="footer-social">
                        <a href="https://www.instagram.com/richards.plus/" target="_blank" rel="noopener noreferrer" class="social-link" aria-label="Instagram">
                            <svg viewBox="0 0 24 24"><path d="M12 0C8.74 0 8.333.015 7.053.072 5.775.132 4.905.333 4.14.63c-.789.306-1.459.717-2.126 1.384S.935 3.35.63 4.14C.333 4.905.131 5.775.072 7.053.012 8.333 0 8.74 0 12s.015 3.667.072 4.947c.06 1.277.261 2.148.558 2.913.306.788.717 1.459 1.384 2.126.667.666 1.336 1.079 2.126 1.384.766.296 1.636.499 2.913.558C8.333 23.988 8.74 24 12 24s3.667-.015 4.947-.072c1.277-.06 2.148-.262 2.913-.558.788-.306 1.459-.718 2.126-1.384.666-.667 1.079-1.335 1.384-2.126.296-.765.499-1.636.558-2.913.06-1.28.072-1.687.072-4.947s-.015-3.667-.072-4.947c-.06-1.277-.262-2.149-.558-2.913-.306-.789-.718-1.459-1.384-2.126C21.319 1.347 20.651.935 19.86.63c-.765-.297-1.636-.499-2.913-.558C15.667.012 15.26 0 12 0zm0 2.16c3.203 0 3.585.016 4.85.071 1.17.055 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.015 3.585-.074 4.85c-.061 1.17-.256 1.805-.421 2.227-.224.562-.479.96-.899 1.382-.419.419-.824.679-1.38.896-.42.164-1.065.36-2.235.413-1.274.057-1.649.07-4.859.07-3.211 0-3.586-.015-4.859-.074-1.171-.061-1.816-.256-2.236-.421-.569-.224-.96-.479-1.379-.899-.421-.419-.69-.824-.9-1.38-.165-.42-.359-1.065-.42-2.235-.045-1.26-.061-1.649-.061-4.844 0-3.196.016-3.586.061-4.861.061-1.17.255-1.814.42-2.234.21-.57.479-.96.9-1.381.419-.419.81-.689 1.379-.898.42-.166 1.051-.361 2.221-.421 1.275-.045 1.65-.06 4.859-.06l.045.03zm0 3.678c-3.405 0-6.162 2.76-6.162 6.162 0 3.405 2.76 6.162 6.162 6.162 3.405 0 6.162-2.76 6.162-6.162 0-3.405-2.76-6.162-6.162-6.162zM12 16c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4zm7.846-10.405c0 .795-.646 1.44-1.44 1.44-.795 0-1.44-.646-1.44-1.44 0-.794.646-1.439 1.44-1.439.793-.001 1.44.645 1.44 1.439z"/></svg>
                        </a>
                        <a href="https://www.linkedin.com/in/jefferson-richards/" target="_blank" rel="noopener noreferrer" class="social-link" aria-label="LinkedIn">
                            <svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                        </a>
                        <a href="https://github.com/jeffy893" target="_blank" rel="noopener noreferrer" class="social-link" aria-label="GitHub">
                            <svg viewBox="0 0 24 24"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
                        </a>
                        <a href="https://x.com/perrydime" target="_blank" rel="noopener noreferrer" class="social-link" aria-label="X (Twitter)">
                            <svg viewBox="0 0 24 24"><path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/></svg>
                        </a>
                    </div>
                    <p>&copy; 2026 Richards Systems. Knowledge base for AI, responsibility, and systems architecture.</p>
                </div>
            </footer>
        </main>
    </div>
</div>

<!-- Mobile Bottom Navigation -->
<nav class="mobile-bottom-nav">
    <ul class="bottom-nav-items">
        <li><a href="{'index.html' if is_home else '../index.html'}" class="bottom-nav-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9,22 9,12 15,12 15,22"/></svg>
            <span>Home</span>
        </a></li>
        <li><a href="https://jefferson.cloud" target="_blank" class="bottom-nav-item socialize">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>
            <span>Socialize</span>
        </a></li>
        <li><a href="https://richards.systems" target="_blank" class="bottom-nav-item decode">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="16,18 22,12 16,6"/><polyline points="8,6 2,12 8,18"/></svg>
            <span>Decode</span>
        </a></li>
        <li><a href="https://richards.plus" target="_blank" class="bottom-nav-item consult">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
            <span>Consult</span>
        </a></li>
    </ul>
</nav>

<script src="{js_path}"></script>
</body>
</html>'''

# ============================================
# Content extraction from Confluence HTML
# ============================================

def extract_content(filepath):
    """Extract the main content from a Confluence HTML export page."""
    content = filepath.read_text(errors='replace')
    
    # Extract main content div - try multiple patterns
    main_m = re.search(
        r'id="main-content"[^>]*class="wiki-content group">(.*?)</div>\s*\n\s*(?:</div>|<div class="pageSection)',
        content, re.DOTALL
    )
    if not main_m:
        # Fallback: broader match
        main_m = re.search(
            r'id="main-content"[^>]*class="wiki-content group">(.*?)</div>\s*\n\s*\n',
            content, re.DOTALL
        )
    if not main_m:
        # Last resort: get everything after wiki-content group until footer
        main_m = re.search(
            r'id="main-content"[^>]*class="wiki-content group">(.*?)(?=<div id="footer")',
            content, re.DOTALL
        )
    if not main_m:
        return ""
    
    raw = main_m.group(1).strip()
    
    # Clean up Confluence-specific markup
    raw = clean_confluence_html(raw)
    
    return raw


def clean_confluence_html(raw):
    """Clean Confluence HTML into presentable article content."""
    # Remove local-id attributes
    raw = re.sub(r'\s*local-id="[^"]*"', '', raw)
    
    # Remove data-colorid spans (keep inner text)
    raw = re.sub(r'<span data-colorid="[^"]*">(.*?)</span>', r'\1', raw)
    
    # Remove confluence layout divs but keep content
    raw = re.sub(r'<div class="contentLayout2">.*?</style>\s*', '', raw, flags=re.DOTALL)
    raw = re.sub(r'<div class="columnLayout[^"]*"[^>]*>', '', raw)
    raw = re.sub(r'<div class="cell[^"]*"[^>]*>', '', raw)
    raw = re.sub(r'<div class="innerCell">', '', raw)
    raw = re.sub(r'</div>\s*</div>\s*</div>', '', raw)
    
    # Remove search macro
    raw = re.sub(r'<div class="search-macro.*?</div>\s*</div>\s*</div>', '', raw, flags=re.DOTALL)
    
    # Remove inline comment markers
    raw = re.sub(r'<span class="inline-comment-marker"[^>]*>(.*?)</span>', r'\1', raw, flags=re.DOTALL)
    
    # Remove data-linked-resource attributes
    raw = re.sub(r'\s*data-linked-resource[^=]*="[^"]*"', '', raw)
    raw = re.sub(r'\s*data-[a-z-]+="[^"]*"', '', raw)
    
    # Fix image paths - point to compressed images, converting extensions to .jpg
    def fix_img_src(m):
        path = m.group(1)
        # Strip any ?width= params
        path = re.sub(r'\?.*$', '', path)
        # Change extension to .jpg, or add .jpg if no extension
        if re.search(r'\.(png|heic|jpeg|jpg)$', path, re.IGNORECASE):
            path = re.sub(r'\.(png|heic|jpeg)$', '.jpg', path, flags=re.IGNORECASE)
        else:
            path = path + '.jpg'
        return f'src="../assets/images/attachments/{path}"'
    
    raw = re.sub(r'src="attachments/([^"]*)"', fix_img_src, raw)
    
    # Remove width/height constraints from images but keep reasonable
    raw = re.sub(r'<img class="confluence-embedded-image[^"]*"', '<img class="article-image"', raw)
    raw = re.sub(r'\s*loading="lazy"', '', raw)
    
    # Convert YouTube links to embeds
    raw = re.sub(
        r'<a href="(https://www\.youtube\.com/watch\?v=([^"&]+))[^"]*"[^>]*>[^<]*</a>',
        r'<div class="video-embed"><iframe src="https://www.youtube.com/embed/\2" allowfullscreen></iframe></div>',
        raw
    )
    
    # Fix internal page links
    raw = fix_internal_links(raw)
    
    # Remove empty paragraphs
    raw = re.sub(r'<p\s*/>', '', raw)
    raw = re.sub(r'<p>\s*</p>', '', raw)
    
    # Remove remaining closing divs
    raw = re.sub(r'</div>', '', raw)
    
    # Clean up excessive whitespace
    raw = re.sub(r'\n{3,}', '\n\n', raw)
    
    return raw.strip()


def fix_internal_links(html_str):
    """Fix links to other wiki pages to point to new site structure."""
    def replace_link(match):
        full_match = match.group(0)
        href = match.group(1)
        
        # Skip external links
        if href.startswith('http://') or href.startswith('https://'):
            return full_match
        
        # Skip anchors
        if href.startswith('#'):
            return full_match
        
        # Internal page link
        if href.endswith('.html'):
            filename = href
            if filename in EXTERNAL_LINKS:
                return full_match.replace(href, EXTERNAL_LINKS[filename])
            slug = get_page_slug(filename)
            return full_match.replace(href, f"{slug}.html")
        
        return full_match
    
    return re.sub(r'href="([^"]*)"', replace_link, html_str)

# ============================================
# Page generation
# ============================================

def get_breadcrumbs(filename, tree, path=None):
    """Get breadcrumb path for a file in the nav tree."""
    if path is None:
        path = []
    for node in tree:
        if node["file"] == filename:
            return path + [node]
        if "children" in node:
            result = get_breadcrumbs(filename, node["children"], path + [node])
            if result:
                return result
    return None


def render_breadcrumbs(filename, is_home=False):
    """Render breadcrumb HTML."""
    if is_home:
        return ''
    
    crumbs = get_breadcrumbs(filename, NAV_TREE)
    if not crumbs or len(crumbs) <= 1:
        return ''
    
    parts = []
    parts.append('<nav class="breadcrumbs">')
    for i, crumb in enumerate(crumbs[:-1]):
        f = crumb["file"]
        if f == "Richards-Systems_16679146.html":
            url = "../index.html"
        else:
            url = f"{get_page_slug(f)}.html"
        parts.append(f'<a href="{url}">{html_escape(crumb["title"])}</a>')
        parts.append('<span class="separator">/</span>')
    parts.append(f'<span>{html_escape(crumbs[-1]["title"])}</span>')
    parts.append('</nav>')
    return '\n'.join(parts)


def generate_gdrive_page(filename, title):
    """Generate a page that embeds a Google Drive document."""
    url = GDRIVE_LINKS[filename]
    
    # Convert view links to preview/embed links
    embed_url = url
    if '/view' in url:
        embed_url = url.replace('/view', '/preview')
    elif '/edit' in url:
        embed_url = url.replace('/edit', '/preview')
    
    content = f'''<h1 class="page-title">{html_escape(title)}</h1>
<div class="page-meta">Document hosted on Google Drive</div>
<div class="article-content">
    <a href="{url}" target="_blank" class="external-link-card">
        <div class="link-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
            </svg>
        </div>
        <div class="link-text">
            <div class="link-title">Open Document in Google Drive</div>
            <div class="link-url">Click to view the full document</div>
        </div>
    </a>
    <iframe class="pdf-embed" src="{embed_url}" allowfullscreen></iframe>
</div>'''
    return content


def generate_external_link_page(filename, title):
    """Generate a page for external links."""
    url = EXTERNAL_LINKS.get(filename) or AMAZON_LINKS.get(filename, '#')
    
    icon_svg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/></svg>'
    
    content = f'''<h1 class="page-title">{html_escape(title)}</h1>
<div class="page-meta">External resource</div>
<div class="article-content">
    <a href="{url}" target="_blank" rel="noopener" class="external-link-card">
        <div class="link-icon">{icon_svg}</div>
        <div class="link-text">
            <div class="link-title">{html_escape(title)}</div>
            <div class="link-url">{html_escape(url)}</div>
        </div>
    </a>
</div>'''
    return content


def generate_content_page(filename, title):
    """Generate a page from actual Confluence content."""
    filepath = RS_DIR / filename
    if not filepath.exists():
        raw_content = ""
    else:
        raw_content = extract_content(filepath)
    
    # Check if content is essentially empty (just whitespace/empty tags)
    text_only = re.sub(r'<[^>]+>', '', raw_content).strip()
    
    # If empty, check if this is a parent page and generate child links
    if len(text_only) < 30:
        children = get_children(filename, NAV_TREE)
        if children:
            raw_content = generate_children_list(title, children)
    
    # Extract metadata
    meta = ""
    if filepath.exists():
        file_content = filepath.read_text(errors='replace')
        meta_m = re.search(r'Created by.*?<span class=.author.>\s*(.*?)</span>(.*?)(?:</div>)', file_content, re.DOTALL)
        if meta_m:
            author = meta_m.group(1).strip()
            rest = meta_m.group(2).strip()
            date_m = re.search(r'(?:last modified on|on)\s+(\w+ \d+,\s*\d+)', rest)
            date_str = date_m.group(1) if date_m else ""
            meta = f"By {author}"
            if date_str:
                meta += f" · {date_str}"
    
    content = f'''<h1 class="page-title">{html_escape(title)}</h1>
<div class="page-meta">{meta}</div>
<div class="article-content">
{raw_content}
</div>'''
    return content


def get_children(filename, tree):
    """Find the children of a given filename in the nav tree."""
    for node in tree:
        if node["file"] == filename:
            return node.get("children", [])
        if "children" in node:
            result = get_children(filename, node["children"])
            if result is not None:
                return result
    return None


def generate_children_list(parent_title, children):
    """Generate a nice list of child page links for a folder page."""
    parts = []
    parts.append(f'<p>Explore the pages in this section:</p>')
    parts.append('<div class="links-grid">')
    
    for child in children:
        child_file = child["file"]
        child_title = child["title"]
        has_grandchildren = "children" in child and len(child.get("children", [])) > 0
        
        if child_file in EXTERNAL_LINKS:
            url = EXTERNAL_LINKS[child_file]
            parts.append(f'<a href="{url}" target="_blank" class="link-item">')
            parts.append(f'<span class="link-dot"></span>{html_escape(child_title)}')
            parts.append('</a>')
        else:
            slug = get_page_slug(child_file)
            popular_cls = ' link-item-popular' if child_file in POPULAR_PAGES else ''
            parts.append(f'<a href="{slug}.html" class="link-item{popular_cls}">')
            parts.append(f'<span class="link-dot"></span>{html_escape(child_title)}')
            if has_grandchildren:
                count = len(child["children"])
                parts.append(f' <span style="color:var(--color-text-muted);font-size:0.8rem;">({count} pages)</span>')
            parts.append('</a>')
    
    parts.append('</div>')
    return '\n'.join(parts)

# ============================================
# Homepage generation
# ============================================

def generate_homepage():
    """Generate the main index.html homepage."""
    content = '''<div class="home-hero">
    <img src="assets/images/logo.jpeg" alt="Richards Systems" class="home-logo">
    <h1>Richards Systems</h1>
    <p class="subtitle">Navigating 10+ years of homegrown AI to steer Integral Manufacturing and Shared Services, making a case for <a href="pages/9-Constraints-of-AI_91389954.html" class="hero-link">9 Constraints of AI</a>, and deriving an <strong>Ontology</strong> of Survitality.</p>
    <div class="contact-info">
        <a href="#" class="copy-email-btn" data-email="jefferson@richards.plus">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
            <span class="copy-text">jefferson@richards.plus</span>
        </a>
        <a href="https://calendar.app.google/P5EQ2C3zceR9r1NM8" target="_blank">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            Book 30min with Jefferson
        </a>
    </div>
    <div class="home-search">
        <div class="search-input-wrapper">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
            <input type="text" class="search-input home-search-input" placeholder="Search all pages..." aria-label="Search pages">
            <div class="search-results"></div>
        </div>
    </div>
</div>

<!-- Featured: Survitality Book Series -->
<section class="books-feature">
    <div class="books-feature-inner">
        <a href="https://www.amazon.com/dp/B0GQVVVD6Q?binding=paperback" target="_blank" class="books-image-link">
            <img src="assets/images/survitality-books.png" alt="The Survitality Series by Jefferson Richards" class="books-image">
        </a>
        <div class="books-content">
            <h2 class="books-title">The Survitality Series</h2>
            <p class="books-tagline">Three volumes exploring data architecture, neurobiology, linguistics, and socioeconomic governance — a framework for navigating an algorithmic world with engineered certainty and vitality.</p>
            <div class="books-list">
                <div class="book-item">
                    <strong>Book 1: Survitality of the Synapse</strong>
                    <p>The architecture of language, machine vs. organic learning, and the macro synapse — how neural networks mirror data architecture.</p>
                </div>
                <div class="book-item">
                    <strong>Book 2: Stockholm Forgiveness of Responsibility</strong>
                    <p>The calculus of choice (R = I/N), media event codes, and responsibility futures — locking in future choices through agreements.</p>
                </div>
                <div class="book-item">
                    <strong>Book 3: Put Options on Loyalty</strong>
                    <p>Optionality requires loyalty. The Dunbar Calculus of Value, Ambient Gantt, Family Medic, and the Family Charter — translating macroeconomic tools into household cooperation.</p>
                </div>
            </div>
            <a href="https://www.amazon.com/dp/B0GQVVVD6Q?binding=paperback" target="_blank" class="books-cta">
                View on Amazon
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3"/></svg>
            </a>
        </div>
    </div>
</section>

<!-- Watch: 5 Minute Overview -->
<section class="video-feature">
    <h2 class="video-feature-title">&#127916; Watch 5 Minute Overview</h2>
    <div class="video-feature-player">
        <video controls preload="metadata" poster="assets/images/logo.jpeg">
            <source src="assets/videos/survitality-overview.mp4" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
</section>

<!-- Table of Contents -->
<nav class="toc">
    <h2 class="toc-title">Table of Contents</h2>
    <div class="toc-grid">
        <a href="pages/2015-2025-Cortext.io_193134629.html" class="toc-card">
            <div class="toc-icon">&#128640;</div>
            <div class="toc-card-content">
                <h3>2015-2025 Cortext.io</h3>
                <p>A lightweight AI middleware — semantic algebra, microservices, elastic stack, and the evolution to LinguaLint</p>
                <span class="toc-count">17 pages</span>
            </div>
        </a>
        <a href="pages/2019-2025-Responsibility-Futures_192643159.html" class="toc-card">
            <div class="toc-icon">&#9878;&#65039;</div>
            <div class="toc-card-content">
                <h3>Responsibility Futures</h3>
                <p>Constitution of MANGO, 9 Constraints of AI, Sugar Oracle, Social Agent-Based Models, and predicate calculus</p>
                <span class="toc-count">19 pages</span>
            </div>
        </a>
        <a href="pages/Allegories_17760257.html" class="toc-card toc-card-featured">
            <div class="toc-icon">&#128214;</div>
            <div class="toc-card-content">
                <h3>Allegories</h3>
                <p>Speaking Otherwise — 21 stories from Crypto Mine to Street Math, translating complex systems into narrative</p>
                <span class="toc-count">21 stories</span>
            </div>
        </a>
        <a href="pages/iMASS-and-Family-Resource-Mgmt_125206530.html" class="toc-card">
            <div class="toc-icon">&#127968;</div>
            <div class="toc-card-content">
                <h3>iMASS &amp; Family Resource Mgmt</h3>
                <p>Account Ninja, Ambient-Gantt, Family FHIR, Tiny Homes Digital Twin, and the Language of Happiness</p>
                <span class="toc-count">10 pages</span>
            </div>
        </a>
        <a href="pages/Survitality-Series_273645597.html" class="toc-card">
            <div class="toc-icon">&#127793;</div>
            <div class="toc-card-content">
                <h3>Survitality Series</h3>
                <p>Put Options on Loyalty, Street Math with a Super Computer, and the Ontology of Survitality</p>
                <span class="toc-count">4 pages</span>
            </div>
        </a>
        <a href="pages/AI-Resilience-Architecture_203751428.html" class="toc-card">
            <div class="toc-icon">&#129302;</div>
            <div class="toc-card-content">
                <h3>AI Resilience Architecture</h3>
                <p>Potential projects — agentic procurement, gurila.tools, and riskrunners</p>
                <span class="toc-count">3 pages</span>
            </div>
        </a>
        <a href="pages/This-Ship-is-Built---Final-Reflection_112001110.html" class="toc-card">
            <div class="toc-icon">&#9973;</div>
            <div class="toc-card-content">
                <h3>This Ship is Built</h3>
                <p>Final reflection and New Horizon</p>
                <span class="toc-count">2 pages</span>
            </div>
        </a>
        <a href="pages/Central-Links_192643158.html" class="toc-card">
            <div class="toc-icon">&#128279;</div>
            <div class="toc-card-content">
                <h3>Central Links</h3>
                <p>LinguaLint, Richards Plus, About Jefferson, iMASS, Codebase, and Philosophy Club</p>
                <span class="toc-count">7 links</span>
            </div>
        </a>
    </div>
</nav>

<!-- Initial Design -->
<section class="home-section">
    <h2 class="section-heading">Initial Design</h2>
    <div class="featured-links">
        <a href="pages/2014-Cosmos-Introduction_91488258.html" class="featured-link">
            <span class="featured-emoji">&#127756;</span>
            <span class="featured-text">2014 Cosmos Introduction</span>
        </a>
        <a href="pages/96337921.html" class="featured-link">
            <span class="featured-emoji">&#128161;</span>
            <span class="featured-text">2014 Philosophy: Freedom to Model</span>
        </a>
        <a href="pages/2015-Philosophy-of-AI_247627792.html" class="featured-link">
            <span class="featured-emoji">&#129504;</span>
            <span class="featured-text">2015 Philosophy of AI</span>
        </a>
    </div>
</section>

<!-- Top Topics -->
<section class="home-section">
    <h2 class="section-heading">Cortext.io Top Topics</h2>
    <div class="topic-grid">
        <div class="topic-card">
            <h3>&#127827; Nascent Aim</h3>
            <ul><li>Primal Semantic Lean</li><li>2015-2017 News</li></ul>
        </div>
        <div class="topic-card">
            <h3>&#129373; End in Mind</h3>
            <ul><li>Semantic Algebra</li><li>Thread of Intent</li><li>Tokenize on Primes</li></ul>
        </div>
        <div class="topic-card">
            <h3>&#127821; ISO 31000 News</h3>
            <ul><li>Tired of Fake News?</li><li>50 Emails in 3 Days</li><li>GDELT Project</li></ul>
        </div>
        <div class="topic-card">
            <h3>&#127824; Microservices</h3>
            <ul><li>Lambda &lt; 15 Min</li><li>AWS Batch &gt; 15 Min</li><li>API Gateway</li></ul>
        </div>
        <div class="topic-card">
            <h3>&#127819; Architecture</h3>
            <ul><li>Data: Event Store</li><li>Elastic Stack</li><li>&rarr; Vector DB</li></ul>
        </div>
        <div class="topic-card">
            <h3>&#127826; Consolidation</h3>
            <ul><li>Modularize</li><li>Federate</li><li>Lakehouse</li></ul>
        </div>
    </div>
</section>

<!-- Projects -->
<section class="home-section">
    <h2 class="section-heading">Projects</h2>
    <div class="featured-links">
        <a href="pages/AI-Resilience-Architecture_203751428.html" class="featured-link">
            <span class="featured-emoji">&#128736;</span>
            <span class="featured-text">Potential Projects for Us to Vibe On</span>
        </a>
        <a href="https://www.lingualint.com" target="_blank" class="featured-link">
            <span class="featured-emoji">&#128300;</span>
            <span class="featured-text">LinguaLint (formerly Cortext.io) — LLM-middleware</span>
        </a>
        <a href="https://riskrunners.com" target="_blank" class="featured-link">
            <span class="featured-emoji">&#9888;&#65039;</span>
            <span class="featured-text">Wiki for Public Risk Factors</span>
        </a>
        <a href="https://plm.integralmass.com" target="_blank" class="featured-link">
            <span class="featured-emoji">&#127981;</span>
            <span class="featured-text">Integral Manufacturing and Shared Services (iMASS)</span>
        </a>
        <a href="pages/iMASS-and-Family-Resource-Mgmt_125206530.html" class="featured-link">
            <span class="featured-emoji">&#128106;</span>
            <span class="featured-text">iMASS and Family Resource Mgmt</span>
        </a>
        <a href="https://account.ninja" target="_blank" class="featured-link">
            <span class="featured-emoji">&#128176;</span>
            <span class="featured-text">Account Growth Simulator</span>
        </a>
        <a href="https://github.com/jeffy893/gurila.tools/tree/dev/2.0/use-cases/observability-ml-for-api" target="_blank" class="featured-link">
            <span class="featured-emoji">&#128065;</span>
            <span class="featured-text">Observability ML for API Service</span>
        </a>
        <a href="https://github.com/jeffy893/riskrunners/tree/dev/2.0/legacy/humanitarian-gambit" target="_blank" class="featured-link">
            <span class="featured-emoji">&#127758;</span>
            <span class="featured-text">Humanitarian Gambit</span>
        </a>
    </div>
</section>

<!-- Personal -->
<section class="home-section">
    <h2 class="section-heading">Personal</h2>
    <div class="featured-links">
        <a href="https://www.jefferson.cloud" target="_blank" class="featured-link">
            <span class="featured-emoji">&#9729;&#65039;</span>
            <span class="featured-text">jefferson.cloud — Socialize</span>
        </a>
        <a href="https://www.richards.systems" target="_blank" class="featured-link">
            <span class="featured-emoji">&#128421;</span>
            <span class="featured-text">richards.systems — Decode</span>
        </a>
        <a href="https://www.richards.plus" target="_blank" class="featured-link">
            <span class="featured-emoji">&#129309;</span>
            <span class="featured-text">richards.plus — Consult</span>
        </a>
        <a href="https://github.com/sponsors/jeffy893" target="_blank" class="featured-link">
            <span class="featured-emoji">&#10084;&#65039;</span>
            <span class="featured-text">Sponsor Jefferson to Keep Coding</span>
        </a>
        <a href="https://rizzcapture.com" target="_blank" class="featured-link">
            <span class="featured-emoji">&#127907;</span>
            <span class="featured-text">Marketing Methodology</span>
        </a>
        <a href="https://github.com/jeffy893" target="_blank" class="featured-link">
            <span class="featured-emoji">&#128187;</span>
            <span class="featured-text">Codebase (GitHub)</span>
        </a>
        <a href="https://street.riskrunners.com" target="_blank" class="featured-link">
            <span class="featured-emoji">&#128200;</span>
            <span class="featured-text">Street Math for UA RiskRunners</span>
        </a>
    </div>
</section>

<!-- Most Popular Pages -->
<section class="home-section">
    <h2 class="section-heading">&#128293; Most Viewed Pages</h2>
    <div class="popular-grid">
        <a href="pages/AI-Resilience-Architecture_203751428.html" class="popular-card">
            <span class="popular-views">69 views</span>
            <span class="popular-title">AI Resilience Architecture</span>
        </a>
        <a href="pages/Allegories_17760257.html" class="popular-card">
            <span class="popular-views">63 views</span>
            <span class="popular-title">Allegories</span>
        </a>
        <a href="pages/Lavender-Cucumber-Blueberry-Water_69926913.html" class="popular-card">
            <span class="popular-views">54 views</span>
            <span class="popular-title">Lavender-Cucumber-Blueberry Water</span>
        </a>
        <a href="pages/iMASS-and-Family-Resource-Mgmt_125206530.html" class="popular-card">
            <span class="popular-views">54 views</span>
            <span class="popular-title">iMASS and Family Resource Mgmt</span>
        </a>
        <a href="pages/9-Constraints-of-AI_91389954.html" class="popular-card">
            <span class="popular-views">44 views</span>
            <span class="popular-title">9 Constraints of AI</span>
        </a>
        <a href="pages/2014-Cosmos-Introduction_91488258.html" class="popular-card">
            <span class="popular-views">43 views</span>
            <span class="popular-title">2014 Cosmos Introduction</span>
        </a>
        <a href="pages/This-Ship-is-Built---Final-Reflection_112001110.html" class="popular-card">
            <span class="popular-views">39 views</span>
            <span class="popular-title">This Ship is Built - Final Reflection</span>
        </a>
        <a href="pages/The-Boxers-Strategy_17760371.html" class="popular-card">
            <span class="popular-views">37 views</span>
            <span class="popular-title">The Boxers Strategy</span>
        </a>
        <a href="pages/2024-10-01-Reverse-Conway-on-Richards-Systems_39616513.html" class="popular-card">
            <span class="popular-views">37 views</span>
            <span class="popular-title">Reverse Conway on Richards Systems</span>
        </a>
        <a href="pages/Quotas-took-our-jobs!_17760423.html" class="popular-card">
            <span class="popular-views">33 views</span>
            <span class="popular-title">Quotas took our jobs!</span>
        </a>
        <a href="pages/The-Great-Polished-Catamaran_17760341.html" class="popular-card">
            <span class="popular-views">28 views</span>
            <span class="popular-title">The Great Polished Catamaran</span>
        </a>
        <a href="pages/The-Grand-Arbiter_78675969.html" class="popular-card">
            <span class="popular-views">27 views</span>
            <span class="popular-title">The Grand Arbiter</span>
        </a>
        <a href="pages/Ambient-Gantt_152797206.html" class="popular-card">
            <span class="popular-views">27 views</span>
            <span class="popular-title">Ambient-Gantt</span>
        </a>
        <a href="pages/Account-Ninja_125206539.html" class="popular-card">
            <span class="popular-views">26 views</span>
            <span class="popular-title">Account Ninja</span>
        </a>
        <a href="pages/Digital-Icarus_33030147.html" class="popular-card">
            <span class="popular-views">25 views</span>
            <span class="popular-title">Digital Icarus</span>
        </a>
        <a href="pages/Cortext.io-Event-Report_17498151.html" class="popular-card">
            <span class="popular-views">25 views</span>
            <span class="popular-title">Cortext.io Event Report</span>
        </a>
    </div>
</section>'''
    return content

# ============================================
# Main build function
# ============================================

def build_all_pages():
    """Build all pages for the wiki site."""
    print("Building Richards Systems Wiki...")
    
    # Build flat list of all pages from nav tree
    all_pages = []
    def collect_pages(tree):
        for node in tree:
            all_pages.append(node)
            if "children" in node:
                collect_pages(node["children"])
    collect_pages(NAV_TREE)
    
    # Generate sidebar for home
    home_sidebar = render_nav_tree(NAV_TREE[0]["children"], "Richards-Systems_16679146.html")
    
    # Generate homepage
    home_content = generate_homepage()
    home_html = page_template(
        "Richards Systems",
        home_content,
        home_sidebar,
        '',
        is_home=True
    )
    (BASE_DIR / 'index.html').write_text(home_html)
    print(f"  Generated: index.html (homepage)")
    
    # Generate all sub-pages
    count = 0
    for page in all_pages:
        filename = page["file"]
        title = page["title"]
        
        # Skip the home page (already generated as index.html)
        if page.get("is_home"):
            continue
        
        # Skip pages with custom manual content
        slug = get_page_slug(filename)
        output_path = PAGES_DIR / f"{slug}.html"
        if filename in CUSTOM_PAGES and output_path.exists():
            count += 1
            continue
        
        # Generate sidebar with this page active
        sidebar = render_nav_tree(NAV_TREE[0]["children"], filename)
        
        # Generate breadcrumbs
        breadcrumbs = render_breadcrumbs(filename)
        
        # Determine content type and generate
        if filename in GDRIVE_LINKS:
            content = generate_gdrive_page(filename, title)
        elif filename in EXTERNAL_LINKS:
            content = generate_external_link_page(filename, title)
        elif filename in AMAZON_LINKS:
            content = generate_external_link_page(filename, title)
        else:
            content = generate_content_page(filename, title)
        
        # Generate full page
        slug = get_page_slug(filename)
        page_html = page_template(title, content, sidebar, breadcrumbs, is_home=False)
        
        output_path = PAGES_DIR / f"{slug}.html"
        output_path.write_text(page_html)
        count += 1
    
    print(f"  Generated: {count} sub-pages in pages/")
    print("Done!")


def build_search_index():
    """Generate a JSON search index of all pages for client-side search."""
    import json
    
    all_pages = []
    def collect_pages(tree, path_parts=None):
        if path_parts is None:
            path_parts = []
        for node in tree:
            filename = node["file"]
            title = node["title"]
            current_path = path_parts + [title]
            
            # Skip home
            if node.get("is_home"):
                if "children" in node:
                    collect_pages(node["children"], [])
                continue
            
            # Determine URL
            if filename in EXTERNAL_LINKS:
                url = EXTERNAL_LINKS[filename]
                is_external = True
            else:
                url = f"pages/{get_page_slug(filename)}.html"
                is_external = False
            
            # Get content snippet for search
            snippet = ""
            if not is_external and filename not in GDRIVE_LINKS and filename not in AMAZON_LINKS:
                filepath = RS_DIR / filename
                if filepath.exists():
                    raw = filepath.read_text(errors='replace')
                    # Extract text content
                    text_m = re.search(r'wiki-content group">(.*?)(?:</div>\s*\n|<div class="pageSection)', raw, re.DOTALL)
                    if text_m:
                        snippet = re.sub(r'<[^>]+>', ' ', text_m.group(1))
                        snippet = re.sub(r'\s+', ' ', snippet).strip()[:200]
            
            entry = {
                "title": title,
                "url": url,
                "path": " > ".join(current_path[:-1]) if len(current_path) > 1 else "",
                "snippet": snippet,
                "external": is_external
            }
            all_pages.append(entry)
            
            if "children" in node:
                collect_pages(node["children"], current_path)
    
    collect_pages(NAV_TREE)
    
    # Write search index
    index_path = BASE_DIR / 'assets' / 'search-index.json'
    index_path.write_text(json.dumps(all_pages, ensure_ascii=False))
    print(f"  Generated: search-index.json ({len(all_pages)} entries)")


if __name__ == "__main__":
    build_all_pages()
    build_search_index()
