from pathlib import Path
import shutil
import typing as t
import itertools as itt
import pytest
from helpers import make_tmppath
from . import (clean_tree, make_ignore,
               is_nm_or_blk, fat_dir_rpaths, slim_dir_rpaths,
               is_blk, bbf_dir_rpaths)

tmppath = make_tmppath(__name__)


def make_tmprespath(rpaths: t.Iterable[str], pred: t.Callable[[Path], bool], prefix: str):
    ignore = make_ignore(pred)
    respath_name = f'{prefix}respath'

    @pytest.fixture(scope='module')
    def tmprespath(tmppath: Path, request):
        respath = request.getfixturevalue(respath_name)
        dst_paths = []
        for rpath in rpaths:
            src = respath / rpath
            dst = tmppath / prefix / rpath
            shutil.copytree(src, dst, ignore=ignore)
            dst_paths.append(dst)

        yield tmppath / prefix

        for path in dst_paths:
            clean_tree(path, pred)

    return tmprespath


tmprespath = make_tmprespath(itt.chain(fat_dir_rpaths, slim_dir_rpaths), is_nm_or_blk, 'cur')
bbf_tmprespath = make_tmprespath(bbf_dir_rpaths, is_blk, 'bbf')
