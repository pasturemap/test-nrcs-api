import timeit
from typing import List

import nrcs_api


def get_test_data() -> List[nrcs_api.Region]:
    import json
    with open('tomkat_paddocks.json') as f:
        paddocks = json.loads(f.read())
    return [
        nrcs_api.Region(**x)
        for x in paddocks
    ]


def main(regions: List[nrcs_api.Region]):
    nrcs_api.estimate_forage(regions)


if __name__ == '__main__':
    test_data = get_test_data()
    result = timeit.timeit(lambda: main(test_data), number=1)
