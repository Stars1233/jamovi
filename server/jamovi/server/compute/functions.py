
import random
import math
from numbers import Number as num
import statistics as stats
from datetime import datetime
from datetime import timezone

from numpy import quantile
from scipy.stats import boxcox
# numpy, scipy return numpy.float64's, so need to convert back to float
from scipy.stats import rankdata

from jamovi.core import DataType
from jamovi.core import MeasureType
from jamovi.server.compute import is_missing
from jamovi.server.compute import is_equal

from .funcmeta import row_wise
from .funcmeta import column_wise
from .funcmeta import column_wise_no_group_by
from .funcmeta import returns
from .funcmeta import levels


NaN = float('nan')


@row_wise
def MAX(index, arg0: float, *args: float):
    values = [ arg0 ]
    values.extend(args)
    values = list(filter(lambda x: not is_missing(x), values))
    return max(values)


@row_wise
def MEAN(index, arg0: float, *args: float, ignore_missing: int = 0, min_valid: int = 0):
    values = [ arg0 ]
    values.extend(args)
    if min_valid > 0 or ignore_missing != 0:
        values = list(filter(lambda x: not is_missing(x), values))
    if len(values) < min_valid:
        return NaN
    else:
        return stats.mean(values)


@row_wise
def MIN(index, arg0: float, *args: float):
    values = [ arg0 ]
    values.extend(args)
    values = list(filter(lambda x: not is_missing(x), values))
    return min(values)


@row_wise
def STDEV(index, arg0: float, *args: float, ignore_missing: int = 0):
    values = [ arg0 ]
    values.extend(args)
    if ignore_missing != 0:
        values = list(filter(lambda x: not is_missing(x), values))
    return stats.stdev(values)


@row_wise
def SUM(index, arg0: float, *args: float, ignore_missing: int = 0, min_valid: int = 0):
    values = [ arg0 ]
    values.extend(args)
    if min_valid > 0 or ignore_missing != 0:
        values = list(filter(lambda x: not is_missing(x), values))
    if len(values) < min_valid:
        return NaN
    return math.fsum(values)


@row_wise
@returns(DataType.DECIMAL, MeasureType.CONTINUOUS, 0)
def ABS(index, value: num):
    if is_missing(value):
        return value
    return abs(value)


@row_wise
@returns(DataType.DECIMAL, MeasureType.CONTINUOUS)
def ROUND(index, value: num, digits: int = 0):
    if is_missing(value):
        return(value)
    return round(value, digits)


@row_wise
@returns(DataType.INTEGER, MeasureType.CONTINUOUS)
def FLOOR(index, value: num):
    if is_missing(value):
        return(value)
    return int(value // 1)

@row_wise
@returns(DataType.INTEGER, MeasureType.CONTINUOUS)
def CEILING(index, value: num):
    if is_missing(value):
        return(value)
    return int(math.ceil(value))

@row_wise
def EXP(index, value: float):
    return math.exp(value)


@row_wise
def LN(index, value: float):
    return math.log(value)


@row_wise
def LOG10(index, value: float):
    return math.log10(value)


@row_wise
def SQRT(index, value: float):
    return math.sqrt(value)


@row_wise
def UNIF(index, a: float = 0.0, b: float = 1.0):
    return random.uniform(a, b)


@row_wise
def NORM(index, mu: float = 0.0, sd: float = 1.0):
    return random.gauss(mu, sd)


@row_wise
def BETA(index, alpha: float = 1.0, beta: float = 1.0):
    return random.betavariate(alpha, beta)


@row_wise
@returns(DataType.INTEGER, MeasureType.ORDINAL)
def MATCH(index, needle, *haystack):
    if is_missing(needle):
        return -2147483648
    for index, value in enumerate(haystack):
        if is_equal(needle, value):
            return index + 1
    return -2147483648


@row_wise
@returns(DataType.INTEGER, MeasureType.NOMINAL, range(1, 10000))
@levels(range(1, 10000))
def HLOOKUP(index, lookup_index: int, *args, ignore_missing: int = 0):
    lookup_index -= 1  # was indexed from 1
    if lookup_index < 0 or lookup_index >= len(args):
        return -2147483648
    if ignore_missing == 0:
        return args[lookup_index]
    arg_i = 0
    for v in args:
        if is_missing(v):
            continue
        if arg_i == lookup_index:
            return v
        arg_i += 1
    return -2147483648


@row_wise
def GAMMA(index, alpha: float = 1.0, beta: float = 1.0):
    return random.gammavariate(alpha, beta)


@row_wise
@returns(DataType.INTEGER, MeasureType.ORDINAL)
def ROW(index):
    return index + 1


@row_wise
@returns(DataType.INTEGER, MeasureType.NOMINAL)
def NOTROW(index, arg0, *args):
    if (index + 1) == arg0:
        return 0
    elif (index + 1) in args:
        return 0
    return 1


@column_wise
def Q1(values: float):
    values = filter(lambda x: not math.isnan(x), values)
    return float(quantile(list(values), 0.25))


@column_wise
def Q3(values: float):
    values = filter(lambda x: not math.isnan(x), values)
    return float(quantile(list(values), 0.75))


@row_wise
def IIQR(index, value: float, q1: float, q3: float):
    if value < q1:
        value = (value - q1) / (q3 - q1)
    elif value > q3:
        value = (value - q3) / (q3 - q1)
    else:
        value = 0
    return value


@column_wise
def VMEAN(values: float):
    values = filter(lambda x: not math.isnan(x), values)
    return stats.mean(values)


@column_wise
def VSTDEV(values: float):
    values = filter(lambda x: not math.isnan(x), values)
    return stats.stdev(values)


@column_wise
def VSE(values: float):
    values = list(filter(lambda x: not math.isnan(x), values))
    n = sum(1 for _ in values)
    return math.sqrt(stats.variance(values) / n)


@row_wise
def VAR(index, arg0: float, *args: float, ignore_missing: int = 0):
    values = [ arg0 ]
    values.extend(args)
    if ignore_missing != 0:
        values = list(filter(lambda x: not is_missing(x), values))
    return stats.variance(values)


@column_wise
def VVAR(values: float):
    values = filter(lambda x: not math.isnan(x), values)
    return stats.variance(values)


@column_wise
def VMED(values: float):
    values = filter(lambda x: not math.isnan(x), values)
    return stats.median(values)


@column_wise
def VMAD(values: float):
    median = VMED(values)
    return VMED(map(lambda v: abs(v - median), values))


@column_wise
def VMADR(values: float):
    return VMAD(values)*1.4826


@column_wise
def VMODE(values: float):
    values = filter(lambda x: not math.isnan(x), values)
    return stats.mode(values)


@column_wise
@returns(DataType.INTEGER, MeasureType.ORDINAL)
def VN(values):
    values = filter(lambda v: not is_missing(v), values)
    return sum(1 for _ in values)


@column_wise
def VSUM(values: float):
    values = filter(lambda x: not math.isnan(x), values)
    return math.fsum(values)


@column_wise
@returns(DataType.INTEGER, MeasureType.ORDINAL)
def VROWS(values):
    return sum(1 for _ in values)


@column_wise
def VMIN(values: float):
    values = filter(lambda x: not math.isnan(x), values)
    return min(values)


@column_wise
def VMAX(values: float):
    values = filter(lambda x: not math.isnan(x), values)
    return max(values)


@column_wise
def VBOXCOXLAMBDA(values: float):
    values = filter(lambda x: not math.isnan(x), values)
    values = list(values)
    # numpy returns numpy.float64, so need to convert back to float
    return float(boxcox(values)[1])


@row_wise
def BOXCOX(index, x: float, lmbda: float = VBOXCOXLAMBDA):
    if x < 0:
        return NaN
    elif x == 0 and lmbda < 0:
        return float('-inf')
    elif lmbda == 0:
        return math.log(x)
    else:
        return (x ** lmbda - 1) / lmbda


@row_wise
def Z(index, x: float):
    # see the transfudgifier
    return x


@row_wise
def ABSZ(index, x: float):
    # see the transfudgifier
    return x


@row_wise
def MAXABSZ(index, x: float):
    # see the transfudgifier
    return x


@row_wise
def SCALE(index, x: float):
    # see the transfudgifier
    return x


@row_wise
@returns(DataType.INTEGER, MeasureType.NOMINAL, 0)
def OFFSET(index, x, offset: int):
    # this is handled specially elsewhere
    return x


@row_wise
@returns(DataType.INTEGER, MeasureType.NOMINAL, [1, 2])
@levels([1, 2])
def IF(index, cond: int, x=1, y=-2147483648):
    if is_missing(cond, True):
        return -2147483648
    return x if cond else y


@row_wise
@returns(DataType.INTEGER, MeasureType.NOMINAL, [1, 2])
def IFMISS(index, cond, x=1, y=-2147483648):
    return x if is_missing(cond, empty_str_is_missing=True) else y


@row_wise
@returns(DataType.INTEGER, MeasureType.NOMINAL)
def _FILTER(index, cond: int):
    # this is used by filters
    return 0 if is_missing(cond, empty_str_is_missing=True) else cond


@row_wise
@returns(DataType.INTEGER, MeasureType.NOMINAL, 0)
def NOT(index, x):
    if is_missing(x):
        return x
    return 1 if not x else 0


@row_wise
@returns(DataType.INTEGER, MeasureType.NOMINAL, 0)
def FILTER(index, x, *conds: int):
    for cond in conds:
        if is_missing(cond, True):
            return -2147483648
        if not cond:
            return -2147483648
    return x


@row_wise
@returns(DataType.INTEGER, MeasureType.CONTINUOUS)
def DATEVALUE(_, x: str, fmt: str = '%Y-%m-%d'):
    return int(datetime.strptime(x, fmt).replace(tzinfo=timezone.utc).timestamp() // 60 // 60 // 24)


@row_wise
@returns(DataType.TEXT, MeasureType.ORDINAL)
def DATE(_, x: int, fmt: str = '%Y-%m-%d'):
    return datetime.fromtimestamp(x * 60 * 60 * 24, timezone.utc).strftime(fmt)


@row_wise
@returns(DataType.TEXT, MeasureType.NOMINAL)
def TEXT(index, x: str):
    return x


@row_wise
def VALUE(index, x: str):
    try:
        return float(x)
    except ValueError:
        return NaN


@row_wise
@returns(DataType.INTEGER, MeasureType.CONTINUOUS)
def COUNT(index, *args):
    c = 0
    for v in args:
        if not is_missing(v):
            c += 1
    return c


@row_wise
@returns(DataType.INTEGER, MeasureType.CONTINUOUS)
def INT(index, x):
    try:
        return int(float(x))
    except ValueError:
        return -2147483648


@row_wise
@returns(DataType.TEXT, MeasureType.NOMINAL)
def SPLIT(index, x: str, sep: str = ',', piece: int = -2147483648):
    pieces = x.split(sep)
    if piece == -2147483648:
        return ' '.join(pieces)
    elif piece <= 0:
        return ''
    else:
        return pieces[piece - 1]


@row_wise
@returns(DataType.INTEGER, MeasureType.NOMINAL, range(2, 10000, 2))
@levels(range(0, 10000, 2))
def RECODE(index, x, *args):
    for i in range(0, len(args) - 1, 2):
        cond = args[i]
        if not is_missing(cond) and cond:
            return args[i + 1]
    if len(args) % 2 == 1:
        return args[-1]
    else:
        return x


@row_wise
@returns(DataType.INTEGER, MeasureType.NOMINAL)
def CONTAINS(index, item1: str, in1: str, *args: str, in2: str = '', in3: str = '', in4: str = '', in5: str = '', in6: str = '', in7: str = '', in8: str = '', in9: str = ''):
    needles = [ item1, in1 ] + list(args)
    haystacks = [ in2, in3, in4, in5, in6, in7, in8, in9 ]
    first_haystack = needles.pop()
    haystacks.insert(0, first_haystack)
    for needle in needles:
        for haystack in haystacks:
            if needle in haystack:
                return 1
    else:
        return 0


@column_wise
@returns(DataType.DECIMAL, MeasureType.CONTINUOUS)
def RANK(var: float):
    ranks = rankdata(list(var)).tolist()
    for i, v in enumerate(var):
        if math.isnan(v):
            ranks[i] = NaN
    return ranks


@column_wise_no_group_by
@returns(DataType.DECIMAL, MeasureType.CONTINUOUS, (0, 2))
def SAMPLE(v, n: int, otherwise = None):
    v = list(v)
    v_len = len(v)
    if v_len == 0:
        return v

    n = n.__iter__().__next__()
    if n >= v_len:
        return v

    invert = False
    if (v_len - n < n):
        invert = True
        n = v_len - n

    sample = [False] * v_len
    c = 0
    while True:
        if c == n:
            break
        index = random.randrange(v_len)
        if not sample[index]:
            sample[index] = True
            c += 1

    if otherwise:
        for i, o in enumerate(otherwise):
            if sample[i] == invert:
                v[i] = o
    else:
        for i in range(v_len):
            if sample[i] == invert:
                v[i] = NaN

    return v


_RECODE_NOM = RECODE
_RECODE_ORD = RECODE
_RECODE_CONT = RECODE
_RECODE_ID  = RECODE
