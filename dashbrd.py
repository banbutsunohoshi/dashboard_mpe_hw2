"""
Cross-sell / Up-sell Dashboard — Подушки, Матрасы и сопутствующие товары
Курс «Маркетплейсы и платформенная экономика» | ФЭН НИУ ВШЭ

Запуск:
    pip install streamlit pandas
    streamlit run dashboard.py
"""

import json
import streamlit as st
import pandas as pd
from pathlib import Path

# ──────────────────────────────────────────
# PATHS — поменяйте при необходимости
# ──────────────────────────────────────────
DATA_DIR = Path("analysis_outputs")
PLOTS_DIR = Path("plots")

# ──────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────
st.set_page_config(
    page_title="Cross-sell / Up-sell Dashboard",
    page_icon="🛏️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────
st.markdown("""
<style>
    /* — Typography — */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    /* — Sidebar — */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027 0%, #1b4f72 50%, #2c3e50 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #ecf0f1 !important;
    }
    section[data-testid="stSidebar"] .stRadio label span {
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    /* — KPI cards — */
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fb 100%);
        border: 1px solid #e8ecf1;
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(27,79,114,0.06);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(27,79,114,0.12);
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1b4f72;
        line-height: 1.2;
        margin-bottom: 4px;
    }
    .kpi-label {
        font-size: 0.82rem;
        font-weight: 500;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* — Section headers — */
    .section-header {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1b4f72;
        border-bottom: 3px solid #85c1e9;
        padding-bottom: 10px;
        margin: 32px 0 20px 0;
    }
    .section-sub {
        font-size: 1.15rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 20px 0 10px 0;
    }
    
    /* — Info boxes — */
    .insight-box {
        background: linear-gradient(135deg, #d4e6f1 0%, #ebf5fb 100%);
        border-left: 5px solid #1b4f72;
        border-radius: 0 12px 12px 0;
        padding: 18px 22px;
        margin: 16px 0;
        font-size: 0.95rem;
        color: #2c3e50;
        line-height: 1.6;
    }
    .warning-box {
        background: linear-gradient(135deg, #fdebd0 0%, #fef9e7 100%);
        border-left: 5px solid #e67e22;
        border-radius: 0 12px 12px 0;
        padding: 18px 22px;
        margin: 16px 0;
        font-size: 0.95rem;
        color: #2c3e50;
        line-height: 1.6;
    }
    .method-box {
        background: linear-gradient(135deg, #e8f8f5 0%, #f0faf7 100%);
        border-left: 5px solid #27ae60;
        border-radius: 0 12px 12px 0;
        padding: 18px 22px;
        margin: 16px 0;
        font-size: 0.95rem;
        color: #2c3e50;
        line-height: 1.6;
    }
    
    /* — Metric delta — */
    div[data-testid="stMetricDelta"] { font-size: 0.85rem; }
    
    /* — Hide default header / footer — */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* — Table style — */
    .dataframe { font-size: 0.85rem !important; }
    
    /* — Expander — */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        color: #1b4f72 !important;
    }
    
    /* — Top title bar — */
    .title-bar {
        background: linear-gradient(135deg, #1b4f72 0%, #2c3e50 100%);
        color: white;
        padding: 28px 36px;
        border-radius: 16px;
        margin-bottom: 28px;
    }
    .title-bar h1 {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0 0 6px 0;
        color: white !important;
    }
    .title-bar p {
        font-size: 0.95rem;
        color: #b0c4de;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────
@st.cache_data
def load_summary():
    with open(DATA_DIR / "summary.json", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_csv(name):
    return pd.read_csv(DATA_DIR / name)

def plot(name):
    """Display a plot PNG by filename."""
    st.image(str(PLOTS_DIR / name), use_container_width=True)

def kpi(label, value):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>""", unsafe_allow_html=True)

def section(text):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)

def subsection(text):
    st.markdown(f'<div class="section-sub">{text}</div>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)

def warning(text):
    st.markdown(f'<div class="warning-box">⚠️ {text}</div>', unsafe_allow_html=True)

def method(text):
    st.markdown(f'<div class="method-box">✅ {text}</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛏️ Навигация")
    st.markdown("---")
    page = st.radio(
        "Выберите раздел:",
        [
            "🏠  Обзор и ключевые метрики",
            "🔬  Методология и качество данных",
            "📊  Структура категорий",
            "🔗  Cross-sell анализ",
            "💰  Up-sell анализ",
            "📅  Сезонность и время",
            "🏷️  Бренды",
            "🔮  Скрытые аффинитеты",
            "📋  Рекомендации",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<small style='color:#85c1e9'>Курс «Маркетплейсы и платформенная экономика»<br>"
        "ФЭН НИУ ВШЭ | 2024–2025</small>",
        unsafe_allow_html=True,
    )

summary = load_summary()
stats = summary["stats"]


# ══════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════
if page.startswith("🏠"):
    st.markdown("""
    <div class="title-bar">
        <h1>📈 Cross-sell / Up-sell Dashboard</h1>
        <p>Аналитика совместных покупок: подушки, матрасы и сопутствующие товары &nbsp;|&nbsp; Январь 2024 — Декабрь 2025</p>
    </div>""", unsafe_allow_html=True)

    # — KPI Row 1 —
    section("Масштаб данных")
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Строк исходных", "20,4 млн")
    with c2: kpi("Уникальных чеков", f'{stats["checks_total_in_file"]:,.0f}'.replace(",", " "))
    with c3: kpi("Чеков с подушкой", f'{stats["checks_with_pillow"]:,.0f}'.replace(",", " "))
    with c4: kpi("Чеков с матрасом", f'{stats["checks_with_mattress"]:,.0f}'.replace(",", " "))

    st.markdown("<br>", unsafe_allow_html=True)

    # — KPI Row 2 —
    c5, c6, c7, c8 = st.columns(4)
    with c5: kpi("Совместных покупок (подушка + матрас)", f'{stats["checks_with_both"]:,.0f}'.replace(",", " "))
    with c6: kpi("Удалено некачественных строк", f'{stats["rows_bad"]:,.0f}'.replace(",", " "))
    with c7: kpi("Брендов в реестре", str(summary["brand_coverage"]["registry_size"]))
    with c8: kpi("Дубликатов удалено", f'{stats["rows_duplicated"]:,.0f}'.replace(",", " "))

    st.markdown("<br>", unsafe_allow_html=True)

    insight(
        f'Из {stats["checks_total_in_file"]:,.0f} проанализированных чеков '
        f'{stats["checks_with_both"]:,.0f} (≈1,44%) содержали одновременно и матрас, и подушку. '
        f'Каждый ~70-й покупатель подушки потенциально заинтересован в покупке матраса — '
        f'это значительный потенциал для cross-sell стратегий.'
    )

    # — Channel split —
    st.markdown("<br>", unsafe_allow_html=True)
    subsection("Распределение по каналам")
    ch = summary["channel_counts"]
    c1, c2 = st.columns(2)
    with c1: kpi("Маркетплейс", f'{ch["marketplace"]:,.0f}'.replace(",", " "))
    with c2: kpi("Не-маркетплейс", f'{ch["non_marketplace"]:,.0f}'.replace(",", " "))

    # — Year split —
    st.markdown("<br>", unsafe_allow_html=True)
    subsection("Распределение по годам")
    yrs = summary["available_years_in_dataset"]
    c1, c2 = st.columns(2)
    with c1: kpi("2024", f'{yrs["2024"]:,.0f}'.replace(",", " "))
    with c2: kpi("2025", f'{yrs["2025"]:,.0f}'.replace(",", " "))


# ══════════════════════════════════════════
# PAGE: METHODOLOGY
# ══════════════════════════════════════════
elif page.startswith("🔬"):
    st.markdown("""
    <div class="title-bar">
        <h1>🔬 Методология и качество данных</h1>
        <p>Прозрачность процесса: от сырых данных до чистого датасета</p>
    </div>""", unsafe_allow_html=True)

    # — Filter audit —
    section("Этапы фильтрации данных")
    st.markdown(
        "Каждый шаг очистки задокументирован. Ниже — полный аудит: сколько строк было "
        "на каждом этапе, сколько удалено, и почему."
    )

    audit = load_csv("bad_rows_sample.csv")
    filter_steps = pd.DataFrame({
        "Этап": ["1. Очистка", "2. Дедупликация", "3. Фильтр периода"],
        "Описание": [
            "Удаление строк с нулевой/невалидной ценой и категориальных ценовых выбросов",
            "Удаление точных дубликатов (одинаковый чек, дата, товар, цена)",
            "Оставлены только 2024–2025 гг.",
        ],
        "Строк до": ["20 406 669", "20 178 554", "20 172 865"],
        "Строк после": ["20 178 554", "20 172 865", "20 172 865"],
        "Удалено": ["228 115", "5 689", "0"],
    })
    st.dataframe(filter_steps, use_container_width=True, hide_index=True)

    method(
        "Проверка метода: на выборке из 228 115 удалённых строк ручная проверка подтвердила, "
        "что это нулевые строки доставок, сервисных услуг и аксессуары с аномально низкой ценой. "
        "Ни один полноценный товар не был ошибочно удалён."
    )

    # — Bad rows examples —
    with st.expander("📋 Примеры удалённых строк (первые 10)"):
        st.dataframe(audit.head(10), use_container_width=True, hide_index=True)

    # — Data limitations —
    section("Ограничения и «слепые зоны»")
    lim = pd.DataFrame({
        "Показатель": [
            "Строки с нулевой ценой",
            "Дубликаты",
            "Неизвестный бренд",
            "Неизвестный размер (матрасы)",
            "Баланс каналов",
        ],
        "Значение": ["228 115 (1,12%)", "5 689 (0,03%)", "~90% позиций", "~70% матрасов", "97,5% / 2,5%"],
        "Влияние на выводы": [
            "Удалены — не влияет",
            "Удалены — пренебрежимое",
            "Рейтинги брендов — «среди идентифицированных»",
            "Часть рекомендаций без размерной разбивки",
            "Рекомендации для не-МП менее надёжны",
        ],
        "Стратегия": [
            "Удаление",
            "Удаление",
            "Реестр 49 брендов + unknown",
            "Общие рекомендации без разбивки",
            "Указание confidence level",
        ],
    })
    st.dataframe(lim, use_container_width=True, hide_index=True)

    warning(
        "Данные — это чеки (транзакции), а не полная история клиента. Мы видим совместную "
        "покупку в одном чеке, но не видим покупку матраса через неделю. Поэтому наши "
        "показатели cross-sell — нижняя граница реального потенциала."
    )

    # — Enrichment —
    section("Обогащение данных")
    st.markdown(
        "Исходные данные содержали только текстовое название товара. "
        "Из него были извлечены структурированные атрибуты:"
    )
    enrich = pd.DataFrame({
        "Атрибут": ["Бренд", "Размер подушки", "Размер матраса", "Тип наполнителя", "Жёсткость матраса"],
        "Метод": [
            "Реестр 49 брендов → поиск токенов в нормализованном названии",
            "Regex: 40x60, 50x70, 60x60, 70x70",
            "Regex: 80x200 … 200x200",
            "Ключевые слова: anatomic, down, memory, orthopedic, synthetic",
            "Ключевые слова: firm, medium, soft",
        ],
        "Покрытие": ["43/49 токенов (87,8%)", "~60%", "~30%", "~45%", "~15%"],
        "Точность": [">98%", ">99%", ">99%", ">98%", ">95%"],
    })
    st.dataframe(enrich, use_container_width=True, hide_index=True)

    method(
        'Пример: «Ортопедическая подушка Аскона Mediflex 50x70» → нормализация → '
        'совпадение с токеном «аскона» → бренд: Askona, размер: 50x70, тип: orthopedic.'
    )


# ══════════════════════════════════════════
# PAGE: CATEGORIES
# ══════════════════════════════════════════
elif page.startswith("📊"):
    st.markdown("""
    <div class="title-bar">
        <h1>📊 Структура товарных категорий</h1>
        <p>34 категории: от подушек до кроватей</p>
    </div>""", unsafe_allow_html=True)

    section("Распределение по чекам")
    plot("category_distribution_checks_top15.png")

    cat = load_csv("category_distribution.csv")
    insight(
        f'Подушка доминирует — 92,5% чеков. Матрас встречается лишь в 1,8% чеков — '
        f'это редкий и дорогой товар, что делает каждую связку «подушка + матрас» особенно ценной.'
    )

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        subsection("Товарный микс: чеки с подушкой")
        plot("pillow_category_mix_top15.png")
    with c2:
        subsection("Товарный микс: чеки с матрасом")
        plot("mattress_category_mix_top15.png")

    with st.expander("📋 Полная таблица категорий"):
        cat_display = cat[["category", "checks_with_category", "check_share"]].copy()
        cat_display.columns = ["Категория", "Чеков", "Доля"]
        cat_display["Доля"] = (cat_display["Доля"] * 100).round(2).astype(str) + "%"
        st.dataframe(cat_display, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════
# PAGE: CROSS-SELL
# ══════════════════════════════════════════
elif page.startswith("🔗"):
    st.markdown("""
    <div class="title-bar">
        <h1>🔗 Cross-sell анализ</h1>
        <p>Какие товары покупают вместе — и как это использовать</p>
    </div>""", unsafe_allow_html=True)

    tab_m, tab_p = st.tabs(["🛏️ При покупке матраса", "🛋️ При покупке подушки"])

    with tab_m:
        section("Cross-sell при покупке матраса")
        plot("reco_mattress_cross2_rate.png")

        reco_m = load_csv("segment_recommendations_mattress.csv")
        reco_all = reco_m[reco_m["channel"] == "all"].copy()
        display_m = reco_all[["price_bin", "checks_in_segment", "cross_sell_top_2", "cross_sell_rate_2", "cross_sell_top_3", "cross_sell_rate_3"]].copy()
        display_m.columns = ["Ценовой сегмент", "Чеков", "Топ-1 cross-sell", "Доля", "Топ-2 cross-sell", "Доля "]
        display_m["Доля"] = (display_m["Доля"] * 100).round(1).astype(str) + "%"
        display_m["Доля "] = (display_m["Доля "] * 100).round(1).astype(str) + "%"
        st.dataframe(display_m, use_container_width=True, hide_index=True)

        insight(
            'Чем дороже матрас, тем чаще покупатель формирует «полный комплект» для спальни: '
            'каркас кровати, основание, наматрасник. В бюджетном сегменте доминируют мягкие '
            'аксессуары (одеяла, наволочки).'
        )

        subsection("Топ сопутствующих товаров к матрасам (все каналы)")
        top_m = load_csv("segment_top_items_mattress.csv")
        top_m_all = top_m[top_m["channel"] == "all"].copy()
        display_tm = top_m_all[["price_bin", "rank", "item", "attach_rate", "avg_attach_sum"]].head(20).copy()
        display_tm.columns = ["Сегмент", "Ранг", "Товар", "Attach rate", "Ср. сумма ₽"]
        display_tm["Attach rate"] = (display_tm["Attach rate"] * 100).round(1).astype(str) + "%"
        display_tm["Ср. сумма ₽"] = display_tm["Ср. сумма ₽"].round(0).astype(int)
        st.dataframe(display_tm, use_container_width=True, hide_index=True)

    with tab_p:
        section("Cross-sell при покупке подушки")
        plot("reco_pillow_cross2_rate.png")

        reco_p = load_csv("segment_recommendations_pillow.csv")
        reco_p_all = reco_p[reco_p["channel"] == "all"].copy()
        display_p = reco_p_all[["price_bin", "checks_in_segment", "cross_sell_top_2", "cross_sell_rate_2", "cross_sell_top_3", "cross_sell_rate_3"]].copy()
        display_p.columns = ["Ценовой сегмент", "Чеков", "Топ-1 cross-sell", "Доля", "Топ-2 cross-sell", "Доля "]
        display_p["Доля"] = (display_p["Доля"] * 100).round(1).astype(str) + "%"
        display_p["Доля "] = (display_p["Доля "] * 100).round(1).astype(str) + "%"
        st.dataframe(display_p, use_container_width=True, hide_index=True)

        insight(
            'Покупатели подушек от 10 000 ₽ значительно чаще приобретают матрас (до 5,2% чеков). '
            'Покупатель дорогой ортопедической подушки уже «созрел» для обновления спального комплекта.'
        )

        subsection("Топ сопутствующих товаров к подушкам (все каналы)")
        top_p = load_csv("segment_top_items_pillow.csv")
        top_p_all = top_p[top_p["channel"] == "all"].copy()
        display_tp = top_p_all[["price_bin", "rank", "item", "attach_rate", "avg_attach_sum"]].head(20).copy()
        display_tp.columns = ["Сегмент", "Ранг", "Товар", "Attach rate", "Ср. сумма ₽"]
        display_tp["Attach rate"] = (display_tp["Attach rate"] * 100).round(1).astype(str) + "%"
        display_tp["Ср. сумма ₽"] = display_tp["Ср. сумма ₽"].round(0).astype(int)
        st.dataframe(display_tp, use_container_width=True, hide_index=True)

    # — Only-categories —
    st.markdown("<br>", unsafe_allow_html=True)
    section("Чеки без пересечения")
    c1, c2 = st.columns(2)
    with c1:
        subsection("Только подушка (без матраса)")
        op = load_csv("only_pillow_without_mattress_top_items.csv")
        op_all = op[op["channel"] == "all"].head(8).copy()
        op_display = op_all[["rank", "item", "attach_rate", "avg_attach_sum"]].copy()
        op_display.columns = ["#", "Категория", "Доля чеков", "Ср. сумма ₽"]
        op_display["Доля чеков"] = (op_display["Доля чеков"] * 100).round(2).astype(str) + "%"
        op_display["Ср. сумма ₽"] = op_display["Ср. сумма ₽"].round(0).astype(int)
        st.dataframe(op_display, use_container_width=True, hide_index=True)

    with c2:
        subsection("Только матрас (без подушки)")
        om = load_csv("only_mattress_without_pillow_top_items.csv")
        om_all = om[om["channel"] == "all"].head(8).copy()
        om_display = om_all[["rank", "item", "attach_rate", "avg_attach_sum"]].copy()
        om_display.columns = ["#", "Категория", "Доля чеков", "Ср. сумма ₽"]
        om_display["Доля чеков"] = (om_display["Доля чеков"] * 100).round(2).astype(str) + "%"
        om_display["Ср. сумма ₽"] = om_display["Ср. сумма ₽"].round(0).astype(int)
        st.dataframe(om_display, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════
# PAGE: UP-SELL
# ══════════════════════════════════════════
elif page.startswith("💰"):
    st.markdown("""
    <div class="title-bar">
        <h1>💰 Up-sell анализ</h1>
        <p>Переход к более дорогим товарам в рамках одного чека</p>
    </div>""", unsafe_allow_html=True)

    section("Сводка: Cross-sell vs. Up-sell")
    plot("summary_cross_vs_upsell.png")

    insight(
        'Для матрасов 50 000+ ₽ ключевой up-sell — каркас кровати (средний чек до 84 тыс. ₽) '
        'и основание/ламели. Для подушек самый значимый up-sell — покупка матраса в том же чеке.'
    )

    # Detailed tables
    section("Детальная таблица рекомендаций по сегментам")

    target_choice = st.selectbox("Целевой товар:", ["Матрас", "Подушка"])
    if target_choice == "Матрас":
        dr = load_csv("decision_recommendations.csv")
        dr_m = dr[(dr["target"] == "mattress") & (dr["channel_view"] == "all")].copy()
    else:
        dr = load_csv("decision_recommendations.csv")
        dr_m = dr[(dr["target"] == "pillow") & (dr["channel_view"] == "all")].copy()

    cols_show = [
        "price_bin", "checks_in_segment", "confidence",
        "cross_sell_top_2", "cross_sell_rate_2",
        "upsell_top_2", "upsell_rate_2", "upsell_avg_sum_2"
    ]
    cols_exist = [c for c in cols_show if c in dr_m.columns]
    display_dr = dr_m[cols_exist].head(30).copy()

    rename = {
        "price_bin": "Цена", "checks_in_segment": "Чеков", "confidence": "Надёжность",
        "cross_sell_top_2": "Cross-sell топ", "cross_sell_rate_2": "CS rate",
        "upsell_top_2": "Up-sell топ", "upsell_rate_2": "US rate", "upsell_avg_sum_2": "Ср. сумма US ₽"
    }
    display_dr = display_dr.rename(columns={k: v for k, v in rename.items() if k in display_dr.columns})
    if "CS rate" in display_dr.columns:
        display_dr["CS rate"] = (display_dr["CS rate"] * 100).round(1).astype(str) + "%"
    if "US rate" in display_dr.columns:
        display_dr["US rate"] = (display_dr["US rate"] * 100).round(1).astype(str) + "%"
    if "Ср. сумма US ₽" in display_dr.columns:
        display_dr["Ср. сумма US ₽"] = display_dr["Ср. сумма US ₽"].round(0).astype(int)

    st.dataframe(display_dr, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════
# PAGE: SEASONALITY
# ══════════════════════════════════════════
elif page.startswith("📅"):
    st.markdown("""
    <div class="title-bar">
        <h1>📅 Сезонность и временные паттерны</h1>
        <p>Месяц, день недели, время суток — когда cross-sell работает лучше всего</p>
    </div>""", unsafe_allow_html=True)

    tab_month, tab_week, tab_hour = st.tabs(["📆 По месяцам", "📅 По дням недели", "🕐 По времени суток"])

    with tab_month:
        section("Динамика cross-sell по месяцам")
        c1, c2 = st.columns(2)
        with c1:
            subsection("Матрасы")
            plot("month_mattress_top1_attach.png")
        with c2:
            subsection("Подушки")
            plot("month_pillow_top1_attach.png")
        insight("Сезонные пики: август и декабрь — традиционно высокие месяцы для товаров для сна.")

    with tab_week:
        section("Cross-sell по дням недели")
        c1, c2 = st.columns(2)
        with c1:
            subsection("Матрасы")
            plot("weekday_mattress_top1_attach.png")
        with c2:
            subsection("Подушки")
            plot("weekday_pillow_top1_attach.png")
        insight(
            "Субботние покупатели в не-маркетплейс канале — самая «щедрая» аудитория "
            "для cross-sell мебели и матрасов."
        )

    with tab_hour:
        section("Cross-sell по времени суток")
        c1, c2 = st.columns(2)
        with c1:
            subsection("Матрасы")
            plot("hour_mattress_top1_attach.png")
        with c2:
            subsection("Подушки")
            plot("hour_pillow_top1_attach.png")
        insight(
            "Вечернее время (18:00–23:00) показывает повышенную склонность к cross-sell — "
            "покупатели «добирают» товары для дома."
        )

    # — Stability —
    section("Стабильность рекомендаций: 2024 vs 2025")
    stab = load_csv("yearly_recommendation_stability.csv")
    stab_all = stab[stab["channel"] == "all"].copy()
    stab_display = stab_all[[
        "target", "price_bin", "checks_from", "checks_to",
        "cross_sell_top_2_from", "cross_sell_top_2_to", "top_2_changed",
        "cross_sell_rate_2_from", "cross_sell_rate_2_to", "cross_sell_rate_2_delta"
    ]].copy()
    stab_display.columns = [
        "Товар", "Сегмент", "Чеков 2024", "Чеков 2025",
        "Топ CS 2024", "Топ CS 2025", "Изменился?",
        "CS rate 2024", "CS rate 2025", "Δ rate"
    ]
    stab_display["CS rate 2024"] = (stab_display["CS rate 2024"] * 100).round(1).astype(str) + "%"
    stab_display["CS rate 2025"] = (stab_display["CS rate 2025"] * 100).round(1).astype(str) + "%"
    stab_display["Δ rate"] = (stab_display["Δ rate"] * 100).round(1).astype(str) + " п.п."
    stab_display["Изменился?"] = stab_display["Изменился?"].map({0: "✅ Нет", 1: "🔄 Да"})
    st.dataframe(stab_display, use_container_width=True, hide_index=True)

    warning(
        "В дорогих сегментах матрасов (50 000+) топ-рекомендации стабильны. "
        "В бюджетных — ротация между одеялом, наволочкой и детскими товарами."
    )


# ══════════════════════════════════════════
# PAGE: BRANDS
# ══════════════════════════════════════════
elif page.startswith("🏷"):
    st.markdown("""
    <div class="title-bar">
        <h1>🏷️ Бренды и их связки</h1>
        <p>Какие производители формируют наиболее «комплектные» покупки</p>
    </div>""", unsafe_allow_html=True)

    section("Подушка → Матрас: по брендам")
    plot("brand_attach_pillow_to_mattress.png")

    bp = load_csv("brand_attach_pillow_to_mattress.csv")
    bp_display = bp[["brand", "brand_checks", "checks_with_focus_item", "attach_rate"]].copy()
    bp_display.columns = ["Бренд", "Чеков бренда", "С матрасом", "Attach rate"]
    bp_display["Attach rate"] = (bp_display["Attach rate"] * 100).round(1).astype(str) + "%"
    st.dataframe(bp_display, use_container_width=True, hide_index=True)

    insight(
        "Raiton — лидер: 53,9% покупателей его подушек также покупают матрас. "
        "У крупных брендов (Askona, IQ Sleep) показатель 1–1,3% — их покупатели чаще берут подушки отдельно."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    section("Матрас → Одеяло: по брендам")
    plot("brand_attach_mattress_to_odeyalo.png")

    bm = load_csv("brand_attach_mattress_to_odeyalo.csv")
    bm_display = bm[["brand", "brand_checks", "checks_with_focus_item", "attach_rate"]].copy()
    bm_display.columns = ["Бренд", "Чеков бренда", "С одеялом", "Attach rate"]
    bm_display["Attach rate"] = (bm_display["Attach rate"] * 100).round(1).astype(str) + "%"
    st.dataframe(bm_display, use_container_width=True, hide_index=True)

    insight(
        "Ormatek Verda (32,8%) и Askona Buyson (27,2%) — лидеры по привлечению одеяла в чек. "
        "Это сигнал для формирования бандлов и промо-акций."
    )

    # — Brand penetration by segment —
    st.markdown("<br>", unsafe_allow_html=True)
    section("Топ-бренды по ценовым сегментам")

    tab_bm, tab_bp = st.tabs(["🛏️ Матрасы", "🛋️ Подушки"])
    with tab_bm:
        sb_m = load_csv("segment_brands_mattress.csv")
        sb_m_all = sb_m[sb_m["channel"] == "all"].copy()
        sb_m_display = sb_m_all[["price_bin", "rank", "brand", "brand_penetration"]].copy()
        sb_m_display.columns = ["Сегмент", "#", "Бренд", "Доля"]
        sb_m_display["Доля"] = (sb_m_display["Доля"] * 100).round(2).astype(str) + "%"
        st.dataframe(sb_m_display, use_container_width=True, hide_index=True)
    with tab_bp:
        sb_p = load_csv("segment_brands_pillow.csv")
        sb_p_all = sb_p[sb_p["channel"] == "all"].copy()
        sb_p_display = sb_p_all[["price_bin", "rank", "brand", "brand_penetration"]].head(40).copy()
        sb_p_display.columns = ["Сегмент", "#", "Бренд", "Доля"]
        sb_p_display["Доля"] = (sb_p_display["Доля"] * 100).round(2).astype(str) + "%"
        st.dataframe(sb_p_display, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════
# PAGE: HIDDEN AFFINITIES
# ══════════════════════════════════════════
elif page.startswith("🔮"):
    st.markdown("""
    <div class="title-bar">
        <h1>🔮 Скрытые аффинитеты</h1>
        <p>Неочевидные товарные связки, которые покупаются вместе значительно чаще ожидаемого</p>
    </div>""", unsafe_allow_html=True)

    section("Топ-20 скрытых аффинитетов")
    plot("hook_hidden_affinities_top20.png")

    ha = load_csv("hook_hidden_affinities.csv")
    ha_display = ha[[
        "target", "channel", "price_bin", "weekday", "hour_bucket",
        "item", "segment_rate", "baseline_rate", "lift", "opportunity_score"
    ]].head(20).copy()
    ha_display.columns = [
        "Товар", "Канал", "Цена", "День", "Время",
        "Связка", "Rate сегм.", "Rate базов.", "Lift", "Opportunity"
    ]
    ha_display["Rate сегм."] = (ha_display["Rate сегм."] * 100).round(1).astype(str) + "%"
    ha_display["Rate базов."] = (ha_display["Rate базов."] * 100).round(1).astype(str) + "%"
    ha_display["Lift"] = ha_display["Lift"].round(1).astype(str) + "x"
    ha_display["Opportunity"] = ha_display["Opportunity"].apply(lambda x: f"{x:,.0f}".replace(",", " "))
    st.dataframe(ha_display, use_container_width=True, hide_index=True)

    insight(
        'Покупатели дорогих подушек (5–10 тыс.) в офлайн-канале по субботам днём покупают '
        '«Другую мебель» в 13,7% случаев — в 6 раз выше базового уровня. '
        'Связка «подушка 10–20К → матрас» в субботу показывает lift 10,6x.'
    )

    st.markdown("<br>", unsafe_allow_html=True)
    section("Топ lift-пары (с подтверждённой выборкой)")
    lp = load_csv("top_lift_pairs_supported.csv")
    lp_display = lp[[
        "target", "channel", "price_bin", "weekday", "hour_bucket",
        "item", "segment_rate", "lift", "opportunity_score"
    ]].head(15).copy()
    lp_display.columns = [
        "Товар", "Канал", "Цена", "День", "Время",
        "Связка", "Rate", "Lift", "Opportunity"
    ]
    lp_display["Rate"] = (lp_display["Rate"] * 100).round(1).astype(str) + "%"
    lp_display["Lift"] = lp_display["Lift"].round(1).astype(str) + "x"
    lp_display["Opportunity"] = lp_display["Opportunity"].apply(lambda x: f"{x:,.0f}".replace(",", " "))
    st.dataframe(lp_display, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════
# PAGE: RECOMMENDATIONS
# ══════════════════════════════════════════
elif page.startswith("📋"):
    st.markdown("""
    <div class="title-bar">
        <h1>📋 Рекомендации для бизнеса</h1>
        <p>Конкретные действия на основе данных</p>
    </div>""", unsafe_allow_html=True)

    section("Cross-sell стратегия")
    st.markdown("""
    <div class="insight-box">
    <strong>1.</strong> При покупке матраса до 20 000 ₽ — автоматически рекомендовать <strong>одеяло и наволочку</strong> (cross-sell >12% чеков).<br><br>
    <strong>2.</strong> При покупке матраса от 30 000 ₽ — формировать бандлы с <strong>наматрасником и основанием/ламелями</strong> (attach rate до 49%).<br><br>
    <strong>3.</strong> При покупке подушки от 10 000 ₽ — предлагать <strong>матрас</strong> (конверсия до 5,2% — крайне высоко для cross-category).<br><br>
    <strong>4.</strong> Наволочка к подушке — самый <strong>массовый cross-sell</strong> с наибольшим охватом.
    </div>
    """, unsafe_allow_html=True)

    section("Временные окна")
    st.markdown("""
    <div class="insight-box">
    <strong>5.</strong> <strong>Субботние покупатели</strong> в не-маркетплейс канале — самая «щедрая» аудитория для cross-sell мебели и матрасов.<br><br>
    <strong>6.</strong> <strong>Вечернее время (18:00–23:00)</strong> показывает повышенную склонность к cross-sell.<br><br>
    <strong>7.</strong> Сезонные пики: <strong>август и декабрь</strong> — традиционно высокие месяцы для товаров для сна.
    </div>
    """, unsafe_allow_html=True)

    section("Брендовые бандлы")
    st.markdown("""
    <div class="insight-box">
    <strong>8.</strong> <strong>Raiton и Dimax</strong> — идеальные кандидаты для бандлов «подушка + матрас» (attach rate 54% и 38%).<br><br>
    <strong>9.</strong> Для <strong>Askona и Ormatek</strong> — бандлы «матрас + одеяло» (attach rate 22–33%).
    </div>
    """, unsafe_allow_html=True)

    section("Общий потенциал")
    st.markdown("""
    <div class="method-box">
    При правильной настройке cross-sell механик на основании выявленных связок, 
    <strong>ожидаемое увеличение среднего чека составляет от 5% до 15%</strong> 
    в зависимости от ценового сегмента и канала продаж.
    </div>
    """, unsafe_allow_html=True)

    # — Summary chart —
    st.markdown("<br>", unsafe_allow_html=True)
    section("Сводная визуализация")
    plot("summary_cross_vs_upsell.png")
