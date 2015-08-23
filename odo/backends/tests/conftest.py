import os
import shutil
import pytest


@pytest.fixture(scope='session')
def sc():
    pytest.importorskip('pyspark')
    from pyspark import SparkContext
    return SparkContext('local[*]', 'odo')


@pytest.yield_fixture(scope='session')
def sqlctx(sc):
    pytest.importorskip('pyspark')
    from odo.backends.sparksql import HiveContext, SQLContext, SPARK_ONE_TWO

    try:
        yield HiveContext(sc) if not SPARK_ONE_TWO else SQLContext(sc)
    finally:
        dbpath = 'metastore_db'
        logpath = 'derby.log'
        if os.path.exists(dbpath):
            assert os.path.isdir(dbpath)
            shutil.rmtree(dbpath)
        if os.path.exists(logpath):
            assert os.path.isfile(logpath)
            os.remove(logpath)
