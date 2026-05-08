/**
 * Tomchi Tech — i18n (Internationalization)
 * ==========================================
 * Qo'llab-quvvatlanadigan tillar: uz (asosiy), ru, en
 *
 * Ishlatish (har bir sahifada):
 *   <script src="js/i18n.js"></script>   (head yoki body oxirida)
 *   applyI18n();                          (script oxirida chaqiring)
 *
 * Til o'zgartirish:
 *   localStorage.setItem('lang', 'ru');
 *   applyI18n();
 *
 * Yoki: setLang('en');  // saqlaydi + tatbiq qiladi
 *
 * Arxitektura:
 *   - HTML ga data-i18n qo'shish shart emas.
 *   - Text-node walker barcha ko'rinadigan matni topa oladi.
 *   - O'zbek matni → Rus/Ingliz matni almashtirish prinsipi.
 */

/* ── Supported languages ─────────────────────────────────────── */
const I18N_LANGS = {
  uz: { label: "O'zbek",  flag: '🇺🇿', dir: 'ltr' },
  ru: { label: 'Русский', flag: '🇷🇺', dir: 'ltr' },
  en: { label: 'English', flag: '🇬🇧', dir: 'ltr' },
};

/* ── Translation map (UZ → RU / EN) ─────────────────────────── */
const I18N = {

  ru: {
    /* ─── Navigation ─────────────────────────────────────────── */
    'Dashboard':           'Дашборд',
    'Sensorlar':           'Датчики',
    'Fermalar':            'Фермы',
    'Tavsiyalar':          'Рекомендации',
    'Alertlar':            'Оповещения',
    'Hisobotlar':          'Отчёты',
    'Mijozlar':            'Клиенты',
    'Sozlamalar':          'Настройки',
    'Yordam':              'Помощь',
    'Tezkor kirish':       'Быстрый доступ',
    "Sensorlar ro'yxati":  'Список датчиков',

    /* ─── Page subtitles ─────────────────────────────────────── */
    '— barcha sensorlar monitoringi': '— мониторинг всех датчиков',
    '— ferma xaritasi va sensorlar':  '— карта фермы и датчики',
    '— sensor ma\'lumotlari':         '— данные датчиков',

    /* ─── Buttons ────────────────────────────────────────────── */
    'Yangilash':              'Обновить',
    'Yangi ferma':            'Новая ферма',
    'Yangi sensor':           'Новый датчик',
    'Yangi mijoz':            'Новый клиент',
    'Chop etish':             'Распечатать',
    'CSV yuklab olish':       'Скачать CSV',
    "Qo'shish":               'Добавить',
    'Saqlash':                'Сохранить',
    'Bekor qilish':           'Отмена',
    "O'chirish":              'Удалить',
    'Tahrirlash':             'Редактировать',
    'Ko\'rish':               'Просмотр',
    'Tasdiqla':               'Подтвердить',
    'Yuborish':               'Отправить',
    'Ulanishni tekshir':      'Проверить соединение',
    'Hammasini saqlash':      'Сохранить всё',
    'Test yuborish':          'Отправить тест',
    'Konfigni eksport qilish':'Экспорт конфига',
    'Konfigni import qilish': 'Импорт конфига',
    "Ko'rish va tahrirlash":  'Просмотр и редактирование',

    /* ─── Table headers ──────────────────────────────────────── */
    'Sensor':                 'Датчик',
    'Ferma':                  'Ферма',
    'Ekin':                   'Культура',
    'Namlik':                 'Влажность',
    'Temperatura':            'Температура',
    'Batareya':               'Батарея',
    'Status':                 'Статус',
    'Amallar':                'Действия',
    'Joylashuv':              'Расположение',
    "So'nggi o'qish":         'Последнее чтение',
    'Tavsiya':                'Рекомендация',
    'Kerak suv (L)':          'Нужно воды (Л)',
    "An'anaviy (L)":          'Традиционный (Л)',
    'Tejash':                 'Экономия',
    'Mijoz':                  'Клиент',
    'Obuna':                  'Подписка',
    'Ferma soni':             'Кол-во ферм',
    'Telefon':                'Телефон',
    'Sana':                   'Дата',
    'Sabab':                  'Причина',
    'Xabar':                  'Сообщение',
    'Daraja':                 'Уровень',
    'Vaqt':                   'Время',

    /* ─── Status badges ──────────────────────────────────────── */
    'Onlayn':      'Онлайн',
    'Oflayn':      'Офлайн',
    'Diqqat':      'Внимание',
    'Kritik':      'Критический',
    'Xato':        'Ошибка',
    'Normal':      'Норма',
    'Faol':        'Активен',
    'Nofaol':      'Неактивен',
    'Test rejim':  'Тестовый режим',
    'Ulangan':     'Подключён',
    'Sozlanmagan': 'Не настроен',

    /* ─── Metric cards ───────────────────────────────────────── */
    'Aktiv sensorlar':            'Активных датчиков',
    "O'rtacha namlik":            'Средняя влажность',
    'Aktiv alertlar':             'Активных оповещений',
    'Aktiv tavsiyalar':           'Активных рекомендаций',
    "Jami suv tejalgan":          'Сэкономлено воды всего',
    "O'rtacha tejash":            'Средняя экономия',
    'Jami alertlar':              'Всего оповещений',
    "Sug'orish tavsiyalari":      'Рекомендации по орошению',
    "an'anaviy usulga nisbatan":  'относительно традиционного',
    'barcha tavsiyalar bo\'yicha':'по всем рекомендациям',
    'bugungi kunda':              'на сегодня',
    'aktiv tavsiyalar':           'активных рекомендаций',

    /* ─── Irrigation actions ─────────────────────────────────── */
    "Zudlik bilan sug'or":   'Немедленно поливать',
    "Tez sug'or":            'Скоро поливать',
    "Sug'orishni to'xtat":   'Остановить полив',
    'Amal talab etmaydi':    'Действий не требуется',

    /* ─── Chart titles ───────────────────────────────────────── */
    'Namlik trendi':                               'Тренд влажности',
    'Barcha sensorlar bo\'yicha o\'rtacha tuproq namligi': 'Средняя влажность почвы по всем датчикам',
    "Ekin turlari bo'yicha tejash":                "Экономия по культурам",
    "O'rtacha suv tejash foizi":                   'Средний % экономии воды',
    'Alert taqsimoti':                             'Распределение оповещений',
    'Jiddiylik darajasi bo\'yicha':                'По уровню серьёзности',
    "Sensor bo'yicha suv tejash":                  'Экономия воды по датчикам',
    'Tavsiyalar asosida hisoblangan':              'Рассчитано по рекомендациям',
    '7 kun':   '7 дней',
    '14 kun':  '14 дней',
    '30 kun':  '30 дней',

    /* ─── Filter tabs ────────────────────────────────────────── */
    'Barchasi':   'Все',
    'Onlaynlar':  'Онлайн',
    'Offlaynlar': 'Офлайн',
    'Ogohlantirishlar': 'Предупреждения',
    'Barcha obunalar':  'Все подписки',
    'Faollar':    'Активные',
    'Muddati o\'tganlar': 'Истекшие',

    /* ─── Placeholders & hints ───────────────────────────────── */
    "Sensor ID, ferma yoki xolat bo'yicha qidiring...": 'Поиск по датчику, ферме или статусу...',
    "Mijoz ismi yoki telefoni bo'yicha qidiring...":    'Поиск по имени клиента или телефону...',
    'Qidirish...':            'Поиск...',
    "Bo'lim tanlang...":      'Выберите раздел...',

    /* ─── Modal titles ───────────────────────────────────────── */
    "Yangi ferma qo'shish":   'Добавить новую ферму',
    "Yangi sensor qo'shish":  'Добавить новый датчик',
    "Yangi mijoz qo'shish":   'Добавить нового клиента',
    'Ferma ma\'lumotlari':     'Данные фермы',
    'Sensor ma\'lumotlari':    'Данные датчика',

    /* ─── Form labels ────────────────────────────────────────── */
    'Ism va familiya':         'Имя и фамилия',
    'Telefon raqam':           'Номер телефона',
    'Manzil':                  'Адрес',
    'Maydon (gektar)':         'Площадь (га)',
    "Ekin turi":               'Тип культуры',
    "Viloyat":                 'Область',
    "Tuman":                   'Район',
    "Latitude":                'Широта',
    "Longitude":               'Долгота',
    "Sensor ID":               'ID датчика',
    "Chuqurlik (sm)":          'Глубина (см)',

    /* ─── Settings tabs ──────────────────────────────────────── */
    'Umumiy':                  'Общие',
    'Davlat tizimlari':        'Государственные системы',
    "To'lov tizimlari":        'Платёжные системы',
    'Bot & API':               'Бот и API',
    'Asosiy API':              'Основной API',
    'Sessiya va Xavfsizlik':   'Сессия и безопасность',
    'Alert sozlamalari':       'Настройки оповещений',
    'Sessiya vaqti':           'Время сессии',
    'Interfeys tili':          'Язык интерфейса',
    'Buffer vaqti':            'Время буфера',
    'Minimum daraja':          'Минимальный уровень',
    'Davlat tizimlar integratsiyasi': 'Интеграция с государственными системами',

    /* ─── Integration section ────────────────────────────────── */
    'Faol':          'Активен',
    'Nofaol':        'Неактивен',
    'Ulanilmoqda': 'Подключение...',
    'Tekshirilmoqda...': 'Проверка...',

    /* ─── Sidebar account ────────────────────────────────────── */
    'Agrotexnik · Admin':      'Агротехник · Администратор',

    /* ─── Common sentences ───────────────────────────────────── */
    "Yuklanmoqda...":           'Загрузка...',
    "Ma'lumot yo'q":           'Нет данных',
    'Xabar yuborildi':         'Сообщение отправлено',
    'Saqlandi':                'Сохранено',
    'Xatolik':                 'Ошибка',
    "Diqqat va yuqori":        'Внимание и выше',
    "Xato va yuqori":          'Ошибка и выше',
    'Faqat kritik':            'Только критические',
    '30 daqiqa':               '30 минут',
    '1 soat':                  '1 час',
    '8 soat':                  '8 часов',
    '1 kun':                   '1 день',
    '1 daqiqa':                '1 минута',
    '2 daqiqa':                '2 минуты',
    '5 daqiqa':                '5 минут',
    '10 daqiqa':               '10 минут',
  },

  en: {
    /* ─── Navigation ─────────────────────────────────────────── */
    'Dashboard':           'Dashboard',
    'Sensorlar':           'Sensors',
    'Fermalar':            'Farms',
    'Tavsiyalar':          'Recommendations',
    'Alertlar':            'Alerts',
    'Hisobotlar':          'Reports',
    'Mijozlar':            'Clients',
    'Sozlamalar':          'Settings',
    'Yordam':              'Help',
    'Tezkor kirish':       'Quick access',
    "Sensorlar ro'yxati":  'Sensor list',

    /* ─── Page subtitles ─────────────────────────────────────── */
    '— barcha sensorlar monitoringi': '— all sensors monitoring',
    '— ferma xaritasi va sensorlar':  '— farm map and sensors',
    '— sensor ma\'lumotlari':         '— sensor data',

    /* ─── Buttons ────────────────────────────────────────────── */
    'Yangilash':              'Refresh',
    'Yangi ferma':            'New farm',
    'Yangi sensor':           'New sensor',
    'Yangi mijoz':            'New client',
    'Chop etish':             'Print',
    'CSV yuklab olish':       'Download CSV',
    "Qo'shish":               'Add',
    'Saqlash':                'Save',
    'Bekor qilish':           'Cancel',
    "O'chirish":              'Delete',
    'Tahrirlash':             'Edit',
    "Ko'rish":                'View',
    'Tasdiqla':               'Confirm',
    'Yuborish':               'Send',
    'Ulanishni tekshir':      'Test connection',
    'Hammasini saqlash':      'Save all',
    'Test yuborish':          'Send test',
    'Konfigni eksport qilish':'Export config',
    'Konfigni import qilish': 'Import config',
    "Ko'rish va tahrirlash":  'View & edit',

    /* ─── Table headers ──────────────────────────────────────── */
    'Sensor':                 'Sensor',
    'Ferma':                  'Farm',
    'Ekin':                   'Crop',
    'Namlik':                 'Humidity',
    'Temperatura':            'Temperature',
    'Batareya':               'Battery',
    'Status':                 'Status',
    'Amallar':                'Actions',
    'Joylashuv':              'Location',
    "So'nggi o'qish":         'Last reading',
    'Tavsiya':                'Recommendation',
    'Kerak suv (L)':          'Water needed (L)',
    "An'anaviy (L)":          'Traditional (L)',
    'Tejash':                 'Saving',
    'Mijoz':                  'Client',
    'Obuna':                  'Subscription',
    'Ferma soni':             'Farms',
    'Telefon':                'Phone',
    'Sana':                   'Date',
    'Sabab':                  'Reason',
    'Xabar':                  'Message',
    'Daraja':                 'Level',
    'Vaqt':                   'Time',

    /* ─── Status badges ──────────────────────────────────────── */
    'Onlayn':      'Online',
    'Oflayn':      'Offline',
    'Diqqat':      'Warning',
    'Kritik':      'Critical',
    'Xato':        'Error',
    'Normal':      'Normal',
    'Faol':        'Active',
    'Nofaol':      'Inactive',
    'Test rejim':  'Test mode',
    'Ulangan':     'Connected',
    'Sozlanmagan': 'Not configured',

    /* ─── Metric cards ───────────────────────────────────────── */
    'Aktiv sensorlar':            'Active sensors',
    "O'rtacha namlik":            'Average humidity',
    'Aktiv alertlar':             'Active alerts',
    'Aktiv tavsiyalar':           'Active recommendations',
    "Jami suv tejalgan":          'Total water saved',
    "O'rtacha tejash":            'Average saving',
    'Jami alertlar':              'Total alerts',
    "Sug'orish tavsiyalari":      'Irrigation recommendations',
    "an'anaviy usulga nisbatan":  'compared to traditional method',
    'barcha tavsiyalar bo\'yicha':'across all recommendations',
    'bugungi kunda':              'today',
    'aktiv tavsiyalar':           'active recommendations',

    /* ─── Irrigation actions ─────────────────────────────────── */
    "Zudlik bilan sug'or":   'Irrigate now',
    "Tez sug'or":            'Irrigate soon',
    "Sug'orishni to'xtat":   'Stop irrigation',
    'Amal talab etmaydi':    'No action needed',

    /* ─── Chart titles ───────────────────────────────────────── */
    'Namlik trendi':                               'Moisture trend',
    "Barcha sensorlar bo'yicha o'rtacha tuproq namligi": 'Average soil moisture across all sensors',
    "Ekin turlari bo'yicha tejash":                'Saving by crop type',
    "O'rtacha suv tejash foizi":                   'Average water saving percentage',
    'Alert taqsimoti':                             'Alert distribution',
    'Jiddiylik darajasi bo\'yicha':                'By severity level',
    "Sensor bo'yicha suv tejash":                  'Water saving by sensor',
    'Tavsiyalar asosida hisoblangan':              'Calculated based on recommendations',
    '7 kun':   '7 days',
    '14 kun':  '14 days',
    '30 kun':  '30 days',

    /* ─── Filter tabs ────────────────────────────────────────── */
    'Barchasi':   'All',
    'Onlaynlar':  'Online',
    'Offlaynlar': 'Offline',
    'Ogohlantirishlar': 'Warnings',
    'Barcha obunalar':  'All subscriptions',
    'Faollar':    'Active',
    'Muddati o\'tganlar': 'Expired',

    /* ─── Placeholders & hints ───────────────────────────────── */
    "Sensor ID, ferma yoki xolat bo'yicha qidiring...": 'Search by sensor ID, farm or status...',
    "Mijoz ismi yoki telefoni bo'yicha qidiring...":    'Search by client name or phone...',
    'Qidirish...':            'Search...',
    "Bo'lim tanlang...":      'Choose a section...',

    /* ─── Modal titles ───────────────────────────────────────── */
    "Yangi ferma qo'shish":   'Add new farm',
    "Yangi sensor qo'shish":  'Add new sensor',
    "Yangi mijoz qo'shish":   'Add new client',
    'Ferma ma\'lumotlari':     'Farm details',
    'Sensor ma\'lumotlari':    'Sensor details',

    /* ─── Form labels ────────────────────────────────────────── */
    'Ism va familiya':         'Full name',
    'Telefon raqam':           'Phone number',
    'Manzil':                  'Address',
    'Maydon (gektar)':         'Area (hectares)',
    "Ekin turi":               'Crop type',
    "Viloyat":                 'Region',
    "Tuman":                   'District',
    "Latitude":                'Latitude',
    "Longitude":               'Longitude',
    "Sensor ID":               'Sensor ID',
    "Chuqurlik (sm)":          'Depth (cm)',

    /* ─── Settings tabs ──────────────────────────────────────── */
    'Umumiy':                  'General',
    'Davlat tizimlari':        'Government systems',
    "To'lov tizimlari":        'Payment systems',
    'Bot & API':               'Bot & API',
    'Asosiy API':              'Main API',
    'Sessiya va Xavfsizlik':   'Session & Security',
    'Alert sozlamalari':       'Alert settings',
    'Sessiya vaqti':           'Session timeout',
    'Interfeys tili':          'Interface language',
    'Buffer vaqti':            'Buffer time',
    'Minimum daraja':          'Minimum level',
    'Davlat tizimlar integratsiyasi': 'Government system integrations',

    /* ─── Integration ────────────────────────────────────────── */
    'Ulanilmoqda': 'Connecting...',
    'Tekshirilmoqda...': 'Checking...',

    /* ─── Sidebar account ────────────────────────────────────── */
    'Agrotexnik · Admin':      'Agronomist · Admin',

    /* ─── Common sentences ───────────────────────────────────── */
    "Yuklanmoqda...":           'Loading...',
    "Ma'lumot yo'q":           'No data',
    'Xabar yuborildi':         'Message sent',
    'Saqlandi':                'Saved',
    'Xatolik':                 'Error',
    "Diqqat va yuqori":        'Warning and above',
    "Xato va yuqori":          'Error and above',
    'Faqat kritik':            'Critical only',
    '30 daqiqa':               '30 minutes',
    '1 soat':                  '1 hour',
    '8 soat':                  '8 hours',
    '1 kun':                   '1 day',
    '1 daqiqa':                '1 minute',
    '2 daqiqa':                '2 minutes',
    '5 daqiqa':                '5 minutes',
    '10 daqiqa':               '10 minutes',
  },
};

/* ── Core translation function ───────────────────────────────── */
function t(key, lang) {
  lang = lang || getCurrentLang();
  if (lang === 'uz') return key;
  return (I18N[lang] && I18N[lang][key]) || key;
}

function getCurrentLang() {
  return localStorage.getItem('lang') || 'uz';
}

function setLang(lang) {
  if (!I18N_LANGS[lang]) return;
  localStorage.setItem('lang', lang);
  applyI18n();
}

/* ── DOM translation engine ──────────────────────────────────── */
function applyI18n() {
  const lang = getCurrentLang();
  const map  = lang === 'uz' ? null : I18N[lang];

  // Update <html lang=""> attribute
  document.documentElement.lang = lang;

  // Update page title
  const pageTitle = document.querySelector('title');
  if (pageTitle) {
    const parts = pageTitle.textContent.split('—');
    if (parts.length >= 2) {
      const section = t(parts[1].trim(), lang);
      pageTitle.textContent = parts[0].trim() + ' — ' + section;
    }
  }

  if (!map) return; // UZ is base — no translation needed

  // 1. Walk all visible text nodes
  _translateTextNodes(document.body, map);

  // 2. Translate placeholder attributes
  document.querySelectorAll('[placeholder]').forEach(el => {
    const orig = el.dataset.i18nPhOrig || el.getAttribute('placeholder');
    el.dataset.i18nPhOrig = orig;
    if (map[orig]) el.setAttribute('placeholder', map[orig]);
  });

  // 3. Translate title/tooltip attributes
  document.querySelectorAll('[title]').forEach(el => {
    const orig = el.dataset.i18nTitleOrig || el.getAttribute('title');
    el.dataset.i18nTitleOrig = orig;
    if (map[orig]) el.setAttribute('title', map[orig]);
  });

  // 4. Translate data-i18n elements (explicit markup — takes priority)
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (map[key]) el.textContent = map[key];
  });

  // 5. Update language selector if present
  const langSelect = document.getElementById('ui-lang');
  if (langSelect) langSelect.value = lang;

  // 6. Update language label in header if present (cycleLang button)
  const langLabel = document.getElementById('lang-label');
  if (langLabel) langLabel.textContent = lang.toUpperCase();
}

/* ── Text node walker ────────────────────────────────────────── */
function _translateTextNodes(root, map) {
  // Skip these tags entirely
  const SKIP_TAGS = new Set(['SCRIPT', 'STYLE', 'INPUT', 'TEXTAREA', 'CODE', 'PRE']);

  const walker = document.createTreeWalker(
    root,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode(node) {
        if (!node.textContent.trim()) return NodeFilter.FILTER_REJECT;
        const tag = node.parentElement?.tagName;
        if (SKIP_TAGS.has(tag)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    }
  );

  const nodes = [];
  while (walker.nextNode()) nodes.push(walker.currentNode);

  nodes.forEach(node => {
    // Save original text on first run
    if (!node._i18nOrig) node._i18nOrig = node.textContent;
    const trimmed = node._i18nOrig.trim();
    if (!trimmed) return;

    // Try exact match
    if (map[trimmed] !== undefined) {
      // Preserve surrounding whitespace
      node.textContent = node._i18nOrig.replace(trimmed, map[trimmed]);
      return;
    }

    // Try partial matches for longer strings (e.g. subtitle phrases)
    let text = node._i18nOrig;
    let changed = false;
    for (const [uz, translated] of Object.entries(map)) {
      if (uz.length > 8 && text.includes(uz)) {
        text = text.replace(uz, translated);
        changed = true;
      }
    }
    if (changed) node.textContent = text;
  });
}

/* ── Language switcher UI component ─────────────────────────── */
function buildLangSwitcher(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  const current = getCurrentLang();
  container.innerHTML = Object.entries(I18N_LANGS).map(([code, info]) =>
    `<button onclick="setLang('${code}')"
      style="padding:6px 12px;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer;
             border:1px solid ${code===current?'var(--brand)':'var(--border-secondary)'};
             background:${code===current?'var(--brand-50)':'transparent'};
             color:${code===current?'var(--brand)':'var(--text-secondary)'}">
      ${info.flag} ${info.label}
    </button>`
  ).join('');
}

/* ── Auto-init on DOM ready ──────────────────────────────────── */
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', applyI18n);
} else {
  // DOM already ready
  setTimeout(applyI18n, 0);
}
