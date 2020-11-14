# Yitizi

[![](https://badge.fury.io/py/yitizi.svg)](https://pypi.org/project/yitizi/) [![](https://data.jsdelivr.com/v1/package/npm/yitizi/badge)](https://www.jsdelivr.com/package/npm/yitizi) [![](https://github.com/nk2028/yitizi/workflows/Package/badge.svg)](https://github.com/nk2028/yitizi/actions?query=workflow%3APackage)

Input a Chinese character. Output all the variant characters of it.<br>
輸入一個漢字，輸出它的全部異體字。<br>
输入一个汉字，输出它的全部异体字。

## Usage

### Python

```sh
pip install yitizi
```

```python
>>> import yitizi
>>> yitizi.get('和')
['咊', '龢']
```

### JavaScript (Node.js)

```sh
npm install yitizi
```

```javascript
> const Yitizi = require('yitizi');
> Yitizi.get('和');
[ '咊', '龢' ]
```

### JavaScript (browser)

```html
<script src="https://cdn.jsdelivr.net/npm/yitizi@0.0.2"></script>
```

```javascript
> Yitizi.get('和');
[ '咊', '龢' ]
```

## Design

As shown in the figure, the following information is stored in `yitizi.csv`:

![](https://raw.githubusercontent.com/nk2028/yitizi/main/demo/char.png)

This file is processed by `build/main.py`. The data in the file is converted into a graph.

Then, for each node in the graph, output the node and all its neighbor nodes. This becomes the final dictionary of the variant characters.

```
{ 正字: 異體字1, 異體字2,
  異體字1: 正字,
  異體字2: 正字
}
```

When using the library, the above dictionary is used to determine the variant characters of a given character.

## Note for developers

You need to substitute all the occurrences of the version string when publishing a new release.
