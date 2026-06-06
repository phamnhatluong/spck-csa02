"""
i18n.py — IndustryLens Translation Module
Supported: vi (Tiếng Việt) · en (English) · zh (中文) · ko (한국어)
"""

LANGUAGES = {
    "vi": {"name": "Tiếng Việt", "flag": "🇻🇳", "label": "🇻🇳 Tiếng Việt"},
    "en": {"name": "English",    "flag": "🇬🇧", "label": "🇬🇧 English"},
    "zh": {"name": "中文",        "flag": "🇨🇳", "label": "🇨🇳 中文"},
    "ko": {"name": "한국어",      "flag": "🇰🇷", "label": "🇰🇷 한국어"},
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ── App ──────────────────────────────────────────────────────────────────
    "app_badge":          {"vi":"🔬 AI-Powered Industry Intelligence","en":"🔬 AI-Powered Industry Intelligence","zh":"🔬 AI 驱动的行业洞察","ko":"🔬 AI 기반 산업 인텔리전스"},
    "app_version":        {"vi":"v2.0 · Phiên bản Streamlit","en":"v2.0 · Streamlit Edition","zh":"v2.0 · Streamlit 版本","ko":"v2.0 · Streamlit 버전"},
    # ── Hero ─────────────────────────────────────────────────────────────────
    "hero_title_line1":   {"vi":"Khám phá xu hướng","en":"Discover industry","zh":"探索行业","ko":"업계 트렌드를"},
    "hero_title_line2":   {"vi":"ngành nghề tương lai","en":"trends of the future","zh":"未来发展趋势","ko":"미래에서 발견하다"},
    "hero_sub":           {"vi":"Tải lên dữ liệu CSV / Excel của bạn → Nhận ngay phân tích xu hướng, dự báo tăng trưởng và chiến lược định hướng phát triển.","en":"Upload your CSV / Excel data → Get instant trend analysis, growth forecasts, and strategic development insights.","zh":"上传您的 CSV / Excel 数据 → 立即获取趋势分析、增长预测和战略发展建议。","ko":"CSV / Excel 데이터를 업로드하세요 → 즉각적인 트렌드 분석, 성장 예측 및 전략적 인사이트를 받으세요."},
    "hero_cta":           {"vi":"← Tải file CSV/Excel lên từ sidebar để bắt đầu","en":"← Upload a CSV/Excel file from the sidebar to get started","zh":"← 从侧边栏上传 CSV/Excel 文件开始使用","ko":"← 사이드바에서 CSV/Excel 파일을 업로드하여 시작하세요"},
    # ── Feature cards ────────────────────────────────────────────────────────
    "feat_trend_title":   {"vi":"Xác định xu hướng","en":"Identify Trends","zh":"识别趋势","ko":"트렌드 파악"},
    "feat_trend_desc":    {"vi":"Phát hiện quy luật tăng/giảm từ dữ liệu lịch sử","en":"Detect growth and decline patterns from historical data","zh":"从历史数据中发现增长和下降规律","ko":"과거 데이터에서 성장 및 하락 패턴 발견"},
    "feat_forecast_title":{"vi":"Dự báo tương lai","en":"Forecast the Future","zh":"预测未来","ko":"미래 예측"},
    "feat_forecast_desc": {"vi":"Dự đoán tuyển dụng & lương 6 tháng tới","en":"Predict hiring and salary for the next 6 months","zh":"预测未来6个月的招聘和薪资情况","ko":"향후 6개월 채용 및 급여 예측"},
    "feat_strategy_title":{"vi":"Đề xuất chiến lược","en":"Strategic Insights","zh":"战略建议","ko":"전략적 제언"},
    "feat_strategy_desc": {"vi":"Nhận định thực tế giúp định hướng phát triển","en":"Actionable insights to guide your development strategy","zh":"切实可行的见解，助力发展战略规划","ko":"개발 전략을 이끄는 실행 가능한 인사이트"},
    # ── Sidebar ───────────────────────────────────────────────────────────────
    "sidebar_language":   {"vi":"🌐 Ngôn ngữ","en":"🌐 Language","zh":"🌐 语言","ko":"🌐 언어"},
    "sidebar_theme":      {"vi":"🎨 Chủ đề màu sắc","en":"🎨 Color Theme","zh":"🎨 颜色主题","ko":"🎨 색상 테마"},
    "sidebar_custom_color":{"vi":"🖌️ Tuỳ chỉnh màu chính","en":"🖌️ Custom Primary Color","zh":"🖌️ 自定义主色","ko":"🖌️ 기본 색상 사용자 정의"},
    "sidebar_custom_color_label":{"vi":"Màu nhấn","en":"Accent color","zh":"强调色","ko":"강조 색상"},
    "sidebar_drive":      {"vi":"☁️ Dữ liệu mẫu (Google Drive)","en":"☁️ Sample Data (Google Drive)","zh":"☁️ 示例数据（Google Drive）","ko":"☁️ 샘플 데이터 (Google Drive)"},
    "sidebar_upload":     {"vi":"📂 Tải dữ liệu lên","en":"📂 Upload Data","zh":"📂 上传数据","ko":"📂 데이터 업로드"},
    "sidebar_public":     {"vi":"🌐 Báo cáo công khai","en":"🌐 Public Reports","zh":"🌐 公开报告","ko":"🌐 공개 보고서"},
    "sidebar_columns_hint":{"vi":"📋 Các cột được hỗ trợ","en":"📋 Supported columns","zh":"📋 支持的列","ko":"📋 지원되는 열"},
    "color_preview_main": {"vi":"Chính","en":"Main","zh":"主色","ko":"주색"},
    "color_preview_sub1": {"vi":"Phụ 1","en":"Sub 1","zh":"辅色 1","ko":"보조 1"},
    "color_preview_sub2": {"vi":"Phụ 2","en":"Sub 2","zh":"辅色 2","ko":"보조 2"},
    "color_preview_sub3": {"vi":"Phụ 3","en":"Sub 3","zh":"辅色 3","ko":"보조 3"},
    # ── Google Drive ─────────────────────────────────────────────────────────
    "drive_file_downloaded": {"vi":"Đã tải về","en":"Downloaded","zh":"已下载","ko":"다운로드됨"},
    "drive_file_not_downloaded":{"vi":"⬇️ File chưa được tải về máy","en":"⬇️ File not yet downloaded","zh":"⬇️ 文件尚未下载到本地","ko":"⬇️ 파일이 아직 다운로드되지 않음"},
    "btn_drive_download": {"vi":"⬇️ Tải từ Drive","en":"⬇️ Download from Drive","zh":"⬇️ 从 Drive 下载","ko":"⬇️ Drive에서 다운로드"},
    "btn_drive_refresh":  {"vi":"🔄 Cập nhật","en":"🔄 Refresh","zh":"🔄 刷新","ko":"🔄 새로고침"},
    "btn_drive_use":      {"vi":"📊 Dùng file mẫu từ Drive","en":"📊 Use Drive Sample File","zh":"📊 使用 Drive 示例文件","ko":"📊 Drive 샘플 파일 사용"},
    "drive_downloading":  {"vi":"Đang tải từ Google Drive...","en":"Downloading from Google Drive...","zh":"正在从 Google Drive 下载...","ko":"Google Drive에서 다운로드 중..."},
    "drive_refreshing":   {"vi":"Đang cập nhật...","en":"Refreshing...","zh":"正在刷新...","ko":"새로고침 중..."},
    "drive_analyzing":    {"vi":"Đang phân tích...","en":"Analyzing...","zh":"分析中...","ko":"분석 중..."},
    "drive_records_loaded":{"vi":"bản ghi từ Drive!","en":"records loaded from Drive!","zh":"条记录已从 Drive 加载！","ko":"개 레코드가 Drive에서 로드됨!"},
    "drive_not_configured":{"vi":"Chưa cấu hình Google Drive.<br>Thêm <code>GDRIVE_FILE_ID</code> vào file <code>.env</code> hoặc Streamlit Cloud <b>Secrets</b> để kích hoạt.","en":"Google Drive not configured.<br>Add <code>GDRIVE_FILE_ID</code> to your <code>.env</code> file or Streamlit Cloud <b>Secrets</b> to enable.","zh":"未配置 Google Drive。<br>请在 <code>.env</code> 文件或 Streamlit Cloud <b>Secrets</b> 中添加 <code>GDRIVE_FILE_ID</code>。","ko":"Google Drive가 구성되지 않았습니다.<br><code>.env</code> 파일 또는 Streamlit Cloud <b>Secrets</b>에 <code>GDRIVE_FILE_ID</code>를 추가하세요."},
    "drive_err_no_id":    {"vi":"⚠️ Chưa cấu hình GDRIVE_FILE_ID trong file .env","en":"⚠️ GDRIVE_FILE_ID not configured in .env file","zh":"⚠️ .env 文件中未配置 GDRIVE_FILE_ID","ko":"⚠️ .env 파일에 GDRIVE_FILE_ID가 구성되지 않음"},
    "drive_err_no_gdown": {"vi":"⚠️ Thư viện `gdown` chưa được cài. Chạy: `pip install gdown`","en":"⚠️ Library `gdown` not installed. Run: `pip install gdown`","zh":"⚠️ 库 `gdown` 未安装，请运行：`pip install gdown`","ko":"⚠️ `gdown` 라이브러리 미설치. 실행: `pip install gdown`"},
    "drive_success":      {"vi":"✅ Đã tải về","en":"✅ Downloaded","zh":"✅ 下载完成","ko":"✅ 다운로드 완료"},
    "drive_err_empty":    {"vi":"❌ File tải về rỗng hoặc bị lỗi","en":"❌ Downloaded file is empty or corrupted","zh":"❌ 下载的文件为空或已损坏","ko":"❌ 다운로드된 파일이 비어 있거나 손상됨"},
    "drive_err_generic":  {"vi":"❌ Lỗi khi tải","en":"❌ Download error","zh":"❌ 下载错误","ko":"❌ 다운로드 오류"},
    # ── Upload ────────────────────────────────────────────────────────────────
    "upload_name_label":  {"vi":"Tên của bạn (tuỳ chọn)","en":"Your name (optional)","zh":"您的姓名（可选）","ko":"이름 (선택사항)"},
    "upload_placeholder": {"vi":"Ẩn danh","en":"Anonymous","zh":"匿名","ko":"익명"},
    "upload_btn":         {"vi":"⚡ Phân tích ngay","en":"⚡ Analyze Now","zh":"⚡ 立即分析","ko":"⚡ 지금 분석"},
    "upload_spinner":     {"vi":"Đang phân tích dữ liệu...","en":"Analyzing data...","zh":"正在分析数据...","ko":"데이터 분석 중..."},
    "upload_success":     {"vi":"✅ Phân tích xong!","en":"✅ Analysis complete!","zh":"✅ 分析完成！","ko":"✅ 분석 완료!"},
    "upload_records":     {"vi":"bản ghi.","en":"records.","zh":"条记录。","ko":"개 레코드."},
    "upload_error":       {"vi":"❌ Lỗi","en":"❌ Error","zh":"❌ 错误","ko":"❌ 오류"},
    # ── Public reports ────────────────────────────────────────────────────────
    "public_select_placeholder":{"vi":"-- Chọn báo cáo --","en":"-- Select a report --","zh":"-- 选择报告 --","ko":"-- 보고서 선택 --"},
    "public_loaded":      {"vi":"📖 Đã tải báo cáo công khai!","en":"📖 Public report loaded!","zh":"📖 已加载公开报告！","ko":"📖 공개 보고서 로드됨!"},
    # ── Dashboard ─────────────────────────────────────────────────────────────
    "dashboard_records":  {"vi":"bản ghi","en":"records","zh":"条记录","ko":"개 레코드"},
    "dashboard_title":    {"vi":"Dashboard Phân Tích","en":"Analysis Dashboard","zh":"分析仪表板","ko":"분석 대시보드"},
    "btn_share_public":   {"vi":"🌐 Chia sẻ công khai","en":"🌐 Share Publicly","zh":"🌐 公开分享","ko":"🌐 공개 공유"},
    "published_success":  {"vi":"✅ Đã đăng công khai! ID:","en":"✅ Published publicly! ID:","zh":"✅ 已公开发布！ID：","ko":"✅ 공개 게시됨! ID:"},
    "btn_already_public": {"vi":"✅ Đã công khai rồi!","en":"✅ Already public!","zh":"✅ 已经公开！","ko":"✅ 이미 공개됨!"},
    "btn_download_json":  {"vi":"⬇️ Tải báo cáo JSON","en":"⬇️ Download JSON Report","zh":"⬇️ 下载 JSON 报告","ko":"⬇️ JSON 보고서 다운로드"},
    # ── KPIs ──────────────────────────────────────────────────────────────────
    "kpi_salary":         {"vi":"💼 Lương TB","en":"💼 Avg Salary","zh":"💼 平均薪资","ko":"💼 평균 급여"},
    "kpi_openings":       {"vi":"📋 Tổng tuyển dụng","en":"📋 Total Openings","zh":"📋 职位总数","ko":"📋 총 채용 수"},
    "kpi_growth":         {"vi":"🚀 Điểm tăng trưởng","en":"🚀 Growth Score","zh":"🚀 增长评分","ko":"🚀 성장 점수"},
    "kpi_salary_growth":  {"vi":"💹 Tăng lương","en":"💹 Salary Growth","zh":"💹 薪资增长","ko":"💹 급여 성장률"},
    "kpi_remote":         {"vi":"🌐 Remote TB","en":"🌐 Avg Remote","zh":"🌐 远程比例","ko":"🌐 평균 원격 비율"},
    # ── Tabs ──────────────────────────────────────────────────────────────────
    "tab_trends":         {"vi":"📈 Xu hướng","en":"📈 Trends","zh":"📈 趋势","ko":"📈 트렌드"},
    "tab_forecast":       {"vi":"🔮 Dự báo","en":"🔮 Forecast","zh":"🔮 预测","ko":"🔮 예측"},
    "tab_distribution":   {"vi":"📊 Phân phối","en":"📊 Distribution","zh":"📊 分布","ko":"📊 분포"},
    "tab_advanced":       {"vi":"🔬 Nâng cao","en":"🔬 Advanced","zh":"🔬 高级分析","ko":"🔬 고급 분석"},
    "tab_strategy":       {"vi":"💡 Chiến lược","en":"💡 Strategy","zh":"💡 战略","ko":"💡 전략"},
    "tab_data":           {"vi":"📋 Dữ liệu","en":"📋 Data","zh":"📋 数据","ko":"📋 데이터"},
    # ── Tab 1: Trends ─────────────────────────────────────────────────────────
    "trends_header":      {"vi":"📈 Xu hướng theo thời gian","en":"📈 Trends Over Time","zh":"📈 随时间变化的趋势","ko":"📈 시간에 따른 트렌드"},
    "trend_increasing":   {"vi":"tăng","en":"increasing","zh":"上升","ko":"증가"},
    "trend_decreasing":   {"vi":"giảm","en":"decreasing","zh":"下降","ko":"감소"},
    "trend_direction_msg":{"vi":"Xu hướng tuyển dụng đang","en":"Hiring trend is","zh":"招聘趋势正在","ko":"채용 트렌드가"},
    "trend_coefficient":  {"vi":"hệ số","en":"slope","zh":"斜率","ko":"기울기"},
    "trend_unit":         {"vi":"vị trí/ngày","en":"positions/day","zh":"职位/天","ko":"직위/일"},
    "chart_jobs_monthly": {"vi":"📋 Tuyển dụng theo tháng","en":"📋 Monthly Job Openings","zh":"📋 每月招聘职位","ko":"📋 월별 채용 공고"},
    "chart_salary_monthly":{"vi":"💰 Lương TB theo tháng","en":"💰 Monthly Average Salary","zh":"💰 月平均薪资","ko":"💰 월별 평균 급여"},
    "chart_growth_monthly":{"vi":"🚀 Điểm tăng trưởng theo tháng","en":"🚀 Monthly Growth Score","zh":"🚀 月度增长评分","ko":"🚀 월별 성장 점수"},
    "chart_dual_axis":    {"vi":"Tuyển dụng & Điểm tăng trưởng","en":"Openings & Growth Score","zh":"招聘数量与增长评分","ko":"채용 수 & 성장 점수"},
    "chart_dual_openings":{"vi":"Tuyển dụng","en":"Openings","zh":"招聘数","ko":"채용 수"},
    "no_jobs_date":       {"vi":"Cần cột `job_openings` và `date`","en":"Requires `job_openings` and `date` columns","zh":"需要 `job_openings` 和 `date` 列","ko":"`job_openings` 및 `date` 열이 필요합니다"},
    "no_salary_date":     {"vi":"Cần cột `avg_salary` và `date`","en":"Requires `avg_salary` and `date` columns","zh":"需要 `avg_salary` 和 `date` 列","ko":"`avg_salary` 및 `date` 열이 필요합니다"},
    # ── Tab 2: Forecast ───────────────────────────────────────────────────────
    "forecast_header":    {"vi":"🔮 Dự báo 6 tháng tới","en":"🔮 6-Month Forecast","zh":"🔮 未来6个月预测","ko":"🔮 6개월 예측"},
    "forecast_avg_growth":{"vi":"Điểm tăng trưởng trung bình","en":"Average Growth Score","zh":"平均增长评分","ko":"평균 성장 점수"},
    "forecast_std_dev":   {"vi":"Độ lệch chuẩn","en":"Std. deviation","zh":"标准差","ko":"표준 편차"},
    "forecast_outlook":   {"vi":"Triển vọng","en":"Outlook","zh":"展望","ko":"전망"},
    "outlook_positive":   {"vi":"Tích cực 🟢","en":"Positive 🟢","zh":"乐观 🟢","ko":"긍정적 🟢"},
    "outlook_neutral":    {"vi":"Trung bình 🟡","en":"Neutral 🟡","zh":"一般 🟡","ko":"보통 🟡"},
    "outlook_caution":    {"vi":"Thận trọng 🔴","en":"Caution 🔴","zh":"谨慎 🔴","ko":"주의 🔴"},
    "chart_forecast_jobs":{"vi":"📋 Dự báo tuyển dụng 6 tháng tới","en":"📋 Job Openings Forecast — Next 6 Months","zh":"📋 未来6个月招聘预测","ko":"📋 향후 6개월 채용 예측"},
    "chart_forecast_salary":{"vi":"💰 Dự báo lương 6 tháng tới","en":"💰 Salary Forecast — Next 6 Months","zh":"💰 未来6个月薪资预测","ko":"💰 향후 6개월 급여 예측"},
    "forecast_col_month": {"vi":"Tháng","en":"Month","zh":"月份","ko":"월"},
    "forecast_col_openings":{"vi":"Dự báo tuyển dụng","en":"Forecasted Openings","zh":"预测招聘数","ko":"예측 채용 수"},
    "forecast_col_salary":{"vi":"Lương dự báo","en":"Forecasted Salary","zh":"预测薪资","ko":"예측 급여"},
    "no_forecast_jobs":   {"vi":"Cần ít nhất 4 tháng dữ liệu để dự báo tuyển dụng.","en":"Need at least 4 months of data to forecast job openings.","zh":"需要至少4个月的数据才能预测招聘情况。","ko":"채용 예측을 위해 최소 4개월의 데이터가 필요합니다."},
    "no_forecast_salary": {"vi":"Cần cột `avg_salary` và `salary_growth_rate` để dự báo lương.","en":"Need `avg_salary` and `salary_growth_rate` columns to forecast salary.","zh":"需要 `avg_salary` 和 `salary_growth_rate` 列才能预测薪资。","ko":"급여 예측을 위해 `avg_salary` 및 `salary_growth_rate` 열이 필요합니다."},
    # ── Tab 3: Distribution ───────────────────────────────────────────────────
    "dist_header":        {"vi":"📊 Phân phối & thống kê","en":"📊 Distribution & Statistics","zh":"📊 分布与统计","ko":"📊 분포 및 통계"},
    "chart_exp_level":    {"vi":"👥 Cấp độ kinh nghiệm","en":"👥 Experience Level","zh":"👥 经验水平","ko":"👥 경험 수준"},
    "chart_competition":  {"vi":"⚔️ Mức cạnh tranh","en":"⚔️ Competition Level","zh":"⚔️ 竞争程度","ko":"⚔️ 경쟁 수준"},
    "chart_auto_risk":    {"vi":"🤖 Rủi ro AI thay thế","en":"🤖 Automation Risk","zh":"🤖 自动化风险","ko":"🤖 자동화 위험"},
    "chart_top_jobs":     {"vi":"💼 Top vị trí lương cao nhất","en":"💼 Top Highest-Paying Roles","zh":"💼 薪资最高的职位","ko":"💼 최고 급여 직무 TOP"},
    "chart_top_skills":   {"vi":"🛠️ Kỹ năng được yêu cầu nhiều nhất","en":"🛠️ Most In-Demand Skills","zh":"🛠️ 最需求的技能","ko":"🛠️ 가장 수요가 많은 스킬"},
    "chart_jobs_region":  {"vi":"🗺️ Tuyển dụng theo khu vực","en":"🗺️ Openings by Region","zh":"🗺️ 各地区招聘数量","ko":"🗺️ 지역별 채용 수"},
    "chart_demand_dist":  {"vi":"📡 Phân bố nhu cầu dự báo","en":"📡 Demand Forecast Distribution","zh":"📡 需求预测分布","ko":"📡 수요 예측 분포"},
    "remote_avg_label":   {"vi":"REMOTE RATIO TRUNG BÌNH","en":"AVERAGE REMOTE RATIO","zh":"平均远程比例","ko":"평균 원격 비율"},
    "chart_remote_dist":  {"vi":"🌐 Phân bố tỷ lệ làm việc từ xa","en":"🌐 Remote Work Ratio Distribution","zh":"🌐 远程工作比例分布","ko":"🌐 원격 근무 비율 분포"},
    # ── Tab 4: Advanced ───────────────────────────────────────────────────────
    "advanced_header":    {"vi":"🔬 Phân tích nâng cao","en":"🔬 Advanced Analysis","zh":"🔬 高级分析","ko":"🔬 고급 분석"},
    "chart_scatter":      {"vi":"💹 Tương quan Lương & Điểm tăng trưởng","en":"💹 Salary vs. Growth Score Correlation","zh":"💹 薪资与增长评分相关性","ko":"💹 급여 & 성장 점수 상관관계"},
    "chart_salary_box":   {"vi":"📦 Phân phối lương theo cấp độ","en":"📦 Salary Distribution by Level","zh":"📦 各级别薪资分布","ko":"📦 수준별 급여 분포"},
    "chart_salary_hist":  {"vi":"📊 Phân phối lương","en":"📊 Salary Distribution","zh":"📊 薪资分布","ko":"📊 급여 분포"},
    "chart_heatmap":      {"vi":"Ma trận tương quan","en":"Correlation Matrix","zh":"相关性矩阵","ko":"상관관계 행렬"},
    "heatmap_salary":     {"vi":"Lương TB","en":"Avg Salary","zh":"平均薪资","ko":"평균 급여"},
    "heatmap_openings":   {"vi":"Tuyển dụng","en":"Openings","zh":"招聘数","ko":"채용 수"},
    "heatmap_growth":     {"vi":"Tăng trưởng","en":"Growth","zh":"增长","ko":"성장"},
    "heatmap_sal_growth": {"vi":"Tăng lương %","en":"Salary Growth %","zh":"薪资增长%","ko":"급여 성장률%"},
    "heatmap_remote":     {"vi":"Remote %","en":"Remote %","zh":"远程%","ko":"원격%"},
    "chart_salary_region":{"vi":"🗺️ Lương trung bình theo khu vực","en":"🗺️ Average Salary by Region","zh":"🗺️ 各地区平均薪资","ko":"🗺️ 지역별 평균 급여"},
    "salary_region_x":    {"vi":"Khu vực","en":"Region","zh":"地区","ko":"지역"},
    "salary_region_y":    {"vi":"Lương TB ($)","en":"Avg Salary ($)","zh":"平均薪资（$）","ko":"평균 급여 ($)"},
    "chart_salary_growth_t":{"vi":"📈 Tốc độ tăng lương theo tháng (%)","en":"📈 Monthly Salary Growth Rate (%)","zh":"📈 月度薪资增长率（%）","ko":"📈 월별 급여 성장률 (%)"},
    "scatter_salary_x":   {"vi":"Lương TB ($)","en":"Avg Salary ($)","zh":"平均薪资（$）","ko":"평균 급여 ($)"},
    "scatter_growth_y":   {"vi":"Điểm tăng trưởng","en":"Growth Score","zh":"增长评分","ko":"성장 점수"},
    "no_scatter":         {"vi":"Cần cột `avg_salary` và `growth_score`.","en":"Requires `avg_salary` and `growth_score` columns.","zh":"需要 `avg_salary` 和 `growth_score` 列。","ko":"`avg_salary` 및 `growth_score` 열이 필요합니다."},
    "no_salary_col":      {"vi":"Cần cột `avg_salary`.","en":"Requires `avg_salary` column.","zh":"需要 `avg_salary` 列。","ko":"`avg_salary` 열이 필요합니다."},
    "no_advanced_raw":    {"vi":"📁 Tải file dữ liệu lên để xem phân tích nâng cao.","en":"📁 Upload a data file to view advanced analysis.","zh":"📁 请上传数据文件以查看高级分析。","ko":"📁 고급 분석을 보려면 데이터 파일을 업로드하세요."},
    # ── Tab 5: Strategy ───────────────────────────────────────────────────────
    "strategy_header":    {"vi":"💡 Nhận định & đề xuất chiến lược","en":"💡 Insights & Strategic Recommendations","zh":"💡 洞察与战略建议","ko":"💡 인사이트 및 전략적 권고사항"},
    "no_insights":        {"vi":"Không đủ dữ liệu để tạo nhận định.","en":"Not enough data to generate insights.","zh":"数据不足，无法生成洞察。","ko":"인사이트를 생성하기에 데이터가 부족합니다."},
    "summary_header":     {"vi":"📌 Tóm tắt thông tin ngành","en":"📌 Industry Summary","zh":"📌 行业信息摘要","ko":"📌 산업 요약 정보"},
    "tag_industry":       {"vi":"NGÀNH","en":"INDUSTRY","zh":"行业","ko":"산업"},
    "tag_region":         {"vi":"KHU VỰC","en":"REGION","zh":"地区","ko":"지역"},
    "tag_job_title":      {"vi":"VỊ TRÍ CÔNG VIỆC","en":"JOB TITLES","zh":"职位名称","ko":"직무 명칭"},
    "tag_others":         {"vi":"khác","en":"more","zh":"更多","ko":"더보기"},
    # ── Tab 6: Data ───────────────────────────────────────────────────────────
    "data_header":        {"vi":"📋 Dữ liệu thô","en":"📋 Raw Data","zh":"📋 原始数据","ko":"📋 원시 데이터"},
    "filter_industry":    {"vi":"Lọc ngành","en":"Filter by industry","zh":"按行业筛选","ko":"산업별 필터"},
    "filter_region":      {"vi":"Lọc khu vực","en":"Filter by region","zh":"按地区筛选","ko":"지역별 필터"},
    "filter_exp":         {"vi":"Lọc cấp độ","en":"Filter by level","zh":"按级别筛选","ko":"수준별 필터"},
    "data_showing":       {"vi":"Hiển thị","en":"Showing","zh":"显示","ko":"표시 중"},
    "data_of":            {"vi":"/","en":"of","zh":"/","ko":"/"},
    "data_records":       {"vi":"bản ghi","en":"records","zh":"条记录","ko":"개 레코드"},
    "btn_download_csv":   {"vi":"⬇️ Tải CSV đã lọc","en":"⬇️ Download Filtered CSV","zh":"⬇️ 下载筛选后的 CSV","ko":"⬇️ 필터링된 CSV 다운로드"},
    "no_raw_data":        {"vi":"📁 Dữ liệu thô không khả dụng với báo cáo công khai. Hãy upload file mới.","en":"📁 Raw data is not available for public reports. Please upload a new file.","zh":"📁 公开报告不提供原始数据，请上传新文件。","ko":"📁 공개 보고서에는 원시 데이터를 사용할 수 없습니다. 새 파일을 업로드하세요."},
    # ── Insights ──────────────────────────────────────────────────────────────
    "insight_auto_high_title":{"vi":"Rủi ro tự động hóa cao","en":"High Automation Risk","zh":"自动化风险较高","ko":"자동화 위험 높음"},
    "insight_auto_high_desc": {"vi":"% vị trí có nguy cơ bị AI thay thế. Nên đầu tư vào kỹ năng sáng tạo & quản lý.","en":"% of positions at risk of AI replacement. Invest in creative and management skills.","zh":"%的职位面临被AI取代的风险，建议投资创意和管理技能。","ko":"%의 직위가 AI 대체 위험에 처해 있습니다. 창의적 및 관리 역량에 투자하세요."},
    "insight_auto_low_title": {"vi":"Ngành an toàn trước AI","en":"Industry Safe from AI","zh":"行业抵御AI风险能力强","ko":"AI로부터 안전한 산업"},
    "insight_auto_low_desc":  {"vi":"Chỉ % rủi ro cao — ngành này còn nhiều dư địa phát triển.","en":"Only % high risk — this industry still has plenty of room to grow.","zh":"仅%的高风险职位，该行业仍有很大发展空间。","ko":"%만 고위험 — 이 산업은 여전히 성장 여지가 충분합니다."},
    "insight_remote_high_title":{"vi":"Xu hướng Remote mạnh","en":"Strong Remote Work Trend","zh":"远程工作趋势强劲","ko":"강한 원격 근무 트렌드"},
    "insight_remote_high_desc":{"vi":"Tỷ lệ remote TB %. Cơ hội tuyển dụng toàn cầu.","en":"Average remote ratio %. Global hiring opportunities are expanding.","zh":"平均远程比例%，全球招聘机会正在扩大。","ko":"평균 원격 비율%. 글로벌 채용 기회가 확대되고 있습니다."},
    "insight_remote_low_title":{"vi":"Văn hóa làm việc trực tiếp","en":"On-Site Work Culture","zh":"线下工作文化","ko":"현장 근무 문화"},
    "insight_remote_low_desc": {"vi":"Remote chỉ %. Ngành yêu cầu hiện diện thực tế cao.","en":"Remote only %. Industry requires strong in-person presence.","zh":"远程仅%，该行业对现场办公要求较高。","ko":"원격 근무 %. 업계는 강한 현장 출근을 요구합니다."},
    "insight_growth_high_title":{"vi":"Ngành tăng trưởng mạnh","en":"Strong Industry Growth","zh":"行业增长强劲","ko":"강력한 산업 성장"},
    "insight_growth_high_desc": {"vi":"Điểm tăng trưởng TB /100 — thời điểm vàng để đầu tư nhân lực.","en":"Average growth score /100 — golden moment to invest in talent.","zh":"平均增长评分/100，现在是投资人才的黄金时机。","ko":"평균 성장 점수/100 — 인재에 투자할 황금 기회입니다."},
    "insight_growth_low_title": {"vi":"Tăng trưởng chậm","en":"Slow Growth","zh":"增长缓慢","ko":"성장 둔화"},
    "insight_growth_low_desc":  {"vi":"Điểm /100. Cân nhắc chiến lược đa dạng hóa.","en":"Score /100. Consider diversification strategies.","zh":"评分/100，建议考虑多元化战略。","ko":"점수/100. 다각화 전략을 고려하세요."},
    "insight_sal_exc_title":    {"vi":"Lương tăng trưởng xuất sắc","en":"Excellent Salary Growth","zh":"薪资增长出色","ko":"우수한 급여 성장"},
    "insight_sal_exc_desc":     {"vi":"TB %/năm — ngành hấp dẫn nhân tài hàng đầu.","en":"Avg %/year — top talent magnet industry.","zh":"平均%/年，该行业对顶尖人才极具吸引力。","ko":"평균%/년 — 최고 인재를 끌어들이는 산업입니다."},
    "insight_sal_ok_title":     {"vi":"Lương tăng ổn định","en":"Steady Salary Growth","zh":"薪资增长稳定","ko":"안정적인 급여 성장"},
    "insight_sal_ok_desc":      {"vi":"TB %/năm — duy trì sức hút với ứng viên tốt.","en":"Avg %/year — maintaining appeal for quality candidates.","zh":"平均%/年，对优质候选人保持吸引力。","ko":"평균%/년 — 우수 지원자에게 매력을 유지합니다."},
    "insight_comp_high_title":  {"vi":"Cạnh tranh gay gắt","en":"High Competition","zh":"竞争激烈","ko":"치열한 경쟁"},
    "insight_comp_high_desc":   {"vi":"% vị trí cạnh tranh cao. Cần xây dựng employer brand mạnh.","en":"% of positions are highly competitive. Build a strong employer brand.","zh":"%的职位竞争激烈，需要打造强大的雇主品牌。","ko":"%의 직위가 경쟁이 치열합니다. 강한 고용주 브랜드를 구축하세요."},
}


def t(key: str, lang: str = "vi") -> str:
    """Get translation for key in given language; fallback vi → key."""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    return entry.get(lang) or entry.get("vi") or key


def tmap(keys: list, lang: str = "vi") -> list:
    """Translate a list of keys."""
    return [t(k, lang) for k in keys]

# ── Additional keys (auto-added) ─────────────────────────────────────────────
_EXTRA = {
    "app_subtitle":       {"vi":"v2.0 · Phiên bản Streamlit","en":"v2.0 · Streamlit Edition","zh":"v2.0 · Streamlit 版本","ko":"v2.0 · Streamlit 버전"},
    "sidebar_gdrive":     {"vi":"☁️ Dữ liệu mẫu (Google Drive)","en":"☁️ Sample Data (Google Drive)","zh":"☁️ 示例数据（Google Drive）","ko":"☁️ 샘플 데이터 (Google Drive)"},
    "sidebar_color_label":{"vi":"Màu nhấn","en":"Accent color","zh":"强调色","ko":"강조 색상"},
    "color_main":         {"vi":"Chính","en":"Main","zh":"主色","ko":"주색"},
    "color_sub1":         {"vi":"Phụ 1","en":"Sub 1","zh":"辅色 1","ko":"보조 1"},
    "color_sub2":         {"vi":"Phụ 2","en":"Sub 2","zh":"辅色 2","ko":"보조 2"},
    "color_sub3":         {"vi":"Phụ 3","en":"Sub 3","zh":"辅色 3","ko":"보조 3"},
    "chart_salary_dist":  {"vi":"📦 Phân phối lương theo cấp độ","en":"📦 Salary Distribution by Level","zh":"📦 各级别薪资分布","ko":"📦 수준별 급여 분포"},
    "chart_corr_heatmap": {"vi":"Ma trận tương quan","en":"Correlation Matrix","zh":"相关性矩阵","ko":"상관관계 행렬"},
    "scatter_x_label":    {"vi":"Lương TB ($)","en":"Avg Salary ($)","zh":"平均薪资（$）","ko":"평균 급여 ($)"},
    "scatter_y_label":    {"vi":"Điểm tăng trưởng","en":"Growth Score","zh":"增长评分","ko":"성장 점수"},
    "drive_downloaded":   {"vi":"Đã tải về","en":"Downloaded","zh":"已下载","ko":"다운로드됨"},
    "drive_not_downloaded":{"vi":"⬇️ File chưa được tải về máy","en":"⬇️ File not yet downloaded","zh":"⬇️ 文件尚未下载到本地","ko":"⬇️ 파일이 아직 다운로드되지 않음"},
    "drive_btn_download": {"vi":"⬇️ Tải từ Drive","en":"⬇️ Download from Drive","zh":"⬇️ 从 Drive 下载","ko":"⬇️ Drive에서 다운로드"},
    "drive_btn_refresh":  {"vi":"🔄 Cập nhật","en":"🔄 Refresh","zh":"🔄 刷新","ko":"🔄 새로고침"},
    "drive_btn_use":      {"vi":"📊 Dùng file mẫu từ Drive","en":"📊 Use Drive Sample File","zh":"📊 使用 Drive 示例文件","ko":"📊 Drive 샘플 파일 사용"},
    "drive_updating":     {"vi":"Đang cập nhật...","en":"Refreshing...","zh":"正在刷新...","ko":"새로고침 중..."},
}
TRANSLATIONS.update(_EXTRA)
