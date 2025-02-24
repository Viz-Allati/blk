import pytest
from blk.binary.constructor import BlockInfoCon
from . import _test_parse_all


@pytest.mark.parametrize(['bs_hex', 'info'], [
    pytest.param('00 00 00', (None, 0, 0, None), id='empty root'),
    pytest.param('00 c001 00', (None, 192, 0, None), id='params only root'),
    pytest.param('00 00 8002 c002', (None, 0, 256, 320), id='block only root'),
    pytest.param('00 c001 8002 c002', (None, 192, 256, 320), id='mixed root'),
    pytest.param('8101 00 00', (128, 0, 0, None), id='empty non root'),
    pytest.param('8101 c001 00', (128, 192, 0, None), id='params only non root'),
    pytest.param('8101 00 8002 c002', (128, 0, 256, 320), id='block only non root'),
    pytest.param('8101 c001 8002 c002', (128, 192, 256, 320), id='mixed non root'),
])
def test_con(bs_hex, info):
    bs = bytes.fromhex(bs_hex)
    _test_parse_all(BlockInfoCon, bs, info.__eq__)
    assert BlockInfoCon.build(info) == bs
