from collections import defaultdict
import json
from typing import Dict

# Note: Use `Dict[str, Dict[str, None]]` instead of `Dict[str, Set[str]]`
# to preserve the insert order.
d: Dict[str, Dict[str, None]] = defaultdict(dict)

with open('yitizi.csv') as f:
	next(f)  # skip header
	for line in f:
		k, vs = line.rstrip().split(',')
		for v in vs:
			# Rule 1 (See README.md)
			d[k][v] = None
			d[v][k] = None

			# Rule 2 (See README.md)
			for c in vs:
				if v != c:
					d[v][c] = None

# Note: `d2` is a compact version of `d`, to reduce size.
d2: Dict[str, str] = {k: ''.join(vs) for k, vs in d.items()}

with open('yitizi.json', 'w') as f:
	json.dump(d2, f, ensure_ascii=False, separators=(',\n', ':'))
