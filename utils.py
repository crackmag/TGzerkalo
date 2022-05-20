from pyparsing import (Combine, LineEnd, LineStart, OneOrMore, ParseException,
                       Suppress, Word, ZeroOrMore, nums)

PREFIX = "-100"
# id1 = -100\d+
CHANNEL_ID = Combine(PREFIX + Word(nums))
# [id1, id2]
ARRAY_CHANNELS = Suppress("[") \
    + CHANNEL_ID + ZeroOrMore(Suppress(",") + CHANNEL_ID) \
    + Suppress("]")

# ((ARRAY|ID):ID;)+
ALL = LineStart() \
    + OneOrMore((ARRAY_CHANNELS | CHANNEL_ID).setResultsName('source*') \
    + Suppress(":") \
    + CHANNEL_ID.setResultsName('target*')
    + Suppress(";")) \
    + LineEnd()

def parse_string(string):
    """Parse a string into channel mapping represenation

    Args:
        string (str): String to be parsed

    Returns:
        dict: Dict with source channels as keys and target channels as values
    """
    channels_mapping = {}
    try:
        res = ALL.parseString(string).asDict()
        for idx in range(len(res['source'])):
            if isinstance(res['source'][idx], list):
                for item in res['source'][idx]:
                    channels_mapping.setdefault(
                        int(item), []).append(int(res['target'][idx]))
            else:
                channels_mapping.setdefault(
                    int(res['source'][idx]), []).append(int(res['target'][idx]))
    except ParseException as e:
        print('Wrong string:', e)
    except Exception as e:
        print(e)

    return channels_mapping


if __name__ == "__main__":
    print(parse_string("[-1001,-1002]:-1003;[-1004]:-1005;-1006:-1007;"))
