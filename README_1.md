# UMT-pythonweb-hw-04 

Асинхронний скрипт для сортування файлів за розширеннями.

## Встановлення залежностей

```bash
pip install aiofiles aiopath
```

## Використання

```bash
python main.py <вхіднв папка> <вихідна папка>
```

### Приклад

```bash
python main.py C:\Users\Admin\Downloads  C:\Users\Admin\Desktop\sort
```

Після виконання у `sort` з'являться підпапки за розширеннями:
```
sort/
  txt/
  jpg/
  pdf/
  ...
```
