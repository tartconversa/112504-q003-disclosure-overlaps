# 公益成效月报的交叠披露限制

报出的计数单位见 unit。相同人口框的分区可随版本改变。历史表的可见范围由 access 表解释。所有计数均为虚构。

## 资料

CSV 样例为合成记录，使用 UTF-8，首行为字段名。多值用竖线分隔，空单元格表示来源未填。记录日期和业务生效日期各有含义。

- reports.csv 的字段为 row、period、version、provider、zone、group、activity、unit、low、high。
- intersections.csv 的字段为 fact、row_a、row_b、low、high、revision。
- zones.csv 的字段为 zone、frame、previous、effective、kind。
- published.csv 的字段为 release、period、access_group、cell、value_low、value_high、approved_at。
- access.csv 的字段为 group、can_read、min_count、min_uncertainty。
- requests.csv 的字段为 request、access_group、period、cell、priority、requested_on。

## 运行资料检查

在项目根目录使用 Python 3.11 或更高版本。依赖仅为标准库。

~~~sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
~~~
