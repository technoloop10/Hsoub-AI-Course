<div dir="rtl" style="text-align: right;">

# مثال عملي: استخراج بيانات الطقس من الويب (Web Scraping)

## نظرة عامة

هذا المثال من مشروع **weatherscraper** يوضح كيف نستخرج بيانات توقعات الطقس لمدن مختلفة من موقع ويب، ثم ننظمها ونحفظها في ملف نصي (`output.txt`) وملف JSON (`output.json`) باستخدام مكتبات بايثون.

---

## 1. المكتبات المستخدمة

| المكتبة | الاستخدام |
|--------|-----------|
| `requests` | إرسال طلب HTTP لجلب محتوى الصفحة |
| `BeautifulSoup` (من `bs4`) | تحليل HTML واستخراج العناصر المطلوبة |
| `re` | التعابير النمطية لاستخراج أسماء المدن ودرجات الحرارة |
| `datetime` (مثل `date`) | الحصول على التاريخ الحالي لتوثيق البيانات |
| `tabulate` | تنسيق البيانات في شكل جدول للعرض النصي |
| `json` | حفظ البيانات بصيغة JSON في ملف |

---

## 2. دالة جلب البيانات: `get_forecast_data()`

### تحديد الرابط والترويسات (Headers)

```python
url = 'https://world-weather.info/'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/114.0',
    'cookie': 'celsius=1'
}
```

* **user-agent:** يجعل الطلب يبدو وكأنه من متصفح حقيقي؛ يقلل احتمال حظر الموقع للطلبات الآلية.
* **cookie: celsius=1:** لطلب درجة الحرارة بالسيلسيوس.

### إرسال الطلب وتحليل الصفحة

```python
response = requests.get(url, headers=headers)
if response.ok:
    soup = BeautifulSoup(response.content, 'html.parser')
    resorts = soup.find('div', id='resorts')
```

* `response.ok` يتحقق من نجاح الطلب (مثلاً كود 200).
* `BeautifulSoup` يحلل محتوى HTML.
* `soup.find('div', id='resorts')` يحدد القسم الذي يحتوي على قائمة المدن/المنتجعات.

### استخراج أسماء المدن (تعابير نمطية)

```python
re_cities = r'">([\w\s]+)<\/a><span>'
cities = re.findall(re_cities, str(resorts))
```

* النمط يبحث عن النص الواقع بين `">` و `</a><span>`.
* `([\w\s]+)` مجموعة تُستخرج منها أسماء المدن (أحرف ومسافات).

### استخراج درجات الحرارة

```python
# نمط لاستخراج الأرقام (درجات الحرارة)
temps = re.findall(re_temps, str(resorts))
temps = [int(temp) for temp in temps]
```

* استخدام `re.findall` مع نمط مناسب لاستخراج القيم الرقمية ثم تحويلها إلى أعداد صحيحة.

### استخراج الحالة الجوية (Conditions)

```python
conditions_tags = resorts.find_all('span', class_='tooltip')
conditions = [condition.get('title') for condition in conditions_tags]
```

* البحث عن كل عناصر `<span>` ذات الصنف `tooltip`.
* أخذ قيمة السمة `title` من كل عنصر (مثل: سماء صافية، غائم جزئياً).

### دمج البيانات وإرجاعها

```python
data = zip(cities, temps, conditions)
return data
# أو في حال الفشل:
return False
```

* `zip()` يربط كل مدينة بدرجة حرارتها وحالتها الجوية في tuples.
* النتيجة قابلة للاستخدام في الكتابة إلى ملف نصي أو JSON.

---

## 3. دالة الكتابة إلى ملف نصي: `get_forecast_txt()`

```python
def get_forecast_txt():
    data = get_forecast_data()
    if data:
        today = date.today().strftime('%d/%m/%Y')
        with open('output.txt', 'w') as f:
            f.write('Popular Cities Forecast' + '\n')
            f.write(today + '\n')
            f.write('='*23 + '\n')
            table = tabulate(data, headers=['City', 'Temp.', 'Condition'], tablefmt='fancy_grid')
            f.write(table)
```

* استدعاء `get_forecast_data()` للحصول على البيانات.
* كتابة عنوان وتاريخ وفاصل.
* استخدام `tabulate` لإنشاء جدول برؤوس **City**, **Temp.**, **Condition** وتنسيق `fancy_grid`.
* كتابة الجدول في `output.txt`.

### شرح مكتبة `tabulate`

**ما هي tabulate؟**  
مكتبة بايثون لتنسيق البيانات (قوائم، tuples، قواميس) في شكل **جدول نصي** يسهل قراءته في الطرفية أو في ملف نصي.

**التثبيت:**
```bash
pip install tabulate
```

**الدالة الأساسية:**
```python
tabulate(tabular_data, headers=..., tablefmt='...')
```

| المعامل | الوصف |
|---------|--------|
| `tabular_data` | البيانات المراد عرضها: قائمة قوائم، قائمة tuples، أو قائمة قواميس. في مثالنا: `data` (ناتج `zip`) أي مكرر من tuples مثل `(مدينة، درجة، حالة)`. |
| `headers` | قائمة أسماء الأعمدة، تُعرض في السطر الأول. مثال: `['City', 'Temp.', 'Condition']`. |
| `tablefmt` | شكل الجدول. قيم شائعة: `'plain'`, `'simple'`, `'grid'`, `'fancy_grid'`, `'pipe'`, `'orgtbl'` وغيرها. |

**أمثلة على تنسيقات الجدول (`tablefmt`):**

| القيمة | الوصف |
|--------|--------|
| `'plain'` | جدول بسيط بدون خطوط |
| `'simple'` | رؤوس مع خط فاصل |
| `'grid'` | حدود شبكية |
| `'fancy_grid'` | شبكة مع زوايا مستديرة (كما في المثال) |
| `'pipe'` | مناسب لـ Markdown (أعمدة بـ `|`) |

**مثال توضيحي:**
```python
from tabulate import tabulate
data = [('القاهرة', 37, 'سماء صافية'), ('دبي', 41, 'صافي')]
table = tabulate(data, headers=['City', 'Temp.', 'Condition'], tablefmt='fancy_grid')
print(table)
```

**ناتج تقريبي:**
```
╒══════════╤═══════╤════════════╕
│ City     │ Temp. │ Condition  │
╞══════════╪═══════╪════════════╡
│ القاهرة  │ 37    │ سماء صافية │
│ دبي      │ 41    │ صافي       │
╘══════════╧═══════╧════════════╝
```

في مشروع الطقس، نمرّر `data` (من `zip`) و`headers` و`tablefmt='fancy_grid'` ثم نكتب النتيجة في `output.txt` ليكون التقرير منسقاً وواضحاً.

---

## 4. دالة الكتابة إلى JSON: `get_forecast_json()`

```python
def get_forecast_json():
    data = get_forecast_data()
    if data:
        today = date.today().strftime('%d/%m/%Y')
        cities = [{'city': city, 'temp': temp, 'condition': condition} for city, temp, condition in data]
        data_json = {'title': 'Popular Cities Forecast', 'date': today, 'cities': cities}
        with open('output.json', 'w') as f:
            json.dump(data_json, f, ensure_ascii=False)
```

* تحويل كل tuple (مدينة، درجة، حالة) إلى قاموس.
* بناء قاموس رئيسي يحتوي على العنوان والتاريخ وقائمة المدن.
* `json.dump(..., ensure_ascii=False)` لحفظ النص كما هو (مثل العربية) دون تحويله إلى `\uXXXX`.

### مثال على محتوى `output.json`

```json
{
  "title": "Popular Cities Forecast",
  "date": "21/07/2023",
  "cities": [
    {"city": "Amsterdam", "temp": 19, "condition": "Few clouds"},
    {"city": "Cairo", "temp": 37, "condition": "Clear sky"},
    ...
  ]
}
```

---

## 5. نقطة التنفيذ

```python
if __name__ == '__main__':
    get_forecast_txt()
    get_forecast_json()
```

* تشغيل الدالتين عند تنفيذ الملف مباشرة (وليس عند استيراده كوحدة).

---

## الخلاصة

| الخطوة | الأداة | الغرض |
|--------|--------|--------|
| جلب الصفحة | `requests.get()` | الحصول على HTML من الموقع |
| تحليل HTML | `BeautifulSoup` | العثور على العناصر (مثل `div#resorts`, `span.tooltip`) |
| استخراج أنماط | `re.findall()` | استخراج المدن ودرجات الحرارة من النص |
| تنظيم البيانات | `zip()` وقوائم القواميس | ربط المدينة بالحرارة والحالة |
| حفظ نصي | `tabulate` + `open().write()` | جدول منسق في `output.txt` |
| حفظ JSON | `json.dump(..., ensure_ascii=False)` | بيانات منظمة في `output.json` |

هذا المثال يجمع بين **استخراج البيانات من الويب** (Requests + BeautifulSoup + re) و**معالجتها وحفظها** (ملف نصي وJSON) كما في دروس الملفات و JSON.

</div>
