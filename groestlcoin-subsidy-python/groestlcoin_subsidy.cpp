#include <Python.h>

static const int64_t COIN = 100000000;
static const int64_t minimumSubsidy = 5.0 * COIN;
static const int64_t nGenesisBlockRewardCoin = 1 * COIN;
static const int64_t nPremine = 240640 * COIN;

int64_t static GetBlockSubsidy(int nHeight)
{
    if (nHeight == 0) { return nGenesisBlockRewardCoin; }
    if (nHeight == 1) { return nPremine; }
    
    // Subsidy is reduced by 6% every 10080 blocks, which will occur approximately every 1 week
    int64_t nSubsidy = 512 * COIN;
    int exponent = nHeight / 10080;
    for (int i = 0; i < exponent; i++) {
        nSubsidy = (nSubsidy * 47) / 50;
    }

    return (nSubsidy < minimumSubsidy) ? minimumSubsidy : nSubsidy;
}

int64_t static GetBlockSubsidy120000(int nHeight)
{
    // Subsidy is reduced by 10% every day (1440 blocks)
    int64_t nSubsidy = 250 * COIN;
    int exponent = ((nHeight - 120000) / 1440);
    for (int i = 0; i < exponent; i++) {
        nSubsidy = (nSubsidy * 45) / 50;
    }

    return nSubsidy;
}

int64_t static GetBlockSubsidy150000(int nHeight)
{
    // Subsidy is reduced by 1% every week (10080 blocks)
    int64_t nSubsidy = 25 * COIN;
    int exponent = ((nHeight - 150000) / 10080);
    for (int i = 0; i < exponent; i++) {
        nSubsidy = (nSubsidy * 99) / 100;
    }

    return (nSubsidy < minimumSubsidy) ? minimumSubsidy : nSubsidy;
}

int64_t static GetBlockBaseValue(int nBits, int nHeight)
{
    if (nHeight >= 150000) {
        return GetBlockSubsidy150000(nHeight);
    }

    if (nHeight >= 120000) {
        return GetBlockSubsidy120000(nHeight);
    }

    return GetBlockSubsidy(nHeight);
}

static PyObject *groestlcoin_subsidy_getblockbasevalue(PyObject *self, PyObject *args)
{
    int input_bits;
    int input_height;
    if (!PyArg_ParseTuple(args, "ii", &input_bits, &input_height))
        return NULL;
    long long output = GetBlockBaseValue(input_bits, input_height);
    return Py_BuildValue("L", output);
}

static PyMethodDef groestlcoin_subsidy_methods[] = {
    { "getBlockBaseValue", groestlcoin_subsidy_getblockbasevalue, METH_VARARGS, "Returns the block value" },
    { NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC initgroestlcoin_subsidy(void) {
    (void) Py_InitModule("groestlcoin_subsidy", groestlcoin_subsidy_methods);
}
