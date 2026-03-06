<div dir="rtl" style="text-align: right;">

# التعامل مع الملفات

عند فتح ملف، نستخدم الدالة `open` لتحديد العملية المطلوبة.

## 1. أوضاع فتح الملفات (Modes)

| الوضع | الوظيفة |
|-------|----------|
| `'x'` | للإنشاء فقط: يستخدم لإنشاء ملف جديد. إذا كان هناك ملف بنفس الاسم، سيتوقف. |
| `'w'` | للكتابة: ينشئ ملفاً جديداً، ولكن إذا وجد ملفاً قديماً فإنه يمسح كل ما فيه ويبدأ من الصفر. |
| `'a'` | للإضافة: لا يمسح شيئاً، بل يضيف النص الجديد في نهاية الملف. |
| `'r'` | للقراءة: لفتح الملف واستعراض ما بداخله فقط. |

## 2. أمثلة

```python
# استخدام وضع الإنشاء الحصري لضمان عدم الكتابة فوق ملف قديم
f_new = open('staff_names.txt', 'x')
f_new.write('Yassine')
f_new.write('\n')
f_new.close()

# استخدام وضع الكتابة لمسح المحتوى القديم وتحديث البيانات
with open('staff_names.txt', 'w') as f_write:
    f_write.write('Mariam')
    f_write.write('\n')

# استخدام وضع الإضافة لزيادة البيانات
with open('staff_names.txt', 'a') as f_append:
    f_append.write('Omar')
    f_append.write('\n')

# استخدام وضع القراءة لعرض النتيجة النهائية
with open('staff_names.txt', 'r') as f_read:
    print(f_read.read())
```

## 3. الفرق بين الحرف 'x' والحرف 'w'

* إذا استخدمت الحرف `'w'` على ملف موجود، ستفقد بياناتك القديمة فوراً.
* إذا استخدمت الحرف `'x'` على ملف موجود، سيعطي البرنامج تنبيهاً بالخطأ ولن يمسح أي حرف من بياناتك، مما يجعله الخيار الأكثر أماناً عند إنشاء الملفات لأول مرة.

---

## معالجة الملفات المتعددة

```python
import fileinput

with fileinput.input(files=['asia.txt', 'africa.txt']) as files:
    index = 1
    for line in files:
        if fileinput.isfirstline():
            print(f"\n--- Reading {fileinput.filename()} ---")
        print(f"{index} - {line}", end="")
        index += 1
```

* `import fileinput` — استيراد مكتبة قراءة الملفات
* `with fileinput.input(...)` — فتح الملفات للقراءة
* `index = 1` — بدء الترقيم من 1
* `for line in files` — المرور على كل سطر في الملفات
* `if fileinput.isfirstline()` — التحقق إذا كان هذا أول سطر في الملف الحالي
* `print(...)` — طباعة اسم الملف عند بداية كل ملف جديد

---

## ما هو JSON؟

JSON هي صيغة لـ تخزين وتبادل البيانات بين البرامج.
* خفيفة وسهلة القراءة
* تشبه القواميس في بايثون
* تستخدم في APIs وملفات التكوين

## التحويل بين JSON وPython

| اتجاه | الوصف |
|-------|--------|
| **Deserializing (فك التشفير)** | JSON → Python: نحول من نص JSON إلى بيانات Python |
| **Serializing (التشفير)** | Python → JSON: نحول من بيانات Python إلى نص JSON |

## المراسلة بين JSON وPython

| JSON | Python |
|------|--------|
| object | dict (قاموس) |
| array | list (قائمة) |
| string | str (نص) |
| number (int) | int (عدد صحيح) |
| number (float) | float (عدد عشري) |
| true / false | True / False |
| null | None |

## الدوال المهمة في وحدة json

**Deserializing (JSON ← Python):**
```python
import json

# من نص JSON إلى قاموس Python
json_string = '{"name": "Ahmed", "age": 25}'
data = json.loads(json_string)  # loads = load string
print(data["name"])

# من ملف JSON إلى Python
with open('data.json', 'r') as file:
    data = json.load(file)  # load من ملف
```

**Serializing (Python → JSON):**
```python
import json

# من قاموس Python إلى نص JSON
person = {"name": "Sara", "age": 22, "student": True}
json_text = json.dumps(person)  # dumps = dump string
print(json_text)

# من قائمة Python إلى JSON وحفظ في ملف
tasks = [
    {"id": 1, "title": "Study", "done": False},
    {"id": 2, "title": "Walk", "done": True}
]
with open('output.json', 'w') as file:
    json.dump(tasks, file)
```

## أهم الدوال باختصار

| الدالة | الوظيفة |
|--------|----------|
| json.loads() | تحويل نص JSON إلى Python |
| json.load() | تحويل ملف JSON إلى Python |
| json.dumps() | تحويل Python إلى نص JSON |
| json.dump() | تحويل Python وحفظه في ملف |

## مثال تطبيقي كامل

```python
import json

my_tasks = [
    {'id': 1, 'title': 'Study for 4 hours', 'done': False},
    {'id': 2, 'title': 'Walk for 30 minutes', 'done': True}
]

json_data = json.dumps(my_tasks)
print("JSON:", json_data)

with open('tasks.json', 'w') as f:
    json.dump(my_tasks, f)

with open('tasks.json', 'r') as f:
    loaded_data = json.load(f)
    print("المهمة الأولى:", loaded_data[0]['title'])
```

**خلاصة:**  
* `s` في loads و dumps تعني **string** (نص).  
* بدون s نتعامل مع **ملفات**.

</div>
